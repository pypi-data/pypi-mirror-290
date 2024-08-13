import os
from pathlib import Path
from urllib.parse import urlparse

import boto3

s3_profile = os.getenv("PROFILE")
if s3_profile:
    boto3.setup_default_session(profile_name=s3_profile)


def is_authentication_data_available():
    if s3_profile:
        return True
    else:
        aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        aws_session_token = os.getenv("AWS_SESSION_TOKEN")

        return aws_access_key and aws_secret_access_key and aws_session_token


class S3Url:
    def __init__(self, url: str):
        if not url.startswith("s3://"):
            raise ValueError("DownloadablePath: Only S3 URLs are supported")

        self._parsed = urlparse(url, allow_fragments=False)

        if not self.key:
            raise ValueError("No key provided in the S3 URL.")

    @property
    def bucket(self) -> str:
        return self._parsed.netloc

    @property
    def key(self) -> str:
        return self._parsed.path.lstrip("/")

    @property
    def url(self) -> str:
        return self._parsed.geturl()

    @property
    def is_file(self) -> bool:
        return not self.key.endswith("/")

    @property
    def is_dir(self) -> bool:
        return self.key.endswith("/")

    @property
    def filename(self) -> str:
        filename = self.key.split("/")[-1] if self.is_file else None
        return filename

    @property
    def dirname(self) -> str:
        foldername = self.key.split("/")[-2] if self.is_dir else None
        return foldername

    def download(self, base_folder: str) -> Path:
        if self.is_file:
            return download_s3_file(url=self.url, destination_folder=base_folder)
        else:
            return download_s3_folder(url=self.url, base_folder=base_folder)

    @classmethod
    def from_bucket_key(cls, bucket: str, key: str) -> "S3Url":
        str_url = f"s3://{bucket}/{key}"
        return cls(str_url)


def download_s3_file(
    url: str, destination_folder: Path, destination_filename: str = None
) -> Path:
    """
    Download a file from S3 into a local folder
    Use `destination_filename` to rename the file to download.
    """
    if not is_authentication_data_available():
        raise ValueError(
            f"No S3 Profile or ACCESS_KEYS available. Cannot download {url}"
        )

    destination_folder.mkdir(parents=True, exist_ok=True)

    s3_url = S3Url(url)
    s3_client = boto3.client("s3")

    if not destination_filename:
        destination_filename = s3_url.filename

    destination_file_path = destination_folder / destination_filename

    s3_client.download_file(
        s3_url.bucket,
        s3_url.key,
        destination_file_path,
    )

    return destination_file_path


def download_s3_folder(url: str, base_folder: Path) -> Path:
    """
    Download a folder and all its content (files and subfolder) into a local folder
    """
    if not is_authentication_data_available():
        raise ValueError(
            f"No S3 Profile or ACCESS_KEYS available. Cannot download {url}"
        )

    s3_url = S3Url(url)
    destination_folder = base_folder / s3_url.dirname
    destination_folder.mkdir(parents=True, exist_ok=True)
    s3_resource = boto3.resource("s3")
    bucket = s3_resource.Bucket(s3_url.bucket)

    for obj in bucket.objects.filter(Prefix=s3_url.key):
        relative_key = obj.key.removeprefix(s3_url.key).removeprefix("/")
        # Ignoring root element and subfolder elements
        if relative_key == "" or relative_key.endswith("/"):
            continue

        if (last_folder := relative_key.rfind("/")) > 0:
            subfolder = destination_folder / relative_key[:last_folder]
            subfolder.mkdir(parents=True, exist_ok=True)

        bucket.download_file(obj.key, destination_folder / relative_key)

    return destination_folder


def upload_file(path: Path, url: str) -> None:
    """
    Upload a local file to S3.
    If the url is an S3 directory, the local file name will be appended.
    """
    if not is_authentication_data_available():
        raise ValueError(
            f"No S3 Profile or ACCESS_KEYS available. Cannot upload {path} to {url}"
        )

    if url.endswith("/"):
        url += path.name
    s3_url = S3Url(url)

    s3_client = boto3.client("s3")
    s3_client.upload_file(path, s3_url.bucket, s3_url.key)
