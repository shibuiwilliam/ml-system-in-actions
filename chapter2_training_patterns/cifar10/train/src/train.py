import argparse
import logging
import os

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
from torchvision import transforms

from src.model import Cifar10Dataset, SimpleModel, VGG16, evaluate, train
from src.constants import MODEL_ENUM

import mlflow
import mlflow.pytorch


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def start_run(
    mlflow_experiment_id: str,
    upstream_directory: str,
    downstream_directory: str,
    tensorboard_directory: str,
    batch_size: int,
    num_workers: int,
    epochs: int,
    learning_rate: float,
    model_type: str,
):
    writer = SummaryWriter(log_dir=tensorboard_directory)

    batch_size = batch_size
    transform = transforms.Compose(
        [transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))],
    )

    train_dataset = Cifar10Dataset(
        data_directory=os.path.join(upstream_directory, "train"),
        transform=transform,
    )
    train_dataloader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
    )

    test_dataset = Cifar10Dataset(
        data_directory=os.path.join(upstream_directory, "test"),
        transform=transform,
    )
    test_dataloader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
    )

    if model_type == MODEL_ENUM.SIMPLE_MODEL.value:
        model = SimpleModel()
    elif model_type == MODEL_ENUM.VGG16.value:
        model = VGG16()
    else:
        raise ValueError("Unknown model")
    model.eval()

    mlflow.pytorch.log_model(model, "model")

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    train(
        model=model,
        train_dataloader=train_dataloader,
        test_dataloader=test_dataloader,
        criterion=criterion,
        optimizer=optimizer,
        epochs=epochs,
        writer=writer,
        checkpoints_directory=downstream_directory,
    )

    accuracy, loss = evaluate(
        model=model,
        test_dataloader=test_dataloader,
        criterion=criterion,
        writer=writer,
        epoch=epochs + 1,
    )
    logger.info(f"Latest performance: Accuracy: {accuracy}, Loss: {loss}")

    writer.close()

    model_file_name = os.path.join(downstream_directory, f"cifar10_{mlflow_experiment_id}.pth")
    onnx_file_name = os.path.join(downstream_directory, f"cifar10_{mlflow_experiment_id}.onnx")

    torch.save(model.state_dict(), model_file_name)

    dummy_input = torch.randn(1, 3, 32, 32)
    torch.onnx.export(
        model,
        dummy_input,
        onnx_file_name,
        verbose=True,
        input_names=["input1"],
        output_names=["output1"],
    )

    mlflow.log_param("optimizer", "Adam")
    mlflow.log_param("preprocess", "Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))")
    mlflow.log_param("epochs", epochs)
    mlflow.log_param("learning_rate", learning_rate)
    mlflow.log_param("batch_size", batch_size)
    mlflow.log_param("num_workers", num_workers)
    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("loss", loss)
    mlflow.log_artifact(model_file_name)
    mlflow.log_artifact(onnx_file_name)
    mlflow.log_artifacts(tensorboard_directory, artifact_path="events")


def main():
    parser = argparse.ArgumentParser(
        description="Train Cifar10",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--upstream",
        type=str,
        default="/opt/data/preprocess",
        help="upstream directory",
    )
    parser.add_argument(
        "--downstream",
        type=str,
        default="/opt/cifar10/model/",
        help="downstream directory",
    )
    parser.add_argument(
        "--tensorboard",
        type=str,
        default="/opt/cifar10/tensorboard/",
        help="tensorboard directory",
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=100,
        help="epochs",
    )
    parser.add_argument(
        "--batch_size",
        type=int,
        default=32,
        help="batch size",
    )
    parser.add_argument(
        "--num_workers",
        type=int,
        default=4,
        help="number of workers",
    )
    parser.add_argument(
        "--learning_rate",
        type=float,
        default=0.001,
        help="learning rate",
    )
    parser.add_argument(
        "--model_type",
        type=str,
        default=MODEL_ENUM.SIMPLE_MODEL.value,
        choices=[MODEL_ENUM.SIMPLE_MODEL.value, MODEL_ENUM.VGG16.value],
        help="simple or vgg",
    )
    args = parser.parse_args()
    mlflow_experiment_id = int(os.getenv("MLFLOW_EXPERIMENT_ID", 0))

    upstream_directory = args.upstream
    downstream_directory = args.downstream
    tensorboard_directory = args.tensorboard
    os.makedirs(downstream_directory, exist_ok=True)
    os.makedirs(tensorboard_directory, exist_ok=True)

    start_run(
        mlflow_experiment_id=mlflow_experiment_id,
        upstream_directory=upstream_directory,
        downstream_directory=downstream_directory,
        tensorboard_directory=tensorboard_directory,
        batch_size=args.batch_size,
        num_workers=args.num_workers,
        epochs=args.epochs,
        learning_rate=args.learning_rate,
        model_type=args.model_type,
    )


if __name__ == "__main__":
    main()
