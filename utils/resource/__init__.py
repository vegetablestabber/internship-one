from enum import Enum

# Resource classification standard object
class ResourceStandard(Enum):
    CPC = "CPC"

# Resource classification code object
class ResourceCode:
    def __init__(self, std: ResourceStandard, value: str):
        self.std = std
        self.value = value
        
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.std == other.std and self.value == other.value
        
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

# Product object
class Product:
    def __init__(self, code: ResourceCode, desc: str):
        self.code = code
        self.description = desc