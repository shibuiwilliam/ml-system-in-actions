import uuid
from logging import getLogger
from typing import Any, Dict, List

from fastapi import APIRouter
from src.configurations import ModelConfigurations
from src.ml.prediction import Data, classifier
from src.utils.profiler import wrap_time

logger = getLogger(__name__)
router = APIRouter()


@router.get("/health")
def health() -> Dict[str, str]:
    return {"health": "ok"}


@router.get("/metadata")
def metadata() -> Dict[str, Any]:
    return {
        "data_type": "float32",
        "data_structure": "(1,4)",
        "data_sample": Data().data,
        "prediction_type": "float32",
        "prediction_structure": "(1,3)",
        "prediction_sample": [0.97093159, 0.01558308, 0.01348537],
    }


@router.get("/label")
def label() -> Dict[int, str]:
    return classifier.label


@wrap_time(logger=logger)
def _predict_test(job_id: str) -> Dict[str, List[float]]:
    prediction = classifier.predict(data=Data().data)
    prediction_list = list(prediction)
    logger.info(f"{ModelConfigurations.mode} {job_id}: {prediction_list}")
    return {"prediction": prediction_list}


@router.get("/predict/test")
def predict_test() -> Dict[str, List[float]]:
    job_id = str(uuid.uuid4())[:6]
    return _predict_test(job_id=job_id)


@wrap_time(logger=logger)
def _predict_test_label(job_id: str) -> Dict[str, str]:
    prediction = classifier.predict_label(data=Data().data)
    logger.info(f"{ModelConfigurations.mode} {job_id}: {prediction}")
    return {"prediction": prediction}


@router.get("/predict/test/label")
def predict_test_label() -> Dict[str, str]:
    job_id = str(uuid.uuid4())[:6]
    return _predict_test_label(job_id=job_id)


@wrap_time(logger=logger)
def _predict(data: Data, job_id: str) -> Dict[str, List[float]]:
    prediction = classifier.predict(data.data)
    prediction_list = list(prediction)
    logger.info(f"{ModelConfigurations.mode} {job_id}: {prediction_list}")
    return {"prediction": prediction_list}


@router.post("/predict")
def predict(data: Data) -> Dict[str, List[float]]:
    job_id = str(uuid.uuid4())[:6]
    return _predict(data=data, job_id=job_id)


@wrap_time(logger=logger)
def _predict_label(data: Data, job_id: str) -> Dict[str, str]:
    prediction = classifier.predict_label(data.data)
    logger.info(f"{ModelConfigurations.mode} {job_id}: {prediction}")
    return {"prediction": prediction}


@router.post("/predict/label")
def predict_label(data: Data) -> Dict[str, str]:
    job_id = str(uuid.uuid4())[:6]
    return _predict_label(data=data, job_id=job_id)
