# Accelerate Hatch

Shortens every recipe of the multiblock, on top of the normal overclock. Ported from GregTech Odyssey.

| | |
|---|---|
| **Tiers** | LV to MAX |
| **Fits** | electric multiblocks (GTCEu and GTNA) whose structure accepts it, and the [auxiliary modules](../systems/modules.md) that add it |
| **Per machine** | one |

## Duration

The value is the duration left, in percent of the original:

| Hatch | Duration | Hatch | Duration |
|---|---:|---|---:|
| LV | 50% | UV | 36% |
| MV | 48% | UHV | 34% |
| HV | 46% | UEV | 32% |
| EV | 44% | UIV | 30% |
| IV | 42% | UXV | 28% |
| LuV | 40% | OpV | 26% |
| ZPM | 38% | MAX | 24% |

The formula is $50 - 2 \cdot (\text{tier} - 1)$ percent. You can raise the value in the hatch UI, up to 100% (no effect).

## Penalty

For each tier the **recipe** is above the hatch, add 20 points. A low-tier recipe in a high-tier machine is never penalised.

!!! example
    An HV hatch (46%) running an EV recipe: 46% + 20% = 66%. A 100-tick recipe takes 66 ticks.

The final value stays between 1% and 100%. Values are in `config/gtna/balance/hatches.json` (`accelerateHatch`), and the EU cost multiplier is `machines.accelerateHatchEnergyCost` in `config/gtna.yaml` (default 1.5).

## With other hatches

Everything multiplies: $\text{duration} = \text{base} \times \text{overclock steps} \times \text{accelerate}$. See the [Overclock Hatch](overclock-hatch.md) for an example.
