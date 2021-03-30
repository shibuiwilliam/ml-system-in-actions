import datetime
import time
from logging import DEBUG, Formatter, StreamHandler, getLogger
from typing import List

import click
from src.db import cruds, schemas
from src.db.database import get_context_db

logger = getLogger(__name__)
logger.setLevel(DEBUG)
formatter = Formatter("[%(asctime)s] [%(process)d] [%(name)s] [%(levelname)s] %(message)s")

handler = StreamHandler()
handler.setLevel(DEBUG)
handler.setFormatter(formatter)
logger.addHandler(handler)


def evaluate_prediction(
    average_sepal_length: float,
    average_sepal_width: float,
    average_petal_length: float,
    average_petal_width: float,
    threshold: float,
    prediction_logs: List[schemas.PredictionLog],
):
    logger.info("evaluate predictions...")
    sepal_lengths = [0.0 for _ in prediction_logs]
    sepal_widths = [0.0 for _ in prediction_logs]
    petal_length = [0.0 for _ in prediction_logs]
    petal_width = [0.0 for _ in prediction_logs]
    for i, p in enumerate(prediction_logs):
        sepal_lengths[i] = p.log["data"][0][0]
        sepal_widths[i] = p.log["data"][0][1]
        petal_length[i] = p.log["data"][0][2]
        petal_width[i] = p.log["data"][0][3]
    pred_average_sepal_length = sum(sepal_lengths) / len(sepal_lengths)
    pred_average_sepal_width = sum(sepal_widths) / len(sepal_widths)
    pred_average_petal_length = sum(petal_length) / len(petal_length)
    pred_average_petal_width = sum(petal_width) / len(petal_width)

    if pred_average_sepal_length < average_sepal_length * (
        1 - threshold
    ) or pred_average_sepal_length > average_sepal_length * (1 + threshold):
        logger.error(f"average sepal length out of threshold: {pred_average_sepal_length}")
    if pred_average_sepal_width < average_sepal_width * (
        1 - threshold
    ) or pred_average_sepal_width > average_sepal_width * (1 + threshold):
        logger.error(f"average sepal width out of threshold: {pred_average_sepal_width}")
    if pred_average_petal_length < average_petal_length * (
        1 - threshold
    ) or pred_average_petal_length > average_petal_length * (1 + threshold):
        logger.error(f"average petal length out of threshold: {pred_average_petal_length}")
    if pred_average_petal_width < average_petal_width * (
        1 - threshold
    ) or pred_average_petal_width > average_petal_width * (1 + threshold):
        logger.error(f"average petal width out of threshold: {pred_average_petal_width}")
    logger.info(f"average sepal length: {pred_average_sepal_length}")
    logger.info(f"average sepal width: {pred_average_sepal_width}")
    logger.info(f"average petal length: {pred_average_petal_length}")
    logger.info(f"average petal width: {pred_average_petal_width}")
    logger.info("done evaluating predictions")


def evaluate_outlier(
    outlier_threshold: float,
    outlier_logs: List[schemas.OutlierLog],
):
    logger.info("evaluate outliers...")
    outliers = 0
    for o in outlier_logs:
        if o.log["is_outlier"]:
            outliers += 1
    if outliers > len(outlier_logs) * outlier_threshold:
        logger.error(f"too many outliers: {outliers}")
    logger.info(f"outliers: {outliers}")
    logger.info("done evaluating outliers")


@click.command(name="request job")
@click.option("--interval", type=int, default=1)
@click.option("--outlier_threshold", type=float, default=0.2)
@click.option("--average_sepal_length", type=float, default=5.84)
@click.option("--average_sepal_width", type=float, default=3.06)
@click.option("--average_petal_length", type=float, default=3.76)
@click.option("--average_petal_width", type=float, default=1.20)
@click.option("--threshold", type=float, default=0.05)
def main(
    interval: int,
    outlier_threshold: float,
    average_sepal_length: float,
    average_sepal_width: float,
    average_petal_length: float,
    average_petal_width: float,
    threshold: float,
):
    logger.info("start monitoring...")
    while True:
        now = datetime.datetime.now()
        interval_ago = now - datetime.timedelta(minutes=(interval + 1))
        time_later = now.strftime("%Y-%m-%d %H:%M:%S")
        time_before = interval_ago.strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"time between {time_before} and {time_later}")
        with get_context_db() as db:
            prediction_logs = cruds.select_prediction_log_between(db=db, time_before=time_before, time_later=time_later)
            outlier_logs = cruds.select_outlier_log_between(db=db, time_before=time_before, time_later=time_later)
        logger.info(f"prediction_logs between {time_before} and {time_later}: {len(prediction_logs)}")
        logger.info(f"outlier_logs between {time_before} and {time_later}: {len(outlier_logs)}")
        if len(prediction_logs) > 0:
            evaluate_prediction(
                average_sepal_length=average_sepal_length,
                average_sepal_width=average_sepal_width,
                average_petal_length=average_petal_length,
                average_petal_width=average_petal_width,
                threshold=threshold,
                prediction_logs=prediction_logs,
            )
        if len(outlier_logs) > 0:
            evaluate_outlier(
                outlier_threshold=outlier_threshold,
                outlier_logs=outlier_logs,
            )
        time.sleep(interval * 60)


if __name__ == "__main__":
    main()
