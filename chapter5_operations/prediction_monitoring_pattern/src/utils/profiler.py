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


def log_decorator(endpoint: str = "/", logger=logger):
    def _log_decorator(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            res = func(*args, **kwargs)
            elapsed = 1000 * (time.time() - start)
            job_id = kwargs.get("job_id")
            data = kwargs.get("data")
            prediction = res.get("prediction")
            is_outlier = res.get("is_outlier")
            outlier_score = res.get("outlier_score")
            logger.info(
                f"[{endpoint}] [{job_id}] [{elapsed} ms] [{data}] [{prediction}] [{is_outlier}] [{outlier_score}]"
            )
            return res

        return wrapper

    return _log_decorator
