from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.schemas.item import ItemCreate, ItemResponse
from app.services.item_service import get_all_items, get_item_by_id, create_item, delete_item

router = APIRouter(prefix="/items", tags=["items"])

DbSession = Annotated[AsyncSession, Depends(get_session)]


@router.get("/", response_model=list[ItemResponse])
async def list_items(db: DbSession):
    return await get_all_items(db)


@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int, db: DbSession):
    return await get_item_by_id(item_id, db)


@router.post("/", response_model=ItemResponse, status_code=201)
async def create_item_endpoint(data: ItemCreate, db: DbSession):
    return await create_item(data, db)


@router.delete("/{item_id}", status_code=204)
async def delete_item_endpoint(item_id: int, db: DbSession):
    await delete_item(item_id, db)
