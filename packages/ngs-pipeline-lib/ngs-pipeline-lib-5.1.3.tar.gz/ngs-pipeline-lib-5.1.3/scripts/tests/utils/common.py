import hashlib
import json
import os
import shutil
from contextlib import contextmanager
from pathlib import Path

import boto3
import structlog
from pgzip import open as pgzip_open

from ngs_pipeline_lib.tools.s3 import S3Url

logger = structlog.getLogger("ngs-test")


def download_s3_file(
    url: str, destination_folder: Path, destination_filename: str = None
) -> None:
    """
    Download a file from S3 into a local folder
    Use `destination_filename` to rename the file to download.
    """
    destination_folder.mkdir(parents=True, exist_ok=True)

    s3_url = S3Url(url)
    s3_client = boto3.client("s3")

    if not destination_filename:
        destination_filename = s3_url.key[s3_url.key.rfind("/") + 1 :]

    s3_client.download_file(
        s3_url.bucket,
        s3_url.key,
        destination_folder / destination_filename,
    )


def list_outputs_from_s3(url: S3Url) -> list[S3Url]:
    """
    Return all outputs.json S3 URL within all subfolder of a S3 folder
    """
    s3_resource = boto3.resource("s3")
    bucket = s3_resource.Bucket(url.bucket)

    files = []

    for obj in bucket.objects.filter(Prefix=url.key):
        # Ignoring root element and subfolder elements
        if not obj.key.endswith("outputs.json"):
            continue

        files.append(S3Url.from_bucket_key(bucket=obj.bucket, key=obj.key))

    return files


def get_json_content_from_s3_file(url: S3Url) -> dict:
    """
    Open json file from S3 and return its content as a dict
    """
    s3 = boto3.client("s3")

    obj = s3.get_object(Bucket=url.bucket, Key=url.key)
    data = obj["Body"].read()

    return json.loads(data)


def download_s3_folder(url: str, destination_folder: Path):
    """
    Download a folder and all its content (files and subfolder) into a local folder
    """
    destination_folder.mkdir(parents=True, exist_ok=True)
    s3_url = S3Url(url)
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


def list_outputs_from_local_folder(local_path: Path) -> list[Path]:
    """
    Return all outputs.json files in a given Path and its subfolders
    """
    sub_paths = local_path.iterdir()
    for path in sub_paths:
        if (path.is_file() or path.is_symlink()) and path.name == "outputs.json":
            yield path
        elif path.is_dir():
            yield from list_outputs_from_local_folder(path)


def get_json_content_from_local_file(file_path: Path) -> dict:
    """
    Open local json file and return its content as a dict
    """
    with open(file=file_path, mode="rt", encoding="utf-8") as reader:
        json_content = json.load(reader)
    return json_content


@contextmanager
def get_file_content(file: Path, mode: str = "rb", encoding=None):
    """
    Utility method to provid a file handler wether it's gzipped or not
    """
    if file.suffix == ".gz":
        with pgzip_open(file, mode=mode, encoding=encoding) as f:
            yield f

    else:
        with open(file, mode=mode, encoding=encoding) as f:
            yield f


def get_json_file_content(file: Path) -> dict:
    """
    Open a JSON file and return the corresponding dict object
    The JSON file can be a gzipped one.
    """
    output_dict = {}

    with get_file_content(file=file, mode="rt", encoding="utf-8") as f:
        output_dict = json.load(f)

    return output_dict


def hash_file(filepath: Path) -> str:
    """
    Returns the SHA-1 hash of the file passed as argument.
    """

    # make a hash object
    h = hashlib.sha1()

    # open file for reading in binary mode
    with get_file_content(file=filepath) as file:
        # loop till the end of the file
        chunk = 0
        while chunk != b"":
            # read only 1024 bytes at a time
            chunk = file.read(1024)
            h.update(chunk)

    # return the hex representation of digest
    return h.hexdigest()


def clean_files(path: Path):
    """
    Iterate on all subfolders, files and link within the specified path
    And remove them.
    """
    logger.debug(f"Cleaning files and subfolders in {path}")
    paths_to_clean = path.iterdir()
    for path in paths_to_clean:
        if path.is_file() or path.is_symlink():
            os.unlink(path)
        elif path.is_dir():
            shutil.rmtree(path)
