from sqlalchemy.sql.expression import null
from flask_login import login_manager
from flask import session
import jwt
import bcrypt
import datetime
import repository as repo


class Cart:
    def __init__(self):
        pass

    def check_email_existed(self, email):
        res = self.user_repository.select_by_email(email)
        if res is None:
            return True
        else:
            return False

    def register(self, request):
        name = request["name"]
        email = request['email']
        password = request['password']

        new_user = self.user_repository.insert_user({"name":name, "email":email, "password":password})
        group_response = self.user_group_repository.insert(new_user["id"], 4) #4 for register user group

        return {"data": new_user}

    @classmethod
    def login(cls, data):
        # user = self.user_repository.select(data)
        user = repository.UserRepository.select(data)
        if user is not None:
            token = jwt.encode({
                "email": data["email"],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)},
                "secretkey",
                algorithm="HS256"
            )
            session["token"] = token
            print(token)
            return user
        return None

    @classmethod
    def loaded_user(cls, user_id):
        return repository.UserRepository.loaded_user(user_id)

    @classmethod
    def get_current_cart(cls, current_user_id) -> dict:
        cart = repo.CartRepository.get_carts(current_user_id)[0]
        cart_items = repo.CartItemRepository.get_by_cart_id(cart.id)
        for item in cart_items:
            print(item.cart_id)
            print(item.id)
            print(item.product_id)
            product = repo.ProductRepository.get_by_id(item.product_id.expression.foreign_keys.pop())
            item["name"] = product.name
            item["code"] = product.code
        return {
            "cart": cart,
            "cart_items": cart_items,
        }
