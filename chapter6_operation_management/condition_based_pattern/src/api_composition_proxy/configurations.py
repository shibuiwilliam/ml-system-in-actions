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
    rest: str = os.getenv("REST", "mobilenet_v2:8501")
    grpc: str = os.getenv("GRPC", "mobilenet_v2:8500")


class APIConfigurations:
    title = os.getenv("API_TITLE", "ServingPattern")
    description = os.getenv("API_DESCRIPTION", "machine learning system serving patterns")
    version = os.getenv("API_VERSION", "0.1")


class ModelConfigurations:
    model_spec_name = os.getenv("MODEL_SPEC_NAME", "mobilenet_v2")
    signature_name = os.getenv("SIGNATURE_NAME", "serving_default")

    label_path = os.getenv("LABEL_PATH", "./data/image_net_labels.json")
    labels = get_label(json_path=label_path)

    timeout_second = int(os.getenv("TIMEOUT_SECOND", 10))

    sample_image_path = os.getenv("SAMPLE_IMAGE_PATH", "./data/cat.jpg")
    sample_image = read_image(image_file=sample_image_path)


logger.info(f"{ServiceConfigurations.__name__}: {ServiceConfigurations.__dict__}")
logger.info(f"{APIConfigurations.__name__}: {APIConfigurations.__dict__}")
logger.info(f"{PlatformConfigurations.__name__}: {PlatformConfigurations.__dict__}")
logger.info(f"{ModelConfigurations.__name__}: {ModelConfigurations.__dict__}")
