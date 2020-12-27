from typing import List, Sequence
import joblib
import numpy as np

from src.app.configurations import _ModelConfigurations
from src.app.ml.base_predictor import BaseData, BaseDataInterface, BaseDataConverter, BasePredictor
from src.app.ml.save_helper import load_labels
import logging


logger = logging.getLogger(__name__)

LABELS = load_labels(_ModelConfigurations().options["label_filepath"])


class _Data(BaseData):
    test_data: List[List[int]] = [[5.1, 3.5, 1.4, 0.2]]
    labels: List[str] = LABELS


class _DataInterface(BaseDataInterface):
    pass


class _DataConverter(BaseDataConverter):
    pass


class _Classifier(BasePredictor):
    def __init__(self, model_runners):
        self.model_runners = model_runners
        self.classifier = None
        self.load_model()

    def load_model(self):
        logger.info(f"run load model in {self.__class__.__name__}")
        for k, v in self.model_runners[0].items():
            self.classifier = joblib.load(k)
        logger.info(f"initialized {self.__class__.__name__}")

    def predict(self, input: np.ndarray) -> np.ndarray:
        logger.info(f"run predict proba in {self.__class__.__name__}")
        output = self.classifier.predict_proba(input)
        return output

    async def async_predict(self, input: np.ndarray) -> np.ndarray:
        logger.info(f"run predict proba in {self.__class__.__name__}")
        output = self.predict(input)
        return output
