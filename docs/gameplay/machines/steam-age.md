# Steam age

GTNA turns the steam age into a full factory tier: large steam multiblocks with parallel, steam without pipes, machines that need no energy at all, and a steam elevator that reaches other planets. Every machine here has a [catalog page](catalog/index.md) with its structure.

## Steam supply

| Machine | What it gives |
|---|---|
| [Large Steam Solar Boiler](catalog/large_steam_solar_boiler.md) | expandable field of solar boiling cells, up to 63 blocks sideways and 125 back; output grows with sunlit cells. The only structure that takes the [wireless steam output hatch](../systems/wireless-steam-network.md) |
| [Cactus Wonder](catalog/steam_cactus_wonder.md) | burns coal and charcoal (8,000 mB of steam each) or coal blocks (90,000 mB), one item per second; needs fully grown cacti on its sand floor |
| [Large Steam Storage Tank](catalog/large_steam_storage_tank.md) | stores 120,000,000 mB of steam to smooth out boiler output |
| [Dimensionally Transcendent Steam Boiler](catalog/dimensionally_transcendent_steam_boiler.md) | a very large late boiler from GregTech Leisure |

Then carry the steam with the [wireless steam network](../systems/wireless-steam-network.md) instead of pipes.

## Large steam machines

Steam versions of the basic GregTech machines, ported from GT: Not Leisure: furnace, macerator, alloy smelter, compressor, extractor, forge hammer, lathe, cutter, bender, extruder, wiremill, forming press, sifter, mixer, centrifuge, thermal centrifuge, ore washer, chemical bath and circuit assembler.

- They run many items at once. The parallel cap depends on the machine and can be lowered in the controller:

    | Parallel | Machines |
    |---:|---|
    | 128 | Furnace, Crusher |
    | 96 | Ore Washer |
    | 64 | Alloy Smelter, Hammer, Mixer, Centrifuge, Thermal Centrifuge, Bath |
    | 48 | Compressor, Extractor |
    | 32 | Forming Press |
    | 16 | Lathe, Cutting Machine, Bending Machine, Extruder, Wiremill, Sifter |
    | 4 | Circuit Assembler |

- Each is faster than its single-block version: 10× for the Furnace, 5× for the Ore Washer, 2.5× for the Compressor and Forming Press, about 1.75× for the Alloy Smelter and Extractor, 2× for the rest.
- **High pressure:** build the structure with the steel casings instead of the bronze ones (every casing must be steel) and the machine runs 2× faster for 2× steam.
- Use [Huge Steam Buses](../parts/huge-steam-bus.md) (54 slots) to feed them.

Their recipes use GTNA's [hydraulic components](../systems/hydraulic-system.md), made by hand or in the **Steam Manufacturer**.

## Primitive machines

None of these uses EU. Only the Infernal Coke Oven uses steam.

| Machine | Highlights |
|---|---|
| [Infernal Coke Oven](catalog/infernal_coke_oven.md) | speeds up by 1% every 5 s up to 10×, and gains 16 parallel every 10 minutes (8 up to 256). Uses steam: 6,400 L/s plus 1,600 L/s per stage. The speed bonus decays while idle |
| [Hyper Pressure Reactor](catalog/hyper_pressure_reactor.md) | fluid reactions with no energy and no steam, 1 parallel; the Compact version has 512 |
| [Leap Forward One Blast Furnace](catalog/leap_forward_one_blast_furnace.md) | primitive blast furnace that grows: every extra layer doubles the parallel (up to 32,000) and adds 20 s to the 20 s cycle |
| [Primitive Stone Furnace](catalog/primitive_stone_furnace.md) | smelts every furnace recipe at once, each in 1 tick |
| [Brick Kiln](catalog/brick_kiln.md) | fires bricks and ceramics from compressed clay and coal |

## Specialists

| Machine | What it does |
|---|---|
| [Stone SuperHeater](catalog/stone_superheater.md) | super-heating recipes of the steam age, 32 parallel |
| [Steam Woodcutter](catalog/steam_woodcutter.md) | sapling in, logs out, 64 parallel |
| [Steam Cobbler](catalog/steam_cobbler.md) | rock breaker; the circuit picks the stone, 16 parallel |
| [Steam Manufacturer](catalog/steam_manufacturer.md) | Hydraulic Manufacturing, 16 parallel; builds the biggest steam machines |
| [Steam Supercompressor](catalog/steam_mega_compressor.md) | 256 parallel; made from 64 Large Steam Compressors |
| [Void Miner SteamGate Aged](catalog/void_miner_steam_gate_aged.md) | mines raw ores from nothing; see [void mining](../systems/void-mining.md) |

Most of them let you lower the parallel in the controller.

## Steam Elevator

The [Steam Elevator](catalog/steam_elevator.md) is a modular structure with up to 12 module slots. With Ad Astra installed, *Set out* opens the planet selection. Its modules only work while attached:

| Module | Tiers |
|---|---|
| Flight, Beacon, Weather, Monster Repellator, Entity Crusher, Oil Drill | I, II, III |
| Greenhouse Planting, Steam-Powered Apiary, Bee Breeding, Ore Processing | one each |

The Bee Breeding module exists only when Productive Bees is installed.

## Balance for modpacks

A modpack can scale the parallel and the duration of **every** GTNA steam multiblock from one place in Java (`GTNASteamBalance`), for example per difficulty.
