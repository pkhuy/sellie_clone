import bcrypt
from .base import DBConnectionHandler
import model.cart as cart_entity
from typing import List
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.expression import text


class CartRepository:
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
    def select(cls, data) -> List[cart_entity.Cart]:

        with DBConnectionHandler() as db_connection:
            try:
                user = (
                    db_connection.session.query(cart_entity.cart)
                    .filter_by(email=str(data["email"]))
                    .one()
                )
                if bcrypt.checkpw(str(data["password"]).encode('utf-8'), user.password):
                    return user
                else:
                    return None

            except NoResultFound:
                return []
            except Exception as ex:
                db_connection.session.rollback()
                print(ex)
                raise
            finally:
                db_connection.session.close()

    @classmethod
    def get_by_id(cls, id: int) -> cart_entity.Cart:
        db_conn = DBConnectionHandler()
        data = db_conn.execute(text("""SELECT * FROM carts WHERE id={}""".format(id))).fetchone()
        # json_data = User(id, data.name, data.email, data.password).get_as_json()
        return data

    @classmethod
    def select_by_email(cls, email: str) -> cart_entity.Cart:
        db_conn = DBConnectionHandler()
        data = db_conn.execute(
            text("""SELECT * FROM users WHERE email='{}'""".format(email))).fetchone()
        if data is None:
            return None
        return cart_entity.Cart(id, data.name, data.email,
                                data.password).get_as_json()


    @classmethod
    def loaded_user(cls, id: int) -> cart_entity.Cart:
        with DBConnectionHandler() as db_connection:
            try:
                data = None

                if id:
                    # Select user by id
                    with DBConnectionHandler() as db_connection:
                        data = (
                            db_connection.session.query(cart_entity.Cart)
                            .filter_by(id=id)
                            .one()
                        )

                return data

            except NoResultFound:
                return data
            except Exception as ex:
                db_connection.session.rollback()
                print(ex)
                raise
            finally:
                db_connection.session.close()

    @classmethod
    def update(cls, data) -> cart_entity.Cart:

        with DBConnectionHandler() as db_connection:
            try:
                json_data = None
                id = int(data["id"])
                user=db_connection.session.query(
                    cart_entity.cart).filter_by(id=id).one()
                user.name = data["name"]
                user.email = data["email"]
                user.password = bcrypt.hashpw(
                    data["password"].encode('utf-8'), bcrypt.gensalt())
                db_connection.session.commit()

                data = db_connection.session.query(
                    cart_entity.Cart).filter_by(id=id).one()
                json_data = cart_entity.Cart(
                    data.id, data.name, data.email, data.password).get_as_json()
                return json_data

            except NoResultFound:
                return []
            except Exception as ex:
                db_connection.session.rollback()
                print(ex)
                raise
            finally:
                db_connection.session.close()

    #Not done yet
    @classmethod
    def get_carts(cls, created_by_id) -> cart_entity.Cart:
        with DBConnectionHandler() as db_connection:
            try:
                data = db_connection.session.query(cart_entity.Cart).filter_by(created_by_id=created_by_id).all()

                return data

            except NoResultFound:
                return data
            except Exception as ex:
                db_connection.session.rollback()
                print(ex)
                raise
            finally:
                db_connection.session.close()

    # @classmethod
    # def get_cart_items(cls, cart_id) -> cart_entity.Cart:
    #     with DBConnectionHandler() as db_connection:
    #         try:
    #             data = db_connection.session.query(cart_item_entity.CartI).filter_by(cart_id=cart_id).all()
    #
    #             return data
    #
    #         except NoResultFound:
    #             return data
    #         except Exception as ex:
    #             db_connection.session.rollback()
    #             print(ex)
    #             raise
    #         finally:
    #             db_connection.session.close()

    @classmethod
    def drop_row(cls, id) -> bool:

        with DBConnectionHandler() as db_connection:
            dropable = False
            try:
                if id:
                    data = db_connection.session.query(
                        cart_entity.cart).filter_by(id=id).one()
                    db_connection.session.delete(data)
                    db_connection.session.commit()
            except NoResultFound:
                return dropable
            except Exception as ex:
                db_connection.session.rollback()
                print(ex)
                raise
            finally:
                db_connection.session.close()
