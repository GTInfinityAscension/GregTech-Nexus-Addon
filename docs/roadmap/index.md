# Roadmap

O GTNA tem hoje **164 multiblocos** registrados. Esta página mostra o andamento dos ports pedidos e dos multiblocos originais. Ela é gerada a partir dos documentos de trabalho do projeto, então acompanha o que está no código.

## Progresso geral dos ports

`████████████████░░░░░░░░░░░░░░` **46/86** (53%)

| Fase | Progresso | Feitos |
|---|---|---|
| 3.1 Fase A: necessário e mecânicas do endgame existente | `███████████████░░░░░` | 3/4 |
| 3.2 Fase B: barato e de alto valor (GTO/GTL, poucos blocos faltando) | `███████████████████░` | 18/19 |
| 3.3 Fase C: médio (GTO, 2–5 blocos faltando ou classe própria) | `███████████████████░` | 21/22 |
| 3.4 Fase D: caro / sistemas grandes (GTO) | `█████░░░░░░░░░░░░░░░` | 4/16 |
| 3.5 Fase E: GTNH 1.7.10 sem equivalente no GTO/GTL (conversão por script) | `░░░░░░░░░░░░░░░░░░░░` | 0/5 |
| 3.6 Fase F: TST, GTNL e 123Tech sem versão no GTO/GTL | `░░░░░░░░░░░░░░░░░░░░` | 0/10 |
| 3.7 Fase G: GTLAdditions | `░░░░░░░░░░░░░░░░░░░░` | 0/10 |

## Multiblocos originais (em desenvolvimento)

Máquinas criadas para o GTNA, sem equivalente em outro mod. Cada uma tem ficha técnica com fórmulas, progressão própria e render animado.

| Máquina | Tier | Estado | Ficha |
|---|---|---|---|
| Reator de Água Pressurizada | IV | :material-progress-wrench: design fechado, implementação começando | [abrir](design/reator-pwr.md) |
| Lança Cinética Orbital | UEV | :material-progress-wrench: em implementação | [abrir](design/lanca-cinetica-orbital.md) |
| Portão de Fenda Dimensional | UIV | :material-progress-wrench: em implementação | [abrir](design/portao-de-fenda.md) |
| Anel Colisor de Antimatéria | UIV | :material-progress-wrench: em implementação | [abrir](design/anel-colisor.md) |
| Câmara de Contenção Estelar | MAX | :material-progress-wrench: em implementação | [abrir](design/camara-estelar.md) |

??? note "3.1 Fase A: necessário e mecânicas do endgame existente — 3/4"
    | Máquina | Fonte | Estado |
    |---|---|---|
    | Multiblocos BEC (Condensate Assembler + geradores/contenção) | GTNH (GT5U `BECRecipes`, tectech) | ✅ portado |
    | Convergence do DTPF | GTNH `MTEPlasmaForge` | ⏳ pendente |
    | Nano Forge tier 4 | GTNH `MTENanoForge` | ✅ portado |
    | Hyperdimensional Plasma Fusion Core ("DTPF MK2") | GTO | ✅ portado |

??? note "3.2 Fase B: barato e de alto valor (GTO/GTL, poucos blocos faltando) — 18/19"
    | Máquina | Fonte | Estado |
    |---|---|---|
    | Cracker Hub | GTO | ✅ portado |
    | Mega Distillation | GTL `mega_distillery` | ✅ portado |
    | Desulfurizer | GTO | ✅ portado |
    | Supercomputing Center | GTO | ✅ portado |
    | Research / Analysis Center | GTO `analysis_and_research_center` | ✅ portado |
    | Data Center | GTO | ✅ portado |
    | Giant Flotation Tank | GTO | ✅ portado |
    | Dimensional Focus Engraving Array | GTO | ✅ portado |
    | Phase Change Cube | GTO | ✅ portado |
    | Large Incubator | GTO | ✅ portado |
    | Mega Vacuum Drying | GTO | ✅ portado |
    | Mega Brewer | GTO | ✅ portado |
    | Engraving Laser Plant | GTO | ✅ portado |
    | Large Pyrolyse Oven | GTO/GTL | ✅ portado |
    | Infinity Fluid Drilling Rig | GTO | ✅ portado |
    | Star Ultimate Material Forge | GTO | ✅ portado |
    | Reaction Furnace | GTO | ✅ portado |
    | PCB Factory | GTO | ✅ portado |
    | Tiers da ISA Mill / Isa Factory | GTO `isa_mill` + 123Tech `OTEMegaIsaFactory` | ⏳ pendente |

??? note "3.3 Fase C: médio (GTO, 2–5 blocos faltando ou classe própria) — 21/22"
    | Máquina | Fonte | Estado |
    |---|---|---|
    | Crystal Builder | GTO | ✅ portado |
    | Holy Separator | GTO/GTL (também no TST) | ✅ portado |
    | High Energy Laser Lathe | GTO | ✅ portado |
    | Neutronium Wire Cutting | GTO | ✅ portado |
    | Superconducting Magnetic Presser | GTO | ✅ portado |
    | Giant Electrochemical Workstation | GTO | ✅ portado |
    | Heavy Rolling | GTO | ✅ portado |
    | Hand of Arachne (tear) | GTO | ✅ portado |
    | Lightning Rod (gerador de arco) | GTO | ✅ portado |
    | Fuel Cell Generator | GTO | ✅ portado |
    | Giant Sintering Array | GTO | ✅ portado |
    | Particle Stream Matrix Filling | GTO | ✅ portado |
    | Extreme Compressor | GTO | ✅ portado |
    | Gemini Containment System | GTO | ✅ portado |
    | Space Probe Surface Reception | GTO | ✅ portado |
    | Integrated Vapor Deposition System | GTO | ✅ portado |
    | Integrated Assembler  / Integrated Assembly Facility | GTO (+ versões GTNL/TST) | ✅ portado |
    | Compound Extreme Cooling Unit | GTO | ✅ portado |
    | Hyper Naquadah Reactor / Advanced | GTO `hyper_reactor` / `advanced_hyper_reactor` | ✅ portado |
    | Nanites Circuit Assembly Factory | GTO | ✅ portado |
    | Rare Earth Centrifugal  / Advanced | GTO/GTL | ✅ portado |
    | Platinum Group Processing Hub | GTNL | ⏳ pendente |

