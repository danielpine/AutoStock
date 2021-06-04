from unittest import TestCase
from util.utils import AutoJSONEncoder


from database import db
from models import StockMonitor
from util.logger import log
from flask import json


class TestStockMonitor(TestCase):
    def test_insert(self):
        mon = StockMonitor(
            stock_id="sz000068",
            monitoring_type="top",
            threshold_value="top",
            status="0",
            user_id="default"
        )
        db.session.add(mon)
        db.session.commit()
        mons = StockMonitor.query.all()
        log.info(json.dumps(mons,cls=AutoJSONEncoder,indent=2))
