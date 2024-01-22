from .core import PluginManagerInterface, PluginManagerDefault, PluginInterface

class PluginManager:

    _instance = PluginManagerDefault()

    @classmethod
    def startup(cls):
        cls._instance.startup()
        print("Plugins started.")

    @classmethod
    def stop(cls):
        cls._instance.stop()
        print("Plugins stopped.")

    @classmethod
    def get_plugins(cls, filter_interface=None, filter_ids: list = []) -> list:
        return cls._instance.get_plugins(filter_interface=filter_interface, filter_ids=filter_ids)

    @classmethod
    def register_plugin(cls, plugin: PluginInterface) -> bool:
        return cls._instance.register_plugin(plugin=plugin)