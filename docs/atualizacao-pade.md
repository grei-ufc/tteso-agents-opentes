# A atualização do PADE: da versão 2.2 à 3.0

O PADE (Python Agent DEvelopment framework) é a plataforma de agentes do GREI.
Para que os agentes do mercado rodassem em Python 3.12, a versão usada por todos
os times do OpenTES, a plataforma precisou ser migrada. Esta página registra de
onde ela partiu, o que travava a atualização, o que mudou e o que ficou igual.

## O ponto de partida

A última versão no repositório [grei-ufc/pade](https://github.com/grei-ufc/pade)
antes da migração era a 2.2 (2.2.5 no código e 2.2.4 no PyPI, publicada em
janeiro de 2021, commit `2bc47e2` de outubro de 2022). Ela declarava Python 3.7
e fixava 18 dependências em versões exatas.

Além do núcleo de agentes, a 2.2 trazia dois recursos:

- **armazenamento das mensagens em banco de dados**, um arquivo SQLite acessado
  pelo SQLAlchemy;
- **interface web de gerenciamento**, um servidor Flask com autenticação de
  usuários, dezoito modelos de página e migrações de esquema.

Esses recursos não eram opcionais. O AMS (o agente que registra os demais) e o
Sniffer (o que registra as mensagens) importavam os modelos de dados (sessões,
usuários, agentes e mensagens) do próprio módulo do servidor web e gravavam no
banco a cada agente registrado e a cada lote de mensagens. O AMS chegava a pedir
usuário, e-mail e senha na partida, para criar o acesso à interface, de modo
que retirar a camada web era mexer no núcleo.

## O que travava

O SQLAlchemy é síncrono, e o PADE roda sobre o laço de eventos do Twisted. A
ponte entre os dois era a biblioteca **Alchimia**, e foi ela que travou a
atualização:

- a última versão do Alchimia, a 0.8.1, é de março de 2018;
- em Python 3.12, a importação do Alchimia falha a partir do SQLAlchemy 1.4.0,
  porque ela depende de uma classe interna que o SQLAlchemy removeu (testado
  com o SQLAlchemy 1.3.24, 1.4.0 e 1.4.54);
- o código do PADE também usava recursos que o SQLAlchemy 2.0 eliminou, como a
  execução direta de comandos pelo objeto de conexão e a ligação implícita entre
  metadados e banco;
- o Twisted 19.7, fixado pela versão 2.2, não compila em Python 3.12.

Manter o banco obrigaria a congelar o SQLAlchemy numa série sem manutenção, por
causa de recursos de que a comunicação entre agentes não depende.

## O que mudou

A migração, feita no fork [douglas-fdbs/pade2026](https://github.com/douglas-fdbs/pade2026)
e incorporada ao repositório do grupo pelos pull requests #85 (abril de 2026) e
#86 (maio de 2026), removeu a camada web e o banco e reescreveu as partes do
núcleo que dependiam deles: a linha de comando, o AMS, o Sniffer e a sessão. Foram
151 arquivos alterados na primeira etapa (`169fb47`, 30/03/2026) e 45 na segunda
(`27b9809`, 07/04/2026).

**Registro em CSV.** O banco deu lugar a quatro arquivos na pasta `logs/`:

| Arquivo | Quem grava | Conteúdo |
|---|---|---|
| `sessions.csv` | AMS | as sessões de execução |
| `agents.csv` | AMS | os agentes registrados |
| `messages.csv` | Sniffer | cada mensagem, com os metadados ACL e o conteúdo |
| `events.csv` | cada agente | eventos de envio e recebimento, criação e protocolos |

Uma sessão compartilhada, passada aos processos pela variável de ambiente
`PADE_SESSION_ID`, liga os registros de uma mesma execução.

**Linha de comando.** A interface web deu lugar ao comando
`pade start-runtime`, que sobe o AMS, o Sniffer e os scripts dos agentes como
processos separados. A opção `--detailed` mostra no terminal os rastros do AMS e
do Sniffer, para depuração, e os comandos `show-logs`, `export-logs`,
`clean-logs` e `version` cuidam dos registros.

**Dependências.** Com o Flask, o SQLAlchemy e o Alchimia fora, a lista caiu
para sete pacotes, com versões mínimas no lugar das exatas. Sobre essa base, o
mantenedor da plataforma, Lucas Silveira Melo, levou o empacotamento ao padrão
atual do Python (`pyproject.toml`, gerenciado pelo uv), reduziu as dependências
a quatro e publicou o resultado como versão 3.0 no PyPI, com o nome
`pade-agents` (abril de 2026).

**Núcleo.** As mudanças de comportamento foram pontuais:

- o driver de ligação com o Mosaik passou a tratar cada mensagem do orquestrador
  sempre como um gerador, a separar o tipo da mensagem do identificador recebido
  e a mostrar no terminal os erros devolvidos pelo Mosaik;
- o comportamento temporizado (`TimedBehaviour`) ficou definido como
  recorrente, e um disparo único passa a ser feito por agendamento simples.

**Exemplos.** Os exemplos da plataforma foram migrados e conferidos um a um, dos
agentes mínimos aos de sistemas de potência, à norma IEC 61850 e ao acoplamento
com o Mosaik. Cada pasta de `exemplos/` tem um `changelogs.md` com o que foi
verificado. Quem traz um agente da versão anterior precisa usar identificadores
de agente completos, com endereço e porta (`agente@localhost:20000`), e a sessão
compartilhada da execução; o resto está no [guia de migração](MIGRACAO_GUIA.md).

## O que ficou igual

O formato das mensagens não mudou. Os módulos da mensagem ACL
(`pade/acl/messages.py`) e dos identificadores de agente (`pade/acl/aid.py`) são
idênticos aos da versão 2.2, e os protocolos FIPA (Request, Contract Net e
Subscribe) seguem os mesmos.

## Comparação

| Aspecto | Versão 2.2 | Versão 3.0 |
|---|---|---|
| Python | 3.7 | 3.12 ou mais recente |
| Dependências | 18, fixadas em versões exatas, entre elas Flask e seis extensões, SQLAlchemy 1.3, Alchimia e Twisted 19.7 | quatro: Twisted, requests, click e terminaltables |
| Registro | banco SQLite, via SQLAlchemy e Alchimia | arquivos CSV de sessões, agentes, mensagens e eventos |
| Interface | servidor web Flask, com autenticação | linha de comando, `pade start-runtime` |
| Empacotamento | `setup.py` | `pyproject.toml`, com o uv |
| Publicação | `pade` 2.2.4, de 2021 | `pade-agents` 3.0, de 2026 |

## O custo

Com a camada web, a plataforma perdeu a interface de visualização das
mensagens. No OpenTES, essa função passa às ferramentas de análise, como as do
time TSDQ (qualidade de energia e análise de dados), que leem os arquivos CSV
sem depender de um servidor da própria plataforma.

## Fontes

- Repositório do grupo: <https://github.com/grei-ufc/pade>
- Fork da migração: <https://github.com/douglas-fdbs/pade2026>
- PADE 3.0 no PyPI: <https://pypi.org/project/pade-agents/>
- Alchimia no PyPI: <https://pypi.org/project/alchimia/>
