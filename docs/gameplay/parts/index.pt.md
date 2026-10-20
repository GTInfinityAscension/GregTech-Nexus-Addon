# Hatches e partes

As peças de multibloco do GTNA. Cada uma só funciona em estruturas que a aceitam: no JEI/EMI, passe o mouse numa posição de hatch da prévia da estrutura para ver quais peças cabem ali.

## Velocidade e paralelo

| Peça | Tiers | O que faz |
|---|---|---|
| [Hatch de Aceleração](accelerate-hatch.md) | LV–MAX | encurta todas as receitas, além do overclock normal |
| [Hatch de Overclock](overclock-hatch.md) | UV–MAX | faz cada passo de overclock cortar mais tempo |
| [Hatch de Threads](thread-hatch.md) | ZPM–MAX | roda receitas diferentes ao mesmo tempo |
| [Hatch de Controle de Paralelismo (UHV+)](advanced-parallel-hatch.md) | UHV–OpV | de 1.024 a 262.144 de paralelo |

Os três hatches ajustáveis têm uma pequena interface: abra para diminuir o efeito quando uma receita deve rodar mais devagar.

## Vapor

| Peça | O que faz |
|---|---|
| Hatch de Entrada / Saída de Vapor Wireless | vapor sem canos, veja a [rede de vapor sem fio](../systems/wireless-steam-network.md) |
| [Barramento Grande de Entrada / Saída a Vapor](huge-steam-bus.md) | barramentos de itens a vapor com 54 slots |

## AE2 e energia

Pattern Buffers, o Pattern Buffer Proxy, o Buffer de Exportação ME e os hatches de acesso ao armazenamento estão na página [ME Pattern Buffers](../systems/pattern-buffers.md). Os hatches de energia e dínamo sem fio estão na página da [rede de energia Nexus](../systems/nexus-energy-network.md).

## Peças restritas {#restricted-parts}

Estas peças quebram o balanceamento normal. Existem para construção no criativo, testes e packs que queiram usá-las:

| Peça | Tiers | O que faz |
|---|---|---|
| Barramento / Hatch de Entrada Infinito | LV–MAX | multiblocos compatíveis leem os itens ou fluidos dentro sem consumir |
| Hatch, Barramento de Itens e Hatch de Fluido com Saída Ampliada | LV–MAX | multiplicam as saídas das receitas: 25× até MV, depois 50×, 100×, 250×… até 250.000× em MAX |
| Barramento de Entrada de Vapor Infinito | — | a versão a vapor do barramento de entrada infinito |
| Barramento de Saída a Vapor com Boost de Saída | — | multiplica as saídas de itens de um multibloco a vapor |

Cada grupo pode ser desligado, escondido do JEI ou ficar sem receitas em `config/gtna/balance/restricted_items.json`; veja [Configuração](../../getting-started/configuration.md#restricted-items). Também existem peças de depuração só do criativo, sem receita, para testes.
