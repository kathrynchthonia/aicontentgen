from typing import Optional, List
from sqlmodel import select, Session
from app.models.schemas import Item, ItemCreate, ItemUpdate


def get_item_by_id(db: Session, item_id: str) -> Optional[Item]:
    return db.exec(select(Item).where(Item.id == item_id)).first()


def get_items(db: Session, skip: int = 0, limit: int = 100) -> List[Item]:
    return db.exec(select(Item).offset(skip).limit(limit)).all()


def create_item(db: Session, item_in: ItemCreate, owner_id: str) -> Item:
    item = Item(**item_in.dict(), owner_id=owner_id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update_item(db: Session, db_item: Item, item_in: ItemUpdate) -> Item:
    item_data = item_in.dict(exclude_unset=True)
    for field, value in item_data.items():
        setattr(db_item, field, value)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_item(db: Session, item_id: str) -> None:
    item = get_item_by_id(db, item_id)
    if item:
        db.delete(item)
        db.commit()
