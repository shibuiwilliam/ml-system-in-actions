import json
from logging import getLogger
from typing import Any, List

import grpc
import joblib
import numpy as np
from PIL import Image
from pydantic import BaseModel
from src.configurations import ModelConfigurations
from src.ml.transformers import PytorchImagePreprocessTransformer, SoftmaxTransformer
from src.proto import onnx_ml_pb2, predict_pb2, prediction_service_pb2_grpc

logger = getLogger(__name__)


class Data(BaseModel):
    data: Any = ModelConfigurations.sample_image


class Classifier(object):
    def __init__(
        self,
        preprocess_transformer_path: str = "/prep_pred_pattern/models/preprocess_transformer.pkl",
        softmax_transformer_path: str = "/prep_pred_pattern/models/softmax_transformer.pkl",
        label_path: str = "/prep_pred_pattern/data/image_net_labels.json",
        serving_address: str = "localhost:50051",
        onnx_input_name: str = "input",
        onnx_output_name: str = "output",
    ):
        self.preprocess_transformer_path: str = preprocess_transformer_path
        self.softmax_transformer_path: str = softmax_transformer_path
        self.preprocess_transformer: PytorchImagePreprocessTransformer = None
        self.softmax_transformer: SoftmaxTransformer = None

        self.serving_address = serving_address
        self.channel = grpc.insecure_channel(self.serving_address)
        self.stub = prediction_service_pb2_grpc.PredictionServiceStub(self.channel)

        self.label_path = label_path
        self.label: List[str] = []

        self.onnx_input_name: str = onnx_input_name
        self.onnx_output_name: str = onnx_output_name

        self.load_model()
        self.load_label()

    def load_model(self):
        logger.info(f"load preprocess in {self.preprocess_transformer_path}")
        self.preprocess_transformer = joblib.load(self.preprocess_transformer_path)
        logger.info(f"initialized preprocess")

        logger.info(f"load postprocess in {self.softmax_transformer_path}")
        self.softmax_transformer = joblib.load(self.softmax_transformer_path)
        logger.info(f"initialized postprocess")

    def load_label(self):
        logger.info(f"load label in {self.label_path}")
        with open(self.label_path, "r") as f:
            self.label = json.load(f)
        logger.info(f"label: {self.label}")

    def predict(self, data: Image) -> List[float]:
        preprocessed = self.preprocess_transformer.transform(data)

        input_tensor = onnx_ml_pb2.TensorProto()
        input_tensor.dims.extend(preprocessed.shape)
        input_tensor.data_type = 1
        input_tensor.raw_data = preprocessed.tobytes()

        request_message = predict_pb2.PredictRequest()
        request_message.inputs[self.onnx_input_name].data_type = input_tensor.data_type
        request_message.inputs[self.onnx_input_name].dims.extend(preprocessed.shape)
        request_message.inputs[self.onnx_input_name].raw_data = input_tensor.raw_data

        response = self.stub.Predict(request_message)
        output = np.frombuffer(response.outputs[self.onnx_output_name].raw_data, dtype=np.float32)

        softmax = self.softmax_transformer.transform(output).tolist()

        logger.info(f"predict proba {softmax}")
        return softmax

    def predict_label(self, data: Image) -> str:
        softmax = self.predict(data=data)
        argmax = int(np.argmax(np.array(softmax)[0]))
        return self.label[argmax]


classifier = Classifier(
    preprocess_transformer_path=ModelConfigurations().preprocess_transformer_path,
    softmax_transformer_path=ModelConfigurations().softmax_transformer_path,
    label_path=ModelConfigurations().label_path,
    serving_address=f"{ModelConfigurations.api_address}:{ModelConfigurations.grpc_port}",
    onnx_input_name=ModelConfigurations().onnx_input_name,
    onnx_output_name=ModelConfigurations().onnx_output_name,
)
