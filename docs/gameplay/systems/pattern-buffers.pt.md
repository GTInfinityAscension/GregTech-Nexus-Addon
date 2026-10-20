# ME Pattern Buffers

Um Pattern Buffer é uma peça de multibloco que guarda patterns de processamento do AE2 e serve ao mesmo tempo de barramento de entrada, hatch de entrada e pattern provider. Ponha um num multibloco do GTCEu ou do GTNA e o AE2 manda as encomendas direto para ele. Precisa do Applied Energistics 2.

## Os quatro buffers

| Buffer | Slots de pattern (padrão) |
|---|---:|
| ME Mini Pattern Buffer | 9 |
| ME Pattern Buffer | 21 |
| ME Advanced Pattern Buffer | 32 |
| ME Ultimate Pattern Buffer | 72 |

A GUI mostra 90 slots por página. A quantidade de slots vem de `config/gtna/balance/pattern_buffers.json` (de 1 a 540 por buffer) e é lida na inicialização.

Os **cartões de upgrade** transformam um buffer no seguinte sem tirá-lo do lugar, mantendo patterns, ajustes dos slots e itens guardados: o Cartão de Expansão (21 slots), o Cartão de Precisão (32) e o Cartão de Ascensão (72). Os cartões de **Cópia** e **Recorte** levam uma configuração inteira: agache e clique direito num buffer para pegar, clique direito em outro para colar. Um buffer quebrado mantém patterns e dados dos slots.

## Ajustes por slot

Clique com o botão do meio num slot de pattern para editar:

- **Circuito:** um circuito programado só para aquele pattern. *Embutir Circuito*, na aba de ferramentas, grava um circuito em todos os patterns (com a opção de pular os que já têm).
- **Catalisadores (itens e fluidos):** ficam no slot e nunca são consumidos, como moldes, lentes ou um fluido catalisador.
- **Itens e fluidos fantasmas:** entradas extras somadas ao pattern com as quantidades que você escolher.
- **Modo preferido:** em multiblocos com vários tipos de receita, o modo em que aquele pattern deve rodar. Com `machines.bufferDrivenMachineMode` ligado (padrão), o buffer troca o modo de uma máquina do GTCEu enquanto ela está parada, então um Large Cutter corta e torneia pelo mesmo buffer.
- **Cache de receita:** o buffer lembra a receita que cada slot encontrou. Limpe depois de mudar receitas por script.

O **modo do buffer**, no topo, limita o buffer inteiro a um tipo de receita.

## Peças relacionadas

| Peça | O que faz |
|---|---|
| ME Pattern Buffer Proxy | deixa um segundo multibloco usar os patterns de um buffer em outro lugar. Agache e clique direito no buffer com um Data Stick, depois clique direito no proxy. Mesma dimensão, e o chunk do buffer precisa estar carregado |
| Buffer de Exportação ME | barramento e hatch de saída num bloco só: manda itens e fluidos direto para a rede ME. O buffer interno guarda até 9,2 × 10¹⁸ de cada item ou fluido, então a receita nunca trava com saída cheia |
| Hatch de Pattern de Craft Nexus | recebe patterns de bancada para a [Forja de Montagem Nexus](../machines/catalog/nexus_molecular_forge.md) |
| Hatch de Acesso ao Armazenamento ME / a Grande Armazenamento ME | liga o multibloco [ME Storage](../machines/catalog/me_storage.md) a uma rede AE2; a versão grande conta além de 64 bits |

## Dicas

- Um buffer por linha de produção é mais fácil de ler que um buffer gigante: o Pattern Access Terminal do AE2 lista cada buffer separado. Um buffer também pode ficar oculto nesse terminal.
- Se um pattern não faz nada, abra o slot: circuito faltando ou modo preferido errado é a causa mais comum.
- Quando um modpack diminui a quantidade de slots, o GTNA mantém o tamanho antigo nos buffers que já estão no mundo (`pattern_buffer_capacity_history.json`). Guarde esse arquivo junto com o mundo.
