# Original multiblocks

Machines designed for GTNA, with no equivalent in another mod. The four below are in the game and **under test**: numbers and recipes may still change. Each controller has its own screen with a **field manual** (chapters on how it works, in English, Portuguese and Chinese).

!!! warning "Work in progress"
    Report problems with these machines on the [issue tracker](https://github.com/GTInfinityAscension/GregTech-Nexus-Addon/issues).

| Machine | Tier | What it does | Only it makes |
|---|---|---|---|
| [Kinetic Orbital Lance](catalog/kinetic_orbital_lance.md) | UEV | fires projectiles at moons and asteroids from a capacitor bank and recovers the fragments in capsules | Primordial Tholin (Arrokoth), Nexium (Nexus-1) |
| [Dimensional Rift Gate](catalog/dimensional_rift_gate.md) | UIV | opens rifts to seeded dimensions; tune frequency, phase and amplitude until the rift holds | one exclusive material per biome: Prismatium, Chronomercury, Forgecore, Vivispore, Abyssal Antimatter, Precursor Residue, Void Ash |
| [Antimatter Collider Ring](catalog/antimatter_collider_ring.md) | UIV | collides counter-rotating beams for exotic particles and stores antiprotons in Penning traps | antiproton cells, Higgs and top particles |
| [Stellar Containment Chamber](catalog/stellar_containment_chamber.md) | MAX | holds a neutron star in field bands and sends the energy of its spin to the Nexus network | Magnetar Crystals, Degenerate Core Matter |

The four feed each other and the endgame: their products go into the Forge of the Gods, the Eye of Harmony field generators and the antimatter fuel rods.

## Kinetic Orbital Lance

- Survey each body to open it on the orbital map.
- Fit rails, coolers and sensors on the barrel bench. Shot energy is `½ m v²`, drawn from the whole capacitor bank.
- The impact regime (fragment, melt, vaporise) decides what comes back. Capsules return after the travel time.
- A worn liner misfires; a hot barrel drifts off target. Nexus-1 can only be hit with the Magnetar Slug.

## Dimensional Rift Gate

- Resonance comes from three tuning axes. Recorded harmonics form chords that shape the rift; dissonant chords dig deeper but cost more.
- SpaceTime keeps the rift stable; at 0 stability it collapses.
- Depth Anchors raise the output by `D^1.5`. From depth 40 each anchor also uses one Contained X-Nexus.

## Antimatter Collider Ring

- Beam energy follows `p = 0.3 · B · ρ`. Liquid helium cools the superconducting magnets; without it they quench.
- A particle gives its full yield once discovered with 5σ significance. Research proposals unlock stronger magnets and traps.
- Penning traps run on wireless EU; an unpowered trap annihilates its antimatter.

## Stellar Containment Chamber

- Up to `2^59` EU/t as a neutron star. Above 2.2 solar masses the star collapses into a black hole, which gives up to `2^62` EU/t from the ergosphere.
- Feeding mass spins the star up. Spinning it faster than the Kepler limit tears it apart.
- Starquakes decode the star and unlock band tiers; field bands left unpowered during a quake damage the containment. A magnetar uses one Forgecore plate every 60 s.

## Coming next

The **Pressurized Water Reactor** (IV) is designed and its implementation is starting. Progress is on the [roadmap](../../roadmap/index.md).
