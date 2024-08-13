import asyncio
from concurrent.futures import ThreadPoolExecutor
import logging
from math import exp
import traceback
from typing import Optional, Union

from platform.data_processor.handlers.database import MongoDBHandler
from platform.data_processor.models import StockTrade, Config
from polygon.rest import RESTClient
from polygon.websocket import WebSocketClient
from polygon.websocket.models import EquityTrade, EquityQuote


# Add these imports at the top of the file
def sigmoid(x):
    return 1 / (1 + exp(-x))


logger = logging.getLogger(__name__)


class StockQuoteHandler:
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
                logging.error(f"Error processing trade id:{equity_trade.id}\nError: {e}\n{traceback.format_tb()}")
            finally:
                self.api_call_queue.task_done()

    def get_quote(self, ticker) -> EquityQuote:
        quote = self.client.get_last_quote(ticker)
        return quote if quote else EquityQuote(bid_price=0.0, ask_price=0.0)


class StockTradeHandler:
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
                logging.error(f"Error handling message: {e}\n{traceback.format_exc()}")
            finally:
                self.handler_queue.task_done()


class OptionTradeHandler:
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
            # print(traceback.format_exc())
            logger.error(f"Error processing message: {e}\n{traceback.format_exc()}")

    async def run(self):
        """Connects to the Unusual Whales WebSocket API and listens for messages."""

        async with websockets.connect(self.websocket_url) as ws:
            await ws.send(json.dumps({"channel": "option_trades", "msg_type": "join"}))
            async for message in ws:
                await self.handle_message(message)

