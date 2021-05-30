FROM python:3.8-slim

ENV PROJECT_DIR model_db
WORKDIR /${PROJECT_DIR}
ADD requirements.txt /${PROJECT_DIR}/
RUN apt-get -y update && \
    apt-get -y install \
    apt-utils \
    gcc \
    libpq-dev \
    python-dev \
    git \
    build-essential \
    libtool \
    automake && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install Cython && \
    pip install git+https://github.com/MagicStack/uvloop && \
    pip install --no-cache-dir -r requirements.txt

COPY src/ /${PROJECT_DIR}/src/

COPY run.sh /${PROJECT_DIR}/run.sh
RUN chmod +x /${PROJECT_DIR}/run.sh
CMD [ "./run.sh" ]