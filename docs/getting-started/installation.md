# Installation

## Requirements

| Mod | Version | |
|---|---|---|
| Minecraft | 1.20.1 | required |
| Forge | 47.4.1 or newer | required |
| [GregTech CEu Modern](https://www.curseforge.com/minecraft/mc-mods/gregtechceu-modern) | 7.5.3 or newer | required; Forge stops with a message if it is older |
| [GTIA Lib](https://github.com/GTInfinityAscension/GTIA-Lib) | 0.5.0 or newer | required since GTNA 0.6.1 |
| [Applied Energistics 2](https://www.curseforge.com/minecraft/mc-mods/applied-energistics-2) | for 1.20.1 (tested with 15.4.10) | required: the ME parts are always registered |
| JEI or EMI | any recent | optional, strongly recommended: recipes and structure previews |
| KubeJS | 2001.6.5 | optional: [scripting API](../development/api/kubejs.md) |
| Ad Astra | 1.15.20 or newer | optional: planets for the Steam Elevator, the Eye of Harmony and the planetary void mining programs |
| FTB Teams / FTB Quests | — | optional: team progress for research and fluid discoveries, research quest task |
| Productive Bees | — | optional: the Steam Elevator Bee Breeding module |
| Jade | — | optional: wireless steam hatch details |

GTCEu needs its own dependencies (such as LDLib); install the versions its download page asks for. RenderBlender is **not** needed since GTNA 0.5.6.

## Steps

1. Install Forge 47.4.1 or newer for Minecraft 1.20.1.
2. Put GTCEu, GTIA Lib, Applied Energistics 2 and GTNA in the `mods` folder.
3. Add the optional mods you want.
4. Start the game once. GTNA writes `config/gtna.yaml` and the balance files in `config/gtna/balance/` (see [Configuration](configuration.md)).

Downloads: [GitHub releases](https://github.com/GTInfinityAscension/GregTech-Nexus-Addon/releases). Developers can also get release jars from the [organisation's Maven](https://gtinfinityascension.github.io/maven/).

## Servers

GTNA runs on dedicated servers. Install the same mods on the server and on every client; client-only options (HUDs, item effects) stay in each player's `config/gtna.yaml`.
