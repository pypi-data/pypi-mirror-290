from dataclasses import dataclass, field, asdict
from datetime import datetime, date
import math
import os
from typing import Dict, Any, List, Literal, Union
from enum import StrEnum
from bson import ObjectId
from polygon.websocket.models import EquityTrade, EquityQuote
import yaml


TradeSide = Literal["above_ask", "at_ask", "near_ask", "mid", "near_bid", "at_bid", "below_bid"]

class OrderSide(StrEnum):
    ABOVE_ASK = "ABOVE_ASK"
    AT_ASK = "AT_ASK"
    NEAR_ASK = "NEAR_ASK"
    NO_SIDE = "NO_SIDE"
    NEAR_BID = "NEAR_BID"
    AT_BID = "AT_BID"
    BELOW_BID = "BELOW_BID"

BULLBEAR_SIDE_FACTORS = {
    "ABOVE_ASK": 1.0,
    "AT_ASK": 0.65,
    "NEAR_ASK": 0.25,
    "NO_SIDE": 0,
    "NEAR_BID": -0.25,
    "AT_BID": -0.65,
    "BELOW_BID": -1,
}

TRADE_SIZE_FACTORS = {
    "X_LARGE": 1.0,
    "LARGE": 0.849,
    "MEDIUM": 0.349,
    "SMALL": 0.1499,
    "MICRO": 0.0099,
}

EXPIRY_TIMEFRAME_CLASS_FACTORS = {
    "0dtx": 1.0,
    "1_7dtx": 0.80,
    "7_14dtx": 0.65,
    "14_30dtx": 0.33,
    "30_90dtx": 0.21,
    "90_365dtx": 0.10,
    "365_plus": 0.033,
}


@dataclass
class Config:
    """Configuration class to load the config file and store the configuration values."""
    def __init__(self) -> None:
        self.config_path = "./tradestream/worker/config.yml"
        with open(self.config_path, "r") as file:
            self.config:Dict[str, Any] = yaml.safe_load(file)

        self.unusualwhales_api_key: Union[str, None] = os.getenv("UNUSUALWHALES_API_KEY", None)
        self.polygon_api_key: Union[str, None] = os.getenv("POLYGON_API_KEY", None)
        self.fmp_api_key: Union[str, None] = os.getenv("FMP_API_KEY", None)
        self.databento_api_key: Union[str, None] = os.getenv("DATABENTO_API_KEY", None)
        self.mongo_uri: Union[str, None] = os.getenv("MONGO_URI", None)
        self.mongo_db_name: Union[str, None] = os.getenv("MONGO_DB_NAME", None)
        self.option_trade_collection: str = "option_trades"
        self.stock_trade_collection: str = "stock_trades"
        self.order_flow_report_collection: str = "flow_reports"
        self.option_chain_collection: str = "option_chains"
        self.equity_symbol_collection: str = "equity_symbols"
        self.trading_plan_collection: str = "trading_plans"
        self.user_collection: str = "users"
        self.subscription_plan_collection: str = "subscription_plans"
        self.customer_collection: str = "customers"
        self.customer_order_collection: str = "customer_orders"
        self.custom_report_collection: str = "custom_reports"
        self.trading_journal_collection: str = "trading_journals"
        self.equity_watchlist:List[str] = self.config["equity_watchlist"] or []
        self.index_watchlist:List[str] = self.config["index_watchlist"] or []
        self.futures_watchlist:List[str] = self.config["futures_watchlist"] or []
        self.currency_watchlist:List[str] = self.config["currency_watchlist"] or []
        self.stock_trading_symbols:List[str] = self.config["stock_trading_symbols"] or []
        self.option_trading_symbols:List[str] = self.config["option_trading_symbols"] or []
        self.news_api:str = self.config["news_api"] or None
        self.x_large_stk_trade:int = self.config["x_large_stk_trade"] or None
        self.large_stk_trade:int = self.config["large_stk_trade"] or None
        self.medium_stk_trade:int = self.config["medium_stk_trade"] or None
        self.small_stk_trade:int = self.config["small_stk_trade"] or None
        self.micro_stk_trade:int = self.config["micro_stk_trade"] or None
        self.x_large_opt_trade:int = self.config["x_large_opt_trade"] or None
        self.large_opt_trade:int = self.config["large_opt_trade"] or None
        self.medium_opt_trade:int = self.config["medium_opt_trade"] or None
        self.small_opt_trade:int = self.config["small_opt_trade"] or None
        self.micro_opt_trade:int = self.config["micro_opt_trade"] or None
        # if self.unusualwhales_api_key is None:
        #     raise ValueError("UNUSUALWHALES_API_KEY is not set")
        # if self.polygon_api_key is None:
        #     raise ValueError("POLYGON_API_KEY is not set")
        # if self.fmp_api_key is None:
        #     raise ValueError("FMP_API_KEY is not set")
        # if self.databento_api_key is None:
        #     raise ValueError("DATABENTO_API_KEY is not set")

