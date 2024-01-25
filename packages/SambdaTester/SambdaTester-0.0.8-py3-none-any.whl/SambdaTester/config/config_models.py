from pydantic import BaseModel
from pathlib import Path

class Config(BaseModel):
    """
    Configuration model class
    """
    
    TemplateName: str
    DirectoryPath: str
    Port: str | int
    MonitorLayers: bool
    Debug: bool
    Host: str