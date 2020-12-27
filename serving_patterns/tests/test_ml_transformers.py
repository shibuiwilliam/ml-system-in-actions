import pytest
from PIL import Image
import numpy as np

from src.app.ml import transformers


mock_image = Image.new("RGB", size=(300, 300), color=(10, 10, 10))


@pytest.mark.parametrize(("image", "image_size", "prediction_shape"), [(mock_image, (224, 224), (1, 3, 224, 224)), (mock_image, (124, 124), (1, 3, 124, 124))])
def test_onnx_image_preprocess_transformer(mocker, image, image_size, prediction_shape):
    onnx_image_preprocess_transformer = transformers.PytorchImagePreprocessTransformer(image_size, prediction_shape)
    result = onnx_image_preprocess_transformer.transform(image)
    assert result.shape == prediction_shape


@pytest.mark.parametrize(
    ("np_image", "image_size", "prediction_shape"),
    [(np.array(mock_image.resize((224, 224))), (224, 224), (1, 3, 224, 224)), (np.array(mock_image.resize((224, 224))), (224, 224), (1, 3, 224, 224))],
)
def test_onnx_image_preprocess_transformer_np(mocker, np_image, image_size, prediction_shape):
    onnx_image_preprocess_transformer = transformers.PytorchImagePreprocessTransformer(image_size, prediction_shape)
    result = onnx_image_preprocess_transformer.transform(np_image)
    assert result.shape == prediction_shape


@pytest.mark.parametrize(("image", "image_size", "prediction_shape"), [(mock_image, (224, 224), (1, 3, 224, 224)), (mock_image, (124, 124), (1, 3, 124, 124))])
def test_tf_image_preprocess_transformer(mocker, image, image_size, prediction_shape):
    tf_image_preprocess_transformer = transformers.TFImagePreprocessTransformer(image_size, prediction_shape)
    result = tf_image_preprocess_transformer.transform(image)
    assert result.shape == prediction_shape


@pytest.mark.parametrize(
    ("np_image", "image_size", "prediction_shape"),
    [(np.array(mock_image.resize((224, 224))), (224, 224), (1, 3, 224, 224)), (np.array(mock_image.resize((224, 224))), (224, 224), (1, 3, 224, 224))],
)
def test_tf_image_preprocess_transformer_np(mocker, np_image, image_size, prediction_shape):
    tf_image_preprocess_transformer = transformers.TFImagePreprocessTransformer(image_size, prediction_shape)
    result = tf_image_preprocess_transformer.transform(np_image)
    assert result.shape == prediction_shape


@pytest.mark.parametrize(("X"), [(np.array((0.1, 0.8, 0.6))), (np.array((-0.1, 0.8, -0.6))), ([0.1, 0.8, 0.6]), ([[0.2, -0.6, 0.7]])])
def test_softmax_transformer(mocker, X):
    softmax_transformer = transformers.SoftmaxTransformer()
    Y = softmax_transformer.transform(X)
    assert sum(Y[0]) == pytest.approx(1)
