from typing import List

from pydantic import BaseModel


class Config(BaseModel):
    language: str
    version: str
    codebase: str
    project_setup: List[str]
    name: str
