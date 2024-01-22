from .logger import LoggerInterface
class InterfaceBase:
    @classmethod
    def log_error(cls, msg):
        print(f"Error: {msg}")

    @classmethod
    def log_info(cls, msg):
        print(f"Info: {msg}")

    def get_logger(cls) -> LoggerInterface:
        cls.log_error("no logger interface available")


class ManagerInstanceInterface(InterfaceBase):

    def initialize(self) -> bool:
        pass

    def startup(self) -> bool:
        pass

    def stop(self) -> bool:
        pass

    def cleanup(self) -> bool:
        pass
class SingletonManagerClassInterface(InterfaceBase):

    _instance: ManagerInstanceInterface = None
    _description: str = None
    @classmethod
    def register(cls, instance: ManagerInstanceInterface) -> bool:
        if not cls._instance:
            cls._instance = instance
            cls.log_info(f"Custom Manager instance registered: {instance}")
            return True
        else:
            cls.log_error(f"Register manager instance {instance} failed. Already initialized.")
            return True

    @classmethod
    def get_description(cls) -> str:
        if cls._description:
            return cls._description
        else:
            return cls
    @classmethod
    def get(cls):
        if not cls._instance:
            cls.log_error(f"no manager instance initialized for {cls}")
            return None
        else:
            return cls._instance

    @classmethod
    def startup(cls):
        instance = cls.get()
        description = cls.get_description()

        if instance:
            if not instance.startup():
                cls.log_error(f"Manager {description} startup failed in {cls}")
                return False
            else:
                return True
        else:
            cls.log_error(f"Manager instance missing for startup - {description} - {cls}")
            return False

    @classmethod
    def stop(cls):
        instance = cls.get()
        description = cls.get_description()

        if instance:
            if not instance.startup():
                cls.log_error(f"Manager {description} stop failed in {cls}")
                return False
            else:
                return True
        else:
            cls.log_error(f"Manager instance missing for stop - {description} - {cls}")
            return False


