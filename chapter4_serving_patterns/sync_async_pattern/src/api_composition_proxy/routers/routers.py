import asyncio
import base64
import io
import logging
import os
import uuid
from typing import Any, Dict

import grpc
import httpx
from fastapi import APIRouter, BackgroundTasks
from PIL import Image
from src.api_composition_proxy.backend import background_job, request_tfserving, store_data_job
from src.api_composition_proxy.backend.data import Data
from src.api_composition_proxy.configurations import ModelConfigurations, ServiceConfigurations
from tensorflow_serving.apis import prediction_service_pb2_grpc

logger = logging.getLogger(__name__)

router = APIRouter()


channel = grpc.insecure_channel(ServiceConfigurations.grpc_mobilenet_v2)
stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)


@router.get("/health")
def health() -> Dict[str, str]:
    return {"health": "ok"}


@router.get("/metadata")
def metadata() -> Dict[str, Any]:
    return {
        "data_type": "str",
        "data_structure": "(1,1)",
        "data_sample": "base64 encoded image file",
        "prediction_type": "float32",
        "prediction_structure": "(1,1001)",
        "prediction_sample": "[0.07093159, 0.01558308, 0.01348537, ...]",
    }


@router.get("/health/all")
async def health_all() -> Dict[str, Any]:
    logger.info(f"GET redirect to: /health")
    results = {}
    async with httpx.AsyncClient() as ac:

        async def req(ac, service, url):
            response = await ac.get(f"http://{url}/v1/models/{service}/versions/0/metadata")
            return service, response

        tasks = [
            req(
                ac,
                ServiceConfigurations.mobilenet_v2,
                ServiceConfigurations.rest_mobilenet_v2,
            ),
            req(
                ac,
                ServiceConfigurations.inception_v3,
                ServiceConfigurations.rest_inception_v3,
            ),
        ]

        responses = await asyncio.gather(*tasks)

        for service, response in responses:
            if response.status_code == 200:
                results[service] = "ok"
            else:
                results[service] = "ng"
    return results


@router.get("/predict/test")
def predict_test(background_tasks: BackgroundTasks) -> Dict[str, Any]:
    logger.info(f"TEST GET redirect to: /predict/test")
    job_id = str(uuid.uuid4())[:6]
    results = {"job_id": job_id}
    image = Data().image_data

    bytes_io = io.BytesIO()
    image.save(bytes_io, format=image.format)
    bytes_io.seek(0)
    r = request_tfserving.request_grpc(
        stub=stub,
        image=bytes_io.read(),
        model_spec_name=ModelConfigurations.sync_model_spec_name,
        signature_name=ModelConfigurations.sync_signature_name,
        timeout_second=5,
    )
    logger.info(f"prediction: {r}")
    results[ServiceConfigurations.mobilenet_v2] = r

    background_job.save_data_job(
        data=Data().image_data,
        job_id=job_id,
        background_tasks=background_tasks,
        enqueue=True,
    )
    return results


@router.post("/predict")
def predict(data: Data, background_tasks: BackgroundTasks) -> Dict[str, Any]:
    logger.info(f"POST redirect to: /predict")
    job_id = str(uuid.uuid4())[:6]
    results = {"job_id": job_id}
    image = base64.b64decode(str(data.image_data))
    bytes_io = io.BytesIO(image)
    image_data = Image.open(bytes_io)

    image_data.save(bytes_io, format=image_data.format)
    bytes_io.seek(0)
    r = request_tfserving.request_grpc(
        stub=stub,
        image=bytes_io.read(),
        model_spec_name=ModelConfigurations.sync_model_spec_name,
        signature_name=ModelConfigurations.sync_signature_name,
        timeout_second=5,
    )
    logger.info(f"prediction: {r}")
    results[ServiceConfigurations.mobilenet_v2] = r

    background_job.save_data_job(
        data=image_data,
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
