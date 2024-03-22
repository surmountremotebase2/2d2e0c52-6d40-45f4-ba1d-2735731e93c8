from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, EMA, SMA, MACD, MFI, BB
from surmount.logging import log
from surmount.data import Asset

class TradingStrategy(Strategy):
    def __init__(self):
        # List of tickers for the stocks you want to monitor
        self.tickers = ["AAPL", "GOOGL", "MSFT", "AMZN"]

    @property
    def interval(self):
        # Defines the interval at which the strategy runs. 
        # '1day' means the strategy evaluates once a day.
        return "1day"

    @property
    def assets(self):
        # Returning the list of tickers that this strategy will operate on.
        return self.tickers

    def run(self, data):
        allocation_dict = {}
        for ticker in self.tickers:
            # For each stock ticker, check if there is enough historical data to compare.
            if len(data["ohlcv"]) > 1:
                # Retrieves the closing prices for the last two days.
                prev_close = data["ohlcv"][-2][ticker]['close']
                today_close = data["ohlcv"][-1][ticker]['close']
                
                # Calculates the percentage change between the two days.
                change_percentage = ((today_close - prev_close) / prev_close) * 100
                
                # If the stock's value has dipped more than 2%, allocate funds to buy it.
                # Otherwise, do not allocate any funds to it by setting its value to 0.
                if change_percentage < -2:
                    allocation_dict[ticker] = 1 / len(self.tickers)
                else:
                    allocation_dict[ticker] = 0
            else:
                # If there's not enough data, allocate nothing for safety.
                allocation_dict[ticker] = 0
                
        # Returns a TargetAllocation object based on the calculated allocations.
        # The allocations determine the proportion of the portfolio to invest in each asset.
        return TargetAllocation(allocation_dict)