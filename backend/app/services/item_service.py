from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.item import Item
from app.schemas.item import ItemCreate, ItemResponse


async def get_all_items(db: AsyncSession) -> list[ItemResponse]:
    result = await db.execute(select(Item))
    items = result.scalars().all()
    return [ItemResponse.model_validate(item) for item in items]


async def get_item_by_id(item_id: int, db: AsyncSession) -> ItemResponse:
    result = await db.execute(select(Item).where(Item.id == item_id))
    item = result.scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return ItemResponse.model_validate(item)


async def create_item(data: ItemCreate, db: AsyncSession) -> ItemResponse:
    item = Item(name=data.name, description=data.description)
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return ItemResponse.model_validate(item)


async def delete_item(item_id: int, db: AsyncSession) -> None:
    result = await db.execute(select(Item).where(Item.id == item_id))
    item = result.scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    await db.delete(item)
    await db.commit()
