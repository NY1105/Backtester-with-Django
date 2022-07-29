from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_page, name='backtest'),
    path('acs_result/', views.backtest_result, name='acs_backtest_result'),
    path('ccy_result/', views.ccybt_result, name='ccy_backtest_result'),
    path('optimize/', views.optimize_result, name='optimize_result'),
]