import bcrypt
from .base import DBConnectionHandler
import model.order_item as order_item_entity
from typing import List
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.expression import text


class OrderItemRepository:
    # @classmethod
    # def insert_carts(cls, data) -> model.Cart:
    #     with DBConnectionHandler() as db_connection:
    #         try:
    #             hash_pass = bcrypt.hashpw(
    #                 data["password"].encode('utf-8'), bcrypt.gensalt())
    #             new_user = UserModel(
    #                 name=data["name"], email=data["email"], password=hash_pass)
    #             db_connection.session.add(new_user)
    #             db_connection.session.commit()
    #             return User(
    #                 id=new_user.id, name=new_user.name, email=new_user.email
    #             ).get_as_json()
    #         except Exception as ex:
    #             db_connection.session.rollback()
    #             print(ex)
    #             raise
    #         finally:
    #             db_connection.session.close()

    # @classmethod
    # def get_by_id(cls, id) -> model.Cart:
    #     db_conn = DBConnectionHandler()
    #     datas = db_conn.execute(text("""SELECT * FROM carts WHERE id = """))
    #     print(type(datas))
    #     json_datas = {}
    #     for data in datas:
    #         print(type(data))
    #         json_datas[str(data.name)] = User(
    #             data.id, data.name, data.email).get_as_json()
    #     return json_datas


    @classmethod
    def get_by_order_id(cls, order_id) -> List[order_item_entity.OrderItem]:
        with DBConnectionHandler() as db_connection:
            try:
                cart_items = (
                    db_connection.session.query(order_item_entity.OrderItem)
                    .filter_by(order_id=order_id)
                    .all()
                )
                return cart_items

            except NoResultFound:
                return []
            except Exception as ex:
                db_connection.session.rollback()
                print(ex)
                raise
            finally:
                db_connection.session.close()
