from fastapi import APIRouter, BackgroundTasks
import logging

from src.app.api import _predict_image
from src.app.ml.active_predictor import Data
from src.helper import get_job_id

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("")
async def test():
    result = await _predict_image._test()
    return result


@router.post("")
async def predict(data: Data, background_tasks: BackgroundTasks = BackgroundTasks()):
    job_id = data.job_id if data.job_id is not None else get_job_id()
    result = await _predict_image._predict(data, job_id, background_tasks)
    return result


@router.get("/labels")
def labels():
    return _predict_image._labels()


@router.get("/label")
async def test_label():
    result = await _predict_image._test_label()
    return result


@router.post("/label")
async def predict_label(data: Data, background_tasks: BackgroundTasks = BackgroundTasks()):
    job_id = data.job_id if data.job_id is not None else get_job_id()
    result = await _predict_image._predict_label(data, job_id, background_tasks)
    return result


@router.post("/async")
async def predict_async_post(data: Data, background_tasks: BackgroundTasks = BackgroundTasks()):
    job_id = data.job_id if data.job_id is not None else get_job_id()
    return await _predict_image._predict_async_post(data, job_id, background_tasks)


@router.get("/async/{job_id}")
def predict_async_get_job_id(job_id: str):
    return _predict_image._predict_async_get(job_id)


@router.get("/async/label/{job_id}")
def predict_async_get_label_job_id(job_id: str):
    return _predict_image._predict_async_get_label(job_id)