class TradeMixin:

    def sigmoid(self, x: float) -> float:
        return 1 / (1 + math.exp(-x))
    
    def calculate_bull_bear(self):
        # Base score from trade side
        side_scores = {
            "above_ask": 1.0,
            "at_ask": 0.75,
            "near_ask": 0.25,
            "mid": 0.0,
            "near_bid":-0.25,
            "at_bid":-0.75,
            "below_bid":-1.0
        }
        base_score = side_scores.get(self.side, 0.0)

        # Adjust for spread
        self.spread = self.ask_price - self.bid_price
        mid_price = (self.ask_price + self.bid_price) / 2
        relative_spread = self.spread / mid_price if mid_price != 0 else 0
        spread_factor = self.sigmoid(relative_spread * 10) * 2 - 1  # Transforms to [-1, 1]

        # Size factor (assumes self.size exists)
        size_factor = self.sigmoid(self.size / 1000) * 2 - 1  # Transforms to [-1, 1]

        # Combine factors
        raw_score = base_score * (1 + spread_factor * 0.3 + size_factor * 0.5)

        # Normalize to [-1, 1]
        self.bull_bear = max(min(raw_score, 1.0), -1.0)

        # Adjust for option type if applicable
        if hasattr(self, "option_type"):
            if self.option_type.lower() == "call":
                if self.side in ["below_bid", "near_bid", "at_bid"]:
                    self.bull_bear *= -1
                else:
                    self.bull_bear *= 1
            else: 
                if self.side in ["below_bid", "near_bid", "at_bid"]:
                    self.bull_bear *= 1
                else:
                    self.bull_bear *= -1

