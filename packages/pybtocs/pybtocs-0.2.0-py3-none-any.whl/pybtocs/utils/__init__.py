from ..interfaces import SingletonManagerClassInterface, UtilsManagerInterface
from .core import UtilsManagerDefault

class UtilsManager(SingletonManagerClassInterface):

    _description = "UtilsManager"

    @classmethod
    def get(cls):
        if not cls._instance:
            cls._instance = UtilsManagerDefault()
        return super().get()

    @classmethod
    def get_manager(cls) -> UtilsManagerInterface:
        return cls.get()