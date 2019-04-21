from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    access_key = Column(String, unique=True)
    personal_key = Column(String)
    storage_limit = Column(Integer, default=10737418240)  # 10 GB in bytes


class Transmissions(Base):
    TYPE_GET = 1
    TYPE_UPLOAD = 2

    __tablename__ = 'transmissions'

    id = Column(Integer, primary_key=True)
    transmission_key = Column(String, unique=True)
    transmission_type = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"),
                     nullable=False, unique=True)  # only one transmission is allowed at a time
    user = relation(Users)
