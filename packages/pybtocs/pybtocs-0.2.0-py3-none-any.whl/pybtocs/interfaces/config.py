from ..interfaces import ManagerInstanceInterface
class ConfigManagerInterface(ManagerInstanceInterface):

    def get_config(self, key: str, default=None):
        pass