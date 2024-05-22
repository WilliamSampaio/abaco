"""
IMPLEMENTA CONSULTAS POR MEIO DA LIB yfinance,
CASO A INFORMAÇÃO NÃO EXISTA EM CACHE
"""
from datetime import datetime

import yfinance as yf

from .database import get_query, get_stocks


def yf_get_stock_info(ticker: str):
    try:
        stock = yf.Ticker(f'{ticker}.sa'.upper())
        data = stock.get_info()
        data['updatedAt'] = int(datetime.now().timestamp())
        return get_stocks().insert(data)
    except Exception:
        return False


def get_stock_info(ticker: str):
    Stock = get_query()
    stocks = get_stocks()
    results = stocks.search(Stock.symbol == f'{ticker}.sa'.upper())
    if len(results) == 0:
        stock = yf_get_stock_info(ticker)
        if not stock:
            return False
        return get_stocks().get(doc_id=stock)
    stock = results[0]
    return stock
