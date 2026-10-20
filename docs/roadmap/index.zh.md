# Roadmap

GTNA 目前注册了 **168 个多方块**。本页展示所需移植项目以及原创多方块的进度，由项目工作文档生成，与代码保持同步。

## 移植总进度

`████████████████░░░░░░░░░░░░░░` **46/86** (53%)

| 阶段 | 进度 | 完成 |
|---|---|---|
| A 阶段：必需项与现有终局机制 | `███████████████░░░░░` | 3/4 |
| B 阶段：成本低、价值高（GTO/GTL，缺少的方块很少） | `███████████████████░` | 18/19 |
| C 阶段：中等（GTO，缺 2–5 个方块或需要独立类） | `███████████████████░` | 21/22 |
| D 阶段：昂贵或大型系统（GTO） | `█████░░░░░░░░░░░░░░░` | 4/16 |
| E 阶段：GTO/GTL 中没有对应的 GTNH 1.7.10 机器 | `░░░░░░░░░░░░░░░░░░░░` | 0/5 |
| F 阶段：GTO/GTL 中没有版本的 TST、GTNL 与 123Tech 机器 | `░░░░░░░░░░░░░░░░░░░░` | 0/10 |
| G 阶段：GTLAdditions | `░░░░░░░░░░░░░░░░░░░░` | 0/10 |

## 原创多方块（开发中）

为 GTNA 设计、其他模组中没有对应机器的多方块。每台都有一份技术说明（葡萄牙语），包含公式、独立进度和动画渲染。

| 机器 | Tier | 状态 | 说明 |
|---|---|---|---|
| 压水反应堆 | IV | :material-progress-wrench: 设计完成，开始实现 | [打开](design/reator-pwr.md) |
| 动能轨道长矛 | UEV | :material-progress-wrench: 已在游戏中，测试中（WIP） | [打开](design/lanca-cinetica-orbital.md) |
| 维度裂隙之门 | UIV | :material-progress-wrench: 已在游戏中，测试中（WIP） | [打开](design/portao-de-fenda.md) |
| 反物质对撞环 | UIV | :material-progress-wrench: 已在游戏中，测试中（WIP） | [打开](design/anel-colisor.md) |
| 恒星约束舱 | MAX | :material-progress-wrench: 已在游戏中，测试中（WIP） | [打开](design/camara-estelar.md) |

??? note "A 阶段：必需项与现有终局机制 — 3/4"
    | 机器 | 来源 | 状态 |
    |---|---|---|
    | Multiblocos BEC (Condensate Assembler + geradores/contenção) | GTNH (GT5U `BECRecipes`, tectech) | ✅ 已移植 |
    | Convergence do DTPF | GTNH `MTEPlasmaForge` | ⏳ 待移植 |
    | Nano Forge tier 4 | GTNH `MTENanoForge` | ✅ 已移植 |
    | Hyperdimensional Plasma Fusion Core ("DTPF MK2") | GTO | ✅ 已移植 |

??? note "B 阶段：成本低、价值高（GTO/GTL，缺少的方块很少） — 18/19"
    | 机器 | 来源 | 状态 |
    |---|---|---|
    | Cracker Hub | GTO | ✅ 已移植 |
    | Mega Distillation | GTL `mega_distillery` | ✅ 已移植 |
    | Desulfurizer | GTO | ✅ 已移植 |
    | Supercomputing Center | GTO | ✅ 已移植 |
    | Research / Analysis Center | GTO `analysis_and_research_center` | ✅ 已移植 |
    | Data Center | GTO | ✅ 已移植 |
    | Giant Flotation Tank | GTO | ✅ 已移植 |
    | Dimensional Focus Engraving Array | GTO | ✅ 已移植 |
    | Phase Change Cube | GTO | ✅ 已移植 |
    | Large Incubator | GTO | ✅ 已移植 |
    | Mega Vacuum Drying | GTO | ✅ 已移植 |
    | Mega Brewer | GTO | ✅ 已移植 |
    | Engraving Laser Plant | GTO | ✅ 已移植 |
    | Large Pyrolyse Oven | GTO/GTL | ✅ 已移植 |
    | Infinity Fluid Drilling Rig | GTO | ✅ 已移植 |
    | Star Ultimate Material Forge | GTO | ✅ 已移植 |
    | Reaction Furnace | GTO | ✅ 已移植 |
    | PCB Factory | GTO | ✅ 已移植 |
    | Tiers da ISA Mill / Isa Factory | GTO `isa_mill` + 123Tech `OTEMegaIsaFactory` | ⏳ 待移植 |

??? note "C 阶段：中等（GTO，缺 2–5 个方块或需要独立类） — 21/22"
    | 机器 | 来源 | 状态 |
    |---|---|---|
    | Crystal Builder | GTO | ✅ 已移植 |
    | Holy Separator | GTO/GTL (também no TST) | ✅ 已移植 |
    | High Energy Laser Lathe | GTO | ✅ 已移植 |
    | Neutronium Wire Cutting | GTO | ✅ 已移植 |
    | Superconducting Magnetic Presser | GTO | ✅ 已移植 |
    | Giant Electrochemical Workstation | GTO | ✅ 已移植 |
    | Heavy Rolling | GTO | ✅ 已移植 |
    | Hand of Arachne (tear) | GTO | ✅ 已移植 |
    | Lightning Rod (gerador de arco) | GTO | ✅ 已移植 |
    | Fuel Cell Generator | GTO | ✅ 已移植 |
    | Giant Sintering Array | GTO | ✅ 已移植 |
    | Particle Stream Matrix Filling | GTO | ✅ 已移植 |
    | Extreme Compressor | GTO | ✅ 已移植 |
    | Gemini Containment System | GTO | ✅ 已移植 |
    | Space Probe Surface Reception | GTO | ✅ 已移植 |
    | Integrated Vapor Deposition System | GTO | ✅ 已移植 |
    | Integrated Assembler  / Integrated Assembly Facility | GTO (+ versões GTNL/TST) | ✅ 已移植 |
    | Compound Extreme Cooling Unit | GTO | ✅ 已移植 |
    | Hyper Naquadah Reactor / Advanced | GTO `hyper_reactor` / `advanced_hyper_reactor` | ✅ 已移植 |
    | Nanites Circuit Assembly Factory | GTO | ✅ 已移植 |
    | Rare Earth Centrifugal  / Advanced | GTO/GTL | ✅ 已移植 |
    | Platinum Group Processing Hub | GTNL | ⏳ 待移植 |

