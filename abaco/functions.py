from .config import settings as s
from .yfinance import get_stock_info


def render_ticker_links(ticker: str) -> str:

    imglink = '[<img src="{}" style="width: 32px;">]({})'

    stock = get_stock_info()
    if stock:
        fii = stock['isFii']

    list_links = [
        imglink.format(s.STATUSINVEST_ICON, s.STATUSINVEST_URL2.format(ticker))
        if fii
        else imglink.format(
            s.STATUSINVEST_ICON, s.STATUSINVEST_URL1.format(ticker)
        ),
        imglink.format(s.FUNDAMENTUS_ICON, s.FUNDAMENTUS_URL.format(ticker)),
        imglink.format(s.YAHOOFINANCE_ICON, s.YAHOOFINANCE_URL.format(ticker)),
        imglink.format(s.INVESTIDOR10_ICON, s.INVESTIDOR10_URL2.format(ticker))
        if fii
        else imglink.format(
            s.INVESTIDOR10_ICON, s.INVESTIDOR10_URL1.format(ticker)
        ),
        imglink.format(
            s.FUNDSEXPLORER_ICON, s.FUNDSEXPLORER_URL.format(ticker)
        )
        if fii
        else '',
    ]

    return '{}'.format(''.join(list_links))
