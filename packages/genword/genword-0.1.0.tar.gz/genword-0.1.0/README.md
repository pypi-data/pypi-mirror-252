# Genword

[![codecov](https://codecov.io/gh/henriquesebastiao/genword/graph/badge.svg?token=1l33SfJIyG)](https://codecov.io/gh/henriquesebastiao/genword)
[![CI](https://github.com/henriquesebastiao/genword/actions/workflows/ci.yml/badge.svg)](https://github.com/henriquesebastiao/genword/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/genword.svg)](https://badge.fury.io/py/genword)

Genword é uma ferramenta simples de linha de comando, escrita em Python, que gera todas as combinações possíveis de caracteres, dado um conjunto de caracteres e um comprimento.
## Instalação

Genword está disponível no PyPi, então recomendo instalá-lo usando pipx:

```bash
pipx install genword
```

## Como usar

Você pode chamar o Genword através da linha de comando. Por exemplo:

```bash
genword abc123 1 4
```

Este comando irá gerar todas as combinações possíveis de 1 a 4 caracteres de comprimento, com todos os caracteres fornecidos (`abc123`). Os resultados serão salvos em um arquivo de texto chamado `words.txt`.

## O que é o padrão?

Se você apenas executar:

```bash
genword
```

Sem nenhum argumento, irá gerar todas as combinações possíveis de 1 a 8 caracteres de comprimento, com os seguintes caracteres: `abcdefghijklmnopqrstuvwxyz1234567890!@#$%&`. Esta tarefa pode demorar muito, dependendo do seu computador; por isso, é muito mais interessante se você especificar os argumentos.

## LICENSE

Este projeto é oferecido sob os termos da "BEER-WARE LICENSE". Em outras palavras, você pode fazer o que quiser com esse código. Se nos encontrarmos algum dia, e você achar que vale a pena, você pode me pagar uma cerveja. Pode ser a sua cerveja favorita, ou mesmo algo exótico que você descobriu em uma viagem.

Lembre-se, a cerveja é um excelente motivador para manter esse código atualizado hehe!