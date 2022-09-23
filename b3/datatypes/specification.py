import enum

__all__ = [
    'Specification'
]

class Specification(enum.Enum):
    BDR     = 'BDR'     # Brazilian Depositary Receipt
    BNS     = 'BNS'     # Subscription bonus for miscellaneous
    BNS_BA  = 'BNS B/A' # Subscription bonus for preferred shares
    BNS_ORD = 'BNS ORD' # Subscription bonus for common shares
    ...
    ON      = 'ON'      # Nominative common shares
    ON_P    = 'ON P'    # Nominative common shares with differentiated rights
    ON_REC  = 'ON REC'  # Receipt of subscriptions for common shares
    ...