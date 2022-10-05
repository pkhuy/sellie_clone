import bcrypt
from .base import DBConnectionHandler
import model.product as product_entity
from typing import List
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.expression import text


class ProductRepository:
    @classmethod
    def insert_carts(cls, data) -> product_entity.Product:
        with DBConnectionHandler() as db_connection:
            try:
                hash_pass = bcrypt.hashpw(
                    data["password"].encode('utf-8'), bcrypt.gensalt())
                new_user = product_entity.Product(
                    name=data["name"], email=data["email"], password=hash_pass)
                db_connection.session.add(new_user)
                db_connection.session.commit()
                return product_entity.Product(
                    id=new_user.id, name=new_user.name, email=new_user.email
                ).get_as_json()
            except Exception as ex:
                db_connection.session.rollback()
                print(ex)
                raise
            finally:
                db_connection.session.close()


    @classmethod
    def get_all(cls)  -> product_entity.Product:
        with DBConnectionHandler() as db_connection:
            try:
                products = db_connection.session.query(product_entity.Product).all()
            except Exception as ex:
                db_connection.session.rollback()
                print(ex)
                raise
            finally:
                db_connection.session.close()\


    @classmethod
    def get_by_id(cls, product_id) -> product_entity.Product:
        with DBConnectionHandler() as db_connection:
            try:
                product = db_connection.session.query(product_entity.Product).filter_by(id=product_id).one()
                return product
            except Exception as ex:
                db_connection.session.rollback()
                print(ex)
                raise
            finally:
                db_connection.session.close()
