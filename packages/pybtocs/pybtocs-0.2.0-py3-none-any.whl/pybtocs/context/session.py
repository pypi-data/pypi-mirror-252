import datetime
import uuid
from ..context.core import ContextValues
from ..log.core import DefaultLogger, LoggerInterface

class SessionInterface:
    TYPE_UNKNOWN: str = "unknown"
    TYPE_RESTAPI: str = "restapi"
    TYPE_CLI: str = "cli"

    def __init__(self):
        self.session_uuid: str = None
        self.session_type: str = None
        self.started_at = None
        self.finished_at = None
        self.headers: None
        self.parameters: None
        self.logger: None

    def get_uuid(self) -> str:
        pass
    def get_session_type(self) -> str:
        pass

    def finish(self, result, *args):
        pass

    def get_runtime(self):
        pass

    def get_parameters(self) -> ContextValues:
        pass

    def get_headers(self) -> ContextValues:
        pass

    def get_logger(self) -> LoggerInterface:
        pass

class DefaultSession(SessionInterface):
    def __init__(self, session_type: str = SessionInterface.TYPE_UNKNOWN):
        super().__init__()
        self.session_type = session_type
        self.session_uuid = str(uuid.uuid4())
        self.started_at = None
        self.finished_at = None
        self.headers: ContextValues = ContextValues()
        self.parameters: ContextValues = ContextValues()
        self.logger: LoggerInterface = DefaultLogger()


    def get_uuid(self) -> str:
        return self.session_uuid
    def get_session_type(self) -> str:
        return self.session_type

    def finish(self, result, *args):
        self.finished_at = datetime.datetime.now()

    def get_runtime(self):
        if self.started_at and self.finished_at:
            return self.finished_at - self.started_at

    def get_parameters(self) -> ContextValues:
        return self.parameters

    def get_headers(self) -> ContextValues:
        return self.headers

    def get_logger(self) -> LoggerInterface:
        return self.logger


class RestAPISession(DefaultSession):

    def __init__(self, api_method: str, access_level: int = 0, required_role: int = 0, tenant: str = None, account: str = None):
        super().__init__(session_type=SessionInterface.TYPE_RESTAPI)
        self.started_at = datetime.datetime.now()

        self.api_method = api_method
        self.access_level = access_level
        self.required_role = required_role
        self.tenant = tenant
        self.account = account


