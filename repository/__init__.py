from .user import UserRepository
from .cart import CartRepository
from .category import CategoryRepository
from .order import OrderRepository
from .product import ProductRepository
from .user import UserRepository


class Repo:
    def __init__(self):
        # cart_repo = CartRepository
        # category_repo = CategoryRepository
        # order_repo = OrderRepository
        # partner_repo = CartRepository
        # product_repo = ProductRepository
        user_repo = UserRepository
