import asyncio
import os
import redis

from dotenv_vault import load_dotenv
from polygon.websocket import WebSocketClient
from polygon.websocket.models import Market, Feed
from rq import Worker, Queue, Connection

from tradestream.worker.api import EquityTradeHandler, OptionOrderFlowHandler, MongoDBHandler, QuoteHandler
from tradestream.worker.models import Config

# using dot_env vault
load_dotenv()

class WorkerService:

    """
    Main application class for streaming trades from Polygon and Unusual Whales APIs.

    This class initializes all necessary components, including Redis connection,
    database handler, and various data handlers for processing trades, quotes,
    and option order flow. It also sets up the Polygon WebSocket client for
    real-time data streaming.

    Attributes:
        config (Config): Configuration object containing app settings.
        redis_channels (list): List of Redis channels for job queues.
        redis_url (str): URL for Redis connection.
        redis_connection (redis.Redis): Redis connection object.
        db_handler (MongoDBHandler): Handler for MongoDB operations.
        order_flow_handler (OptionOrderFlowHandler): Handler for option order flow data.
        quote_handler (QuoteHandler): Handler for quote data.
        trade_handler (EquityTradeHandler): Handler for equity trade data.
        polygon_channels (list): List of Polygon WebSocket channels to subscribe to.
        polygon_feed (Feed): Polygon feed type (RealTime).
        polygon_market (Market): Polygon market type (Stocks).
        polygon_websocket_client (WebSocketClient): Polygon WebSocket client.
    """

    def __init__(self):
        self.config = Config()
        self.redis_channels = ["high", "default", "low"]
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        self.redis_connection = redis.from_url(self.redis_url)
        self.db_handler = MongoDBHandler(self.config)
        self.order_flow_handler = OptionOrderFlowHandler(self.config, self.db_handler)
        self.quote_handler = QuoteHandler(self.config, self.db_handler)
        self.trade_handler = EquityTradeHandler(self.config, self.db_handler, self.quote_handler)
        self.start_worker_queue()
        self.setup_websocket_client()

    def start_worker_queue(self) -> None:
        """
        Initializes and starts the Redis worker queue.

        This method sets up a Redis worker that listens to the specified channels
        ('high', 'default', 'low') for incoming jobs. The worker is configured
        to use the Redis connection established during the class initialization.

        The method doesn't return anything but sets up the worker as an instance
        variable, which is then started in the context of the Redis connection.

        Note: This method is called in the __init__ method of the WorkerService class.
        """
        with Connection(self.redis_connection):
            print(f"Redis worker starting with channels: {', '.join(self.redis_channels)}")
            self.worker = Worker(map(Queue, self.redis_channels))
            self.worker.work()


    def setup_websocket_client(self) -> None:
        """
        Sets up the Polygon WebSocket client for real-time data streaming.

        This method initializes the Polygon WebSocket client with the necessary
        configurations. It sets up the channels to subscribe to, including trades
        for all symbols ('T.*') and aggregated minute data ('AM') and quotes ('Q')
        for specific symbols in the equity watchlist.

        The method configures:
        - Polygon channels: List of channels to subscribe to.
        - Polygon feed: Set to RealTime for live data.
        - Polygon market: Set to Stocks for equity market data.
        - Polygon WebSocket client: Initialized with API key, feed, market, and subscriptions.

        Note: This method is called in the __init__ method of the WorkerService class.
        """
        self.polygon_channels:list[str] = []
        self.polygon_channels.append("T.*")
        for symbol in self.config.equity_watchlist:
            print(f"{symbol} added to your watchlist")
            self.polygon_channels.append("AM.{symbol}")
            self.polygon_channels.append("Q.{symbol}")
        self.polygon_feed = Feed.RealTime
        self.polygon_market = Market.Stocks
        self.polygon_websocket_client = WebSocketClient(
            api_key=self.config.polygon_api_key,
            feed=Feed.RealTime,
            market=Market.Stocks,
            subscriptions=self.polygon_channels,
        )

    async def run(self) -> None:
        """
        Main execution method for the WorkerService.

        This asynchronous method orchestrates the core functionality of the application:
        - Starts the order flow handler to process incoming orders.
        - Connects to the Polygon WebSocket client and sets up the trade handler.
        - Initiates the trade handler to process incoming trade data.
        - Begins processing API calls in the quote handler.

        The method uses asyncio.gather to run these tasks concurrently. If any
        exception occurs during execution, it will be caught and printed.

        Returns:
            None

        Raises:
            Exception: Prints any exception that occurs during the execution of the tasks.
        """
        try:
            await asyncio.gather(
                # self.order_flow_handler.run(),
                self.polygon_websocket_client.connect(self.trade_handler.add),
                self.trade_handler.run(),
                self.quote_handler.start_processing_api_calls(),
            )
        except Exception as e:
            print(f"Error in event stream: {e}")

# initialize a new instance of WorkerService
app = WorkerService()

async def run_service():
    await app.run()

def start():
    asyncio.run(run_service())

if __name__ == "__main__":
    asyncio.run(run_service())
