# Roadmap

GTNA currently registers **168 multiblocks**. This page shows the progress of the requested ports and of the original multiblocks. It is generated from the project working documents, so it follows the code.

## Overall port progress

`████████████████░░░░░░░░░░░░░░` **46/86** (53%)

| Phase | Progress | Done |
|---|---|---|
| Phase A: required, and mechanics of existing endgame | `███████████████░░░░░` | 3/4 |
| Phase B: cheap and high value (GTO/GTL, few missing blocks) | `███████████████████░` | 18/19 |
| Phase C: medium (GTO, 2–5 missing blocks or own class) | `███████████████████░` | 21/22 |
| Phase D: expensive or large systems (GTO) | `█████░░░░░░░░░░░░░░░` | 4/16 |
| Phase E: GTNH 1.7.10 with no GTO/GTL equivalent | `░░░░░░░░░░░░░░░░░░░░` | 0/5 |
| Phase F: TST, GTNL and 123Tech with no GTO/GTL version | `░░░░░░░░░░░░░░░░░░░░` | 0/10 |
| Phase G: GTLAdditions | `░░░░░░░░░░░░░░░░░░░░` | 0/10 |

## Original multiblocks (in development)

Machines made for GTNA, with no equivalent in another mod. Each has a spec sheet (in Portuguese) with formulas, its own progression and an animated render.

| Machine | Tier | Status | Spec |
|---|---|---|---|
| Pressurized Water Reactor | IV | :material-progress-wrench: design done, implementation starting | [open](design/reator-pwr.md) |
| Kinetic Orbital Lance | UEV | :material-progress-wrench: in game, under test (WIP) | [open](design/lanca-cinetica-orbital.md) |
| Dimensional Rift Gate | UIV | :material-progress-wrench: in game, under test (WIP) | [open](design/portao-de-fenda.md) |
| Antimatter Collider Ring | UIV | :material-progress-wrench: in game, under test (WIP) | [open](design/anel-colisor.md) |
| Stellar Containment Chamber | MAX | :material-progress-wrench: in game, under test (WIP) | [open](design/camara-estelar.md) |

??? note "Phase A: required, and mechanics of existing endgame — 3/4"
    | Machine | Source | Status |
    |---|---|---|
    | Multiblocos BEC (Condensate Assembler + geradores/contenção) | GTNH (GT5U `BECRecipes`, tectech) | ✅ ported |
    | Convergence do DTPF | GTNH `MTEPlasmaForge` | ⏳ pending |
    | Nano Forge tier 4 | GTNH `MTENanoForge` | ✅ ported |
    | Hyperdimensional Plasma Fusion Core ("DTPF MK2") | GTO | ✅ ported |

??? note "Phase B: cheap and high value (GTO/GTL, few missing blocks) — 18/19"
    | Machine | Source | Status |
    |---|---|---|
    | Cracker Hub | GTO | ✅ ported |
    | Mega Distillation | GTL `mega_distillery` | ✅ ported |
    | Desulfurizer | GTO | ✅ ported |
    | Supercomputing Center | GTO | ✅ ported |
    | Research / Analysis Center | GTO `analysis_and_research_center` | ✅ ported |
    | Data Center | GTO | ✅ ported |
    | Giant Flotation Tank | GTO | ✅ ported |
    | Dimensional Focus Engraving Array | GTO | ✅ ported |
    | Phase Change Cube | GTO | ✅ ported |
    | Large Incubator | GTO | ✅ ported |
    | Mega Vacuum Drying | GTO | ✅ ported |
    | Mega Brewer | GTO | ✅ ported |
    | Engraving Laser Plant | GTO | ✅ ported |
    | Large Pyrolyse Oven | GTO/GTL | ✅ ported |
    | Infinity Fluid Drilling Rig | GTO | ✅ ported |
    | Star Ultimate Material Forge | GTO | ✅ ported |
    | Reaction Furnace | GTO | ✅ ported |
    | PCB Factory | GTO | ✅ ported |
    | Tiers da ISA Mill / Isa Factory | GTO `isa_mill` + 123Tech `OTEMegaIsaFactory` | ⏳ pending |

??? note "Phase C: medium (GTO, 2–5 missing blocks or own class) — 21/22"
    | Machine | Source | Status |
    |---|---|---|
    | Crystal Builder | GTO | ✅ ported |
    | Holy Separator | GTO/GTL (também no TST) | ✅ ported |
    | High Energy Laser Lathe | GTO | ✅ ported |
    | Neutronium Wire Cutting | GTO | ✅ ported |
    | Superconducting Magnetic Presser | GTO | ✅ ported |
    | Giant Electrochemical Workstation | GTO | ✅ ported |
    | Heavy Rolling | GTO | ✅ ported |
    | Hand of Arachne (tear) | GTO | ✅ ported |
    | Lightning Rod (gerador de arco) | GTO | ✅ ported |
    | Fuel Cell Generator | GTO | ✅ ported |
    | Giant Sintering Array | GTO | ✅ ported |
    | Particle Stream Matrix Filling | GTO | ✅ ported |
    | Extreme Compressor | GTO | ✅ ported |
    | Gemini Containment System | GTO | ✅ ported |
    | Space Probe Surface Reception | GTO | ✅ ported |
    | Integrated Vapor Deposition System | GTO | ✅ ported |
    | Integrated Assembler  / Integrated Assembly Facility | GTO (+ versões GTNL/TST) | ✅ ported |
    | Compound Extreme Cooling Unit | GTO | ✅ ported |
    | Hyper Naquadah Reactor / Advanced | GTO `hyper_reactor` / `advanced_hyper_reactor` | ✅ ported |
    | Nanites Circuit Assembly Factory | GTO | ✅ ported |
    | Rare Earth Centrifugal  / Advanced | GTO/GTL | ✅ ported |
    | Platinum Group Processing Hub | GTNL | ⏳ pending |

