import cProfile
import time
from logging import getLogger

logger = getLogger(__name__)


def do_cprofile(func):
    def profiled_func(*args, **kwargs):
        profile = cProfile.Profile()
        try:
            profile.enable()
            result = func(*args, **kwargs)
            profile.disable()
            return result
        finally:
            profile.print_stats()

    return profiled_func


def wrap_time(logger=logger):
    def _log_decorator(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            res = func(*args, **kwargs)
            logger.info(f"time: {1000*(time.time() - start)} ms")
            return res

        return wrapper

    return _log_decorator
