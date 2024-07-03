from enum import Enum

# Industry classification standards (ICSs)
class IndustryStandard(Enum):
    NACE = "NACE"
    ISIC = "ISIC"
    WZ = "WZ"
    SSIC = "SSIC"

# Industry classification codes
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

class NACECode(IndustryCode):
    def __init__(self, value):
        super().__init__(IndustryStandard.NACE, value)