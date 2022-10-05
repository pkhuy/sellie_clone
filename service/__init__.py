from .auth import Auth
from .cart import Cart
from .product import Product
# from .user import User
# from .user import User
# from .user import User


class Service:
    auth = Auth()
    cart = Cart()
    product = Product()
