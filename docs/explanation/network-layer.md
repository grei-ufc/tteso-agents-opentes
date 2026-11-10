# A camada de rede

No PADE 3.0, o envio de um agente vai direto para uma conexão TCP, e nenhuma
mensagem passa por um simulador de rede. A camada de rede
(`agentes/network_link.py`) põe um modelo de rede nesse caminho **sem tocar no
núcleo do PADE**: o método de envio de cada agente é substituído em tempo de
execução, e a entrega passa a ser agendada pelo modelo.

Ela substitui o módulo que, no PADE 2.2, desviava as mensagens para o simulador
ns-3, e que não existe mais.

## Os backends

| `NET_BACKEND` | O que faz |
|---|---|
| `ideal` | entrega tudo, sem atraso; é o caso de controle |
| `lossy` | sorteia a perda, e o atraso é propagação, mais a transmissão do tamanho da mensagem sobre a banda, mais um atraso aleatório exponencial; não precisa do OMNeT++ |
| `omnet` | pergunta ao servidor de rede do co-simulation-opentes, por ZMQ, o caminho, o atraso e a perda de cada mensagem: a rede 6TiSCH (ou Wi-SUN FAN) de Melo (2022, seção 6.1.5) |

Com `ideal` e sem `NET_TRACE`, a camada nem é instalada.

## O tempo

O atraso é aplicado no relógio do reactor do Twisted, porque na co-simulação a
negociação inteira acontece dentro de um passo do mosaik, com o relógio da
co-simulação parado. `NET_TIME_SCALE` comprime esse atraso: a rede de rádio
entrega em dezenas de segundos por mensagem, e com `0.02` o padrão temporal se
mantém e a execução fica viável. O que vai para o traço é o atraso nominal, sem
a compressão.

## Quem fala com quem

O canal `lossy` só precisa do tamanho da mensagem. O `omnet` precisa saber quem
fala com quem, porque o erro de pacote depende da distância entre os dois
rádios. A camada passa origem e destino em todos os backends, e traduz o nome de
cada agente para a posição dele no caso.

## O tamanho das mensagens

Com `NET_MESSAGE_SIZE=real`, o padrão, a rede recebe o tamanho do conteúdo
serializado em JSON. As mensagens da negociação com λ e programação por porta
têm de 11 a 34 kB, e numa rede de rádio de baixa taxa isso domina o tempo. Com
`declarado`, a rede recebe as classes de tamanho fixas da implementação de
referência, de 100 a 1.500 bytes, para comparação.
