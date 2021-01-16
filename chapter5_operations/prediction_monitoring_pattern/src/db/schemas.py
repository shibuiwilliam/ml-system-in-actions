import datetime
from typing import Dict

from pydantic import BaseModel


class PredictionLogBase(BaseModel):
    log_id: str
    log: Dict


class PredictionLog(PredictionLogBase):
    created_datetime: datetime.datetime

    class Config:
        orm_mode = True


class OutlierLogBase(BaseModel):
    log_id: str
    log: Dict


class OutlierLog(OutlierLogBase):
    created_datetime: datetime.datetime

    class Config:
        orm_mode = True
