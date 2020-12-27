from typing import List, Any
import numpy as np
import onnxruntime as rt
from PIL import Image
from collections import OrderedDict
import joblib
import os

from src.app.configurations import _ModelConfigurations
from src.app.constants import MODEL_RUNTIME
from src.app.ml.base_predictor import BaseData, BaseDataInterface, BaseDataConverter, BasePredictor
from src.app.ml.transformers import PytorchImagePreprocessTransformer, SoftmaxTransformer
from src.app.ml.save_helper import load_labels

import logging


logger = logging.getLogger(__name__)

LABELS = load_labels(_ModelConfigurations().options["label_filepath"])


class _Data(BaseData):
    image_data: Any = None
    test_data: str = os.path.join("./src/app/ml/resnet50_onnx/data", "good_cat.jpg")
    labels: List[str] = LABELS


class _DataInterface(BaseDataInterface):
    pass


class _DataConverter(BaseDataConverter):
    pass


class _Classifier(BasePredictor):
    def __init__(self, model_runners):
        self.model_runners = model_runners
        self.classifiers = OrderedDict()
        self.input_name = None
        self.output_name = None
        self.load_model()

    def load_model(self):
        logger.info(f"run load model in {self.__class__.__name__}")
        for m in self.model_runners:
            logger.info(f"{m.items()}")
            for k, v in m.items():
                if v == MODEL_RUNTIME.SKLEARN.value:
                    self.classifiers[k] = {"runner": v, "predictor": joblib.load(k)}
                elif v == MODEL_RUNTIME.ONNX_RUNTIME.value:
                    self.classifiers[k] = {"runner": v, "predictor": rt.InferenceSession(k)}
                    self.input_name = self.classifiers[k]["predictor"].get_inputs()[0].name
                    self.output_name = self.classifiers[k]["predictor"].get_outputs()[0].name
                else:
                    pass
        logger.info(f"initialized {self.__class__.__name__}")

    def predict(self, input_data: Image) -> np.ndarray:
        logger.info(f"run predict proba in {self.__class__.__name__}")
        _prediction = input_data
        for k, v in self.classifiers.items():
            if v["runner"] == MODEL_RUNTIME.SKLEARN.value:
                _prediction = np.array(v["predictor"].transform(_prediction))
            elif v["runner"] == MODEL_RUNTIME.ONNX_RUNTIME.value:
                _prediction = np.array(v["predictor"].run([self.output_name], {self.input_name: _prediction.astype(np.float32)}))
        output = _prediction
        return output

    async def async_predict(self, input_data: Image) -> np.ndarray:
        logger.info(f"run predict proba in {self.__class__.__name__}")
        output = self.predict(input_data)
        return output
