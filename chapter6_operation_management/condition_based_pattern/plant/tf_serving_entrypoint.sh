#!/bin/bash

set -eu

PORT=${PORT:-9500}
REST_API_PORT=${REST_API_PORT:-9501}
MODEL_NAME=${MODEL_NAME:-"plant"}
MODEL_BASE_PATH=${MODEL_BASE_PATH:-"/plant/saved_model/${MODEL_NAME}"}

tensorflow_model_server \
    --port=${PORT} \
    --rest_api_port=${REST_API_PORT} \
    --model_name=${MODEL_NAME} \
    --model_base_path=${MODEL_BASE_PATH} 