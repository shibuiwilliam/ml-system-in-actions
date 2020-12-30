from typing import Dict, List, Any
from logging import getLogger
from fastapi import BackgroundTasks
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
        "data_sample": Data().data,
        "prediction_type": "float32",
        "prediction_structure": "(1,1000)",
        "prediction_sample": "[0.07093159, 0.01558308, 0.01348537, ...]",
    }


def label() -> Dict[int, str]:
    return classifier.label


async def predict_test(background_tasks: BackgroundTasks) -> Dict[str, List[float]]:
    prediction = await classifier.predict(data=Data(), background_tasks=background_tasks)
    return {"prediction": list(prediction)}


async def predict_test_label(background_tasks: BackgroundTasks) -> Dict[str, str]:
    prediction = await classifier.predict_label(data=Data(), background_tasks=background_tasks)
    return {"prediction": prediction}


async def predict(data: Data, background_tasks: BackgroundTasks) -> Dict[str, List[float]]:
    prediction = await classifier.predict(data=data, background_tasks=background_tasks)
    return {"prediction": list(prediction)}


async def predict_label(data: Data, background_tasks: BackgroundTasks) -> Dict[str, str]:
    prediction = await classifier.predict_label(data=data, background_tasks=background_tasks)
    return {"prediction": prediction}
