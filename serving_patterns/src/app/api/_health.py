from typing import Dict
import logging
from src.middleware.profiler import do_cprofile

logger = logging.getLogger(__name__)


@do_cprofile
def health() -> Dict[str, str]:
    return {"health": "ok"}


def health_sync() -> Dict[str, str]:
    return health()


async def health_async() -> Dict[str, str]:
    return health()
