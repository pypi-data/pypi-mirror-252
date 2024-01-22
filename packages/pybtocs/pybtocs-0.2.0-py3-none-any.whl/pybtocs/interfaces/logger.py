class LoggerInterface:

    TYPE_ERROR = "E"
    TYPE_WARNING = "W"
    TYPE_TRACE = "T"
    TYPE_INFO = "I"

    def __init__(self, console: bool = True):
        self.console: bool = console

    def info(self, msg:str, *args):
        pass

    def error(self, msg:str, *args):
        pass

    def warning(self, msg:str, *args):
        pass

    def trace(self, msg:str, *args):
        pass

    def add_log(self, type:str, msg:str, *args):
        pass
    def get_logs(self) -> list:
        pass

    def get_count(self) -> int:
        pass

    def is_console(self) -> bool:
        return self.console