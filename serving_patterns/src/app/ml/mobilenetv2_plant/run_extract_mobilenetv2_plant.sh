#!/bin/bash

set -eu

work_dir=./src/app/ml/mobilenetv2_plant
model_dir=${work_dir}/model
data_dir=${work_dir}/data
label_file=${data_dir}/aiy_plants_V1_labelmap.csv

mkdir -p ${model_dir}
mkdir -p ${data_dir}

if [ ! -f "${label_file}" ]; then
    curl --output ${label_file} https://www.gstatic.com/aihub/tfhub/labelmaps/aiy_plants_V1_labelmap.csv
fi

PYTHONPATH=./ python -m src.app.ml.mobilenetv2_plant.extract_mobilenetv2
