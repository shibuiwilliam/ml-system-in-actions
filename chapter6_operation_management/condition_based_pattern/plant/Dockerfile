FROM tensorflow/tensorflow:2.5.1 as builder

ARG SERVER_DIR=plant
ENV PROJECT_DIR plant
WORKDIR /${PROJECT_DIR}
ADD ./${SERVER_DIR}/requirements.txt /${PROJECT_DIR}/

COPY ./${SERVER_DIR}/extract_plant.py /${PROJECT_DIR}/extract_plant.py
COPY ./${SERVER_DIR}/data/plant_labels.json /${PROJECT_DIR}/data/plant_labels.json

RUN apt-get -y update && \
    apt-get -y install apt-utils gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install  --no-cache-dir -r requirements.txt && \
    touch __init__.py && \
    python -m extract_plant


FROM tensorflow/serving:2.5.2

ARG SERVER_DIR=plant
ENV PROJECT_DIR plant
ENV MODEL_BASE_PATH /${PROJECT_DIR}/saved_model/plant
ENV MODEL_NAME plant

COPY --from=builder /${PROJECT_DIR}/saved_model/plant ${MODEL_BASE_PATH}
EXPOSE 8500
EXPOSE 8501

COPY ./${SERVER_DIR}/tf_serving_entrypoint.sh /usr/bin/tf_serving_entrypoint.sh
RUN chmod +x /usr/bin/tf_serving_entrypoint.sh
ENTRYPOINT ["/usr/bin/tf_serving_entrypoint.sh"]