from nis import match
from .datafeeds import DownloadedCSVData
from .strategies import *
from backtrader_plotly.plotter import BacktraderPlotly
from backtrader_plotly.scheme import PlotScheme
from contextlib import redirect_stdout
from datetime import datetime
from numbers import Number
import backtrader as bt
import collections
import io
import os
import pandas as pd
import plotly.io
import sys


class Backtest:

    cash_deposit = 100000.0


    symbols = [
        "EURUSD=X", "EURGBP=X", "EURAUD=X", "EURCAD=X",
        "EURCHF=X", "EURJPY=X", "EURNZD=X", "AUDCAD=X",
        "AUDCHF=X", "AUDJPY=X", "AUDNZD=X", "AUDUSD=X",
        "CADCHF=X", "CADJPY=X", "CHFJPY=X", "GBPAUD=X",
        "GBPCAD=X", "GBPCHF=X", "GBPJPY=X", "GBPNZD=X",
        "GBPUSD=X", "NZDCAD=X", "NZDCHF=X", "NZDJPY=X",
        "NZDUSD=X", "USDCAD=X", "USDCHF=X", "USDJPY=X"
    ]

    def __init__(self, from_date='2019-01-01', to_date='2021-12-31',
                 min_ma_fast=2, max_ma_fast=3, min_ma_slow=3, max_ma_slow=5, min_dis=8, max_dis=8, trp=1, mode="ACS_bt"):

        self.new_stdout = io.StringIO()
        sys.stdout = self.new_stdout

        self.cerebro = bt.Cerebro()
        self.cerebro.broker.setcash(self.cash_deposit)
        self.cerebro.broker.setcommission(commission=0.00075)

        def acs_test_case_generator(lower_fast, upper_fast, lower_slow, upper_slow, lower_distance, upper_distance):
            for slow in range(lower_slow, upper_slow + 1):
                fast_upper_bound = slow if slow < upper_fast + 1 else upper_fast + 1
                for fast in range(lower_fast, fast_upper_bound):
                    for dist in range(lower_distance, upper_distance + 1):
                        yield {
                            'smaf_period': fast,
                            'smas_period': slow,
                            'distance': dist,
                        }

        match

        if (mode == 'ACS_opt'):
            self.cerebro.optstrategy(
                ACSStrategy, opt_dict=acs_test_case_generator(min_ma_fast, max_ma_fast, min_ma_slow, max_ma_slow, min_dis, max_dis))
        elif (mode == 'ACS_bt'):
            self.cerebro.addstrategy(ACSStrategy, smaf_period=max_ma_fast, smas_period=max_ma_slow, distance=max_dis, trailing_prc=trp)
        elif (mode == 'CCY_bt'):
            self.cerebro.addstrategy(CCYStrategy, distance=max_dis, trailing_prc=trp)
    
        from_date = datetime.strptime(from_date, "%d/%m/%Y")
        to_date = datetime.strptime(to_date, "%d/%m/%Y")
        for i, symbol in enumerate(self.symbols):
            self.cerebro.adddata(DownloadedCSVData(dataname=(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0]),), './webapp/data/' + symbol[0:6] + '.csv')),
                                                   plot=(i == 0),
                                                   fromdate=from_date,
                                                   todate=to_date
                                                   ),
                                 name=symbol[0:6],)

        self.cerebro.addanalyzer(bt.analyzers.TradeAnalyzer)
        self.cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name="Sharpe")
        self.cerebro.addanalyzer(bt.analyzers.Transactions)
        self.cerebro.addanalyzer(bt.analyzers.Returns, _name="returns")

        self.cerebro.addwriter(bt.WriterFile)

        self.stratruns = self.cerebro.run(maxcpus=1, optreturn=False)

    def createDf(self):
        self.stratruns = [x[0] for x in self.stratruns]
        cols = tuple(self.stratruns[0].p._getkeys())

        for name_of_analyzer, analyzer in zip(self.stratruns[0].analyzers._names, self.stratruns[0].analyzers._items):
            if name_of_analyzer in ('tradeanalyzer', 'transactions'):
                continue
            else:
                rets_dict = analyzer.get_analysis()
                rets_dict = flatten_dict(rets_dict)
                for name_of_ret in rets_dict.keys():
                    cols += (f'{name_of_analyzer}_{name_of_ret}',)

        df = pd.DataFrame(columns=cols)
        for strat in self.stratruns:
            row = [value if isinstance(value, Number) else str(value) for value in strat.p._getvalues()]
            for name_of_analyzer, analyzer in zip(strat.analyzers._names, strat.analyzers._items):
                if name_of_analyzer in ('tradeanalyzer', 'transactions'):
                    continue

                else:
                    rets_dict = analyzer.get_analysis()
                    rets_dict = flatten_dict(rets_dict)
                    for ret in rets_dict.values():
                        row += [ret if isinstance(ret, Number) else str(ret)]

            df.loc[len(df)] = row

        df = df.drop('opt_dict', 1)
        df = df.sort_values(by=['returns_rtot'], ascending=False)
        return df

    def getGraph(self):
        scheme = PlotScheme(decimal_places=5, max_legend_text_width=16)
        figs = self.cerebro.plot(BacktraderPlotly(show=False, scheme=scheme))
        figs = [x for fig in figs for x in fig]  # flatten output
        html_boby = ''.join(plotly.io.to_html(figs[i], full_html=False) for i in range(len(figs)))
        return html_boby

    def getReport(self):
        return self.new_stdout.getvalue().replace(' ', '&nbsp;').split('\n')

    def getBestSetting(self):
        best_setting = self.stratruns[0].params._getkwargs()

        # sharpe = self.stratruns[6].analyzers.returns.get_analysis()
        for strat in self.stratruns:
            if strat.params._getkwargs()['price'] > best_setting['price']:
                best_setting = strat.params._getkwargs()
        best_setting.popitem(last=False)
        return best_setting


def flatten_dict(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.abc.MutableMapping):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)
