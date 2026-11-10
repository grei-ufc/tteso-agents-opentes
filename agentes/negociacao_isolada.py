#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Negociacao do mercado pelos agentes PADE, sem Mosaik, OpenDSS ou OMNeT++.

Na co-simulacao (co-simulation-opentes), quem dispara a negociacao e o Mosaik,
no passo 0 do dia, e quem a encerra e o `step_done` que devolve o passo a ele.
Aqui o disparo e feito pelo proprio reactor do Twisted, um segundo depois de os
agentes subirem, e o fim da negociacao encerra o processo. O resto e o mesmo
codigo da co-simulacao (`market_agents.py`): os mesmos agentes, os mesmos
protocolos FIPA, os mesmos modelos do pacote `market_opentes`.

So a fase de PROGRAMACAO (dia seguinte) roda isolada. A fase de operacao precisa
do relogio do Mosaik e do fluxo de potencia no OpenDSS, e fica na co-simulacao.

A camada de rede entre os agentes continua disponivel: `NET_BACKEND=lossy` com
`NET_DROP_PROBABILITY` sorteia perdas e atrasos, e `NET_TRACE` grava o traco de
mensagens. O backend `omnet` precisa do servidor 6TiSCH do co-simulation.

    uv run agentes/negociacao_isolada.py
    NET_BACKEND=lossy NET_DROP_PROBABILITY=0.05 uv run agentes/negociacao_isolada.py

O registro da negociacao vai para `resultados/negociacao/run.json` (ou para
`MARKET_RUN_DIR`).
"""

import os
import sys
from pathlib import Path

from market_opentes.config import DATA_DIR

# Os padroes do `market_agents.py` sao os caminhos do conteiner da co-simulacao.
# Fora dele, o caso vem do pacote `market_opentes` e a saida vai para a pasta
# atual. Variaveis ja definidas pelo usuario prevalecem.
os.environ.setdefault("MARKET_CONFIG", str(DATA_DIR / "config.json"))
os.environ.setdefault("MARKET_RUN_DIR", str(Path("resultados") / "negociacao"))
# Mesmo teto do docker-compose da co-simulacao; o padrao do modulo (30) para
# antes da convergencia, que na IEEE 13 por fase leva 42 rodadas.
os.environ.setdefault("MARKET_MAX_ROUNDS", "150")
if os.environ.get("MARKET_OPERATION", "0") != "0":
    print("[isolada] MARKET_OPERATION ignorado: a fase de operacao so roda na "
          "co-simulacao.", flush=True)
os.environ["MARKET_OPERATION"] = "0"
# No conteiner as pastas de saida ja existem; aqui o traco de mensagens pode
# apontar para uma pasta nova.
if os.environ.get("NET_TRACE"):
    Path(os.environ["NET_TRACE"]).parent.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(Path(__file__).resolve().parent))

import market_agents as ma                    # noqa: E402
from twisted.internet import reactor          # noqa: E402


def main():
    case, agents = ma.build_agents()
    market = agents[0]
    print(f"[isolada] {len(agents)} agentes: 1 mercado, 1 solver, 1 DSO, "
          f"{len(case.concentrators)} concentradores, "
          f"{len(case.prosumer_storage_nodes)} prosumidores", flush=True)

    # Sem Mosaik, liberar o passo e encerrar: o `run.json` e gravado no
    # desligamento do reactor (`start_market_loop`).
    market.mosaik_sim.release_step = lambda: reactor.callLater(0.5, reactor.stop)

    ams = {"name": ma.HOST, "port": ma.AMS_PORT}
    for agent in agents:
        agent.update_ams(ams)
    reactor.callWhenRunning(reactor.callLater, 1.0, market.start_negotiation)
    ma.start_market_loop(agents, case)


if __name__ == "__main__":
    main()
