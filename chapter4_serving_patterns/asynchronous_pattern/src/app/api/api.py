from typing import Dict, List, Any
from PIL import Image
import io
import numpy as np
import base64
import uuid
import requests
from fastapi import BackgroundTasks

from src.app.backend import background_job, store_data_job
from src.app.backend.data import Data
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
    model_spec_name = ModelConfigurations.model_spec_name
    address = ModelConfigurations.address
    port = ModelConfigurations.rest_port
    serving_address = f"http://{address}:{port}/v1/models/{model_spec_name}/versions/0/metadata"
    response = requests.get(serving_address)
    return response.json()


def label() -> Dict[int, str]:
    return ModelConfigurations.labels


async def predict_test(background_tasks: BackgroundTasks) -> Dict[str, str]:
    job_id = str(uuid.uuid4())[:6]
    data = Data()
    data.image_data = ModelConfigurations.sample_image
    background_job.save_data_job(data.image_data, job_id, background_tasks, True)
    return {"job_id": job_id}


async def predict(data: Data, background_tasks: BackgroundTasks) -> Dict[str, str]:
    image = base64.b64decode(str(data.image_data))
    io_bytes = io.BytesIO(image)
    data.image_data = Image.open(io_bytes)
    job_id = str(uuid.uuid4())[:6]
    background_job.save_data_job(
        data=data.image_data,
        job_id=job_id,
        background_tasks=background_tasks,
        enqueue=True,
    )
    return {"job_id": job_id}


def prediction_result(job_id: str) -> Dict[str, Dict[str, str]]:
    result = {job_id: {"prediction": ""}}
    data = store_data_job.get_data_redis(job_id)
    result[job_id]["prediction"] = data
    return result
