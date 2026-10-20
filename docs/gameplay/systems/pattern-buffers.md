# ME Pattern Buffers

A Pattern Buffer is a multiblock part that holds AE2 processing patterns and acts as input bus, input hatch and pattern provider at once. Put one on a GTCEu or GTNA multiblock and AE2 can send it crafting jobs directly. Requires Applied Energistics 2.

## The four buffers

| Buffer | Pattern slots (default) |
|---|---:|
| ME Mini Pattern Buffer | 9 |
| ME Pattern Buffer | 21 |
| ME Advanced Pattern Buffer | 32 |
| ME Ultimate Pattern Buffer | 72 |

The GUI shows 90 slots per page. Slot counts come from `config/gtna/balance/pattern_buffers.json` (1 to 540 per buffer) and are read at startup.

**Upgrade cards** turn a buffer into the next one in place, keeping patterns, slot settings and stored items: the Expansion Card (21 slots), the Precision Card (32) and the Ascension Card (72). **Copy** and **Cut** cards move a whole configuration: sneak-right-click a buffer to take it, right-click another to paste it. A broken buffer keeps its patterns and slot data.

## Per-slot settings

Middle-click a pattern slot to edit it:

- **Circuit:** a programmed circuit for that pattern only. *Embed Circuit* in the tools tab writes one circuit into every pattern (optionally skipping patterns that already have one).
- **Catalyst items and fluids:** kept in the slot and never consumed, such as molds, lenses or a catalyst fluid.
- **Ghost items and fluids:** extra inputs added to the pattern with your own amounts.
- **Preferred mode:** for multiblocks with several recipe types, the mode this pattern should run in. With `machines.bufferDrivenMachineMode` on (default), the buffer switches a GTCEu machine's mode while it is idle, so one Large Cutter can cut and lathe from the same buffer.
- **Recipe cache:** the buffer remembers which recipe each slot resolved to. Clear it after you change recipes with scripts.

A **buffer mode** at the top limits the whole buffer to one recipe type.

## Related parts

| Part | What it does |
|---|---|
| ME Pattern Buffer Proxy | lets a second multiblock use the patterns of a buffer elsewhere. Shift-right-click the buffer with a Data Stick, then right-click the proxy. Same dimension, and the buffer's chunk must be loaded |
| ME Export Buffer | output bus and output hatch in one block: sends items and fluids straight to the ME network. Its internal buffer holds up to 9.2 × 10¹⁸ of each item or fluid, so recipes never stall on a full output |
| Nexus Craft Pattern Hatch | takes crafting-table patterns for the [Nexus Assembly Forge](../machines/catalog/nexus_molecular_forge.md) |
| ME Storage Access Hatch / Big Storage Access Hatch | connects the [ME Storage](../machines/catalog/me_storage.md) multiblock to an AE2 network; the big version counts beyond 64-bit |

## Tips

- One buffer per production line is easier to read than one huge buffer: AE2's Pattern Access Terminal lists each buffer separately. A buffer can also be hidden from that terminal.
- If a pattern does nothing, open the slot: a missing circuit or a wrong preferred mode is the usual cause.
- When a modpack lowers the slot count, GTNA keeps the old size for buffers already in the world (`pattern_buffer_capacity_history.json`). Keep that file with the world.
