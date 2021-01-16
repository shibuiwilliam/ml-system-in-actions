from typing import List

from pydantic import BaseModel


class Data(BaseModel):
    data: List[List[float]] = [[5.1, 3.5, 1.4, 0.2]]
