import os
from typing import Tuple

import mlflow
import mlflow.sklearn
import numpy as np
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType
from sklearn.datasets import load_iris
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import OneClassSVM


def get_data() -> Tuple[np.ndarray]:
    iris = load_iris()
    data = iris.data
    data = np.array(data).astype("float32")
    return data


def define_ocs_pipeline() -> Pipeline:
    steps = [("normalize", StandardScaler()), ("ocs", OneClassSVM(nu=0.1, gamma="auto"))]
    pipeline = Pipeline(steps=steps)
    return pipeline


def train(model, data):
    model.fit(data)


def evaluate(model, data) -> float:
    size = len(data)
    predict = model.predict(data)
    return sum(predict) / size


def save_onnx(model, filepath: str):
    initial_type = [("float_input", FloatTensorType([None, 4]))]
    onx = convert_sklearn(model, initial_types=initial_type)
    with open(filepath, "wb") as f:
        f.write(onx.SerializeToString())


def main():
    mlflow_experiment_id = int(os.getenv("MLFLOW_EXPERIMENT_ID", 0))

    data = get_data()

    model = define_ocs_pipeline()

    train(model, data)

    outlier_rate = evaluate(model, data)

    mlflow.log_param("normalize", "StandardScaler")
    mlflow.log_param("model", "one_class_svm")
    mlflow.log_metric("outlier_rate", outlier_rate)
    mlflow.sklearn.log_model(model, "model")

    onnx_name = f"iris_ocs_{mlflow_experiment_id}.onnx"
    onnx_path = os.path.join("/tmp/", onnx_name)
    save_onnx(model, onnx_path)
    mlflow.log_artifact(onnx_path)


if __name__ == "__main__":
    main()
