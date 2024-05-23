import requests
from bs4 import BeautifulSoup
from lxml import etree

from .config import settings as s


def company_icon(ticker: str, is_fii: bool = False):
    url = s.INVESTIDOR10_URL2 if is_fii else s.INVESTIDOR10_URL1
    req = requests.get(
        str(url).format(ticker.lower()), headers={'User-Agent': 'Mozilla/5.0'}
    )
    if req.status_code != 200:
        return False
    soup = BeautifulSoup(req.content, 'html.parser')
    dom = etree.HTML(str(soup))
    try:
        uri = dom.xpath('//*[@id="header_action"]/div[1]/div[1]/img')[
            0
        ].attrib['src']
        return str(s.INVESTIDOR10_URL_BASE + uri)
    except Exception:
        return False
