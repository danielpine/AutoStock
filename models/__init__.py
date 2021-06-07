from functools import partial

from sqlalchemy.orm import defaultload
from database import db
from sqlalchemy.sql import func
from sqlalchemy.sql.schema import UniqueConstraint

import datetime

print(datetime.datetime.now())


class StockMonitor(db.Model):
    '''
    {
        "id": 2,
        "stock_id": "sz000069",
        "threshold_value": "2.78",
        "threshold_type": "percent",
        "status": "0",
        "user_id": "default",
        "over_limit": 1,
        "over_count": 0,
        "monitoring_type": "high"
    }
    '''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    stock_id = db.Column(db.String(50))
    # high low
    monitoring_type = db.Column(db.String(50))
    threshold_value = db.Column(db.String(50))
    # absolute percent
    threshold_type = db.Column(db.String(50))
    # 0 1 2 3 4
    status = db.Column(db.String(50))
    # the notification limit times after the value over
    over_limit = db.Column(db.String(50))
    over_count = db.Column(db.Integer, default=0)
    user_id = db.Column(db.String(50))
    time_stamp = db.Column(
        db.DateTime(timezone=True), default=datetime.datetime.now, onupdate=datetime.datetime.now)

    __table_args__ = (
        UniqueConstraint('stock_id', 'user_id',
                         'monitoring_type', 'threshold_value'),
    )

    def __json__(self):
        return {
            'id': self.id,
            'stock_id': self.stock_id,
            'threshold_value': self.threshold_value,
            'threshold_type': self.threshold_type,
            'status': self.status,
            'user_id': self.user_id,
            'over_limit': self.over_limit,
            'over_count': self.over_count,
            'monitoring_type': self.monitoring_type,
            'time_stamp': self.time_stamp.strftime(r"%Y-%m-%d %H:%M:%S"),

        }

    @staticmethod
    def of(json):
        return StockMonitor(
            stock_id=json['stock_id'],
            monitoring_type=json['monitoring_type'],
            threshold_value=json['threshold_value'],
            threshold_type=json['threshold_type'],
            status=json['status'],
            user_id=json['user_id'],
            over_limit=json['over_limit']
        )
