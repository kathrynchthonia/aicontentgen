from typing import Optional, List
from uuid import uuid4
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlmodel import SQLModel


# --------------------------
# SQLAlchemy DB Models
# --------------------------

class User(SQLModel, table=True):
    __tablename__ = "user"

    id: Mapped[str] = mapped_column(primary_key=True, default_factory=lambda: str(uuid4()))
    email: Mapped[str] = mapped_column(index=True, unique=True, nullable=False)
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    full_name: Mapped[Optional[str]] = mapped_column(default=None)

    items: Mapped[List["Item"]] = relationship(back_populates="owner")

    model_config = {
        "arbitrary_types_allowed": True
    }


class Item(SQLModel, table=True):
    __tablename__ = "item"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(index=True)
    description: Mapped[Optional[str]]
    owner_id: Mapped[str] = mapped_column(ForeignKey("user.id"))
    owner: Mapped[User] = relationship(back_populates="items")

    model_config = {
        "arbitrary_types_allowed": True
    }

# --------------------------
# Pydantic Schema Config
# --------------------------

class CustomModelConfig:
    from_attributes = True
    arbitrary_types_allowed = True


# --------------------------
# Pydantic Schemas
# --------------------------

# --- User Schemas ---

class UserBase(BaseModel):
    email: EmailStr
    role: Optional[str] = "user"


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[str] = None


class UserRead(UserBase):
    id: str

    model_config = CustomModelConfig


# --- Item Schemas ---

class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class ItemRead(ItemBase):
    id: int
    owner_id: str

    model_config = CustomModelConfig
