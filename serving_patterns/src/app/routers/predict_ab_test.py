from fastapi import APIRouter, BackgroundTasks
import logging
import os

from src.app.api import _predict_ab_test
from src.app.ml.active_predictor import Data
from src.helper import get_job_id

logger = logging.getLogger(__name__)
router = APIRouter()

AB_TEST_GROUP = os.getenv("AB_TEST_GROUP", "A")


@router.get("")
def test():
    return _predict_ab_test._test()


@router.post("")
async def predict(data: Data, background_tasks: BackgroundTasks = BackgroundTasks()):
    job_id = data.job_id if data.job_id is not None else get_job_id()
    return await _predict_ab_test._predict(data, job_id, background_tasks, AB_TEST_GROUP)


@router.get("/labels")
def labels():
    return _predict_ab_test._labels()


@router.get("/label")
def test_label():
    return _predict_ab_test._test_label()


@router.post("/label")
async def predict_label(data: Data, background_tasks: BackgroundTasks = BackgroundTasks()):
    job_id = data.job_id if data.job_id is not None else get_job_id()
    return await _predict_ab_test._predict_label(data, job_id, background_tasks, AB_TEST_GROUP)
