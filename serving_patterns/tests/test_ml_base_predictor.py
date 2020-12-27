import pytest
from typing import List
import numpy as np

from src.app.ml.base_predictor import BaseData, BaseDataInterface, BaseDataConverter


f_data = [[0.1, 0.9, 1.1, 1.1]]
i_data = [[1, 2, 3, 4]]
f_proba = [0.1, 0.2, 0.3]


@pytest.mark.parametrize(("input_data", "prediction"), [(f_data, [f_proba])])
def test_BaseData(mocker, input_data, prediction):
    class MockData(BaseData):
        test_data: List[List[int]] = [[5.1, 3.5, 1.4, 0.2]]

    mock_data = MockData()
    mock_data.input_data = input_data
    mock_data.prediction = prediction


@pytest.mark.parametrize(("data_dict"), [({"input_data": f_data, "prediction": [f_proba]}), ({"input_data": f_data[0], "prediction": [f_proba]})])
def test_BaseDataDict(mocker, data_dict):
    class MockData(BaseData):
        test_data: List[List[int]] = [[5.1, 3.5, 1.4, 0.2]]

    mock_data = MockData(**data_dict)
    assert mock_data.input_data == data_dict["input_data"]
    assert mock_data.prediction == data_dict["prediction"]


@pytest.mark.parametrize(("input_shape", "input_type", "output_shape", "output_type"), [((1, 4), "float32", (1, 3), "float32")])
def test_BaseDataInterface(mocker, input_shape, input_type, output_shape, output_type):
    class MockDataInterface(BaseDataInterface):
        pass

    MockDataInterface.input_shape = input_shape
    MockDataInterface.input_type = input_type
    MockDataInterface.output_shape = output_shape
    MockDataInterface.output_type = output_type


@pytest.mark.parametrize(
    ("data_interface_data_dict"),
    [
        ({"input_shape": (1, 4), "input_type": "float32", "output_shape": (1, 3), "output_type": "float32"}),
        ({"input_shape": (1, 4), "input_type": "float32", "output_shape": (1, 3), "output_type": "float32"}),
    ],
)
def test_BaseDataDict(mocker, data_interface_data_dict):
    class MockDataInterface(BaseDataInterface):
        pass

    MockDataInterface.input_type = data_interface_data_dict["input_type"]
    MockDataInterface.input_shape = data_interface_data_dict["input_shape"]
    MockDataInterface.output_shape = data_interface_data_dict["output_shape"]
    MockDataInterface.output_type = data_interface_data_dict["output_type"]
    assert MockDataInterface.input_type == data_interface_data_dict["input_type"]
    assert MockDataInterface.input_shape == data_interface_data_dict["input_shape"]
    assert MockDataInterface.output_shape == data_interface_data_dict["output_shape"]
    assert MockDataInterface.output_type == data_interface_data_dict["output_type"]


@pytest.mark.parametrize(
    ("input_data", "input_shape", "input_type", "expected_input_datatype", "prediction", "output_shape", "output_type", "expected_output_datatype"),
    [
        (f_data, (1, 4), "float", np.float, [f_proba], (1, 3), "float32", np.float32),
        (f_data, (1, 4), "float64", np.float64, [f_proba], (1, 3), "float32", np.float32),
        (f_data[0], (1, 4), "float32", np.float32, [f_proba], (1, 3), "float32", np.float32),
        (i_data, (1, 4), "int8", np.int8, [f_proba], (1, 3), "float32", np.float32),
        (i_data[0], (1, 4), "int16", np.int16, [f_proba], (1, 3), "float32", np.float32),
    ],
)
def test_BaseDataConverter(
    mocker, input_data, input_shape, input_type, expected_input_datatype, prediction, output_shape, output_type, expected_output_datatype
):
    class MockData(BaseData):
        testf_data: List[List[int]] = [[5.1, 3.5, 1.4, 0.2]]

    class MockDataInterface(BaseDataInterface):
        pass

    mock_data = MockData()
    mock_data.input_data = input_data
    mock_data.prediction = prediction

    MockDataInterface.input_shape = input_shape
    MockDataInterface.input_type = input_type
    MockDataInterface.output_shape = output_shape
    MockDataInterface.output_type = output_type

    BaseDataConverter.data_interface = MockDataInterface
    np_data = BaseDataConverter.convert_input_data_to_np(mock_data.input_data)
    output = BaseDataConverter.reshape_output(np.array([mock_data.prediction]))
    assert np_data.shape == BaseDataConverter.data_interface.input_shape
    assert np_data.dtype == expected_input_datatype
    assert output.shape == BaseDataConverter.data_interface.output_shape
    assert output.dtype == expected_output_datatype
    # print()
    # print(MockDataInterface.__dict__)
    # print(BaseDataConverter.data_interface.__dict__)
    # print(MockDataInterface.input_shape)
    # print(MockDataInterface.output_shape)
    # print(np_data.shape)
    # print(output.shape)
    # print(np_data.dtype)
    # print(output.dtype)


@pytest.mark.parametrize(
    ("input_data", "input_shape", "input_type", "expected_input_datatype", "prediction", "output_shape", "output_type", "expected_output_datatype"),
    [
        (f_data, (1, 4), "float", np.float, [f_proba], (1, 3), "float32", np.float32),
        (f_data, (1, 4), "float64", np.float64, [f_proba], (1, 3), "float32", np.float32),
        (f_data[0], (1, 4), "float32", np.float32, [f_proba], (1, 3), "float32", np.float32),
        (i_data, (1, 4), "int8", np.int8, [f_proba], (1, 3), "float32", np.float32),
        (i_data[0], (1, 4), "int16", np.int16, [f_proba], (1, 3), "float32", np.float32),
    ],
)
def test_BaseDataConverter2(
    mocker, input_data, input_shape, input_type, expected_input_datatype, prediction, output_shape, output_type, expected_output_datatype
):
    class MockData(BaseData):
        testf_data: List[List[int]] = [[5.1, 3.5, 1.4, 0.2]]

    class MockDataInterface(BaseDataInterface):
        pass

    class MockDataConverter(BaseDataConverter):
        pass

    mock_data = MockData()
    mock_data.input_data = input_data
    mock_data.prediction = prediction

    MockDataInterface.input_shape = input_shape
    MockDataInterface.input_type = input_type
    MockDataInterface.output_shape = output_shape
    MockDataInterface.output_type = output_type

    MockDataConverter.data_interface = MockDataInterface
    np_data = MockDataConverter.convert_input_data_to_np(mock_data.input_data)
    output = MockDataConverter.reshape_output(np.array([mock_data.prediction]))
    assert np_data.shape == MockDataConverter.data_interface.input_shape
    assert np_data.dtype == expected_input_datatype
    assert output.shape == MockDataConverter.data_interface.output_shape
    assert output.dtype == expected_output_datatype
    # print()
    # print(MockDataInterface.__dict__)
    # print(MockDataConverter.data_interface.__dict__)
    # print(MockDataInterface.input_shape)
    # print(MockDataInterface.output_shape)
    # print(MockDataConverter.data_interface.input_shape)
    # print(MockDataConverter.data_interface.output_shape)
    # print(np_data.shape)
    # print(output.shape)
    # print(np_data.dtype)
    # print(output.dtype)
