# A sequência da negociação

Os papéis e a sequência são os de Melo (2022, seção 6.1.2), aqui sobre o PADE
3.0. A negociação programa o armazenamento do dia seguinte inteiro, em 96
intervalos de 15 minutos.

## Os quatro ciclos

```mermaid
sequenceDiagram
    participant AM as Mercado (AM)
    participant AD as Operador (AD)
    participant AC as Concentrador (AC)
    participant AP as Prosumidores (AP)
    Note over AC,AP: ciclo 1
    AC->>AP: CFP: programação de armazenamento
    AP->>AC: propostas
    Note over AD,AC: ciclo 2
    AD->>AC: CFP: programação agregada
    AC->>AD: proposta
    Note over AM,AD: ciclo 3
    AM->>AC: CFP: análise
    AM->>AD: CFP: análise
    AC->>AM: proposta
    AD->>AM: proposta
    loop ciclo 4, até convergir
        AM->>AC: CFP com o preço sombra λ
        AM->>AD: CFP com o preço sombra λ
        AC->>AM: programação reotimizada (x)
        AD->>AM: programação reotimizada (y)
        AM->>AM: λ ← λ + α (x − y); testa |x − y|
    end
    AM->>AC: aceite
    AM->>AD: aceite
    AD->>AC: despacho (Subscribe)
    AC->>AP: despacho
    AP->>AC: confirmação
    AC->>AD: confirmação
    AD->>AM: despacho confirmado
```

| Ciclo | Quem pede | A quem | O quê |
|---|---|---|---|
| 1 | concentrador | prosumidores | cada prosumidor resolve o próprio modelo, uma vez, e devolve a programação |
| 2 | operador | concentradores | a programação agregada de cada concentrador |
| 3 | mercado | concentradores e operador | a primeira análise de cada lado |
| 4 | mercado | concentradores e operador | a cada rodada, os dois reotimizam com o preço sombra corrente |

O critério de parada padrão é relativo: a negociação fecha quando o desacordo
entre concentrador (x) e operador (y), em toda variável e intervalo, fica abaixo
de 0,1% da potência do próprio dispositivo. Na IEEE 13 por fase, são 42 rodadas.

## Os modelos ficam fora dos agentes

Os agentes não resolvem os modelos de otimização dentro de si: pedem ao agente
solver, por FIPA Request, que os resolve fora do laço de eventos do Twisted. Cada
rodada leva perto de um segundo de cálculo; feito dentro do laço, esse cálculo
travaria a recepção de mensagens dos 14 agentes, que dividem o mesmo processo. Os modelos vêm do
pacote `market_opentes`
([tteso-market-opentes](https://grei-ufc.github.io/tteso-market-opentes/)).

## Orçamento de tempo de cada ciclo

Na tese, os três primeiros ciclos acontecem em instantes fixos da janela de
15 minutos: o 1 no minuto 1, o 2 no minuto 5 e o 3 no minuto 10. Aqui esses
instantes são **orçamentos**, e não esperas:

| Ciclo | Nome no registro | Orçamento |
|---|---|---|
| 1 | `ciclo1_AC_AP` | 240 s |
| 2 | `ciclo2_AD_AC` | 300 s |
| 3 | `ciclo3_AM_AC_AD` | 300 s |

A camada de rede mede o tempo de rede de cada ciclo, e o `run.json` registra se
ele coube no orçamento. Com entrega ideal, o tempo de rede é zero.

## Sem AMS

No PADE, uma mensagem só é entregue se o destinatário estiver na tabela de
endereços do agente, e quem preenche essa tabela é o AMS, um processo separado.
Sem AMS, a tabela fica vazia e as mensagens são descartadas em silêncio.

Como os agentes do mercado são fixos e conhecidos na partida, a tabela é
preenchida direto, antes de os comportamentos começarem. Isso dispensa o AMS e
evita que o tráfego de registro e de manutenção dele se misture à medição de
comunicação. Por isso a negociação não gera os registros CSV do
`start-runtime`.

## Isolada e na co-simulação

Na co-simulação, quem dispara a negociação é o mosaik, no passo 0 do dia, e o
passo fica aberto até o acordo fechar; o fim da negociação devolve o passo ao
mosaik. No `negociacao_isolada.py`, o disparo é do próprio reactor, um segundo
depois de os agentes subirem, e o fim encerra o processo. O resto do código é o
mesmo.
