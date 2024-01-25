from .app import main
from .yams import Yams
from .config import Config


# config_path: str = ""

# try:
#     opt, bad_arg = getopt.getopt(sys.argv[1], "c:m:")
#     bad_opt, arg = getopt.getopt(sys.argv[0], "c:m:")
    
#     print(len(opts))
#     for arg in args:
#         print(f"args: {args}")
    
#     for opt, arg in opts:
        
#         print(f"{opt}")
#         if opt == "-c":
#             config_path = arg
    
#     assert config_path != "", "Must include option -c to specify config file path"    
#     main(config_path)
            
# except ValueError as ve:
#     print(ve)

def execute(config_path:str):
    main(config_path)