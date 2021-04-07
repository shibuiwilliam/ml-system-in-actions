import os
from logging import getLogger
from typing import Dict

logger = getLogger(__name__)


class ServiceConfigurations:
    services: Dict[str, str] = {}
    thresholds: Dict[str, float] = {}
    default_threshold: float = float(
        os.getenv(
            "DEFAULT_THRESHOLD",
            0.95,
        )
    )
    activates: Dict[str, bool] = {}
    for environ in os.environ.keys():
        if environ.startswith("SERVICE_"):
            url = str(os.getenv(environ))
            if not url.startswith("http"):
                url = f"http://{url}"
            services[environ.lower().replace("service_", "")] = url
        if environ.startswith("THRESHOLD_"):
            threshold_key = environ.lower().replace("threshold_", "")
            thresholds[threshold_key] = float(os.getenv(environ, 0.95))
        if environ.startswith("ACTIVATE_"):
            activate_key = environ.lower().replace("activate_", "")
            if int(os.getenv(environ)) == 1:
                activates[activate_key] = True
            else:
                activates[activate_key] = False


class APIConfigurations:
    title = os.getenv("API_TITLE", "ServingPattern")
    description = os.getenv("API_DESCRIPTION", "machine learning system serving patterns")
    version = os.getenv("API_VERSION", "0.1")


logger.info(f"{ServiceConfigurations.__name__}: {ServiceConfigurations.__dict__}")
logger.info(f"{APIConfigurations.__name__}: {APIConfigurations.__dict__}")
