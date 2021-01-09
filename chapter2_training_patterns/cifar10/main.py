import argparse
import logging
import os

import mlflow
from mlflow.utils import mlflow_tags
from mlflow.entities import RunStatus

from mlflow.tracking.fluent import _get_experiment_id

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    with mlflow.start_run() as r:
        base_dir = "/opt/data/"
        preprocess_run = mlflow.run(
            "./preprocess",
            "preprocess",
            backend="local",
            parameters={
                "data": "cifar10",
                "downstream": os.path.join(base_dir, "preprocess/"),
            },
        )
        preprocess_run = mlflow.tracking.MlflowClient().get_run(preprocess_run.run_id)

        train_run = mlflow.run(
            "./train",
            "train",
            backend="local",
            parameters={
                # "upstream": os.path.join(
                #     "/tmp/mlruns/0", "624b8c80539c4de998d203890841f204", "artifacts/downstream_directory"
                # ),
                "upstream": os.path.join("/tmp/mlruns/0", preprocess_run.run_id, "artifacts/downstream_directory"),
            },
        )
        train_run = mlflow.tracking.MlflowClient().get_run(train_run.run_id)


if __name__ == "__main__":
    main()