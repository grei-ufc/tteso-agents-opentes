# Arquivos de saída

## `run.json`

A negociação isolada grava `run.json` em `MARKET_RUN_DIR`
(`resultados/negociacao/`) quando o processo encerra.

| Campo | Conteúdo |
|---|---|
| `config` | a configuração da execução: rede, tamanho de mensagem, demanda realizada, margem de tensão, teto de rodadas, cenários, fator de potência, operação |
| `rounds` | rodadas da negociação |
| `converged` | se fechou pelo critério de parada |
| `history` | uma entrada por rodada: `round`, `d_lambda_max`, `residual_max`, `residual_rel_max`, `lambda_max`, as programações `x` (concentrador) e `y` (operador) e o tempo de rede do ciclo 3 (`cycle3_net_s`) |
| `operation` | o registro de cada janela da operação (vazio na negociação isolada) |
| `cycles` | por ciclo: mensagens, perdas, maior atraso e tempo de rede, quando há camada de rede |
| `cycle_budget_s` | o orçamento de cada ciclo dentro da janela de 15 min |
| `schedules_lost` | programações de prosumidor que se perderam de vez e entraram com zero |
| `retransmissions` | quantas mensagens foram reenviadas |

A configuração gravada em `config` existe para que duas execuções com
configurações diferentes não se misturem sem aviso.

## `msg_trace.csv`

Com `NET_TRACE`, uma linha por mensagem enviada:

| Coluna | Conteúdo |
|---|---|
| `wall_time` | instante de relógio do envio |
| `t` | o intervalo de 15 min, na operação |
| `ciclo` | `ciclo1_AC_AP`, `ciclo2_AD_AC` ou `ciclo3_AM_AC_AD` |
| `sender`, `receiver` | nomes locais dos agentes |
| `performative` | `cfp`, `propose`, `accept-proposal`... |
| `bytes` | tamanho informado à rede |
| `delay_s` | atraso nominal, antes de `NET_TIME_SCALE` |
| `dropped` | se a mensagem se perdeu |

O `tteso-figuras` do tteso-market-opentes desenha as figuras de comunicação a
partir deste arquivo e do `run.json`.

## `logs/` dos exemplos

Os exemplos do PADE rodados pelo `start-runtime` gravam `sessions.csv`,
`agents.csv`, `messages.csv` e `events.csv` em `logs/`
([Ler os registros do PADE](../how-to-guides/read-pade-logs.md)).
