from .auth import Auth
from .cart import Cart
from .product import Product
from .order import Order
from .user import User
from .warehouse import Warehouse


class Service:
    auth = Auth()
    cart = Cart()
    order = Order()
    user = User()
    product = Product()
    warehouse = Warehouse()
