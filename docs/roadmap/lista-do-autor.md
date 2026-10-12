# Lista do autor: multiblocos pedidos para o GTNA

**Regra:** porta-se só o que está aqui, **da fonte (mod) indicada**. Se a fonte é o GTNL, porta-se a versão GTNL:
muitas são estruturas do GTO adaptadas ao GTNH, que usam tipos de receita padrão em vez dos tipos exclusivos do GTO
(rolling, cluster etc.). Do GTO vem só a estrutura e os blocos. Não se criam tipos exclusivos do GTO sem o autor pedir
(exceção já aprovada: `precision_laser_engraver`, como o precision assembler).

Origem: listas do autor registradas em `auditoria-multiblocos.md` (2026-10-07) e as correções de 2026-10-08.
Ao receber um pedido novo, acrescente uma linha com a data e a fonte que o autor disse.

## Portados

| Máquina | Fonte | Checkpoint |
|---|---|---|
| Cracker Hub | GTO | G-0204 |
| Mega Brewer | GTO | G-0204 |
| Mega Vacuum Drying Furnace | GTO | G-0204 |
| Large Pyrolyse Oven | GTO | G-0204 |
| Giant Flotation Tank | GTO | G-0204 |
| Phase Change Cube | GTO | G-0205 |
| Engraving Laser Plant | GTO | G-0205 |
| Infinity Fluid Drilling Rig | GTO | G-0205 |
| Mega Distillation | GTL (`mega_distillery`) | G-0205 |
| Super Blast Smelter | GTO (autor confirmou em 2026-10-08) | G-0206 |
| Integrated Assembler | GTO (ROADMAP) | G-0206 |
| Holy Separator | GTO | G-0207 |
| Neutronium Wire Cutting | GTO | G-0207 |
| Superconducting Magnetic Presser | GTO | G-0207 |
| Superconducting Electromagnetism | GTO (autor confirmou em 2026-10-08) | G-0207 |
| Particle Stream Matrix Filling Machine | GTO | G-0209 |
| Crystal Builder | GTO | G-0210 |
| High Energy Laser Lathe | GTO | G-0243 |
| Extreme Compressor | GTO (só o modo compressor) | G-0243 |
| Hyperdimensional Plasma Fusion Core | GTO (só o modo DTPF) | G-0244 |
| Gemini Containment System | GTO (packer do GTCEu) | G-0244 |
| Giant Electrochemical Workstation | GTO (só electrolyzer) | G-0244 |
| Desulfurizer | GTO (tipo próprio) | G-0245 |
| Dimensional Focus Engraving Array | GTO (tipo próprio) | G-0245 |
| Star Ultimate Material Forge | GTO (tipo próprio) | G-0245 |
| Hand of Arachne | GTO (loom) | G-0245 |
| Rare Earth Centrifugal | GTO (tipo próprio) | G-0245 |
| Heavy Rolling | GTO (bender) | G-0245 |
| Lightning Rod | GTO (tipo próprio) | G-0246 |
| PCB Factory | GTO (tipo próprio) | G-0246 |
| Space Probe Surface Reception | GTO (tipo próprio) | G-0246 |
| Compound Extreme Cooling Unit | GTO (tipos próprios) | G-0246 |
| Hyper Reactor / Advanced Hyper Reactor | GTO (tipos próprios) | G-0247 |
| Fuel Cell Generator | GTO (tipos próprios) | G-0248 |
| Supercomputing Center | GTO (lote de pesquisa) | G-0249 |
| Data Center | GTO (lote de pesquisa) | G-0250 |
| Analysis & Research Center | GTO (lote de pesquisa) | G-0250 |
| Large Incubator | GTO (sem a Radiation Hatch) | G-0255 |
| Kerr-Newman Homogenizer | GTO (mixer do GTCEu) | G-0255 |
| Nyarlathotep's Tentacle | GTO (só Assembly Line) | G-0255 |
| Giant Sintering Array | GTO (tipo próprio) | G-0255 |
| Integrated Vapor Deposition System | GTO (tipos próprios) | G-0255 |
| Reaction Furnace | GTO (tipo próprio + módulo) | G-0255 |
| Dyson Sphere Launch Silo / Receiving Station | GTO (tipo próprio) | G-0255 |

## Portados fora da lista, mantidos até o autor decidir

Large Cracker (G-0206), Magnetic Energy Reaction Furnace (G-0209), Nanites Circuit Assembly Factory e Mega Wiremill
(G-0210). Removidos em 2026-10-08: Molecular Oscillation Dehydrator, Gravity Bending Device, Extreme Electric Furnace.

## Pedidos que faltam

Ver `auditoria-multiblocos.md` (primeira e segunda lista) e o ROADMAP §3. **Antes de portar, confira aqui a fonte.**

## Pedido de 2026-10-09 (autoriza tipos de receita próprios do GTO)

Portar **com os tipos de receita do GTO**: Desulfurizer, Dimensional Focus Engraving Array, Star Ultimate Material
Forge, PCB Factory, Hand of Arachne, Lightning Rod, Fuel Cell Generator, Space Probe Surface Reception, Hyper Reactors
(Hyper e Advanced), Rare Earth Centrifugal, Compound Extreme Cooling Unit. **Heavy Rolling** vem com o tipo bending
(bender do GTCEu), sem o rolling/cluster do GTO. O lote de pesquisa (Supercomputing Center, Data Center, Analysis &
Research Center) entra inteiro.

## Pedido de 2026-10-12 (quatro lotes aprovados)

Todos da fonte já indicada (GTO, exceto o último lote):
1. **Sem tipo novo:** Large Incubator (tipo incubator do GTNA), Kerr-Newman Homogenizer (mixer do GTCEu), Nyarlathotep's Tentacle (Assembly Line + Circuit Assembly Line, sem o modo Suprachronal).
2. **Space Elevator + módulos** (GTO), base para o Road of Heaven.
3. **Com tipos próprios do GTO (aprovados):** Giant Sintering Array (sintering), Integrated Vapor Deposition System (CVD/PVD), Reaction Furnace (reaction_furnace), Dyson Sphere Launch Silo + Receiving Station (dyson_sphere).
4. **Endgame do GTNH:** multiblocos BEC e Nano Forge tier 4.