??? note "Phase D: expensive or large systems (GTO) — 4/16"
    | Machine | Source | Status |
    |---|---|---|
    | Space Elevator + módulos (Ore Extraction, drilling, assembly) | GTO | ✅ ported |
    | Road of Heaven | GTO | ⏳ pending |
    | Dyson Sphere Launch Silo + Receiving Station | GTO | ✅ ported |
    | Kerr-Newman Homogenizer | GTO | ✅ ported |
    | Nyarlathotep's Tentacle | GTO | ✅ ported |
    | Nano Phagocytosis Plant | GTO | ⏳ pending |
    | Plasma Centrifuge | GTO | ⏳ pending |
    | Stellar Forge | GTO | ⏳ pending |
    | Planetary Gas Collector | GTO | ⏳ pending |
    | Core Drilling Plant (`planet_core_drilling`) | GTO | ⏳ pending |
    | Petrochemical Plant | GTO | ⏳ pending |
    | Fuel Refining Complex | GTO | ⏳ pending |
    | Neutron Forging Anvil | GTO | ⏳ pending |
    | Transliminal Oasis | GTO | ⏳ pending |
    | Biochemical Extraction | GTO | ⏳ pending |
    | Fast Neutron Breeder Reactor | GTO | ⏳ pending |

??? note "Phase E: GTNH 1.7.10 with no GTO/GTL equivalent — 0/5"
    | Machine | Source | Status |
    |---|---|---|
    | Semi-Stable Antimatter Stabilization Sequencer | GoodGenerator `AntimatterForge` | ⏳ pending |
    | Pseudostable Black Hole Containment Field | GT5U `MTEBlackHoleCompressor` | ⏳ pending |
    | Industrial Arc Furnace | GT++ | ⏳ pending |
    | Endothermic Fridge | GT5U | ⏳ pending |
    | Mega Distillation Tower / Mega Oil Cracker | BartWorks | ⏳ pending |

??? note "Phase F: TST, GTNL and 123Tech with no GTO/GTL version — 0/10"
    | Machine | Source | Status |
    |---|---|---|
    | Hyper Thermal Convector | TST | ⏳ pending |
    | Magnetic Drive Pressure Former | TST | ⏳ pending |
    | Precise High-Energy Photonic Quantum Master | TST | ⏳ pending |
    | DTPF MK-II (`MM_…PlasmaForgePrototypeMK2`) | TST (modular) | ⏳ pending |
    | Eye of Harmony Injector | GTNL | ⏳ pending |
    | EGTW (Eternal GregTech Workshop) + módulos | GTNL (2.376 linhas) | ⏳ pending |
    | Vortex Matter Centrifuge, Field Forge Press, Horizontal Compressor, Mega Mixer, Nano Assembler Mk-50 | GTNL | ⏳ pending |
    | Tangshan Steel Mill | 123Tech | ⏳ pending |
    | Hyperdimensional Biebie Plasma Forge | 123Tech | ⏳ pending |
    | Ammonia Plant | Steam Reborn (gtsr) | ⏳ pending |

??? note "Phase G: GTLAdditions — 0/10"
    | Machine | Source | Status |
    |---|---|---|
    | Apocalyptic Torsion Quantum Matrix | QFT com 100% de chance, 1/10 do insumo probabilístico, 1024 threads + distort + neutron compressor | ⏳ pending |
    | Heart of the Universe | Genesis Engine: 4096× um Creative Laser por plano | ⏳ pending |
    | Fuxi Bagua Heaven Forging Furnace | 4 tipos de endgame do GTL | ⏳ pending |
    | Primordial Evolution Nexus | Tipo de receita próprio | ⏳ pending |
    | Biosphere III + módulos Garden of Hermes | Hospedeiro de módulos com laser | ⏳ pending |
    | Skeleton Shift Rift Engine | Decay hastener | ⏳ pending |
    | Space Scaling Instrument | Packer com bobina especial | ⏳ pending |
    | Planetary Ionisation Convergence Tower | Mecânica própria (classe ainda não lida) | ⏳ pending |
    | Inferno Cleft Smelting Vault | Pirólise + cracking | ⏳ pending |
    | Space Elevator MKII / Mega Space Elevator / Light Hunter Space Station | Hubs de módulos com paralelo máximo | ⏳ pending |

## How it works

- Only machines the author asked for are ported, from the named source (GTO, GTL, GTNL, TST, GTNH).
- Each port brings its original structure, mechanics and textures, with KubeJS support.
- Default recipes are a baseline; balance belongs to the modpack.
