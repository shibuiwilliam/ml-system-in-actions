import json
from logging import getLogger
from typing import Dict, List, Sequence

import numpy as np
import onnxruntime as rt
from pydantic import BaseModel
from src.configurations import ModelConfigurations

logger = getLogger(__name__)


class Data(BaseModel):
    data: List[List[float]] = [[5.1, 3.5, 1.4, 0.2]]


class Classifier(object):
    def __init__(
        self,
        model_filepath: str,
    ):
        self.model_filepath: str = model_filepath
        self.classifier = None
        self.input_name: str = ""
        self.output_name: str = ""

        self.load_model()

    def load_model(self):
        logger.info(f"load model in {self.model_filepath}")
        self.classifier = rt.InferenceSession(self.model_filepath)
        self.input_name = self.classifier.get_inputs()[0].name
        self.output_name = self.classifier.get_outputs()[0].name
        logger.info(f"initialized model")

    def predict(self, data: List[List[float]]) -> List[float]:
        np_data = np.array(data).astype(np.float32)
        prediction = self.classifier.run(None, {self.input_name: np_data})
        return prediction[1][0].values()


classifier = Classifier(model_filepath=ModelConfigurations().model_filepath)
