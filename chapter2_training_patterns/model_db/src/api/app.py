from fastapi import FastAPI

from src.configurations import APIConfigurations
from src.api.routers import health, api
from src.db import initialize
from src.db.database import engine
from logging import getLogger

logger = getLogger(__name__)

initialize.initialize_table(engine=engine, checkfirst=True)


app = FastAPI(
    title=APIConfigurations.title,
    description=APIConfigurations.description,
    version=APIConfigurations.version,
)

app.include_router(health.router, prefix=f"/v{APIConfigurations.version}/health", tags=["health"])
app.include_router(api.router, prefix=f"/v{APIConfigurations.version}/api", tags=["api"])
