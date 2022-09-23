import collections
import enum
import functools
import typing
from b3.datatypes import (
    DailyBulletinType,
    DailyBulletin,
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
    'historical_quotes_reader'
]

class _RegistryType(enum.Enum):
    HEADER  = '00'
    QUOTES  = '01'
    TRAILER = '99'

_QuotesField = collections.namedtuple('QuotesField', ['name', 'size', 'factory'])

@functools.lru_cache
def _quotes_fields():
    return (
        _QuotesField('EXCDAT', 8,  date_from_string),
        _QuotesField('CODBDI', 2,  lambda value: DailyBulletinType(int(value))),
        _QuotesField('CODNEG', 12, str),
        _QuotesField('TPMERC', 3,  MarketType),
        _QuotesField('NOMRES', 12, str),
        _QuotesField('ESPECI', 10, str),
        _QuotesField('PRAZOT', 3,  lambda value: int(value) if value != '' else None),
        _QuotesField('MODREF', 4,  str),
        _QuotesField('PREABE', 13, pic11v99),
        _QuotesField('PREMAX', 13, pic11v99),
        _QuotesField('PREMIN', 13, pic11v99),
        _QuotesField('PREMED', 13, pic11v99),
        _QuotesField('PREULT', 13, pic11v99),
        _QuotesField('PREOFC', 13, pic11v99),
        _QuotesField('PREOFV', 13, pic11v99),
        _QuotesField('TOTNEG', 5,  int),
        _QuotesField('QUATOT', 18, int),
        _QuotesField('VOLTOT', 18, pic16v99),
        _QuotesField('PREEXE', 13, pic11v99),
        _QuotesField('INDOPC', 1,  lambda value: ContractCorrection(int(value)) if int(value) != 0 else None),
        _QuotesField('DATVEN', 8,  date_from_string),
        _QuotesField('FATCOT', 7,  lambda value: QuoteSize(int(value))),
        _QuotesField('PTOEXE', 13, pic7v06),
        _QuotesField('CODISI', 12, str),
        _QuotesField('DISMES', 3,  int),
    )

def _parse_header_line(line: str) -> typing.Dict:
    return {} # Should return anything?

def _parse_quotes_line(line: str) -> typing.Dict[str, typing.Any]:
    values = {}
    pos    = 0

    for (field_name, field_size, factory) in _quotes_fields():
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

def _parse_line(line: str) -> typing.Tuple[_RegistryType, typing.Dict[str, typing.Any]]:
    registry_type = _RegistryType(line[0:2])
    leftover_line = line[2:]
    
    if registry_type == _RegistryType.HEADER:
        return registry_type, _parse_header_line(leftover_line)

    elif registry_type == _RegistryType.QUOTES:
        return registry_type, _parse_quotes_line(leftover_line)

    elif registry_type == _RegistryType.TRAILER:
        return registry_type, _parse_trailer_line(leftover_line)

    else:
        raise ValueError(f'unknown registry type {registry_type}')

def _make_quotes(values: typing.Dict[str, typing.Any]) -> Quotes:
    return Quotes(
        open     = values['PREABE'],
        high     = values['PREMAX'],
        low      = values['PREMIN'],
        average  = values['PREMED'],
        close    = values['PREULT'],
        best_ask = values['PREOFC'],
        best_bid = values['PREOFV']
    )

def _make_daily_bulleting(values: typing.Dict[str, typing.Any]) -> DailyBulletin:
    return DailyBulletin(
        exchange_date                 = values['EXCDAT'],
        type                          = values['CODBDI'],
        isin                          = values['CODISI'],
        ticker                        = values['CODNEG'],
        market_type                   = values['TPMERC'],
        company_short_name            = values['NOMRES'],
        especification                = values['ESPECI'],
        forward_market_remaining_days = values['PRAZOT'],
        reference_currency            = values['MODREF'],
        quotes                        = _make_quotes(values),
        total_trade_market            = values['TOTNEG'],
        total_trade_count             = values['QUATOT'],
        total_trade_volume            = values['VOLTOT'],
        strike_price                  = values['PREEXE'],
        strike_price_correction_type  = values['INDOPC'],
        maturity_date                 = values['DATVEN'],
        quote_size                    = values['FATCOT'],
        strike_price_points           = values['PTOEXE'],
        distribution_number           = values['DISMES']
    )

def historical_quotes_reader(stream: typing.IO) -> typing.Generator[DailyBulletin, None, None]:
    for line in stream:
        registry_type, values = _parse_line(line)

        if registry_type == _RegistryType.QUOTES:
            yield _make_daily_bulleting(values)