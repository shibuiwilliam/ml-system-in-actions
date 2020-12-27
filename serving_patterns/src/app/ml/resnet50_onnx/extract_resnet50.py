import onnxruntime as rt
import os
from PIL import Image
import numpy as np
import torch
import torch.nn as nn
from torchvision.models.resnet import resnet50

from src.app.constants import PREDICTION_TYPE, MODEL_RUNTIME, DATA_TYPE
from src.app.ml.save_helper import save_interface, load_labels, dump_sklearn
from src.app.ml.transformers import PytorchImagePreprocessTransformer, SoftmaxTransformer


WORK_DIR = "./src/app/ml/resnet50_onnx/"

MODEL_DIR = os.path.join(WORK_DIR, "model")
MODEL_FILENAME = "resnet50v2.onnx"
MODEL_FILEPATH = os.path.join(MODEL_DIR, MODEL_FILENAME)

DATA_DIR = os.path.join(WORK_DIR, "data")
SAMPLE_IMAGE = os.path.join(DATA_DIR, "good_cat.jpg")
LABEL_FILEPATH = os.path.join(DATA_DIR, "imagenet_labels_1000.json")


def main():
    modelname = "resnet50_onnx"
    interface_filename = f"{modelname}.yaml"

    model = resnet50(pretrained=True)
    x_dummy = torch.rand((1, 3, 224, 224), device="cpu")
    model.eval()
    torch.onnx.export(
        model,
        x_dummy,
        MODEL_FILEPATH,
        export_params=True,
        opset_version=10,
        do_constant_folding=True,
        input_names=["input"],
        output_names=["output"],
        verbose=False,
    )

    labels = load_labels(LABEL_FILEPATH)

    preprocess = PytorchImagePreprocessTransformer()

    image = Image.open(SAMPLE_IMAGE)
    np_image = preprocess.transform(image)
    print(np_image.shape)

    preprocess_name = f"{modelname}_preprocess_transformer"
    preprocess_filename = f"{preprocess_name}.pkl"
    preprocess_filepath = os.path.join(MODEL_DIR, preprocess_filename)
    dump_sklearn(preprocess, preprocess_filepath)

    sess = rt.InferenceSession(MODEL_FILEPATH)
    inp, out = sess.get_inputs()[0], sess.get_outputs()[0]
    print(f"input name='{inp.name}' shape={inp.shape} type={inp.type}")
    print(f"output name='{out.name}' shape={out.shape} type={out.type}")
    pred_onx = sess.run([out.name], {inp.name: np_image})

    postprocess = SoftmaxTransformer()
    postprocess_name = f"{modelname}_softmax_transformer"
    postprocess_filename = f"{postprocess_name}.pkl"
    postprocess_filepath = os.path.join(MODEL_DIR, postprocess_filename)
    dump_sklearn(postprocess, postprocess_filepath)
    prediction = postprocess.transform(np.array(pred_onx))

    print(prediction.shape)
    print(labels[np.argmax(prediction[0])])

    save_interface(
        modelname,
        os.path.join(MODEL_DIR, interface_filename),
        [1, 3, 224, 224],
        "float32",
        [1, 1000],
        "float32",
        DATA_TYPE.IMAGE,
        [{preprocess_filepath: MODEL_RUNTIME.SKLEARN}, {MODEL_FILEPATH: MODEL_RUNTIME.ONNX_RUNTIME}, {postprocess_filepath: MODEL_RUNTIME.SKLEARN}],
        PREDICTION_TYPE.CLASSIFICATION,
        "src.app.ml.resnet50_onnx.resnet50_predictor",
        label_filepath=LABEL_FILEPATH,
    )


if __name__ == "__main__":
    main()
