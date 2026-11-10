# Instalação

## Requisitos

- **Python 3.12**
- **[uv](https://github.com/astral-sh/uv)**
- **IBM CPLEX**, só para os agentes do mercado: os modelos de otimização que eles
  chamam pedem um solver inteiro-misto e quadrático. A licença acadêmica é
  pessoal, pelo IBM Academic Initiative. Os exemplos do PADE não precisam dele.

## Instalar

```bash
git clone https://github.com/grei-ufc/tteso-agents-opentes.git
cd tteso-agents-opentes
uv sync
```

O `uv sync` instala:

| Pacote | De onde | Para quê |
|---|---|---|
| `pade-agents` 3.0 | PyPI | a plataforma de agentes e o comando `pade` |
| `tteso-market-opentes` | o repositório [tteso-market-opentes](https://github.com/grei-ufc/tteso-market-opentes), pelo git | os modelos de otimização e o caso IEEE 13 |
| `numpy` | PyPI | cálculo dos agentes |

## Extras

| Extra | Para quê | Instalar |
|---|---|---|
| `rede` | o backend `omnet` da camada de rede (pyzmq), com o servidor de rede do co-simulation-opentes | `uv sync --extra rede` |
| `mosaik` | o exemplo `exemplos/mosaik_example` | `uv sync --extra mosaik` |
| grupo `docs` | esta documentação | `uv sync --group docs` |

O exemplo `exemplos/iec_61850` precisa do `pyiec61850`, que é instalado à parte
(ver o README da pasta).

## Apontar o solver

```bash
export MARKET_SOLVER_PATH=$HOME/IBM/CPLEX_Studio2211/cplex/bin/x86-64_linux/cplex
```

Outros solvers: [Configurar o solver](https://grei-ufc.github.io/tteso-market-opentes/how-to-guides/configure-solver/),
no tteso-market-opentes.

## Conferir

```bash
uv run pade version
```

Deve mostrar a versão 3.0 do PADE. Siga para a
[Primeira Negociação](first-negotiation.md) ou para os
[Primeiros agentes no PADE](../tutorials/first-pade-agents.md).
