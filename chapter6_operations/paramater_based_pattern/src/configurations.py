import os
from logging import getLogger

from src.constants import CONSTANTS, IRIS, PLATFORM_ENUM

logger = getLogger(__name__)


class PlatformConfigurations:
    platform = os.getenv("PLATFORM", PLATFORM_ENUM.DOCKER.value)
    if not PLATFORM_ENUM.has_value(platform):
        raise ValueError(f"PLATFORM must be one of {[v.value for v in PLATFORM_ENUM.__members__.values()]}")


class CacheConfigurations:
    cache_host = os.getenv("CACHE_HOST", "redis")
    cache_port = int(os.getenv("CACHE_PORT", 6379))
    queue_name = os.getenv("QUEUE_NAME", "queue")


class RedisCacheConfigurations(CacheConfigurations):
    redis_db = int(os.getenv("REDIS_DB", 0))
    redis_decode_responses = bool(os.getenv("REDIS_DECODE_RESPONSES", True))


class APIConfigurations:
    title = os.getenv("API_TITLE", "ServingPattern")
    description = os.getenv("API_DESCRIPTION", "machine learning system serving patterns")
    version = os.getenv("API_VERSION", "0.1")


class ModelConfigurations:
    mode: IRIS = IRIS.SETOSA
    model_filepath: str = ""
    model_directory: str = "/parameter_based_pattern/models/"
    mode_name: str = os.getenv("MODE", "setosa")
    if mode_name == "setosa":
        mode = IRIS.SETOSA
        model_filepath = os.path.join(model_directory, "iris_svc_0_setosa.onnx")
    elif mode_name == "versicolor":
        mode = IRIS.VERSICOLOR
        model_filepath = os.path.join(model_directory, "iris_svc_0_versicolor.onnx")
    elif mode_name == "virginica":
        mode = IRIS.VIRGINICA
        model_filepath = os.path.join(model_directory, "iris_svc_0_virginica.onnx")
    else:
        raise ValueError("mode should be one of setosa, versicolor and virginica")


logger.info(f"{PlatformConfigurations.__name__}: {PlatformConfigurations.__dict__}")
logger.info(f"{CacheConfigurations.__name__}: {CacheConfigurations.__dict__}")
logger.info(f"{RedisCacheConfigurations.__name__}: {RedisCacheConfigurations.__dict__}")
logger.info(f"{APIConfigurations.__name__}: {APIConfigurations.__dict__}")
logger.info(f"{ModelConfigurations.__name__}: {ModelConfigurations.__dict__}")
