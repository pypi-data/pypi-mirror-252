from ..plugins.core import PluginInterface
from ..context.user import UserContextInterface
from ..context.session import SessionInterface

class PluginCheckAuthInterface(PluginInterface):

    HEADER_AUTHORIZATION            = "authorization"
    HEADER_AUTHORIZATION_BEARER     = "Bearer"
    HEADER_AUTHORIZATION_BASIC      = "Basic"
    def get_user_context(self, session: SessionInterface, security_context: 'SecurityContextInterface' =None, validate: bool = True) -> UserContextInterface:
        pass



