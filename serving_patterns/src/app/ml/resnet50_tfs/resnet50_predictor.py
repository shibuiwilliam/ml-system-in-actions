from typing import List, Any
import numpy as np

from PIL import Image
from collections import OrderedDict
import joblib
import os

import grpc
import tensorflow as tf
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2_grpc

from src.app.configurations import _ModelConfigurations
from src.app.constants import MODEL_RUNTIME
from src.app.ml.base_predictor import BaseData, BaseDataInterface, BaseDataConverter, BasePredictor
from src.app.ml.transformers import PytorchImagePreprocessTransformer, SoftmaxTransformer
from src.app.ml.save_helper import load_labels

import logging


logger = logging.getLogger(__name__)


LABELS = load_labels(_ModelConfigurations().options["label_filepath"])
TFS_GPRC = os.getenv("TFS_GRPC", "prep_pred_tfs:8510")
TIMEOUT_SECOND = int(os.getenv("TIMEOUT_SECOND", 5.0))


class _Data(BaseData):
    image_data: Any = None
    test_data: str = os.path.join("./src/app/ml/resnet50_tfs/data", "good_cat.jpg")
    labels: List[str] = LABELS


class _DataInterface(BaseDataInterface):
    input_name = os.getenv("INPUT_NAME", _ModelConfigurations().options["input_name"])
    output_name = os.getenv("OUTPUT_NAME", _ModelConfigurations().options["output_name"])


class _DataConverter(BaseDataConverter):
    pass


class _Classifier(BasePredictor):
    def __init__(self, model_runners):
        self.model_runners = model_runners
        self.classifiers = OrderedDict()
        self.input_name = None
        self.channel = None
        self.stub = None
        self.model_spec_name = os.getenv("MODEL_SPEC_NAME", _ModelConfigurations().options["model_spec_name"])
        self.model_spec_signature_name = os.getenv("MODEL_SPEC_SIGNATURE_NAME", _ModelConfigurations().options["model_spec_signature_name"])
        self.load_model()

    def load_model(self):
        logger.info(f"run load model in {self.__class__.__name__}")
        for m in self.model_runners:
            logger.info(f"{m.items()}")
            for k, v in m.items():
                if v == MODEL_RUNTIME.SKLEARN.value:
                    self.classifiers[k] = {"runner": v, "predictor": joblib.load(k)}
                else:
                    self.classifiers[k] = {"runner": v, "predictor": None}
                    self.channel = grpc.insecure_channel(TFS_GPRC)
                    self.stub = prediction_service_pb2_grpc.PredictionServiceStub(self.channel)
        logger.info(f"initialized {self.__class__.__name__}")

    def predict(self, input_data: Image) -> np.ndarray:
        logger.info(f"run predict proba in {self.__class__.__name__}")
        _prediction = input_data
        for k, v in self.classifiers.items():
            if v["runner"] == MODEL_RUNTIME.SKLEARN.value:
                _prediction = np.array(v["predictor"].transform(_prediction))
            else:
                request = predict_pb2.PredictRequest()
                request.model_spec.name = self.model_spec_name
                request.model_spec.signature_name = self.model_spec_signature_name
                request.inputs[_DataInterface().input_name].CopyFrom(tf.make_tensor_proto(_prediction, shape=_ModelConfigurations().io["input_shape"]))
                result = self.stub.Predict(request, TIMEOUT_SECOND)
                _prediction = np.array(result.outputs[_DataInterface().output_name].float_val)
        output = _prediction
        return output

    async def async_predict(self, input_data: Image) -> np.ndarray:
        logger.info(f"run predict proba in {self.__class__.__name__}")
        output = self.predict(input_data)
        return output
