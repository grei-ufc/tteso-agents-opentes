# Variáveis de ambiente

Os agentes leem a configuração do ambiente na importação. As variáveis do
modelo de mercado (`MARKET_FASE`, `MARKET_DISPOSITIVO`, `MARKET_CRITERIO`,
`MARKET_SOLVER_PATH` e as demais) são as do pacote de mercado, listadas na
[referência do tteso-market-opentes](https://grei-ufc.github.io/tteso-market-opentes/reference/environment-variables/).
Abaixo, as que são dos agentes e da camada de rede.

## Execução

| Variável | Padrão | O que muda |
|---|---|---|
| `MARKET_CONFIG` | o `config.json` do pacote de mercado | caso de estudo |
| `MARKET_RUN_DIR` | `resultados/negociacao` | pasta do `run.json` |
| `MARKET_MAX_ROUNDS` | `150` na negociação isolada | teto de rodadas |
| `MARKET_MAX_RETRIES` | `10` | tentativas de retransmissão antes de desistir |
| `MARKET_ROUND_TIMEOUT` | calculado pela rede | tempo limite de cada rodada, em segundos |
| `MARKET_WINDOW_S` | `900` | a janela de 15 min, base dos orçamentos de cada ciclo |
| `PADE_PORT` | `5678` | porta do primeiro agente |
| `PADE_AGENT_HOST` | `127.0.0.1` | endereço que os agentes usam para se conectar entre si |

A negociação isolada força `MARKET_OPERATION=0`: a fase de operação precisa do
mosaik e do OpenDSS e só roda na co-simulação.

## Camada de rede

| Variável | Padrão | O que muda |
|---|---|---|
| `NET_BACKEND` | `ideal` | `ideal`, `lossy` ou `omnet` |
| `NET_TIME_SCALE` | `1.0` | fração do atraso nominal esperada em relógio real; também escala o tempo limite |
| `NET_TRACE` | vazio | arquivo do traço de mensagens; a pasta é criada se faltar |
| `NET_MESSAGE_SIZE` | `real` | tamanho informado à rede: `real` (conteúdo serializado) ou `declarado` (classes fixas da implementação de referência) |
| `NET_DROP_PROBABILITY` | `0.0` | com `lossy`, probabilidade de perda por mensagem |
| `NET_BANDWIDTH_BPS` | `50000` | com `lossy`, a banda do canal |
| `NET_PROPAGATION` | `0.010` | com `lossy`, o atraso de propagação, em segundos |
| `NET_JITTER_MEAN` | `0.05` | com `lossy`, a média do atraso aleatório exponencial, em segundos |
| `NET_SEED` | `0` | com `lossy`, a semente do sorteio |
| `OMNET_HOST`, `OMNET_NET_PORT` | `comm`, `5556` | com `omnet`, o endereço do servidor de rede |
