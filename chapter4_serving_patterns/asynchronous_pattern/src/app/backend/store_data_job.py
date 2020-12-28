from typing import Dict, Any
import logging
import json
import numpy as np
import io
import base64
from PIL import Image

from src.app.backend.redis_client import redis_client


logger = logging.getLogger(__name__)


def make_image_key(key: str) -> str:
    return f"{key}_image"


def left_push_queue(queue_name: str, key: str) -> bool:
    try:
        redis_client.lpush(queue_name, key)
        return True
    except Exception:
        return False


def right_pop_queue(queue_name: str) -> Any:
    if redis_client.llen(queue_name) > 0:
        return redis_client.rpop(queue_name)
    else:
        return None


def set_data_redis(key: str, value: str) -> bool:
    redis_client.set(key, value)
    return True


def get_data_redis(key: str) -> Any:
    data = redis_client.get(key)
    return data


def set_image_redis(key: str, image: Image.Image) -> str:
    bytes_io = io.BytesIO()
    image.save(bytes_io, format=image.format)
    image_key = make_image_key(key)
    encoded = base64.b64encode(bytes_io.getvalue())
    redis_client.set(image_key, encoded)
    return image_key


def get_image_redis(key: str) -> Image.Image:
    redis_data = get_data_redis(key)
    decoded = base64.b64decode(redis_data)
    io_bytes = io.BytesIO(decoded)
    image = Image.open(io_bytes)
    return image


def save_data_redis_job(job_id: str, data: Any) -> bool:
    return save_data_dict_redis_job(job_id, data.__dict__)


def save_data_dict_redis_job(job_id: str, data: Dict[str, Any]) -> bool:
    data_dict = {}
    for k, v in data.items():
        if isinstance(v, np.ndarray):
            data_dict[k] = v.tolist()
        elif isinstance(v, Image.Image):
            image_key = set_image_redis(job_id, v)
            data_dict[k] = image_key
        else:
            data_dict[k] = v
    logger.info(f"job_id: {job_id}")
    redis_client.set(job_id, json.dumps(data_dict))
    return True


def save_image_redis_job(job_id: str, image: Image.Image) -> bool:
    set_image_redis(job_id, image)
    redis_client.set(job_id, "")
    return True
