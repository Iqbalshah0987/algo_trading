import backtrader as bt
from datetime import *

class MovingAverageCrossover(bt.Strategy):
    def __init__(self):
        self.ma50 = bt.indicators.SMA(self.data.close, period=50)
        self.ma200 = bt.indicators.SMA(self.data.close, period=200)

    def next(self):
        if not self.position:  # not in the market
            if self.ma50 > self.ma200:
                self.buy()
        elif self.ma50 < self.ma200:
            self.sell()

# Create a cerebro entity
cerebro = bt.Cerebro()

# Add a strategy
cerebro.addstrategy(MovingAverageCrossover)

# Load data
data = bt.feeds.YahooFinanceData(dataname='AAPL_data.csv',
                                 fromdate=datetime(2015, 1, 1),
                                 todate=datetime(2020, 1, 1))
cerebro.adddata(data)

# Set initial capital
cerebro.broker.setcash(100000.0)

# Run backtest
cerebro.run()

# Plot results
cerebro.plot()
