from typing import List
from sqlalchemy import ARRAY, Column, ForeignKey, Integer, String, DateTime, Uuid, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, Mapped
from fastapi_users.db import (
    SQLAlchemyBaseOAuthAccountTableUUID,
    SQLAlchemyBaseUserTableUUID,
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class OAuthAccount(SQLAlchemyBaseOAuthAccountTableUUID, Base):
    pass


class User(SQLAlchemyBaseUserTableUUID, Base):
    __table_args__ = {"extend_existing": True}

    first_name: str = Column(String(length=1024), nullable=True)
    last_name = Column(String, nullable=True)
    county = Column(String, nullable=True)
    district = Column(String, nullable=True)
    birth_date = Column(Date(), nullable=True)

    facebook_id = Column(String, nullable=True)
    line_id = Column(String, nullable=True)
    mobile = Column(String, nullable=True)

    modify_time = Column(DateTime(timezone=True), nullable=True)
    create_time = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(), nullable=True)
    oauth_accounts: Mapped[List[OAuthAccount]] = relationship(
        "OAuthAccount", lazy="joined"
    )


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    stock = Column(Integer)
    price = Column(Integer)
    category = Column(ARRAY(String))
    picture = Column(String)
