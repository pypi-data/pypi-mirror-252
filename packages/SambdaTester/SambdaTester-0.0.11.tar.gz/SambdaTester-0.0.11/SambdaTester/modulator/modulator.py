from .models import DirObj
from pathlib import Path
from importlib.util import spec_from_file_location, module_from_spec
import sys


class Modulator:
    """
    Builds and imports modules into current application
    """

    def build_modules_from_dir(self, dir_path: Path):
        dir = DirObj(dir_path=dir_path, dir_children=[], modules={})
        self.__build_nodes(dir)
        self.__parse_nodes(dir)

    def build_modules_from_file(self, file_path: Path, func_name: str):
        return self.__import_module(file_path)

    def __build_nodes(self, parent_dir: DirObj):
        print("Building Nodes...")
        dem_strs = parent_dir.dir_path.glob("*")

        for item_path in dem_strs:
            if "__" in item_path.name:
                continue
            print(f"layer_item: {item_path}")

            if item_path.suffix == ".py" and item_path.name != "__init__.py":
                print(
                    f"Added module: {item_path.name} to node: {parent_dir.dir_path.name}"
                )
                parent_dir.modules[item_path.stem] = item_path

            elif item_path.is_dir():
                print(f"is Directory: {item_path}")
                child_dir = DirObj(dir_path=item_path)
                parent_dir.add_child(child_dir)
                self.__build_nodes(child_dir)

    def __parse_nodes(self, node: DirObj):
        print("Parsing Nodes...")

        if node.dir_children is not None and len(node.dir_children) > 0:
            print(f"{node.dir_path.name}: has children")
            for child in node.dir_children:
                if child.modules is not None and len(child.modules) > 0:
                    print(f"child dir: {child.dir_path.name}")
                    self.__parse_nodes(child)

        if node.modules is not None and len(node.modules) > 0:
            print(f"{node.dir_path.name}: has modules")
            for module in node.modules:
                self.__import_module(node.modules[module])

    def __import_module(self, path_str: str, func_name: str | None = None):
        module_path = Path(path_str)

        spec = spec_from_file_location(module_path.stem, module_path)
        func = module_from_spec(spec)
        
        if func_name is not None: 
            sys.modules[func_name] = func  
        else:
            sys.modules[module_path.stem] = func
        
        spec.loader.exec_module(func)

        return (spec, func)
