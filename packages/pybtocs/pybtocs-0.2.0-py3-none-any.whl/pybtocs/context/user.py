import datetime
import uuid
from ..context.core import ContextValues
from ..log.core import DefaultLogger, LoggerInterface

class UserContextInterface:

    SOURCE_LOCAL = "local"
    ROLES_ANONYMOUS = ["public"]

    def __init__(self, source: str, id:str, description: str, email:str=None, roles:list=[]):
        self.source = source
        self.id     = id
        self.description = description
        self.email = email
        self.roles:list=roles
        self.validated = False

    def is_valid(self) -> bool:
        pass


class UserContext(UserContextInterface, ContextValues):

    def __init__(self, source: str, id:str, description: str, email:str=None, roles:list=[]):
        self.source = source
        self.id     = id
        self.description = description
        self.email = email
        self.roles:list=roles
        self.validated = False

    def is_valid(self) -> bool:
        return self.validated
    def __init__(self, source: str, id: str, description: str, email: str = None, roles: list = []):
      super().__init__(source=source, id=id, description=description, email=email, roles=roles)

class UserContextAnonymous(UserContext):
    def __init__(self):
        super().__init__(source=UserContextInterface.SOURCE_LOCAL, id="anonymous", description="Anonymous", roles=UserContextInterface.ROLES_ANONYMOUS)
