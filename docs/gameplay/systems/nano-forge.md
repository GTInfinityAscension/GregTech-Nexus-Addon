# Nano Forge

![Nano Forge](../../assets/machines/nano_forge.webp){ loading=lazy }

Builds nanites with huge amounts of power. Ported from GT: New Horizons.

## Tiers

The nanite in any input bus sets the forge's tier and **is never consumed**. Each tier also needs a bigger structure; the extra parts are [auxiliary modules](modules.md), so JEI/EMI shows each tier as its own preview page.

| Tier | Nanite in the bus |
|---|---|
| 1 | Carbon Nanites |
| 2 | Neutronium Nanites |
| 3 | Transcendent Metal Nanites |
| 4 | MagMatter Nanites |

Recipes below the forge's tier get **perfect overclock**.

## Tier 4: MagMatter

With a nanite equal to the recipe's output in the bus, the forge drains **all** molten MagMatter in its hatches and turns it into parallel:

$$
\begin{aligned}
\text{parallel} &= \frac{\text{MagMatter}}{288 / 2^{\,4 - \text{recipe tier}}} \\
\text{duration} &\times 0.9999^{\text{parallel}}
\end{aligned}
$$
