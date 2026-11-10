# Ambiente de desenvolvimento

## Ambiente

```bash
git clone https://github.com/grei-ufc/tteso-agents-opentes.git
cd tteso-agents-opentes
uv sync --group docs
export MARKET_SOLVER_PATH=$HOME/IBM/CPLEX_Studio2211/cplex/bin/x86-64_linux/cplex
```

## Mudar os agentes junto com o pacote de mercado

O `uv sync` instala o `tteso-market-opentes` do GitHub, no commit registrado no
`uv.lock`. Para mexer nos dois ao mesmo tempo, com os dois repositórios lado a
lado na mesma pasta, instale o de mercado em modo editável:

```bash
uv pip install -e ../tteso-market-opentes
```

Para trazer a versão mais nova do pacote de mercado para o lock:

```bash
uv lock --upgrade-package tteso-market-opentes
```

## Conferir uma mudança

O repositório não tem suíte de testes automatizados. A conferência é rodar a
negociação e um exemplo do PADE:

| Mudança em | Rode | Confira |
|---|---|---|
| agentes ou camada de rede | `uv run agentes/negociacao_isolada.py` | `convergiu em 42 rodadas, 0 retransmissoes` |
| retransmissão | o mesmo, com `NET_BACKEND=lossy NET_DROP_PROBABILITY=0.05 NET_TIME_SCALE=0.02` | 42 rodadas, com retransmissões |
| exemplos | o exemplo pelo `pade start-runtime` | as mensagens que o `changelogs.md` da pasta lista |

## Manter em sincronia com a plataforma

`agentes/market_agents.py` e `agentes/network_link.py` também vivem em
`simulators/pade-opentes/agents/` do co-simulation-opentes. Uma correção deve ir
para os dois ([Usar na co-simulação](../how-to-guides/use-in-co-simulation.md)).
O `negociacao_isolada.py` é só daqui.

## Comentários

O código e os comentários estão em português. Os comentários explicam o porquê
de cada escolha, e as docstrings alimentam a
[API gerada](../reference/api/index.md).
