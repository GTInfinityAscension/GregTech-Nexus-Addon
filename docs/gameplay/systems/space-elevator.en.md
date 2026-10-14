# Space Elevator

![](../../assets/machines/space_elevator.webp){ loading=lazy }

## How it works

The elevator only powers modules above ZPM, with computation (`128 · (tier − ZPM)` CWU/t) and **256 Nanotube Spools** fed through its input bus. Up to 12 modules.

## Power Modules

The MK (I–V) of the Power Modules sets every module's parallel: `4^(MK − 1)`, and which Assembler Module recipes may run. All must share the same MK.

## Modules

**Assembler:** builds parts in orbit. **Resource Collection:** drones mining 20 asteroid ore mixes and collecting 11 gases, with MK I–VI drones and rocket fuel.
