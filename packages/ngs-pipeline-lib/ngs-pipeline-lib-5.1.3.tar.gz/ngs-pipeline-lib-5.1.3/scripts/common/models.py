from pathlib import Path

from pydantic import BaseSettings


class LogBaseSettings(BaseSettings):
    verbose: bool = False
    json_logger: bool = False
    log_file: Path = None


class RunSettings(LogBaseSettings):
    process_package: str = "src"
