from ..context.core import ContextValues


class CONTEXT:

    SERVICE_ID = "SERVICE_ID"
    PLATFORM = "PLATFORM"
    FILE_SEPARATOR = "FILE_SEPARATOR"
    RUNTIME_PATH = "RUNTIME_PATH"
    APP_DIR = "APP_DIR"
    DATA_DIR = "DATA_DIR"

    _service = ContextValues()
    _server  = ContextValues()

    @classmethod
    def get_server(cls) -> ContextValues:
        return cls._server

    @classmethod
    def get_service(cls) -> ContextValues:
        return cls._server
