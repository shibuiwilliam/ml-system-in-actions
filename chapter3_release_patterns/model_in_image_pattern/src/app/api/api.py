from typing import Dict, List, Any
from src.ml.prediction import classifier, Data

from logging import getLogger

logger = getLogger(__name__)


def health() -> Dict[str, str]:
    return {"health": "ok"}


def health_sync() -> Dict[str, str]:
    return health()


async def health_async_api() -> Dict[str, str]:
    return health()


def metadata() -> Dict[str, Any]:
    return {
        "data_type": "float32",
        "data_structure": "(1,4)",
        "data_sample": Data().data,
        "prediction_type": "float32",
        "prediction_structure": "(1,3)",
        "prediction_sample": [0.97093159, 0.01558308, 0.01348537],
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
    prediction = await classifier.predict(data.data)
    return {"prediction": list(prediction)}


async def predict_label(data: Data) -> Dict[str, str]:
    prediction = await classifier.predict_label(data.data)
    return {"prediction": prediction}
