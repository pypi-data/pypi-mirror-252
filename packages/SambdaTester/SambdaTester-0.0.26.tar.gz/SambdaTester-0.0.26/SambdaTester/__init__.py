from .app import main
from .yams import Yams
from .config import Config
import getopt
import sys



def execute():
    config_path: str = ""

    try:
        opts, args = getopt.getopt(sys.argv[1:], "c", ["config="])
        
        print(len(opts))
        for arg in args:
            print(f"args: {args}")
        
        for opt, arg in opts:
            
            print(f"opt: {opt}, arg: {arg}")
            if opt == "-c":
                config_path = args[0]
        
        assert config_path != "", "Must include option -c to specify config file path"    
        main(config_path)
                
    except ValueError as ve:
        print(ve)
    main(config_path)