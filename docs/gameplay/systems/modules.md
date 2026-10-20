# Modules and the Structure Terminal

## Auxiliary modules {#auxiliary-modules}

Some multiblocks accept an **auxiliary module**: an optional extra structure built next to the main one and checked by the same controller. The machine forms without it. When the module forms, the hatches found in it are added to the machine, which unlocks new hatch types or new recipe types. The controller shows *Formed modules: n / total*, JEI/EMI shows each module as an extra page of the structure preview, and the item tooltip lists what the module unlocks.

| Machine | What the module adds |
|---|---|
| Electric Blast Furnace (GTCEu) | Accelerate Hatch and extra wired Energy Hatches |
| Liquefaction Furnace | Parallel Hatch and Accelerate Hatch |
| Evaporation Plant | Parallel Hatch and Accelerate Hatch |
| Cold Ice Freezer | Atomization Condensation recipes, an Accelerate Hatch and up to six extra Energy Hatches |
| Component Assembler | two extension shapes (normal and wide) with more hatches |
| Rocket Large Turbine | 2× output, +20% efficiency, 2× rotor damage, up to three extra Energy Output Hatches |
| Supercritical Steam Turbine | same bonuses as the Rocket Large Turbine module |
| Advanced Fusion Reactor | four tier modules (MK-II to MK-V) and a cross-recipe module |
| Nano Forge | the tier 2, 3 and 4 structures |

Modpacks can add modules to any multiblock, GTNA's or another mod's, with KubeJS: see [`GTNAServerEvents.subPatterns`](../../development/api/kubejs.md#auxiliary-modules). The module registry lives in GTIA Lib since GTNA 0.6.1.

## Nexus Structure Terminal {#nexus-structure-terminal}

A builder for big multiblocks.

- **Right-click** in the air: settings.
- **Shift + right-click** a controller: builds the structure around it, modules included.

| Setting | Effect |
|---|---|
| Blocks by tier | pick the coil, casing or glass tier to place, per category |
| Repetitions (0–1000) | layers for expandable structures such as a distillation tower |
| Module build (0–100) | how many module layers to build |
| No Hatch | skips buses and hatches, so you can place them yourself |
| Replace | swaps blocks already in place (coils of another tier, for example) for your choice; the old blocks go to your inventory |
| Mirror | builds the mirrored version of the structure |
| Demolition | clears blocks that stand where the structure needs air |

In survival the terminal takes blocks from your inventory. Right-click an AE2 Wireless Access Point with it to also take blocks from that ME network while you are in range.
