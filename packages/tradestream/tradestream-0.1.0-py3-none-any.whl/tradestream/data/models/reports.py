from dataclasses import dataclass, field
import enum

import datetime as dt


class ExpiryFilters(enum.StrEnum):
    """
    ExpiryFilters enum to store the expiry filters of a report.
    """
    ALL_EXPIRIES = enum.auto()
    NEAR_TO_EXPIRE_ONLY = enum.auto()
    EXCLUDE_NEAR_TO_EXPIRE = enum.auto()
    LEAPS_ONLY = enum.auto()
    EXCLUDE_LEAPS = enum.auto()

    def __repr__(self) -> str:
        return self.name.lower()

    def __str__(self) -> str:
        return self.name.lower()

    
class SizeFilters(enum.StrEnum):
    """
    SizeFilters enum to store the size filters of a report.
    """
    ALL_SIZES = enum.auto()
    ALL_RETAIL = enum.auto()
    ALL_WHALE = enum.auto()

    def __repr__(self) -> str:
        return self.name.lower()

    def __str__(self) -> str:
        return self.name.lower()


class BidAskFilters(enum.StrEnum):
    BUY_SIDE_ONLY = enum.auto()
    SELL_SIDE_ONLY = enum.auto()
    EXCLUDE_NO_SIDE = enum.auto()

    def __repr__(self) -> str:
        return self.name.lower()

    def __str__(self) -> str:
        return self.name.lower()


class PutCallFilters(enum.StrEnum):
    PUT_ONLY = enum.auto()
    CALL_ONLY = enum.auto()

    def __repr__(self) -> str:
        return self.name.lower()

    def __str__(self) -> str:
        return self.name.lower()


@dataclass
class TechnicalIndicators:
    vwap:float
    vwap_change:float
    vwap_change_percent:float
    five_day_ema:float
    ten_day_ema:float
    thirteen_day_ema:float
    five_day_cross_up:bool
    ten_day_cross_up:bool
    thirteen_day_cross_up:bool
    five_day_cross_down:bool
    ten_day_cross_down:bool
    thirteen_day_cross_down:bool
    rsi:float
    macd:float
    macd_signal:float
    macd_histogram:float
    adx:float
    average_true_range:float


@dataclass
class OrderBookStats:
    """
    OrderBookStats dataclass to store the data of an order book stats.
    """
    offer_orders_added:int
    offer_orders_cancelled:int
    offer_orders_modified:int
    offer_orders_filled:int
    trade_or_fill_count:int
    bid_orders_added:int
    bid_orders_cancelled:int
    bid_orders_modified:int
    buy_orders_filled:int
    best_bid:float
    best_offer:float
    best_bid_size:int
    best_offer_size:int
    total_bid_volume:int
    total_offer_volume:int
    trade_price_up_count:int
    trade_price_down_count:int
    best_offer_change_count:int
    best_offer_price_up_count:int
    best_offer_price_down_count:int
    best_bid_change_count:int
    best_offer_change_count:int
    best_offer_price_up_count:int
    best_offer_price_down_count:int
    bid_orders_at_start:int
    bid_orders_at_end:int
    offer_orders_at_start:int
    offer_orders_at_end:float
    total_buy_volume:int
    total_sell_volume:int
    total_no_side_volume:int
    avg_buy_price:float
    avg_sell_price:float
    avg_no_side_price:float
    no_side_order_count:int


