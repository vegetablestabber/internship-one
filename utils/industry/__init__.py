from enum import Enum

# Industry classification standard object
class IndustryStandard(Enum):
    NACE = "NACE"
    ISIC = "ISIC"
    WZ = "WZ"
    SSIC = "SSIC"

# Industry classification code object
class IndustryCode:
    def __init__(self, std: IndustryStandard, value: str):
        self.std = std
        self.value = value
        
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.std == other.std and self.value == other.value
        
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

# Company object
class Company:
    def __init__(self, code: IndustryCode, desc: str):
        self.code = code
        self.description = desc