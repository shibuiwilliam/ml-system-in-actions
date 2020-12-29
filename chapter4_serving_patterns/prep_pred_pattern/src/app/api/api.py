from typing import Dict, List, Any
import base64
import io
from PIL import Image
from logging import getLogger

from src.ml.prediction import classifier, Data

logger = getLogger(__name__)


def health() -> Dict[str, str]:
    return {"health": "ok"}


def health_sync() -> Dict[str, str]:
    return health()


async def health_async_api() -> Dict[str, str]:
    return health()


def metadata() -> Dict[str, Any]:
    return {
        "data_type": "str",
        "data_structure": "(1,1)",
        "data_sample": "base64 encoded image file",
        "prediction_type": "float32",
        "prediction_structure": "(1,1000)",
        "prediction_sample": "[0.07093159, 0.01558308, 0.01348537, ...]",
    }


def label() -> Dict[int, str]:
    return classifier.label


async def predict_test() -> Dict[str, List[float]]:
    prediction = await classifier.predict(data=Data().data)
    return {"prediction": list(prediction)}


async def predict_test_label() -> Dict[str, str]:
    prediction = await classifier.predict_label(data=Data().data)
    return {"prediction": prediction}


async def predict(data: Data) -> Dict[str, List[float]]:
    image = base64.b64decode(str(data.data))
    io_bytes = io.BytesIO(image)
    image_data = Image.open(io_bytes)
    prediction = classifier.predict(data=image_data)
    return {"prediction": list(prediction)}


async def predict_label(data: Data) -> Dict[str, str]:
    prediction = await classifier.predict_label(data.data)
    return {"prediction": prediction}
