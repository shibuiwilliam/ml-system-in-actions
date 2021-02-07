import logging
import os
import time
from typing import Tuple

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
from PIL import Image
from torch.utils.data import DataLoader, Dataset
from torch.utils.tensorboard import SummaryWriter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Cifar10Dataset(Dataset):
    def __init__(self, data_directory, transform):
        super().__init__()
        self.data_directory = data_directory
        self.transform = transform
        self.image_array_list = []
        self.label_list = []
        self.__load_image_files_and_labels()

    def __len__(self):
        return len(self.image_array_list)

    def __getitem__(self, index):
        image_array = self.image_array_list[index]

        image_tensor = self.transform(image_array)
        label = self.label_list[index]

        return image_tensor, label

    def __load_image_files_and_labels(self):
        class_directories = [i for i in os.listdir(self.data_directory) if i.isdecimal()]
        filepath_list = []
        for d in class_directories:
            _d = os.path.join(self.data_directory, d)
            filepath_list.extend([os.path.join(_d, f) for f in os.listdir(_d)])
            self.label_list.extend([int(d) for _ in os.listdir(_d)])
        for fp in filepath_list:
            with Image.open(fp, "r") as img:
                self.image_array_list.append(np.array(img))
        logger.info(f"loaded: {len(self.label_list)} data")


class SimpleModel(nn.Module):
    def __init__(self):
        super(SimpleModel, self).__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 16 * 5 * 5)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


class VGG11(nn.Module):
    def __init__(self):
        super(VGG11, self).__init__()
        num_classes = 10

        self.block1_output = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )

        self.block2_output = nn.Sequential(
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )

        self.block3_output = nn.Sequential(
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )

        self.block4_output = nn.Sequential(
            nn.Conv2d(256, 512, kernel_size=3, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(inplace=True),
            nn.Conv2d(512, 512, kernel_size=3, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )

        self.block5_output = nn.Sequential(
            nn.Conv2d(512, 512, kernel_size=3, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(inplace=True),
            nn.Conv2d(512, 512, kernel_size=3, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )

        self.classifier = nn.Sequential(
            nn.Linear(512, 512),
            nn.ReLU(True),
            nn.Dropout(),
            nn.Linear(512, 32),
            nn.ReLU(True),
            nn.Dropout(),
            nn.Linear(32, num_classes),
        )

    def forward(self, x):
        x = self.block1_output(x)
        x = self.block2_output(x)
        x = self.block3_output(x)
        x = self.block4_output(x)
        x = self.block5_output(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x


class VGG16(nn.Module):
    def __init__(self):
        super(VGG16, self).__init__()
        num_classes = 10

        self.block1_output = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )

        self.block2_output = nn.Sequential(
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )

        self.block3_output = nn.Sequential(
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )

        self.block4_output = nn.Sequential(
            nn.Conv2d(256, 512, kernel_size=3, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(inplace=True),
            nn.Conv2d(512, 512, kernel_size=3, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(inplace=True),
            nn.Conv2d(512, 512, kernel_size=3, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )

        self.block5_output = nn.Sequential(
            nn.Conv2d(512, 512, kernel_size=3, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(inplace=True),
            nn.Conv2d(512, 512, kernel_size=3, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(inplace=True),
            nn.Conv2d(512, 512, kernel_size=3, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )

        self.classifier = nn.Sequential(
            nn.Linear(512, 512),
            nn.ReLU(True),
            nn.Dropout(),
            nn.Linear(512, 32),
            nn.ReLU(True),
            nn.Dropout(),
            nn.Linear(32, num_classes),
        )

    def forward(self, x):
        x = self.block1_output(x)
        x = self.block2_output(x)
        x = self.block3_output(x)
        x = self.block4_output(x)
        x = self.block5_output(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x


def evaluate(
    model: nn.Module,
    test_dataloader: DataLoader,
    criterion,
    writer: SummaryWriter,
    epoch: int,
    device: str = "cpu",
) -> Tuple[float, float]:
    correct = 0
    total = 0
    total_loss = 0.0
    with torch.no_grad():
        for data in test_dataloader:
            images, labels = data[0].to(device), data[1].to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            total_loss += criterion(outputs, labels)

    accuracy = 100 * float(correct / total)
    loss = total_loss / 10000

    writer.add_scalar("Loss/test", loss, epoch)
    writer.add_scalar("Accuracy/test", accuracy, epoch)
    logger.info(f"Accuracy: {accuracy}, Loss: {loss}")
    return accuracy, float(loss)


def train(
    model: nn.Module,
    train_dataloader: DataLoader,
    test_dataloader: DataLoader,
    criterion,
    optimizer,
    writer: SummaryWriter,
    epochs: int = 10,
    checkpoints_directory: str = "/opt/cifar10/model/",
    device: str = "cpu",
):
    logger.info("start training...")
    for epoch in range(epochs):
        running_loss = 0.0
        logger.info(f"starting epoch: {epoch}")
        epoch_start = time.time()
        start = time.time()
        for i, data in enumerate(train_dataloader, 0):
            images, labels = data[0].to(device), data[1].to(device)

            optimizer.zero_grad()

            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            writer.add_scalar("data/total_loss", float(loss.item()), (epoch + 1) * i)
            writer.add_scalar("Loss/train", float(running_loss / (i + 1)), (epoch + 1) * i)

            if i % 200 == 199:
                end = time.time()
                logger.info(f"[{epoch}, {i}] loss: {running_loss / 200} duration: {end - start}")
                running_loss = 0.0
                start = time.time()
        epoch_end = time.time()
        logger.info(f"[{epoch}] duration in seconds: {epoch_end - epoch_start}")

        _, loss = evaluate(
            model=model,
            test_dataloader=test_dataloader,
            criterion=criterion,
            writer=writer,
            epoch=epoch,
            device=device,
        )
        checkpoints = os.path.join(checkpoints_directory, f"epoch_{epoch}_loss_{loss}.pth")
        logger.info(f"save checkpoints: {checkpoints}")
        torch.save(model.state_dict(), checkpoints)
