from sqlalchemy.sql.schema import UniqueConstraint
from database import db


class StockMonitor(db.Model):
    '''
    {
        "id": 2,
        "stock_id": "sz000069",
        "threshold_value": "2.78",
        "threshold_type": "percent",
        "status": "0",
        "user_id": "default",
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
    user_id = db.Column(db.String(50))

    __table_args__ = (
        UniqueConstraint('stock_id', 'user_id'),
    )

    def __json__(self):
        return {
            'id': self.id,
            'stock_id': self.stock_id,
            'threshold_value': self.threshold_value,
            'threshold_type': self.threshold_type,
            'status': self.status,
            'user_id': self.user_id,
            'monitoring_type': self.monitoring_type
        }

    @staticmethod
    def of(json):
        return StockMonitor(
            stock_id=json['stock_id'],
            monitoring_type=json['monitoring_type'],
            threshold_value=json['threshold_value'],
            threshold_type=json['threshold_type'],
            status=json['status'],
            user_id=json['user_id']
        )
