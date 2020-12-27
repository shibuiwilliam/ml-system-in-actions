from fastapi import APIRouter, BackgroundTasks
import logging

from src.app.api import _predict
from src.app.ml.active_predictor import Data
from src.helper import get_job_id

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("")
def test():
    return _predict._test()


@router.post("")
async def predict_async(data: Data, background_tasks: BackgroundTasks):
    job_id = data.job_id if data.job_id is not None else get_job_id()
    return await _predict._predict_async_post(data, job_id, background_tasks)


@router.get("/job/{job_id}")
def predict_async_get_job_id(job_id: str):
    return _predict._predict_async_get(job_id)


@router.get("/labels")
def labels():
    return _predict._labels()


@router.get("/label")
def test_label():
    return _predict._test_label()


@router.get("/label/{job_id}")
def predict_async_label(job_id: str):
    return _predict._predict_async_get_label(job_id)
