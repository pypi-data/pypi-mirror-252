class ContextValuesInterface:
    def __init__(self):
        self.values = {}

    def clear(self):
        pass

    def key_exists(self, key:str) -> bool:
        pass

    def set(self, key:str, value, overwrite:bool=True) -> bool:
        pass

    def get(self, key: str, default=None):
        pass

    def remove(self, key) -> bool:
        pass

    def get_dict(self) -> dict:
        pass

    def get_keys(self) -> list:
        pass
    def count(self) -> int:
        pass

class ContextValues(ContextValuesInterface):
    def __init__(self):
        self.values = {}

    def clear(self):
        self.values = {}

    def key_exists(self, key:str) -> bool:
        if key in self.values:
            return True
        else:
            return False

    def set(self, key:str, value, overwrite:bool=True) -> bool:
        if key in self.values and not overwrite:
            return False
        else:
            self.values[key] = value
            return True

    def get(self, key: str, default=None):
        return self.values.get(key, default)

    def remove(self, key) -> bool:
        if self.key_exists(key):
            del self.values[key]
            return True
        else:
            return False

    def get_dict(self) -> dict:
        return self.values

    def get_keys(self) -> list:
        result = []
        for key in self.values:
            result.append(key)
        return result
    def count(self) -> int:
        return len(self.values)


