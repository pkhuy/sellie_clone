from sqlalchemy.sql.sqltypes import BigInteger
from util.postgre import db
from sqlalchemy.sql import func
from sqlalchemy import DateTime, Integer, String, Enum
import enum
from .base import Base


class OrderStatus(enum.Enum):
    waiting_shipper = 1
    delivering = 2
    complete = 3
    cancel = 4


class Order(Base):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String, nullable=False)
    status = db.Column(Enum(OrderStatus))
    created_at = db.Column(DateTime(timezone=True), server_default=func.now())

    def to_dict(self):
        d = {
            "id": self.id,
            "name": self.name,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
        }
        return d


class OrderItem(Base):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String, nullable=False)
    status = db.Column(Enum(OrderStatus))
    created_at = db.Column(DateTime(timezone=True), server_default=func.now())

    def to_dict(self):
        d = {
            "id": self.id,
            "name": self.name,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
        }
        return d