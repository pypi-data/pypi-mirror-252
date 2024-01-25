import os
import json
from dotenv import load_dotenv
from enum import Enum
from pathlib import Path
from .config_models import Config

class EnvironmentType(Enum):
    Dev = 0,
    Test = 1,
    Prod = 2,

class Configurator(object):
    
    # Constants to find default AWS Sam template
    _default_template_name:str = "template"
    _four_char_ext: str = "yaml"
    _three_char_ext: str = "yml"
    
    Environment: EnvironmentType = EnvironmentType.Prod
    Config: Config
    
    def __init__(self, dev_mode: bool = False, config_path: str | None = None):        
        file_path: str | None = None
        
        if dev_mode: 
            file_path = r"D:\WorkTools\SambdaTester\resources\config.json"        
        if config_path is not None:
            file_path = config_path

        if file_path is not None:
            file = Path(file_path).open()
            
            config_data = json.load(file)
            assert config_data is not None, f"Error loading configuration file at path [{config_path}]"
            self.Config = Config(**config_data)
        else:
            self.__get_directory_info()
    
    def __get_directory_info(self):
        templatePath: Path | None = None
        
        work_dir_path = os.getcwd()
        work_dir = Path(work_dir_path)
        assert work_dir.is_dir(), "Error: Path needs to be working directory"
        
        # Looks for the template file 
        for file in work_dir.iterdir():
            if not file.is_file(): continue
            
            if file.suffix == self._three_char_ext or file.suffix == self._four_char_ext and file.stem == f"{self._default_template_name}":
                templatePath = file
                break
        
        assert templatePath != None, "Error: template"
        
        self.Config = Config()
        self.Config.TemplateName = templatePath.name
        self.Config.DirectoryPath = work_dir_path
        
            
        
            
            
        
        
        
        
        
            
        