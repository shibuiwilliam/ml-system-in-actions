import argparse
import json
import logging
import os
import time
from typing import Dict, List, Tuple, Union

import grpc
import mlflow
import numpy as np
from PIL import Image
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.metrics import accuracy_score
from src.proto import onnx_ml_pb2, predict_pb2, prediction_service_pb2_grpc

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PytorchImagePreprocessTransformer(
    BaseEstimator,
    TransformerMixin,
):
    def __init__(
        self,
        image_size: Tuple[int, int] = (32, 32),
        prediction_shape: Tuple[int, int, int, int] = (1, 3, 32, 32),
        mean_vec: List[float] = [0.485, 0.456, 0.406],
        stddev_vec: List[float] = [0.229, 0.224, 0.225],
    ):
        self.image_size = image_size
        self.prediction_shape = prediction_shape
        self.mean_vec = mean_vec
        self.stddev_vec = stddev_vec

    def fit(self, X, y=None):
        return self

    def transform(self, X: Union[Image.Image, np.ndarray]) -> np.ndarray:
        if isinstance(X, np.ndarray):
            dim_0 = (3,) + self.image_size
            dim_1 = self.image_size + (3,)
            if X.shape != dim_0 and X.shape != dim_1:
                raise ValueError(f"resize to image_size {self.image_size} beforehand for numpy array")
        else:
            X = np.array(X.resize(self.image_size))

        image_data = X.transpose(2, 0, 1).astype(np.float32)
        mean_vec = np.array(self.mean_vec)
        stddev_vec = np.array(self.stddev_vec)
        norm_image_data = np.zeros(image_data.shape).astype(np.float32)
        for i in range(image_data.shape[0]):
            norm_image_data[i, :, :] = (image_data[i, :, :] / 255 - mean_vec[i]) / stddev_vec[i]
        norm_image_data = norm_image_data.reshape(self.prediction_shape).astype(np.float32)
        return norm_image_data


class SoftmaxTransformer(
    BaseEstimator,
    TransformerMixin,
):
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(
        self,
        X: Union[np.ndarray, List[float], List[List[float]]],
    ) -> np.ndarray:
        if isinstance(X, List):
            X = np.array(X)
        x = X.reshape(-1)
        e_x = np.exp(x - np.max(x))
        result = np.array([e_x / e_x.sum(axis=0)])
        return result


class Classifier(object):
    def __init__(
        self,
        preprocess_transformer: BaseEstimator = PytorchImagePreprocessTransformer,
        softmax_transformer: BaseEstimator = SoftmaxTransformer,
        serving_address: str = "localhost:50051",
        onnx_input_name: str = "input",
        onnx_output_name: str = "output",
    ):
        self.preprocess_transformer: BaseEstimator = preprocess_transformer()
        self.preprocess_transformer.fit(None)
        self.softmax_transformer: BaseEstimator = softmax_transformer()
        self.softmax_transformer.fit(None)

        self.serving_address = serving_address
        self.channel = grpc.insecure_channel(self.serving_address)
        self.stub = prediction_service_pb2_grpc.PredictionServiceStub(self.channel)

        self.onnx_input_name: str = onnx_input_name
        self.onnx_output_name: str = onnx_output_name

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

    def predict_label(self, data: Image) -> int:
        softmax = self.predict(data=data)
        argmax = int(np.argmax(np.array(softmax)[0]))
        logger.info(f"predict label {argmax}")
        return argmax


def evaluate(
    test_data_directory: str,
    preprocess_transformer: BaseEstimator = PytorchImagePreprocessTransformer,
    softmax_transformer: BaseEstimator = SoftmaxTransformer,
) -> Dict:
    classifier = Classifier(
        preprocess_transformer=preprocess_transformer,
        softmax_transformer=softmax_transformer,
        serving_address="localhost:50051",
        onnx_input_name="input",
        onnx_output_name="output",
    )

    directory_list = os.listdir(test_data_directory)
    predictions = {}
    predicted = []
    labels = []
    durations = []
    for c in directory_list:
        c_path = os.path.join(test_data_directory, c)
        c_list = os.listdir(c_path)

        for f in c_list:
            image_path = os.path.join(c_path, f)
            image = Image.open(image_path)
            start = time.time()
            x = classifier.predict_label(image)
            end = time.time()
            duration = end - start
            predicted.append(x)
            labels.append(int(c))
            durations.append(duration)
            predictions[image_path] = {"label": c, "prediction": x}
            logger.info(f"{image_path} label: {c} predicted: {x} duration: {duration} seconds")
    total_time = sum(durations)
    total_tested = len(predicted)
    average_duration_second = total_time / total_tested
    accuracy = accuracy_score(labels, predicted)

    evaluation = {
        "total_tested": total_tested,
        "accuracy": accuracy,
        "total_time": total_time,
        "average_duration_second": average_duration_second,
    }

    return {"evaluation": evaluation, "predictions": predictions}


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate Cifar10 model",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--upstream",
        type=str,
        default="/opt/data/train",
        help="upstream directory",
    )
    parser.add_argument(
        "--downstream",
        type=str,
        default="/opt/data/evaluate/",
        help="downstream directory",
    )
    parser.add_argument(
        "--test_data_directory",
        type=str,
        default="/opt/data/preprocess/test",
        help="test data directory",
    )
    args = parser.parse_args()
    mlflow_experiment_id = int(os.getenv("MLFLOW_EXPERIMENT_ID", 0))

    upstream_directory = args.upstream
    downstream_directory = args.downstream
    os.makedirs(upstream_directory, exist_ok=True)
    os.makedirs(downstream_directory, exist_ok=True)

    result = evaluate(
        test_data_directory=args.test_data_directory,
    )

    log_file = os.path.join(downstream_directory, f"{mlflow_experiment_id}.json")
    with open(log_file, "w") as f:
        json.dump(log_file, f)

    mlflow.log_metric(
        "total_tested",
        result["evaluation"]["total_tested"],
    )
    mlflow.log_metric(
        "total_time",
        result["evaluation"]["total_time"],
    )
    mlflow.log_metric(
        "accuracy",
        result["evaluation"]["accuracy"],
    )
    mlflow.log_metric(
        "average_duration_second",
        result["evaluation"]["average_duration_second"],
    )
    mlflow.log_artifact(log_file)


if __name__ == "__main__":
    main()
