from abc import ABCMeta, abstractmethod
from pydantic import BaseModel
from typing import List, Any, Sequence, Union
import numpy as np


class BaseData(BaseModel):
    input_data: Union[List[float], List[List[float]]] = None
    prediction: Union[List[float], List[List[float]], float] = None
    job_id: str = None


class BaseDataInterface(BaseModel):
    input_shape: Sequence[int] = None
    input_type: str = None
    output_shape: Sequence[int] = None
    output_type: str = None
    data_type: str = None


class BaseDataConverter(BaseModel):
    data_interface: BaseDataInterface = None

    @classmethod
    def convert_input_data_to_np(cls, input_data: Any) -> np.ndarray:
        np_data = np.array(input_data).astype(cls.data_interface.input_type).reshape(cls.data_interface.input_shape)
        return np_data

    @classmethod
    def reshape_output(cls, output: np.ndarray) -> np.ndarray:
        np_data = output.astype(cls.data_interface.output_type).reshape(cls.data_interface.output_shape)
        return np_data


class BasePredictor(metaclass=ABCMeta):
    @abstractmethod
    def load_model(self):
        raise NotImplementedError()

    @abstractmethod
    def predict(self, data) -> Any:
        raise NotImplementedError()

    @abstractmethod
    async def async_predict(self, data) -> Any:
        raise NotImplementedError()
