from typing import Any

from pydantic import BaseModel
from src.api_composition_proxy.configurations import ModelConfigurations


class Data(BaseModel):
    image_data: Any = ModelConfigurations.sample_image
