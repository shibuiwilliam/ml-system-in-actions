FROM tensorflow/tensorflow:2.4.0 as builder

ARG SERVER_DIR=imagenet_inception_v3
ENV PROJECT_DIR training_patterns
WORKDIR /${PROJECT_DIR}
ADD ./${SERVER_DIR}/requirements.txt /${PROJECT_DIR}/
RUN apt-get -y update && \
    apt-get -y install apt-utils gcc curl && \
    pip install  --no-cache-dir -r requirements.txt && \
    touch __init__.py

COPY ./${SERVER_DIR}/extract_inception_v3.py /${PROJECT_DIR}/extract_inception_v3.py
COPY ./${SERVER_DIR}/image_net_labels.json /${PROJECT_DIR}/image_net_labels.json

RUN python -m extract_inception_v3


FROM tensorflow/serving:2.4.0

ARG SERVER_DIR=imagenet_inception_v3
ENV PROJECT_DIR synchronous_pattern
ENV MODEL_BASE_PATH /${PROJECT_DIR}/saved_model/inception_v3
ENV MODEL_NAME inception_v3

COPY --from=builder /training_patterns/saved_model/inception_v3 ${MODEL_BASE_PATH}
EXPOSE 8500
EXPOSE 8501

COPY ./${SERVER_DIR}/tf_serving_entrypoint.sh /usr/bin/tf_serving_entrypoint.sh
RUN chmod +x /usr/bin/tf_serving_entrypoint.sh
ENTRYPOINT ["/usr/bin/tf_serving_entrypoint.sh"]