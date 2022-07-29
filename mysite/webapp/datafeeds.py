import backtrader as bt


class DownloadedCSVData(bt.feeds.GenericCSVData):
    # default parameters
    params = (
        ('nullvalue', 0.0),
        ('dtformat', '%Y-%m-%d'),
        ('tmformat', '%H:%M:%S'),
        ('timeframe', bt.TimeFrame.Days),
        ('compression', 1),

        ('datetime', 0),
        ('time', -1),
        ('open', 1),
        ('high', 2),
        ('low', 3),
        ('close', 4),
        ('volume', 6),
        ('openinterest', -1),
    )