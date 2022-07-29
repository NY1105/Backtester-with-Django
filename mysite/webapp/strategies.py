from .indicators import EightCurrenciesIndicatorEMA as ECIEMA
from .indicators import EightCurrenciesIndicatorCCY as ECICCY
import backtrader as bt


class StrategyTemplate(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        # print('%s, %s' % (dt.isoformat(), txt))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            elif order.issell():
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))


class TestStrategy(StrategyTemplate):
    params = (
        ('smal_period', 8),
        ('smas_period', 4),
        ('size', 1000),
        ('trailing_perc', 1)
    )

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        # To keep track of pending orders and buy price/commission
        self.order = None
        self.orders = [None, None, None]
        self.buyprice = None
        self.buycomm = None
        self.smal = bt.indicators.MovingAverageSimple(self.datas[0], period=self.params.smal_period)
        self.smas = bt.indicators.MovingAverageSimple(self.datas[0], period=self.params.smas_period)
        self.crossup = bt.ind.CrossUp(self.smas, self.smal)
        '''
        bt.indicators.ExponentialMovingAverage(self.datas[0], period=25)
        bt.indicators.WeightedMovingAverage(self.datas[0], period=25).subplot = True
        bt.indicators.StochasticSlow(self.datas[0])
        bt.indicators.MACDHisto(self.datas[0])
        rsi = bt.indicators.RSI(self.datas[0])
        bt.indicators.SmoothedMovingAverage(rsi, period=10)
        bt.indicators.ATR(self.datas[0]).plot = False
        '''

    def notify_order(self, order):
        if not order.status == order.Completed:
            return
        if not self.position:
            return

        self.sell(size=self.p.size, exectype=bt.Order.StopTrail, trailpercent=0.01)

    def next(self):
        # Simply log the closing price of the series from the reference

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return
        self.log('Close, %.2f' % self.dataclose[0])
        # Check if we are in the market
        if not self.position:
            # Not yet ... we MIGHT BUY if ...
            if self.crossup > 0:  # <--------------------------------------------------------------------------------------------------
                # BUY, BUY, BUY!!! (with default parameters)

                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                # Keep track of the created order to avoid a 2nd order
                order0 = self.buy(size=self.p.size)
                # order1 = self.sell(size=self.p.size, exectype=bt.Order.Limit, price=(self.data.close[0] * (1 + self.p.take_profit)))  # TP
                # order2 = self.sell(size=self.p.size, exectype=bt.Order.Stop, price=(self.data.close[0] * (1 - self.p.stop_loss)),oco=order1)  # SL

                # self.orders[1] = self.buy(exectype=bt.Order.StopLimit, price=self.data.close[0] * 1.02, plimit=self.data.close[0] * 1.07)

        '''
        else:
            # Already in the market ... we might sell
            if self.dataclose[0] < self.sma[0]:  # <--------------------------------------------------------------------------------------------------------
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()
        '''


class ACSStrategy(StrategyTemplate):
    params = (
        ('opt_dict', {}),
        ('smaf_period', 2),
        ('smas_period', 20),
        ('distance', 8),  # <------------------------
        ('size', 1000),  # <---------confidence level
        ('trailing_prc', 1),
        ('price', None)
    )

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        # To keep track of pending orders and buy price/commission
        if self.p.opt_dict:
            for key, value in self.p.opt_dict.items():
                setattr(self.p, key, value)  # self.p.key = value

        self.orders = [None for i in range(len(self.datas))]  # current pending order
        self.acs = ECIEMA(*self.datas[:], smaf_period=self.p.smaf_period, smas_period=self.p.smas_period)
        self.entryprice = None
        self.CCY_PAIRS = (
            "EURUSD", "EURGBP", "EURAUD", "EURCAD",
            "EURCHF", "EURJPY", "EURNZD", "AUDCAD",
            "AUDCHF", "AUDJPY", "AUDNZD", "AUDUSD",
            "CADCHF", "CADJPY", "CHFJPY", "GBPAUD",
            "GBPCAD", "GBPCHF", "GBPJPY", "GBPNZD",
            "GBPUSD", "NZDCAD", "NZDCHF", "NZDJPY",
            "NZDUSD", "USDCAD", "USDCHF", "USDJPY"
        )
        self.currencies = ('AUD', 'CAD', 'CHF', 'EUR', 'GBP', 'JPY', 'NZD', 'USD')
        self.opened = []

    def notify_order(self, order):
        if not order.status == order.Completed:
            return
        size = self.p.size
        if 'JPY' in order.data._name:
            size //= 100
        if order.isbuy():
            self.sell(data=order.data, size=size, exectype=bt.Order.StopTrail, trailpercent=self.p.trailing_prc / 100)
        else:
            self.buy(data=order.data, size=size, exectype=bt.Order.StopTrail, trailpercent=self.p.trailing_prc / 100)
        # , price= (order.data.close[0]*(1-self.p.take_profit))

    def stop(self):
        self.params.price = self.broker.getvalue()

    def next(self):
        self.major = {}
        for i in self.currencies:
            self.major[i] = getattr(self.acs, i)[0]

        high_currency = max(self.major, key=self.major.get)
        low_currency = min(self.major, key=self.major.get)

        symbol_name = ''
        isbuy = True
        if high_currency + low_currency in self.CCY_PAIRS:
            symbol_name = high_currency + low_currency
            isbuy = True
        else:
            symbol_name = low_currency + high_currency
            isbuy = False

        # check if any shares owned in the market
        if not self.getposition(self.getdatabyname(symbol_name)).size and (symbol_name not in self.opened):
            if self.major[high_currency] - self.major[low_currency] >= self.p.distance / 100:
                size = self.p.size
                if 'JPY' in symbol_name:
                    size //= 100

                # generate buy signal
                if isbuy:
                    self.buy(data=self.dnames[symbol_name], size=size)
                    self.entryprice = self.dnames[symbol_name].close[0]
                    self.log('BUY CREATE, %.2f' % self.entryprice)
                    self.opened.append(symbol_name)
                else:
                    self.sell(data=self.dnames[symbol_name], size=size)
                    self.entryprice = self.dnames[symbol_name].close[0]
                    self.log('SELL CREATE, %.2f' % self.dnames[symbol_name].close[0])
                    self.opened.append(symbol_name)


