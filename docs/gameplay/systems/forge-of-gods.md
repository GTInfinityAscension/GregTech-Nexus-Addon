# Forja dos Deuses

![Forja dos Deuses](../../assets/gtnh/forge_of_the_gods.png){ loading=lazy }

<small>Imagem: GTNH Wiki, CC BY-SA 4.0.</small>

A Forja dos Deuses (Godforge) é um multibloco UIV que mantém uma estrela artificial e alimenta até 16 **módulos** de processamento com energia wireless. Esta página reúne o que o jogo não mostra: todas as fórmulas, as tabelas calculadas a partir do código do GTNA e as diferenças em relação ao GTNH.

|  |  |
|---|---|
| **Tier** | UIV |
| **Tamanho** | 186 × 127 × 29 (anel 1) |
| **Energia** | wireless, sem hatch de energia |
| **Overclock** | imperfeito (4/2), 4/2,3 com GGEBE |
| **Fonte** | port de GT5-Unofficial a3e1e112 |

## Estrutura

Até três anéis. Os módulos ficam em anéis menores ao redor. Para construir um anel novo, desligue a animação (chave de fenda no controlador ou o botão nos cosméticos), construa e religue com o martelo macio. O projetor holográfico usa o tamanho da pilha para escolher quantos anéis mostrar.

![structure](../../assets/machines/forge_of_gods.webp){ loading=lazy }

## Módulos

| Módulo | Libera | Paralelo base | Função |
|---|---|---|---|
| Helioflare Power Forge | START | 1024 | alto-forno ou multi-fornalha (modo fornalha não conta nos marcos) |
| Helioflux Melting Core | FDIM | 512 | alto-forno com saída fundida |
| Heliothermal Plasma Fabricator | GPCI | 512 | pó/fluido direto para plasma |
| Heliofusion Exoticizer | QGPIU (matéria mágica: EE) | 64 | plasma de quarks e glúons e MagMatter; precisa de automação |

Limite de módulos: 8, 12 com o anel 2 (CD), 16 com o anel 3 (EE). Passar do limite desconecta todos.

## Combustível

A estrela é acesa com Combustível Estelar no barramento de entrada. Custo de partida: `f · 25 · 1,2^f` itens. O fator de consumo `f` vai até 5 sem upgrades. O controlador drena a cada 5 s (×2 com a bateria carregando).

```
DTR (resíduo)        f · 300 · 1,15^f      (×0,8 com STEM)
Plasma estelar       f · 2 · 1,08^f        (×0,8 com STEM)
MCSM                 f / 25
calor                12601 + log₁,₅(f) · 1000   (base 1,12 / 1,18 com SEFCP)
```

| f | Calor base (K) | Partida (itens) | DTR/s | DTR/s com STEM | Plasma estelar/s | MCSM/s |
|---|---|---|---|---|---|---|
| 1 | 12.601 | 30 | 345 | 276 | 2,16 | 0,04 |
| 2 | 14.310 | 72 | 793 | 635 | 4,67 | 0,08 |
| 3 | 15.310 | 129 | 1.369 | 1.095 | 7,56 | 0,12 |
| 4 | 16.020 | 207 | 2.099 | 1.679 | 10,88 | 0,16 |
| 5 | 16.570 | 311 | 3.017 | 2.414 | 14,69 | 0,20 |
| 6 | 17.020 | 447 | 4.164 | 3.331 | 19,04 | 0,24 |
| 10 | 18.279 | 1.547 | 12.137 | 9.709 | 43,18 | 0,40 |
| 20 | 19.989 | 19.168 | 98.199 | 78.559 | 186 | 0,80 |
| 43 | 21.877 | 2.730.247 | 5.255.292 | 4.204.234 | 2.354 | 1,72 |
| 70 | 23.079 | 6,11e8 | 3,72e8 | 2,98e8 | 30.605 | 2,80 |

Fatores máximos com TSE: resíduo 70 (72 com STEM), plasma estelar 181 (184 com STEM), MCSM sem limite. Acima de 43 o fator efetivo do SA cresce devagar: `43 + (f − 43)^0,4`.

## Calor e teto de bônus

Os bônus de calor valem até o teto: 15.000 K, ou 30.000 K com CNTI. Com NDPE, acima de 30.000 K o calor conta comprimido: `30000 + (calor − 30000)^e`, com e = 0,85 no Power Forge e 0,8 nos demais.

