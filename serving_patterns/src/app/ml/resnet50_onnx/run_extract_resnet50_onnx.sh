#!/bin/bash

set -eu


work_dir=./src/app/ml/resnet50_onnx
model_dir=${work_dir}/model
data_dir=${work_dir}/data
label_file=${data_dir}/imagenet_labels_1000.json

mkdir -p ${model_dir}
mkdir -p ${data_dir}

[ ! -f "${label_file}" ] && curl --output ${label_file} https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/master/imagenet-simple-labels.json

PYTHONPATH=./ python -m src.app.ml.resnet50_onnx.extract_resnet50
