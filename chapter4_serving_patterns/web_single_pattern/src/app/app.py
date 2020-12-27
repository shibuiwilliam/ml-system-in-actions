import os
from fastapi import FastAPI
from logging import getLogger

from src.configurations import PlatformConfigurations, APIConfigurations
from src.app.routers import routers

logger = getLogger(__name__)
logger.info(f"starts {APIConfigurations.title}:{APIConfigurations.version}")
logger.info(f"platform: {PlatformConfigurations.platform}")


app = FastAPI(
    title=APIConfigurations.title,
    description=APIConfigurations.description,
    version=APIConfigurations.version,
)

app.include_router(routers.router, prefix="", tags=[""])
