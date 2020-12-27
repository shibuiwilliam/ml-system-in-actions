from sklearn import svm, tree, metrics
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType
import onnxruntime as rt
import os
import numpy as np
from typing import Dict, List, Any
import sys

sys.path.append(os.path.abspath(".."))
import save_helper
from constants import PREDICTION_TYPE, MODEL_RUNTIME, DATA_TYPE


MODEL_DIR = "./models/"
DATA_DIR = "./data/"
LABEL_FILEPATH = os.path.join(DATA_DIR, "iris_label.csv")
DATA_FILEPATH = os.path.join(DATA_DIR, "iris_data.csv")


def split_dataset(data: List[List[Any]], target: List[Any]) -> Dict[str, np.ndarray]:
    x_train, x_test, y_train, y_test = train_test_split(data, target, shuffle=True, test_size=0.3)
    x_train = np.array(x_train).astype("float32")
    y_train = np.array(y_train).astype("float32")
    x_test = np.array(x_test).astype("float32")
    y_test = np.array(y_test).astype("float32")
    return {"x_train": x_train, "x_test": x_test, "y_train": y_train, "y_test": y_test}


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


def evaluate_model(model, x: np.ndarray, y: np.ndarray):
    p = model.predict(x)
    score = metrics.accuracy_score(y, p)
    print(score)


def train_and_save(model, modelname: str, filename: str, x_train: np.ndarray, y_train: np.ndarray, x_test: np.ndarray, y_test: np.ndarray):
    train_model(model, x_train, y_train)
    evaluate_model(model, x_test, y_test)
    save_helper.dump_sklearn(model, os.path.join(MODEL_DIR, filename))


def main():
    os.makedirs(MODEL_DIR, exist_ok=True)
    labels = save_helper.load_labels(LABEL_FILEPATH)
    _full_data = save_helper.load_data(DATA_FILEPATH)
    _data = [d[:4] for d in _full_data]
    _target = [d[4] for d in _full_data]
    data = split_dataset(_data, _target)

    svc_pipeline = define_svc_pipeline()
    svc_modelname = "iris_svc"
    svc_model_filename = f"{svc_modelname}.pkl"
    svc_sklearn_interface_filename = f"{svc_modelname}_sklearn.yaml"
    train_model(svc_pipeline, data["x_train"], data["y_train"])
    evaluate_model(svc_pipeline, data["x_test"], data["y_test"])
    save_helper.dump_sklearn(svc_pipeline, os.path.join(MODEL_DIR, svc_model_filename))
    save_helper.save_interface(
        svc_modelname,
        os.path.join(MODEL_DIR, svc_sklearn_interface_filename),
        [1, 4],
        str(data["x_train"].dtype).split(".")[-1],
        [1, 3],
        "float32",
        DATA_TYPE.ARRAY,
        [{svc_model_filename: MODEL_RUNTIME.SKLEARN}],
        PREDICTION_TYPE.CLASSIFICATION,
        "src.app.ml.iris.iris_predictor_sklearn",
        label_filepath=LABEL_FILEPATH,
    )

    svc_onnx_filename = f"{svc_modelname}.onnx"
    svc_onnx_interface_filename = f"{svc_modelname}_onnx_runtime.yaml"
    save_helper.save_onnx(svc_pipeline, os.path.join(MODEL_DIR, svc_onnx_filename))
    save_helper.save_interface(
        svc_modelname,
        os.path.join(MODEL_DIR, svc_onnx_interface_filename),
        [1, 4],
        str(data["x_train"].dtype).split(".")[-1],
        [1, 3],
        "float32",
        DATA_TYPE.ARRAY,
        [{svc_onnx_filename: MODEL_RUNTIME.ONNX_RUNTIME}],
        PREDICTION_TYPE.CLASSIFICATION,
        "src.app.ml.iris.iris_predictor_onnx",
        label_filepath=LABEL_FILEPATH,
    )

    tree_pipeline = define_tree_pipeline()
    tree_modelname = "iris_tree"
    tree_model_filename = f"{tree_modelname}.pkl"
    tree_sklearn_interface_filename = f"{tree_modelname}_sklearn.yaml"
    train_model(tree_pipeline, data["x_train"], data["y_train"])
    evaluate_model(tree_pipeline, data["x_test"], data["y_test"])
    save_helper.dump_sklearn(tree_pipeline, os.path.join(MODEL_DIR, tree_model_filename))
    save_helper.save_interface(
        tree_modelname,
        os.path.join(MODEL_DIR, tree_sklearn_interface_filename),
        [1, 4],
        str(data["x_train"].dtype).split(".")[-1],
        [1, 3],
        "float32",
        DATA_TYPE.ARRAY,
        [{tree_model_filename: MODEL_RUNTIME.SKLEARN}],
        PREDICTION_TYPE.CLASSIFICATION,
        "src.app.ml.iris.iris_predictor_sklearn",
        label_filepath=LABEL_FILEPATH,
    )

    tree_onnx_filename = f"{tree_modelname}.onnx"
    tree_onnx_interface_filename = f"{tree_modelname}_onnx_runtime.yaml"
    save_helper.save_onnx(tree_pipeline, os.path.join(MODEL_DIR, tree_onnx_filename))
    save_helper.save_interface(
        tree_modelname,
        os.path.join(MODEL_DIR, tree_onnx_interface_filename),
        [1, 4],
        str(data["x_train"].dtype).split(".")[-1],
        [1, 3],
        "float32",
        DATA_TYPE.ARRAY,
        [{tree_onnx_filename: MODEL_RUNTIME.ONNX_RUNTIME}],
        PREDICTION_TYPE.CLASSIFICATION,
        "src.app.ml.iris.iris_predictor_onnx",
        label_filepath=LABEL_FILEPATH,
    )


if __name__ == "__main__":
    main()
