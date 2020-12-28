import logging
from time import sleep
import asyncio
import os
import base64
import io
from concurrent.futures import ProcessPoolExecutor

from src.configurations import CacheConfigurations, ModelConfigurations
from src.app.backend import store_data_job, request_inception_v3


logger = logging.getLogger("prediction_batch")


def _run_prediction(job_id: str) -> bool:
    data = store_data_job.get_data_redis(job_id)
    if data != "":
        return True
    image_key = store_data_job.make_image_key(job_id)
    image_data = store_data_job.get_data_redis(image_key)
    decoded = base64.b64decode(image_data)
    io_bytes = io.BytesIO(decoded)
    prediction = request_inception_v3.request_grpc(
        image=io_bytes.read(),
        model_spec_name=ModelConfigurations.model_spec_name,
        signature_name=ModelConfigurations.signature_name,
        address=ModelConfigurations.address,
        port=ModelConfigurations.grpc_port,
        timeout_second=5,
    )
    if prediction is not None:
        return store_data_job.set_data_redis(job_id, prediction)
    else:
        return store_data_job.left_push_queue(CacheConfigurations.queue_name, job_id)


def _trigger_prediction_if_queue():
    job_id = store_data_job.right_pop_queue(CacheConfigurations.queue_name)
    logger.info(f"predict job_id: {job_id}")
    if job_id is not None:
        _run_prediction(job_id)


def _loop():
    while True:
        sleep(1)
        _trigger_prediction_if_queue()


def prediction_loop(num_procs: int = 2):
    executor = ProcessPoolExecutor(num_procs)
    loop = asyncio.get_event_loop()

    for _ in range(num_procs):
        asyncio.ensure_future(loop.run_in_executor(executor, _loop))

    loop.run_forever()
