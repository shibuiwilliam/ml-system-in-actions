#!/bin/bash

set -eu

work_dir=./src/app/ml/mobilenetv2
model_dir=${work_dir}/model
data_dir=${work_dir}/data
label_file=${data_dir}/imagenet_labels_1001.json

mkdir -p ${model_dir}
mkdir -p ${data_dir}

if [ ! -f "${label_file}" ]; then
    curl --output ${label_file} https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/master/imagenet-simple-labels.json
    sed -i 's/"tench"/"background","tench"/' "${label_file}"
fi

PYTHONPATH=./ python -m src.app.ml.mobilenetv2.extract_mobilenetv2
