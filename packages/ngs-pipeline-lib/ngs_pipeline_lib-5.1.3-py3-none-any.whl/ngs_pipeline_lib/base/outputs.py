from abc import ABCMeta
from logging import Logger
from pathlib import Path
from shutil import move

from ngs_pipeline_lib.base.file import File, OutputsFile
from ngs_pipeline_lib.tools.s3 import upload_file
from ngs_pipeline_lib.tools.tools import gzip_file


class BaseOutputs(metaclass=ABCMeta):
    def __init__(self):
        self._outputs = OutputsFile()

    @property
    def files(self) -> list[File]:
        return [value for value in vars(self).values() if isinstance(value, File)]

    @property
    def files_path(self) -> list[str]:
        return [str(file.output_path) for file in self.files]

    def to_files(self):
        for file_ in self.files:
            file_.to_file()

    def compress_files(self, logger: Logger):
        for file_ in self.files:
            if file_.compress:
                logger.debug(f"Compressing file: {file_.path}")
                gzip_file(file_.path)
                logger.debug(f"Done compressing file: {file_.path}")
                file_.path.unlink()

    def publish_files(self, publish_dir: str, logger: Logger):
        for file_ in self.files:
            logger.debug(f"Publishing file: {file_.output_path}")
            if Path(publish_dir).exists():
                # -> publish_dir is created as a directory in the inputs validator
                # -> specifying the full destination file path will force overwrite
                #    if the file alredy exists
                destination_path = Path(publish_dir) / file_.output_path.name
                move(file_.output_path, destination_path)
            else:
                upload_file(file_.output_path, publish_dir)
                file_.output_path.unlink()
            logger.debug(f"Done publishing file: {file_.output_path}")
