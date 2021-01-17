import csv
import json
import time
from logging import DEBUG, Formatter, StreamHandler, getLogger

import click
import requests

logger = getLogger(__name__)
logger.setLevel(DEBUG)
formatter = Formatter("[%(asctime)s] [%(process)d] [%(name)s] [%(levelname)s] %(message)s")

handler = StreamHandler()
handler.setLevel(DEBUG)
handler.setFormatter(formatter)
logger.addHandler(handler)


def read_csv(data_file: str):
    with open(data_file, "r") as f:
        reader = csv.reader(f)
        data = [[float(r) for r in row] for row in reader]
    return data


@click.command(name="request job")
@click.option("--data_file", type=str, default="job/rand_iris.csv")
@click.option("--rate_per_second", type=int, default=10)
@click.option("--target_url", type=str, default="http://localhost:8000/predict")
def main(data_file: str, rate_per_second: int, target_url: str):
    logger.info("starting job...")
    time.sleep(30)
    data = read_csv(data_file)
    interval_second = 1 / rate_per_second
    while True:
        for d in data:
            logger.info(f"request: {d}")
            data_json = json.dumps({"data": [d]})
            headers = {"Content-Type": "application/json", "accept": "application/json"}
            response = requests.post(target_url, data_json, headers=headers)
            logger.info(f"response: {response.json()}")
            time.sleep(interval_second)


if __name__ == "__main__":
    main()
