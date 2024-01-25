from flask import Flask, request
from ..yams.yams import Yams
from ..config.config_models import Config
from ..yams.models.yaml_model import Lambda
from time import sleep

def create_server(config: Config, lambdas: dict[Lambda], layers: dict):
    app = Flask(__name__)
    
    extra_files = []

    def create_view(lam: object):
        module, func = lam.Handler.split(".")

        def internal_func():
            data = {"body": request.data.decode("utf-8")}
            # global to_reload
            # to_reload = True
            return getattr(lam.func, func)(event=data, context="")
            

        return internal_func

    for key, lam in lambdas.items():
        print(lam.Path)
        extra_files.append(lam.FullPath)
        
        app.add_url_rule(
            rule=lam.Path,
            methods=[lam.Method],
            endpoint=lam.FunctionName,
            view_func=create_view(lam),
        )
        

    app.run(extra_files=extra_files, host=config.Host, port=config.Port, debug=config.Debug)
    
