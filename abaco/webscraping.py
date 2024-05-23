import requests
from bs4 import BeautifulSoup
from lxml import etree

from .config import settings as s


def company_icon(ticker: str, is_fii: bool = False):
    url = s.STATUSINVEST_URL2 if is_fii else s.STATUSINVEST_URL1
    req = requests.get(
        str(url).format(ticker.lower()), headers={'User-Agent': 'Mozilla/5.0'}
    )
    if req.status_code != 200:
        return False
    soup = BeautifulSoup(req.content, 'html.parser')
    dom = etree.HTML(str(soup))
    try:
        parentid = dom.xpath('//*[@id="btn-resume-wallet"]')[0].attrib[
            'data-parentid'
        ]
        return str(s.STATUSINVEST_URL_STOCK_ICON).format(parentid)
    except Exception:
        return False
