from datetime import date, datetime
from flask_login import UserMixin
from flask_bcrypt import Bcrypt
from sqlalchemy.sql.schema import ForeignKey, Table
from .base import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from flask_login import LoginManager


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    img_url = Column(String(200))

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'img_url': self.img_url
        }
