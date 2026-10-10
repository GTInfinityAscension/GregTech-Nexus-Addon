# Relatório de Calibração Visual Integral dos 50 Material Sets

Este documento detalha a resolução completa de todos os problemas reportados, cobrindo os **50 Material Sets Animados do GTNA**.

👉 [material_preview.html](file:///home/raishxn/MineProjects/GregTech-Nexus-Addon/material_preview.html) — Abra este showcase interativo para ver as animações em tempo real e a tabela com os 50 sets.

---

## 1. Problemas Identificados e Soluções Globais

### A. Resolução da Ausência de Texturas no Jogo (Echoite, Hypogen, Infinity, etc.)
- **Causa Raiz Descoberta**: O `MaterialIconType` do GTCEu e o `TagPrefix` realizam o lookup de modelos e texturas usando convenções em camelCase (ex: `ingotDouble.json`, `ingotTriple.json`, `plateTriple.json`, `wireFine.json`, `gearSmall.json`, `rodLong.json`). Os scripts anteriores gravavam apenas snake_case (`ingot_double.json`, `wire_fine.json`), fazendo com que o jogo caísse no fallback padrão sem carregar a textura ou modelo animado customizado.
- **Solução Implementada**: Implementamos **paridade dual irrestrita (camelCase + snake_case)** em **todos os 50 material sets**. Tanto `ingotDouble` quanto `ingot_double`, `wireFine` quanto `wire_fine`, `pipeSide` quanto `pipe_side`, `wireSide` quanto `wire_side`, etc., existem como arquivos físicos PNG, MCMETA e modelos JSON.

### B. Correção dos Fine Wires em TODOS os Sets (Hypogen, Echoite, etc.)
- Anteriormente, vários conjuntos gravavam `wire_fine_overlay.png` como um PNG 16x16 transparente (0 pixels).
- Agora, o overlay padrão do carretel de madeira autêntico do Modernity/GTCEu (`wireFine_OVERLAY.png`, exatamente **115 pixels** de madeira/flange) foi aplicado a **todos os 50 material sets**.
- Tanto `wireFine_overlay.png` quanto `wire_fine_overlay.png` possuem o carretel de madeira, permitindo que a camada do fio metálico animado seja exibida perfeitamente enrolada no carretel.

### C. Cobertura Total de Itens e Blocos em TODOS os 50 Sets
Cada um dos 50 material sets agora possui obrigatoriamente:
1. **Multi-ingots**: `ingotDouble`, `ingotTriple`, `ingotQuadruple`, `ingotQuintuple` (e variantes `ingot_double`...).
2. **Multi-plates**: `plateDouble`, `plateTriple`, `plateQuadruple`, `plateQuintuple`, `plateDense`, `plateSuperdense` (e variantes `plate_double`...).
3. **Pipes de Fluido**: Todas as 8 variações (`pipeSide`, `pipeTiny`, `pipeSmall`, `pipeMedium`, `pipeLarge`, `pipeHuge`, `pipeQuadruple`, `pipeNonuple` e variantes snake_case).
4. **Cabos e Fios**: `wireSide`, `wire_side`, `wireEnd`, `wire_end` e overlays.
5. **Fluidos Animados**: `liquid.png` e `molten.png` com metadados de animação.
6. **Mecânica e Rotação**: `gear`, `gearSmall`, `gearGtSmall`, `rod`, `rodLong`, `stickLong`, `round`, `ring`, `rotor`, `spring`, `springSmall`.
7. **Singularidades**: `singularity.png` e modelo com shader loaders ativos.

### D. Calibração Tonal Rigorosa
- **Shirabon**: Ajustado para o magenta canônico profundo `#c61361` (`[198, 19, 97]`) com ressonância osciloscópica, eliminando o tom rosa pastel desbotado.
- **Dragon Metal (Dragonblood)**: Ajustado para o carmesim arterial canônico `#dc2814` (`[220, 40, 20]`) com pulso radial de sangue dracônico.
- **Hastelloy N 75**: Ajustado para verde-oliva metálico `#5a5c44` (`[90, 92, 68]`), combinando perfeitamente com a Carcaça (`hastelloy_n_75_casing.png`, média `[88, 90, 66]`) e o Tubo (`hastelloy_n_75_pipe.png`, média `[91, 88, 75]`).

### E. Variação Estrutural de Silhuetas de Ingots (Gordinhos vs Pequenininhos)
- **Mais Gordinhos (`SHINY` / Ultimet - 136px)**:
  - `hastelloy_n_75`, `mar_m_200_steel`, `stellite`, `trinaquadalloy`, `stellar_alloy`.
- **Mais Pequenininhos (`DULL` / Battery Alloy - 114px)**:
  - `indalloy_140`, `advanced_nitinol`, `shijima`.
- **Padrão Moderno (`WhiteDwarfMatter` / `METALLIC` - 135px)**:
  - `echoite`, `hypogen`, `celestial_tungsten`, `astral_titanium`, `infinity`, `cosmic_neutronium`, etc.

---

## 2. Auditoria dos 50 Material Sets

Executamos uma varredura automatizada em todos os diretórios do projeto:
- **Total de sets verificados**: 50 / 50 (`gtna_*`).
- **Falhas de itens**: 0.
- **Falhas de blocos/pipes/fios/fluidos**: 0.
- **Fine Wire overlays inválidos/transparentes**: 0 (100% possuem os 115 pixels de carretel).
- **Paridade dual**: 100% dos sets possuem arquivos camelCase e snake_case.
