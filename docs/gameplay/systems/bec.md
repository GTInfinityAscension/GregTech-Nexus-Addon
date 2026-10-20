# Bose-Einstein Condensate

![Entanglement Apparatus](../../assets/machines/bec_generator.webp){ loading=lazy }

A late-game crafting network ported from GT: New Horizons. Five multiblocks share **condensate**, an exotic resource made from molten metals, and use it with nanites to craft Condensate Assembly recipes.

## The network

The machines are linked by **BEC Conduits**. Dye conduits to split one network into several. Condensate is a network resource, like energy in a cable: it never sits in a hatch.

| Machine | Role |
|---|---|
| [Entanglement Apparatus](../machines/catalog/bec_generator.md) | turns molten metals and fluids into condensate, all fluids in its hatches at once. Parallel fills the available EU/t; the cycle lasts as long as the slowest recipe. Condensate is voided if the network has no room |
| [Containment Field](../machines/catalog/bec_storage.md) | stores condensate (see below) |
| [Maxwell Gate](../machines/catalog/bec_diode.md) | lets condensate flow one way, with per-type filters set by fluid input hatches. Uses 1A UIV while active and blocks the network while off |
| [Observation Array](../machines/catalog/bec_assembler.md) | feeds Teleportation Nodes linked by Line-of-Sight connectors with nanites, EU and condensate. One array serves many nodes. The nanite tier is the lowest among its buses; at most 30,720 nanites count |
| [Teleportation Node](../machines/catalog/bec_io_node.md) | crafts the recipes with its own buses (see below) |

## Crafting

The Teleportation Node crafts **Condensate Assembly** recipes:

- Each item slot asks for one nanite tier at a time.
- Extra nanites speed the craft up linearly. Higher-tier nanites than required slow it down by `2^(supplied − required)`.
- Condensate may arrive any time before the end of the craft. If it is still missing at the end, the craft fails.
- More than 3 condensate types the recipe did not ask for also fail the craft.
- No overclock. Minimum and maximum parallel and a speed divisor are set in the node's parameters.
- Nodes stall while their Observation Array lacks EU.

## Storage

In the **Containment Field**, 1 field strength stores 1 mB and costs 1 EU/t. Injected condensate is split between fields by capacity. Above capacity a field keeps 9/10 of each condensate per second.

!!! danger "Power loss"
    A Containment Field that loses power or is switched off **voids everything** it holds.
