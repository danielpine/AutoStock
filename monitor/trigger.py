from util.utils import csv_content_to_json
from api.price_provider import get_info_from_sina
from models import StockMonitor


def check():
    mons = StockMonitor.query.all()
    stock_code_set = set()
    for mon in mons:
        stock_code_set.add(mon.stock_id)
    res = get_info_from_sina(",".join(stock_code_set))
    print(csv_content_to_json(res))