## Paralelo

```
paralelo = base · CTCDD(×2) · SA · EPEC · PoS
SA    = 1 + f_efetivo / 15          (TCT: ×3 no Melting Core e no Power Forge com DoP, ×2 nos outros)
EPEC  = 1 + calor / 15000           (Melting Core e Power Forge com DoP) ou 1 + calor / 25000
PoS   = 1 + upgrades / 5            (Melting Core e Power Forge com DoP) ou 1 + upgrades / 8
Exoticizer: raiz quadrada do total com PA, senão 1
```

| f | f_ef. | SA | SA+TCT (Melting) |
|---|---|---|---|
| 5 | 5 | 1,33 | 4 |
| 15 | 15 | 2 | 6 |
| 43 | 43 | 3,87 | 11,60 |
| 70 | 46 | 4,07 | 12,20 |
| 181 | 50 | 4,33 | 13 |
| 1000 | 58 | 4,87 | 14,60 |

A wiki do GTNH mostra só a versão de 15000 e de /5. O código usa divisores maiores fora do Melting Core.

## Velocidade e energia

```
IGCC   tempo × calor^−0,01
DoR    tempo ÷ paralelo^0,02 (plasma) ou ^0,012 (outros)
REC    desconto = (1 − 1,05^(−0,05 · bateria máx)) / 20
IMKG   desconto pela carga: 1 − (−0,6·(c − 0,5)² + 0,15) no plasma, ×2/3 nos outros
GISS   voltagem += unidades de combustível/s · 1e8 EU/t
NGMS   voltagem × 4 por anel ativo (aplicado por último)
```

## Marcos

Cada marco tem 7 níveis e dá fragmentos de gráviton iguais ao nível. Depois que os quatro chegam ao nível 7, a **Inversão** remove o teto e cada nível novo custa o mesmo que o 7.

| Nível | Carga (EU) | Conversão (receitas) | Catalisador (combustível) | Composição |
|---|---|---|---|---|
| 1 | 1e15 | 1e7 | 10.000 | 1 |
| 2 | 9e15 | 4e7 | 30.000 | 2 |
| 3 | 8,1e16 | 1,6e8 | 90.000 | 3 |
| 4 | 7,29e17 | 6,4e8 | 270.000 | 4 |
| 5 | 6,56e18 | 2,56e9 | 810.000 | 5 |
| 6 | 5,9e19 | 1,02e10 | 2.430.000 | 6 |
| 7 | 5,31e20 | 4,1e10 | 7.290.000 | 7 |

## Upgrades

Comprados com fragmentos. Linha azul: basta um pré-requisito; vermelha: todos. Depois do Exoticizer a árvore se divide em três (roxo: calor; laranja: paralelo; verde: plasma). Um ramo no começo, o segundo com o anel 2, os três com o anel 3. Reembolso só sem upgrades dependentes ativos.

| Tag | Custo | Pré-requisito | Efeito |
|---|---|---|---|
| START | 0 | — | 8 módulos, anel 1, Power Forge, 2 bi EU/t, teto 15.000 K |
| IGCC | 1 | START | tempo × calor^−0,01 |
| STEM | 1 | IGCC | combustível × 0,8 |
| CFCE | 1 | IGCC | fator máximo × 1,2 |
| GISS | 1 | STEM | voltagem += combustível/s · 1e8 |
| FDIM | 1 | STEM, CFCE | libera Melting Core |
| SA | 1 | CFCE | paralelo × (1 + f/15) |
| GPCI | 2 | FDIM | libera Plasma Fabricator (T3, um passo) |
| REC | 2 | GISS + GPCI | bateria configurável e desconto |
| GEM | 2 | GPCI | fator máximo += upgrades ativos |
| CTCDD | 2 | GPCI + SA | paralelo × 2 |
| QGPIU | 2 | REC, CTCDD | libera Exoticizer |
| SEFCP | 3 | QGPIU | calor com base 1,12 / 1,18 |
| TCT | 3 | QGPIU | SA × 2 ou × 3 |
| GGEBE | 3 | QGPIU | overclock 4/2,3 |
| TPTP | 4 | GGEBE | plasmas de vários passos |
| CNTI | 3 | SEFCP | teto 30.000 K |
| DOP | 4 | CNTI | Power Forge ganha bônus do Melting Core |
| EPEC | 3 | TCT | paralelo × (1 + calor/15000 ou /25000) |
| IMKG | 3 | GGEBE | desconto pela carga da bateria |
| NDPE | 3 | CNTI | calor comprimido acima de 30.000 K |
| POS | 3 | EPEC | paralelo × (1 + upgrades/5 ou /8) |
| DOR | 3 | IMKG | tempo ÷ paralelo^0,02 |
| NGMS | 4 | NDPE, POS, DOR | voltagem × 4 por anel |
| SEDS | 5 | NGMS | plasmas até T5 |
| PA | 6 | SEDS | Exoticizer recebe os bônus (raiz quadrada) |
| CD | 7 | PA | anel 2, +4 módulos |
| TSE | 8 | CD | tira o teto do combustível |
| TBF | 9 | TSE | voltagem livre por módulo |
| EE | 10 | TBF | anel 3, +4 módulos, matéria mágica |
| END | 12 | EE | plasmas exóticos, ejeção de fragmentos |

