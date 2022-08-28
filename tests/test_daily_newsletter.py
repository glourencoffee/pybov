import b3
import datetime
import decimal
import unittest
import typing

class TestDailyNewsletter(unittest.TestCase):
    def assertValueEquals(self, container: typing.Dict[str, typing.Any], key: str, expected: typing.Any):
        self.assertIn(key, container)
        self.assertEquals(container[key], expected)

    def testLineParser(self):
        line = '012022022302A1AP34      010ADVANCE AUTODRN          R$  000000000703400000000070340000000006169000000000616900000000061690000000000000000000000616900003000000000000001883000000000011618028000000000000009999123100000010000000000000BRA1APBDR001109'

        registry_type, values = b3.parsing.daily_newsletter.parse_line(line)

        self.assertEquals(registry_type, b3.parsing.daily_newsletter.RegistryType.QUOTES)
        self.assertValueEquals(values, 'CODBDI', b3.datatypes.DailyNewsletterType.ROUND_LOT)
        self.assertValueEquals(values, 'CODISI', 'BRA1APBDR001')
        self.assertValueEquals(values, 'CODNEG', 'A1AP34')
        self.assertValueEquals(values, 'DATVEN', datetime.date(9999, 12, 31))
        self.assertValueEquals(values, 'DISMES', 109)
        self.assertValueEquals(values, 'ESPECI', 'DRN')
        self.assertValueEquals(values, 'EXCDAT', datetime.date(2022, 2, 23))
        self.assertValueEquals(values, 'FATCOT', b3.datatypes.QuoteSize.UNIT)
        self.assertValueEquals(values, 'INDOPC', None)
        self.assertValueEquals(values, 'MODREF', 'R$')
        self.assertValueEquals(values, 'NOMRES', 'ADVANCE AUTO')
        self.assertValueEquals(values, 'PRAZOT', None)
        self.assertValueEquals(values, 'PREABE', decimal.Decimal('70.34'))
        self.assertValueEquals(values, 'PREEXE', decimal.Decimal('0.00'))
        self.assertValueEquals(values, 'PREMAX', decimal.Decimal('70.34'))
        self.assertValueEquals(values, 'PREMED', decimal.Decimal('61.69'))
        self.assertValueEquals(values, 'PREMIN', decimal.Decimal('61.69'))
        self.assertValueEquals(values, 'PREOFC', decimal.Decimal('0.00'))
        self.assertValueEquals(values, 'PREOFV', decimal.Decimal('61.69'))
        self.assertValueEquals(values, 'PREULT', decimal.Decimal('61.69'))
        self.assertValueEquals(values, 'PTOEXE', decimal.Decimal('0.000000'))
        self.assertValueEquals(values, 'QUATOT', 1883)
        self.assertValueEquals(values, 'TOTNEG', 3)
        self.assertValueEquals(values, 'TPMERC', b3.datatypes.MarketType.CASH)
        self.assertValueEquals(values, 'VOLTOT', decimal.Decimal('116180.28'))