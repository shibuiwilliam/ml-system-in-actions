from typing import Dict, List, Any
import uuid
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
    job_id = str(uuid.uuid4())
    prediction = await classifier.predict(data=Data().data)
    prediction_list = list(prediction)
    logger.info(f"test {job_id}: {prediction_list}")
    return {"prediction": prediction_list}


async def predict_test_label() -> Dict[str, str]:
    job_id = str(uuid.uuid4())
    prediction = await classifier.predict_label(data=Data().data)
    logger.info(f"test {job_id}: {prediction}")
    return {"prediction": prediction}


async def predict(data: Data) -> Dict[str, List[float]]:
    job_id = str(uuid.uuid4())
    prediction = await classifier.predict(data.data)
    prediction_list = list(prediction)
    logger.info(f"{job_id}: {prediction_list}")
    return {"prediction": prediction_list}


async def predict_label(data: Data) -> Dict[str, str]:
    job_id = str(uuid.uuid4())
    prediction = await classifier.predict_label(data.data)
    logger.info(f"test {job_id}: {prediction}")
    return {"prediction": prediction}
