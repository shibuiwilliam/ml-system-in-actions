FROM mcr.microsoft.com/onnxruntime/server:latest

ARG model_filename=cifar10_0.onnx
ARG model_directory=./
ARG entrypoint_path=./building/onnx_runtime_server_entrypoint.sh

ENV PROJECT_DIR cifar10

WORKDIR /${PROJECT_DIR}

COPY ./${model_filename} /${PROJECT_DIR}/${model_filename}

ENV MODEL_PATH /${PROJECT_DIR}/${model_filename}

WORKDIR /onnxruntime/server/
COPY ./${entrypoint_path} ./onnx_runtime_server_entrypoint.sh
RUN chmod +x onnx_runtime_server_entrypoint.sh
ENTRYPOINT ["./onnx_runtime_server_entrypoint.sh"]
