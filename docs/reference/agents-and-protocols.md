# Agentes e protocolos

Os agentes ficam em `agentes/market_agents.py`. A nomenclatura é a de Melo
(2022, cap. 6), de onde vem a formulação.

## Os agentes

| Sigla | Classe | Quantos (IEEE 13) | Nome local | Papel |
|---|---|---|---|---|
| AP | `ProsumerAgent` | 10 | `prosumer<barra>` | programa o próprio armazenamento contra o preço do mercado |
| AC | `ConcentratorAgent` | 1 | `concentrator_<nome>` | agrega os prosumidores sob um transformador e reotimiza com o preço sombra |
| AD | `DSOAgent` | 1 | `dso` | tem o modelo da rede e as restrições de tensão; despacha o armazenamento de rede |
| AM | `MarketAgent` | 1 | `market` | coordena a decomposição dual: atualiza o preço sombra e testa a convergência |
| | `SolverAgent` | 1 | `solver` | resolve os modelos de otimização fora do laço de eventos do Twisted |

Os agentes ocupam portas consecutivas a partir de `PADE_PORT` (5678), na ordem:
mercado, solver, DSO, concentradores e prosumidores.

`MarketAgent` carrega também o `MarketMosaikSim`, o único simulador mosaik do
sistema, que na co-simulação recebe o passo do orquestrador e devolve a
potência de cada barra e porta e as derivações do regulador.

## Os protocolos

| Classe | Protocolo FIPA | Quem inicia | Quem participa | Para quê |
|---|---|---|---|---|
| `ConcentratorInitiator` / `ProsumerParticipant` | Contract Net | concentrador | prosumidores | ciclo 1: as programações dos prosumidores |
| `ReportInitiator` / `ConcentratorParticipant` | Contract Net | DSO | concentradores | ciclo 2: a programação agregada |
| `MarketInitiator` / `ConcentratorParticipant`, `DSOParticipant` | Contract Net | mercado | concentradores e DSO | ciclos 3 e 4: as análises e cada rodada com o preço sombra |
| `OperationInitiator` | Contract Net | mercado | concentradores e DSO | a verificação de cada janela da operação (só na co-simulação) |
| `SolverClient` / `SolverProtocol` | Request | os demais agentes | solver | resolver um modelo de otimização |
| `DispatchPublisher` / `DispatchSubscriber` | Subscribe | DSO e concentradores | concentradores e prosumidores | o despacho da programação acordada e as confirmações |

## As mensagens

O conteúdo de cada mensagem é JSON. O tamanho serializado é o que a camada de
rede usa para calcular o atraso, então a escolha de serialização afeta o
resultado com a rede de rádio
([A camada de rede](../explanation/network-layer.md)).

## Tempo limite e retransmissão

O `handle_all_proposes` do Contract Net do PADE só dispara quando todas as
propostas chegam, e o tempo limite do protocolo está desativado no PADE. Por
isso cada rodada arma o próprio tempo limite e retransmite aos que faltam, até
`MARKET_MAX_RETRIES` vezes (10).

| Rede | Tempo limite padrão |
|---|---|
| `ideal` | 120 s |
| `lossy` | 60 s × `NET_TIME_SCALE`, no mínimo 3 s |
| `omnet` | três janelas de 15 min × `NET_TIME_SCALE`, no mínimo 20 s |

`MARKET_ROUND_TIMEOUT` fixa outro valor.
