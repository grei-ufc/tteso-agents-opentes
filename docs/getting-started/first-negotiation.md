# Primeira Negociação

Este passo a passo roda a negociação do dia seguinte entre os agentes do mercado,
sem mosaik, OpenDSS ou OMNeT++, no cenário padrão: análise por fase, inversor de
quatro fios e entrega ideal das mensagens. Pressupõe a
[Instalação](installation.md) feita e o solver apontado.

## Rodar

```bash
uv run agentes/negociacao_isolada.py
```

Leva menos de um minuto. Os agentes sobem a partir da porta 5678, numa só
máquina:

```text
[isolada] 14 agentes: 1 mercado, 1 solver, 1 DSO, 1 concentradores, 10 prosumidores
[market-mas] pronto: 14 agentes ouvindo a partir da porta 5678
[market] ... --> iniciando a fase de programacao
```

## O que acontece

Um segundo depois de subir, o agente de mercado abre a negociação, nos quatro
ciclos da tese ([A sequência da negociação](../explanation/negotiation-sequence.md)):

1. o concentrador pede a programação de armazenamento a cada um dos 10
   prosumidores (a barra `CFP responses received` mostra as respostas chegando);
2. o operador (DSO) pede ao concentrador a programação agregada;
3. o mercado pede as análises ao concentrador e ao operador;
4. concentrador e operador reotimizam com o preço sombra corrente, e o mercado
   o atualiza, rodada a rodada:

```text
[market] ... --> rodada 1: |dlambda|=3.419e+02 |x-y|=300.0000 kW (2.0e+00 de Pmax)
[market] ... --> rodada 2: |dlambda|=1.812e+02 |x-y|=222.1894 kW (1.5e+00 de Pmax)
```

`|x-y|` é o desacordo entre concentrador e operador. A negociação fecha quando
ele fica abaixo de 0,1% da potência de cada dispositivo. Depois, o operador
despacha a programação acordada por FIPA-Subscribe, e as confirmações sobem:

```text
[market] ... --> acordo fechado; iniciando o despacho
[concentrator_alimentador_650] ... --> despachando 7 armazenamentos de rede e repassando a 10 prosumidores
[market] ... --> despacho confirmado por todos
[market] ... --> negociacao encerrada: convergiu em 42 rodadas, 0 retransmissoes
[mercado] execucao gravada em resultados/negociacao/run.json
```

O processo encerra sozinho.

## O resultado

`resultados/negociacao/run.json` tem a configuração da execução, o número de
rodadas, o histórico de cada rodada e as retransmissões
([Arquivos de saída](../reference/output-files.md)).

O histórico é o mesmo da negociação centralizada do
[tteso-market-opentes](https://grei-ufc.github.io/tteso-market-opentes/): 42
rodadas, com o desacordo final de 0,136 kW nos dois. A diferença está na sexta
casa decimal, do arredondamento das mensagens em JSON.

## Próximos passos

- [Negociação com perda de mensagens](../tutorials/negotiation-with-losses.md)
- [Agentes e protocolos](../reference/agents-and-protocols.md)
- [Primeiros agentes no PADE](../tutorials/first-pade-agents.md), para entender a
  plataforma pelos exemplos
