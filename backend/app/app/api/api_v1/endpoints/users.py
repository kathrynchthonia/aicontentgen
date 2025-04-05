from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from uuid import UUID

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=schemas.UsersPublic)
async def read_users(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    users = await crud.user.get_multi(db=db, skip=skip, limit=limit)
    total = await crud.user.count(db=db)
    return schemas.UsersPublic(data=users, count=total)


@router.get("/me", response_model=schemas.UserPublic)
async def read_user_me(current_user: models.User = Depends(deps.get_current_active_user)) -> Any:
    return current_user


@router.get("/{user_id}", response_model=schemas.UserPublic)
async def read_user_by_id(
    user_id: UUID,
    db: AsyncSession = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    user = await crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
