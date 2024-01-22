from .core import SecurityManagerInterface, SecurityManagerDefault
from .context import SecurityContext
class SecurityManager:

    _instance = SecurityManagerDefault()

    @classmethod
    def startup(cls):
        cls._instance.startup()

    @classmethod
    def stop(cls):
        cls._instance.stop()

    @classmethod
    def get_security_context(cls, access_level, account=None, tenant=None) -> SecurityContext:
        return cls._instance.get_security_context(access_level=access_level, account=account, tenant=tenant)


