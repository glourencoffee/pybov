# About

`b3` is a Python library that allows extracting data provided by B3.
The library was designed to be part of a software for analysis of public
companies, although it can be used on its own for other purposes.

# What is B3?

B3 is the Brazilian stock exchange. Among its responsibilities is buying
and selling securities, such as stocks and stock options.

Note that, as B3 is concerned with market data, it is beyond its scope to
store or provide financial data from publicly-held companies, such as the
balance sheet and the income statement. Such financial data is the responsibility
of CVM, and its automated handling is possible with the library [cvm][repo-pycvm].

# Usage

To retrieve online information of companies:

```py
>>> import b3
>>> co = b3.company_detail('1023')
>>> co.company_name
'BCO BRASIL S.A.'
>>> co.cnpj
'00000000000191'
>>> co.company_code
'BBAS'
```

To extract historical quotes:

```py
import b3

with b3.historical_quotes_reader('path/to/COTAHIST.txt') as reader:
    for bulletin in reader:
        print(bulletin)
```

# Disclaimer

`b3` is an open-source library that has no connection or affiliation with
B3. The library uses the public API from B3's website and was created solely
for educational purposes. Read B3's [Terms of Use][b3-terms-of-use] for
details about your rights to use their information.

  [repo-pycvm]: <https://github.com/callmegiorgio/pycvm>
  [b3-terms-of-use]: <https://www.b3.com.br/en_us/terms-of-use-and-data-protection/terms-of-use/>