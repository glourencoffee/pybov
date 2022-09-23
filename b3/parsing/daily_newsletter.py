import collections
import enum
import functools
import typing
from b3.datatypes import (
    DailyNewsletterType,
    DailyNewsletter,
    MarketType,
    ContractCorrection,
    QuoteSize,
    Quotes
)
from b3.utils import (
    date_from_string,
    pic11v99,
    pic16v99,
    pic7v06
)

__all__ = [
    'RegistryType',
    'QuotesField',
    'quotes_fields',
    'parse_line',
    'make_quotes',
    'make_daily_newsletter',
    'reader'
]

class RegistryType(enum.Enum):
    HEADER  = '00'
    QUOTES  = '01'
    TRAILER = '99'

QuotesField = collections.namedtuple('QuotesField', ['name', 'size', 'factory'])

@functools.lru_cache
def quotes_fields():
    return (
        QuotesField('EXCDAT', 8,  date_from_string),
        QuotesField('CODBDI', 2,  lambda value: DailyNewsletterType(int(value))),
        QuotesField('CODNEG', 12, str),
        QuotesField('TPMERC', 3,  MarketType),
        QuotesField('NOMRES', 12, str),
        QuotesField('ESPECI', 10, str),
        QuotesField('PRAZOT', 3,  lambda value: int(value) if value != '' else None),
        QuotesField('MODREF', 4,  str),
        QuotesField('PREABE', 13, pic11v99),
        QuotesField('PREMAX', 13, pic11v99),
        QuotesField('PREMIN', 13, pic11v99),
        QuotesField('PREMED', 13, pic11v99),
        QuotesField('PREULT', 13, pic11v99),
        QuotesField('PREOFC', 13, pic11v99),
        QuotesField('PREOFV', 13, pic11v99),
        QuotesField('TOTNEG', 5,  int),
        QuotesField('QUATOT', 18, int),
        QuotesField('VOLTOT', 18, pic16v99),
        QuotesField('PREEXE', 13, pic11v99),
        QuotesField('INDOPC', 1,  lambda value: ContractCorrection(int(value)) if int(value) != 0 else None),
        QuotesField('DATVEN', 8,  date_from_string),
        QuotesField('FATCOT', 7,  lambda value: QuoteSize(int(value))),
        QuotesField('PTOEXE', 13, pic7v06),
        QuotesField('CODISI', 12, str),
        QuotesField('DISMES', 3,  int),
    )

def _parse_header_line(line: str) -> typing.Dict:
    return {} # Should return anything?

def _parse_quotes_line(line: str) -> typing.Dict[str, typing.Any]:
    values = {}
    pos    = 0

    for (field_name, field_size, factory) in quotes_fields():
        stop = (pos + field_size)

        try:
            value = line[pos:stop]
            values[field_name] = factory(value.strip())
        except (IndexError, ValueError) as exc:
            print(f"failed to read field '{field_name}': {exc}")
            raise
        else:
            pos = stop

    return values

def _parse_trailer_line(line: str) -> typing.Dict:
    return {} # Should return anything?

def parse_line(line: str) -> typing.Tuple[RegistryType, typing.Dict[str, typing.Any]]:
    registry_type = RegistryType(line[0:2])
    leftover_line = line[2:]
    
    if registry_type == RegistryType.HEADER:
        return registry_type, _parse_header_line(leftover_line)

    elif registry_type == RegistryType.QUOTES:
        return registry_type, _parse_quotes_line(leftover_line)

    elif registry_type == RegistryType.TRAILER:
        return registry_type, _parse_trailer_line(leftover_line)

    else:
        raise ValueError(f'unknown registry type {registry_type}')

def make_quotes(values: typing.Dict[str, typing.Any]) -> Quotes:
    return Quotes(
        open     = values['PREABE'],
        high     = values['PREMAX'],
        low      = values['PREMIN'],
        close    = values['PREMED'],
        average  = values['PREULT'],
        best_ask = values['PREOFC'],
        best_bid = values['PREOFV']
    )

def make_daily_newsletter(values: typing.Dict[str, typing.Any]) -> DailyNewsletter:
    return DailyNewsletter(
        exchange_date                 = values['EXCDAT'],
        type                          = values['CODBDI'],
        ticker                        = values['CODNEG'],
        market_type                   = values['TPMERC'],
        company_short_name            = values['NOMRES'],
        especification                = values['ESPECI'],
        forward_market_remaining_days = values['PRAZOT'],
        reference_currency            = values['MODREF'],
        quotes                        = make_quotes(values),
        total_trade_market            = values['TOTNEG'],
        total_trade_count             = values['QUATOT'],
        total_trade_volume            = values['VOLTOT'],
        strike_price                  = values['PREEXE'],
        strike_price_correction_type  = values['INDOPC'],
        maturity_date                 = values['DATVEN'],
        quote_size                    = values['FATCOT'],
        strike_price_points           = values['PTOEXE'],
        isin                          = values['CODISI'],
        distribution_number           = values['DISMES']
    )

def reader(file: typing.IO) -> typing.Generator[DailyNewsletter, None, None]:
    for line in file:
        registry_type, values = parse_line(line)

        if registry_type == RegistryType.QUOTES:
            yield make_daily_newsletter(values)