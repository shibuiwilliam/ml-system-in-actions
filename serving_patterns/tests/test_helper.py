import pytest

from src.helper import get_uuid, get_incremental_id, get_uuid_incremental_id


def test_get_uuid():
    assert get_uuid()


@pytest.mark.parametrize(("incr"), [(0), (1), (100)])
def test_incremental_id(mocker, incr):
    mocker.patch("src.middleware.redis_client.redis_client.get", return_value=incr)
    mocker.patch("src.middleware.redis_client.redis_client.incr", return_value=0)
    result = get_incremental_id()
    assert result == incr


@pytest.mark.parametrize(("incr"), [(0), (1), (100)])
def test_get_uuid_incremental_id(mocker, incr):
    mocker.patch("src.middleware.redis_client.redis_client.get", return_value=incr)
    mocker.patch("src.middleware.redis_client.redis_client.incr", return_value=0)
    result = get_uuid_incremental_id()
    assert result.split("_")[-1] == str(incr)
