from sqlalchemy.sql.schema import ForeignKey, Table
from .base import Base
from sqlalchemy import Column, Integer, String


class CartItem(Base):
    __tablename__ = 'cart_items'

    id = Column(Integer, primary_key=True)
    product_id = Integer, ForeignKey('products.id', name='product_id')
    cart_id = Column(Integer, ForeignKey('carts.id'))
    customer_price = Column(Integer)
    quantity = Column(Integer)
