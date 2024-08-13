
from math import exp


class TradeMixin:

    def sigmoid(self, x):
        return 1 / (1 + exp(-x))

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
        spread = self.ask_price - self.bid_price
        mid_price = (self.ask_price + self.bid_price) / 2
        relative_spread = spread / mid_price if mid_price != 0 else 0
        spread_factor = self.sigmoid(relative_spread * 10) * 2 - 1  # Transforms to [-1, 1]

        # Size factor (assumes self.size exists)
        size_factor = self.sigmoid(self.size / 1000) * 2 - 1  # Transforms to [-1, 1]

        # Combine factors
        raw_score = base_score * (1 + spread_factor * 0.3 + size_factor * 0.5)

        # Normalize to [-1, 1]
        self.bull_bear = max(min(raw_score, 1.0), -1.0)

        # Adjust for option type if applicable
        if hasattr(self, 'option_type'):
            if self.option_type.lower() == 'put':
                self.bull_bear *= -1


class OptionTrade(TradeMixin):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sigmoid = self.sigmoid

    def calculate_bull_bear(self):
        super().calculate_bull_bear()
        
        # Additional option-specific factors
        iv_factor = self.sigmoid(self.implied_volatility * 10) * 2 - 1  # Transforms to [-1, 1]
        delta_factor = self.delta * 2 - 1  # Delta is already in [0, 1], transform to [-1, 1]
        
        # Combine with existing score
        self.bull_bear = (self.bull_bear + iv_factor * 0.2 + delta_factor * 0.3) / 1.5
        
        # Normalize again
        self.bull_bear = max(min(self.bull_bear, 1.0), -1.0)


class StockTrade(TradeMixin):
    # ... (other methods remain the same)

    def calculate_bull_bear(self):
        super().calculate_bull_bear()
        # Additional stock-specific factors
        volume_factor = super().sigmoid(self.volume / 100000) * 2 - 1  # Transforms to [-1, 1]
        self.bull_bear = (self.bull_bear + volume_factor * 0.2) / 1.2
        
        # Normalize again
        self.bull_bear = max(min(self.bull_bear, 1.0), -1.0)
