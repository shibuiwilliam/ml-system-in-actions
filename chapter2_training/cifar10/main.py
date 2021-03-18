import argparse
import os

import mlflow


def main():
    parser = argparse.ArgumentParser(
        description="Runner",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "--commit_hash",
        type=str,
        default="000000",
        help="code commit hash",
    )

    parser.add_argument(
        "--preprocess_data",
        type=str,
        default="cifar10",
        help="cifar10 or cifar100; default cifar10",
    )
    parser.add_argument(
        "--preprocess_downstream",
        type=str,
        default="./preprocess/data/preprocess",
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
        default="./preprocess/data/preprocess",
        help="upstream directory",
    )
    parser.add_argument(
        "--train_downstream",
        type=str,
        default="./train/data/model/",
        help="downstream directory",
    )
    parser.add_argument(
        "--train_tensorboard",
        type=str,
        default="./train/data/tensorboard/",
        help="tensorboard directory",
    )
    parser.add_argument(
        "--train_epochs",
        type=int,
        default=1,
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
        "--building_dockerfile_path",
        type=str,
        default="./Dockerfile",
        help="building Dockerfile path",
    )
    parser.add_argument(
        "--building_model_filename",
        type=str,
        default="cifar10_0.onnx",
        help="building model file name",
    )
    parser.add_argument(
        "--building_entrypoint_path",
        type=str,
        default="./onnx_runtime_server_entrypoint.sh",
        help="building entrypoint path",
    )

    parser.add_argument(
        "--evaluate_downstream",
        type=str,
        default="./data/evaluate/",
        help="evaluate downstream directory",
    )

    args = parser.parse_args()
    mlflow_experiment_id = int(os.getenv("MLFLOW_EXPERIMENT_ID", 0))

    with mlflow.start_run() as r:
        preprocess_run = mlflow.run(
            uri="./preprocess",
            entry_point="preprocess",
            backend="local",
            parameters={
                "data": args.preprocess_data,
                "downstream": args.preprocess_downstream,
                "cached_data_id": args.preprocess_cached_data_id,
            },
        )
        preprocess_run = mlflow.tracking.MlflowClient().get_run(preprocess_run.run_id)

        dataset = os.path.join(
            "/tmp/mlruns/",
            str(mlflow_experiment_id),
            preprocess_run.info.run_id,
            "artifacts/downstream_directory",
        )

        train_run = mlflow.run(
            uri="./train",
            entry_point="train",
            backend="local",
            parameters={
                "upstream": dataset,
                "downstream": args.train_downstream,
                "tensorboard": args.train_tensorboard,
                "epochs": args.train_epochs,
                "batch_size": args.train_batch_size,
                "num_workers": args.train_num_workers,
                "learning_rate": args.train_learning_rate,
                "model_type": args.train_model_type,
            },
        )
        train_run = mlflow.tracking.MlflowClient().get_run(train_run.run_id)

        building_run = mlflow.run(
            uri="./building",
            entry_point="building",
            backend="local",
            parameters={
                "dockerfile_path": args.building_dockerfile_path,
                "model_filename": args.building_model_filename,
                "model_directory": os.path.join(
                    "mlruns/",
                    str(mlflow_experiment_id),
                    train_run.info.run_id,
                    "artifacts",
                ),
                "entrypoint_path": args.building_entrypoint_path,
                "dockerimage": f"shibui/ml-system-in-actions:training_pattern_cifar10_evaluate_{mlflow_experiment_id}",
            },
        )
        building_run = mlflow.tracking.MlflowClient().get_run(building_run.run_id)

        evaluate_run = mlflow.run(
            uri="./evaluate",
            entry_point="evaluate",
            backend="local",
            parameters={
                "upstream": os.path.join(
                    "../mlruns/",
                    str(mlflow_experiment_id),
                    train_run.info.run_id,
                    "artifacts",
                ),
                "downstream": args.evaluate_downstream,
                "test_data_directory": os.path.join(
                    "../mlruns/",
                    str(mlflow_experiment_id),
                    preprocess_run.info.run_id,
                    "artifacts/downstream_directory/test",
                ),
                "dockerimage": f"shibui/ml-system-in-actions:training_pattern_cifar10_evaluate_{mlflow_experiment_id}",
                "container_name": f"training_pattern_cifar10_evaluate_{mlflow_experiment_id}",
            },
        )
        evaluate_run = mlflow.tracking.MlflowClient().get_run(evaluate_run.run_id)


if __name__ == "__main__":
    main()
