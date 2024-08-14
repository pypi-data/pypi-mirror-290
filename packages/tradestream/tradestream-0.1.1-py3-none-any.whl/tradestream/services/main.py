"""
This module contains the main application for streaming trades from Polygon and Unusual Whales APIs.

It sets up logging, initializes the necessary handlers, and runs the main application loop.
"""
import asyncio
import logging

from polygon.websocket import WebSocketClient
from polygon.websocket.models import Market, Feed

from tradestream.api import EquityTradeHandler, OptionOrderFlowHandler, MongoDBHandler, QuoteHandler
from tradestream.models import Config


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


class TradesStreamApp:
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
        try:
            await asyncio.gather(
                self.order_flow_handler.run(),
                self.polygon_websocket_client.connect(self.equity_trade_handler.add),
                self.equity_trade_handler.run(),
                self.quote_handler.start_processing_api_calls(),
            )
        except Exception as e:
            logging.error(f"Error in event stream: {e}")


async def main():
    """
    Main entry point for the application.

    This function creates an instance of TradesStreamApp and runs it.
    """
    websocket_subscriptions:list[str] = []
    config = Config()
    websocket_subscriptions.append("T.*")
    """Websocket Subscriptions
    only collect quotes and aggregated minute bars 
    for tickers found in the config file. The name
    of the property is equity_watchlist, which is a list
    of strings, where each string is a ticker symbol.
    
    Feel free to modify the watchlist as you see fit for
    your own personal trading strategy.
    
    The symbols are appended to the websocket_subscriptions list
    twice. Once to collect all changes to the top of the book,
    and once to collect ohlcv data for the ticker by minute.
    """
    watchlist = config.equity_watchlist
    if watchlist:
        for sym in watchlist:
            watchlist_length: int = len(config.watchlist)
            counter:int = 0
        if watchlist_length > 0:
            logger.info(
                f"""
                    {watchlist_length - counter} tickers remaining.
                    Subscribing to trades, quotes, and aggregate minute bars for {sym}.
                """)
            print(f"Subscribing to trades, quotes, and aggregate minute bars for {sym}.")
            websocket_subscriptions.append(f"Q.{sym}")
            websocket_subscriptions.append(f"AM.{sym}")
            counter += 1
            logger.info(f"{sym} subscribed to quote, aggregate minute, and trade websocket channels.")
            print(f"{sym} subscribed to quote, aggregate minute, and trade websocket channels.")
        else:
            logger.error("No tickers found in the configuration file.")
    app = TradesStreamApp(
        config,
        feed=Feed.RealTime,
        market=Market.Stocks,
        subscriptions=websocket_subscriptions
    )
    logger.info(f"Starting trade stream for {len(websocket_subscriptions)} tickers.")
    await app.run()

def start_daemon():
    print("starting daemon")
    asyncio.run(main())

def stop_daemon():
    print("stopping daemon")
    print("daemon stopped")
    pass
    
if __name__ == "__main__":
    asyncio.run(main())
