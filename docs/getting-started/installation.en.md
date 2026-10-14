# Installation

## Requirements

| Mod | Version | Required |
|---|---|---|
| Minecraft | 1.20.1 | yes |
| Forge | 47.4.1 or newer | yes |
| GregTech CEu Modern | 7.5.3 or newer | yes |
| LDLib | the one bundled with GTCEu | yes (comes with GTCEu) |
| Ad Astra | 1.15.20 or newer | no: planets, Steam Elevator, Eye of Harmony beyond the Overworld |
| Stargate Journey | 0.6.44 or newer | no: portal integration |
| KubeJS | 2001.6.5 | no: scripts (see the KubeJS API) |
| Applied Energistics 2 | 15.x | no: Pattern Buffer, ME hatches, automation |
| JEI or EMI | any recent | no: recipes and structures |

!!! info "RenderBlender is no longer needed"
    Up to 0.5.5 material icon effects depended on RenderBlender. Since 0.5.6 GTNA has its own renderer.

## Steps

1. Install Forge 47.4.1 or newer for Minecraft 1.20.1.
2. Put GTCEu Modern and GTNA in the `mods` folder.
3. Add the optional mods you want.
4. Start the game once to generate `config/gtna.json`.

## Configuration

`config/gtna.json` has sections for gameplay, client, machines, restricted items, wireless steam and per-machine and per-hatch toggles. Every option has a name and comment in the in-game config menu.
