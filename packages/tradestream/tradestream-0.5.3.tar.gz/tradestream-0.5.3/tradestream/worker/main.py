"""
This module contains the main application for streaming trades from Polygon and Unusual Whales APIs.

It sets up logging, initializes the necessary handlers, and runs the main application loop.
"""
import asyncio

from polygon.websocket import WebSocketClient
from polygon.websocket.models import Market, Feed

from tradestream.worker.api import EquityTradeHandler, OptionOrderFlowHandler, MongoDBHandler, QuoteHandler

from tradestream.worker.models import Config

app = None

class TradesStreamApp:
    global app
    """ 
    Main application class for streaming trades from Polygon and Unusual Whales APIs.

    This class initializes the necessary handlers and provides a method to run the application.

    Attributes:
        config (Config): Configuration object loaded from the config file.
        db_handler (MongoDBHandler): Handler for MongoDB operations.
        order_flow_handler (OptionOrderFlowHandler): Handler for Unusual Whales API.
        equity_trade_handler (EquityTradeHandler): Handler for Polygon API.
    """

    def __init__(self, config: Config, feed, market, subscriptions):
        """
        Initialize the TradesStreamApp.

        Args:
            config (Config): Configuration object initialized by yaml file.
        """
        self.config = config
        self.db_handler = MongoDBHandler(self.config)
        self.order_flow_handler = OptionOrderFlowHandler(self.config, self.db_handler)
        self.quote_handler = QuoteHandler(self.config, self.db_handler)
        self.equity_trade_handler = EquityTradeHandler(self.config, self.db_handler, self.quote_handler)
        self.polygon_websocket_client = WebSocketClient(
            api_key=self.config.polygon_api_key,
            feed=feed,
            market=market,
            verbose=True,
            subscriptions=subscriptions,
        )

    async def run(self):
        """
        Run the main application loop.

        This method starts both the Unusual Whales and Polygon handlers concurrently.
        """
        print("Starting TradeStream Daemon")
        try:
            await asyncio.gather(
                self.order_flow_handler.run(),
                self.polygon_websocket_client.connect(self.equity_trade_handler.add),
                self.equity_trade_handler.run(),
                self.quote_handler.start_processing_api_calls(),
            )
        except Exception as e:
            print(f"Error in event stream: {e}")

    async def stop(self):
        cls_name = self.__name__
        print(f"Stopping TradeStream Daemon: {cls_name}")



async def start_worker():
    """
    Main entry point for the application.
    """
    print("Starting TradeStream Daemon")
    websocket_subscriptions:list[str] = []
    config = Config()
    websocket_subscriptions.append("T.*")
    watchlist = config.equity_watchlist
    if watchlist:
        for sym in watchlist:
            # websocket_subscriptions.append(f"Q.{sym}")
            # websocket_subscriptions.append(f"AM.{sym}")
            print(f"Subscribing to trades, quotes, and aggregate minute bars for {sym}.")
    app = TradesStreamApp(
        config,
        feed=Feed.RealTime,
        market=Market.Stocks,
        subscriptions=websocket_subscriptions
    )
    await app.run()

async def stop_worker():
    await app.stop()


def start():
    asyncio.run(start_worker())

def stop():
    asyncio.run(stop_worker())
    
if __name__ == "__main__":
    asyncio.run(start_worker())
