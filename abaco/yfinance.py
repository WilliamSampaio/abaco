"""
IMPLEMENTA CONSULTAS POR MEIO DA LIB yfinance
"""
import time
from datetime import datetime

import streamlit as st
import yfinance as yf

from .cache import add_stock_info
from .cache import get_stock_info as cache_get_stock_info
from .cache import update_stock_info
from .webscraping import company_icon


@st.cache_data(show_spinner=False)
def get_stock_info(ticker: str):
    def load_data_from_api(ticker: str):
        try:
            stock = yf.Ticker(f'{ticker}.sa'.upper())
            return stock.get_info()
        except Exception as e:
            print(e)
            return False

    def update_data(data: dict):
        data['abaco_updatedat'] = int(datetime.now().timestamp())
        if str(data['shortName']).split(' ')[0] == 'FII':
            data['abaco_tipo_ativo'] = 'fii'
        else:
            data['abaco_tipo_ativo'] = 'açoẽs'
        icon = company_icon(ticker.lower(), data['abaco_tipo_ativo'] == 'fii')
        if icon is not False:
            data['abaco_icon'] = icon
        return data

    stock = cache_get_stock_info(ticker)
    if stock is False:
        data = load_data_from_api(ticker)
        if data is False:
            return False
        if not add_stock_info(update_data(data)):
            return False
        return data
    if time.time() > (stock['abaco_updatedat'] + 86400):
        data = load_data_from_api(ticker)
        if data is False:
            return False
        if not update_stock_info(update_data(data)):
            return False
        return data
    return stock
