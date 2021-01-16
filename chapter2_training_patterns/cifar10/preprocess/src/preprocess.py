import argparse
import json
import logging
import os
from distutils.dir_util import copy_tree

import torch
import torchvision
import torchvision.transforms as transforms
import mlflow

from src.configurations import PreprocessConfigurations, PlatformConfigurations
from src.extract_data import parse_pickle, unpickle

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_raw_data(downstream_directory: str):
    torchvision.datasets.CIFAR10(root=downstream_directory, train=True, download=True)
    torchvision.datasets.CIFAR10(root=downstream_directory, train=False, download=True)


def main():
    parser = argparse.ArgumentParser(description="Make dataset", formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument(
        "--data",
        type=str,
        default="cifar10",
        help="cifar10 or cifar100; default cifar10",
    )
    parser.add_argument(
        "--downstream",
        type=str,
        default="/opt/cifar10/preprocess/",
        help="downstream directory",
    )
    parser.add_argument(
        "--cached_data_id",
        type=str,
        default="",
        help="previous run id for cache",
    )
    args = parser.parse_args()

    downstream_directory = args.downstream

    if args.cached_data_id:
        cached_artifact_directory = os.path.join("/tmp/mlruns/0", args.cached_data_id, "artifacts/downstream_directory")
        copy_tree(cached_artifact_directory, downstream_directory)
    else:
        train_output_destination = os.path.join(downstream_directory, "train")
        test_output_destination = os.path.join(downstream_directory, "test")
        cifar10_directory = os.path.join(downstream_directory, "cifar-10-batches-py")

        os.makedirs(downstream_directory, exist_ok=True)
        os.makedirs(train_output_destination, exist_ok=True)
        os.makedirs(test_output_destination, exist_ok=True)
        os.makedirs(cifar10_directory, exist_ok=True)

        get_raw_data(downstream_directory=downstream_directory)

        meta_train = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: []}
        meta_test = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: []}

        for f in PreprocessConfigurations.train_files:
            rawdata = unpickle(file=os.path.join(cifar10_directory, f))
            class_to_filename = parse_pickle(rawdata=rawdata, rootdir=train_output_destination)
            for cf in class_to_filename:
                meta_train[int(cf[0])].append(cf[1])

        for f in PreprocessConfigurations.test_files:
            rawdata = unpickle(file=os.path.join(cifar10_directory, f))
            class_to_filename = parse_pickle(rawdata=rawdata, rootdir=test_output_destination)
            for cf in class_to_filename:
                meta_test[int(cf[0])].append(cf[1])

        classes_filepath = os.path.join(downstream_directory, "classes.json")
        meta_train_filepath = os.path.join(downstream_directory, "meta_train.json")
        meta_test_filepath = os.path.join(downstream_directory, "meta_test.json")
        with open(classes_filepath, "w") as f:
            json.dump(PreprocessConfigurations.classes, f)
        with open(meta_train_filepath, "w") as f:
            json.dump(meta_train, f)
        with open(meta_test_filepath, "w") as f:
            json.dump(meta_test, f)

    mlflow.log_artifacts(downstream_directory, artifact_path="downstream_directory")


if __name__ == "__main__":
    main()