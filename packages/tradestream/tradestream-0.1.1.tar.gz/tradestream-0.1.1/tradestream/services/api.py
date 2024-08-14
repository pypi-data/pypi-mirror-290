import asyncio
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import json
import logging
import traceback
from typing import Optional, Union

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from polygon.rest import RESTClient
from polygon.websocket import WebSocketClient
from polygon.websocket.models import EquityTrade, EquityQuote
import websockets

from models import OptionTrade, StockTrade, Config


config = Config()

equity_trade_error_file = open(config.log_dir / f"stock_trade_log_{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.log", "w")
option_trade_error_file = open(config.log_dir / f"option_trade_log_{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.log", "w")
quote_error_file = open(config.log_dir / f"stock_quote_log_{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.log", "w")

logger = logging.getLogger(__name__)

class MongoDBHandler:
    """Handles MongoDB operations for saving market data."""

    def __init__(self, config: Config):
        self.client: AsyncIOMotorClient = AsyncIOMotorClient(config.mongo_uri)
        self.db: AsyncIOMotorDatabase = self.client[config.mongo_db_name]
        self.option_trades_collection: AsyncIOMotorCollection = self.db['option_trades']
        self.stock_trades_collection: AsyncIOMotorCollection = self.db['stock_trades']

    async def save_option_trade(self, trade: OptionTrade):
        """Saves an option trade to the database."""
        await self.option_trades_collection.insert_one(trade.to_dict())

    async def save_stock_trade(self, trade: StockTrade):
        """Saves a stock trade to the database."""
        await self.stock_trades_collection.insert_one(trade.to_dict())


class OptionOrderFlowHandler:
    """Handles WebSocket connections and messages from Unusual Whales API."""

    def __init__(self, config: Config, db_handler: MongoDBHandler):
        self.api_key = config.unusual_whales_api_key
        self.db_handler = db_handler
        self.websocket_url = f"wss://api.unusualwhales.com/socket?token={self.api_key}"

    async def handle_message(self, message: str):
        """Processes incoming WebSocket messages."""
        try:
            msg = json.loads(message)
            channel, payload = msg
            if channel == "option_trades":
                option_trade = OptionTrade.from_dict(payload)
                await self.db_handler.save_option_trade(option_trade)
        except Exception as e:
            option_trade_error_file.write(f"Error processing message: {e}\n{message}")
            logger.info(f"Error processing message: {e}\n{traceback.format_exc()}")
            
    async def run(self):
        """Connects to the Unusual Whales WebSocket API and listens for messages."""

        async with websockets.connect(self.websocket_url) as ws:
            await ws.send(json.dumps({"channel": "option_trades", "msg_type": "join"}))
            async for message in ws:
                await self.handle_message(message)


class QuoteHandler:
    """Handles the API calls for getting the last quote for a given stock symbol."""

    def __init__(self, config: Config, db_handler: MongoDBHandler):
        self.api_call_queue = asyncio.Queue()
        self.executor = ThreadPoolExecutor()  # Thread pool for running synchronous code
        self.db_handler = db_handler
        self.config = config
        self.client = RESTClient(self.config.polygon_api_key)

    async def enqueue_api_call(self, equity_trade: EquityTrade):
        await self.api_call_queue.put(equity_trade)

    async def start_processing_api_calls(self):
        while True:
            equity_trade = await self.api_call_queue.get()
            try:
                quote = await asyncio.get_running_loop().run_in_executor(
                    self.executor, self.get_quote, equity_trade.symbol
                )
                stock_trade = StockTrade.from_equity_trade(equity_trade, quote)
                await self.db_handler.save_stock_trade(stock_trade)
                
            except Exception as e:
                equity_trade_error_file.write(f"{traceback.format_stack}")
                logging.info(f"Error: {e}")
                continue
            finally:
                self.api_call_queue.task_done()

    def get_quote(self, ticker) -> EquityQuote:
        try:
            quote = self.client.get_last_quote(ticker)
            return quote if quote else EquityQuote(bid_price=0.0, ask_price=0.0)
        except Exception as e:
            quote_error_file.write(f"{traceback.format_stack}")
            logging.error(f"Error: {e}")
            return EquityQuote(bid_price=0.0, ask_price=0.0)


class EquityTradeHandler:
    """Handles WebSocket connections and messages from Polygon API."""

    def __init__(self, config: Config, db_handler: MongoDBHandler, quote_handler: QuoteHandler):
        self.api_key = config.polygon_api_key
        self.db_handler = db_handler        
        self.websocket_client = WebSocketClient(api_key=self.api_key, subscriptions=["T.*"])
        self.handler_queue = asyncio.Queue()
        self.quote_handler = quote_handler

    async def add(self, message_response: Optional[Union[str, bytes]]) -> None:
        await self.handler_queue.put(message_response)

    async def run(self) -> None:
        while True:
            message_response = await self.handler_queue.get()
            try:
                for trade in message_response:
                        asyncio.create_task(
                            self.quote_handler.enqueue_api_call(trade)
                        )
            except Exception as e:
                equity_trade_error_file.write(f"Error handling message: {e}\n{traceback.format_stack}")
                logging.error(f"Error handling message: {e}\n{traceback.format_stack()}")
            finally:
                self.handler_queue.task_done()
