# Hatches and parts

GTNA's multiblock parts. Each one works only in structures that accept it: in JEI/EMI, hover a hatch position of the structure preview to see which parts fit there.

## Speed and parallel

| Part | Tiers | What it does |
|---|---|---|
| [Accelerate Hatch](accelerate-hatch.md) | LV–MAX | shortens every recipe, on top of the normal overclock |
| [Overclock Hatch](overclock-hatch.md) | UV–MAX | makes each overclock step cut more time |
| [Thread Hatch](thread-hatch.md) | ZPM–MAX | runs different recipes at the same time |
| [Parallel Control Hatch (UHV+)](advanced-parallel-hatch.md) | UHV–OpV | 1,024 to 262,144 parallel |

The three adjustable hatches have a small UI: open them to lower their effect when a recipe should run slower.

## Steam

| Part | What it does |
|---|---|
| Wireless Steam Input / Output Hatch | steam without pipes, see the [wireless steam network](../systems/wireless-steam-network.md) |
| [Huge Steam Input / Output Bus](huge-steam-bus.md) | steam item buses with 54 slots |

## AE2 and energy

Pattern Buffers, the Pattern Buffer Proxy, the ME Export Buffer and the storage access hatches are on the [ME Pattern Buffers](../systems/pattern-buffers.md) page. Wireless energy and dynamo hatches are on the [Nexus energy network](../systems/nexus-energy-network.md) page.

## Restricted parts {#restricted-parts}

These parts break normal balance. They exist for creative building, testing and packs that want them:

| Part | Tiers | What it does |
|---|---|---|
| Infinite Input Bus / Hatch | LV–MAX | compatible multiblocks read the items or fluids inside without consuming them |
| Output Boost Hatch, Item Bus and Fluid Hatch | LV–MAX | multiply recipe outputs: 25× up to MV, then 50×, 100×, 250×… up to 250,000× at MAX |
| Infinite Steam Input Bus | — | the steam version of the Infinite Input Bus |
| Output Boost Steam Output Bus | — | multiplies a steam multiblock's item outputs |

Each group can be turned off, hidden from JEI or stripped of its recipes in `config/gtna/balance/restricted_items.json`; see [Configuration](../../getting-started/configuration.md#restricted-items). Creative-only debug parts, without recipes, also exist for testing.
