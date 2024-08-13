
import asyncio
from concurrent.futures import ThreadPoolExecutor
import json
import logging
from math import exp
import traceback
from typing import Optional, Union

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
import websockets

from platform.data_processor.models import OptionTrade, StockTrade, Config
from polygon.rest import RESTClient
from polygon.websocket import WebSocketClient
from polygon.websocket.models import EquityTrade, EquityQuote


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

