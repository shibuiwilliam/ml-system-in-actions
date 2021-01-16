import uuid
from logging import getLogger
from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException
from src.ml.data import Data
from src.ml.outlier_detection import outlier_detector
from src.ml.prediction import classifier
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
        "outlier_type": "bool, float32",
        "outlier_structure": "(1,2)",
        "outlier_sample": [False, 0.4],
    }


@router.get("/label")
def label() -> Dict[int, str]:
    return classifier.label


@log_decorator(endpoint="/predict/test", logger=logger)
def _predict_test(job_id: str) -> Dict[str, Any]:
    logger.info(f"execute: [{job_id}]")
    prediction = classifier.predict(data=Data().data)
    is_outlier, outlier_score = outlier_detector.predict(data=Data().data)
    prediction_list = list(prediction)
    return {
        "job_id": job_id,
        "prediction": prediction_list,
        "is_outlier": is_outlier,
        "outlier_score": outlier_score,
    }


@router.get("/predict/test")
def predict_test() -> Dict[str, Any]:
    job_id = str(uuid.uuid4())[:6]
    return _predict_test(job_id=job_id)


@log_decorator(endpoint="/predict/test/label", logger=logger)
def _predict_test_label(job_id: str) -> Dict[str, Any]:
    logger.info(f"execute: [{job_id}]")
    prediction = classifier.predict_label(data=Data().data)
    is_outlier, outlier_score = outlier_detector.predict(data=Data().data)
    return {
        "job_id": job_id,
        "prediction": prediction,
        "is_outlier": is_outlier,
        "outlier_score": outlier_score,
    }


@router.get("/predict/test/label")
def predict_test_label() -> Dict[str, Any]:
    job_id = str(uuid.uuid4())[:6]
    return _predict_test_label(job_id=job_id)


@log_decorator(endpoint="/predict", logger=logger)
def _predict(data: Data, job_id: str) -> Dict[str, Any]:
    logger.info(f"execute: [{job_id}]")
    if len(data.data) != 1 or len(data.data[0]) != 4:
        raise HTTPException(status_code=404, detail="Invalid input data")
    prediction = classifier.predict(data.data)
    is_outlier, outlier_score = outlier_detector.predict(data=data.data)
    prediction_list = list(prediction)
    return {
        "job_id": job_id,
        "prediction": prediction_list,
        "is_outlier": is_outlier,
        "outlier_score": outlier_score,
    }


@router.post("/predict")
def predict(data: Data) -> Dict[str, Any]:
    job_id = str(uuid.uuid4())[:6]
    return _predict(data=data, job_id=job_id)


@log_decorator(endpoint="/predict/label", logger=logger)
def _predict_label(data: Data, job_id: str) -> Dict[str, str]:
    logger.info(f"execute: [{job_id}]")
    if len(data.data) != 1 or len(data.data[0]) != 4:
        raise HTTPException(status_code=404, detail="Invalid input data")
    prediction = classifier.predict_label(data.data)
    is_outlier, outlier_score = outlier_detector.predict(data=data.data)
    return {
        "job_id": job_id,
        "prediction": prediction,
        "is_outlier": is_outlier,
        "outlier_score": outlier_score,
    }


@router.post("/predict/label")
def predict_label(data: Data) -> Dict[str, Any]:
    job_id = str(uuid.uuid4())[:6]
    return _predict_label(data=data, job_id=job_id)
