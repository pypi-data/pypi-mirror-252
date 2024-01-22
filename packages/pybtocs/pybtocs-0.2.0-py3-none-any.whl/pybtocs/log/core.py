import datetime
from ..interfaces import LoggerInterface

# class LoggerInterface:
#
#     TYPE_ERROR = "E"
#     TYPE_WARNING = "W"
#     TYPE_TRACE = "T"
#     TYPE_INFO = "I"
#
#     def __init__(self, console: bool = True):
#         self.console: bool = console
#
#     def info(self, msg:str, *args):
#         pass
#
#     def error(self, msg:str, *args):
#         pass
#
#     def warning(self, msg:str, *args):
#         pass
#
#     def trace(self, msg:str, *args):
#         pass
#
#     def add_log(self, type:str, msg:str, *args):
#         pass
#     def get_logs(self) -> list:
#         pass
#
#     def get_count(self) -> int:
#         pass
#
#     def is_console(self) -> bool:
#         return self.console

class DefaultLogger(LoggerInterface):

    def __init__(self, console: bool = True):
        super().__init__(console)
        self.logs = []

    def add_log(self, msg_type:str, msg:str, *args):
        log_tupel = (msg_type, datetime.datetime.now(), msg)
        self.logs.append(log_tupel)
        if self.is_console():
            print(f"{log_tupel[0]}: {log_tupel[1]} - {log_tupel[2]}")

    def get_logs(self) -> list:
        return self.logs

    def get_count(self) -> int:
        return len(self.logs)

    def error(self, msg:str, *args):
        self.add_log(LoggerInterface.TYPE_ERROR, msg, args)

    def info(self, msg:str, *args):
        self.add_log(LoggerInterface.TYPE_INFO, msg, args)

    def trace(self, msg:str, *args):
        self.add_log(LoggerInterface.TYPE_TRACE, msg, args)

    def warning(self, msg:str, *args):
        self.add_log(LoggerInterface.TYPE_WARNING, msg, args)
