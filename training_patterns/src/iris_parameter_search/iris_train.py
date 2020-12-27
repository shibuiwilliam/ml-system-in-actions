from sklearn import svm, tree
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from typing import Dict, Any
import os
import shutil
import yaml
import numpy as np
import sys

sys.path.append(os.path.abspath(".."))
from constants import PREDICTION_TYPE, MODEL_RUNTIME, DATA_TYPE
import save_helper


PARAMS_YAML = "./train_params.yaml"
MODEL_DIR = "./models/"
DATA_DIR = "./data/"
LABEL_FILENAME = "iris_label.csv"
UPSTREAM_DIR = os.path.join(DATA_DIR, "prepared")
LABEL_FILEPATH = os.path.join(DATA_DIR, LABEL_FILENAME)
X_TRAIN_NPY = os.path.join(UPSTREAM_DIR, "x_train.npy")
Y_TRAIN_NPY = os.path.join(UPSTREAM_DIR, "y_train.npy")
DOWNSTREAM_DIR = os.path.join(DATA_DIR, "trained")


def get_params() -> Dict[str, Any]:
    params = {"save_model_name": "iris_svc", "save_format": "sklearn", "ml_model": "svc"}
    if os.path.exists(PARAMS_YAML):
        with open(PARAMS_YAML, "r") as f:
            _params = yaml.load(f, Loader=yaml.SafeLoader)
        for k, v in _params["train"].items():
            if isinstance(v, int):
                params[k] = int(os.getenv(k.upper(), v))
            elif isinstance(v, float):
                params[k] = float(os.getenv(k.upper(), v))
            else:
                params[k] = str(os.getenv(k.upper(), v))

    return params


def define_svc_pipeline() -> Pipeline:
    steps = [("normalize", StandardScaler()), ("svc", svm.SVC(probability=True))]
    pipeline = Pipeline(steps=steps)
    return pipeline


def define_tree_pipeline() -> Pipeline:
    steps = [("normalize", StandardScaler()), ("tree", tree.DecisionTreeClassifier())]
    pipeline = Pipeline(steps=steps)
    return pipeline


def train_model(model, x: np.ndarray, y: np.ndarray):
    model.fit(x, y)


def main():
    os.makedirs(DOWNSTREAM_DIR, exist_ok=True)
    os.makedirs(MODEL_DIR, exist_ok=True)

    params = get_params()

    x_train = np.load(X_TRAIN_NPY)
    y_train = np.load(Y_TRAIN_NPY)

    if params["ml_model"] == "svc":
        pipeline = define_svc_pipeline()
    elif params["ml_model"] == "tree":
        pipeline = define_tree_pipeline()
    else:
        pass

    train_model(pipeline, x_train, y_train)

    modelname = params["save_model_name"]

    if params["save_format"] == "sklearn":
        model_filename = f"{modelname}.pkl"
        sklearn_interface_filename = f"{modelname}_sklearn.yaml"
        save_helper.dump_sklearn(pipeline, os.path.join(MODEL_DIR, model_filename))
        save_helper.save_interface(
            modelname,
            os.path.join(MODEL_DIR, sklearn_interface_filename),
            [1, 4],
            str(x_train.dtype).split(".")[-1],
            [1, 3],
            "float32",
            DATA_TYPE.ARRAY,
            [{model_filename: MODEL_RUNTIME.SKLEARN}],
            PREDICTION_TYPE.CLASSIFICATION,
            "src.app.ml.iris.iris_predictor_sklearn",
            label_filepath=os.path.join(MODEL_DIR, LABEL_FILENAME),
        )
    elif params["save_format"] == "onnx":
        onnx_filename = f"{modelname}.onnx"
        onnx_interface_filename = f"{modelname}_onnx_runtime.yaml"
        save_helper.save_onnx(pipeline, os.path.join(MODEL_DIR, onnx_filename))
        save_helper.save_interface(
            modelname,
            os.path.join(MODEL_DIR, onnx_interface_filename),
            [1, 4],
            str(x_train.dtype).split(".")[-1],
            [1, 3],
            "float32",
            DATA_TYPE.ARRAY,
            [{onnx_filename: MODEL_RUNTIME.ONNX_RUNTIME}],
            PREDICTION_TYPE.CLASSIFICATION,
            "src.app.ml.iris.iris_predictor_onnx",
            label_filepath=os.path.join(MODEL_DIR, LABEL_FILENAME),
        )
    else:
        pass

    shutil.copy2(LABEL_FILEPATH, os.path.join(MODEL_DIR, LABEL_FILENAME))


if __name__ == "__main__":
    main()
