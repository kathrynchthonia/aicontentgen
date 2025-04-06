from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=schemas.ItemsPublic)
async def read_items(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    items = await crud.item.get_multi(db=db, skip=skip, limit=limit)
    total = await crud.item.count(db=db)
    return schemas.ItemsPublic(data=items, count=total)


@router.post("/", response_model=schemas.ItemPublic)
async def create_item(
    *,
    db: AsyncSession = Depends(deps.get_db),
    item_in: schemas.ItemCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    return await crud.item.create_with_owner(db=db, obj_in=item_in, owner_id=current_user.id)


@router.get("/{id}", response_model=schemas.ItemPublic)
async def read_item(
    id: UUID,
    db: AsyncSession = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    item = await crud.item.get(db=db, id=id)
    if not item or (item.owner_id != current_user.id and not current_user.is_superuser):
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.put("/{id}", response_model=schemas.ItemPublic)
async def update_item(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: UUID,
    item_in: schemas.ItemUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    item = await crud.item.get(db=db, id=id)
    if not item or (item.owner_id != current_user.id and not current_user.is_superuser):
        raise HTTPException(status_code=404, detail="Item not found")
    return await crud.item.update(db=db, db_obj=item, obj_in=item_in)


@router.delete("/{id}", response_model=schemas.ItemPublic)
async def delete_item(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: UUID,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    item = await crud.item.get(db=db, id=id)
    if not item or (item.owner_id != current_user.id and not current_user.is_superuser):
        raise HTTPException(status_code=404, detail="Item not found")
    return await crud.item.remove(db=db, id=id)
