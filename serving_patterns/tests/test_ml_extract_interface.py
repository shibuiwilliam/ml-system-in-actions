import pytest
from src.app.ml import extract_interface
from typing import Tuple, List


filepath = "./models/iris_svc_sklearn.yaml"


@pytest.mark.parametrize(("filepath"), [(filepath)])
def test_extract_interface_yaml(filepath):
    interface = extract_interface.extract_interface_yaml(filepath)
    model_name = list(interface.keys())[0]
    assert isinstance(interface[model_name]["data_interface"]["input_shape"], Tuple)
    assert isinstance(interface[model_name]["data_interface"]["input_type"], str)
    assert isinstance(interface[model_name]["data_interface"]["output_shape"], Tuple)
    assert isinstance(interface[model_name]["data_interface"]["output_type"], str)
    assert isinstance(interface[model_name]["meta"]["prediction_type"], str)
    assert isinstance(interface[model_name]["meta"]["models"], List)
    assert isinstance(interface[model_name]["meta"]["runner"], str)
