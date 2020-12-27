import pytest
from src.app.api._health import health, health_sync, health_async


HEALTH = {"health": "ok"}


@pytest.mark.parametrize(("expected"), [(HEALTH)])
def test_health(expected):
    result = health()
    assert result == expected


@pytest.mark.parametrize(("expected"), [(HEALTH)])
def test_health_sync(expected):
    result = health_sync()
    assert result == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(("expected"), [(HEALTH)])
async def test_health_async(expected):
    result = await health_async()
    assert result == expected
