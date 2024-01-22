from ..interfaces import FileStorageManagerInterface

class FileStorageManagerDefault(FileStorageManagerInterface):

    def startup(self) -> bool:
        return True

    def stop(self) -> bool:
        return True
