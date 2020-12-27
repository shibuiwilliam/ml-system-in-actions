import os
from typing import Dict, Any
from fastapi import BackgroundTasks
import logging
from pydantic import BaseModel
import json
import csv
import numpy as np
import io
import base64
import datetime
from PIL import Image

from src.constants import PLATFORM_ENUM, CONSTANTS
from src.configurations import PlatformConfigurations, CacheConfigurations
from src.middleware.redis_client import redis_client


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


def load_data_redis(key: str) -> Dict[str, Any]:
    data_dict = json.loads(redis_client.get(key))
    return data_dict


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


def save_data_csv_job(job_id: str, filepath: str, data: Any, ab_test_group: str) -> bool:
    if not os.path.exists(filepath):
        with open(filepath, "w") as f:
            _header = ["datetime", "job_id"]
            _header.extend([f"data_{i}" for i in range(len(data.input_data))])
            if hasattr(data, "labels"):
                _label = [label for label in data.labels]
            else:
                _label = [f"label_{i}" for i in range(len(data.labels))]
            _header.extend((_label))
            _header.append("prediction")
            _header.append("ab_test_group")
            writer = csv.writer(f)
            writer.writerows([_header])
    with open(filepath, "a") as f:
        _data = [datetime.datetime.now(), job_id]
        _data.extend(data.input_data)
        _data.extend(data.prediction[0])
        _data.append(int(np.argmax(np.array(data.prediction)[0])))
        _data.append(ab_test_group)
        writer = csv.writer(f)
        writer.writerows([_data])
    return True


def save_data_file_job(job_id: str, directory: str, data: Any) -> bool:
    file_path = os.path.join(directory, f"{job_id}.json")
    with open(file_path, "w") as f:
        json.dump(data, f)
    return True


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


class SaveDataJob(BaseModel):
    job_id: str
    data: Any
    queue_name: str = CONSTANTS.REDIS_QUEUE
    is_completed: bool = False

    def __call__(self):
        pass


class SaveDataFileJob(SaveDataJob):
    directory: str

    def __call__(self):
        save_data_jobs[self.job_id] = self
        logger.info(f"registered job: {self.job_id} in {self.__class__.__name__}")
        self.is_completed = save_data_file_job(self.job_id, self.directory, self.data)
        logger.info(f"completed save data: {self.job_id}")


class SaveDataCSVJob(SaveDataJob):
    filepath: str
    ab_test_group: str

    def __call__(self):
        save_data_jobs[self.job_id] = self
        logger.info(f"registered job: {self.job_id} in {self.__class__.__name__}")
        self.is_completed = save_data_csv_job(self.job_id, self.filepath, self.data, self.ab_test_group)
        logger.info(f"completed save data: {self.job_id}")


class SaveDataRedisJob(SaveDataJob):
    enqueue: bool = False

    def __call__(self):
        save_data_jobs[self.job_id] = self
        logger.info(f"registered job: {self.job_id} in {self.__class__.__name__}")
        if isinstance(self.data, Dict):
            self.is_completed = save_data_dict_redis_job(self.job_id, self.data)
        else:
            self.is_completed = save_data_redis_job(self.job_id, self.data)
        if self.enqueue:
            self.is_completed = left_push_queue(self.queue_name, self.job_id)
        logger.info(f"completed save data: {self.job_id}")


def _save_data_job(data: Any, job_id: str, background_tasks: BackgroundTasks, enqueue: bool = False) -> str:
    if PlatformConfigurations.platform == PLATFORM_ENUM.DOCKER_COMPOSE.value:
        task = SaveDataRedisJob(job_id=job_id, data=data, queue_name=CacheConfigurations.queue_name, enqueue=enqueue)

    elif PlatformConfigurations.platform == PLATFORM_ENUM.KUBERNETES.value:
        task = SaveDataRedisJob(job_id=job_id, data=data, queue_name=CacheConfigurations.queue_name, enqueue=enqueue)

    elif PlatformConfigurations.platform == PLATFORM_ENUM.TEST.value:
        task = SaveDataRedisJob(job_id=job_id, data=data, queue_name=CacheConfigurations.queue_name, enqueue=enqueue)
    else:
        raise ValueError("platform must be chosen from constants.PLATFORM_ENUM")
    background_tasks.add_task(task)
    return job_id


def _save_data_csv_job(data: Any, job_id: str, background_tasks: BackgroundTasks, filepath: str, ab_test_group: str) -> str:
    if PlatformConfigurations.platform == PLATFORM_ENUM.DOCKER_COMPOSE.value:
        task = SaveDataCSVJob(job_id=job_id, data=data, queue_name=CacheConfigurations.queue_name, filepath=filepath, ab_test_group=ab_test_group)

    elif PlatformConfigurations.platform == PLATFORM_ENUM.KUBERNETES.value:
        task = SaveDataCSVJob(job_id=job_id, data=data, queue_name=CacheConfigurations.queue_name, filepath=filepath, ab_test_group=ab_test_group)

    elif PlatformConfigurations.platform == PLATFORM_ENUM.TEST.value:
        task = SaveDataCSVJob(job_id=job_id, data=data, queue_name=CacheConfigurations.queue_name, filepath=filepath, ab_test_group=ab_test_group)
    else:
        raise ValueError("platform must be chosen from constants.PLATFORM_ENUM")
    background_tasks.add_task(task)
    return job_id


save_data_jobs: Dict[str, SaveDataJob] = {}
