import bcrypt
from .base import DBConnectionHandler
import model.order as order_entity
from typing import List
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.expression import text


class OrderRepository:
    @classmethod
    def insert_carts(cls, data) -> order_entity.Order:
        with DBConnectionHandler() as db_connection:
            try:
                hash_pass = bcrypt.hashpw(
                    data["password"].encode('utf-8'), bcrypt.gensalt())
                new_user = order_entity.Order(
                    name=data["name"], email=data["email"], password=hash_pass)
                db_connection.session.add(new_user)
                db_connection.session.commit()
                return order_entity.Order(
                    id=new_user.id, name=new_user.name, email=new_user.email
                ).get_as_json()
            except Exception as ex:
                db_connection.session.rollback()
                print(ex)
                raise
            finally:
                db_connection.session.close()
