import pytest
from fastapi import BackgroundTasks
from typing import List, Tuple, Any
from PIL import Image
import numpy as np
import os

from src.constants import PLATFORM_ENUM
from tests.utils import floats_almost_equal, nested_floats_almost_equal, get_image_data
from src.app.ml.base_predictor import BaseData, BaseDataInterface, BaseDataConverter, BasePredictor
from src.app.ml.active_predictor import DataConverter
import src.app
from src.app.api._predict_image import (
    __predict,
    __predict_label,
    _predict_from_redis_cache,
    _labels,
    _test,
    _test_label,
    _predict,
    _predict_label,
    _predict_async_post,
    _predict_async_get,
    _predict_async_get_label,
)


mock_image = Image.new("RGB", size=(300, 300), color=(10, 10, 10))
mock_image_path = os.path.join("./src/app/ml/data", "good_cat.jpg")
labels = ["a", "b", "c"]
test_uuid = "550e8400-e29b-41d4-a716-446655440000"
job_id = f"{test_uuid}_0"
mock_BackgroundTasks = BackgroundTasks()
f_proba = [0.7, 0.2, 0.1]


class MockPredictor(BasePredictor):
    def load_model(self):
        pass

    def predict(self, data):
        return None


class MockData(BaseData):
    image_data: Any = mock_image
    test_data: str = mock_image_path
    labels: List[str] = labels


class MockDataInterface(BaseDataInterface):
    pass


MockDataInterface.input_shape = (1, 3, 224, 224)
MockDataInterface.input_type = "float32"
MockDataInterface.output_shape = (1, 3)
MockDataInterface.output_type = "float32"


class MockDataConverter(BaseDataConverter):
    pass


MockDataConverter.meta_data = MockDataInterface


class MockJob:
    def __call__(self):
        return True


@pytest.mark.parametrize(
    ("prediction", "expected"),
    [(np.array([[0.8, 0.1, 0.1]]), {"prediction": [[0.8, 0.1, 0.1]]}), (np.array([[0.2, 0.1, 0.7]]), {"prediction": [[0.2, 0.1, 0.7]]})],
)
def test__predict(mocker, prediction, expected):
    mock_data = MockData()
    mocker.patch("src.app.ml.active_predictor.DataConverter.reshape_output", return_value=prediction)
    mocker.patch("src.app.ml.active_predictor.active_predictor.predict", return_value=prediction)
    __predict(data=mock_data)
    assert nested_floats_almost_equal(mock_data.prediction, expected["prediction"])


@pytest.mark.parametrize(("prediction", "expected"), [(np.array([[0.1, 0.1, 0.8]]), {"c": 0.8}), (np.array([[0.2, 0.1, 0.7]]), {"c": 0.7})])
def test__predict_label(mocker, prediction, expected):
    mock_data = MockData()
    mocker.patch("src.app.ml.active_predictor.DataConverter.reshape_output", return_value=prediction)
    mocker.patch("src.app.ml.active_predictor.active_predictor.predict", return_value=prediction)
    result = __predict_label(data=mock_data)
    assert result == expected


@pytest.mark.parametrize(("job_id", "data", "expected"), [(job_id, {"image_data": mock_image}, {"image_data": mock_image, "prediction": [f_proba]})])
def test_predict_from_redis_cache(mocker, job_id, data, expected):
    mocker.patch("src.jobs.store_data_job.load_data_redis", return_value=data)
    mocker.patch("src.jobs.store_data_job.get_image_redis", return_value=data["image_data"])
    mocker.patch("src.app.ml.active_predictor.active_predictor.predict", return_value=np.array(expected["prediction"]))
    result = _predict_from_redis_cache(job_id, MockData)
    assert expected["image_data"] == result.image_data
    assert nested_floats_almost_equal(result.prediction, expected["prediction"])


