from typing import List
import numpy as np
from fastapi import BackgroundTasks
import json
import joblib
import os
from PIL import Image
import requests
from onnx import numpy_helper
from google.protobuf.json_format import MessageToJson
from src.proto import predict_pb2, onnx_ml_pb2

from pydantic import BaseModel
from src.configurations import ModelConfigurations
from src.app.backend import background_job
from src.ml.transformers import PytorchImagePreprocessTransformer, SoftmaxTransformer
from logging import getLogger

logger = getLogger(__name__)


class Data(BaseModel):
    data: str = "0000"


class Classifier(object):
    def __init__(
        self,
        preprocess_transformer_path: str = "/data_cache_pattern/models/preprocess_transformer.pkl",
        softmax_transformer_path: str = "/data_cache_pattern/models/softmax_transformer.pkl",
        label_path: str = "/data_cache_pattern/data/image_net_labels.json",
        api_address: str = "localhost",
        rest_api_port: int = 8001,
        grpc_port: int = 50051,
        onnx_input_name: str = "input",
        onnx_output_name: str = "output",
    ):
        self.preprocess_transformer_path: str = preprocess_transformer_path
        self.softmax_transformer_path: str = softmax_transformer_path
        self.preprocess_transformer: PytorchImagePreprocessTransformer = None
        self.softmax_transformer: SoftmaxTransformer = None

        self.label_path = label_path
        self.label: List[str] = []

        self.api_address = api_address
        self.rest_api_port = rest_api_port
        self.grpc_port = grpc_port

        self.rest_api_address = f"http://{self.api_address}:{self.rest_api_port}/v1/models/default/versions/1:predict"

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

    async def predict(
        self,
        data: Data,
        background_tasks: BackgroundTasks,
    ) -> List[float]:
        cache_data = background_job.get_data_redis(key=data.data)
        if cache_data is None:
            logger.info(f"registering cache: {data.data}")
            image = Image.open(os.path.join("data/", f"{data.data}.jpg"))
            preprocessed = self.preprocess_transformer.transform(image)
            background_job.save_data_job(data=list(preprocessed), item_id=data.data, background_tasks=background_tasks)
        else:
            logger.info(f"cache hit: {data.data}")
            preprocessed = np.array(cache_data)

        _tensor_proto = numpy_helper.from_array(preprocessed)
        tensor_proto = onnx_ml_pb2.TensorProto()
        tensor_proto.ParseFromString(_tensor_proto.SerializeToString())
        predict_request = predict_pb2.PredictRequest()
        predict_request.inputs[self.onnx_input_name].CopyFrom(tensor_proto)
        predict_request.output_filter.append(self.onnx_output_name)
        payload = predict_request.SerializeToString()
        response = requests.post(
            self.rest_api_address,
            data=payload,
            headers={"Content-Type": "application/octet-stream", "Accept": "application/x-protobuf"},
        )
        actual_result = predict_pb2.PredictResponse()
        actual_result.ParseFromString(response.content)
        prediction = np.frombuffer(actual_result.outputs[self.onnx_output_name].raw_data, dtype=np.float32)

        softmax = self.softmax_transformer.transform(prediction).tolist()

        logger.info(f"predict proba {softmax}")
        return softmax

    async def predict_label(
        self,
        data: Data,
        background_tasks: BackgroundTasks,
    ) -> str:
        softmax = await self.predict(data=data, background_tasks=background_tasks)
        argmax = int(np.argmax(np.array(softmax)[0]))
        return self.label[argmax]


classifier = Classifier(
    preprocess_transformer_path=ModelConfigurations().preprocess_transformer_path,
    softmax_transformer_path=ModelConfigurations().softmax_transformer_path,
    label_path=ModelConfigurations().label_path,
    api_address=ModelConfigurations().api_address,
    rest_api_port=ModelConfigurations().rest_api_port,
    grpc_port=ModelConfigurations().grpc_port,
    onnx_input_name=ModelConfigurations().onnx_input_name,
    onnx_output_name=ModelConfigurations().onnx_output_name,
)
