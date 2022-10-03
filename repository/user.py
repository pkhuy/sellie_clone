import bcrypt
import model.user as model_user
from .base import DBConnectionHandler
# from database.model import model.User as model.UserModel
from typing import List
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.expression import text


class UserRepository:
    @classmethod
    def insert_user(cls, data) -> model_user.User:
        with DBConnectionHandler() as db_connection:
            try:
                hash_pass = bcrypt.hashpw(
                    data["password"].encode('utf-8'), bcrypt.gensalt())
                new_user = model.UserModel(
                    name=data["name"], email=data["email"], password=hash_pass)
                db_connection.session.add(new_user)
                db_connection.session.commit()
                return model.User(
                    id=new_user.id, name=new_user.name, email=new_user.email
                ).get_as_json()
            except Exception as ex:
                db_connection.session.rollback()
                print(ex)
                raise
            finally:
                db_connection.session.close()

    @classmethod
    def select_all(cls) -> List[model_user.User]:
        db_conn = DBConnectionHandler()
        datas = db_conn.execute(text("""SELECT * FROM model.Users"""))
        print(type(datas))
        json_datas = {}
        for data in datas:
            print(type(data))
            json_datas[str(data.name)] = model_user.User(
                data.id, data.name, data.email).get_as_json()
        return json_datas

    @classmethod
    def select(cls, data) -> List[model_user.User]:

        with DBConnectionHandler() as db_connection:
            try:
                user = (
                    db_connection.session.query(model_user.User)
                    .filter_by(email=str(data["email"]))
                    .one()
                )
                print(user.password)
                print(str(data["password"]).encode('utf-8'))
                if str(data["password"]) == user.password:
                # if bcrypt.checkpw(str(data["password"]).encode('utf-8'), user.password):
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

    # @classmethod
    # def select_by_id(cls, id: int) -> model.User:
    #     db_conn = DBConnectionHandler()
    #     data = db_conn.execute(text("""SELECT * FROM model.Users WHERE id={}""".format(id))).fetchone()
    #     json_data = model.User(id, data.name, data.email, data.password).get_as_json()
    #     return json_data
    #
    # @classmethod
    # def select_by_email(cls, email: str) -> model.User:
    #     db_conn = DBConnectionHandler()
    #     data = db_conn.execute(
    #         text("""SELECT * FROM model.Users WHERE email='{}'""".format(email))).fetchone()
    #     if data is None:
    #         return None
    #     return model.User(id, data.name, data.email,
    #                       data.password).get_as_json()

    @classmethod
    def loaded_user(cls, id: int) -> model_user.User:
        with DBConnectionHandler() as db_connection:
            try:
                data = None

                if id:
                    # Select model.User by id
                    with DBConnectionHandler() as db_connection:
                        data = (
                            db_connection.session.query(model_user.User)
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
    #
    # @classmethod
    # def update(cls, data) -> model.User:
    #
    #     with DBConnectionHandler() as db_connection:
    #         try:
    #             json_data = None
    #             id = int(data["id"])
    #             model.User = db_connection.session.query(
    #                 model.UserModel).filter_by(id=id).one()
    #             model.User.name = data["name"]
    #             model.User.email = data["email"]
    #             model.User.password = bcrypt.hashpw(
    #                 data["password"].encode('utf-8'), bcrypt.gensalt())
    #             db_connection.session.commit()
    #
    #             data = db_connection.session.query(
    #                 model.UserModel).filter_by(id=id).one()
    #             json_data = model.User(
    #                 data.id, data.name, data.email, data.password).get_as_json()
    #             return json_data
    #
    #         except NoResultFound:
    #             return []
    #         except Exception as ex:
    #             db_connection.session.rollback()
    #             print(ex)
    #             raise
    #         finally:
    #             db_connection.session.close()
    #
    # # Not done yet
    # @classmethod
    # def get_permission(cls, entity: str) -> model.UserModel:
    #     with DBConnectionHandler() as db_connection:
    #         try:
    #             data = None
    #
    #             if id:
    #                 # Select model.User by id
    #                 with DBConnectionHandler() as db_connection:
    #                     data = (
    #                         db_connection.session.query(model.UserModel)
    #                         .filter_by(id=id)
    #                         .one()
    #                     )
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
    #
    # @classmethod
    # def drop_row(cls, id) -> bool:
    #
    #     with DBConnectionHandler() as db_connection:
    #         dropable = False
    #         try:
    #             if id:
    #                 data = db_connection.session.query(
    #                     model.UserModel).filter_by(id=id).one()
    #                 db_connection.session.delete(data)
    #                 db_connection.session.commit()
    #         except NoResultFound:
    #             return dropable
    #         except Exception as ex:
    #             db_connection.session.rollback()
    #             print(ex)
    #             raise
    #         finally:
    #             db_connection.session.close()
