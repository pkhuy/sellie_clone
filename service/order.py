from sqlalchemy.sql.expression import null
from flask_login import login_manager
from flask import session
import jwt
import bcrypt
import datetime
import repository as repo
import service
import model.order as order_model


class Order:
    def __init__(self):
        pass


    @classmethod
    def get_current_user_orders(cls, user_id):
        orders = repo.OrderRepository.get_orders(user_id)
        return orders


    @classmethod
    def get_order_detail(cls, order_id) -> dict:
        order = repo.OrderRepository.get_by_id(order_id)
        items = repo.OrderItemRepository.get_by_order_id(order.id)
        return {
            'order': order,
            'order_items': items,
        }

    @classmethod
    def get_item_by_order_id(cls, order_id) -> dict:
        items = repo.OrderItemRepository.get_by_order_id(order_id)

        return {
            'order_items': items,
        }

    @classmethod
    def create_order(cls, cart_id) -> dict:
        cart = service.Cart.get_current_cart()
        order = repo.OrderRepository.insert_order({
            'code': str(datetime.now()),
            'cart_id': cart_id,
            'owner_id': cart['cart'].owner_id
        })
        return order.json()