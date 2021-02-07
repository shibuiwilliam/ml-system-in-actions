import uuid
from logging import getLogger
from typing import Any, Dict, List

from fastapi import APIRouter
from src.ml.prediction import Data, classifier
from src.utils.profiler import log_decorator

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


@log_decorator(endpoint="/predict-test", logger=logger)
def _predict_test(job_id: str) -> Dict[str, Any]:
    logger.info(f"execute: [{job_id}]")
    prediction = classifier.predict(data=Data().data)
    prediction_list = list(prediction)
    return {
        "job_id": job_id,
        "prediction": prediction_list,
    }


@router.get("/predict-test/{job_id}")
def predict_test(job_id: str = str(uuid.uuid4())[:6]) -> Dict[str, Any]:
    return _predict_test(job_id=job_id)


@log_decorator(endpoint="/predict-test-label", logger=logger)
def _predict_test_label(job_id: str) -> Dict[str, Any]:
    logger.info(f"execute: [{job_id}]")
    prediction = classifier.predict_label(data=Data().data)
    return {
        "job_id": job_id,
        "prediction": prediction,
    }


@router.get("/predict-test-label/{job_id}")
def predict_test_label(job_id: str = str(uuid.uuid4())[:6]) -> Dict[str, Any]:
    return _predict_test_label(job_id=job_id)


@log_decorator(endpoint="/predict", logger=logger)
def _predict(data: Data, job_id: str) -> Dict[str, Any]:
    logger.info(f"execute: [{job_id}]")
    prediction = classifier.predict(data.data)
    prediction_list = list(prediction)
    return {
        "job_id": job_id,
        "prediction": prediction_list,
    }


@router.post("/predict/{job_id}")
def predict(data: Data, job_id: str = str(uuid.uuid4())[:6]) -> Dict[str, Any]:
    return _predict(data=data, job_id=job_id)


@log_decorator(endpoint="/predict-label", logger=logger)
def _predict_label(data: Data, job_id: str) -> Dict[str, str]:
    logger.info(f"execute: [{job_id}]")
    prediction = classifier.predict_label(data.data)
    return {
        "job_id": job_id,
        "prediction": prediction,
    }


@router.post("/predict-label/{job_id}")
def predict_label(data: Data, job_id: str = str(uuid.uuid4())[:6]) -> Dict[str, Any]:
    return _predict_label(data=data, job_id=job_id)
