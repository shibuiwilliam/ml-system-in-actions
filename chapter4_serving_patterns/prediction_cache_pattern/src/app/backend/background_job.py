import json
import logging
from typing import Any, Dict, List, Union

from fastapi import BackgroundTasks
from pydantic import BaseModel
from src.app.backend.redis_client import redis_client

logger = logging.getLogger(__name__)


def set_data_redis(key: str, value: List) -> bool:
    data_json = json.dumps(value)
    redis_client.set(key, data_json)
    return True


def get_data_redis(key: str) -> Union[List, None]:
    data = redis_client.get(key)
    if data is None:
        return None
    original_data = json.loads(data)
    return original_data


class SaveDataJob(BaseModel):
    item_id: str
    data: Any
    is_completed: bool = False

    def __call__(self):
        pass


class SaveDataRedisJob(SaveDataJob):
    def __call__(self):
        save_data_jobs[self.item_id] = self
        logger.info(f"registered cache: {self.item_id} in {self.__class__.__name__}")
        self.is_completed = set_data_redis(key=self.item_id, value=self.data)
        logger.info(f"completed save data: {self.item_id}")


def save_data_job(data: Any, item_id: str, background_tasks: BackgroundTasks) -> str:
    task = SaveDataRedisJob(item_id=item_id, data=data)
    background_tasks.add_task(task)
    return item_id


save_data_jobs: Dict[str, SaveDataJob] = {}
