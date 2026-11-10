# Negociação com perda de mensagens

O protocolo FIPA supõe que toda mensagem chega. Este tutorial põe perda entre os
agentes e mostra como a negociação se recupera.

## Rodar

```bash
NET_BACKEND=lossy NET_DROP_PROBABILITY=0.05 NET_TIME_SCALE=0.02 \
NET_TRACE=resultados/perda/msg_trace.csv MARKET_RUN_DIR=resultados/perda \
  uv run agentes/negociacao_isolada.py
```

| Variável | O que faz |
|---|---|
| `NET_BACKEND=lossy` | põe o modelo de canal com perda no envio de cada agente |
| `NET_DROP_PROBABILITY=0.05` | cada mensagem se perde com 5% de probabilidade |
| `NET_TIME_SCALE=0.02` | comprime o atraso e o tempo limite: com perda, cada rodada espera 3 s em vez de 60 s por mensagem perdida |
| `NET_TRACE` | grava uma linha por mensagem enviada |
| `MARKET_RUN_DIR` | pasta do `run.json` |

O atraso de cada mensagem é a propagação, mais a transmissão do tamanho real da
mensagem a 50 kbps, mais um atraso aleatório. O modelo está em
[A camada de rede](../explanation/network-layer.md).

## A recuperação

Quando uma resposta não chega dentro do tempo limite da rodada, quem enviou o
pedido retransmite só aos que faltam:

```text
[market] ... --> rodada 13: timeout, retransmitindo o CFP para ['concentrator_alimentador_650', 'dso'] (tentativa 1/10)
[market] ... --> rodada 13: |dlambda|=1.210e+01 |x-y|=14.0076 kW (1.0e-01 de Pmax) rede=5 s
```

Uma resposta duplicada, que chega depois do reenvio, é descartada: a rodada que
ela fecharia já fechou. Depois de 10 tentativas sem resposta, o que acontece
depende do ciclo: no ciclo 1, a programação do prosumidor que não respondeu
entra com zero; numa rodada da negociação, ela termina sem convergir
(`TIMEOUT definitivo`).

## O que conferir

| Onde | O quê |
|---|---|
| fim do terminal | `negociacao encerrada: convergiu em 42 rodadas, N retransmissoes` |
| `run.json` | `retransmissions`, e `schedules_lost`: programações de prosumidor que se perderam de vez e entraram com zero |
| `msg_trace.csv` | cada mensagem com remetente, destino, performativa, bytes, atraso e se foi descartada (`dropped`) |

Com o comando acima, a negociação fecha nas mesmas 42 rodadas da entrega ideal,
com 18 retransmissões e nenhuma programação perdida. Na co-simulação, com a
mesma perda, os números são iguais, e o resultado elétrico é idêntico ao da
entrega ideal
([Resultados do co-simulation-opentes](https://grei-ufc.github.io/co-simulation-opentes/results/#de-onde-vem-esse-tempo)).

## Sem a escala de tempo

Com `NET_TIME_SCALE=1.0`, o padrão, o tempo limite com perda é de 60 s, e cada
mensagem perdida segura a rodada por um minuto. Com 5% de perda, a negociação
leva perto de um minuto por rodada.
