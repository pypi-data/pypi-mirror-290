import importlib
import sys

import uvicorn

from ngs_pipeline_lib.api import app
from scripts import configure_logging
from scripts.common.models import RunSettings


def api():
    settings = RunSettings()
    configure_logging(
        verbose=settings.verbose,
        json=settings.json_logger,
        log_file_path=settings.log_file,
    )
    sys.path.insert(0, ".")
    importlib.import_module(f"{settings.process_package}.api", package=".")

    uvicorn.run(app)
