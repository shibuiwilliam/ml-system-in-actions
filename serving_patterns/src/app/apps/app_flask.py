from flask import Flask, jsonify, request
import numpy as np
from PIL import Image
from typing import List
import logging
import io
import base64

from src.app.ml.active_predictor import Data, DataConverter, active_predictor
from src.helper import get_job_id, get_image_data
from src.middleware.profiler import do_cprofile
from src.configurations import PlatformConfigurations
from src.app.configurations import APIConfigurations


logger = logging.getLogger(__name__)
logger.info(f"starts {APIConfigurations.title}:{APIConfigurations.version}")
logger.info(f"platform: {PlatformConfigurations.platform}")


app = Flask(
    import_name=APIConfigurations.title,
)


@do_cprofile
def predict_image(image_data: Image.Image) -> List:
    output_np = active_predictor.predict(image_data)
    reshaped_output_nps = DataConverter.reshape_output(output_np)
    prediction = reshaped_output_nps.tolist()
    return prediction


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"health": "ok"})


@app.route("/predict", methods=["GET", "POST"])
def predict():
    _data = Data()
    if request.method == "GET":
        data = _data.test_data
        image_data = get_image_data(data)
        prediction = predict_image(image_data)
        return jsonify({"prediction": prediction})

    elif request.method == "POST":
        input_data = request.get_json()
        raw_data = input_data["image_data"]
        decoded = base64.b64decode(str(raw_data))
        io_bytes = io.BytesIO(decoded)
        data = Image.open(io_bytes)
        image_data = get_image_data(data)
        prediction = predict_image(image_data)
        job_id = data["job_id"] if "job_id" in input_data.keys() else get_job_id()
        return jsonify({"prediction": prediction, "job_id": job_id})


@app.route("/labels", methods=["GET"])
def labels():
    _data = Data()
    labels = _data.labels
    return jsonify({"labels": labels})


@app.route("/predict/label", methods=["GET", "POST"])
def predict_label():
    _data = Data()
    labels = _data.labels
    if request.method == "GET":
        data = _data.test_data
        image_data = get_image_data(data)
        prediction = predict_image(image_data)
        argmax = int(np.argmax(np.array(prediction)[0]))
        return jsonify({labels[argmax]: prediction[0][argmax]})

    elif request.method == "POST":
        input_data = request.get_json()
        raw_data = input_data["image_data"]
        decoded = base64.b64decode(str(raw_data))
        io_bytes = io.BytesIO(decoded)
        data = Image.open(io_bytes)
        image_data = get_image_data(data)
        prediction = predict_image(image_data)
        argmax = int(np.argmax(np.array(prediction)[0]))
        job_id = data["job_id"] if "job_id" in input_data.keys() else get_job_id()
        return jsonify({labels[argmax]: prediction[0][argmax], "job_id": job_id})


if __name__ == "__main__":
    app.run(debug=True)
