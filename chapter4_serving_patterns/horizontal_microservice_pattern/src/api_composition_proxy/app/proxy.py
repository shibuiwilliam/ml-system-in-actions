from fastapi import FastAPI
import logging

from src.api_composition_proxy.routers import health, proxy, abtest
from src.api_composition_proxy.configurations import APIConfigurations
from src.configurations import PlatformConfigurations


logger = logging.getLogger(__name__)
logger.info(f"starts {APIConfigurations.title}:{APIConfigurations.version}")
logger.info(f"platform: {PlatformConfigurations.platform}")

app = FastAPI(
    title=APIConfigurations.title,
    description=APIConfigurations.description,
    version=APIConfigurations.version,
)

app.include_router(health.router, prefix="/health", tags=["health"])

app.include_router(proxy.router, prefix="/redirect", tags=["redirect"])

app.include_router(abtest.router, prefix="/abtest", tags=["abtest"])
