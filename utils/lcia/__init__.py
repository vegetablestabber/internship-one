from utils import DATA_PATH
from utils.industry import Company, IndustryCode, IndustryStandard
from utils.resource import ResourceCode, ResourceStandard

LCIA_PATH = DATA_PATH / "lcia_v3.9.1 1.csv"

class ISICCode(IndustryCode):
    def __init__(self, value):
        super().__init__(IndustryStandard.ISIC, value)

class ISICCompany(Company):
    def __init__(self, code: str, desc: str):
        super().__init__(ISICCode(code), desc)

class CPCCode(ResourceCode):
    def __init__(self, value):
        super().__init__(ResourceStandard.CPC, value)