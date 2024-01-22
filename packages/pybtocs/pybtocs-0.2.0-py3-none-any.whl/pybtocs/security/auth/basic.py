from ..plugins import PluginCheckAuthInterface


class PluginCheckAuthBasic(PluginCheckAuthInterface):

    def get_id(self) -> str:
        return "pybtocs.PluginCheckAuthBasic"

    def get_title(self) -> str:
        return "Check Auth for Basic Auth"