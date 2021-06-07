from util import result
from util.utils import csv_content_to_json
from api.price_provider import get_info_from_sina
from models import StockMonitor


def check_stock_value():
    mons = StockMonitor.query.all()
    stock_code_set = set()
    user_stock_dict = {}
    for mon in mons:
        stock_code_set.add(mon.stock_id)
        user_stock_dict[mon.stock_id] = mon
    res = get_info_from_sina(",".join(stock_code_set))
    res_json_array = csv_content_to_json(res)
    print(res_json_array)
    response = []
    for mon_real_value in res_json_array:
        print(mon_real_value)
        stock_code = mon_real_value['ID']
        curr_price = mon_real_value['当前价格']
        yestoday_close_price = mon_real_value['昨日收盘价']
        if curr_price:
            user_order = user_stock_dict[stock_code]
            tv = user_order.threshold_value
            mt = user_order.monitoring_type
            tt = user_order.threshold_type
            if is_reach(curr_price, tv, mt, tt):
                mes = 'stock_code %s current  %s reach threshold_value %s ,threshold_type %s monitoring_type %s' % (
                    stock_code, curr_price, tv, tt, mt)
                print('***', mes)
                response.append(
                    {
                        'id': stock_code,
                        'user': user_order.user_id,
                        'message': mes
                    }
                )
    return response


def is_reach(curr_price, tv, mt, tt):
    print(curr_price, tv, mt, tt)
    if tt == 'absolute':
        if mt == 'high':
            return float(curr_price) >= float(tv)
        elif mt == 'low':
            return float(curr_price) <= float(tv)

    print('not implements : %s %s' % (mt, tt))
