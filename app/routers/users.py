import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from app import crud, schemas
from app.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User
from app.users import current_active_verified_user

router = APIRouter()


@router.get(
    "/users-simple/",
    tags=["users"],
    response_model=schemas.Pagination[schemas.UserReadSimple],
)
async def read_users(
    page: int = 1,
    page_size: int = 10,
    db_session: AsyncSession = Depends(get_async_session),
):
    c = await crud.get_users_count(db_session)
    skips = (page - 1) * page_size
    products = []  # await crud.get_users(db_session, skip=skips, limit=page_size)
    return {"count": c, "results": products}


@router.get(
    "/users-simple/{user_id}", tags=["users"], response_model=schemas.UserReadSimple
)
async def read_user(
    user_id: uuid.UUID,
    db_session: AsyncSession = Depends(get_async_session),
):
    db_user = await crud.get_user(db_session, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post(
    "/users/{user_id}/products", response_model=schemas.Product, tags=["users"]
)
async def create_contract_for_user(
    user_id: uuid.UUID,
    contract: schemas.ProductCreate,
    db_session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_verified_user),
):
    if user.id != user_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    return await crud.create_user_contract(
        db_session=db_session, contract=contract, user_id=user_id
    )


@router.get(
    "/users/{user_id}/products", response_model=list[schemas.Product], tags=["users"]
)
async def read_user_products(
    user_id: uuid.UUID,
    db_session: AsyncSession = Depends(get_async_session),
):
    return await crud.read_user_products(db_session=db_session, user_id=user_id)
