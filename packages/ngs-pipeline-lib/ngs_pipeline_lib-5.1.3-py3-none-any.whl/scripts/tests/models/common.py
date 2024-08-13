from pathlib import Path

from pydantic import BaseModel


class ScenarioMetadata(BaseModel):
    name: str
    description: str
    path: Path
