
from django.shortcuts import render
import pandas as pd
# import backtest as bt
from .backtest import Backtest
# Create your views here.

from django.http import HttpResponse


def index(request):
    print('im debug message')
    return HttpResponse("Hello, world. You're at the webapp index.")


def index_page(request):
    return render(request, 'backtester/index.html')


def backtest_result(request):
    context = {}

    if request.POST:
        fast_ma_period = request.POST.get("fast_ma_period", 3)
        slow_ma_period = request.POST.get("slow_ma_period", 20)

        distanc = request.POST.get("distance", 8)
        trailing_percentage = request.POST.get("trailing_percentage", 1)

        start_date = request.POST.get("backtest_startdate", '2019-01-01')
        end_date = request.POST.get("backtest_enddate", '2021-12-31')

        cerebro = Backtest(from_date=start_date, to_date=end_date, max_ma_fast=int(fast_ma_period), max_ma_slow=int(slow_ma_period),
                           max_dis=int(distanc), trp=int(trailing_percentage), mode='ACS_bt')

        graph_body = cerebro.getGraph()
        report = cerebro.getReport()
        context = {'html_body': graph_body, 'report': report, 'strategy': 'ACS'}

    return render(request, 'backtester/result.html', context)


def ccybt_result(request):
    context = {}

    if request.POST:

        distanc = request.POST.get("distance", 38)
        trailing_percentage = request.POST.get("trailing_percentage", 1)

        start_date = request.POST.get("backtest_startdate", '2019-01-01')
        end_date = request.POST.get("backtest_enddate", '2021-12-31')

        cerebro = Backtest(from_date=start_date, to_date=end_date,
                           max_dis=int(distanc), trp=int(trailing_percentage), mode='CCY_bt')

        graph_body = cerebro.getGraph()
        report = cerebro.getReport()
        context = {'html_body': graph_body, 'report': report, 'strategy': 'CCY'}

    return render(request, 'backtester/result.html', context)


def optimize_result(request):
    context = {}

    if request.POST:
        min_ma_fast_period = request.POST.get("min_ma_fast_period", 2)
        max_ma_fast_period = request.POST.get("max_ma_fast_period", 3)

        min_ma_slow_period = request.POST.get("min_ma_slow_period", 3)
        max_ma_slow_period = request.POST.get("max_ma_slow_period", 4)

        max_distanc = request.POST.get("max_distance", 5)
        min_distanc = request.POST.get("min_distance", 6)

        trailing_percentage = request.POST.get("trailing_percentage", 1)

        start_date = request.POST.get("optimize_startdate", '2019-01-01')
        end_date = request.POST.get("optimize_enddate", '2021-12-31')

        cerebro = Backtest(start_date, end_date, int(min_ma_fast_period), int(max_ma_fast_period), int(min_ma_slow_period),
                           int(max_ma_slow_period), int(min_distanc), int(max_distanc), int(trailing_percentage), mode='ACS_opt')

        df = cerebro.createDf()

        context = {'result_table': df.to_html(classes='table table-striped table-bordered table-sm'),
                   'best_row': df.iloc[[0]].to_html(classes='table table-striped table-bordered table-sm')}

    return render(request, 'backtester/optimize.html', context)
