from ..interfaces import SingletonManagerClassInterface, FileStorageManagerInterface
from .files import FileStorageManagerDefault

class FileStorageManager(SingletonManagerClassInterface):

    _description = "FileStorageManager"

    @classmethod
    def get(cls):
        if not cls._instance:
            cls._instance = FileStorageManagerDefault()
        return super().get()

    @classmethod
    def get_manager(cls) -> FileStorageManagerInterface:
        return cls.get()
