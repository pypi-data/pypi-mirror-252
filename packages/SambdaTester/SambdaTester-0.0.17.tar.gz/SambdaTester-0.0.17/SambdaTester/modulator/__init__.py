from .modulator import Modulator

def import_module(root_dir:str) -> Modulator:
    
    return Modulator(root_dir)