import time
import uuid
from logging import getLogger
from typing import Any, Dict, List

import numpy as np
from fastapi import APIRouter, BackgroundTasks, HTTPException
from src.db import cruds, schemas
from src.db.database import get_context_db
from src.ml.data import Data
from src.ml.outlier_detection import outlier_detector
from src.ml.prediction import classifier

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


def _predict(data: Data, job_id: str) -> Dict[str, Any]:
    logger.info(f"execute: [{job_id}]")
    if len(data.data) != 1 or len(data.data[0]) != 4:
        raise HTTPException(status_code=404, detail="Invalid input data")

    prediction_start = time.time()
    prediction = classifier.predict(data.data)
    prediction_elapsed = 1000 * (time.time() - prediction_start)

    outlier_start = time.time()
    is_outlier, outlier_score = outlier_detector.predict(data=data.data)
    outlier_elapsed = 1000 * (time.time() - outlier_start)

    return {
        "job_id": job_id,
        "prediction": list(prediction),
        "prediction_elapsed": prediction_elapsed,
        "is_outlier": is_outlier,
        "outlier_score": outlier_score,
        "outlier_elapsed": outlier_elapsed,
    }


@router.post("/predict")
def predict(data: Data, background_tasks: BackgroundTasks) -> Dict[str, Any]:
    job_id = str(uuid.uuid4())[:6]
    result = _predict(data=data, job_id=job_id)

    background_tasks.add_task(
        register_log,
        job_id=job_id,
        prediction_elapsed=result["prediction_elapsed"],
        prediction=result["prediction"],
        is_outlier=result["is_outlier"],
        outlier_elapsed=result["outlier_elapsed"],
        outlier_score=result["outlier_score"],
        data=data,
    )
    return result


@router.post("/predict/label")
def predict_label(data: Data, background_tasks: BackgroundTasks) -> Dict[str, Any]:
    job_id = str(uuid.uuid4())[:6]

    result = _predict(data=data, job_id=job_id)
    argmax = int(np.argmax(np.array(result["prediction"])))
    result["prediction_label"] = classifier.label[str(argmax)]

    background_tasks.add_task(
        register_log,
        job_id=job_id,
        prediction_elapsed=result["prediction_elapsed"],
        prediction=result["prediction"],
        is_outlier=result["is_outlier"],
        outlier_elapsed=result["outlier_elapsed"],
        outlier_score=result["outlier_score"],
        data=data,
    )
    return result


def register_log(
    job_id: str,
    prediction_elapsed: float,
    prediction: np.ndarray,
    is_outlier: bool,
    outlier_elapsed: float,
    outlier_score: float,
    data: Data,
):
    with get_context_db() as db:
        prediction_log = {
            "prediction": prediction,
            "prediction_elapsed": prediction_elapsed,
            "data": data.data,
        }
        cruds.add_prediction_log(db=db, log_id=job_id, log=prediction_log, commit=True)

        outlier_log = {
            "is_outlier": is_outlier,
            "outlier_score": outlier_score,
            "outlier_elapsed": outlier_elapsed,
            "data": data.data,
        }
        cruds.add_outlier_log(db=db, log_id=job_id, log=outlier_log, commit=True)
