import pytest
import numpy as np
from typing import List, Tuple

from src.app.ml.base_predictor import BaseData, BaseDataInterface, BaseDataConverter, BasePredictor
from src.app.backend.prediction_batch import prediction_batch


test_job_id = "550e8400-e29b-41d4-a716-446655440000_0"
f_proba = [0.7, 0.2, 0.1]
f_data = [[5.1, 3.5, 1.4, 0.2]]


class MockData(BaseData):
    input_data: List[List[float]] = f_data
    test_data: List[List[float]] = f_data


class MockDataInterface(BaseDataInterface):
    pass


MockDataInterface.input_shape = (1, 4)
MockDataInterface.input_type = "float32"
MockDataInterface.output_shape = (1, 3)
MockDataInterface.output_type = "float32"


class MockDataConverter(BaseDataConverter):
    pass


MockDataConverter.meta_data = MockDataInterface


@pytest.mark.parametrize(("job_id", "data"), [(test_job_id, MockData())])
def test_run_prediction(mocker, job_id, data):
    mocker.patch("src.jobs.store_data_job.right_pop_queue", return_value=job_id)
    mocker.patch("src.app.api._predict._predict_from_redis_cache", return_value=data)
    mocker.patch("src.jobs.store_data_job.save_data_redis_job", return_value=None)
    mocker.patch("src.jobs.store_data_job.left_push_queue", return_value=None)
    mocker.patch("src.jobs.store_data_job.load_data_redis", return_value=data.__dict__)

    prediction_batch._trigger_prediction_if_queue()


@pytest.mark.parametrize(("job_id", "data"), [(None, None)])
def test_run_prediction_none(mocker, job_id, data):
    mocker.patch("src.jobs.store_data_job.right_pop_queue", return_value=job_id)
    mocker.patch("src.app.api._predict._predict_from_redis_cache", return_value=data)
    mocker.patch("src.jobs.store_data_job.save_data_redis_job", return_value=None)
    mocker.patch("src.jobs.store_data_job.left_push_queue", return_value=None)
    mocker.patch("src.jobs.store_data_job.load_data_redis", return_value=data)

    prediction_batch._trigger_prediction_if_queue()
