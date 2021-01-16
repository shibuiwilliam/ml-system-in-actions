import json
import logging
import os
from logging import getLogger
from typing import Dict, List

from PIL import Image
from src.api_composition_proxy.constants import CONSTANTS, PLATFORM_ENUM

logger = logging.getLogger(__name__)


def get_label(json_path: str = "./data/image_net_labels.json") -> List[str]:
    with open(json_path, "r") as f:
        labels = json.load(f)
    return labels


def read_image(image_file: str = "./data/cat.jpg") -> bytes:
    return Image.open(image_file)


class PlatformConfigurations:
    platform = os.getenv("PLATFORM", PLATFORM_ENUM.DOCKER.value)
    if not PLATFORM_ENUM.has_value(platform):
        raise ValueError(f"PLATFORM must be one of {[v.value for v in PLATFORM_ENUM.__members__.values()]}")


class ServiceConfigurations:
    mobilenet_v2 = "mobilenet_v2"
    inception_v3 = "inception_v3"

    rest_mobilenet_v2 = os.getenv("REST_MOBILENET_V2")
    rest_inception_v3 = os.getenv("REST_INCEPTION_V3")

    grpc_mobilenet_v2 = os.getenv("GRPC_MOBILENET_V2")
    grpc_inception_v3 = os.getenv("GRPC_INCEPTION_V3")


class APIConfigurations:
    title = os.getenv("API_TITLE", "ServingPattern")
    description = os.getenv("API_DESCRIPTION", "machine learning system serving patterns")
    version = os.getenv("API_VERSION", "0.1")


class CacheConfigurations:
    cache_host = os.getenv("CACHE_HOST", "redis")
    cache_port = int(os.getenv("CACHE_PORT", 6379))
    queue_name = os.getenv("QUEUE_NAME", "queue")


class RedisCacheConfigurations(CacheConfigurations):
    redis_db = int(os.getenv("REDIS_DB", 0))
    redis_decode_responses = bool(os.getenv("REDIS_DECODE_RESPONSES", True))


class ModelConfigurations:
    sync_model_spec_name = os.getenv("SYNC_MODEL_SPEC_NAME", "mobilenet_v2")
    sync_signature_name = os.getenv("SYNC_SIGNATURE_NAME", "serving_default")

    async_model_spec_name = os.getenv("ASYNC_MODEL_SPEC_NAME", "inception_v3")
    async_signature_name = os.getenv("ASYNC_SIGNATURE_NAME", "serving_default")

    label_path = os.getenv("LABEL_PATH", "./data/image_net_labels.json")
    labels = get_label(json_path=label_path)

    sample_image_path = os.getenv("SAMPLE_IMAGE_PATH", "./data/cat.jpg")
    sample_image = read_image(image_file=sample_image_path)


logger.info(f"{ServiceConfigurations.__name__}: {ServiceConfigurations.__dict__}")
logger.info(f"{APIConfigurations.__name__}: {APIConfigurations.__dict__}")
logger.info(f"{PlatformConfigurations.__name__}: {PlatformConfigurations.__dict__}")
logger.info(f"{CacheConfigurations.__name__}: {CacheConfigurations.__dict__}")
logger.info(f"{RedisCacheConfigurations.__name__}: {RedisCacheConfigurations.__dict__}")
logger.info(f"{ModelConfigurations.__name__}: {ModelConfigurations.__dict__}")
