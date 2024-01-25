from pathlib import Path
from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass


class DirObj(BaseModel):
    """
    Model for the root directory object
    """

    dir_path: Path 
    dir_children: list = Field(default_factory=list)
    modules: dict[str, object] = Field(default_factory=dict)
    
    def add_child(self, child_dir: object):
        self.dir_children.append(child_dir)
    