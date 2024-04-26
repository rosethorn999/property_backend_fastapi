from datetime import datetime, date
from typing import List, Optional, TypeVar
import uuid
from fastapi_users import schemas
from pydantic import BaseModel
from typing import Generic


T = TypeVar("T")


class ProductCountyScatter(BaseModel):
    county: str
    count: int


class UserReadSimple(BaseModel):
    id: uuid.UUID
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    county: Optional[str]
    district: Optional[str]

    mobile: Optional[str]
    facebook_id: Optional[str]
    line_id: Optional[str]

    modify_time: Optional[datetime]
    create_time: Optional[datetime]
    last_login: Optional[datetime]


class UserRead(schemas.BaseUser[uuid.UUID]):
    id: uuid.UUID
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    county: Optional[str]
    district: Optional[str]

    mobile: Optional[str]
    facebook_id: Optional[str]
    line_id: Optional[str]

    modify_time: Optional[datetime]
    create_time: Optional[datetime]
    last_login: Optional[datetime]


class UserCreate(schemas.BaseUserCreate):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    county: Optional[str] = None
    district: Optional[str] = None
    birth_date: Optional[date] = None

    mobile: Optional[str] = None
    facebook_id: Optional[str] = None
    line_id: Optional[str] = None


class UserUpdate(schemas.BaseUserUpdate):
    first_name: str
    last_name: str
    county: Optional[str]
    district: Optional[str]
    birth_date: Optional[date]

    mobile: Optional[str]
    facebook_id: Optional[str]
    line_id: Optional[str]


class ProductBase(BaseModel):
    title: str
    category: List[str]
    picture: str
    description: str
    price: float


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int
    # class Config:
    #     from_attributes = True


class Pagination(BaseModel, Generic[T]):
    count: int
    results: list[T]


# class UserBase(BaseModel):
#     email: str


# class UserCreate(UserBase):
#     password: str


# class User(UserBase):
#     id: int
#     is_active: bool
#     products: list[Product] = []

#     class Config:
#         from_attributes = True
