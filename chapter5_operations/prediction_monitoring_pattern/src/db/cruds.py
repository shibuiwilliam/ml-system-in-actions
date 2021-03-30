from typing import Dict, List

from sqlalchemy.orm import Session
from src.db import models, schemas


def select_prediction_log_all(db: Session) -> List[schemas.PredictionLog]:
    return db.query(models.PredictionLog).all()


def select_prediction_log_between(
    db: Session,
    time_before: str,
    time_later: str,
) -> List[schemas.PredictionLog]:
    return (
        db.query(models.PredictionLog)
        .filter(models.PredictionLog.created_datetime >= time_before)
        .filter(models.PredictionLog.created_datetime <= time_later)
        .all()
    )


def select_outlier_log_all(db: Session) -> List[schemas.OutlierLog]:
    return db.query(models.OutlierLog).all()


def select_outlier_log_between(
    db: Session,
    time_before: str,
    time_later: str,
) -> List[schemas.OutlierLog]:
    return (
        db.query(models.OutlierLog)
        .filter(models.OutlierLog.created_datetime >= time_before)
        .filter(models.OutlierLog.created_datetime <= time_later)
        .all()
    )


def add_prediction_log(
    db: Session,
    log_id: str,
    log: Dict,
    commit: bool = True,
) -> schemas.PredictionLog:
    data = models.PredictionLog(
        log_id=log_id,
        log=log,
    )
    db.add(data)
    if commit:
        db.commit()
        db.refresh(data)
    return data


def add_outlier_log(
    db: Session,
    log_id: str,
    log: Dict,
    commit: bool = True,
) -> schemas.OutlierLog:
    data = models.OutlierLog(
        log_id=log_id,
        log=log,
    )
    db.add(data)
    if commit:
        db.commit()
        db.refresh(data)
    return data
