import asyncio
import base64
import io
import logging
import uuid
from typing import Any, Dict, List

import grpc
import httpx
from fastapi import APIRouter
from PIL import Image
from src.api_composition_proxy.backend import request_tfserving
from src.api_composition_proxy.backend.data import Data
from src.api_composition_proxy.configurations import ModelConfigurations, ServiceConfigurations
from tensorflow_serving.apis import prediction_service_pb2_grpc

logger = logging.getLogger(__name__)

router = APIRouter()

channel = grpc.insecure_channel(ServiceConfigurations.grpc)
stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)


@router.get("/health")
def health() -> Dict[str, str]:
    return {"health": "ok"}


@router.get("/label")
def label() -> List[str]:
    return ModelConfigurations.labels


@router.get("/metadata")
def metadata() -> Dict[str, Any]:
    return {
        "data_type": "str",
        "data_structure": "(1,1)",
        "data_sample": "base64 encoded image file",
        "prediction_type": "float32",
        "prediction_structure": f"(1,{len(ModelConfigurations.labels)})",
        "prediction_sample": "[0.07093159, 0.01558308, 0.01348537, ...]",
    }


@router.get("/health/pred")
async def health_pred() -> Dict[str, Any]:
    logger.info(f"GET redirect to: /health")
    async with httpx.AsyncClient() as ac:
        serving_address = (
            f"http://{ServiceConfigurations.rest}/v1/models/{ModelConfigurations.model_spec_name}/versions/0/metadata"
        )
        logger.info(f"health pred : {serving_address}")
        r = await ac.get(serving_address)
        logger.info(f"health pred res: {r}")
    if r.status_code == 200:
        return {"health": "ok"}
    else:
        return {"health": "ng"}


@router.get("/predict/test")
def predict_test() -> Dict[str, Any]:
    job_id = str(uuid.uuid4())[:6]
    logger.info(f"{job_id} TEST GET redirect to: /predict/test")
    image = Data().image_data
    bytes_io = io.BytesIO()
    image.save(bytes_io, format=image.format)
    bytes_io.seek(0)
    r = request_tfserving.request_grpc(
        stub=stub,
        image=bytes_io.read(),
        model_spec_name=ModelConfigurations.model_spec_name,
        signature_name=ModelConfigurations.signature_name,
        timeout_second=ModelConfigurations.timeout_second,
    )
    logger.info(f"{job_id} prediction: {r}")
    return r


@router.post("/predict")
def predict(data: Data) -> Dict[str, Any]:
    job_id = str(uuid.uuid4())[:6]
    logger.info(f"{job_id} POST redirect to: /predict")
    image = base64.b64decode(str(data.image_data))
    bytes_io = io.BytesIO(image)
    image_data = Image.open(bytes_io)
    image_data.save(bytes_io, format=image_data.format)
    bytes_io.seek(0)
    r = request_tfserving.request_grpc(
        stub=stub,
        image=bytes_io.read(),
        model_spec_name=ModelConfigurations.model_spec_name,
        signature_name=ModelConfigurations.signature_name,
        timeout_second=ModelConfigurations.timeout_second,
    )
    logger.info(f"{job_id} prediction: {r}")
    return r
