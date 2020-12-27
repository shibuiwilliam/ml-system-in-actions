import os
import tensorflow as tf
import tensorflow_hub as hub
from PIL import Image
import numpy as np

from src.app.constants import PREDICTION_TYPE, MODEL_RUNTIME, DATA_TYPE
from src.app.ml.save_helper import save_interface, load_labels, dump_sklearn
from src.app.ml.transformers import TFImagePreprocessTransformer, SoftmaxTransformer
from src.app.ml.extract_from_tfhub import get_model

WORK_DIR = "./src/app/ml/inceptionv3/"

MODEL_DIR = os.path.join(WORK_DIR, "model")
SAVEDMODEL_DIR = os.path.join(MODEL_DIR, "savedmodel/inceptionv3/4")
PB_FILE = os.path.join(SAVEDMODEL_DIR, "saved_model.pb")

HUB_URL = "https://tfhub.dev/google/imagenet/inception_v3/classification/4"

DATA_DIR = os.path.join(WORK_DIR, "data")
SAMPLE_IMAGE = os.path.join(DATA_DIR, "good_cat.jpg")
LABEL_FILEPATH = os.path.join(DATA_DIR, "imagenet_labels_1001.json")
LABELS = load_labels(LABEL_FILEPATH)


def validate(image, preprocess, predictor, postprocess):
    np_image = preprocess.transform(image)
    result = predictor.predict(np_image)
    result_proba = postprocess.transform(result)
    print(result_proba)
    top1_index = np.argmax(result_proba[0], axis=-1)
    print(top1_index)
    print(LABELS[top1_index])


def main():
    os.makedirs(SAVEDMODEL_DIR, exist_ok=True)

    if os.path.exists(PB_FILE):
        print(f"saved model {SAVEDMODEL_DIR} found")
        model = tf.keras.models.load_model(SAVEDMODEL_DIR)
    else:
        print(f"saved model {SAVEDMODEL_DIR} not found")
        model = get_model(HUB_URL, (299, 299, 3))

    preprocess = TFImagePreprocessTransformer()
    postprocess = SoftmaxTransformer()

    image = Image.open(SAMPLE_IMAGE)

    validate(image, preprocess, model, postprocess)

    tf.saved_model.save(model, SAVEDMODEL_DIR)

    modelname = "inceptionv3"
    interface_filename = f"{modelname}.yaml"
    preprocess_filename = f"{modelname}_preprocess_transformer.pkl"
    postprocess_filename = f"{modelname}_softmax_transformer.pkl"
    preprocess_filepath = os.path.join(MODEL_DIR, preprocess_filename)
    postprocess_filepath = os.path.join(MODEL_DIR, postprocess_filename)
    dump_sklearn(preprocess, preprocess_filepath)
    dump_sklearn(postprocess, postprocess_filepath)

    save_interface(
        modelname,
        os.path.join(MODEL_DIR, interface_filename),
        [1, 299, 299, 3],
        "float32",
        [1, 1001],
        "float32",
        DATA_TYPE.IMAGE,
        [{preprocess_filepath: MODEL_RUNTIME.SKLEARN}, {SAVEDMODEL_DIR: MODEL_RUNTIME.TF_SERVING}, {postprocess_filepath: MODEL_RUNTIME.SKLEARN}],
        PREDICTION_TYPE.CLASSIFICATION,
        "src.app.ml.inceptionv3.inceptionv3_predictor",
        label_filepath=LABEL_FILEPATH,
        model_spec_name="inceptionv3",
        model_spec_signature_name="serving_default",
        input_name="input_1",
        output_name="keras_layer",
    )


if __name__ == "__main__":
    main()
