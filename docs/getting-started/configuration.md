# Configuration

GTNA has two kinds of settings:

- **`config/gtna.yaml`**: gameplay, client and per-machine switches. Every option also shows up in the in-game config menu, with a comment.
- **`config/gtna/balance/*.json`**: balance numbers for modpacks. They are read at startup; restart the game or server after editing.

## `config/gtna.yaml`

### gameplay

| Option | Default | Effect |
|---|---|---|
| `modDifficulty` | `NORMAL` | `JOURNEY` enables restricted utility items; `NORMAL` keeps them disabled |
| `selfRestraint` | `false` | disables restricted cheat-like GTNA items |
| `researchTree` | `true` | the [research tree](../gameplay/systems/research-engine.md) (K key, screen, commands); packs without nodes can turn it off |

### client

| Option | Default | Effect |
|---|---|---|
| `disableFlyInertia` | `true` | stops flight inertia when you stop moving in the air |
| `wirelessSteamHud` | `false` | wireless steam HUD: balance, flow and connected hatches |
| `wirelessSteamHudX`, `wirelessSteamHudY` | `5`, `75` | HUD position, 0 to 100 (percent of the screen) |
| `wirelessSteamHudHistorySeconds` | `60` | seconds of history in the HUD graph, 0 hides it |
| `wirelessEnergyHud` | `false` | Nexus energy HUD |
| `wirelessEnergyHudX`, `wirelessEnergyHudY` | `5`, `60` | its position |
| `itemHalo`, `itemGlowEdge`, `itemShaderEffects` | `true` | [item effects](../gameplay/systems/item-effects.md) |
| `itemEffectSpeed` | `100` | item effect animation speed, 0 to 400 % |

### machines

| Option | Default | Effect |
|---|---|---|
| `accelerateHatchEnergyCost` | `1.5` | EU multiplier while an [Accelerate Hatch](../gameplay/parts/accelerate-hatch.md) is active |
| `bufferDrivenMachineMode` | `true` | lets a [Pattern Buffer](../gameplay/systems/pattern-buffers.md) switch a GTCEu machine's mode while it is idle |
| `nexusPlannerEnabled` | `true` | crafting planner for Nexus ME Hypercore grids |
| `solarBoilerSteamPerCell` | `4000` | steam per sunlit cell per 20-tick cycle in the Large Steam Solar Boiler |
| `nexusFluxMatrix.useHighestTierForEfficiency` | `false` | the Flux Matrix uses its highest capacitor tier instead of the average |

### wirelessSteam {#wireless-steam}

| Option | Default | Effect |
|---|---|---|
| `enabled` | `true` | master switch of the [wireless steam network](../gameplay/systems/wireless-steam-network.md) |
| `bronzeInputBuffer` | `100000` | tank of the bronze input hatch, mB |
| `steelInputBuffer` | `2147483647` | tank of the steel input hatch |
| `bronzeOutputBuffer` | `128000000` | tank of the bronze output hatch |
| `steelOutputBuffer` | `2147483647` | tank of the steel output hatch |
| `bronzeTransferRate`, `steelTransferRate` | `2147483647` | optional per-tick limit; the default moves the whole tank |

### restrictedItems {#restricted-items}

| Option | Default | Effect |
|---|---|---|
| `hideFromJei` | `true` | hide restricted items from JEI and creative tabs when they are disabled |
| `disableRecipes` | `false` | remove the recipes of restricted items |
| `disableUsage` | `false` | block restricted items entirely, except the groups allowed below |
| `allowInfinityCovers`, `allowOutputBoostParts`, `allowInfiniteInputParts`, `allowQuantumCosmicNexusArmor`, `allowRealityRipper` | `true` | allow each group |

### machineToggles and hatchToggles

One `true`/`false` switch per machine family and per hatch family (for example `largeSteamFurnace`, `eyeOfHarmony`, `threadHatches`, `mePatternBuffer`). A disabled entry is **not registered**: only change these before a world is created, or blocks already placed will disappear.

## Balance files: `config/gtna/balance/`

| File | What it controls | Page |
|---|---|---|
| `machines.json` | Void Miner SteamGate Aged boosts | [Void mining](../gameplay/systems/void-mining.md) |
| `hatches.json` | Thread, Accelerate, Overclock and Output Boost values per tier | [Hatches and parts](../gameplay/parts/index.md) |
| `nexus_flux_matrix.json` | capacitor capacity and transfer per tier, loss policy | [Nexus energy network](../gameplay/systems/nexus-energy-network.md) |
| `pattern_buffers.json` | pattern slots per buffer (1 to 540) | [ME Pattern Buffers](../gameplay/systems/pattern-buffers.md) |
| `pattern_buffer_capacity_history.json` | largest slot count ever used; keep it with the world | same |
| `electric_void_miner.json` | Electric Void Miner costs, caps and parallel | [Void mining](../gameplay/systems/void-mining.md) |
| `void_fluid_drill.json` | Void Fluid Drilling Rig programs and parallel | same |
| `universal_factory.json` | Universal Factory parallel, threads and warm-up | [catalog](../gameplay/machines/catalog/universal_factory.md) |
| `restricted_items.json` | per group: enabled, hidden from JEI, recipes removed | [Hatches and parts](../gameplay/parts/index.md#restricted-parts) |

Restricted groups by default: infinity covers, Quantum Cosmic Nexus armor and the Reality Ripper are **off**; infinite input parts and output boost parts are **on**.

Missing keys fall back to their defaults, so a pack only needs to write the values it changes.
