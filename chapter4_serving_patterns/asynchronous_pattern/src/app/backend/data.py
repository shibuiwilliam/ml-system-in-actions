from typing import Any

from pydantic import BaseModel


class Data(BaseModel):
    image_data: Any
