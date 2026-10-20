# Thread Hatch

Lets a multiblock run **different** recipes at the same time. A Parallel Hatch repeats one recipe; a Thread Hatch adds independent recipe slots, each with its own timer.

| Hatch | Extra threads | Total |
|---|---:|---:|
| ZPM | +1 | 2 |
| UV | +3 | 4 |
| UHV | +7 | 8 |
| UEV | +15 | 16 |
| UIV | +31 | 32 |
| UXV | +63 | 64 |
| OpV | +127 | 128 |
| MAX | +255 | 256 |

You can lower the number in the hatch UI. Values are in `config/gtna/balance/hatches.json` (`threadHatch`).

## Where it works

Threads work in machines built on GTNA's **multiple-recipes** logic whose structure has a slot for the hatch, for example the [Industrial Slaughterhouse](../machines/industrial-slaughterhouse.md), the Integrated Ore Processor and its advanced version, the Mega Distillery, the Dimensionally Transcendent Dirt Forge, the Primitive Stone Furnace and the Advanced Fusion Reactor's cross-recipe module. Packs can build more on that base with KubeJS.

## How threads share parallel

With a Parallel Hatch, the parallel is split between the threads. Example: a UEV Parallel Control Hatch (4,096) and a UV Thread Hatch (4 threads) give 4 recipes with 1,024 parallel each.
