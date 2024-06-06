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
            # if (self.std == IndustryStandard.NACE and other.std == IndustryStandard.ISIC) or (self.std == IndustryStandard.ISIC and other.std == IndustryStandard.NACE):
            #     return NACE_df.loc[self.value, "ISIC code"] == other.value
            
            return self.std == other.std and self.value == other.value
        
        return False

    def __ne__(self, other):
        return not self.__eq__(other)