### Árvore de upgrades (GTNH)

![tree](../../assets/gtnh/godforge_upgrade_tree.png){ loading=lazy width=360 }

<small>Imagem: GTNH Wiki, CC BY-SA 4.0.</small>

## Materiais extras dos upgrades (GTNA)

| Tag | Materiais |
|---|---|
| START | 64 frame Superconductor UIV Base, 32 Superconductor Composite, 16 Metastable Oganesson gear, 8 Eternal Singularity, 64 Robot Arm UIV, 64 Field Generator UEV |
| FDIM | 16 Mega Alloy Blast Smelter, 64 Hypogen Coil, 32 Harmonic Phonon Conduit, 16 Eternal Singularity, 48 Field Restriction Coil T3, 64 Robot Arm UIV, 64 Field Generator UEV |
| GPCI | 8 Stellar Energy Siphon, 8 Advanced Fusion, 64 Fusion Casing MK4, 64 Neutronium foil, 48 dense Quantum plate, 32 Rhugnor gear, 16 Eternal Singularity, 64 Robot Arm UIV, 64 Field Generator UEV |
| QGPIU | 16 Stellar Energy Siphon, 2 Advanced Fusion, 64 Compressed Fusion Coil MK2, 16 Harmonic Phonon Conduit, 4 Transcendent Plasma Mixer, 64 Rhugnor gear, 64 Ichorium gear, 32 Eternal Singularity, 64 Robot Arm UIV, 64 Field Generator UEV |
| CD | 64 frame SpaceTime, 64 frame Superconductor UMV Base, 64 frame Hypogen, 64 frame Dragon Metal, 64 Spatial Casing, 8 Boundary Casing, 2 Mega Battery, 32 Field Generator UXV |
| EE | 64 frame White Dwarf Matter, 64 frame Black Dwarf Matter, 16 frame Eternity, 2 frame Universium, 64 Boundary Casing, 48 Stabilisation Field T5, 16 Mega Battery, 32 Exoticizer, 64 Siphon, 64 Field Generator UXV, 64 Robot Arm UXV |
| END | 64 frame MHDCSM, 64 frame Eternity, 64 frame MagMatter, 64 Stabilisation Field T7, 64 Exoticizer, 4 Astral Array Fabricator, 32 Mega Battery, 64 Field Generator UXV, 64 Robot Arm UXV |

Substituições do GTNA em relação ao GTNH: Malha Resistente a UHT → folha de Neutrônio; Fusion Internal Casing 2 → Fusion Casing MK4; Compact Fusion Coil T4 → Compressed Fusion Coil MK2; peças UMV → UXV. Transdimensional Alignment Matrix e nanites de MagMatter não entram.

## Diferenças em relação ao GTNH

- Plasma Fabricator com paralelo base 512 no código (a wiki do GTNH cita 384).
- A matéria mágica do Exoticizer é liberada pelo **EE** no código do GTNA (a wiki do GTNH cita END).
- Custos materiais adaptados aos itens que existem no GTNA (seção anterior).
- Combustíveis e fatores máximos idênticos ao GT5-Unofficial a3e1e112.

## Créditos

Imagens marcadas com "GTNH Wiki" vêm da [wiki do GT New Horizons](https://wiki.gtnewhorizons.com/wiki/Forge_of_the_Gods), licenciadas sob [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Esta página é distribuída sob a mesma licença. Mecânica original: GT5-Unofficial (equipe GTNH).
