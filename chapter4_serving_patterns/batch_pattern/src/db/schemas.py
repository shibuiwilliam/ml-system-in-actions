import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class ItemBase(BaseModel):
    values: List[float]


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    prediction: Optional[Dict[str, float]]
    created_datetime: datetime.datetime
    updated_datetime: datetime.datetime

    class Config:
        orm_mode = True
