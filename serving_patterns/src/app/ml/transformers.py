from PIL import Image
import numpy as np
from typing import Tuple, List, Union
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin


class PytorchImagePreprocessTransformer(BaseEstimator, TransformerMixin):
    def __init__(
        self,
        image_size: Tuple[int] = (224, 224),
        prediction_shape: Tuple[int] = (1, 3, 224, 224),
        mean_vec: List[float] = [0.485, 0.456, 0.406],
        stddev_vec: List[float] = [0.229, 0.224, 0.225],
    ):
        self.image_size = image_size
        self.prediction_shape = prediction_shape
        self.mean_vec = mean_vec
        self.stddev_vec = stddev_vec

    def fit(self, X, y=None):
        return self

    def transform(self, X: Union[Image.Image, np.ndarray]) -> np.ndarray:
        if isinstance(X, np.ndarray):
            dim_0 = (3,) + self.image_size
            dim_1 = self.image_size + (3,)
            if X.shape != dim_0 and X.shape != dim_1:
                raise ValueError(f"resize to image_size {self.image_size} beforehand for numpy array")
        else:
            X = np.array(X.resize(self.image_size))

        image_data = X.transpose(2, 0, 1).astype("float32")
        mean_vec = np.array(self.mean_vec)
        stddev_vec = np.array(self.stddev_vec)
        norm_image_data = np.zeros(image_data.shape).astype("float32")
        for i in range(image_data.shape[0]):
            norm_image_data[i, :, :] = (image_data[i, :, :] / 255 - mean_vec[i]) / stddev_vec[i]
        norm_image_data = norm_image_data.reshape(self.prediction_shape).astype("float32")
        return norm_image_data


class TFImagePreprocessTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, image_size: Tuple[int] = (299, 299), prediction_shape: Tuple[int] = (1, 299, 299, 3)):
        self.image_size = image_size
        self.prediction_shape = prediction_shape

    def fit(self, X, y=None):
        return self

    def transform(self, X: Union[Image.Image, np.ndarray]) -> np.ndarray:
        if isinstance(X, np.ndarray):
            dim_0 = (3,) + self.image_size
            dim_1 = self.image_size + (3,)
            if X.shape != dim_0 and X.shape != dim_1:
                raise ValueError(f"resize to image_size {self.image_size} beforehand for numpy array")
        else:
            X = np.array(X.resize(self.image_size))

        image_data = X.astype("float32")
        norm_image_data = image_data.reshape(self.prediction_shape) / 255.0
        return norm_image_data


class SoftmaxTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X: Union[np.ndarray, List[float], List[List[float]]]) -> np.ndarray:
        if isinstance(X, List):
            X = np.array(X)
        x = X.reshape(-1)
        e_x = np.exp(x - np.max(x))
        result = np.array([e_x / e_x.sum(axis=0)])
        return result