@dataclass
class OrderFlowReport:
    """
    OrderFlowReport dataclass to store the data of an order flow report.
    """
    expiry_filter:ExpiryFilters
    size_filter:SizeFilters
    bid_ask_filter:BidAskFilters
    put_call_filter:PutCallFilters
    volume:int
    prv_volume:int
    volume_change:int
    volume_change_percent:float
    open_interest:int
    prv_open_interest:int
    open_interest_change:int
    open_interest_change_percent:float
    order_count:int
    bullish_order_count:int
    bearish_order_count:int
    no_side_order_count:int
    bullish_volume:int
    bearish_volume:int
    no_side_volume:int
    bullish_volume_percent:float
    bearish_volume_percent:float
    no_side_volume_percent:float
    bullish_premium:float
    bearish_premium:float
    no_side_premium:float
    bullish_premium_percent:float
    bearish_premium_percent:float
    no_side_premium_percent:float
    bull_bear_volume_ratio:float
    bull_bear_order_count_ratio:float
    bull_bear_premium_ratio:float
    put_volume:int
    prv_put_volume:int
    put_volume_change:int
    put_volume_change_percent:float
    put_volume_at_ask:int
    prv_put_volume_at_ask:int
    put_volume_at_ask_change:int
    put_volume_at_bid:int
    prv_put_volume_at_bid:int
    put_volume_at_bid_change:int
    put_volume_at_bid_change_percent:float
    call_volume:int
    prv_call_volume:int
    call_volume_change:int
    call_volume_change_percent:float
    call_volume_at_ask:int
    prv_call_volume_at_ask:int
    call_volume_at_ask_change:int
    call_volume_at_ask_change_percent:float
    call_volume_at_bid:int
    prv_call_volume_at_bid:int
    call_volume_at_bid_change:int
    call_volume_at_bid_change_percent:float
    put_orders_at_ask:int
    prv_put_orders_at_ask:int
    put_orders_at_ask_change:int
    put_orders_at_ask_change_percent:float
    put_orders_at_bid:int
    prv_put_orders_at_bid:int
    put_orders_at_bid_change:int
    put_orders_at_bid_change_percent:float
    call_orders_at_ask:int
    prv_call_orders_at_ask:int
    call_orders_at_ask_change:int
    call_orders_at_ask_change_percent:float
    call_orders_at_bid:int
    prv_call_orders_at_bid:int
    call_orders_at_bid_change:int
    call_orders_at_bid_change_percent:float
    no_side_call_volume:int
    prv_no_side_call_volume:int
    no_side_call_volume_change:int
    no_side_call_volume_change_percent:float
    no_side_put_volume:int
    prv_no_side_put_volume:int
    no_side_put_volume_change:int
    no_side_put_volume_change_percent:float
    no_side_call_volume_at_ask:int
    prv_no_side_call_volume_at_ask:int
    no_side_call_volume_at_ask_change:int
    no_side_call_volume_at_ask_change_percent:float
    no_side_call_volume_at_bid:int
    prv_no_side_call_volume_at_bid:int
    no_side_call_volume_at_bid_change:int
    no_side_call_volume_at_bid_change_percent:float
    no_side_put_volume_at_ask:int
    prv_no_side_put_volume_at_ask:int
    no_side_put_volume_at_ask_change:int
    no_side_put_volume_at_ask_change_percent:float
    no_side_put_volume_at_bid:int
    no_side_call_orders_at_ask:int
    no_side_call_orders_at_bid:int
    no_side_put_orders_at_ask:int
    no_side_put_orders_at_bid:int


@dataclass
class Report:
    """
    Report dataclass to store the data of a aggregate report.
    """
    symbol:str
    report_date:str
    period_start:dt.datetime
    period_end:dt.datetime
    earnings_date:dt.datetime
    days_to_earnings:int
    news_sentiment:float
    news_mentions:int
    social_mentions_sentiment:float
    social_mentions:int
    open:float
    high:float
    low:float
    close:float
    prv_close:float
    change:float
    change_percent:float
    last_price:float
    last_size:int
    last_date:dt.datetime
    last_exchange:str
    volume:int
    prv_volume:int
    volume_change:int
    volume_change_percent:float
    share_float:int
    volume_percent_of_float:float
    order_book_stats:OrderBookStats
    technical_indicators:TechnicalIndicators
    order_flow_report:OrderFlowReport
    
