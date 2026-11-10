# Primeiros agentes no PADE

Este tutorial percorre três exemplos, do agente mínimo ao protocolo que o mercado
usa nas rodadas, e mostra onde cada execução fica registrada. Não precisa do
CPLEX.

## Como um exemplo roda

Cada pasta de `exemplos/` é independente e roda de dentro dela:

```bash
cd exemplos/hello_world
uv run pade start-runtime --username pade_user --password 12345 --port 24000 hello_world.py
```

O `start-runtime` sobe três coisas, cada uma num processo:

| Processo | Porta | Papel |
|---|---|---|
| AMS | 8000 | registra os agentes e distribui os endereços |
| Sniffer | 8001 | grava as mensagens trocadas |
| o script dos agentes | a de `--port` em diante | os agentes do exemplo |

Usuário e senha vão na linha de comando para o terminal não parar pedindo
digitação. Encerre com Ctrl+C.

## 1. Hello world

O `hello_world.py` tem dois agentes: um envia uma mensagem `INFORM` e o outro a
recebe.

```text
[hello_receiver_24000] ... --> Hello World! Receiver online.
[hello_sender_25000] ... --> Hello World! Sender online.
[hello_sender_25000] ... --> Sending Hello World message to hello_receiver_24000
[hello_receiver_24000] ... --> Received message: Hello World Message!
```

O código mostra o padrão de todo agente no PADE 3.0: uma classe que herda de
`Agent`, um `on_start` que roda quando o agente sobe, um `react` que recebe as
mensagens, e um `ACLMessage` com destinatário, ontologia e conteúdo. O
`hello_world_minimal.py` é ainda menor, sem troca de mensagens.

## 2. Os registros

A execução fica em `exemplos/hello_world/logs/`:

```text
logs/
  sessions.csv    a sessão: quando começou e com que nome
  agents.csv      os agentes registrados no AMS
  messages.csv    a mensagem INFORM, gravada pelo Sniffer
  events.csv      envio, recebimento, inicialização do AMS e do Sniffer
```

O `messages.csv` tem uma linha por mensagem, com remetente, destinatários,
performativa, protocolo, conteúdo e ontologia. Como ler cada arquivo está em
[Ler os registros do PADE](../how-to-guides/read-pade-logs.md).

## 3. Contract Net

O mercado usa o FIPA Contract Net em cada ciclo da negociação. O
`agent_example_4` mostra o protocolo sozinho:

```bash
cd ../agent_example_4
uv run pade start-runtime --username pade_user --password 12345 --port 24000 agent_example_4_updated.py
```

Um iniciador envia um `CFP` a dois participantes, recebe duas propostas, rejeita
a menor e aceita a maior:

```text
[initiator_24000@localhost:24000] ... --> The best proposal was: 430.37812114210595 VA
[initiator_24000@localhost:24000] ... --> Sending REJECT_PROPOSAL answers...
[initiator_24000@localhost:24000] ... --> Sending ACCEPT_PROPOSAL answer...
[initiator_24000@localhost:24000] ... --> INFORM message received
```

No `messages.csv` ficam 2 `cfp`, 2 `propose`, 1 `reject-proposal`, 1
`accept-proposal` e 1 `inform`. No mercado, o iniciador é o concentrador (com
os prosumidores) ou o agente de mercado (com o concentrador e o operador), e a
proposta é uma programação de armazenamento.

## Para seguir

| Exemplo | O que acrescenta |
|---|---|
| `agent_example_3`, `script_3` | FIPA Request, usado pelo mercado para pedir os modelos ao agente solver |
| `agent_example_5`, `agent_example_6` | FIPA Subscribe, usado no despacho da programação acordada |
| `mosaik_example` | PADE com o mosaik, o padrão do simulador dos agentes na co-simulação |

A lista completa está em [Exemplos](../reference/examples.md).
