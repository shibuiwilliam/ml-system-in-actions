#!/bin/bash

set -eu

DVC_FILE="dvc.yaml"
ABSOLUTE_PATH=$(pwd)

IMAGE_NAME=training_patterns_train_iris_pipeline
IMAGE_VERSION=latest
LOCAL_MODEL_DIR=${ABSOLUTE_PATH}/models
LOCAL_DATA_DIR=${ABSOLUTE_PATH}/data
LOCAL_DATA_PREPARED_DIR=${LOCAL_DATA_DIR}/prepared
LOCAL_DATA_TRAINED_DIR=${LOCAL_DATA_DIR}/trained
LOCAL_DATA_EVALUATED_DIR=${LOCAL_DATA_DIR}/evaluated


if [ -e ${DVC_FILE} ]; then
    dvc repro
else
    mkdir -p ${LOCAL_DATA_PREPARED_DIR}
    mkdir -p ${LOCAL_DATA_TRAINED_DIR}
    mkdir -p ${LOCAL_DATA_EVALUATED_DIR}
    dvc run -f \
        -n prepare_data \
        -d ./data/iris_data.csv \
        -d ./data/iris_label.csv \
        -d ./iris_prepare_data.py \
        -p params.yaml:prepare.test_rate \
        -o ./data/prepared \
        docker run --rm \
            --name prepare_data \
            -v ${LOCAL_MODEL_DIR}:/training_patterns/src/iris_pipeline/models \
            -v ${LOCAL_DATA_PREPARED_DIR}:/training_patterns/src/iris_pipeline/data/prepared \
            -v ${LOCAL_DATA_TRAINED_DIR}:/training_patterns/src/iris_pipeline/data/trained \
            -v ${LOCAL_DATA_EVALUATED_DIR}:/training_patterns/src/iris_pipeline/data/evaluated \
            ${IMAGE_NAME}:${IMAGE_VERSION} \
            python iris_prepare_data.py

    dvc run -f \
        -n train \
        -d ./data/prepared/x_train.npy \
        -d ./data/prepared/y_train.npy \
        -d ./data/iris_label.csv \
        -p params.yaml:train.save_model_name \
        -p params.yaml:train.save_format \
        -p params.yaml:train.ml_model \
        -o ./data/trained \
        docker run --rm \
            --name train \
            -v ${LOCAL_MODEL_DIR}:/training_patterns/src/iris_pipeline/models \
            -v ${LOCAL_DATA_DIR}:/training_patterns/src/iris_pipeline/data \
            -v ${LOCAL_DATA_PREPARED_DIR}:/training_patterns/src/iris_pipeline/data/prepared \
            -v ${LOCAL_DATA_TRAINED_DIR}:/training_patterns/src/iris_pipeline/data/trained \
            -v ${LOCAL_DATA_EVALUATED_DIR}:/training_patterns/src/iris_pipeline/data/evaluated \
            ${IMAGE_NAME}:${IMAGE_VERSION} \
            python iris_train.py

    dvc run -f \
        -n evaluate \
        -d ./data/prepared/x_test.npy \
        -d ./data/prepared/y_test.npy \
        -d ./models/iris_svc.pkl \
        -p params.yaml:evaluate.evaluation_model_filename \
        -o ./data/evaluated \
        docker run --rm \
            --name evaluate \
            -v ${LOCAL_MODEL_DIR}:/training_patterns/src/iris_pipeline/models \
            -v ${LOCAL_DATA_DIR}:/training_patterns/src/iris_pipeline/data \
            -v ${LOCAL_DATA_PREPARED_DIR}:/training_patterns/src/iris_pipeline/data/prepared \
            -v ${LOCAL_DATA_TRAINED_DIR}:/training_patterns/src/iris_pipeline/data/trained \
            -v ${LOCAL_DATA_EVALUATED_DIR}:/training_patterns/src/iris_pipeline/data/evaluated \
            ${IMAGE_NAME}:${IMAGE_VERSION} \
            python iris_evaluate.py
fi
