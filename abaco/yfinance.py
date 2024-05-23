"""
IMPLEMENTA CONSULTAS POR MEIO DA LIB yfinance
"""
from datetime import datetime

import yfinance as yf

from .cache import add_stock_info
from .cache import get_stock_info as cache_get_stock_info
from .webscraping import company_icon


def get_stock_info(ticker: str):
    stock = cache_get_stock_info(ticker)
    if stock is not False:
        return stock
    try:
        stock = yf.Ticker(f'{ticker}.sa'.upper())
        data = stock.get_info()
        data['updatedAt'] = int(datetime.now().timestamp())
        if str(data['shortName']).split(' ')[0] == 'FII':
            data['isFii'] = True
        else:
            data['isFii'] = False
        icon = company_icon(ticker.lower(), data['isFii'])
        if icon is not False:
            data['companyIcon'] = icon
        if not add_stock_info(data):
            return False
        return data
    except Exception as e:
        print(e)
        return False
