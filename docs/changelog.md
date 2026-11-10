# Changelog

## Documentação no padrão do OpenTES

- Site de documentação no modelo do `tsre-der-opentes`, publicado no GitHub
  Pages pelo workflow de CI, com a API gerada das docstrings.
- O guia de migração e a página da atualização do PADE passam a fazer parte do
  site.
- `negociacao_isolada.py` cria a pasta do traço de mensagens (`NET_TRACE`)
  quando ela não existe.

## 11/2026: criação

- Os agentes do mercado (`market_agents.py`) e a camada de rede
  (`network_link.py`), os mesmos do co-simulation-opentes, e o
  `negociacao_isolada.py`, que roda a negociação sem mosaik.
- Os 16 exemplos do PADE 3.0, com os changelogs de cada um.
- A documentação da atualização do PADE da versão 2.2 para a 3.0 e o guia de
  migração.
- O PADE entra como dependência publicada (`pade-agents` 3.0), e os modelos de
  otimização, pelo `tteso-market-opentes`.

## A migração do PADE (2026)

Registrada no repositório do PADE:

- 30/03/2026 e 07/04/2026: migração para Python 3.12, com a remoção da camada
  web e do banco de dados (fork `douglas-fdbs/pade2026`).
- 12/04/2026: incorporada ao `grei-ufc/pade` (pull request #85).
- 17 a 22/04/2026: empacotamento com o uv e publicação do `pade-agents` 3.0 no
  PyPI, pelo mantenedor.
- 23/04/2026: fluxo de Docker para o PADE 3.0 (pull request #86, maio de 2026).
