from pydantic import BaseModel, Field
from pathlib import Path

class Lambda(BaseModel):
    FunctionName: str
    CodeUri: str
    Path: str
    FullPath: Path = Field(default_factory=lambda: None)
    Method: str
    Handler: str
    func: object = Field(default_factory=lambda: None)
    spec: object = Field(default_factory=lambda: None)