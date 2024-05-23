from .database import get_query, get_stocks_tbl


def add_stock_info(data: dict):
    try:
        return get_stocks_tbl().insert(data)
    except Exception as e:
        print(e)
        return False


def get_stock_info(ticker: str):
    Stock = get_query()
    table = get_stocks_tbl()
    results = table.search(Stock.symbol == f'{ticker}.sa'.upper())
    if len(results) == 0:
        return False
    return results[0]
