from pathlib import Path
import os
import yaml

from ..config.config import EnvironmentType
from ..config.config_models import Config
from .models.yaml_model import Lambda

class Yams(object):
    """
    Class that parses and represents the AWS Sam template file
    """
    ConfigObj: Config
    Lambdas: dict = {}
    Layers: dict = {}
    
    def __init__(self, config: Config) -> None:
        """
        Constructor for Yams class

        Args:
            work_dir_path (str): path to input file, if none is provided this will default to the users working directory.
            config (Config): Configuration object of application
        """
        
        # Sets the configuration object that is referenced when parsing the template
        self.ConfigObj = config
    
    def parse_file(self):
        if os.environ.get("ENV") != EnvironmentType.Prod:
            print(f"FileName: {self.ConfigObj}")
            
        full_path = Path(self.ConfigObj.DirectoryPath).joinpath(self.ConfigObj.TemplateName)
            
        with open(full_path, "r") as file:
            yaml.add_multi_constructor("!", self.__build_loader)
            yaml.add_multi_constructor("Ref:", self.__build_loader)
            
            docs = yaml.load_all(file, Loader=yaml.FullLoader)
        
            for doc in docs:
                global_section: dict
                globe_func: dict
                resources: dict = doc["Resources"]
                handler: str = ""
                
                if "Globals" in doc:
                    global_section = doc["Globals"]
                    
                    if "Function" in global_section:
                        globe_func = global_section["Function"]
                        
                        if "Handler" in globe_func:
                            handler = globe_func["Handler"]
                
                for key, aws_lambda in resources.items():
                    if aws_lambda["Type"] == "AWS::Serverless::LayerVersion":
                        if "Properties" in aws_lambda:
                            props = aws_lambda["Properties"]
                            self.Layers[key] = props["ContentUri"]
                    
                    if aws_lambda["Type"] == "AWS::Serverless::Function":
                        props = aws_lambda["Properties"]

                        if "Events" in props:
                            api_events = {event_key:val for event_key,val in props["Events"].items() if val["Type"] == "Api"}
                            for e_key, event in api_events.items():
                                api_props = event["Properties"]
                                elements = {k:api_props[k] for k in api_props if k !="RestApiId" and k !="Auth"}
                                
                                name: str = props["FunctionName"]
                                elements["FunctionName"] = name
                                code_uri: str = props["CodeUri"]
                                elements["CodeUri"] = code_uri
                                
                                if handler == "" and "Handler" in props:
                                    handler = props["Handler"]
                                
                                assert handler != "", f"Error retrieving handler from lambda {key}"
                                
                                elements["Handler"] = handler
                                
                                self.Lambdas[name] = Lambda(**elements)    
            
    def __build_loader(self, loader, suffix, node):
        if isinstance(node, yaml.ScalarNode):
            constructor = loader.__class__.construct_scalar
        elif isinstance(node, yaml.SequenceNode):
            constructor = loader.__class__.construct_sequence
        elif isinstance(node, yaml.MappingNode):
            constructor = loader.__class__.construct_mapping

        data = constructor(loader, node)
        
        return data
        
        
        