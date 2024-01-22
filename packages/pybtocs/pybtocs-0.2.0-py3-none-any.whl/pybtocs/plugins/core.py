
class PluginInterface:
    def get_id(self) -> str:
        pass

    def get_title(self) -> str:
        pass
class PluginManagerInterface:

    def __init__(self):
        self.plugins: list(PluginInterface) = []
    def startup(self):
        pass

    def stop(self):
        pass

    def register_plugin(self, plugin: PluginInterface) -> bool:
        pass
    def get_plugins(self, filter_interface = None, filter_ids: list = []) -> list:
        pass


class PluginManagerDefault(PluginManagerInterface):

    def startup(self):
        pass

    def stop(self):
        pass

    def get_plugins(self, filter_interface=None, filter_ids: list = []) -> list:
        result = []
        for plugin in self.plugins:
            if filter_interface:
                if not isinstance(plugin, filter_interface):
                    continue
            if filter_ids and len(filter_ids) > 0:
                if not PluginInterface.get_id(plugin) in filter_ids:
                    continue
            result.append(plugin)
        return result

    def register_plugin(self, plugin: PluginInterface) -> bool:
        if plugin not in self.plugins:
            self.plugins.append(plugin)
            print(f"Plugin registered: {plugin.get_id()} - {plugin.get_title()}")
            return True
        else:
            return False

