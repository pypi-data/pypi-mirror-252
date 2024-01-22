from ..interfaces import ServiceManagerInterface, SingletonManagerClassInterface, LoggerInterface
from ..plugins import PluginManager
from ..security import SecurityManager
from ..log import LoggerManager
from ..storage import FileStorageManager
from ..config import ConfigManager
from ..utils import UtilsManager
from .context import CONTEXT

import os

class ServiceManagerDefault(ServiceManagerInterface):

    SERVICE_MANAGER_NAME = 'B-Tocs Service Manager'




    def __init__(self):
        self._manager_utils: list[SingletonManagerClassInterface] = []
        self._manager_core: list[SingletonManagerClassInterface] = []
        self._manager_services: list[SingletonManagerClassInterface] = []
        self._logger = LoggerManager.get("service")
        self._initialized: bool = False
        self._runtime_path = os.getcwd()
        self._root_path: str = None
        self._app_dir : str = None
        self._data_dir: str = None
        self._plattform: str = 'linux'
        self._file_sep: str = '/'

    def get_logger(self) -> LoggerInterface:
        return self._logger

    def initialize_before_layers(self) -> bool:
        # current status
        path = self._runtime_path
        len_path = len(path)
        self.get_logger().info(f"Starting path: {path}")

        # check path
        if path == '/app' or len_path < 3:
            self._root_path = '/'
            self._app_dir   = '/app'
            self._data_dir  = '/data'
        else:
            # check for windows plattform
            if path.find("\\") > 0:
                self._plattform = 'windows'
                self._file_sep  = "\\"
                self.get_logger().info("Windows platform found")

            # check for src folder
            offset_src = path.find("src")
            if offset_src > 0:
                path = path[0:offset_src]
                path = f"{path}files"
            else:
                # check for files
                offset_files = path.find("files")
                if offset_files < 0:
                    self.get_logger().error("Developer path found but no files directory. Leave startup.")
                    return False
                else:
                    path = path[0: offset_files+5]

            # build developer files structure
            self._root_path = path
            self._app_dir   = self._root_path + self._file_sep + 'app'
            self._data_dir   = self._root_path + self._file_sep + 'data'

            CONTEXT.get_service().set(CONTEXT.PLATFORM, self._plattform)
            CONTEXT.get_service().set(CONTEXT.FILE_SEPARATOR, self._file_sep)
            CONTEXT.get_service().set(CONTEXT.APP_DIR, self._app_dir)
            CONTEXT.get_service().set(CONTEXT.DATA_DIR, self._data_dir)


        self.get_logger().info(f"Root path: {self._root_path}")
        self.get_logger().info(f"App directory: {self._app_dir}")
        self.get_logger().info(f"Data directory: {self._data_dir}")

        return True

    def initialize_after_layers(self) -> bool:
        return True


    def initialize(self) -> bool:
        # check
        if self._initialized:
            self.get_logger().error("ServiceManager initialized already")
            return False

        # init before layers
        if not self.initialize_before_layers():
            self.get_logger().error("ServiceManager initializing failed in before layers")
            return False

        # prepare utils
        self._manager_utils.append(UtilsManager)

        # prepare core services
        self._manager_core.append(FileStorageManager)
        self._manager_core.append(ConfigManager)

        # prepare other services

        # init after layers
        if not self.initialize_after_layers():
            self.get_logger().error("ServiceManager initializing failed in after layers")
            return False


        self._initialized = True
        return True


    def cleanup(self) -> bool:
        self._manager_utils: []
        self._manager_core: []
        self._manager_services: []
        self._initialized = False
        return True


    def start_managers(self, description: str, managers: list[SingletonManagerClassInterface]) -> bool:
        result = True
        try:
            if not managers or len(managers) == 0:
                self.get_logger().info(f"Starting managers: {description} - nothing to do")
            else:
                count = len(managers)
                self.get_logger().info(f"Starting {count} managers: {description}")
                # init
                for manager in managers:
                    if not manager.startup():
                        result = False
                        self.get_logger().error(f"Startup of manager {manager} failed")
                    else:
                        self.get_logger().info(f"Manager {manager} started")

            return result
        except Exception as exc:
            self.get_logger(f"Exception {exc} occured while starting managers")
            return False

    def stop_managers(self, description: str, managers: list[SingletonManagerClassInterface]) -> bool:
        result = True
        try:
            if not managers or len(managers) == 0:
                self.get_logger().info(f"Stop managers: {description} - nothing to do")
            else:
                count = len(managers)
                self.get_logger().info(f"Stopping {count} managers: {description}")
                for idx in range(count - 1, 0, -1):
                    manager = managers[idx]
                    if not manager.stop():
                        result = False
                        self.get_logger().error(f"Stopping of manager {manager} failed")
                    else:
                        self.get_logger().info(f"Manager {manager} stopped")

            return result
        except Exception as exc:
            self.get_logger(f"Exception {exc} occured while stopping managers")
            return False

    def startup(self):
        try:
            # prepare
            result = True
            self.get_logger().info(f"{self.SERVICE_MANAGER_NAME} startup...")

            # initialize
            if not self._initialized:
                self.initialize()

            # startup managers in groups
            if not self.start_managers("Utils", self._manager_utils):
                result = False
            if not self.start_managers("Core Services", self._manager_core):
                result = False
            if not self.start_managers("Services", self._manager_services):
                result = False

            if not result:
                self.get_logger().error(f"Starting {self.SERVICE_MANAGER_NAME} failed")
            else:
                self.get_logger().info(f"{self.SERVICE_MANAGER_NAME} started")
        except Exception as exc:
            self.get_logger().error(f"Exception {exc} while starting {self.SERVICE_MANAGER_NAME}")
            return None

    def stop(self):
        try:
            # prepare
            result = True
            self.get_logger().info(f"Stopping {self.SERVICE_MANAGER_NAME}...")

            # startup managers in groups
            if not self.stop_managers("Services", self._manager_services):
                result = False
            if not self.stop_managers("Core Services", self._manager_core):
                result = False
            if not self.stop_managers("Utils", self._manager_utils):
                result = False

            if not result:
                self.get_logger().error(f"Stopping {self.SERVICE_MANAGER_NAME} failed")
            else:
                self.get_logger().info(f"{self.SERVICE_MANAGER_NAME} stopped")

            # cleanup and return
            self.cleanup()
            return result
        except Exception as exc:
            self.get_logger().error(f"Exception {exc} while stopping {self.SERVICE_MANAGER_NAME}")
            return None

    def check_append_path(self, append_path: str) -> str:
        return append_path

    def check_and_create_path(self, path: str) -> bool:
        return True

    def get_app_dir(self, append_path: str = None, check_and_create: bool = False) -> str:
        result = self._app_dir
        if append_path:
            checked = self.check_append_path(append_path)
            result = f"{result}{self._file_sep}{checked}"

        if check_and_create:
            check_and_create(result)

        return result

    def get_data_dir(self, append_path: str = None, check_and_create: bool = False) -> str:
        result = self._data_dir
        if append_path:
            checked = self.check_append_path(append_path)
            result = f"{result}{self._file_sep}{checked}"

        if check_and_create:
            check_and_create(result)

        return result
