# CLI do PADE

O pacote `pade-agents` instala o comando `pade`. Pelo uv, use `uv run pade ...`.

| Comando | O que faz |
|---|---|
| `pade start-runtime [opções] <arquivos>` | sobe o AMS, o Sniffer e os scripts de agentes num runtime integrado |
| `pade start-runtime-detailed` | o mesmo, com os rastros do AMS e do Sniffer no terminal |
| `pade show-logs` | resumo dos registros CSV gerados |
| `pade export-logs [csv\|json\|txt]` | exporta os registros para outro formato |
| `pade clean-logs` | apaga os registros e as exportações |
| `pade version` | a versão do PADE |

## `start-runtime`

| Opção | O que faz |
|---|---|
| `--port` | porta do primeiro agente; o script a recebe como argumento |
| `--num` | quantas instâncias do script |
| `--username`, `--password` | credenciais da sessão; na linha de comando, o terminal não para pedindo digitação |
| `--detailed` / `--no-detailed` | mostra ou esconde os rastros do AMS e do Sniffer |
| `--pade_ams` / `--no_pade_ams` | sobe ou não o AMS |
| `--pade_sniffer` / `--no_pade_sniffer` | sobe ou não o Sniffer |
| `--secure` | modo seguro |
| `--config_file` | lê as opções de um arquivo |

O AMS fica na porta 8000 e o Sniffer na 8001. Os registros vão para `logs/`
na pasta de onde o comando foi chamado
([Ler os registros do PADE](../how-to-guides/read-pade-logs.md)).

A documentação completa do PADE está em [grei-ufc/pade](https://github.com/grei-ufc/pade).
