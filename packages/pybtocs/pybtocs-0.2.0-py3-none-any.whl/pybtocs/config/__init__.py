from ..interfaces import SingletonManagerClassInterface, ConfigManagerInterface
from .core import ConfigManagerDefault

class ConfigManager(SingletonManagerClassInterface):

    _description = "ConfigManager"

    @classmethod
    def get(cls):
        if not cls._instance:
            cls._instance = ConfigManagerDefault()
        return super().get()

    @classmethod
    def get_manager(cls) -> ConfigManagerInterface:
        return cls.get()
