import redis
from src.api_composition_proxy.configurations import RedisCacheConfigurations

redis_client = redis.Redis(
    host=RedisCacheConfigurations.cache_host,
    port=RedisCacheConfigurations.cache_port,
    db=RedisCacheConfigurations.redis_db,
    decode_responses=RedisCacheConfigurations.redis_decode_responses,
)
