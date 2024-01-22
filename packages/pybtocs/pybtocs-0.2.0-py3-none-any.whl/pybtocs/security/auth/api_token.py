from ..plugins import PluginCheckAuthInterface


class PluginCheckAuthAPIToken(PluginCheckAuthInterface):

    def get_id(self) -> str:
        return "pybtocs.PluginCheckAuthAPIToken"

    def get_title(self) -> str:
        return "Check Auth for API Token"