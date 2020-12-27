from sklearn.model_selection import train_test_split
from typing import Dict, List, Any
import os
import yaml
import numpy as np
import sys

sys.path.append(os.path.abspath(".."))
import save_helper


PARAMS_YAML = "./prepare_params.yaml"
DATA_DIR = "./data/"
DATA_FILENAME = "iris_data.csv"
DATA_FILEPATH = os.path.join(DATA_DIR, DATA_FILENAME)
DOWNSTREAM_DIR = os.path.join(DATA_DIR, "prepared")


def get_params() -> Dict[str, Any]:
    params = {"test_rate": 0.3}
    if os.path.exists(PARAMS_YAML):
        with open(PARAMS_YAML, "r") as f:
            _params = yaml.load(f, Loader=yaml.SafeLoader)
        for k, v in _params["prepare"].items():
            if isinstance(v, int):
                params[k] = int(os.getenv(k.upper(), v))
            elif isinstance(v, float):
                params[k] = float(os.getenv(k.upper(), v))
            else:
                params[k] = str(os.getenv(k.upper(), v))

    return params


def split_dataset(data: List[List[Any]], target: List[Any], test_size=0.3) -> Dict[str, np.ndarray]:
    x_train, x_test, y_train, y_test = train_test_split(data, target, shuffle=True, test_size=test_size, stratify=target)
    x_train = np.array(x_train).astype("float32")
    y_train = np.array(y_train).astype("float32")
    x_test = np.array(x_test).astype("float32")
    y_test = np.array(y_test).astype("float32")
    return {"x_train": x_train, "x_test": x_test, "y_train": y_train, "y_test": y_test}


def main():
    os.makedirs(DOWNSTREAM_DIR, exist_ok=True)
    params = get_params()

    _full_data = save_helper.load_data(DATA_FILEPATH)
    _data = [d[:4] for d in _full_data]
    _target = [d[4] for d in _full_data]
    data = split_dataset(_data, _target, params["test_rate"])

    for k, v in data.items():
        np.save(os.path.join(DOWNSTREAM_DIR, f"{k}.npy"), v)


if __name__ == "__main__":
    main()
