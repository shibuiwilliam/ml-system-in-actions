import asyncio
import base64
import io
import logging
import os
from concurrent.futures import ProcessPoolExecutor
from time import sleep

import grpc
from src.api_composition_proxy.backend import request_tfserving, store_data_job
from src.api_composition_proxy.configurations import CacheConfigurations, ModelConfigurations, ServiceConfigurations
from tensorflow_serving.apis import prediction_service_pb2_grpc

log_format = logging.Formatter("%(asctime)s %(name)s [%(levelname)s] %(message)s")
logger = logging.getLogger("prediction_batch")
stdout_handler = logging.StreamHandler()
stdout_handler.setFormatter(log_format)
logger.addHandler(stdout_handler)
logger.setLevel(logging.DEBUG)


def _trigger_prediction_if_queue(stub: prediction_service_pb2_grpc.PredictionServiceStub):
    job_id = store_data_job.right_pop_queue(CacheConfigurations.queue_name)
    logger.info(f"predict job_id: {job_id}")
    if job_id is not None:
        data = store_data_job.get_data_redis(job_id)
        if data != "":
            return True
        image_key = store_data_job.make_image_key(job_id)
        image_data = store_data_job.get_data_redis(image_key)
        decoded = base64.b64decode(image_data)
        io_bytes = io.BytesIO(decoded)
        prediction = request_tfserving.request_grpc(
            stub=stub,
            image=io_bytes.read(),
            model_spec_name=ModelConfigurations.async_model_spec_name,
            signature_name=ModelConfigurations.async_signature_name,
            timeout_second=5,
        )
        if prediction is not None:
            return store_data_job.set_data_redis(job_id, prediction)
        else:
            return store_data_job.left_push_queue(CacheConfigurations.queue_name, job_id)


def _loop():
    channel = grpc.insecure_channel(ServiceConfigurations.grpc_inception_v3)
    stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)

    while True:
        sleep(1)
        _trigger_prediction_if_queue(stub=stub)


def prediction_loop(num_procs: int = 2):
    executor = ProcessPoolExecutor(num_procs)
    loop = asyncio.get_event_loop()

    for _ in range(num_procs):
        asyncio.ensure_future(loop.run_in_executor(executor, _loop))

    loop.run_forever()


def main():
    NUM_PROCS = int(os.getenv("NUM_PROCS", 2))
    prediction_loop(NUM_PROCS)


if __name__ == "__main__":
    logger.info("start backend")
    main()
