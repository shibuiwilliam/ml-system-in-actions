import tensorflow as tf
import tensorflow_hub as hub
from typing import Tuple


def get_model(hub_url: str, input_shape: Tuple[int], **kwargs) -> tf.python.keras.engine.sequential.Sequential:
    hub_keras_layer = hub.KerasLayer(hub_url, input_shape=input_shape, **kwargs)
    model = tf.keras.Sequential([hub_keras_layer])
    return model
