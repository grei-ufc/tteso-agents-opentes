# tteso-agents-opentes

**Agentes do mercado transativo do OpenTES sobre o PADE 3.0, e os exemplos da plataforma**

tteso-agents-opentes é um repositório do time **TTESO** (Sistemas Transativos e
Otimização) do projeto [OpenTES](https://github.com/grei-ufc/general-opentes),
do GREI-UFC. Ele traz os agentes que negociam o mercado transativo, trocando
mensagens FIPA-ACL sobre o [PADE](https://github.com/grei-ufc/pade) (Python
Agent DEvelopment framework), e os exemplos da plataforma usados no projeto.

O PADE é um projeto independente do GREI. Este repositório não copia o núcleo
dele: usa o pacote publicado [`pade-agents` 3.0](https://pypi.org/project/pade-agents/),
fruto da migração da plataforma para Python 3.12, documentada em
[A atualização do PADE](explanation/pade-update.md).

## O que o projeto permite

- Rodar a negociação do dia seguinte entre os agentes do mercado (prosumidores,
  concentrador, operador da rede e mercado) sem mosaik, OpenDSS ou OMNeT++
- Pôr um modelo de rede entre os agentes: entrega ideal ou perda e atraso
  sorteados, com o traço de cada mensagem
- Rodar os 16 exemplos do PADE 3.0, do agente mínimo aos protocolos FIPA, a
  sistemas de potência, à IEC 61850 e ao acoplamento com o mosaik
- Ler a sessão de cada execução nos registros CSV do PADE
- Migrar um agente escrito para o PADE 2.2

## Início rápido

```bash
git clone https://github.com/grei-ufc/tteso-agents-opentes.git
cd tteso-agents-opentes
uv sync
export MARKET_SOLVER_PATH=$HOME/IBM/CPLEX_Studio2211/cplex/bin/x86-64_linux/cplex
uv run agentes/negociacao_isolada.py
```

Os 14 agentes negociam e convergem em 42 rodadas. Consulte
[Instalação](getting-started/installation.md) e
[Primeira Negociação](getting-started/first-negotiation.md). Para começar pelos
exemplos do PADE, veja [Primeiros agentes no PADE](tutorials/first-pade-agents.md).

## Repositórios relacionados

| Repositório | O que tem |
|---|---|
| [tteso-market-opentes](https://grei-ufc.github.io/tteso-market-opentes/) | os modelos de otimização que os agentes chamam |
| [co-simulation-opentes](https://grei-ufc.github.io/co-simulation-opentes/) | a plataforma completa, onde estes agentes rodam com a rede de comunicação e a rede elétrica |
| [grei-ufc/pade](https://github.com/grei-ufc/pade) | a plataforma de agentes |

## Autoria

Os agentes do mercado, a camada de rede e a migração do PADE para Python 3.12
foram desenvolvidos por Francisco Douglas Barros da Silva, no time TTESO. O
empacotamento do PADE 3.0 e a publicação no PyPI foram feitos pelo mantenedor da
plataforma, Lucas Silveira Melo.

## Licença

MIT License, Smart Grids Research Group - UFC (Universidade Federal do Ceará), 2026
