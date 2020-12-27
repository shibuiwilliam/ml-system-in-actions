from skl2onnx.common.data_types import FloatTensorType
from skl2onnx import convert_sklearn
from typing import Dict, List, Any
import yaml
import json
import csv
import joblib

import constants


def load_labels(label_filepath: str) -> Dict[Any, Any]:
    if label_filepath.endswith(".json"):
        return _load_labels_json(label_filepath)
    elif label_filepath.endswith(".csv"):
        return _load_labels_csv(label_filepath)


def _load_labels_json(label_filepath: str) -> Dict[Any, Any]:
    with open(label_filepath, "r") as f:
        return json.load(f)


def _load_labels_csv(label_filepath: str) -> Dict[Any, Any]:
    labels = {}
    with open(label_filepath, "r") as f:
        r = list(csv.reader(f))
        for i in range(len(r)):
            if i == 0:
                continue
            labels[int(r[i][0])] = r[i][1]
    return labels


def load_data(data_filepath: str) -> Any:
    if data_filepath.endswith(".csv"):
        return _load_data_csv(data_filepath)


def _load_data_csv(data_filepath: str, column_first: bool = True) -> List[List[Any]]:
    data = []
    with open(data_filepath, "r") as f:
        r = list(csv.reader(f))
        for i in range(len(r)):
            if column_first and i == 0:
                continue
            data.append(r[i])
    return data


def dump_sklearn(model, name: str):
    joblib.dump(model, name)


def save_onnx(model, filepath: str):
    initial_type = [("float_input", FloatTensorType([None, 4]))]
    onx = convert_sklearn(model, initial_types=initial_type)
    with open(filepath, "wb") as f:
        f.write(onx.SerializeToString())


def save_interface(
    model_name: str,
    interface_filepath: str,
    input_shape: List[int],
    input_type: str,
    output_shape: List[int],
    output_type: str,
    data_type: constants.DATA_TYPE,
    models: List[Dict[str, constants.MODEL_RUNTIME]],
    prediction_type: constants.PREDICTION_TYPE,
    runner: str,
    **kwargs: Dict,
) -> None:
    if not (interface_filepath.endswith("yaml") or interface_filepath.endswith("yml")):
        interface_filepath = f"{interface_filepath}.yaml"
    _models = [{k: v.value for k, v in m.items()} for m in models]
    with open(interface_filepath, "w") as f:
        f.write(
            yaml.dump(
                {
                    model_name: {
                        "data_interface": {
                            "input_shape": input_shape,
                            "input_type": input_type,
                            "output_shape": output_shape,
                            "output_type": output_type,
                            "data_type": data_type.value,
                        },
                        "meta": {
                            "models": _models,
                            "prediction_type": prediction_type.value,
                            "runner": runner,
                        },
                        "options": kwargs,
                    }
                },
                default_flow_style=False,
            )
        )
