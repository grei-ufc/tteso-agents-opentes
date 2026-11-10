# Rodar os exemplos do PADE

## Pelo runtime integrado

De dentro da pasta do exemplo:

```bash
cd exemplos/<exemplo>
uv run pade start-runtime --username pade_user --password 12345 --port 24000 <arquivo>.py
```

O `start-runtime` sobe o AMS (porta 8000), o Sniffer (8001) e o script, e grava a
sessão em `logs/` dentro da pasta. A porta de `--port` é a do primeiro agente; o
script recebe essa porta e numera os demais a partir dela. Encerre com Ctrl+C.

Para depurar, `--detailed` mostra no terminal também o que o AMS e o Sniffer
fazem:

```bash
uv run pade start-runtime --detailed --username pade_user --password 12345 --port 24000 <arquivo>.py
```

## Os exemplos com dependências

| Exemplo | Precisa de |
|---|---|
| `mosaik_example` | o extra `mosaik` (`uv sync --extra mosaik`) e dois terminais: o lado PADE e o cenário `first.py` (ver o `README.md` da pasta) |
| `iec_61850` | o `pyiec61850` e o servidor `server_iec61850.py` (ver o `README.md` da pasta) |
| `power_systems` | nada além do NumPy; o pacote `mygrid` do fluxo de potência vem na própria pasta |

## Conferir o resultado

O `changelogs.md` de cada pasta diz o que o exemplo deve deixar em
`logs/messages.csv`. No `agent_example_4`, por exemplo: 2 `cfp`, 2 `propose`, 1
`reject-proposal`, 1 `accept-proposal` e 1 `inform`.

```bash
uv run pade show-logs       # resumo da sessão
```

Os comandos de registro estão em [CLI do PADE](../reference/pade-cli.md). Para
apagar os registros entre execuções, `uv run pade clean-logs` ou apague a pasta
`logs/`.
