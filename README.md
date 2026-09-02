# Curso TDS — Boas Práticas de Programação em Python

Projeto de apoio às aulas do curso. Mais do que resolver um problema de domínio
(clientes de um banco e suas transações), o objetivo aqui é **mostrar como se
organiza um projeto Python profissional**: separação entre código e testes,
tipagem estática, formatação automática, análise estática e uma suíte de testes
que roda a cada mudança.

O domínio é propositalmente simples. A complexidade que interessa está na
*disciplina de engenharia* em volta dele.

## Organização das pastas

```
curso_tds/
├── src/                  # código de produção — a biblioteca em si
│   └── dominio.py        # Cliente, Transacao, TipoTransacao
├── tests/                # testes automatizados — espelham src/
│   ├── test_cliente.py
│   └── test_transacao.py
├── data/                 # dados de exemplo (CSV) usados nas aulas
│   ├── customers.csv
│   └── transactions.csv
├── pyproject.toml        # dependências + configuração das ferramentas
├── Makefile              # atalhos para as tarefas do dia a dia
└── README.md
```

### Por que `src/` e `tests/` separados?

Essa é a convenção mais importante do projeto, e vale entender o *porquê* de
cada parte dela.

**`src/` contém apenas código de produção.** É o que seria empacotado e
distribuído. Nada de teste, nada de script solto, nada de dado de exemplo.
Ao olhar para `src/` você vê exatamente o que o seu software *é*.

O padrão de colocar o código dentro de um diretório `src/` (em vez de deixar
`dominio.py` na raiz) tem uma consequência prática: **o código não fica
importável por acidente**. Se `dominio.py` estivesse na raiz, os testes o
importariam só porque o Python inclui o diretório atual no `sys.path` — e você
nunca saberia se o pacote realmente funciona quando instalado. Com `src/`, o
caminho precisa ser declarado explicitamente. Neste projeto isso é feito no
`pyproject.toml`:

```toml
[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
```

**`tests/` espelha `src/`.** Cada módulo de produção tem seus testes
correspondentes, e o nome do arquivo de teste deixa óbvio o que ele cobre
(`test_cliente.py`, `test_transacao.py`). Quando alguém precisar mexer em
`Cliente`, sabe imediatamente onde estão os testes que protegem esse
comportamento.

Manter os testes fora de `src/` também deixa claro que eles **não fazem parte
do produto**: são uma ferramenta de desenvolvimento. E, como os testes importam
o código exatamente como um usuário externo faria (`from dominio import
Cliente`), eles exercitam a API pública — não os detalhes internos.

**`data/` guarda dados, não código.** Os CSVs de exemplo ficam separados para
que ninguém seja tentado a misturar carga de arquivo com regra de negócio.

## Requisitos

- Python 3.14 ou superior
- [Poetry](https://python-poetry.org/) para gerenciamento de dependências

## Como começar

```bash
poetry install     # instala as dependências de desenvolvimento
make check         # roda lint + tipos + testes
```

## Tarefas disponíveis

O `Makefile` reúne os comandos do dia a dia. Rodar `make check` antes de cada
commit é o hábito que o curso quer construir.

| Comando        | O que faz                                              |
| -------------- | ------------------------------------------------------ |
| `make check`   | Executa `lint`, `types` e `test` — o portão de qualidade |
| `make format`  | Formata `src/` e `tests/` com o Ruff                   |
| `make lint`    | Verifica estilo e problemas comuns                     |
| `make types`   | Roda o mypy em modo estrito                            |
| `make test`    | Roda a suíte de testes com o pytest                    |

## As ferramentas e o que cada uma ensina

Todas são configuradas em um único lugar — o `pyproject.toml` — o que é em si
uma boa prática: uma fonte de verdade para a configuração do projeto.

- **pytest** — testes automatizados. Repare no estilo dos testes em `tests/`:
  um comportamento por teste, nome descritivo em português dizendo *o que* se
  espera (`test_debito_reduz_o_saldo`), e a estrutura *arrange / act / assert*
  separada por linhas em branco.

- **mypy** (`strict = true`) — tipagem estática. Todas as funções, inclusive as
  de teste, são anotadas. O modo estrito não deixa passar um `Any` implícito
  nem uma função sem anotação, e transforma uma classe inteira de bugs em erro
  de compilação.

- **ruff** — formatador e linter rápido, com as regras `E`, `F`, `I`, `UP`,
  `B` e `SIM` ativadas: estilo, erros prováveis, ordenação de imports,
  modernização de sintaxe, armadilhas comuns e simplificações.

## Detalhes de estilo que valem observar no código

- **Nada de número mágico**: `IDADE_MINIMA_ESPECIAL = 45` é uma constante
  nomeada no topo do módulo. O nome explica a regra; o número, sozinho, não
  explicaria.
- **`Enum` em vez de string**: `TipoTransacao.CREDITO` é verificado pelo mypy;
  `"credito"` seria só uma string sujeita a erro de digitação.
- **Imutabilidade do histórico**: `registra_transacao` guarda o
  `saldo_anterior` em cada transação, preservando o rastro do que aconteceu em
  vez de apenas o estado final.
- **Valores padrão explícitos**: `saldo_inicial: float = 0.0` documenta a
  intenção na assinatura.

## Exercício em aberto

O final de `tests/test_transacao.py` tem um teste comentado:

```python
# def test_debito_saldo_insuficiente() -> None:
#     ...
```

Ele descreve um comportamento que **ainda não existe**: o que deve acontecer
quando um débito ultrapassa o saldo? Descomentar esse teste, vê-lo falhar e
então implementar a regra é o ciclo clássico de TDD — e um bom ponto de
partida para a próxima aula.
