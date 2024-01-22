from ..interfaces import ManagerInstanceInterface, SingletonManagerClassInterface

class ServiceManagerInterface(ManagerInstanceInterface):

    def initialize(self) -> bool:
        pass

    def startup(self) -> bool:
        pass

    def stop(self) -> bool:
        pass

    def cleanup(self) -> bool:
        pass

    def init_managers(self, description: str, managers: list[SingletonManagerClassInterface]) -> bool:
        pass

    def start_managers(self, description: str, managers: list[SingletonManagerClassInterface]) -> bool:
        pass

    def stop_managers(self, description: str, managers: list[SingletonManagerClassInterface]) -> bool:
        pass

    def get_app_dir(self, append_path: str = None, check_and_create: bool = False) -> str:
        pass

    def get_data_dir(self, append_path: str = None, check_and_create: bool = False) -> str:
        pass
