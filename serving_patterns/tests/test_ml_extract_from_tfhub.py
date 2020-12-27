import pytest
import numpy
import tensorflow
import tensorflow_hub

from src.app.ml import extract_from_tfhub


@pytest.mark.parametrize(("hub_url", "input_shape", "kwargs"), [("https://tfhub.dev/google/imagenet/inception_v3/classification/4", (299, 299, 3), {})])
def test_get_model(mocker, hub_url, input_shape, kwargs):
    mock_keras_layer = mocker.Mock(tensorflow_hub.keras_layer.KerasLayer)
    mock_sequential = mocker.Mock(tensorflow.python.keras.engine.sequential.Sequential)
    mocker.patch("tensorflow_hub.KerasLayer", return_value=mock_keras_layer)
    mocker.patch("tensorflow.keras.Sequential", return_value=mock_sequential)
    model = extract_from_tfhub.get_model(hub_url, input_shape, **kwargs)
    assert model == mock_sequential
