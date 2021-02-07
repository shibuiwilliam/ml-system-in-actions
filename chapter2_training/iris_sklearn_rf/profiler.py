import cProfile
import os
from logging import getLogger

logger = getLogger(__name__)


def do_cprofile(func):
    def profiled_func(*args, **kwargs):
        enable_profile = int(os.getenv("PROFILE", 1))
        if enable_profile:
            profile = cProfile.Profile()
            try:
                profile.enable()
                result = func(*args, **kwargs)
                profile.disable()
                return result
            finally:
                profile.print_stats()
        else:
            return func(*args, **kwargs)

    return profiled_func
