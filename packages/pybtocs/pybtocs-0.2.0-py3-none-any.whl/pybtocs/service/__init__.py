"""
B-Tocs Container SDK for Python - Service Layer
Access to different features for main service

mdjoerg@b-tocs.com
"""
from .context import CONTEXT
from ..interfaces import SingletonManagerClassInterface
from .core import ServiceManagerInterface, ServiceManagerDefault
from ..context import ContextValues, ContextValuesInterface

class ServiceManager(SingletonManagerClassInterface):

    RUNTIME_MODE_DEVELOPER:     str = "developer"   # all features are available, no authentification
    RUNTIME_MODE_PRODUCTION:    str = "production"  # features are available with valid environment
    RUNTIME_MODE_TEST:          str = "test"        # features and authentification are available for limited usage

    LAYOUT_DEVELOPER:           str = "developer"
    LAYOUT_PRODUCTION:          str = "production"
    LAYOUT_TEST:                str = "test"
    LAYOUT_DEMO:                str = "demo"

    _instance: ServiceManagerInterface = None
    VERSION: str = '0.1.0'
    TITLE: str = "B-Tocs Container Stack for Python"
    DESCRIPTION: str = "(c) b-tocs.org"


    @classmethod
    def register(cls, title: str, version: str, description: str = None, instance: ServiceManagerInterface = None) -> bool:
        # prepare
        result = True

        # set infos
        cls.TITLE = title
        if version:
            cls.VERSION = version
        if description:
            cls.DESCRIPTION = description

        # output
        cls.log_info(f"Service {cls.TITLE} version {cls.VERSION} is registered")
        if cls.DESCRIPTION:
            cls.log_info(f"Description: {cls.DESCRIPTION}")

        # register instance
        if instance:
            result = cls.register_instance(instance)

        return result

    @classmethod
    def register_instance(cls, instance) -> bool:
        if cls._instance:
            cls.log_error("Service Manager is registered already")
            return False
        else:
            cls._instance = instance
            cls.log_info(f"Custom Service Manager registered: {instance}")
            return True
    @classmethod
    def get(cls):
        if not cls._instance:
            cls._instance = ServiceManagerDefault()
            cls.log_info("Default Service Manager registered")

        return cls._instance

    @classmethod
    def startup(cls):
        instance = cls.get()


        print("B-Tocs Service layer startup... ")
        instance.startup()
        print("B-Tocs Service layer started. ")

    @classmethod
    def stop(cls):
        instance = cls.get()

        print("B-Tocs Service layer stopping...")
        instance.stop()
        print("B-Tocs Service layer stopped.")

    @classmethod
    def get_service_layout(cls) -> str:
        return ServiceManager.LAYOUT_DEVELOPER

    @classmethod
    def get_version(cls) -> str:
        return "0.1.0"

    @classmethod
    def get_title(cls) -> str:
        return "B-Tocs Service"

    @classmethod
    def get_description(cls) -> str:
        return "Generic python based container service"


