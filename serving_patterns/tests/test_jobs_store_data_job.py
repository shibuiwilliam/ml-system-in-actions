import pytest
import json
from PIL import Image
from typing import List, Tuple, Any
from fastapi import BackgroundTasks

from src.constants import PLATFORM_ENUM, CONSTANTS
from src.jobs import store_data_job
import src.jobs
from src.app.ml.base_predictor import BaseData, BaseDataInterface


test_job_id = "550e8400-e29b-41d4-a716-446655440000_0"
test_uuid = "550e8400-e29b-41d4-a716-446655440000"
mock_image = Image.open("src/app/ml/data/good_cat.jpg")
labels = ["a", "b", "c"]
mock_BackgroundTasks = BackgroundTasks()


class MockData(BaseData):
    data: List[List[int]] = [[5.1, 3.5, 1.4, 0.2]]
    test_data: List[List[int]] = [[5.1, 3.5, 1.4, 0.2]]
    labels: List[str] = labels


class MockDataImage(BaseData):
    image_data: Any = mock_image
    data: List[List[int]] = [[5.1, 3.5, 1.4, 0.2]]
    test_data: List[List[int]] = [[5.1, 3.5, 1.4, 0.2]]
    labels: List[str] = labels


class MockDataInterface(BaseDataInterface):
    input_shape: Tuple[int] = (1, 4)
    input_type: str = "float64"
    output_shape: Tuple[int] = (1, 3)
    output_type: str = "float64"


class MockJob:
    def __call__(self):
        return True


@pytest.mark.parametrize(("key", "expected"), [("a", "a_image")])
def test_make_image_key(key, expected):
    result = store_data_job.make_image_key(key)
    assert result == expected


@pytest.mark.parametrize(("queue_name", "key", "expected"), [(CONSTANTS.REDIS_QUEUE, "abc", True)])
def test_left_push_queue(mocker, queue_name, key, expected):
    mocker.patch("src.middleware.redis_client.redis_client.lpush", return_value=expected)
    result = store_data_job.left_push_queue(queue_name, key)
    assert result == expected


@pytest.mark.parametrize(("queue_name", "num", "key"), [(CONSTANTS.REDIS_QUEUE, 1, "abc")])
def test_right_pop_queue(mocker, queue_name, num, key):
    mocker.patch("src.middleware.redis_client.redis_client.llen", return_value=num)
    mocker.patch("src.middleware.redis_client.redis_client.rpop", return_value=key)
    result = store_data_job.right_pop_queue(queue_name)
    assert result == key


@pytest.mark.parametrize(("queue_name", "num"), [(CONSTANTS.REDIS_QUEUE, 0)])
def test_right_pop_queue_none(mocker, queue_name, num):
    mocker.patch("src.middleware.redis_client.redis_client.llen", return_value=num)
    mocker.patch("src.middleware.redis_client.redis_client.rpop", return_value=None)
    result = store_data_job.right_pop_queue(queue_name)
    assert result is None


@pytest.mark.parametrize(("key", "data"), [(test_job_id, {"data": [1.0, -1.0], "prediction": None})])
def test_load_data_redis(mocker, key, data):
    mocker.patch("src.middleware.redis_client.redis_client.get", return_value=data)
    mocker.patch("json.loads", return_value=data)
    result = store_data_job.load_data_redis(key)
    assert result["data"] == data["data"]
    assert result["prediction"] == data["prediction"]


@pytest.mark.parametrize(("key", "data"), [("a", "b")])
def test_get_data_redis(mocker, key, data):
    mocker.patch("src.middleware.redis_client.redis_client.get", return_value=data)
    result = store_data_job.get_data_redis(key)
    assert result == data


@pytest.mark.parametrize(("key", "image", "expected"), [("a", mock_image, "a_image")])
def test_set_image_redis(mocker, key, image, expected):
    mocker.patch("PIL.Image.Image.format", return_value="JPEG")
    mocker.patch("src.middleware.redis_client.redis_client.set", return_value=None)
    result = store_data_job.set_image_redis(key, image)
    assert result == expected


