## #TTESO: agentes do mercado transativo sobre o PADE 3.0

[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Grei](https://img.shields.io/badge/-GREI-Black?logo=INSPIRE&logoColor=blue&color=42b85a&labelColor=white&style=flat)](https://www.linkedin.com/company/grei-ufc/?originalSubdomain=br)
[![image](https://img.shields.io/badge/-Python%20Version%20|%203.12.11-42b85a?logo=Python&logoColor=fbec41&color=42b85a&labelColor=grey&style=flat)](https://www.python.org/downloads/release/python-31112/)
[![PyPI](https://img.shields.io/badge/PyPI-pade--agents%203.0-42b85a?logo=pypi&logoColor=white&style=flat)](https://pypi.org/project/pade-agents/)

Repositório do time **TTESO** (Sistemas Transativos e Otimização) do projeto
[OpenTES](https://github.com/grei-ufc/general-opentes), do Grupo de Redes
Elétricas Inteligentes (GREI) da UFC. Aqui ficam:

- os **agentes do mercado transativo** (prosumidores, concentrador, operador da
  rede e mercado), que negociam a programação do armazenamento por mensagens
  FIPA-ACL, e um script para rodar essa negociação isolada, sem os outros
  simuladores;
- os **exemplos do PADE** usados no projeto, migrados para a versão 3.0, cada um
  com o registro do que mudou;
- a documentação da **atualização do PADE da versão 2.2 para a 3.0**, feita para
  que a plataforma rodasse em Python 3.12.

O PADE (Python Agent DEvelopment framework) é um projeto independente, mantido em
[grei-ufc/pade](https://github.com/grei-ufc/pade). Este repositório não copia o
núcleo dele: usa o pacote publicado `pade-agents` 3.0.

## Onde este repositório se encaixa

| Repositório | O que tem |
|---|---|
| [co-simulation-opentes](https://github.com/grei-ufc/co-simulation-opentes) | a plataforma completa, onde estes agentes rodam com a rede de comunicação (OMNeT++), a rede elétrica (OpenDSS) e o Mosaik |
| [tteso-market-opentes](https://github.com/grei-ufc/tteso-market-opentes) | os modelos de otimização que os agentes chamam, e a mesma negociação num laço único, sem agentes |
| **tteso-agents-opentes** (este) | os agentes e os exemplos do PADE, executáveis sem os outros simuladores |
| [grei-ufc/pade](https://github.com/grei-ufc/pade) | a plataforma de agentes |

## O que há aqui

```
agentes/
  market_agents.py        os agentes do mercado e a ponte com o Mosaik (o mesmo arquivo da co-simulação)
  network_link.py         a camada de rede entre os agentes: ideal, com perda ou 6TiSCH (OMNeT++)
  negociacao_isolada.py   roda a negociação do dia seguinte sem Mosaik, OpenDSS ou OMNeT++
exemplos/                 os exemplos do PADE 3.0, cada um com changelogs.md e changelogs_en.md
docs/
  atualizacao-pade.md     o que mudou do PADE 2.2 para o 3.0, e por quê
  MIGRACAO_GUIA.md        o guia de migração do PADE legado, arquivo por arquivo
```

## Instalação

Requisitos: Python 3.12, [uv](https://github.com/astral-sh/uv) e o IBM CPLEX
(licença acadêmica, pessoal; ver o README do tteso-market-opentes).

```bash
git clone https://github.com/grei-ufc/tteso-agents-opentes.git
cd tteso-agents-opentes
uv sync
export MARKET_SOLVER_PATH=$HOME/IBM/CPLEX_Studio2211/cplex/bin/x86-64_linux/cplex
```

O `uv sync` instala o `pade-agents` 3.0 do PyPI e o pacote de mercado direto do
repositório tteso-market-opentes. Os extras `rede` (backend 6TiSCH) e `mosaik`
(exemplo PADE + Mosaik) entram com `uv sync --extra rede --extra mosaik`.

## Os agentes do mercado

Cinco papéis, com a nomenclatura de Melo (2022, cap. 6), de onde vem a
formulação:

| Agente | Quantos | Papel |
|---|---|---|
| `ProsumerAgent` | um por nó com armazenamento (10 na IEEE 13) | programa o próprio armazenamento contra o preço do mercado |
| `ConcentratorAgent` | um por transformador de distribuição (1) | agrega os prosumidores e reotimiza com o preço sombra |
| `DSOAgent` | um | tem o modelo da rede e vigia a tensão de cada fase; despacha o armazenamento de rede |
| `MarketAgent` | um | coordena a decomposição dual: atualiza o preço sombra e testa a convergência |
| `SolverAgent` | um | resolve os modelos de otimização fora do laço de eventos do Twisted |

A negociação do dia seguinte tem quatro ciclos: o concentrador pede as
programações aos prosumidores, o operador pede ao concentrador a programação
agregada, o mercado pede as análises ao concentrador e ao operador, e daí em
diante concentrador e operador reotimizam a cada rodada com o preço sombra
corrente até concordarem. Cada etapa usa um protocolo FIPA do PADE: Contract Net
para os ciclos, Request para o solver e Subscribe para o despacho final.

Cada rodada tem um tempo limite próprio, com retransmissão para quem não
respondeu. O Contract Net do PADE só fecha quando todas as propostas chegam, e
sem esse limite uma única mensagem perdida travaria a negociação. A sequência
completa e as escolhas de implementação estão no início de `market_agents.py`.

### Rodar a negociação isolada

```bash
uv run agentes/negociacao_isolada.py
```

Os 14 agentes sobem a partir da porta 5678, negociam e gravam o registro em
`resultados/negociacao/run.json` (rodadas, histórico rodada a rodada e retransmissões). Na IEEE 13 por
fase, a negociação converge em **42 rodadas**, com o mesmo histórico da
negociação centralizada do tteso-market-opentes (conferido em 10/11/2026).

Na co-simulação, quem dispara a negociação é o Mosaik, no passo 0 do dia. Aqui é
o próprio laço do Twisted, e o fim da negociação encerra o processo. Por isso só
a fase de programação roda isolada; a fase de operação depende do relógio do
Mosaik e do fluxo de potência no OpenDSS, e roda no co-simulation-opentes.

A camada de rede continua disponível:

```bash
NET_BACKEND=lossy NET_DROP_PROBABILITY=0.05 NET_TRACE=resultados/msg_trace.csv \
  uv run agentes/negociacao_isolada.py
```

`lossy` sorteia perda e atraso por mensagem; `NET_TRACE` grava uma linha por
mensagem enviada, com tamanho e tempo. Cada mensagem perdida espera o tempo
limite da rodada (60 s) antes de ser reenviada, então com perda a negociação
leva bem mais tempo: com 5% de perda, cerca de um minuto por rodada. O backend `omnet` (rede 6TiSCH ou Wi-SUN
FAN) precisa do servidor de rede do co-simulation-opentes.

As variáveis do modelo (`MARKET_FASE`, `MARKET_DISPOSITIVO`, `MARKET_CRITERIO`
e as demais) são as mesmas do tteso-market-opentes.

## Os exemplos do PADE

Cada pasta de `exemplos/` é independente. Rode de dentro dela:

```bash
cd exemplos/agent_example_4
uv run pade start-runtime --username pade_user --password 12345 --port 24000 agent_example_4_updated.py
```

O `start-runtime` sobe o AMS, o Sniffer e o script dos agentes, e grava a sessão
em `logs/` (`sessions.csv`, `agents.csv`, `messages.csv`, `events.csv`). Usuário
e senha vão na linha de comando para o terminal não parar pedindo digitação.
Encerre com Ctrl+C.

| Pasta | Arquivo | O que demonstra |
|---|---|---|
| `hello_world` | `hello_world_minimal.py`, `hello_world.py` | o menor agente possível; a segunda versão troca uma mensagem ACL real |
| `script_5` | `script_5_updated.py` | a menor troca de mensagens entre dois agentes |
| `test_pingpong` | `test_pingpong.py` | PING e PONG, pelo runtime ou em dois terminais |
| `test_agent` | `test_agent_updated.py` | troca simples entre dois agentes de teste |
| `agent_example_1` | `agent_example_1_updated.py` | três agentes trocando mensagens em anel |
| `agent_example_2` | `agent_example_2_updated.py` | comportamento temporal; a variante `_with_messages` gera tráfego ACL |
| `agent_example_3` | `agent_example_3_updated.py` | FIPA Request entre um agente de relógio e um de tempo |
| `script_3` | `script_3_updated.py` | FIPA Request mínimo: REQUEST, AGREE, INFORM |
| `agent_example_4` | `agent_example_4_updated.py` | FIPA Contract Net com dois participantes |
| `script_2` | `script_2_updated.py` | Contract Net entre um consumidor e três livrarias |
| `script_4` | `script_4_updated.py` | Contract Net numa recomposição de energia |
| `agent_example_5` | `agent_example_5_updated.py` | FIPA Subscribe: um publicador, dois assinantes |
| `agent_example_6` | `agent_example_6_updated.py` | Subscribe com dois publicadores e quatro assinantes |
| `power_systems` | `agent_example_power_system_1_updated.py` | agentes supervisionando um fluxo de potência trifásico na IEEE 13 |
| `mosaik_example` | `agent_example_1_mosaik_updated.py` + `first.py` | co-simulação PADE + Mosaik, o padrão que o `MarketMosaikSim` segue; precisa do extra `mosaik` |
| `iec_61850` | `agent_example_iec_61850_1_updated.py` | agentes conversando com um IED IEC 61850; precisa do `pyiec61850`, instalado à parte |

Os protocolos dos exemplos 3 a 6 são os que o mercado usa. Os arquivos
`changelogs.md` (e `changelogs_en.md`, em inglês) de cada pasta dizem o que o
exemplo faz no PADE 3.0, o que foi corrigido na migração e quais mensagens ele
deve deixar em `messages.csv`.

## A atualização do PADE

A versão 2.2 do PADE, de 2021, declarava Python 3.7 e prendia o núcleo a uma
interface web em Flask e a um banco SQLite acessado pelo SQLAlchemy, com a
biblioteca Alchimia fazendo a ponte com o Twisted. O Alchimia não recebe
atualização desde 2018 e não importa a partir do SQLAlchemy 1.4, e o Twisted
fixado pela versão 2.2 não compila em Python 3.12. A migração removeu a camada
web e o banco, passou o registro para arquivos CSV e a operação para a linha de
comando `pade start-runtime`, e resultou na versão 3.0, publicada no PyPI como
`pade-agents`. O formato das mensagens ACL não mudou.

O histórico completo, com a comparação entre as versões, está em
[docs/atualizacao-pade.md](docs/atualizacao-pade.md), e o guia arquivo por
arquivo em [docs/MIGRACAO_GUIA.md](docs/MIGRACAO_GUIA.md).

## Autoria

Os agentes do mercado, a camada de rede e a migração do PADE para Python 3.12
foram desenvolvidos por Francisco Douglas Barros da Silva, no time TTESO. O
empacotamento do PADE 3.0 e a publicação no PyPI foram feitos pelo mantenedor
da plataforma, Lucas Silveira Melo. Para citar o PADE:

> Melo, L. S., Sampaio, R. F., Leão, R. P. S., Barroso, G. C., Bezerra, J. R.
> Python-based multi-agent platform for application on power grids. *Int Trans
> Electr Energ Syst.* 2019; 29:e12012. https://doi.org/10.1002/2050-7038.12012

Licença MIT, em [LICENSE](LICENSE).

<div align="center">
  <a target="_blank" href="https://github.com/grei-ufc" style="background:none">
    <img src="https://github.com/grei-ufc/tsdq-dataview-opentes/blob/main/imagens/Grei2.png?raw=true">
  </a>
</div>
