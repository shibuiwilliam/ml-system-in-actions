FROM python:3.8-slim

ENV PROJECT_DIR circuit_breaker_pattern
WORKDIR /${PROJECT_DIR}
ADD ./requirements.txt /${PROJECT_DIR}/
RUN apt-get -y update && \
    apt-get -y install apt-utils gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir -r requirements.txt

COPY ./src/ /${PROJECT_DIR}/src/
COPY ./models/default_iris_svc.onnx /${PROJECT_DIR}/models/default_iris_svc.onnx
COPY ./models/label.json /${PROJECT_DIR}/models/label.json

ENV MODEL_FILEPATH /${PROJECT_DIR}/models/iris_svc.onnx
ENV LABEL_FILEPATH /${PROJECT_DIR}/models/label.json
ENV LOG_LEVEL DEBUG
ENV LOG_FORMAT TEXT

COPY ./run.sh /${PROJECT_DIR}/run.sh
RUN chmod +x /${PROJECT_DIR}/run.sh
CMD [ "./run.sh" ]
