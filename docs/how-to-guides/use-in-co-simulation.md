# Usar na co-simulação

Os arquivos de `agentes/` são os mesmos da pasta
`simulators/pade-opentes/agents/` do
[co-simulation-opentes](https://grei-ufc.github.io/co-simulation-opentes/). Lá,
eles rodam no contêiner `pade`, com o mosaik disparando a negociação e a fase de
operação, o OpenDSS resolvendo a rede e, com `NET_BACKEND=omnet`, o OMNeT++
calculando o atraso de cada mensagem.

## O que muda entre os dois

| | Aqui | Na co-simulação |
|---|---|---|
| quem dispara a negociação | o reactor do Twisted, um segundo depois de subir | o mosaik, no passo 0 do dia |
| fase de operação | não roda | a cada 15 min, com o ponto de operação no OpenDSS |
| rede entre agentes | `ideal` ou `lossy` | também `omnet` (6TiSCH ou Wi-SUN FAN) |
| modelos de otimização | o pacote `tteso-market-opentes`, instalado pelo uv | a pasta `simulators/market-opentes`, montada em `/market` |
| caso IEEE 13 | embutido no pacote de mercado | `simulators/grid-opentes/src/data/13Bus` |

## Levar uma mudança dos agentes para a plataforma

1. Mude e confira aqui: `uv run agentes/negociacao_isolada.py` deve continuar em
   42 rodadas.
2. Copie o arquivo para `simulators/pade-opentes/agents/` no co-simulation-opentes.
3. Lá, rode `./run.sh market` e confira o `run.json` e o `result_negociado.csv`.

O `negociacao_isolada.py` fica só aqui: na co-simulação, o ponto de entrada é o
próprio `market_agents.py`.

## O backend `omnet` daqui

Com o extra `rede`, a camada de rede daqui também fala com o servidor de rede do
co-simulation-opentes, se ele estiver rodando e alcançável:

```bash
uv sync --extra rede
NET_BACKEND=omnet NET_TIME_SCALE=0.02 OMNET_HOST=localhost OMNET_NET_PORT=5556 \
  uv run agentes/negociacao_isolada.py
```

O contêiner `comm` só expõe a porta 5556 na rede interna do compose; para usá-lo
daqui, a porta precisa ser publicada no host.