@pytest.mark.parametrize(("key", "image", "expected"), [("a", mock_image, mock_image)])
def test_get_image_redis(mocker, key, image, expected):
    mocker.patch("src.jobs.store_data_job.get_data_redis", return_value=True)
    mocker.patch("base64.b64decode", return_value=True)
    mocker.patch("io.BytesIO", return_value=True)
    mocker.patch("PIL.Image.open", return_value=image)
    result = store_data_job.get_image_redis(key)
    assert result == expected


@pytest.mark.parametrize(("job_id", "directory", "data"), [(test_job_id, "/test", {"data": [1.0, -1.0], "prediction": None})])
def test_save_data_file_job(mocker, tmpdir, job_id, directory, data):
    tmp_file = tmpdir.mkdir(directory).join(f"{job_id}.json")
    mocker.patch("os.path.join", return_value=tmp_file)
    result = store_data_job.save_data_file_job(job_id, directory, data)
    assert result
    with open(tmp_file, "r") as f:
        assert data == json.load(f)


class Test:
    mock_redis_cache = {}

    @pytest.mark.parametrize(("job_id", "data"), [(test_job_id, MockData()), (test_job_id, MockDataImage())])
    def test_save_data_redis_job(self, mocker, job_id, data) -> None:
        def set(key, value):
            self.mock_redis_cache[key] = value

        def get(key):
            return self.mock_redis_cache.get(key, None)

        mocker.patch("src.middleware.redis_client.redis_client.set").side_effect = set

        result = store_data_job.save_data_redis_job(job_id, data)
        assert result
        assert get(job_id) is not None

    @pytest.mark.parametrize(("job_id", "data"), [(test_job_id, {"data": [1.0, -1.0], "prediction": None}), (test_job_id, MockDataImage().__dict__)])
    def test_save_data_dict_redis_job(self, mocker, job_id, data) -> None:
        def set(key, value):
            self.mock_redis_cache[key] = value

        def get(key):
            return self.mock_redis_cache.get(key, None)

        mocker.patch("src.middleware.redis_client.redis_client.set").side_effect = set

        result = store_data_job.save_data_dict_redis_job(job_id, data)
        assert result
        assert get(job_id) is not None


@pytest.mark.parametrize(("job_id", "directory", "data"), [(test_job_id, "/tmp/", {"data": [1.0, -1.0], "prediction": None})])
def test_SaveDataFileJob(mocker, job_id, directory, data):
    save_data_file_job = store_data_job.SaveDataFileJob(job_id=job_id, directory=directory, data=data)
    mocker.patch("src.jobs.store_data_job.save_data_file_job", return_value=True)
    save_data_file_job()
    assert save_data_file_job.is_completed


@pytest.mark.parametrize(
    ("job_id", "data", "queue_name", "enqueue"), [(test_job_id, MockData(), CONSTANTS.REDIS_QUEUE, True), (test_job_id, MockData(), "aaaaaaaa", False)]
)
def test_SaveDataRedisJob(mocker, job_id, data, queue_name, enqueue):
    save_data_redis_job = store_data_job.SaveDataRedisJob(job_id=job_id, data=data, queue_name=queue_name, enqueue=enqueue)
    mocker.patch("src.jobs.store_data_job.left_push_queue", return_value=True)
    mocker.patch("src.jobs.store_data_job.save_data_redis_job", return_value=True)
    save_data_redis_job()
    assert save_data_redis_job.is_completed


@pytest.mark.parametrize(
    ("_uuid", "data", "enqueue", "expected"),
    [
        (test_uuid, True, MockData(), test_uuid),
        (test_uuid, True, MockData(), test_uuid),
        (test_uuid, False, MockData(), test_uuid),
        (test_uuid, False, MockData(prediction=[[0.1, 0.2, 0.7]]), test_uuid),
    ],
)
def test_save_data_job(mocker, _uuid, data, enqueue, expected):
    mock_job = MockJob()
    src.jobs.store_data_job._save_data_job.PLATFORM = PLATFORM_ENUM.DOCKER_COMPOSE.value
    mocker.patch("src.jobs.store_data_job.SaveDataRedisJob", return_value=mock_job)
    job_id = store_data_job._save_data_job(data, _uuid, mock_BackgroundTasks, enqueue)
    assert job_id == expected
