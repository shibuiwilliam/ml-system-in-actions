import os
from logging import DEBUG, Formatter, StreamHandler, getLogger

import click
from google.cloud import storage

logger = getLogger(__name__)
logger.setLevel(DEBUG)
strhd = StreamHandler()
strhd.setFormatter(Formatter("%(asctime)s %(levelname)8s %(message)s"))
logger.addHandler(strhd)


@click.command(name="model loader")
@click.option("--gcs_bucket", type=str, required=True, help="GCS bucket name")
@click.option("--gcs_model_blob", type=str, required=True, help="GCS model blob path")
@click.option("--model_filepath", type=str, required=True, help="Local model file path")
def main(gcs_bucket: str, gcs_model_blob: str, model_filepath: str):
    logger.info(f"download from gs://{gcs_bucket}/{gcs_model_blob}")
    dirname = os.path.dirname(model_filepath)
    os.makedirs(dirname, exist_ok=True)

    client = storage.Client.create_anonymous_client()
    bucket = client.bucket(gcs_bucket)
    blob = bucket.blob(gcs_model_blob)
    blob.download_to_filename(model_filepath)
    logger.info(f"download from gs://{gcs_bucket}/{gcs_model_blob} to {model_filepath}")


if __name__ == "__main__":
    main()
