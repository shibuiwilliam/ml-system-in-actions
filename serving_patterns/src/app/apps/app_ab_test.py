import os
from fastapi import FastAPI
import logging

from src.configurations import PlatformConfigurations
from src.app.routers import health, predict_ab_test
from src.app.configurations import APIConfigurations

logger = logging.getLogger(__name__)
logger.info(f"starts {APIConfigurations.title}:{APIConfigurations.version}")
logger.info(f"platform: {PlatformConfigurations.platform}")


app = FastAPI(
    title=APIConfigurations.title,
    description=APIConfigurations.description,
    version=APIConfigurations.version,
)

app.include_router(health.router, prefix="/health", tags=["health"])

app.include_router(predict_ab_test.router, prefix="/predict", tags=["predict"])
