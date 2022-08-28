import dataclasses
import enum

class MarketType(enum.Enum):
    CASH                             = '010'
    EXERCISE_OF_CALL_OPTIONS         = '012'
    EXERCISE_OF_PUT_OPTIONS          = '013'
    AUCTION                          = '017'
    ODD_LOT                          = '020'
    TERM                             = '030'
    FORWARD_WITH_GAIN_RETENTION      = '050'
    FORWARD_WITH_CONTINUOUS_MOVEMENT = '060'
    CALL_OPTIONS                     = '070'
    PUT_OPTIONS                      = '080'

@dataclasses.dataclass(init=True)
class SecurityCode:
    ticker: str
    isin: str