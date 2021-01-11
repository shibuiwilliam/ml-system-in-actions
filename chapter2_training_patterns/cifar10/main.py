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
    parser = argparse.ArgumentParser(description="Runner", formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument(
        "--preprocess_data",
        type=str,
        default="cifar10",
        help="cifar10 or cifar100; default cifar10",
    )
    parser.add_argument(
        "--preprocess_downstream",
        type=str,
        default="/opt/cifar10/preprocess/",
        help="preprocess downstream directory",
    )
    parser.add_argument(
        "--preprocess_cached_data_id",
        type=str,
        default="",
        help="previous run id for cache",
    )

    parser.add_argument(
        "--train_upstream",
        type=str,
        default="/opt/data/preprocess",
        help="upstream directory",
    )
    parser.add_argument(
        "--train_downstream",
        type=str,
        default="/opt/cifar10/model/",
        help="downstream directory",
    )
    parser.add_argument(
        "--train_tensorboard",
        type=str,
        default="/opt/cifar10/tensorboard/",
        help="tensorboard directory",
    )
    parser.add_argument(
        "--train_epochs",
        type=int,
        default=100,
        help="epochs",
    )
    parser.add_argument(
        "--train_batch_size",
        type=int,
        default=32,
        help="batch size",
    )
    parser.add_argument(
        "--train_num_workers",
        type=int,
        default=4,
        help="number of workers",
    )
    parser.add_argument(
        "--train_learning_rate",
        type=float,
        default=0.001,
        help="learning rate",
    )
    parser.add_argument(
        "--train_model_type",
        type=str,
        default="vgg11",
        choices=["simple", "vgg11", "vgg16"],
        help="simple, vgg11 or vgg16",
    )

    parser.add_argument(
        "--evaluate_downstream",
        type=str,
        default="/opt/data/evaluate/",
        help="evaluate downstream directory",
    )
    parser.add_argument(
        "--evaluate_test_data_directory",
        type=str,
        default="/opt/data/preprocess/test",
        help="evaluate test data directory",
    )
    parser.add_argument(
        "--evaluate_dockerfile_path",
        type=str,
        default="/opt/data/evaluate/Dockerfile",
        help="evaluate Dockerfile path",
    )
    parser.add_argument(
        "--evaluate_model_filename",
        type=str,
        default="vgg11.onnx",
        help="evaluate model file name",
    )
    parser.add_argument(
        "--evaluate_model_directory",
        type=str,
        default="/opt/mlruns/0/abc/artifaces/downstream_directory/",
        help="evaluate model file directory",
    )
    parser.add_argument(
        "--evaluate_entrypoint_path",
        type=str,
        default="/opt/data/evaluate/onnx_runtime_server_entrypoint.sh",
        help="evaluate entrypoint path",
    )

    args = parser.parse_args()

    with mlflow.start_run() as r:
        # preprocess_run = mlflow.run(
        #     "./preprocess",
        #     "preprocess",
        #     backend="local",
        #     parameters={
        #         "data": args.preprocess_data,
        #         "downstream": args.preprocess_downstream,
        #         "cached_data_id": args.preprocess_cached_data_id,
        #     },
        # )
        # preprocess_run = mlflow.tracking.MlflowClient().get_run(preprocess_run.run_id)

        # train_run = mlflow.run(
        #     "./train",
        #     "train",
        #     backend="local",
        #     parameters={
        #         "downstream": args.train_downstream,
        #         "tensorboard": args.train_tensorboard,
        #         "epochs": args.train_epochs,
        #         "batch_size": args.train_batch_size,
        #         "num_workers": args.train_num_workers,
        #         "learning_rate": args.train_learning_rate,
        #         "model_type": args.train_model_type,
        #         "upstream": os.path.join("/tmp/mlruns/0", preprocess_run.info.run_id, "artifacts/downstream_directory"),
        #     },
        # )
        # train_run = mlflow.tracking.MlflowClient().get_run(train_run.run_id)
        # evaluate_run = mlflow.run(
        #     "./evaluate",
        #     "evaluate",
        #     backend="local",
        #     parameters={
        #         "downstream": args.evaluate_downstream,
        #         "test_data_directory": args.evaluate_test_data_directory,
        #         "dockerfile_path": args.evaluate_dockerfile_path,
        #         "model_filename": args.evaluate_model_filename,
        #         "model_directory": args.evaluate_model_directory,
        #         "entrypoint_path": args.evaluate_entrypoint_path,
        #         "upstream": os.path.join("/tmp/mlruns/0", train_run.info.run_id, "artifacts/downstream_directory"),
        #     },
        # )
        # evaluate_run = mlflow.tracking.MlflowClient().get_run(evaluate_run.run_id)

        train_run = "43b3c07c316e487b97c194d043e14c49"
        evaluate_run = mlflow.run(
            "./evaluate",
            "evaluate",
            backend="local",
            parameters={
                "downstream": args.evaluate_downstream,
                "test_data_directory": args.evaluate_test_data_directory,
                "dockerfile_path": args.evaluate_dockerfile_path,
                "model_filename": args.evaluate_model_filename,
                "model_directory": args.evaluate_model_directory,
                "entrypoint_path": args.evaluate_entrypoint_path,
                "upstream": os.path.join("/tmp/mlruns/0", train_run, "artifacts/downstream_directory"),
            },
        )
        evaluate_run = mlflow.tracking.MlflowClient().get_run(evaluate_run.run_id)


if __name__ == "__main__":
    main()