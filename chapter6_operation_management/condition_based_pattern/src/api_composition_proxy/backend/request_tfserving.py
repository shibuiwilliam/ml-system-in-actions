import base64
import json

import click
import grpc
import numpy as np
import requests
import tensorflow as tf
from tensorflow_serving.apis import predict_pb2, prediction_service_pb2_grpc


def request_grpc(
    stub: prediction_service_pb2_grpc.PredictionServiceStub,
    image: bytes,
    model_spec_name: str = "inception_v3",
    signature_name: str = "serving_default",
    timeout_second: int = 5,
) -> str:
    request = predict_pb2.PredictRequest()
    request.model_spec.name = model_spec_name
    request.model_spec.signature_name = signature_name
    base64_image = base64.urlsafe_b64encode(image)
    request.inputs["image"].CopyFrom(tf.make_tensor_proto([base64_image]))
    response = stub.Predict(request, timeout_second)

    prediction = response.outputs["output_0"].string_val[0].decode("utf-8")
    return prediction


def request_rest(
    image: bytes,
    model_spec_name: str = "inception_v3",
    address: str = "localhost",
    port: int = 8501,
):
    serving_address = f"http://{address}:{port}/v1/models/{model_spec_name}:predict"
    headers = {"Content-Type": "application/json"}
    base64_image = base64.urlsafe_b64encode(image).decode("ascii")
    request_dict = {"inputs": {"image": [base64_image]}}
    response = requests.post(
        serving_address,
        json.dumps(request_dict),
        headers=headers,
    )
    return dict(response.json())["outputs"][0]
