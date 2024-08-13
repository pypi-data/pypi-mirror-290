from fastapi import APIRouter, Depends, FastAPI
from structlog import get_logger

from ngs_pipeline_lib.api.models import APISettings
from ngs_pipeline_lib.api.security import valid_access_token

logger = get_logger("ngs-api")
settings = APISettings()

app = FastAPI(
    docs_url=settings.prefix_path + "/docs", root_path=settings.root_path, logger=logger
)

public_router = APIRouter(prefix=settings.prefix_path)

if settings.secure:
    logger.info("Secured router with oAuth authentication enabled")
    private_router = APIRouter(
        prefix=settings.prefix_path, dependencies=[Depends(valid_access_token)]
    )
else:
    logger.info("No secured router, only public endpoints")
    private_router = APIRouter(prefix=settings.prefix_path)
