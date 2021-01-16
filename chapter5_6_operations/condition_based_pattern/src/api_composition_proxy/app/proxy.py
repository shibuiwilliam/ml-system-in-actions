import logging

from fastapi import FastAPI
from src.api_composition_proxy.configurations import APIConfigurations, PlatformConfigurations
from src.api_composition_proxy.routers import routers

logger = logging.getLogger(__name__)
logger.info(f"starts {APIConfigurations.title}:{APIConfigurations.version}")
logger.info(f"platform: {PlatformConfigurations.platform}")

app = FastAPI(
    title=APIConfigurations.title,
    description=APIConfigurations.description,
    version=APIConfigurations.version,
)

app.include_router(routers.router, prefix="", tags=[""])
