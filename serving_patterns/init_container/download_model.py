import os
import enum


class TARGET_CLOUD_ENUM(enum.Enum):
    AWS_S3 = "aws_s3"
    AZURE_BLOB = "azure_blob"
    GCS_BUCKET = "gcs_bucket"


TARGET_CLOUD = os.getenv("TARGET_CLOUD", "")
SHARED_DIRECTORY = os.getenv("SHARED_DIRECTORY", "/tmp/")
MODEL_FILENAME = os.getenv("MODEL_FILENAME", "model.onnx")


def download_from_aws_s3(
    shared_directory: str = SHARED_DIRECTORY,
    model_filename: str = MODEL_FILENAME,
    aws_url: str = os.getenv("AWS_URL"),
    aws_region: str = os.getenv("AWS_REGION"),
):
    import boto3

    if os.getenv("AWS_ACCESS_KEY_ID", "") == "" or os.getenv("AWS_SECRET", "") == "":
        raise RuntimeError("")
    s3_resource = boto3.resource("s3", region_name=aws_region)
    s3_resource.Bucket(aws_url).download_file(model_filename, shared_directory)


def download_from_azure_blob(shared_directory: str = SHARED_DIRECTORY, model_filename: str = MODEL_FILENAME):
    from azure.storage.blob import BlobServiceClient

    connect_str = os.getenv("CONNECT_STR", "")
    if connect_str == "":
        raise RuntimeError("")
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    filepath = os.path.join(shared_directory, model_filename)
    with open(filepath, "wb") as f:
        f.write(blob_service_client.download_blob().readall())


def download_from_gcs_bucket(shared_directory: str = SHARED_DIRECTORY, model_filename: str = MODEL_FILENAME, bucket_name: str = os.getenv("BUCKET_NAME")):
    from google.cloud import storage

    if os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "") == "":
        raise RuntimeError("")
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(model_filename)
    filepath = os.path.join(shared_directory, model_filename)
    blob.download_to_filename(filepath)


def main():
    if TARGET_CLOUD == TARGET_CLOUD_ENUM.AWS_S3.value:
        download_from_aws_s3(shared_directory=SHARED_DIRECTORY, model_filename=MODEL_FILENAME)

    elif TARGET_CLOUD == TARGET_CLOUD_ENUM.AZURE_BLOB.value:
        download_from_azure_blob(shared_directory=SHARED_DIRECTORY, model_filename=MODEL_FILENAME)

    elif TARGET_CLOUD == TARGET_CLOUD_ENUM.GCS_BUCKET.value:
        download_from_gcs_bucket(shared_directory=SHARED_DIRECTORY, model_filename=MODEL_FILENAME)

    else:
        raise ValueError("TARGET_CLOUD should be specified from TARGET_CLOUD_ENUM")


if __name__ == "__main__":
    main()
