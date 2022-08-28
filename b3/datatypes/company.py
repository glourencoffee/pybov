import dataclasses
import datetime
import typing
from b3 import datatypes

@dataclasses.dataclass(init=True)
class CompanyDetail:
    cnpj: int
    cvm_code: int
    company_name: str
    trading_name: str
    company_code: str
    security_codes: typing.Tuple[datatypes.SecurityCode]
    activity: str
    industry: str
    market: str
    market_indicator: str
    has_bdr: bool
    bdr_type: str
    has_emissions: bool
    has_quotation: bool
    common_institution: str
    preferred_institution: str
    status: str
    website: str
    last_date: datetime.datetime
    bvmf_describle_category: str