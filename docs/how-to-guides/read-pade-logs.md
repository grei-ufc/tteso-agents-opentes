# Ler os registros do PADE

No PADE 3.0, cada execução pelo `pade start-runtime` grava quatro arquivos CSV
em `logs/`, na pasta de onde o comando foi chamado.

## Os arquivos

| Arquivo | Quem grava | Colunas |
|---|---|---|
| `sessions.csv` | AMS | `timestamp`, `session_id`, `name`, `state` |
| `agents.csv` | AMS | `timestamp`, `agent_id`, `session_id`, `name`, `state` |
| `messages.csv` | Sniffer | `timestamp`, `message_id`, `conversation_id`, `agent_id`, `performative`, `protocol`, `sender`, `receivers`, `content`, `ontology`, `language` |
| `events.csv` | cada agente, o AMS e o Sniffer | `timestamp`, `event_type`, `agent_id`, `data` |

Os quatro se ligam pela sessão da execução, passada a todos os processos pela
variável `PADE_SESSION_ID`. O `messages.csv` e o `events.csv` não têm coluna de
sessão: para separar execuções, limpe `logs/` entre elas.

## Exemplos de leitura

Quantas mensagens de cada performativa:

```bash
cut -d, -f5 logs/messages.csv | sort | uniq -c
```

Os tipos de evento de uma execução:

```bash
cut -d, -f2 logs/events.csv | sort | uniq -c
```

No hello world aparecem, entre outros, `runtime_started`, `ams_initialized`,
`sniffer_initialized`, `message_sent`, `message_received` e `message_stored`.

Com pandas:

```python
import pandas as pd

msgs = pd.read_csv("logs/messages.csv")
msgs.groupby(["sender", "performative"]).size()
```

## E os agentes do mercado?

A negociação isolada (`agentes/negociacao_isolada.py`) não usa o
`start-runtime`: os 14 agentes sobem num processo só, com os endereços
preenchidos direto, sem AMS nem Sniffer. Por isso ela não grava em `logs/`. O
registro dela é o `run.json` e, com `NET_TRACE`, o traço de mensagens
([Arquivos de saída](../reference/output-files.md)). O motivo está em
[A sequência da negociação](../explanation/negotiation-sequence.md#sem-ams).
