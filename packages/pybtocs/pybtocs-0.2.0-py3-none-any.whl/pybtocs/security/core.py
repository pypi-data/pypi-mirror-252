from .context import *
from ..plugins import PluginManager
from .auth.jwt import PluginCheckAuthJWT
from .auth.basic import PluginCheckAuthBasic
from .auth.api_token import PluginCheckAuthAPIToken




class SecurityManagerInterface:

    ACCESS_LAYER_PUBLIC:    str = "public"
    ACCESS_LAYER_SERVER:    str = "server"
    ACCESS_LAYER_SERVICE:   str = "service"
    ACCESS_LAYER_ACCOUNT:   str = "account"
    ACCESS_LAYER_TENANT:    str = "tenant"

    REQUIRED_ROLE_PUBLIC:   str = "public"
    REQUIRED_ROLE_USER:     str = "user"
    REQUIRED_ROLE_KEY_USER: str = "key_user"
    REQUIRED_ROLE_EXT_USER: str = "ext_user"
    REQUIRED_ROLE_SUPPORT:  str = "support"
    REQUIRED_ROLE_ADMIN:    str = "admin"
    def startup(self):
        pass

    def stop(self):
        pass

    def get_security_context(self, access_level, account=None, tenant=None) -> SecurityContext:
        pass

class SecurityManagerDefault(SecurityManagerInterface):

    def startup(self):
        PluginManager.register_plugin(PluginCheckAuthJWT())
        PluginManager.register_plugin(PluginCheckAuthBasic())
        PluginManager.register_plugin(PluginCheckAuthAPIToken())
        print("Security layer started.")

    def stop(self):
        print("Security layer stopped.")

    def get_security_context(self, access_level=SecurityManagerInterface.ACCESS_LAYER_PUBLIC, account=None, tenant=None) -> SecurityContext:
        if access_level == SecurityManagerInterface.ACCESS_LAYER_PUBLIC:
            return SecurityContextPublic()
        elif access_level == SecurityManagerInterface.ACCESS_LAYER_SERVER:
            return SecurityContextServer()
        elif access_level == SecurityManagerInterface.ACCESS_LAYER_SERVICE:
            return SecurityContextService()
        elif access_level == SecurityManagerInterface.ACCESS_LAYER_ACCOUNT and account:
            return SecurityContextAccount(account=account)
        elif access_level == SecurityManagerInterface.ACCESS_LAYER_TENANT and tenant:
            return SecurityContextTenant(tenant=tenant, account=account)
        else:
            return SecurityContextForbidden()


