from ..interfaces import UtilsManagerInterface

class UtilsManagerDefault(UtilsManagerInterface):

    def startup(self) -> bool:
        return True

    def stop(self) -> bool:
        return True