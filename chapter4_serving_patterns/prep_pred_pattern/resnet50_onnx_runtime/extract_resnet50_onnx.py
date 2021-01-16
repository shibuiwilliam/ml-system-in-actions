import json
import os
from typing import List

import click
import joblib
import numpy as np
import onnxruntime as rt
import torch
from PIL import Image
from src.ml.transformers import PytorchImagePreprocessTransformer, SoftmaxTransformer
from torchvision.models.resnet import resnet50


def dump_sklearn(model, name: str):
    joblib.dump(model, name)


def get_label(json_path: str = "./data/image_net_labels.json") -> List[str]:
    with open(json_path, "r") as f:
        labels = json.load(f)
    return labels


@click.command(name="extract resnet50 onnx runtime and preprocessing")
@click.option("--pred", is_flag=True)
@click.option("--prep", is_flag=True)
def main(pred: bool, prep: bool):
    model_directory = "./models/"
    os.makedirs(model_directory, exist_ok=True)

    onnx_filename = "resnet50.onnx"
    onnx_filepath = os.path.join(model_directory, onnx_filename)

    preprocess_filename = f"preprocess_transformer.pkl"
    preprocess_filepath = os.path.join(model_directory, preprocess_filename)

    postprocess_filename = f"softmax_transformer.pkl"
    postprocess_filepath = os.path.join(model_directory, postprocess_filename)

    if pred:
        model = resnet50(pretrained=True)
        x_dummy = torch.rand((1, 3, 224, 224), device="cpu")
        model.eval()
        torch.onnx.export(
            model,
            x_dummy,
            onnx_filepath,
            export_params=True,
            opset_version=10,
            do_constant_folding=True,
            input_names=["input"],
            output_names=["output"],
            verbose=False,
        )

    if prep:
        preprocess = PytorchImagePreprocessTransformer()
        dump_sklearn(preprocess, preprocess_filepath)

        postprocess = SoftmaxTransformer()
        dump_sklearn(postprocess, postprocess_filepath)

    if prep and pred:
        image = Image.open("./data/cat.jpg")
        np_image = preprocess.transform(image)
        print(np_image.shape)

        sess = rt.InferenceSession(onnx_filepath)
        inp, out = sess.get_inputs()[0], sess.get_outputs()[0]
        print(f"input name='{inp.name}' shape={inp.shape} type={inp.type}")
        print(f"output name='{out.name}' shape={out.shape} type={out.type}")
        pred_onx = sess.run([out.name], {inp.name: np_image})

        prediction = postprocess.transform(np.array(pred_onx))

        labels = get_label(json_path="./data/image_net_labels.json")
        print(prediction.shape)
        print(labels[np.argmax(prediction[0])])


if __name__ == "__main__":
    main()
