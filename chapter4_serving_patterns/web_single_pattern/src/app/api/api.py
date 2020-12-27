from typing import Dict, List
from utils.profiler import do_cprofile
from src.ml.prediction import classifier, Data

from logging import getLogger

logger = getLogger(__name__)


@do_cprofile
def health() -> Dict[str, str]:
    return {"health": "ok"}


def health_sync() -> Dict[str, str]:
    return health()


async def health_async_api() -> Dict[str, str]:
    return health()


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
