from ..log import LoggerManager
from ..security.plugins import PluginCheckAuthInterface
from ..plugins import PluginManager
from ..context.user import UserContext, UserContextAnonymous, UserContextInterface
from ..context.session import SessionInterface
class SecurityContextInterface:

    def __init__(self, account: str = None, tenant: str = None):
        pass
    def get_user_context(self) -> UserContextInterface:
        pass

    def get_secret(self) -> str:
        pass

    def is_role_available(self, session: SessionInterface, user_context: UserContextInterface, required_role: str = None) -> bool:
        pass

    def is_authorized(self, session: SessionInterface, required_role: str = None, set_anonymous:bool=False) -> bool:
        pass

    def get_valid_auth_plugins(self) -> list:
        pass

    def get_invalid_auth_plugins(self) -> list:
        pass
class SecurityContext:

    def __init__(self, account: str = None, tenant: str = None):
        self.tenant = tenant
        self.account = account
        self.user_context: UserContext = None
        self.secret = None

    def get_user_context(self) -> UserContext:
        return self.user_context

    def get_secret(self) -> str:
        return self.secret

    def is_role_available(self, session: SessionInterface, user_context: UserContextInterface, required_role: str = None) -> bool:
        return True

    def is_authorized(self, session: SessionInterface, required_role: str = None, set_anonymous:bool=False) -> bool:
        # init
        self.user_context = None
        if set_anonymous:
            self.user_context = UserContextAnonymous()


        # get valid plugins
        valid_plugins = self.get_valid_auth_plugins()
        invalid_plugins = self.get_invalid_auth_plugins()

        plugins: list[PluginCheckAuthInterface] = []
        plugins = PluginManager.get_plugins(PluginCheckAuthInterface, valid_plugins)
        if not plugins or len(plugins) == 0:
            session.get_logger().error("no valid auth plugins found")
            return False

        # check user context in all valid plugins
        for plugin in plugins:
            # prepare
            plugin_id = plugin.get_id()

            if not plugin_id:
                session.get_logger().error(f"Plugin has no id: {plugin}. Skipped.")
                continue

            # check invalid
            if invalid_plugins and len(invalid_plugins) > 0:
                if plugin_id in invalid_plugins:
                    session.get_logger().error(f"Server plugin {plugin_id} skipped.")
                    continue

            # check valid
            if valid_plugins and len(valid_plugins) > 0:
                if not plugin_id in valid_plugins:
                    session.get_logger().error(f"Plugin not in allowed list: {plugin}. Skipped.")
                    continue

            # check first user context
            user_context = plugin.get_user_context(session=session, security_context=self, validate=True)
            if user_context:
                self.user_context = user_context

                # check user context is valid
                if user_context.is_valid():
                    # check authorization
                    if not required_role:
                        return True
                    else:
                        if self.is_role_available(session=session, user_context=user_context, required_role=required_role):
                            return True
                        else:
                            session.get_logger().error(f"user with invalid authirizations found (required role '{required_role}' and other grants missing)")

        # errors
        if self.user_context:
            session.get_logger().error("user with invalid authentification found")
        else:
            session.get_logger().error("no valid authentification found")

        return False


    def get_valid_auth_plugins(self) -> list:
        return []

    def get_invalid_auth_plugins(self) -> list:
        return []

class SecurityContextPublic(SecurityContext):
    pass


class SecurityContextServer(SecurityContext):
    pass


class SecurityContextService(SecurityContext):
    def get_secret(self) -> str:
        return 'my_super_secret_token'


class SecurityContextAccount(SecurityContext):
    pass

class SecurityContextForbidden(SecurityContext):
    pass

class SecurityContextTenant(SecurityContext):
    pass


