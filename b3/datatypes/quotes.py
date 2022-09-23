import decimal
import enum
import dataclasses

__all__ = [
    'QuoteSize',
    'Quotes'
]

class QuoteSize(enum.IntEnum):
    UNIT     = 1
    THOUSAND = 1000

@dataclasses.dataclass(init=True)
class Quotes:
    open: decimal.Decimal
    high: decimal.Decimal
    low: decimal.Decimal
    close: decimal.Decimal
    average: decimal.Decimal
    best_ask: decimal.Decimal
    best_bid: decimal.Decimal