from sklearn import metrics
import onnxruntime as rt
import os
import numpy as np
import joblib
import json
from typing import Dict, Any
import yaml
import sys

sys.path.append(os.path.abspath(".."))
from constants import PREDICTION_TYPE, MODEL_RUNTIME, DATA_TYPE
import save_helper


PARAMS_YAML = "./params.yaml"

DATA_DIR = "./data/"
PREPARED_DIR = os.path.join(DATA_DIR, "prepared")
MODEL_DIR = os.path.join(DATA_DIR, "trained")
X_TEST_NPY = os.path.join(PREPARED_DIR, "x_test.npy")
Y_TEST_NPY = os.path.join(PREPARED_DIR, "y_test.npy")
DOWNSTREAM_DIR = os.path.join(DATA_DIR, "evaluated")
EVALUATION_SCORE = os.path.join(DOWNSTREAM_DIR, "score.json")


def get_params() -> Dict[str, Any]:
    params = {"evaluation_model_filename": "iris_svc.pkl"}
    if os.path.exists(PARAMS_YAML):
        with open(PARAMS_YAML, "r") as f:
            _params = yaml.load(f, Loader=yaml.SafeLoader)
        for k, v in _params["evaluate"].items():
            if isinstance(v, int):
                params[k] = int(os.getenv(k.upper(), v))
            elif isinstance(v, float):
                params[k] = float(os.getenv(k.upper(), v))
            else:
                params[k] = str(os.getenv(k.upper(), v))

    return params


def evaluate_sklearn_model(filepath: str, x_test: np.ndarray, y_test: np.ndarray):
    model = joblib.load(filepath)
    p = model.predict(x_test)

    accuracy = metrics.accuracy_score(y_test, p)
    print(f"accuracy_score: {accuracy}")

    precision = metrics.precision_score(y_test, p, average="micro")
    print(f"precision_score: {precision}")

    recall = metrics.recall_score(y_test, p, average="micro")
    print(f"recall_score: {recall}")

    with open(EVALUATION_SCORE, "w") as f:
        json.dump({"accuracy": accuracy, "precision": precision, "recall": recall}, f)


def evaluate_onnx_model(filepath: str, x_test: np.ndarray, y_test: np.ndarray):
    sess = rt.InferenceSession(filepath)
    input_name = sess.get_inputs()[0].name
    output_name = sess.get_outputs()[0].name
    p = sess.run([output_name], {input_name: x_test.astype("float32")})

    accuracy = metrics.accuracy_score(y_test, p[0])
    print(f"accuracy_score: {accuracy}")

    precision = metrics.precision_score(y_test, p[0], average="micro")
    print(f"precision_score: {precision}")

    recall = metrics.recall_score(y_test, p[0], average="micro")
    print(f"recall_score: {recall}")

    with open(EVALUATION_SCORE, "w") as f:
        json.dump({"accuracy": accuracy, "precision": precision, "recall": recall}, f)


def main():
    os.makedirs(DOWNSTREAM_DIR, exist_ok=True)

    params = get_params()

    x_test = np.load(X_TEST_NPY)
    y_test = np.load(Y_TEST_NPY)

    model_filename = params["evaluation_model_filename"]

    if model_filename.endswith(".pkl"):
        evaluate_sklearn_model(os.path.join(MODEL_DIR, model_filename), x_test, y_test)
    if model_filename.endswith(".onnx"):
        evaluate_onnx_model(os.path.join(MODEL_DIR, model_filename), x_test, y_test)


if __name__ == "__main__":
    main()
