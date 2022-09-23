# Sobre

`b3` é uma biblioteca Python que permite extrair dados fornecidos pela B3.
A biblioteca foi projetada para fazer parte de um software para análise de
companhias abertas, embora ela possa ser usada por conta própria para outros
fins.

# O que é a B3?

A B3 é a bolsa de valores brasileira. Entre suas responsabilidades está
a compra e venda de valores mobiliários, tais como ações e opções de ações.

Note que, como a B3 se ocupa dos dados de mercado, está além do seu escopo
armazenar ou fornecer dados financeiros de companhias abertas, tais como o
balanço patrimonial e o resultado de exercício. Esses dados financeiros são
responsabilidade da CVM, e sua manipulação automatizada é possível pela
biblioteca [cvm][repo-pycvm].

# Uso

Para obter informações online de companhias:

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

Para extrair cotações históricas:

```py
import b3

with b3.historical_quotes_reader('caminho/para/COTAHIST.txt') as reader:
    for bulletin in reader:
        print(bulletin)
```

# Aviso Legal

`b3` é uma biblioteca de código aberto que não possui qualquer vínculo ou
afiliação com a B3. A biblioteca usa a API pública do site da B3 e foi
criada unicamente para fins educacionais. Leia os [Termos de Uso][b3-termos-de-uso]
da B3 para mais detalhes sobre os direitos de uso dessas informações.

  [repo-pycvm]: <https://github.com/callmegiorgio/pycvm>
  [b3-termos-de-uso]: <https://www.b3.com.br/pt_br/termos-de-uso-e-protecao-de-dados/termos-de-uso/>