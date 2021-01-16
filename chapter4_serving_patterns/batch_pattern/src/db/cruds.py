import datetime
from typing import Dict, List

from sqlalchemy.orm import Session
from src.db import models, schemas


def select_all_items(db: Session) -> List[schemas.Item]:
    return db.query(models.Item).all()


def select_without_prediction(db: Session) -> List[schemas.Item]:
    return db.query(models.Item).filter(models.Item.prediction == None).all()


def select_with_prediction(db: Session) -> List[schemas.Item]:
    return db.query(models.Item).filter(models.Item.prediction != None).all()


def select_by_id(db: Session, id: int) -> schemas.Item:
    return db.query(models.Item).filter(models.Item.id == id).first()


def register_item(db: Session, item: schemas.ItemBase, commit: bool = True):
    _item = models.Item(values=item.values)
    db.add(_item)
    if commit:
        db.commit()
        db.refresh(_item)


def register_items(db: Session, items: List[schemas.ItemBase], commit: bool = True):
    for item in items:
        register_item(db=db, item=item, commit=commit)


def register_predictions(db: Session, predictions: Dict[int, Dict[str, float]], commit: bool = True):
    for id, prediction in predictions.items():
        item = select_by_id(db=db, id=id)
        item.prediction = prediction
        if commit:
            db.commit()
            db.refresh(item)
