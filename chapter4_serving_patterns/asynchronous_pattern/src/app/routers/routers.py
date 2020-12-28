from fastapi import APIRouter, BackgroundTasks
from src.app.api import api
from src.app.backend.data import Data
from logging import getLogger

logger = getLogger(__name__)
router = APIRouter()


@router.get("/health")
def health():
    return api.health()


@router.get("/health/sync")
def health_sync():
    return api.health_sync()


@router.get("/health/async")
async def health_async():
    result = await api.health_async()
    return result


@router.get("/metadata")
def metadata():
    return api.metadata()


@router.get("/label")
def label():
    return api.label()


@router.get("/predict/test")
async def predict_test(background_tasks: BackgroundTasks):
    return await api.predict_test(background_tasks=background_tasks)


@router.post("/predict")
async def predict(data: Data, background_tasks: BackgroundTasks):
    return await api.predict(data=data, background_tasks=background_tasks)


@router.get("/job/{job_id}")
def prediction_result(job_id: str):
    return api.prediction_result(job_id)