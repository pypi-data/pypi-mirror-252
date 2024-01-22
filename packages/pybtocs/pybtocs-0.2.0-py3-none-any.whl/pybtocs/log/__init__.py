from pybtocs.log.core import DefaultLogger, LoggerInterface
class LoggerManager:

    _logger = {}

    @classmethod
    def new(cls) -> LoggerInterface:
        return DefaultLogger()


    @classmethod
    def get(cls, key: str) -> LoggerInterface:
        if key in cls._logger:
            return cls._logger.get(key)
        else:
            logger = cls.new()
            cls._logger[key] = logger
            return logger

    @classmethod
    def set(cls, key: str, logger: LoggerInterface):
        cls._logger[key] = logger
