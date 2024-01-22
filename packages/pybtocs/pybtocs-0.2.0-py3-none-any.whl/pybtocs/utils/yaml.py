import yaml
import os
from ..log import LoggerManager, LoggerInterface

class YAMLFileInterface:
    pass
class YAMLFile(YAMLFileInterface):

    SEPARATOR = "/"
    def __init__(self, filename: str = None):
        self.data: dict = None
        self.filename: str = None
        self.logger = LoggerManager.get("yaml")
        self.exit: YAMLFile = None
        self.parent: YAMLFile = None

        if filename:
            self.load_file(filename)


    def get_logger(self) -> LoggerInterface:
        return self.logger

    def is_loaded(self) -> bool:
        if self.filename:
            return True
        else:
            return False

    def is_empty(self) -> bool:
        if not self.data or len(self.data) == 0:
            return True
        else:
            return False

    def set_exit(self, yamlfile: YAMLFileInterface):
        self.exit = yamlfile

    def set_parent(self, yamlfile: YAMLFileInterface):
        self.parent = yamlfile

    def load_file(self, filename:str) -> bool:
        try:
            # check existence
            if not os.path.isfile(filename):
                return False
            # load now
            with open(filename, 'r') as file:
                self.data = yaml.safe_load(file)

            self.get_logger().trace(f"yaml file loaded: {filename}")
            self.filename = filename
            return True
        except Exception as exc:
            self.get_logger().error(f"error while reading yaml file: {exc}")
            return False

    def get_node_for_path(self, path: str, node=None):
        # check root node
        base = node
        if not node:
            base = self.data

        # no root node or no data
        if not base:
            return None

        # no path
        if len(path) == 0 or path == self.SEPARATOR:
            return base

        # check separator at first
        if path.startswith(self.SEPARATOR):
            path = path[1:]

        # check separator
        offset = path.find(self.SEPARATOR)
        current_path = path
        deeper_path = None

        if offset > 0:
            current_path = path[0:offset-1]
            deeper_path  = path[offset+1:]

        # check current available
        if not current_path in base.keys():
            return None
        else:
            node = base.get(current_path)
            if not deeper_path:
                return node
            else:
                return self.get_node_for_path(deeper_path, node)
    def get_value_for_path(self, path: str, check_parent:bool=True):
        node = self.get_node_for_path(path)
        if not node and check_parent and self.parent:
            return self.parent.get_value_for_path(path)
        return node


