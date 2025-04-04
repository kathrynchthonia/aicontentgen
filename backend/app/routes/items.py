from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.ItemResponse)
def create_item(item: schemas.ItemCreate, user_id: int, db: Session = Depends(get_db)):
    return crud.create_item(db, item, user_id)

@router.get("/", response_model=list[schemas.ItemResponse])
def get_items(db: Session = Depends(get_db)):
    return crud.get_items(db)