def test_labels(mocker):
    result = _labels(MockData)
    assert "labels" in result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("output", "expected"), [(np.array([[0.8, 0.1, 0.1]]), {"prediction": [[0.8, 0.1, 0.1]]}), (np.array([[0.2, 0.1, 0.7]]), {"prediction": [[0.2, 0.1, 0.7]]})]
)
async def test_test(mocker, output, expected):
    mocker.patch("src.app.ml.active_predictor.DataConverter.reshape_output", return_value=output)
    mocker.patch("src.app.ml.active_predictor.active_predictor.predict", return_value=output)
    result = await _test(MockData())
    assert nested_floats_almost_equal(result["prediction"], expected["prediction"])


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("output", "expected"), [(np.array([[0.8, 0.1, 0.1]]), {"prediction": {"a": 0.8}}), (np.array([[0.2, 0.1, 0.7]]), {"prediction": {"c": 0.7}})]
)
async def test_test_label(mocker, output, expected):
    mocker.patch("src.app.ml.active_predictor.DataConverter.reshape_output", return_value=output)
    mocker.patch("src.app.ml.active_predictor.active_predictor.predict", return_value=output)
    result = await _test_label(MockData())
    assert result == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("output", "expected"), [(np.array([[0.8, 0.1, 0.1]]), {"prediction": [[0.8, 0.1, 0.1]]}), (np.array([[0.2, 0.1, 0.7]]), {"prediction": [[0.2, 0.1, 0.7]]})]
)
async def test_predict(mocker, output, expected):
    mock_image_base64 = get_image_data()["image_data"]
    mock_data = MockData(image_data=mock_image_base64)
    mocker.patch("PIL.Image.open", return_value=mock_image)
    mocker.patch("io.BytesIO", return_value=mock_image)
    mocker.patch("src.app.ml.active_predictor.active_predictor.predict", return_value=output)
    mocker.patch("src.jobs.store_data_job._save_data_job", return_value=job_id)
    result = await _predict(mock_data, mock_BackgroundTasks)
    assert nested_floats_almost_equal(result["prediction"], expected["prediction"])
    assert "job_id" in result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("output", "expected"), [(np.array([[0.8, 0.1, 0.1]]), {"prediction": {"a": 0.8}}), (np.array([[0.7, 0.1, 0.2]]), {"prediction": {"a": 0.7}})]
)
async def test_predict_label(mocker, output, expected):
    mock_image_base64 = get_image_data()["image_data"]
    mock_data = MockData(image_data=mock_image_base64)
    mocker.patch("PIL.Image.open", return_value=mock_image)
    mocker.patch("io.BytesIO", return_value=mock_image)
    mocker.patch("src.app.ml.active_predictor.active_predictor.predict", return_value=output)
    mocker.patch("src.jobs.store_data_job._save_data_job", return_value=job_id)
    result = await _predict_label(mock_data, mock_BackgroundTasks)
    assert result["prediction"]["a"] == pytest.approx(expected["prediction"]["a"])
    assert "job_id" in result


@pytest.mark.asyncio
@pytest.mark.parametrize(("job_id"), [(job_id)])
async def test_predict_async_post(mocker, job_id):
    mock_image_base64 = get_image_data()["image_data"]
    mock_data = MockData(image_data=mock_image_base64)
    mocker.patch("src.jobs.store_data_job._save_data_job", return_value=job_id)
    mocker.patch("PIL.Image.open", return_value=mock_image)
    mocker.patch("io.BytesIO", return_value=mock_image)
    result = await _predict_async_post(mock_data, job_id, mock_BackgroundTasks)
    assert result["job_id"] == job_id


@pytest.mark.parametrize(
    ("job_id", "data_dict", "expected"), [(job_id, {"image_data": mock_image, "prediction": [[0.8, 0.1, 0.1]]}, {job_id: {"prediction": [[0.8, 0.1, 0.1]]}})]
)
def test_predict_async_get(mocker, job_id, data_dict, expected):
    src.app.api._predict.PLATFORM = PLATFORM_ENUM.DOCKER_COMPOSE.value
    mocker.patch("src.jobs.store_data_job.load_data_redis", return_value=data_dict)
    result = _predict_async_get(job_id)
    assert result == expected


@pytest.mark.parametrize(
    ("job_id", "data_dict", "expected"),
    [(job_id, {"image_data": mock_image, "prediction": [[0.8, 0.1, 0.1]], "labels": labels}, {job_id: {"prediction": {"a": 0.8}}})],
)
def test_predict_async_get_label(mocker, job_id, data_dict, expected):
    src.app.api._predict.PLATFORM = PLATFORM_ENUM.DOCKER_COMPOSE.value
    mocker.patch("src.jobs.store_data_job.load_data_redis", return_value=data_dict)
    result = _predict_async_get_label(job_id)
    assert result == expected
