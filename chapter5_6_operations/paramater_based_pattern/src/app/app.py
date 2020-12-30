import os
from fastapi import FastAPI

from src.configurations import APIConfigurations
from src.app.routers import routers
from logging import getLogger

logger = getLogger(__name__)

app = FastAPI(
    title=APIConfigurations.title,
    description=APIConfigurations.description,
    version=APIConfigurations.version,
)

app.include_router(routers.router, prefix="", tags=[""])