??? note "3.4 Fase D: caro / sistemas grandes (GTO) — 4/16"
    | Máquina | Fonte | Estado |
    |---|---|---|
    | Space Elevator + módulos (Ore Extraction, drilling, assembly) | GTO | ✅ portado |
    | Road of Heaven | GTO | ⏳ pendente |
    | Dyson Sphere Launch Silo + Receiving Station | GTO | ✅ portado |
    | Kerr-Newman Homogenizer | GTO | ✅ portado |
    | Nyarlathotep's Tentacle | GTO | ✅ portado |
    | Nano Phagocytosis Plant | GTO | ⏳ pendente |
    | Plasma Centrifuge | GTO | ⏳ pendente |
    | Stellar Forge | GTO | ⏳ pendente |
    | Planetary Gas Collector | GTO | ⏳ pendente |
    | Core Drilling Plant (`planet_core_drilling`) | GTO | ⏳ pendente |
    | Petrochemical Plant | GTO | ⏳ pendente |
    | Fuel Refining Complex | GTO | ⏳ pendente |
    | Neutron Forging Anvil | GTO | ⏳ pendente |
    | Transliminal Oasis | GTO | ⏳ pendente |
    | Biochemical Extraction | GTO | ⏳ pendente |
    | Fast Neutron Breeder Reactor | GTO | ⏳ pendente |

??? note "3.5 Fase E: GTNH 1.7.10 sem equivalente no GTO/GTL (conversão por script) — 0/5"
    | Máquina | Fonte | Estado |
    |---|---|---|
    | Semi-Stable Antimatter Stabilization Sequencer | GoodGenerator `AntimatterForge` | ⏳ pendente |
    | Pseudostable Black Hole Containment Field | GT5U `MTEBlackHoleCompressor` | ⏳ pendente |
    | Industrial Arc Furnace | GT++ | ⏳ pendente |
    | Endothermic Fridge | GT5U | ⏳ pendente |
    | Mega Distillation Tower / Mega Oil Cracker | BartWorks | ⏳ pendente |

??? note "3.6 Fase F: TST, GTNL e 123Tech sem versão no GTO/GTL — 0/10"
    | Máquina | Fonte | Estado |
    |---|---|---|
    | Hyper Thermal Convector | TST | ⏳ pendente |
    | Magnetic Drive Pressure Former | TST | ⏳ pendente |
    | Precise High-Energy Photonic Quantum Master | TST | ⏳ pendente |
    | DTPF MK-II (`MM_…PlasmaForgePrototypeMK2`) | TST (modular) | ⏳ pendente |
    | Eye of Harmony Injector | GTNL | ⏳ pendente |
    | EGTW (Eternal GregTech Workshop) + módulos | GTNL (2.376 linhas) | ⏳ pendente |
    | Vortex Matter Centrifuge, Field Forge Press, Horizontal Compressor, Mega Mixer, Nano Assembler Mk-50 | GTNL | ⏳ pendente |
    | Tangshan Steel Mill | 123Tech | ⏳ pendente |
    | Hyperdimensional Biebie Plasma Forge | 123Tech | ⏳ pendente |
    | Ammonia Plant | Steam Reborn (gtsr) | ⏳ pendente |

??? note "3.7 Fase G: GTLAdditions — 0/10"
    | Máquina | Fonte | Estado |
    |---|---|---|
    | Apocalyptic Torsion Quantum Matrix | QFT com 100% de chance, 1/10 do insumo probabilístico, 1024 threads + distort + neutron compressor | ⏳ pendente |
    | Heart of the Universe | Genesis Engine: 4096× um Creative Laser por plano | ⏳ pendente |
    | Fuxi Bagua Heaven Forging Furnace | 4 tipos de endgame do GTL | ⏳ pendente |
    | Primordial Evolution Nexus | Tipo de receita próprio | ⏳ pendente |
    | Biosphere III + módulos Garden of Hermes | Hospedeiro de módulos com laser | ⏳ pendente |
    | Skeleton Shift Rift Engine | Decay hastener | ⏳ pendente |
    | Space Scaling Instrument | Packer com bobina especial | ⏳ pendente |
    | Planetary Ionisation Convergence Tower | Mecânica própria (classe ainda não lida) | ⏳ pendente |
    | Inferno Cleft Smelting Vault | Pirólise + cracking | ⏳ pendente |
    | Space Elevator MKII / Mega Space Elevator / Light Hunter Space Station | Hubs de módulos com paralelo máximo | ⏳ pendente |

## Como funciona

- Só se porta o que o autor pediu, da fonte indicada (GTO, GTL, GTNL, TST, GTNH).
- Cada port traz estrutura, mecânica e texturas originais, com suporte a KubeJS.
- As receitas padrão são uma base; o balanço fica com o modpack.
