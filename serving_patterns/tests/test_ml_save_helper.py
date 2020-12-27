import pytest
import os
import tempfile

from src.app.ml import save_helper
from src.app.constants import PREDICTION_TYPE, MODEL_RUNTIME, DATA_TYPE


_models = [{"a.pkl": MODEL_RUNTIME.SKLEARN}, {"b.onnx": MODEL_RUNTIME.ONNX_RUNTIME}, {"c.pkl": MODEL_RUNTIME.SKLEARN}]
_input_shape = [1, 224, 224, 3]
_output_shape = [1, 1000]


def test_dump_sklearn(mocker):
    mocker.patch("joblib.dump", return_value=None)
    save_helper.dump_sklearn("", "test.pkl")


@pytest.mark.parametrize(
    (
        "model_name",
        "interface_filepath",
        "input_shape",
        "input_type",
        "output_shape",
        "output_type",
        "data_type",
        "models",
        "prediction_type",
        "runner",
        "option",
    ),
    [
        (
            "test_sklearn",
            "test.yml",
            _input_shape,
            "float32",
            _output_shape,
            "float32",
            DATA_TYPE.IMAGE,
            _models,
            PREDICTION_TYPE.CLASSIFICATION,
            "src.app.ml.test",
            "option",
        )
    ],
)
def test_save_interface(
    mocker, model_name, interface_filepath, input_shape, input_type, output_shape, output_type, data_type, models, prediction_type, runner, option
):
    with tempfile.TemporaryDirectory() as model_dir:
        interface_filepath = os.path.join(model_dir, interface_filepath)
        save_helper.save_interface(
            model_name, interface_filepath, input_shape, input_type, output_shape, output_type, data_type, models, prediction_type, runner, option=option
        )
