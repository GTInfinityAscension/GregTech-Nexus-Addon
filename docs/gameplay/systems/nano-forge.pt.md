# Nano Forge

![Nano Forge](../../assets/machines/nano_forge.webp){ loading=lazy }

Fabrica nanites com quantidades enormes de energia. Trazida do GT: New Horizons.

## Tiers

A nanite em qualquer barramento de entrada define o tier da forja e **nunca é consumida**. Cada tier também pede uma estrutura maior; as partes extras são [módulos auxiliares](modules.md), então o JEI/EMI mostra cada tier numa página própria da prévia.

| Tier | Nanite no barramento |
|---|---|
| 1 | Nanites de Carbono |
| 2 | Nanites de Neutrônio |
| 3 | Nanites de Metal Transcendente |
| 4 | Nanites de MagMatter |

Receitas abaixo do tier da forja ganham **overclock perfeito**.

## Tier 4: MagMatter

Com uma nanite igual à saída da receita no barramento, a forja drena **todo** o MagMatter fundido dos hatches e transforma em paralelo:

$$
\begin{aligned}
\text{paralelo} &= \frac{\text{MagMatter}}{288 / 2^{\,4 - \text{tier da receita}}} \\
\text{duração} &\times 0{,}9999^{\text{paralelo}}
\end{aligned}
$$
