from database import db


class StockMonitor(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    stock_id = db.Column(db.String(50))
    monitoring_type = db.Column(db.String(50))
    threshold_value = db.Column(db.String(50))
    status = db.Column(db.String(50))
    user_id = db.Column(db.String(50))
