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