@dataclass
class OptionTrade(TradeMixin):
    """OptionTrade dataclass to store the data of an option trade.

    Returns:
        _type_: This dataclass is used to store the data of an option trade.
    """
    record_id: str  # unique identifier for the trade
    underlying_symbol: str  # symbol of the underlying asset
    executed_at: datetime  # time when the trade was executed
    created_at: datetime  # time when the trade was created
    expiry: datetime  # expiry date of the option
    bid_price: float # national best bid price
    ask_price: float# national best ask price
    size: int # size of the trade
    price: float # price of the trade
    option_symbol: str # symbol of the option
    tags: List[str]  # list of tags
    option_type: str
    open_interest: int # open interest of the option
    strike: float # strike price of the option
    premium: float  # premium of the option
    volume: int  # volume of the trade
    underlying_price: float  # price of the underlying asset
    ewma_nbbo_ask: float  # exponential weighted moving average of the national best ask price
    ewma_nbbo_bid: float  # exponential weighted moving average of the national best bid price
    implied_volatility: float = 0.0 # implied volatility of the option
    delta: float = 0.0 # delta of the option
    theta: float = 0.0 # theta of the option
    gamma: float = 0.0 # gamma of the option
    vega: float = 0.0  # vega of the option
    rho: float  = 0.0 # rho of the option
    theo: float  = 0.0 # theoretical price of the option
    trade_code: str  = ""# trade code
    exchange: str  = "unknown" # exchange where the trade was executed
    ask_vol: int = 0  # ask volume
    bid_vol: int = 0  # bid volume
    no_side_vol: int = 0  # volume with no side
    mid_vol: int = 0 # mid volume
    multi_vol: int = 0  # multi volume
    stock_multi_vol: int = 0  # stock multi volume
    sentiment: str  = "unknown" # sentiment of the trade (bullish/bearish/neutral)
    is_earnings_week: bool = False # whether the option expires in earnings week
    days_to_expiry: int = 0 # days to expiry of the option
    market_hours: str = "unknown" # market time of the trade (pre_market/market_hours/post_market/after_hours)
    size_class: str = "unknown" # size class of the trade (tiny/small/medium/large/whale)
    days_to_expiry_class: str = "unknown" # days to expiry class of the option (expires_today/this_week/next_week/this_month/in_3_months/this_year/next_year/leap)
    bull_bear: float = 0.0# bull bear score of the trade
    side: str = "mid"# side of the trade (above_ask/at_ask/near_ask/mid/near_bid/at_bid/below_bid)
    spread: float = 0.0 # spread of the trade
    report_flags: List[str]  = field(default_factory=List[str]) # list of report flags
    _id: ObjectId = field(default_factory=ObjectId)  # unique identifier for the trade
        
    @staticmethod
    def from_dict(obj: Dict[str, Any]) -> "OptionTrade":
        """initializes an OptionTrade object from a dictionary
        Args:
            obj (Dict[str, Any]): dict containing the data of the option trade from unusual whales

        Returns:
            OptionTrade: The OptionTrade object initialized with the data from the dictionary
        """
        executed_at = datetime.fromtimestamp(float(obj.get("executed_at", 0)) / 1000)
        created_at = datetime.fromtimestamp(float(obj.get("created_at", 0)) / 1000)
        expiry = datetime.strptime(str(obj.get("expiry", "")), "%Y-%m-%d")
        days_to_expiry = (expiry.date() - executed_at.date()).days
        tags = obj.get("tags", [])
        sentiment = "bullish" if "bullish" in tags else "bearish" if "bearish" in tags else "neutral"
        market_hours = OptionTrade.determine_market_hours(executed_at)
        size_class = OptionTrade.determine_size_class(int(obj.get("size", 0)))
        days_to_expiry_class = OptionTrade.determine_days_to_expiry_class(days_to_expiry)
        option_trade = OptionTrade(
            record_id=obj.get("id", ""),
            underlying_symbol=obj.get("underlying_symbol", ""),
            executed_at=executed_at,
            created_at=created_at,
            expiry=expiry,
            bid_price=float(obj.get("nbbo_bid", 0.0) or 0.0),
            ask_price=float(obj.get("nbbo_ask", 0.0) or 0.0),
            size=int(obj.get("size", 0) or 0),
            price=float(obj.get("price", 0.0) or 0.0),
            option_symbol=obj.get("option_symbol", ""),
            report_flags=obj.get("report_flags", []),
            tags=tags,
            option_type=obj.get("option_type", ""),
            open_interest=int(obj.get("open_interest", 0) or 0),
            strike=float(obj.get("strike", 0.0) or 0.0),
            premium=float(obj.get("premium", 0.0) or 0.0),
            volume=int(obj.get("volume", 0) or 0),
            underlying_price=float(obj.get("underlying_price", 0.0) or 0.0),
            ewma_nbbo_ask=float(obj.get("ewma_nbbo_ask", 0.0) or 0.0),
            ewma_nbbo_bid=float(obj.get("ewma_nbbo_bid", 0.0) or 0.0),
            implied_volatility=float(obj.get("implied_volatility", 0.0) or 0.0),
            delta=float(obj.get("delta", 0.0) or 0.0),
            theta=float(obj.get("theta", 0.0) or 0.0),
            gamma=float(obj.get("gamma", 0.0) or 0.0),
            vega=float(obj.get("vega", 0.0) or 0.0),
            rho=float(obj.get("rho", 0.0) or 0.0),
            theo=float(obj.get("theo", 0.0) or 0.0),
            trade_code=obj.get("trade_code", ""),
            exchange=obj.get("exchange", ""),
            ask_vol=int(obj.get("ask_vol", 0) or 0),
            bid_vol=int(obj.get("bid_vol", 0) or 0),
            no_side_vol=int(obj.get("no_side_vol", 0) or 0),
            mid_vol=int(obj.get("mid_vol", 0) or 0),
            multi_vol=int(obj.get("multi_vol", 0) or 0),
            stock_multi_vol=int(obj.get("stock_multi_vol", 0) or 0),
            sentiment=sentiment,
            is_earnings_week="earnings_this_week" in tags,
            days_to_expiry=days_to_expiry,
            market_hours=market_hours,
            size_class=size_class,
            days_to_expiry_class=days_to_expiry_class,
            spread=float(obj.get("spread", 0.0) or 0.0),
            bull_bear=0.0,
            side="mid",
        )
        option_trade.determine_side()
        option_trade.calculate_score()
        return option_trade

    def calculate_score(self):
        self.calculate_bull_bear()
        
        # Additional option-specific factors
        iv_factor = self.sigmoid(self.implied_volatility * 10) * 2 - 1  # Transforms to [-1, 1]
        delta_factor = self.delta * 2 - 1  # Delta is already in [0, 1], transform to [-1, 1]
        
        # Combine with existing score
        self.bull_bear = (self.bull_bear + iv_factor * 0.2 + delta_factor * 0.3) / 1.5
        
        # Normalize again
        self.bull_bear = max(min(self.bull_bear, 1.0), -1.0)

    def determine_side(self):
        """
        Determines the side of the trade based on the price, NBBO bid and ask prices.
        """
        self.spread = self.ask_price - self.bid_price
        near_threshold = self.spread * 0.25

        if self.price > self.ask_price:
            self.side = "above_ask"
        elif self.price < self.bid_price:
            self.side = "below_bid"
        elif self.price == self.ask_price:
            self.side = "at_ask"
        elif self.price == self.bid_price:
            self.side = "at_bid"
        elif self.ask_price - self.price <= near_threshold:
            self.side = "near_ask"
        elif self.price - self.bid_price <= near_threshold:
            self.side = "near_bid"
        else:
            self.side = "mid"

    @staticmethod
    def determine_market_hours(executed_at: datetime) -> str:
        r"""\adds the market time of the trade based on the execution time

        Args:
            executed_at (datetime): the time when the trade was executed

        Returns:
            str: market time of the trade (pre_market/market_hours/post_market/after_hours)
        """
        hour, minute = executed_at.hour, executed_at.minute
        if hour < 9 or (hour == 9 and minute < 30):
            return "pre_market"
        elif 9 <= hour < 16 or (hour == 16 and minute == 0):
            return "market_hours"
        elif hour == 16 and 0 < minute < 30:
            return "post_market"
        else:
            return "after_hours"

    @staticmethod
    def determine_size_class(size: int,) -> str:
        """updates the size class of the trade based on the size

        Args:
            size (int): the size of the trade is equal to quantity or volume

        Returns:
            str: a string representing the size class of the trade (tiny/small/medium/large/whale)
        """
        config:Config = Config()
        if size >= config.x_large_opt_trade:
            return "x_large"
        elif size >= config.large_opt_trade:
            return "large"
        elif size >= config.medium_opt_trade:
            return "medium"
        elif size >= config.small_opt_trade:
            return "small"
        else:
            return "tiny"

    @staticmethod
    def determine_days_to_expiry_class(days_to_expiry: int,) -> str:
        """determine the days to expiry class based on the number of days to expiry

        Args:
            days_to_expiry (int): integer of the number of days to expiry

        Returns:
            str: a string representing the days to expiry class of the option
        """
        if days_to_expiry <= 0:
            return "0_dtx"
        elif days_to_expiry <= 7:
            return "1_7dtx"
        elif days_to_expiry <= 14:
            return "7_14dtx"
        elif days_to_expiry <= 30:
            return "14_30dtx"
        elif days_to_expiry <= 90:
            return "30_90dtx"
        elif days_to_expiry <= 365:
            return "90_365dtx"
        else:
            return "365_plus"


    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dictionary
        """
        return {k: str(v) if isinstance(v, (datetime, date, ObjectId)) else v for k, v in asdict(self).items()}

@dataclass
class StockTrade(TradeMixin):
    """
    StockTrade dataclass to store the data of a stock trade.

    Returns:
        _type_: the StockTrade dataclass is used to store the data of a stock trade.
    """
    symbol: str = field(default="")
    exchange: str = field(default="")
    price: float = field(default=0.0)
    size: int = field(default=0)
    timestamp: datetime = field(default=datetime.now())
    conditions: List[int] = field(default_factory=List[int])
    record_id: str = field(default="")
    tape: int = field(default=0)
    bull_bear: float = field(default=0.0)
    side: TradeSide = field(default="mid")
    bid_price: float = field(default=0.0)
    ask_price: float = field(default=0.0)
    spread: float = field(default=0.0)
    is_darkpool_trade: bool = field(default=False)
    trf_id: str = field(default="")
    trf_timestamp: datetime = field(default=datetime.now())
    @staticmethod
    def from_equity_trade(trade: EquityTrade, quote: EquityQuote) -> "StockTrade":
        
        stock_trade = StockTrade(
            symbol=trade.symbol,
            exchange=trade.exchange,
            price=trade.price,
            size=trade.size,
            timestamp=datetime.fromtimestamp(trade.timestamp / 1000) if trade.timestamp else datetime.now(),
            conditions=[int(c) for c in trade.conditions] if trade.conditions else [],
            record_id=trade.id,
            tape=trade.tape,
            bull_bear=0.0,
            side="mid",
            bid_price=quote.bid_price if quote else 0.0,
            ask_price=quote.ask_price if quote else 0.0,
            spread=0.0,
            is_darkpool_trade= trade.exchange == 4 and trade.trf_id != "" and trade.trf_id is not None,
            trf_id = trade.trf_id,
            trf_timestamp = datetime.fromtimestamp(trade.trf_timestamp / 1000) if trade.trf_timestamp else datetime.now(),
        )
        if stock_trade.bid_price > 0.0 and stock_trade.ask_price > 0.0:
            stock_trade.determine_side()
            stock_trade.calculate_bull_bear()
        return stock_trade

    def determine_side(self):
        """Determines the "side" of a trade based on the bid and ask prices.

        Args:
            bid_price (float): national best bid price (NBBO data)
            ask_price (float): national best ask price (NBBO data)
        """
        # spread is the difference between the ask and bid prices
        self.spread = self.ask_price - self.bid_price
        mid_price = (self.ask_price + self.bid_price) / 2
        # error threshold for determining if the price is near the bid or ask
        near_threshold = self.spread * 0.25

        # main logic for determining the side of the trade
        if self.price > self.ask_price:
            self.side = "above_ask"
        elif self.price == self.ask_price:
            self.side = "at_ask"
        elif self.ask_price - self.price <= near_threshold:
            self.side = "near_ask"
        elif abs(self.price - mid_price) <= near_threshold:
            self.side = "mid"
        elif self.price == self.bid_price:
            self.side = "at_bid"
        elif self.price < self.bid_price:
            self.side = "below_bid"
        else:
            self.side = "near_bid"

    # to_dict method converts the object to a dictionary
    def to_dict(self) -> Dict[str, Any]:
        """ Returns the object as a dictionary, 
            converting datetime and ObjectId to strings

        Returns:
            Dict[str, Any]: _description_
        """
        return {k: str(v) if isinstance(v, (datetime, ObjectId)) else v for k, v in asdict(self).items()}
