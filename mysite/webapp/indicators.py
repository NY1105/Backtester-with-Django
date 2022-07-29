import backtrader as bt


class EightCurrenciesIndicator(bt.Indicator):
    # Declare indicator lines
    lines = (
        'AUD', 'CAD', 'CHF', 'EUR', 'GBP', 'JPY', 'NZD', 'USD',
        'AUDCAD', 'AUDCHF', 'AUDJPY', 'AUDNZD', 'AUDUSD', 'CADCHF',
        'CADJPY', 'CHFJPY', 'EURAUD', 'EURCAD', 'EURCHF', 'EURGBP',
        'EURJPY', 'EURNZD', 'EURUSD', 'GBPAUD', 'GBPCAD', 'GBPCHF',
        'GBPJPY', 'GBPNZD', 'GBPUSD', 'NZDCAD', 'NZDCHF', 'NZDJPY',
        'NZDUSD', 'USDCAD', 'USDCHF', 'USDJPY',
    )

    # Default indicator parameters
    params = (
        ('period', 14),
        ('AUDCAD', 0.80), ('AUDCHF', 0.60), ('AUDJPY', 0.85), ('AUDNZD', 0.80),
        ('AUDUSD', 0.85), ('CADCHF', 0.65), ('CADJPY', 0.80), ('CHFJPY', 0.65),
        ('EURAUD', 0.55), ('EURCAD', 0.70), ('EURCHF', 0.44), ('EURGBP', 0.65),
        ('EURJPY', 1.00), ('EURNZD', 1.00), ('EURUSD', 1.00), ('GBPAUD', 0.25),
        ('GBPCAD', 0.25), ('GBPCHF', 0.20), ('GBPJPY', 0.50), ('GBPNZD', 0.05),
        ('GBPUSD', 0.50), ('NZDCAD', 0.70), ('NZDCHF', 0.70), ('NZDJPY', 0.70),
        ('NZDUSD', 0.70), ('USDCAD', 1.00), ('USDCHF', 1.00), ('USDJPY', 1.00),
    )

    # Default indicator plotinfo parameters
    plotinfo = (
        ('plot', True),
        ('subplot', True),
    )
    # Indicator lines specific plotting styles
    plotlines = dict(
        AUD=dict(_plotskip=False),
        CAD=dict(_plotskip=False),
        CHF=dict(_plotskip=False),
        EUR=dict(_plotskip=False),
        GBP=dict(_plotskip=False),
        JPY=dict(_plotskip=False),
        NZD=dict(_plotskip=False),
        USD=dict(_plotskip=False),
        AUDCAD=dict(_plotskip=True),
        AUDCHF=dict(_plotskip=True),
        AUDJPY=dict(_plotskip=True),
        AUDNZD=dict(_plotskip=True),
        AUDUSD=dict(_plotskip=True),
        CADCHF=dict(_plotskip=True),
        CADJPY=dict(_plotskip=True),
        CHFJPY=dict(_plotskip=True),
        EURAUD=dict(_plotskip=True),
        EURCAD=dict(_plotskip=True),
        EURCHF=dict(_plotskip=True),
        EURGBP=dict(_plotskip=True),
        EURJPY=dict(_plotskip=True),
        EURNZD=dict(_plotskip=True),
        EURUSD=dict(_plotskip=True),
        GBPAUD=dict(_plotskip=True),
        GBPCAD=dict(_plotskip=True),
        GBPCHF=dict(_plotskip=True),
        GBPJPY=dict(_plotskip=True),
        GBPNZD=dict(_plotskip=True),
        GBPUSD=dict(_plotskip=True),
        NZDCAD=dict(_plotskip=True),
        NZDCHF=dict(_plotskip=True),
        NZDJPY=dict(_plotskip=True),
        NZDUSD=dict(_plotskip=True),
        USDCAD=dict(_plotskip=True),
        USDCHF=dict(_plotskip=True),
        USDJPY=dict(_plotskip=True),
    )

    def __init__(self):
        # Lookup values
        self.total_number_of_currencies = 8
        self.total_number_of_pairs = 28

        # Two EMAs used for ACS evaluations
        self.rsi = {}

        for i in range(self.total_number_of_pairs):
            pair_name = self.datas[i]._name[0:6]
            self.rsi[pair_name] = bt.indicators.RSI(self.datas[i].lines.close, period=self.p.period).rsi()

    def next(self):
        # Initialize each line value for today
        for line in self.lines:
            line[0] = 0

        # Calculate values for each currency line
        for symbol in self.datas:
            pair_name = symbol._name[0:6]
            base_currency = symbol._name[0:3]
            quot_currency = symbol._name[3:6]

            getattr(self.lines, base_currency)[0] += self.rsi[pair_name] * getattr(self.p, pair_name) / (self.total_number_of_currencies - 1)
            getattr(self.lines, quot_currency)[0] += (100 - self.rsi[pair_name]) * getattr(self.p, pair_name) / (self.total_number_of_currencies - 1)