??? note "D 阶段：昂贵或大型系统（GTO） — 4/16"
    | 机器 | 来源 | 状态 |
    |---|---|---|
    | Space Elevator + módulos (Ore Extraction, drilling, assembly) | GTO | ✅ 已移植 |
    | Road of Heaven | GTO | ⏳ 待移植 |
    | Dyson Sphere Launch Silo + Receiving Station | GTO | ✅ 已移植 |
    | Kerr-Newman Homogenizer | GTO | ✅ 已移植 |
    | Nyarlathotep's Tentacle | GTO | ✅ 已移植 |
    | Nano Phagocytosis Plant | GTO | ⏳ 待移植 |
    | Plasma Centrifuge | GTO | ⏳ 待移植 |
    | Stellar Forge | GTO | ⏳ 待移植 |
    | Planetary Gas Collector | GTO | ⏳ 待移植 |
    | Core Drilling Plant (`planet_core_drilling`) | GTO | ⏳ 待移植 |
    | Petrochemical Plant | GTO | ⏳ 待移植 |
    | Fuel Refining Complex | GTO | ⏳ 待移植 |
    | Neutron Forging Anvil | GTO | ⏳ 待移植 |
    | Transliminal Oasis | GTO | ⏳ 待移植 |
    | Biochemical Extraction | GTO | ⏳ 待移植 |
    | Fast Neutron Breeder Reactor | GTO | ⏳ 待移植 |

??? note "E 阶段：GTO/GTL 中没有对应的 GTNH 1.7.10 机器 — 0/5"
    | 机器 | 来源 | 状态 |
    |---|---|---|
    | Semi-Stable Antimatter Stabilization Sequencer | GoodGenerator `AntimatterForge` | ⏳ 待移植 |
    | Pseudostable Black Hole Containment Field | GT5U `MTEBlackHoleCompressor` | ⏳ 待移植 |
    | Industrial Arc Furnace | GT++ | ⏳ 待移植 |
    | Endothermic Fridge | GT5U | ⏳ 待移植 |
    | Mega Distillation Tower / Mega Oil Cracker | BartWorks | ⏳ 待移植 |

??? note "F 阶段：GTO/GTL 中没有版本的 TST、GTNL 与 123Tech 机器 — 0/10"
    | 机器 | 来源 | 状态 |
    |---|---|---|
    | Hyper Thermal Convector | TST | ⏳ 待移植 |
    | Magnetic Drive Pressure Former | TST | ⏳ 待移植 |
    | Precise High-Energy Photonic Quantum Master | TST | ⏳ 待移植 |
    | DTPF MK-II (`MM_…PlasmaForgePrototypeMK2`) | TST (modular) | ⏳ 待移植 |
    | Eye of Harmony Injector | GTNL | ⏳ 待移植 |
    | EGTW (Eternal GregTech Workshop) + módulos | GTNL (2.376 linhas) | ⏳ 待移植 |
    | Vortex Matter Centrifuge, Field Forge Press, Horizontal Compressor, Mega Mixer, Nano Assembler Mk-50 | GTNL | ⏳ 待移植 |
    | Tangshan Steel Mill | 123Tech | ⏳ 待移植 |
    | Hyperdimensional Biebie Plasma Forge | 123Tech | ⏳ 待移植 |
    | Ammonia Plant | Steam Reborn (gtsr) | ⏳ 待移植 |

??? note "G 阶段：GTLAdditions — 0/10"
    | 机器 | 来源 | 状态 |
    |---|---|---|
    | Apocalyptic Torsion Quantum Matrix | QFT com 100% de chance, 1/10 do insumo probabilístico, 1024 threads + distort + neutron compressor | ⏳ 待移植 |
    | Heart of the Universe | Genesis Engine: 4096× um Creative Laser por plano | ⏳ 待移植 |
    | Fuxi Bagua Heaven Forging Furnace | 4 tipos de endgame do GTL | ⏳ 待移植 |
    | Primordial Evolution Nexus | Tipo de receita próprio | ⏳ 待移植 |
    | Biosphere III + módulos Garden of Hermes | Hospedeiro de módulos com laser | ⏳ 待移植 |
    | Skeleton Shift Rift Engine | Decay hastener | ⏳ 待移植 |
    | Space Scaling Instrument | Packer com bobina especial | ⏳ 待移植 |
    | Planetary Ionisation Convergence Tower | Mecânica própria (classe ainda não lida) | ⏳ 待移植 |
    | Inferno Cleft Smelting Vault | Pirólise + cracking | ⏳ 待移植 |
    | Space Elevator MKII / Mega Space Elevator / Light Hunter Space Station | Hubs de módulos com paralelo máximo | ⏳ 待移植 |

## 规则

- 只移植作者指定的机器，并来自指定的来源（GTO、GTL、GTNL、TST、GTNH）。
- 每个移植都保留原始结构、机制和材质，并支持 KubeJS。
- 默认配方只是基准；平衡由整合包决定。
