import b3
import datetime
import decimal
import io
import unittest

class TestHistoricalQuotes(unittest.TestCase):
    def testReader(self):
        line   = '012022022302A1AP34      010ADVANCE AUTODRN          R$  000000000703400000000070340000000006169000000000616900000000061690000000000000000000000616900003000000000000001883000000000011618028000000000000009999123100000010000000000000BRA1APBDR001109'
        stream = io.StringIO(line)
        
        with b3.historical_quotes_reader(stream) as reader:
            bulletin = next(reader)

            self.assertEquals(bulletin.exchange_date,                 datetime.date(2022, 2, 23))
            self.assertEquals(bulletin.type,                          b3.DailyBulletinType.ROUND_LOT)
            self.assertEquals(bulletin.isin,                          'BRA1APBDR001')
            self.assertEquals(bulletin.ticker,                        'A1AP34')
            self.assertEquals(bulletin.market_type,                   b3.MarketType.CASH)
            self.assertEquals(bulletin.company_short_name,            'ADVANCE AUTO')
            self.assertEquals(bulletin.especification,                'DRN')
            self.assertEquals(bulletin.forward_market_remaining_days, None)
            self.assertEquals(bulletin.reference_currency,            'R$')
            self.assertEquals(bulletin.quotes.open,                   decimal.Decimal('70.34'))
            self.assertEquals(bulletin.quotes.high,                   decimal.Decimal('70.34'))
            self.assertEquals(bulletin.quotes.low,                    decimal.Decimal('61.69'))
            self.assertEquals(bulletin.quotes.average,                decimal.Decimal('61.69'))
            self.assertEquals(bulletin.quotes.close,                  decimal.Decimal('61.69'))
            self.assertEquals(bulletin.quotes.best_ask,               decimal.Decimal('0.00'))
            self.assertEquals(bulletin.quotes.best_bid,               decimal.Decimal('61.69'))
            self.assertEquals(bulletin.total_trade_market,            3)
            self.assertEquals(bulletin.total_trade_count,             1883)
            self.assertEquals(bulletin.total_trade_volume,            decimal.Decimal('116180.28'))
            self.assertEquals(bulletin.strike_price,                  decimal.Decimal('0.00'))
            self.assertEquals(bulletin.strike_price_correction_type,  None)
            self.assertEquals(bulletin.maturity_date,                 datetime.date(9999, 12, 31))
            self.assertEquals(bulletin.quote_size,                    b3.QuoteSize.UNIT)
            self.assertEquals(bulletin.strike_price_points,           decimal.Decimal('0.000000'))
            self.assertEquals(bulletin.distribution_number,           109)