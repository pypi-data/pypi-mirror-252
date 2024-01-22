from ..interfaces import ConfigManagerInterface
from ..service import CONTEXT
from ..utils.yaml import YAMLFile


class ConfigManagerDefault(ConfigManagerInterface):

    def __init__(self):
        self.data_dir: str = None
        self.app_dir: str = None
        self.file_sep: str = None


    def load_yaml_files(self, filename, parent_yaml: YAMLFile = None ) -> YAMLFile:
        # load from app dir as default and then from data for exits
        def_filename    = f"{self.app_dir}{self.file_sep}cfg{self.file_sep}{filename}"
        yaml_default    = YAMLFile(def_filename)

        exit_filename   = f"{self.data_dir}{self.file_sep}cfg{self.file_sep}{filename}"
        yaml_exit       = YAMLFile(exit_filename)
        if yaml_exit.is_loaded():
            yaml_default.set_exit(yaml_exit)

        if parent_yaml:
            yaml_default.set_parent(parent_yaml)

        return yaml_default

    def startup(self) -> bool:
        # check
        self.data_dir = CONTEXT.get_service().get(CONTEXT.DATA_DIR)
        self.app_dir  = CONTEXT.get_service().get(CONTEXT.APP_DIR)
        self.file_sep = CONTEXT.get_service().get(CONTEXT.FILE_SEPARATOR)

        if not self.data_dir or not self.app_dir or not self.file_sep:
            self.get_logger().error("invalid context for ConfigManager: no app/data direction available")
            return False

        # load yaml files
        service_id = CONTEXT.get_service().get(CONTEXT.SERVICE_ID, "service")
        default = self.load_yaml_files("default.yml")
        server  = self.load_yaml_files("server.yml", parent_yaml=default)
        service = self.load_yaml_files(f"{service_id}.yml", parent_yaml=server)

        # check
        constants       = service.get_value_for_path("/Constants")
        runtime_mode    = service.get_value_for_path("/Constants/Service/Runtime_Mode")
        server          = service.get_value_for_path("/Constants/Service")

        # finally result
        return True

    def stop(self) -> bool:
        return True
    def get_config(self, key: str, default=None):
        return default
