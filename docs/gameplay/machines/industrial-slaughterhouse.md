# Industrial Slaughterhouse

![Industrial Slaughterhouse](../../assets/machines/industrial_slaughterhouse.webp){ loading=lazy }

Virtual mob farming: the machine rolls the vanilla loot tables of the chosen mob group, with no mobs in the world. [Catalog page](catalog/industrial_slaughterhouse.md).

## Modes

Put a programmed circuit in the input bus:

| Circuit | Mode | Mobs | From | EU/t | Drop multiplier |
|:---:|---|---|---|---:|---|
| 1 | Passive | chicken, cow, pig, sheep, rabbit, horse, goat | LV | 1,000 | $2^{\,\text{tier} - \text{LV}}$ |
| 2 | Hostile | zombie, skeleton, creeper, spider, enderman, witch, blaze | MV | 2,560 | $2^{\,\text{tier} - \text{MV}}$ |
| 3 | Bosses | warden, wither, elder guardian | ZPM | 32,000 | $3^{\,\text{tier} - \text{ZPM}}$ |
| 4 | Dragon | 1 Dragon Egg, 4 Dragon's Breath, 1 Dragon Head | UHV | 120,000 | $5^{\,\text{tier} - \text{UHV}}$ |

Each run lasts 40 ticks. The tier is the machine's energy tier. Below the mode's starting tier the machine produces nothing.

## How much it drops

Each run repeats $\max(1,\ (\text{tier} - 2) \times 8)$ times: once at LV and MV, 8 at HV, 16 at EV, 24 at IV and so on. Every repeat picks a random mob of the group, rolls its loot table and multiplies each drop by the mode's multiplier, **capped at one stack** per drop.

| Tier | Repeats | Passive | Hostile | Bosses | Dragon |
|---|---:|---:|---:|---:|---:|
| LV | 1 | 1× | — | — | — |
| MV | 1 | 2× | 1× | — | — |
| HV | 8 | 4× | 2× | — | — |
| EV | 16 | 8× | 4× | — | — |
| IV | 24 | 16× | 8× | — | — |
| LuV | 32 | 32× | 16× | — | — |
| ZPM | 40 | 64× | 32× | 1× | — |
| UV | 48 | 128× | 64× | 3× | — |
| UHV | 56 | 256× | 128× | 9× | 1× |
| UEV | 64 | 512× | 256× | 27× | 5× |

Each drop is capped at one stack (64 for most items), so above 64× the multiplier adds nothing more; the extra repeats still do. Since drops come from the real loot tables, mods and datapacks that change mob loot also change this machine.

## Tips

- Give it several output buses: high tiers produce many stacks per run.
- It runs on GTNA's multiple-recipes logic and accepts the [Thread](../parts/thread-hatch.md), [Accelerate](../parts/accelerate-hatch.md) and [Overclock](../parts/overclock-hatch.md) Hatches.
- The GUI shows the current mode, the multiplier and the last drops.
