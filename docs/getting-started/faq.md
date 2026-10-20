# FAQ

??? question "The game stops with a missing dependency message"
    GTNA 0.6.1 needs **GTCEu 7.5.3 or newer** and **GTIA Lib 0.5.0 or newer**. An older GTCEu caused crashes like `NoSuchFieldError: CLUSTER_MAX_HARVESTABLES` (issue #1). Update both mods. See [Installation](installation.md).

??? question "GTNA material icons show as missing textures"
    GTNA 0.5.4 and 0.5.5 depended on RenderBlender for those models. Update to 0.5.6 or newer, which draws the effects itself.

??? question "Can I turn the item effects (halos, shaders) off?"
    Yes, in `config/gtna.yaml`, `client` section: `itemHalo`, `itemGlowEdge`, `itemShaderEffects` and `itemEffectSpeed`. See [Item effects](../gameplay/systems/item-effects.md).

??? question "My structure does not form"
    Open the structure in JEI/EMI and compare layer by layer; hover each position to see what fits there. Check that every casing has the same tier where the machine asks for it (steam machines in high-pressure mode need **all** casings in steel). The [Nexus Structure Terminal](../gameplay/systems/modules.md#nexus-structure-terminal) can build it for you.

??? question "The wireless steam output hatch does nothing on my boiler"
    It only fits the Large Steam Solar Boiler and never accepts steam from pipes. See [Wireless steam network](../gameplay/systems/wireless-steam-network.md).

??? question "A Pattern Buffer pattern never runs"
    Middle-click the slot: a missing programmed circuit or the wrong preferred mode is the usual cause. See [ME Pattern Buffers](../gameplay/systems/pattern-buffers.md).

??? question "The recipes are different from GTNH or GTO"
    GTNA ships working default recipes. Balance belongs to the modpack, which can change them through KubeJS, datapacks and the balance files in `config/gtna/balance/`.

??? question "Do I need Ad Astra?"
    No. Without it the Steam Elevator cannot travel, the Eye of Harmony only has the Minecraft dimensions and the planetary void mining programs are missing.

??? question "Where do I report a bug?"
    On the [issue tracker](https://github.com/GTInfinityAscension/GregTech-Nexus-Addon/issues), with `latest.log` (and `crash-reports/` if the game crashed) and the versions of GTNA, GTCEu and GTIA Lib.

??? question "Can I translate the wiki or the mod?"
    Yes, see [Translating](../development/translating.md).
