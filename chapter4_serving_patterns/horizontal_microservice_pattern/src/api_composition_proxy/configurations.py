import logging
import os
from typing import Dict

logger = logging.getLogger(__name__)


class ServiceConfigurations:
    services: Dict[str, str] = {}
    for environ in os.environ.keys():
        if environ.startswith("SERVICE_"):
            url = f"http://{os.getenv(environ)}"
            services[environ.lower().replace("service_", "")] = url


class APIConfigurations:
    title = os.getenv("API_TITLE", "ServingPattern")
    description = os.getenv("API_DESCRIPTION", "machine learning system serving patterns")
    version = os.getenv("API_VERSION", "0.1")


logger.info(f"{ServiceConfigurations.__name__}: {ServiceConfigurations.__dict__}")
logger.info(f"{APIConfigurations.__name__}: {APIConfigurations.__dict__}")
