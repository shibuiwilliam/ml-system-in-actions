from typing import Dict, List, Any
from src.ml.prediction import classifier, Data
from src.configurations import ModelConfigurations

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
        "prediction_structure": "(1,2)",
        "prediction_sample": [0.970000, 0.030000],
    }


async def predict_test() -> Dict[str, List[float]]:
    prediction = await classifier.predict(data=Data().data)
    prediction_list = list(prediction)
    logger.info(f"{ModelConfigurations.mode_name} {id}: {prediction_list}")
    return {"prediction": prediction_list}


async def predict(data: Data) -> Dict[str, List[float]]:
    prediction = await classifier.predict(data.data)
    prediction_list = list(prediction)
    logger.info(f"{ModelConfigurations.mode_name} {id}: {prediction_list}")
    return {"prediction": prediction_list}
