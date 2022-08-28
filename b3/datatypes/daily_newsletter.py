import dataclasses
import datetime
import decimal
import enum
from b3 import datatypes

class DailyNewsletterType(enum.IntEnum):
    """BDI (Boletim Diário de Informações; "Daily Newsletter")"""

    ROUND_LOT                                          = 2  # Lote padrão
    BMFBOVESPA_REGULATIONS_SANCTION                    = 5  # Sancionadas pelos regulamentos BMF&Bovespa
    STOCKS_OF_COMPANIES_UNDER_REORGANIZATION           = 6  # Concordatárias
    EXTRAJUDICIAL_RECOVERY                             = 7  # Recuperação extrajudicial
    JUDICIAL_RECOVERY                                  = 8  # Recuperação judicial
    RAET                                               = 9  # Regime de Administração Especial Temporária
    RIGHTS_AND_RECEIPTS                                = 10 # Direitos e recibos
    INTERVENTION                                       = 11 # Intervenção
    REAL_ESTATE_FUNDS                                  = 12 # Fundos imobiliários
    _UNKNOWN13                                         = 13 #
    _REMOVED14                                         = 14 #
    BONDS                                              = 18 # Obrigações
    PRIVATE_BONUSES                                    = 22 # Bônus (privados)
    PUBLIC_BONUSES                                     = 26 # Apólices/bônus/títulos públicos
    EXERCISE_OF_INDEX_CALL_OPTIONS                     = 32 # Exercício de opções de compra de índices
    EXERCISE_OF_INDEX_PUT_OPTIONS                      = 33 # Exercício de opções de venda de índices
    EXERCISE_OF_CALL_OPTIONS                           = 38 # Exercício de opções de compra
    EXERCISE_OF_PUT_OPTIONS                            = 42 # Exercício de opções de venda
    AUCTION_OF_NONQUOTED_SECURITIES                    = 46 #
    PRIVATIZATION_AUCTION                              = 48 #
    AUCTION_OF_ECONOMICAL_RECOVERY_FUND_OF_ES_STATE    = 49 # 
    AUCTION                                            = 50 # Leilão
    FINOR_AUCTION                                      = 51 # Leilão FINOR
    FINAM_AUCTION                                      = 52 # Leilão FINAM
    FISET_AUCTION                                      = 53 # Leilão FISET
    AUCTION_OF_SHARES_IN_ARREARS                       = 54 # Leilão de ações em mora
    SALES_BY_COURT_ORDER                               = 56 # Vendas por alvará judicial
    OTHER                                              = 58 # Outros
    SHARE_SWAP                                         = 60
    GOAL                                               = 61 # Meta
    TERM                                               = 62 # Mercado a Termo
    DEBENTURES_WITH_MATURITY_DATE_OF_UP_TO_3_YEARS     = 66 # Debêntures com data de vencimento até 3 anos
    DEBENTURES_WITH_MATURITY_DATE_GREATER_THAN_3_YEARS = 68 # Debêntures com data de vencimento maior que 3 anos
    ...
    FORWARD_WITH_CONTINUOUS_MOVEMENT                   = 70  
    FORWARD_WITH_GAIN_RETENTION                        = 71 # Mercado de Futuro
    INDEX_CALL_OPTIONS                                 = 74
    INDEX_PUT_OPTIONS                                  = 75
    CALL_OPTIONS                                       = 78
    PUT_OPTIONS                                        = 82
    ODD_LOT                                            = 96

@dataclasses.dataclass(init=True, repr=True)
class DailyNewsletter:
    exchange_date: datetime.date
    type: DailyNewsletterType
    ticker: str
    market_type: datatypes.MarketType
    company_short_name: str
    especification: datatypes.Specification
    forward_market_remaining_days: int
    reference_currency: str
    quotes: datatypes.Quotes
    total_trade_market: int
    total_trade_count: int
    total_trade_volume: decimal.Decimal
    strike_price: decimal.Decimal
    strike_price_correction_type: datatypes.ContractCorrection
    maturity_date: datetime.date
    quote_size: datatypes.QuoteSize
    strike_price_points: decimal.Decimal
    isin: str
    distribution_number: int