class CCYStrategy(StrategyTemplate):
    params = (
        ('smaf_period', 2),
        ('smas_period', 20),
        ('distance', 38),  # <------------------------
        ('size', 1000),  # <---------confidence level
        ('trailing_prc', 1),
        ('price', None)
    )

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        # To keep track of pending orders and buy price/commission

        self.orders = [None for i in range(len(self.datas))]  # current pending order
        self.ccy = ECICCY(*self.datas[:])
        self.entryprice = None
        self.CCY_PAIRS = (
            "EURUSD", "EURGBP", "EURAUD", "EURCAD",
            "EURCHF", "EURJPY", "EURNZD", "AUDCAD",
            "AUDCHF", "AUDJPY", "AUDNZD", "AUDUSD",
            "CADCHF", "CADJPY", "CHFJPY", "GBPAUD",
            "GBPCAD", "GBPCHF", "GBPJPY", "GBPNZD",
            "GBPUSD", "NZDCAD", "NZDCHF", "NZDJPY",
            "NZDUSD", "USDCAD", "USDCHF", "USDJPY"
        )
        self.currencies = ('AUD', 'CAD', 'CHF', 'EUR', 'GBP', 'JPY', 'NZD', 'USD')
        self.opened = []

    def notify_order(self, order):
        if not order.status == order.Completed:
            return
        size = self.p.size
        if 'JPY' in order.data._name:
            size //= 100
        if order.isbuy():
            self.sell(data=order.data, size=size, exectype=bt.Order.StopTrail, trailpercent=self.p.trailing_prc / 100)
        else:
            self.buy(data=order.data, size=size, exectype=bt.Order.StopTrail, trailpercent=self.p.trailing_prc / 100)
        # , price= (order.data.close[0]*(1-self.p.take_profit))

    def stop(self):
        self.params.price = self.broker.getvalue()

    def next(self):
        self.major = {}
        for i in self.currencies:
            self.major[i] = getattr(self.ccy, i)[0]

        high_currency = max(self.major, key=self.major.get)
        low_currency = min(self.major, key=self.major.get)

        symbol_name = ''
        isbuy = True
        if high_currency + low_currency in self.CCY_PAIRS:
            symbol_name = high_currency + low_currency
            isbuy = True
        else:
            symbol_name = low_currency + high_currency
            isbuy = False

        # check if any shares owned in the market
        if not self.getposition(self.getdatabyname(symbol_name)).size and (symbol_name not in self.opened):
            if self.major[high_currency] - self.major[low_currency] >= self.p.distance:
                size = self.p.size
                if 'JPY' in symbol_name:
                    size //= 100

                # generate buy signal
                if isbuy:
                    self.buy(data=self.dnames[symbol_name], size=size)
                    self.entryprice = self.dnames[symbol_name].close[0]
                    self.log('BUY CREATE, %.2f' % self.entryprice)
                    self.opened.append(symbol_name)
                else:
                    self.sell(data=self.dnames[symbol_name], size=size)
                    self.entryprice = self.dnames[symbol_name].close[0]
                    self.log('SELL CREATE, %.2f' % self.dnames[symbol_name].close[0])
                    self.opened.append(symbol_name)
