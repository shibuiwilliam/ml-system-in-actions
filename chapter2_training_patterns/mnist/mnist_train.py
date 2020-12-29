import pytorch_lightning as pl
import mlflow.pytorch
import os
import torch
import click
from argparse import ArgumentParser
from pytorch_lightning.callbacks.early_stopping import EarlyStopping
from pytorch_lightning.callbacks import ModelCheckpoint
from pytorch_lightning.callbacks import LearningRateMonitor
from pytorch_lightning.metrics.functional import accuracy
from torch.nn import functional as F
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, transforms


class MNISTDataModule(pl.LightningDataModule):
    def __init__(self, **kwargs):
        super(MNISTDataModule, self).__init__()
        self.df_train = None
        self.df_val = None
        self.df_test = None
        self.train_data_loader = None
        self.val_data_loader = None
        self.test_data_loader = None
        self.args = kwargs

        self.transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])

    def setup(self, stage=None):
        self.df_train = datasets.MNIST("dataset", download=True, train=True, transform=self.transform)
        self.df_train, self.df_val = random_split(self.df_train, [55000, 5000])
        self.df_test = datasets.MNIST("dataset", download=True, train=False, transform=self.transform)

    def create_data_loader(self, df):
        return DataLoader(
            df,
            batch_size=self.args["batch_size"],
            num_workers=self.args["num_workers"],
        )

    def train_dataloader(self):
        return self.create_data_loader(self.df_train)

    def val_dataloader(self):
        return self.create_data_loader(self.df_val)

    def test_dataloader(self):
        return self.create_data_loader(self.df_test)


class LightningMNISTClassifier(pl.LightningModule):
    def __init__(self, **kwargs):
        super(LightningMNISTClassifier, self).__init__()

        self.optimizer = None
        self.scheduler = None
        self.layer_1 = torch.nn.Linear(28 * 28, 128)
        self.layer_2 = torch.nn.Linear(128, 256)
        self.layer_3 = torch.nn.Linear(256, 10)
        self.args = kwargs

    @staticmethod
    def add_model_specific_args(parent_parser):
        parser = ArgumentParser(parents=[parent_parser], add_help=False)
        parser.add_argument(
            "--batch_size",
            type=int,
            default=64,
            metavar="N",
            help="input batch size for training (default: 64)",
        )
        parser.add_argument(
            "--num_workers",
            type=int,
            default=3,
            metavar="N",
            help="number of workers (default: 3)",
        )
        parser.add_argument(
            "--lr",
            type=float,
            default=0.001,
            metavar="LR",
            help="learning rate (default: 0.001)",
        )
        return parser

    def forward(self, x):
        batch_size = x.size()[0]

        x = x.view(batch_size, -1)
        x = self.layer_1(x)
        x = torch.relu(x)
        x = self.layer_2(x)
        x = torch.relu(x)
        x = self.layer_3(x)
        x = torch.log_softmax(x, dim=1)

        return x

    def cross_entropy_loss(self, logits, labels):
        return F.nll_loss(logits, labels)

    def training_step(self, train_batch, batch_idx):
        x, y = train_batch
        logits = self.forward(x)
        loss = self.cross_entropy_loss(logits, y)
        return {"loss": loss}

    def validation_step(self, val_batch, batch_idx):
        x, y = val_batch
        logits = self.forward(x)
        loss = self.cross_entropy_loss(logits, y)
        return {"val_step_loss": loss}

    def validation_epoch_end(self, outputs):
        avg_loss = torch.stack([x["val_step_loss"] for x in outputs]).mean()
        self.log("val_loss", avg_loss, sync_dist=True)

    def test_step(self, test_batch, batch_idx):
        x, y = test_batch
        output = self.forward(x)
        _, y_hat = torch.max(output, dim=1)
        test_acc = accuracy(y_hat.cpu(), y.cpu())
        return {"test_acc": test_acc}

    def test_epoch_end(self, outputs):
        avg_test_acc = torch.stack([x["test_acc"] for x in outputs]).mean()
        self.log("avg_test_acc", avg_test_acc)

    def prepare_data(self):
        return {}

    def configure_optimizers(self):
        self.optimizer = torch.optim.Adam(self.parameters(), lr=self.args["lr"])
        self.scheduler = {
            "scheduler": torch.optim.lr_scheduler.ReduceLROnPlateau(
                self.optimizer,
                mode="min",
                factor=0.2,
                patience=2,
                min_lr=1e-6,
                verbose=True,
            ),
            "monitor": "val_loss",
        }
        return [self.optimizer], [self.scheduler]


def main():
    parser = ArgumentParser(description="PyTorch Autolog Mnist Example")
    parser.add_argument(
        "--es_monitor",
        type=str,
        default="val_loss",
        help="Early stopping monitor parameter",
    )
    parser.add_argument(
        "--es_mode",
        type=str,
        default="min",
        help="Early stopping mode parameter",
    )
    parser.add_argument(
        "--es_verbose",
        type=bool,
        default=True,
        help="Early stopping verbose parameter",
    )
    parser.add_argument(
        "--es_patience",
        type=int,
        default=3,
        help="Early stopping patience parameter",
    )

    parser = pl.Trainer.add_argparse_args(parent_parser=parser)
    parser = LightningMNISTClassifier.add_model_specific_args(parent_parser=parser)

    mlflow.pytorch.autolog()

    args = parser.parse_args()
    dict_args = vars(args)

    if "accelerator" in dict_args:
        if dict_args["accelerator"] == "None":
            dict_args["accelerator"] = None

    model = LightningMNISTClassifier(**dict_args)

    dm = MNISTDataModule(**dict_args)
    dm.prepare_data()
    dm.setup(stage="fit")

    early_stopping = EarlyStopping(
        monitor=dict_args["es_monitor"],
        mode=dict_args["es_mode"],
        verbose=dict_args["es_verbose"],
        patience=dict_args["es_patience"],
    )

    checkpoint_callback = ModelCheckpoint(
        filepath=os.getcwd(),
        save_top_k=1,
        verbose=True,
        monitor="val_loss",
        mode="min",
        prefix="",
    )
    lr_logger = LearningRateMonitor()

    trainer = pl.Trainer.from_argparse_args(
        args,
        callbacks=[lr_logger, early_stopping],
        checkpoint_callback=checkpoint_callback,
    )
    trainer.fit(model, dm)
    trainer.test()


if __name__ == "__main__":
    main()
