from fastapi import APIRouter
import os
import logging
import asyncio
import uuid
import httpx
from typing import Dict, Any, List
from pydantic import BaseModel


logger = logging.getLogger(__name__)

router = APIRouter()

services = {
    "setosa": os.getenv("SERVICE_SETOSA"),
    "versicolor": os.getenv("SERVICE_VERSICOLOR"),
    "virginica": os.getenv("SERVICE_VIRGINICA"),
}


class Data(BaseModel):
    data: List[List[float]] = [[5.1, 3.5, 1.4, 0.2]]


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
        "prediction_structure": "(1,2)",
        "prediction_sample": {
            "service_setosa": [0.970000, 0.030000],
            "service_versicolor": [0.970000, 0.030000],
            "service_virginica": [0.970000, 0.030000],
        },
    }


@router.get("/health/all")
async def health_all() -> Dict[str, Any]:
    logger.info(f"GET redirect to: /health")
    results = {}
    async with httpx.AsyncClient() as ac:
        for service, url in services.items():
            r = await ac.get(f"{url}/health")
            results[service] = r.json()
    return results


@router.get("/predict/get/test")
async def predict_get_test() -> Dict[str, Any]:
    job_id = str(uuid.uuid4())[:6]
    logger.info(f"TEST GET redirect to: /predict/test as {job_id}")
    results = {}
    async with httpx.AsyncClient() as ac:
        for service, url in services.items():
            r = await ac.get(f"{url}/predict/test", params={"id": job_id})
            logger.info(f"{service} {job_id} {r.json()}")
            results[service] = r.json()
    return results


@router.get("/predict/post/test")
async def predict_post_test() -> Dict[str, Any]:
    job_id = str(uuid.uuid4())[:6]
    logger.info(f"TEST POST redirect to: /predict as {job_id}")
    results = {}
    async with httpx.AsyncClient() as ac:
        for service, url in services.items():
            r = await ac.post(f"{url}/predict", json={"data": Data().data}, params={"id": job_id})
            logger.info(f"{service} {job_id} {r.json()}")
            logger.info(f"prediction: {r} {r.__dict__}")
            results[service] = r.json()
    return results


@router.post("/predict")
async def predict(data: Data) -> Dict[str, Any]:
    job_id = str(uuid.uuid4())[:6]
    logger.info(f"POST redirect to: /predict as {job_id}")
    results = {}
    async with httpx.AsyncClient() as ac:
        for service, url in services.items():
            r = await ac.post(f"{url}/predict", json={"data": data.data}, params={"id": job_id})
            logger.info(f"{service} {job_id} {r.json()}")
            results[service] = r.json()
    return results


@router.post("/predict/label")
async def predict_label(data: Data) -> Dict[str, Any]:
    job_id = str(uuid.uuid4())[:6]
    logger.info(f"POST redirect to: /predict as {job_id}")
    results = {"prediction": {"proba": -1.0, "label": None}}
    async with httpx.AsyncClient() as ac:
        for service, url in services.items():
            r = await ac.post(f"{url}/predict", json={"data": data.data}, params={"id": job_id})
            logger.info(f"{service} {job_id} {r.json()}")
            proba = r.json()["prediction"][0]
            if results["prediction"]["proba"] < proba:
                results["prediction"] = {"proba": r.json()["prediction"][0], "label": service}
    return results
