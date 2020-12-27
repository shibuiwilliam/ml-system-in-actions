import os
import logging

from src.constants import PLATFORM_ENUM, JOB_ID_ENUM

logger = logging.getLogger(__name__)


class _PlatformConfigurations:
    # can be docker_compose or kubernetes
    platform = os.getenv("PLATFORM", PLATFORM_ENUM.DOCKER_COMPOSE.value)
    if platform == PLATFORM_ENUM.DOCKER_COMPOSE.value:
        platform = platform
    elif platform == PLATFORM_ENUM.KUBERNETES.value:
        platform = platform
    else:
        platform = PLATFORM_ENUM.TEST.value


class _CacheConfigurations:
    cache_host = os.getenv("CACHE_HOST", "redis")
    cache_port = int(os.getenv("CACHE_PORT", 6379))
    queue_name = os.getenv("QUEUE_NAME", "queue")


class _RedisCacheConfigurations(_CacheConfigurations):
    redis_db = int(os.getenv("REDIS_DB", 0))
    redis_decode_responses = bool(os.getenv("REDIS_DECODE_RESPONSES", True))


class _JobIdConfigurations:
    job_id_type = os.getenv("JOB_ID_TYPE", JOB_ID_ENUM.UUID.value)
    if job_id_type == JOB_ID_ENUM.UUID.value:
        job_id_type = JOB_ID_ENUM.UUID.value
    elif job_id_type == JOB_ID_ENUM.INCREMENTAL.value:
        job_id_type = JOB_ID_ENUM.INCREMENTAL.value
    elif job_id_type == JOB_ID_ENUM.UUID_INCREMENTAL.value:
        job_id_type = JOB_ID_ENUM.UUID_INCREMENTAL.value
    else:
        job_id_type = JOB_ID_ENUM.UUID.value


PlatformConfigurations = _PlatformConfigurations()
CacheConfigurations = _CacheConfigurations()
RedisCacheConfigurations = _RedisCacheConfigurations()
JobIdConfigurations = _JobIdConfigurations()

logger.info(f"platform configurations: {PlatformConfigurations.__dict__}")
logger.info(f"cache configurations: {CacheConfigurations.__dict__}")
logger.info(f"redis cache configurations: {RedisCacheConfigurations.__dict__}")
logger.info(f"job id configurations: {JobIdConfigurations.__dict__}")
