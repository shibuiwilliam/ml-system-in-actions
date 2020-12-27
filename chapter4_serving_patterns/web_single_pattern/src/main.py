import os
import logging
import sys

from gunicorn.app.base import BaseApplication
from gunicorn.glogging import Logger
from loguru import logger

from src.app.app import app
from src.configurations import (
    PlatformConfigurations,
    APIConfigurations,
    CacheConfigurations,
    RedisCacheConfigurations,
    ModelConfigurations,
)

LOG_LEVEL = logging.getLevelName(os.getenv("LOG_LEVEL", "DEBUG"))
JSON_LOGS = True if os.getenv("LOG_FORMAT", "text").lower() == "json" else False


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


class StubbedGunicornLogger(Logger):
    def setup(self, cfg):
        handler = logging.NullHandler()
        self.error_logger = logging.getLogger("gunicorn.error")
        self.error_logger.addHandler(handler)
        self.access_logger = logging.getLogger("gunicorn.access")
        self.access_logger.addHandler(handler)
        self.error_logger.setLevel(LOG_LEVEL)
        self.access_logger.setLevel(LOG_LEVEL)


class StandaloneApplication(BaseApplication):
    """Our Gunicorn application."""

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items() if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    workers = int(os.getenv("WORKERS", 4))
    backlog = int(os.getenv("BACKLOG", 2048))
    max_requests = int(os.getenv("MAX_REQUESTS", 65536))
    max_requests_jitter = int(os.getenv("MAX_REQUESTS_JITTER", 2048))
    graceful_timeout = int(os.getenv("GRACEFUL_TIMEOUT", 10))

    intercept_handler = InterceptHandler()
    # logging.basicConfig(handlers=[intercept_handler], level=LOG_LEVEL)
    # logging.root.handlers = [intercept_handler]
    logging.root.setLevel(LOG_LEVEL)

    seen = set()
    for name in [
        *logging.root.manager.loggerDict.keys(),
        "gunicorn",
        "gunicorn.access",
        "gunicorn.error",
        "uvicorn",
        "uvicorn.access",
        "uvicorn.error",
    ]:
        if name not in seen:
            seen.add(name.split(".")[0])
            logging.getLogger(name).handlers = [intercept_handler]

    logger.configure(handlers=[{"sink": sys.stdout, "serialize": JSON_LOGS}])

    logger.debug(f"{PlatformConfigurations.__name__}:\n{PlatformConfigurations.__dict__}")
    logger.debug(f"{CacheConfigurations.__name__}: {CacheConfigurations.__dict__}")
    logger.debug(f"{RedisCacheConfigurations.__name__}: {RedisCacheConfigurations.__dict__}")
    logger.debug(f"{APIConfigurations.__name__}: {APIConfigurations.__dict__}")
    logger.debug(f"{ModelConfigurations.__name__}: {ModelConfigurations.__dict__}")

    options = {
        "bind": f"0.0.0.0:{port}",
        "workers": workers,
        "backlog": backlog,
        "max_requests": max_requests,
        "max_requests_jitter": max_requests_jitter,
        "graceful_timeout": graceful_timeout,
        "accesslog": "-",
        "errorlog": "-",
        "worker_class": "uvicorn.workers.UvicornWorker",
        "logger_class": StubbedGunicornLogger,
    }

    StandaloneApplication(app, options).run()