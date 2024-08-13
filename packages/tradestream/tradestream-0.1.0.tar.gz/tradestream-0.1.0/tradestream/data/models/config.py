import yaml


class Config:
    """
    Configuration class to load the config file and store the configuration values.
    """

    def __init__(self, config_path: str):
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
            self.unusual_whales_api_key = self.config['unusual_whales_api_key']
            self.polygon_api_key = self.config['polygon_api_key']
            self.mongo_uri = self.config['mongo_uri']
            self.mongo_db_name = self.config['mongo_db_name']
            self.equity_watchlist = self.config['equity_watchlist']