class EightCurrenciesIndicatorEMA(bt.Indicator):
    # Declare indicator lines
    lines = (
        'AUD', 'CAD', 'CHF', 'EUR', 'GBP', 'JPY', 'NZD', 'USD',
        'AUDCAD', 'AUDCHF', 'AUDJPY', 'AUDNZD', 'AUDUSD', 'CADCHF',
        'CADJPY', 'CHFJPY', 'EURAUD', 'EURCAD', 'EURCHF', 'EURGBP',
        'EURJPY', 'EURNZD', 'EURUSD', 'GBPAUD', 'GBPCAD', 'GBPCHF',
        'GBPJPY', 'GBPNZD', 'GBPUSD', 'NZDCAD', 'NZDCHF', 'NZDJPY',
        'NZDUSD', 'USDCAD', 'USDCHF', 'USDJPY',
    )

    # Default indicator parameters
    params = (
        ('period', 14),
        ('AUDCAD', 0.80), ('AUDCHF', 0.60), ('AUDJPY', 0.85), ('AUDNZD', 0.80),
        ('AUDUSD', 0.85), ('CADCHF', 0.65), ('CADJPY', 0.80), ('CHFJPY', 0.65),
        ('EURAUD', 0.55), ('EURCAD', 0.70), ('EURCHF', 0.44), ('EURGBP', 0.65),
        ('EURJPY', 1.00), ('EURNZD', 1.00), ('EURUSD', 1.00), ('GBPAUD', 0.25),
        ('GBPCAD', 0.25), ('GBPCHF', 0.20), ('GBPJPY', 0.50), ('GBPNZD', 0.05),
        ('GBPUSD', 0.50), ('NZDCAD', 0.70), ('NZDCHF', 0.70), ('NZDJPY', 0.70),
        ('NZDUSD', 0.70), ('USDCAD', 1.00), ('USDCHF', 1.00), ('USDJPY', 1.00),
        ('smaf_period', 3),
        ('smas_period', 20)

    )

    # Default indicator plotinfo parameters
    plotinfo = (
        ('plot', True),
        ('subplot', True),
    )
    # Indicator lines specific plotting styles
    plotlines = dict(
        AUD=dict(_plotskip=False),
        CAD=dict(_plotskip=False),
        CHF=dict(_plotskip=False),
        EUR=dict(_plotskip=False),
        GBP=dict(_plotskip=False),
        JPY=dict(_plotskip=False),
        NZD=dict(_plotskip=False),
        USD=dict(_plotskip=False),
        AUDCAD=dict(_plotskip=True),
        AUDCHF=dict(_plotskip=True),
        AUDJPY=dict(_plotskip=True),
        AUDNZD=dict(_plotskip=True),
        AUDUSD=dict(_plotskip=True),
        CADCHF=dict(_plotskip=True),
        CADJPY=dict(_plotskip=True),
        CHFJPY=dict(_plotskip=True),
        EURAUD=dict(_plotskip=True),
        EURCAD=dict(_plotskip=True),
        EURCHF=dict(_plotskip=True),
        EURGBP=dict(_plotskip=True),
        EURJPY=dict(_plotskip=True),
        EURNZD=dict(_plotskip=True),
        EURUSD=dict(_plotskip=True),
        GBPAUD=dict(_plotskip=True),
        GBPCAD=dict(_plotskip=True),
        GBPCHF=dict(_plotskip=True),
        GBPJPY=dict(_plotskip=True),
        GBPNZD=dict(_plotskip=True),
        GBPUSD=dict(_plotskip=True),
        NZDCAD=dict(_plotskip=True),
        NZDCHF=dict(_plotskip=True),
        NZDJPY=dict(_plotskip=True),
        NZDUSD=dict(_plotskip=True),
        USDCAD=dict(_plotskip=True),
        USDCHF=dict(_plotskip=True),
        USDJPY=dict(_plotskip=True),
    )

    def __init__(self):
        # Lookup values
        self.total_number_of_currencies = 8
        self.total_number_of_pairs = 28

        # Two EMAs used for ACS evaluations

        self.EMAslow = {}
        self.EMAfast = {}

        for i in range(len(self.datas)):
            pair_name = self.datas[i]._name[0:6]
            self.wtprice = (self.datas[i].close + self.datas[i].close + self.datas[i].high + self.datas[i].low) / 4
            self.EMAslow[pair_name] = bt.indicators.EMA(self.wtprice, period=self.params.smas_period)
            self.EMAfast[pair_name] = bt.indicators.EMA(self.wtprice, period=self.params.smaf_period)

    def next(self):

        # Initialize each line value for today
        for line in self.lines:
            line[0] = 0

        # Calculate values for each currency line
        for symbol in self.datas:
            pair_name = symbol._name[0:6]
            base_currency = symbol._name[0:3]
            quot_currency = symbol._name[3:6]

            rateofchange = (self.EMAfast[pair_name][0] - self.EMAslow[pair_name][0]) / self.EMAslow[pair_name][0] * getattr(self.p, pair_name)
            getattr(self.lines, base_currency)[0] += rateofchange
            getattr(self.lines, quot_currency)[0] -= rateofchange


