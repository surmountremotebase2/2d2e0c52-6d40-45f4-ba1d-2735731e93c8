from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log
from surmount.data import Asset

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the stock ticker you want to trade.
        self.ticker = "AAPL"

    @property
    def assets(self):
        # Specify which assets this strategy pertains to.
        return [self.ticker]

    @property
    def interval(self):
        # Set the data interval. For this strategy, we're using daily data.
        return "1day"

    def run(self, data):
        # Initialize the allocation for the ticker to 0
        # (i.e., do not hold the stock by default)
        allocation_percentage = 0

        # Retrieve the OHLCV (Open-High-Low-Close-Volume) data for the specified ticker
        d = data["ohlcv"]

        if len(d) > 1:  # Ensure we have at least two days of data to compare
            prev_close = d[-2][self.ticker]["close"]  # Previous day's close price
            curr_close = d[-1][self.ticker]["close"]  # Current day's close price

            # Calculate the percentage dip from the previous close to the current close
            percentage_dip = (prev_close - curr_close) / prev_close * 100

            # If the stock has dipped 2% or more, set allocation to 1
            # (i.e., buy and hold the stock)
            if percentage_dip >= 2:
                allocation_percentage = 1

        # Return the target allocation as a TargetAllocation object. 
        # It takes a dictionary with the ticker as key and the allocation percentage as value.
        return TargetAllocation({self.ticker: allocation_percentage})