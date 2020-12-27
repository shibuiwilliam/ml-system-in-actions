import datetime
import os
import sys
import logging
from logging import DEBUG, INFO, FileHandler, Formatter, StreamHandler, getLogger

from pythonjsonlogger import jsonlogger
import uuid

LOG_LEVEL = os.getenv("LOG_LEVEL", DEBUG)
LOG_FORMAT = os.getenv("LOG_FORMAT", "text")


def CustomTextFormatter():
    return logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [process] %(process)s %(processName)s [thread] %(thread)d %(threadName)s [file] %(pathname)s [func] %(funcName)s [line] %(lineno)d [%(message)s]"
    )


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def parse(self):
        return [
            "timestamp",
            "level",
            "process",
            "processName",
            "thread",
            "threadName",
            "pathname",
            "funcName",
            "lineno",
            "message",
        ]

    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get("timestamp"):
            now = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            log_record["timestamp"] = now
        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname


class SensitiveWordFilter(logging.Filter):
    def filter(self, record):
        sensitive_words = [
            "username",
            "password",
            "auth_token",
            "token",
            "secret",
        ]
        log_message = record.getMessage()
        for word in sensitive_words:
            if word in log_message:
                return False
        return True


def configure_logger(log_folder=f"/tmp/{datetime.date.today()}.log", modname=__name__):
    logger = getLogger(modname)
    logger.addFilter(SensitiveWordFilter())
    logger.setLevel(LOG_LEVEL)

    if LOG_FORMAT.lower() == "json":
        formatter = CustomJsonFormatter()
        fh_formatter = CustomJsonFormatter()
    elif LOG_FORMAT.lower() == "text":
        formatter = CustomTextFormatter()
        fh_formatter = CustomTextFormatter()
    else:
        formatter = CustomJsonFormatter()
        fh_formatter = CustomJsonFormatter()

    sh = StreamHandler()
    sh.setLevel(LOG_LEVEL)
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    fh = FileHandler(log_folder)
    fh.setLevel(LOG_LEVEL)
    fh.setFormatter(fh_formatter)
    logger.addHandler(fh)

    return logger


def override_uvicorn_logger(log_folder=f"/tmp/{datetime.date.today()}.log"):
    def _override_uvicorn_logger(modname):
        logger = getLogger(modname)
        logger.addFilter(SensitiveWordFilter())
        logger.setLevel(LOG_LEVEL)

        if LOG_FORMAT.lower() == "json":
            formatter = CustomJsonFormatter()
            fh_formatter = CustomJsonFormatter()
        elif LOG_FORMAT.lower() == "text":
            formatter = CustomTextFormatter()
            fh_formatter = CustomTextFormatter()
        else:
            formatter = CustomJsonFormatter()
            fh_formatter = CustomJsonFormatter()

        sh = StreamHandler()
        sh.setLevel(LOG_LEVEL)
        sh.setFormatter(formatter)
        logger.addHandler(sh)

        fh = FileHandler(log_folder)
        fh.setLevel(LOG_LEVEL)
        fh.setFormatter(fh_formatter)
        logger.addHandler(fh)

    _override_uvicorn_logger(modname="uvicorn.asgi")
    _override_uvicorn_logger(modname="uvicorn.error")
    _override_uvicorn_logger(modname="uvicorn.access")


def log_decorator(logger=configure_logger()):
    def _log_decorator(func):
        def wrapper(*args, **kwargs):
            job_id = str(uuid.uuid4())[:6]
            logger.debug(f"START {job_id} func:{func.__name__} args:{args}  kwargs:{kwargs}")
            res = func(*args, **kwargs)
            logger.debug(f"RETURN FROM {job_id} return:{res}")
            return res

        return wrapper

    return _log_decorator