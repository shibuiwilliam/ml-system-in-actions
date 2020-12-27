FROM python:3.8-slim

ARG PATTERN=web_single_pattern
ENV PROJECT_DIR web_single_pattern
WORKDIR /${PROJECT_DIR}
ADD ${PATTERN}/requirements.txt /${PROJECT_DIR}/
RUN apt-get -y update && \
    apt-get -y install apt-utils gcc curl && \
    pip install --no-cache-dir -r requirements.txt

COPY ${PATTERN}/src/ /${PROJECT_DIR}/src/
COPY utils/ /${PROJECT_DIR}/src/utils/
COPY ${PATTERN}/models/ /${PROJECT_DIR}/models/

ENV MODEL_FILEPATH /${PROJECT_DIR}/models/iris_svc.onnx
ENV LABEL_FILEPATH /${PROJECT_DIR}/models/label.json
ENV LOG_LEVEL DEBUG
ENV LOG_FORMAT TEXT

COPY ${PATTERN}/scripts/run_api.sh /${PROJECT_DIR}/run_api.sh
RUN chmod +x run_api.sh
CMD ./run_api.sh
