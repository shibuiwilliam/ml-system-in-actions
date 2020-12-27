import os
from src.app.constants import PHYSICAL_SAVE_DATA
from src.app.ml.extract_interface import extract_interface_yaml
import logging

logger = logging.getLogger(__name__)


class _APIConfigurations:
    title = os.getenv("API_TITLE", "ServingPattern")
    description = os.getenv("API_DESCRIPTION", "machine learning system serving patterns")
    version = os.getenv("API_VERSION", "0.1")
    app_name = os.getenv("APP_NAME", "src.app.apps.app_web_single:app")


class _ModelConfigurations:
    interface_filepath = os.getenv("MODEL_INTERFACE")
    if interface_filepath is None:
        logging.info('Environment variable "MODEL_INTERFACE" must be specified.')
        interface_filepath = "./models/iris_svc_sklearn.yaml"

    interface_dict = extract_interface_yaml(interface_filepath)
    model_name = list(interface_dict.keys())[0]
    io = interface_dict[model_name]["data_interface"]
    meta = interface_dict[model_name]["meta"]

    model_runners = meta["models"]
    prediction_type = meta["prediction_type"]
    runner = meta["runner"]

    options = interface_dict[model_name].get("options", None)

    physical_save_data = os.getenv("PHYSICAL_SAVE_DATA", PHYSICAL_SAVE_DATA.SAVE)


APIConfigurations = _APIConfigurations()
ModelConfigurations = _ModelConfigurations()
logger.info(f"model configurations: {ModelConfigurations.__dict__}")
logger.info(f"api configurations: {APIConfigurations.__dict__}")
