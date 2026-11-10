# Exemplos

Os exemplos do PADE 3.0, em `exemplos/`, vêm do repositório da migração
([douglas-fdbs/pade2026](https://github.com/douglas-fdbs/pade2026)) e são os
mesmos da imagem `opentes/pade` do co-simulation-opentes. Cada pasta é
independente; como rodar está em
[Rodar os exemplos do PADE](../how-to-guides/run-pade-examples.md).

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
| `mosaik_example` | `agent_example_1_mosaik_updated.py` + `first.py` | co-simulação PADE + mosaik, o padrão que o simulador dos agentes do mercado segue |
| `iec_61850` | `agent_example_iec_61850_1_updated.py` | agentes conversando com um IED IEC 61850 |

## Os changelogs

Cada pasta tem `changelogs.md` (português) e `changelogs_en.md` (inglês), com:

- o objetivo do exemplo no PADE 3.0;
- o estado verificado: arquivo principal, comando recomendado, sessão
  compartilhada e identificadores de agente completos;
- o que foi corrigido na migração;
- os registros esperados em `messages.csv`, `agents.csv` e `events.csv`.

## Os protocolos do mercado

| Protocolo | Exemplos | Uso no mercado |
|---|---|---|
| FIPA Contract Net | `agent_example_4`, `script_2`, `script_4` | os ciclos da negociação: CFP, proposta, aceite ou rejeição |
| FIPA Request | `agent_example_3`, `script_3` | os agentes pedem a solução dos modelos ao agente solver |
| FIPA Subscribe | `agent_example_5`, `agent_example_6` | o despacho da programação acordada |
