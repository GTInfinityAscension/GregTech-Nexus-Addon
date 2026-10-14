# Bose-Einstein Condensate

![](../../assets/machines/bec_generator.webp){ loading=lazy }

## Condensate network

Five multiblocks linked by **BEC conduits** (dye them to split networks). Condensate is a network resource, like energy: it does not sit in hatches.

## Machines

| Machine | Role |
|---|---|
| Entanglement Apparatus | makes condensate from molten metals; parallels up to the available EU/t |
| Containment Field | stores condensate (section below) |
| Maxwell Gate | lets condensate flow one way, with filters; 1A UIV while active |
| Observation Array | feeds the nodes by line of sight with nanites, EU and condensate; up to 30,720 nanites |
| Teleportation Node | crafts the recipes (section below) |

## Step-by-step crafting

The **Teleportation Node** crafts Condensate Assembly recipes with its own buses. Each item slot asks for one nanite tier at a time; extra nanites speed it up linearly; higher-tier nanites slow it by `2^(supplied − required)`. Condensate may arrive any time before the end; if it is missing at the end, the recipe fails.

## Storage

In the **Containment Field**, 1 strength stores 1 mB and costs 1 EU/t. Above capacity it keeps 9/10 of each condensate per second. **Without power or when off, it destroys everything.**
