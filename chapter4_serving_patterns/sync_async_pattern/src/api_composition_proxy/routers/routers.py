from fastapi import APIRouter, BackgroundTasks
import logging
import asyncio
import io
import httpx
from typing import Dict, Any, List
import uuid
import base64
from PIL import Image

from src.api_composition_proxy.configurations import ServiceConfigurations
from src.api_composition_proxy.backend.data import Data
from src.api_composition_proxy.backend import background_job, store_data_job, request_tfserving

logger = logging.getLogger(__name__)

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
        for service, url in ServiceConfigurations.services.items():
            serving_address = f"http://{url}/v1/models/{service}/versions/0/metadata"
            logger.info(f"health all : {serving_address}")
            r = await ac.get(serving_address)
            logger.info(f"health all res: {r}")
            results[service] = r.status_code
    return results


@router.get("/predict/test")
async def predict_test(background_tasks: BackgroundTasks) -> Dict[str, Any]:
    logger.info(f"TEST GET redirect to: /predict/test")
    job_id = str(uuid.uuid4())[:6]
    results = {"job_id": job_id}
    for service, url in ServiceConfigurations.grpc.items():
        if service == "mobilenet_v2":
            image = Data().image_data
            bytes_io = io.BytesIO()
            image.save(bytes_io, format=image.format)
            bytes_io.seek(0)
            r = request_tfserving.request_grpc(
                image=bytes_io.read(),
                model_spec_name=service,
                signature_name="serving_default",
                serving_address=url,
                timeout_second=5,
            )
            logger.info(f"prediction: {r}")
            results[service] = r
        else:
            background_job.save_data_job(
                data=Data().image_data,
                job_id=job_id,
                background_tasks=background_tasks,
                enqueue=True,
            )
    return results


@router.post("/predict")
async def predict(data: Data, background_tasks: BackgroundTasks) -> Dict[str, Any]:
    logger.info(f"POST redirect to: /predict")
    job_id = str(uuid.uuid4())[:6]
    results = {"job_id": job_id}
    for service, url in ServiceConfigurations.grpc.items():
        if service == "mobilenet_v2":
            image = base64.b64decode(str(data.image_data))
            bytes_io = io.BytesIO(image)
            r = request_tfserving.request_grpc(
                image=bytes_io.read(),
                model_spec_name=service,
                signature_name="serving_default",
                serving_address=url,
                timeout_second=5,
            )
            logger.info(f"prediction: {r}")
            results[service] = r
        else:
            image = base64.b64decode(str(data.image_data))
            bytes_io = io.BytesIO(image)
            data.image_data = Image.open(bytes_io)
            background_job.save_data_job(
                data=data.image_data,
                job_id=job_id,
                background_tasks=background_tasks,
                enqueue=True,
            )
    return results


@router.get("/job/{job_id}")
def prediction_result(job_id: str):
    result = {job_id: {"prediction": ""}}
    data = store_data_job.get_data_redis(job_id)
    result[job_id]["prediction"] = data
    return result
