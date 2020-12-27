from typing import Dict, List
from fastapi import BackgroundTasks
import numpy as np
import logging
import os

from src.middleware.profiler import do_cprofile
from src.jobs import store_data_job
from src.constants import PLATFORM_ENUM
from src.configurations import PlatformConfigurations
from src.app.ml.active_predictor import Data, DataConverter, active_predictor


logger = logging.getLogger(__name__)

CSV_FILE_PATH = os.getenv("CSV_FILE_PATH", "/shared_volume/ab_test_log.csv")
os.makedirs("/shared_volume/", exist_ok=True)


@do_cprofile
def __predict(data: Data):
    input_np = DataConverter.convert_input_data_to_np(data.input_data)
    output_np = active_predictor.predict(input_np)
    reshaped_output_nps = DataConverter.reshape_output(output_np)
    data.prediction = reshaped_output_nps.tolist()
    logger.info({"job_id": data.job_id, "prediction": data.prediction})


@do_cprofile
def __predict_label(data: Data) -> Dict[str, float]:
    __predict(data)
    argmax = int(np.argmax(np.array(data.prediction)[0]))
    return {data.labels[argmax]: data.prediction[0][argmax]}


@do_cprofile
async def __async_predict(data: Data):
    input_np = DataConverter.convert_input_data_to_np(data.input_data)
    output_np = await active_predictor.async_predict(input_np)
    reshaped_output_nps = DataConverter.reshape_output(output_np)
    data.prediction = reshaped_output_nps.tolist()
    logger.info({"job_id": data.job_id, "prediction": data.prediction})


@do_cprofile
async def __async_predict_label(data: Data) -> Dict[str, float]:
    await __async_predict(data)
    argmax = int(np.argmax(np.array(data.prediction)[0]))
    return {data.labels[argmax]: data.prediction[0][argmax]}


def _labels(data_class: callable = Data) -> Dict[str, List[str]]:
    return {"labels": data_class().labels}


def _test(data: Data = Data()) -> Dict[str, int]:
    data.input_data = data.test_data
    __predict(data)
    return {"prediction": data.prediction}


def _test_label(data: Data = Data()) -> Dict[str, Dict[str, float]]:
    data.input_data = data.test_data
    label_proba = __predict_label(data)
    return {"prediction": label_proba}


async def _predict(data: Data, job_id: str, background_tasks: BackgroundTasks, ab_test_group: str) -> Dict[str, List[float]]:
    await __async_predict(data)
    store_data_job._save_data_csv_job(data, job_id, background_tasks, CSV_FILE_PATH, ab_test_group)
    return {"prediction": data.prediction, "job_id": job_id}


async def _predict_label(data: Data, job_id: str, background_tasks: BackgroundTasks, ab_test_group: str) -> Dict[str, Dict[str, float]]:
    label_proba = await __async_predict_label(data)
    store_data_job._save_data_csv_job(data, job_id, background_tasks, CSV_FILE_PATH, ab_test_group)
    return {"prediction": label_proba, "job_id": job_id}
