# Nano Forge

![](../../assets/machines/nano_forge.webp){ loading=lazy }

## Tiers

The nanite in an input bus sets the tier and **is never consumed**: Carbon T1, Neutronium T2, Transcendent T3, MagMatter T4. Each tier changes the structure. Perfect overclock on lower-tier recipes.

## Tier 4: MagMatter

With a nanite equal to the recipe output in the bus, the forge drains **all** molten MagMatter in the hatches. Parallel = `MagMatter / (288 / 2^(4 − recipe tier))`; duration × `0.9999^parallel`.
