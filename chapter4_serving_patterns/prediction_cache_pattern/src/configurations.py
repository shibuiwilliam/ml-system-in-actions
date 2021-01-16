import os
from logging import getLogger

from src.constants import PLATFORM_ENUM

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
    api_address = os.getenv("API_ADDRESS", "localhost")
    grpc_port = int(os.getenv("GRPC_PORT", 50051))
    rest_api_port = int(os.getenv("REST_API_PORT", 8001))
    label_path = os.getenv("LABEL_PATH", "/prediction_cache_pattern/data/image_net_labels.json")

    preprocess_transformer_path = os.getenv(
        "PREPROCESS_TRANSFORMER_PATH", "/prediction_cache_pattern/models/preprocess_transformer.pkl"
    )
    softmax_transformer_path = os.getenv(
        "SOFTMAX_TRANSFORMER_PATH", "/prediction_cache_pattern/models/softmax_transformer.pkl"
    )

    onnx_input_name = os.getenv("ONNX_INPUT_NAME", "input")
    onnx_output_name = os.getenv("ONNX_OUTPUT_NAME", "output")


logger.info(f"{PlatformConfigurations.__name__}: {PlatformConfigurations.__dict__}")
logger.info(f"{CacheConfigurations.__name__}: {CacheConfigurations.__dict__}")
logger.info(f"{RedisCacheConfigurations.__name__}: {RedisCacheConfigurations.__dict__}")
logger.info(f"{APIConfigurations.__name__}: {APIConfigurations.__dict__}")
logger.info(f"{ModelConfigurations.__name__}: {ModelConfigurations.__dict__}")
