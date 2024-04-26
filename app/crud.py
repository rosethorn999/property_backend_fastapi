from typing import List
from uuid import UUID
from sqlalchemy import desc, select, func
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from . import models, schemas
from fastapi import HTTPException, status


async def get_user(db_session: AsyncSession, user_id: UUID):
    result = await db_session.execute(
        select(models.User)
        .filter(models.User.id == user_id)
        .options(selectinload(models.User.contract))
    )
    return result.scalars().first()


async def get_users_count(db_session: AsyncSession) -> int:
    query = select(func.count()).select_from(models.User)
    result = await db_session.execute(query)
    c = result.scalar_one()
    return c


def get_user_by_email(db_session: Session, email: str):
    return db_session.query(models.User).filter(models.User.email == email).first()


async def get_users(db_session: Session, skip: int = 0, limit: int = 100):
    query = select(models.User).options(selectinload(models.User.contract))
    query = query.offset(skip).limit(limit)
    result = await db_session.execute(query)
    return result.unique().scalars().all()


def create_user(db_session: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db_session.add(db_user)
    db_session.commit()
    db_session.refresh(db_user)
    return db_user


async def get_products_group_by_county(db_session: AsyncSession):
    query = (
        select(models.Product.county, func.sum(models.Product.inventory))
        .group_by(models.Product.county)
        .where(models.Product.inventory > 0)
        .order_by(desc(func.sum(models.Product.inventory)))
    )
    result = await db_session.execute(query)
    return result.all()


async def get_products_count(db_session: AsyncSession, q=None, county=None) -> int:
    query = select(func.count()).select_from(models.Product)
    if q:
        query = query.filter(models.Product.title.like(f"%{q}%"))
    if county:
        query = query.filter(models.Product.county == county)
    result = await db_session.execute(query)
    c = result.scalar_one()
    return c


async def get_products(
    db_session: AsyncSession, q=None, county=None, skip: int = 0, limit: int = 10
) -> List[schemas.Product]:
    query = select(models.Product)
    if q:
        query = query.filter(models.Product.title.like(f"%{q}%"))
    if county:
        query = query.filter(models.Product.county == county)

    query = query.offset(skip).limit(limit)
    result = await db_session.execute(query)
    return result.scalars().all()


async def get_contract_by_id(id: int, db_session: AsyncSession) -> schemas.Product:
    result = await db_session.execute(
        select(models.Product).filter(models.Product.id == id)
    )
    return result.scalars().first()


async def create_user_contract(
    db_session: Session, contract: schemas.ProductCreate, user_id: UUID
) -> schemas.Product:
    db_contract = models.Product(**contract.model_dump(), creator_id=user_id)
    db_session.add(db_contract)
    await db_session.commit()
    await db_session.flush()
    result = await db_session.scalars(
        select(models.Product)
        .filter(models.Product.id == db_contract.id)
        .options(selectinload(models.Product.creator))
    )
    return result.first()


async def read_user_products(
    db_session: AsyncSession, user_id: str, skip: int = 0, limit: int = 10
) -> List[schemas.Product]:
    query = (
        select(models.Product)
        .filter(models.Product.creator_id == user_id)
        .options(selectinload(models.Product.creator))
    )
    query = query.offset(skip).limit(limit)
    result = await db_session.execute(query)
    return result.scalars().all()


async def update_contract(
    db_session: AsyncSession,
    contract_id: str,
    update_contract: schemas.Product,
    user: models.User,
) -> schemas.Product:
    contract = await db_session.get(models.Product, contract_id)
    if not contract:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    if user.id != contract.creator_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    contract.title = update_contract.title
    contract.monthly_rental = update_contract.monthly_rental
    contract.processing_fee = update_contract.processing_fee
    contract.store = update_contract.store
    contract.county = update_contract.county
    contract.district = update_contract.district
    contract.description = update_contract.description
    contract.inventory = update_contract.inventory
    contract.expiry_date = update_contract.expiry_date
    contract.gym_type = update_contract.gym_type
    contract.features = update_contract.features
    contract.modify_time = datetime.now()

    await db_session.commit()
    result = await db_session.scalars(
        select(models.Product)
        .filter(models.Product.id == contract.id)
        .options(selectinload(models.Product.creator))
    )
    return result.first()
