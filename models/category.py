from sqlalchemy.sql.sqltypes import BigInteger
from util.postgre import db
from sqlalchemy.sql import func
from sqlalchemy import DateTime, Integer, String
from .base import Base


class Category(Base):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    created_at = db.Column(DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    def to_dict(self):
        d = {
            "id": self.id,
            "name": self.name,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
        }
        return d
