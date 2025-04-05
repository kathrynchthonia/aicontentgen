from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models import Item
from app.schemas import ItemCreate, ItemUpdate


class CRUDItem:
    async def get(self, db: AsyncSession, id: UUID) -> Optional[Item]:
        result = await db.execute(select(Item).where(Item.id == id))
        return result.scalar_one_or_none()

    async def get_multi(self, db: AsyncSession, skip=0, limit=100) -> list[Item]:
        result = await db.execute(select(Item).offset(skip).limit(limit))
        return result.scalars().all()

    async def count(self, db: AsyncSession) -> int:
        result = await db.execute(select(Item))
        return len(result.scalars().all())

    async def create_with_owner(self, db: AsyncSession, obj_in: ItemCreate, owner_id: UUID) -> Item:
        db_obj = Item(**obj_in.dict(), owner_id=owner_id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, db_obj: Item, obj_in: ItemUpdate) -> Item:
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, id: UUID) -> Optional[Item]:
        db_obj = await self.get(db, id=id)
        if db_obj:
            await db.delete(db_obj)
            await db.commit()
        return db_obj


item = CRUDItem()
