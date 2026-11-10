# API (gerada)

Estas páginas são geradas a partir das docstrings dos arquivos de `agentes/`
pelo [mkdocstrings](https://mkdocstrings.github.io/), a cada build da
documentação.

| Página | Arquivo | O que tem |
|---|---|---|
| [Agentes do mercado](market-agents.md) | `market_agents.py` | os agentes, os protocolos, o simulador mosaik e o laço de execução |
| [Camada de rede](network-link.md) | `network_link.py` | os backends `ideal`, `lossy` e `omnet` e a instalação no envio dos agentes |
| [Negociação isolada](isolated-negotiation.md) | `negociacao_isolada.py` | o ponto de entrada sem mosaik |

A API do PADE está em [grei-ufc/pade](https://github.com/grei-ufc/pade); a dos
modelos de otimização, no
[tteso-market-opentes](https://grei-ufc.github.io/tteso-market-opentes/reference/api/).