class EightCurrenciesIndicatorCCY(bt.Indicator):
    # Declare indicator lines
    lines = (
        'AUD', 'CAD', 'CHF', 'EUR', 'GBP', 'JPY', 'NZD', 'USD',
        'AUDCAD', 'AUDCHF', 'AUDJPY', 'AUDNZD', 'AUDUSD', 'CADCHF',
        'CADJPY', 'CHFJPY', 'EURAUD', 'EURCAD', 'EURCHF', 'EURGBP',
        'EURJPY', 'EURNZD', 'EURUSD', 'GBPAUD', 'GBPCAD', 'GBPCHF',
        'GBPJPY', 'GBPNZD', 'GBPUSD', 'NZDCAD', 'NZDCHF', 'NZDJPY',
        'NZDUSD', 'USDCAD', 'USDCHF', 'USDJPY',
    )

    # Default indicator parameters
    params = (

        ('symbols', [
            "EURUSD=X", "EURGBP=X", "EURAUD=X", "EURCAD=X",
            "EURCHF=X", "EURJPY=X", "EURNZD=X", "AUDCAD=X",
            "AUDCHF=X", "AUDJPY=X", "AUDNZD=X", "AUDUSD=X",
            "CADCHF=X", "CADJPY=X", "CHFJPY=X", "GBPAUD=X",
            "GBPCAD=X", "GBPCHF=X", "GBPJPY=X", "GBPNZD=X",
            "GBPUSD=X", "NZDCAD=X", "NZDCHF=X", "NZDJPY=X",
            "NZDUSD=X", "USDCAD=X", "USDCHF=X", "USDJPY=X"
        ]),

    )

    # Default indicator plotinfo parameters
    plotinfo = (
        ('plot', True),
        ('subplot', True),
    )
    # Indicator lines specific plotting styles
    plotlines = dict(
        AUD=dict(_plotskip=False),
        CAD=dict(_plotskip=False),
        CHF=dict(_plotskip=False),
        EUR=dict(_plotskip=False),
        GBP=dict(_plotskip=False),
        JPY=dict(_plotskip=False),
        NZD=dict(_plotskip=False),
        USD=dict(_plotskip=False),
        AUDCAD=dict(_plotskip=True),
        AUDCHF=dict(_plotskip=True),
        AUDJPY=dict(_plotskip=True),
        AUDNZD=dict(_plotskip=True),
        AUDUSD=dict(_plotskip=True),
        CADCHF=dict(_plotskip=True),
        CADJPY=dict(_plotskip=True),
        CHFJPY=dict(_plotskip=True),
        EURAUD=dict(_plotskip=True),
        EURCAD=dict(_plotskip=True),
        EURCHF=dict(_plotskip=True),
        EURGBP=dict(_plotskip=True),
        EURJPY=dict(_plotskip=True),
        EURNZD=dict(_plotskip=True),
        EURUSD=dict(_plotskip=True),
        GBPAUD=dict(_plotskip=True),
        GBPCAD=dict(_plotskip=True),
        GBPCHF=dict(_plotskip=True),
        GBPJPY=dict(_plotskip=True),
        GBPNZD=dict(_plotskip=True),
        GBPUSD=dict(_plotskip=True),
        NZDCAD=dict(_plotskip=True),
        NZDCHF=dict(_plotskip=True),
        NZDJPY=dict(_plotskip=True),
        NZDUSD=dict(_plotskip=True),
        USDCAD=dict(_plotskip=True),
        USDCHF=dict(_plotskip=True),
        USDJPY=dict(_plotskip=True),
    )

    def currency_strength(self, ccy, i):
        strength, cnt = 0, 0
        for symbol in self.p.symbols:
            fact = 0
            if ccy == symbol[0:3] or ccy == symbol[3:6]:
                price_range = self.datas[i].high - self.datas[i].low
                if price_range != 0:
                    ratio = 100.0 * (self.datas[i].close - self.datas[i].low) / price_range
                    if(ratio > 3.0):
                        fact = 1
                    if(ratio > 10.0):
                        fact = 2
                    if(ratio > 25.0):
                        fact = 3
                    if(ratio > 40.0):
                        fact = 4
                    if(ratio > 50.0):
                        fact = 5
                    if(ratio > 60.0):
                        fact = 6
                    if(ratio > 75.0):
                        fact = 7
                    if(ratio > 90.0):
                        fact = 8
                    if(ratio > 97.0):
                        fact = 9
                    cnt += 1
                    if ccy == symbol[3:6]:
                        fact = 9 - fact
                    strength += fact
        if cnt != 0:
            strength /= cnt
        return strength

    def __init__(self):
        # Lookup values
        self.total_number_of_currencies = 8
        self.total_number_of_pairs = 28

        # for i in range(len(self.datas)):
        #     fact = 0
        #     pair_name = self.datas[i]._name[0:6]
        #     self.wtprice = (self.datas[i].close + self.datas[i].close + self.datas[i].high + self.datas[i].low) / 4
        #     self.EMAslow[pair_name] = bt.indicators.EMA(self.wtprice, period=self.params.smas_period)
        #     self.EMAfast[pair_name] = bt.indicators.EMA(self.wtprice, period=self.params.smaf_period)

    def next(self):

        # Initialize each line value for today
        for line in self.lines:
            line[0] = 0

        for i in range(len(self.p.symbols)):
            ccyBase = self.p.symbols[i][0:3]
            ccyQuote = self.p.symbols[i][3:6]
            baseStrength = self.currency_strength(ccyBase,i)
            quoteStrength = self.currency_strength(ccyQuote,i)
            powerBuy = round(baseStrength - quoteStrength, 2)
            powerSell = round(quoteStrength - baseStrength, 2)

            getattr(self.lines, ccyBase)[0] += powerBuy
            getattr(self.lines, ccyQuote)[0] -= powerSell

        #     rateofchange = (self.EMAfast[pair_name][0] - self.EMAslow[pair_name][0]) / self.EMAslow[pair_name][0] * getattr(self.p, pair_name)
        #     getattr(self.lines, base_currency)[0] += rateofchange
        #     getattr(self.lines, quot_currency)[0] -= rateofchange

        # for i in range(len(self.datas)):
        # fact = 0
