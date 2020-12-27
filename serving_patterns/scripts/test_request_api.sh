#!/bin/bash

set -eu

TARGET_HOST=localhost
WEB_SINGLE_PORT=8888
SYNCHRONOUS_PORT=8889
ASYNCHRONOUS_PORT=8890
HEALTH=health
LABELS=labels
PREDICT=predict
LABEL=label


function which_is_it() {
    echo "******* ${1} *******"
}

function finish() {
    echo -e "\n"
}

function health() {
    endpoint=${TARGET_HOST}:$1/${HEALTH}
    which_is_it "${endpoint}"
    curl -X GET \
        ${endpoint}
    finish
}

function labels(){
    endpoint=${TARGET_HOST}:$1/${PREDICT}/${LABELS}
    which_is_it "${endpoint}"
    curl -X GET \
        ${endpoint}
    finish
}

function test_predict() {
    endpoint=${TARGET_HOST}:$1/${PREDICT}
    which_is_it "${endpoint}"
    curl -X GET \
        ${endpoint}
    finish
}

function test_predict_label() {
    endpoint=${TARGET_HOST}:$1/${PREDICT}/${LABEL}
    which_is_it "${endpoint}"
    curl -X GET \
        ${endpoint}
    finish
}

function predict() {
    endpoint=${TARGET_HOST}:$1/${PREDICT}
    which_is_it "${endpoint}"
    curl -X POST \
        -H "Content-Type: application/json" \
        -d '{"input_data": [5.2, 3.1, 0.1, 1.0]}' \
        ${endpoint}
    finish
}

function predict_label() {
    endpoint=${TARGET_HOST}:$1/${PREDICT}/${LABEL}
    which_is_it "${endpoint}"
    curl -X POST \
        -H "Content-Type: application/json" \
        -d '{"input_data": [5.2, 3.1, 0.1, 1.0]}' \
        ${endpoint}
    finish
}

function all() {
    health $1
    labels $1
    test_predict $1
    test_predict_label $1
    predict $1
    predict_label $1
}

function all_wo_pl() {
    health $1
    labels $1
    test_predict $1
    test_predict_label $1
    predict $1
}

all ${WEB_SINGLE_PORT}
all ${SYNCHRONOUS_PORT}
all_wo_pl ${ASYNCHRONOUS_PORT}
