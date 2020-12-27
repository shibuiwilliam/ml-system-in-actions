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
async def predict(data: Data, background_tasks: BackgroundTasks):
    job_id = data.job_id if data.job_id is not None else get_job_id()
    return await _predict._predict(data, job_id, background_tasks)


@router.get("/labels")
def labels():
    return _predict._labels()


@router.get("/label")
def test_label():
    return _predict._test_label()


@router.post("/label")
async def predict_label(data: Data, background_tasks: BackgroundTasks = BackgroundTasks()):
    job_id = data.job_id if data.job_id is not None else get_job_id()
    return await _predict._predict_label(data, job_id, background_tasks)
