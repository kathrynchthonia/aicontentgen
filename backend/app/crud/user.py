from typing import Optional, List
from sqlmodel import select, Session
from app.models import User, UserCreate, UserUpdate
from app.core.security import get_password_hash


def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
    return db.exec(select(User).where(User.id == user_id)).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.exec(select(User).where(User.email == email)).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.exec(select(User).offset(skip).limit(limit)).all()


def create_user(db: Session, user_create: UserCreate) -> User:
    hashed_password = get_password_hash(user_create.password)
    user = User(
        email=user_create.email,
        full_name=user_create.full_name,
        hashed_password=hashed_password,
        is_active=True,
        is_superuser=user_create.is_superuser,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, db_user: User, user_in: UserUpdate) -> User:
    user_data = user_in.dict(exclude_unset=True)
    for field, value in user_data.items():
        setattr(db_user, field, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: str) -> None:
    user = get_user_by_id(db, user_id)
    if user:
        db.delete(user)
        db.commit()
