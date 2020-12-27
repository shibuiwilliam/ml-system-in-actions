import logging
import importlib

from src.app.configurations import ModelConfigurations

runner = importlib.import_module(ModelConfigurations.runner)


logger = logging.getLogger(__name__)
ActiveData = runner._Data
ActiveDataInterface = runner._DataInterface
ActiveDataConverter = runner._DataConverter
ActivePredictor = runner._Classifier


class Data(ActiveData):
    pass


class DataInterface(ActiveDataInterface):
    pass


class DataConverter(ActiveDataConverter):
    pass


class Predictor(ActivePredictor):
    pass


DataInterface.input_shape = ModelConfigurations.io["input_shape"]
DataInterface.input_type = ModelConfigurations.io["input_type"]
DataInterface.output_shape = ModelConfigurations.io["output_shape"]
DataInterface.output_type = ModelConfigurations.io["output_type"]
DataInterface.data_type = ModelConfigurations.io["data_type"]

DataConverter.data_interface = DataInterface

active_predictor = Predictor(ModelConfigurations.model_runners)
