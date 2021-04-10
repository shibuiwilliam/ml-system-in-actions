import base64
import json

import click
import grpc
import numpy as np
import requests
import tensorflow as tf
from tensorflow_serving.apis import predict_pb2, prediction_service_pb2_grpc


def read_image(image_file: str = "./cat.jpg") -> bytes:
    with open(image_file, "rb") as f:
        raw_image = f.read()
    return raw_image


def request_grpc(
    image: bytes,
    model_spec_name: str = "inception_v3",
    signature_name: str = "serving_default",
    address: str = "localhost",
    port: int = 8500,
    timeout_second: int = 5,
) -> str:
    serving_address = f"{address}:{port}"
    channel = grpc.insecure_channel(serving_address)
    stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)
    base64_image = base64.urlsafe_b64encode(image)

    request = predict_pb2.PredictRequest()
    request.model_spec.name = model_spec_name
    request.model_spec.signature_name = signature_name
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


def request_metadata(
    model_spec_name: str = "inception_v3",
    address: str = "localhost",
    port: int = 8501,
):
    serving_address = f"http://{address}:{port}/v1/models/{model_spec_name}/versions/0/metadata"
    response = requests.get(serving_address)
    return response.json()


@click.command(name="inception v3 image classification")
@click.option(
    "--format",
    "-f",
    default="GRPC",
    type=str,
    help="GRPC or REST request",
)
@click.option(
    "--image_file",
    "-i",
    default="./cat.jpg",
    type=str,
    help="input image file path",
)
@click.option(
    "--target",
    "-t",
    default="localhost",
    type=str,
    help="target address",
)
@click.option(
    "--timeout_second",
    "-s",
    default=5,
    type=int,
    help="timeout in second",
)
@click.option(
    "--model_spec_name",
    "-m",
    default="inception_v3",
    type=str,
    help="model spec name",
)
@click.option(
    "--signature_name",
    "-n",
    default="serving_default",
    type=str,
    help="model signature name",
)
@click.option(
    "--metadata",
    is_flag=True,
)
def main(
    format: str,
    image_file: str,
    target: str,
    timeout_second: int,
    model_spec_name: str,
    signature_name: str,
    metadata: bool,
):

    if metadata:
        result = request_metadata(
            model_spec_name=model_spec_name,
            address=target,
            port=8501,
        )
        print(result)

    else:
        raw_image = read_image(image_file=image_file)

        if format.upper() == "GRPC":
            prediction = request_grpc(
                image=raw_image,
                model_spec_name=model_spec_name,
                signature_name=signature_name,
                address=target,
                port=8500,
                timeout_second=timeout_second,
            )
        elif format.upper() == "REST":
            prediction = request_rest(
                image=raw_image,
                model_spec_name=model_spec_name,
                address=target,
                port=8501,
            )
        else:
            raise ValueError("Undefined format; should be GRPC or REST")
        print(prediction)


if __name__ == "__main__":
    main()
