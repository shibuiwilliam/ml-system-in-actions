from logging import getLogger

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.db import cruds
from src.db.database import get_db

logger = getLogger(__name__)
router = APIRouter()


@router.get("/health")
def health():
    return {"health": "ok"}


@router.get("/data/all")
def data_all(db: Session = Depends(get_db)):
    return cruds.select_all_items(db=db)


@router.get("/data/predicted")
def data_predicted(db: Session = Depends(get_db)):
    return cruds.select_with_prediction(db=db)


@router.get("/data/unpredicted")
def data_unpredicted(db: Session = Depends(get_db)):
    return cruds.select_without_prediction(db=db)
