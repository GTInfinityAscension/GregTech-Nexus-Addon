# BEC (Bose-Einstein Condensate) — proposta de port (2026-10-12)

Lote 4 do pedido de 2026-10-12. O Nano Forge tier 4 foi portado (G-0256); o BEC ficou para decisão do autor, pela
regra "pular se travar": o port fiel exige escolhas de arquitetura que não cabe ao assistente presumir.

## O que é no GTNH (GT5-Unofficial `9b4c2a7`, TecTech)

- **5 multiblocos**: BEC Generator (fluido derretido → condensado), BEC Assembler (condensados + itens → produto),
  BEC Storage, BEC IO Node (1.202 linhas) e BEC Diode. Cerca de 4.300 linhas, mais 4 hatches próprios (BEC Hatch,
  IO Node Controller, Nanite Detector, Condensate Detector, LoS) e GUIs em MUI2.
- **Rede física** (`BECFactoryNetwork`, `BECFactoryGrid`): os multiblocos se ligam por hatches e canos de condensado;
  o condensado circula como pilhas no estilo AE (`AEFluidStack`), com rotas e o diodo limitando o sentido.
- **Receitas**: `condensateGeneratorRecipes` (um condensado por material) e `condensateAssemblingRecipes`
  (`BECRecipes`, 694 linhas; `BECMetaMaterialRecipes`, 329): Transdimensional Alignment Matrix, Singularity
  Shielding Casing, Graviton Flow Modulators, Stabilisation/Spacetime Compression Field Generators T0–T8,
  Superconducting Solenoids UHV–UMV, itens MetaMaterial etc.
- **Casings novos**: Coherence-Preserving Plasma Conduit, Electromagnetically Isolated Casing, Fine-Structure
  Constant Manipulator, Conflict Inducement, Peace Enforcement, Condensate Transformative Coil, Electromagnetic
  Waveguide e outros (arte no Modernity-GTNH, CC BY-NC-SA 4.0).

No GTNA, hoje, Shielding Casing e Graviton T2/T3 usam receitas provisórias de Assembly Line (G-0199).

## Decisões para o autor

1. **Rede de condensado**
   - A) Física como no GTNH: hatches e canos ligando os multiblocos, IO Node e Diode portados. Fiel e caro.
   - B) Sem fio por dono, como o vapor sem fio do GTNA: Generator, Assembler e Storage leem uma reserva do time;
     IO Node e Diode não entram. Bem mais barato.
2. **Escopo das receitas**: todas as do GTNH (muitas dependem de itens que o GTNA não tem) ou só as que destravam o
   endgame que já existe (TAM, Shielding Casing, Graviton T2/T3, Convergence do DTPF)?
3. **Condensados**: um por material derretido (gerados) ou só os que as receitas escolhidas usam?
4. **GUIs**: portar as telas de rede ou mostrar o estado no painel do multibloco?

Recomendação do assistente: **B + receitas que destravam o endgame existente + só os condensados usados + painel**.
Custo estimado: um lote do tamanho do Space Elevator. A opção A é várias vezes maior.

## Decisão do autor (2026-10-12)

1. Rede **física** igual ao GTNH (hatches, canos, IO Node, Diode).
2. **Todas** as receitas.
3. **Um condensado por material**.
4. **GUIs da rede portadas**.

A recomendação acima foi rejeitada; vale esta seção.

## Plano do port (fontes: GT5U `9b4c2a7` e NewHorizonsCoreMod `master`, ambos LGPL-3.0)

Fontes lidas: `tectech/mechanics/boseEinsteinCondensate/*`, `multi/bec/*`, `hatch/bec/*`, `pipe/MTEPipeBEC`,
`gui/bec/*`, `BECStructureDefinitions`, `CondensateType`, `NaniteTier`, `MTEHatchNanite`, `BECRecipes`,
`BECMetaMaterialRecipes`, as receitas de Assembly Line das carcaças (`ResearchStationAssemblyLine`), as de prensa
(Peace/Conflict), a do cano (`AssemblerRecipes.withBEC`) e, no coremod, as dos controladores e hatches
(`AssemblingLineRecipes`) e o `BECRecipes` do coremod.

1. **Dados**: 19 condensados emaranhados (`entangled_*`, gás, um por `CondensateType`); `NaniteTier` (12 nanites,
   tiers 1–10); tipos `gtna:condensate_generator` e `gtna:condensate_assembler` (condensados e a sequência de nanites
   ficam nos dados da receita, como os metadados `CONDENSATE_INPUT`/`NANITE_TIERS` do GTNH).
2. **Blocos e itens**: 6 carcaças do `BlockCasingsBEC`, o Electromagnetic Waveguide (vidro), o cano BEC (conecta por
   cor como no GTNH) e os itens MetaMaterial.
3. **Rede**: grafo de canos e BEC Hatches; nós notáveis são os multiblocos formados; busca em largura por distância,
   igual ao `GraphRouteTracker` (o Diode só deixa passar o que o filtro permite e só sai pelo hatch de entrada).
4. **Hatches**: BEC Hatch, Nanite Containment Bus, Line-of-Sight Connector (com feixe), Nanite Detector,
   Condensate Detector e IO Node Controller.
5. **Multiblocos**: Generator, Storage, Diode, Assembler (Observation Array) e IO Node (Teleportation Node), com as
   estruturas convertidas de `BECStructureDefinitions`.
6. **Telas**: o texto de estado e os parâmetros de cada tela do GTNH (field strength, min/max parallel, speed
   divisor, filtros do Diode, configuração dos detectores).
7. **Receitas**: todas as que têm destino no GTNA. Receitas cujo produto não existe no GTNA (Stargate, Exo-Foundry,
   Computation Singularity, circuit arrays do coremod) ficam listadas como não portadas.
