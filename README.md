# Python ACS Strategy Backtester & Optimizer

## Overview

This backtester utilizes Backtrader Library's Cerebro Engine to backtest 28 pairs of forex trading, formed by 8 major currencies. 

## Strategy
This backtester utilize a strategy called Advanced Currency Strength, inspired by -   [Bernhard Schweigert](https://www.mql5.com/en/users/bernardo33/seller).
The strategy intake 28 forex pairs and calculate the relative strength of each major currencies. 
When two currencies are polarizing to a certain level, this backtester form the two currencies as a pair, and make paper trade buy or sell orders. Exitting with a trailing 1 percent (changable).

# How to use
## Set Up
 1. Check Requirements.txt for System specifications, and required python modules
 2. Download `/mysite`
 3. Open with Visual Studio Code
 4. Select `/mysite` and Right-click
 5. Click "*Open in Intergrated Terminal*"
 6. Type in `python manage.py runserver`
 7. Visit the link with browser provided by the kernel, default: `http://127.0.0.1:8000/`
 
## Operate ACS Backtester

 1. Select the time period
 2. Select the Fast Moving Average Period (Default: 3)
 3. Select the Slow Moving Average Period (Default: 20)
 4. Select the Sensitivity level (Default: 8%)
 5. Select the Trailing Percentage (Default: 1%)
 6. Click Submit

## Operate ACS Optimizer

 1. Select the time period
 2. Select the Minimum Fast Moving Average Period (Default: 2)
 3. Select the Maximum Fast Moving Average Period (Default: 3)
 4. Select the Minimum Slow Moving Average Period (Default: 3)
 5. Select the Maximum Slow Moving Average Period (Default: 4)
 6. Select the Minimum Sensitivity level (Default: 8%)
 7. Select the Maximum Sensitivity level (Default: 8%)
 8. Click Submit

## Disclaimer & Ownership

    This backtester is created and used for academic and research purposes, which could be further developed and be used for financial purposes.
    This backtester does not intend to make a recommendation or suggestion to anyone on making financial decision.
    This backtester is created by Elvis Lam and Nicholas Yan, under supervision of Paul Lam. 
