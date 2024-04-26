from fastapi import APIRouter, Depends
from app.users import current_active_verified_user
from app import crud, schemas
from app.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User

router = APIRouter()


@router.get(
    "/products",
    tags=["products"],
    response_model=schemas.Pagination[schemas.Product],
)
async def read_products(
    q=None,
    county=None,
    page: int = 1,
    page_size: int = 10,
    db_session: AsyncSession = Depends(get_async_session),
):
    c = await crud.get_products_count(db_session, q, county)
    skips = (page - 1) * page_size
    products = await crud.get_products(
        db_session, q, county, skip=skips, limit=page_size
    )
    return {"count": c, "results": products}


@router.get(
    "/products/group-by-county",
    tags=["products"],
    response_model=list[schemas.ProductCountyScatter],
)
async def get_products_group_by_county(
    db_session: AsyncSession = Depends(get_async_session),
):
    products = await crud.get_products_group_by_county(db_session)
    return [
        schemas.ProductCountyScatter(county=contract[0], count=contract[1])
        for contract in products
    ]


@router.get("/products/{id}", tags=["products"], response_model=schemas.Product)
async def get_contract_by_id(
    id: int, db_session: AsyncSession = Depends(get_async_session)
):
    contract = await crud.get_contract_by_id(id, db_session)
    return contract


@router.put("/products/{id}", tags=["products"], response_model=schemas.Product)
async def update_contract(
    id: int,
    contract: schemas.Product,
    db_session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_verified_user),
):
    contract = await crud.update_contract(
        db_session, contract_id=id, update_contract=contract, user=user
    )
    return contract
