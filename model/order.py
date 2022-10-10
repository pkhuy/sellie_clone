from sqlalchemy.sql.schema import ForeignKey, Table
from .base import Base
from sqlalchemy import Column, Integer, String


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    code = Column(String, nullable=False)
    cart_id = Column(Integer, ForeignKey('carts.id'))
    owner_id = Column(Integer, ForeignKey('users.id'))
    status = Column(String)
