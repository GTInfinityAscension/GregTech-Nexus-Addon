# Configuração

O GTNA tem dois tipos de ajuste:

- **`config/gtna.yaml`**: jogabilidade, cliente e chaves por máquina. Toda opção também aparece no menu de configuração do jogo, com um comentário.
- **`config/gtna/balance/*.json`**: números de balanceamento para modpacks. São lidos na inicialização; reinicie o jogo ou o servidor depois de editar.

## `config/gtna.yaml`

### gameplay

| Opção | Padrão | Efeito |
|---|---|---|
| `modDifficulty` | `NORMAL` | `JOURNEY` libera os itens utilitários restritos; `NORMAL` mantém desligados |
| `selfRestraint` | `false` | desliga os itens do GTNA que funcionam como trapaça |
| `researchTree` | `true` | a [árvore de pesquisa](../gameplay/systems/research-engine.md) (tecla K, tela, comandos); packs sem nós podem desligar |

### client

| Opção | Padrão | Efeito |
|---|---|---|
| `disableFlyInertia` | `true` | tira a inércia do voo quando você para no ar |
| `wirelessSteamHud` | `false` | HUD do vapor sem fio: saldo, fluxo e hatches conectados |
| `wirelessSteamHudX`, `wirelessSteamHudY` | `5`, `75` | posição do HUD, de 0 a 100 (porcentagem da tela) |
| `wirelessSteamHudHistorySeconds` | `60` | segundos de histórico no gráfico do HUD; 0 esconde |
| `wirelessEnergyHud` | `false` | HUD da energia Nexus |
| `wirelessEnergyHudX`, `wirelessEnergyHudY` | `5`, `60` | posição dele |
| `itemHalo`, `itemGlowEdge`, `itemShaderEffects` | `true` | [efeitos de item](../gameplay/systems/item-effects.md) |
| `itemEffectSpeed` | `100` | velocidade da animação dos efeitos, de 0 a 400 % |

### machines

| Opção | Padrão | Efeito |
|---|---|---|
| `accelerateHatchEnergyCost` | `1.5` | multiplicador de EU com um [Hatch de Aceleração](../gameplay/parts/accelerate-hatch.md) ativo |
| `bufferDrivenMachineMode` | `true` | deixa um [Pattern Buffer](../gameplay/systems/pattern-buffers.md) trocar o modo de uma máquina do GTCEu parada |
| `nexusPlannerEnabled` | `true` | planejador de fabricação das redes do Nexus ME Hypercore |
| `solarBoilerSteamPerCell` | `4000` | vapor por célula ao sol a cada ciclo de 20 ticks no Large Steam Solar Boiler |
| `nexusFluxMatrix.useHighestTierForEfficiency` | `false` | a Flux Matrix usa o maior tier de capacitor em vez da média |

### wirelessSteam {#wireless-steam}

| Opção | Padrão | Efeito |
|---|---|---|
| `enabled` | `true` | chave geral da [rede de vapor sem fio](../gameplay/systems/wireless-steam-network.md) |
| `bronzeInputBuffer` | `100000` | tanque do hatch de entrada de bronze, mB |
| `steelInputBuffer` | `2147483647` | tanque do hatch de entrada de aço |
| `bronzeOutputBuffer` | `128000000` | tanque do hatch de saída de bronze |
| `steelOutputBuffer` | `2147483647` | tanque do hatch de saída de aço |
| `bronzeTransferRate`, `steelTransferRate` | `2147483647` | limite opcional por tick; o padrão move o tanque inteiro |

### restrictedItems {#restricted-items}

| Opção | Padrão | Efeito |
|---|---|---|
| `hideFromJei` | `true` | esconde os itens restritos do JEI e das abas do criativo quando desligados |
| `disableRecipes` | `false` | tira as receitas dos itens restritos |
| `disableUsage` | `false` | bloqueia de vez os itens restritos, menos os grupos liberados abaixo |
| `allowInfinityCovers`, `allowOutputBoostParts`, `allowInfiniteInputParts`, `allowQuantumCosmicNexusArmor`, `allowRealityRipper` | `true` | libera cada grupo |

### machineToggles e hatchToggles

Uma chave `true`/`false` por família de máquina e por família de hatch (por exemplo `largeSteamFurnace`, `eyeOfHarmony`, `threadHatches`, `mePatternBuffer`). Uma entrada desligada **não é registrada**: só mude antes de criar o mundo, ou os blocos já colocados somem.

## Arquivos de balanceamento: `config/gtna/balance/`

| Arquivo | O que controla | Página |
|---|---|---|
| `machines.json` | bônus do Portão a Vapor Envelhecido do Minerador do Vazio | [Mineração do vazio](../gameplay/systems/void-mining.md) |
| `hatches.json` | valores por tier dos Hatches de Threads, Aceleração, Overclock e Saída Ampliada | [Hatches e partes](../gameplay/parts/index.md) |
| `nexus_flux_matrix.json` | capacidade e transferência dos capacitores por tier, política de perda | [Rede de energia Nexus](../gameplay/systems/nexus-energy-network.md) |
| `pattern_buffers.json` | slots de pattern por buffer (1 a 540) | [ME Pattern Buffers](../gameplay/systems/pattern-buffers.md) |
| `pattern_buffer_capacity_history.json` | maior quantidade de slots já usada; guarde junto com o mundo | idem |
| `electric_void_miner.json` | custos, limites e paralelo do Minerador do Vazio Elétrico | [Mineração do vazio](../gameplay/systems/void-mining.md) |
| `void_fluid_drill.json` | programas e paralelo da Void Fluid Drilling Rig | idem |
| `universal_factory.json` | paralelo, threads e aquecimento da Fábrica Universal | [catálogo](../gameplay/machines/catalog/universal_factory.md) |
| `restricted_items.json` | por grupo: ligado, escondido do JEI, receitas removidas | [Hatches e partes](../gameplay/parts/index.md#restricted-parts) |

Grupos restritos no padrão: covers infinitos, armadura Quantum Cosmic Nexus e Reality Ripper vêm **desligados**; peças de entrada infinita e de saída ampliada vêm **ligadas**.

Chaves que faltarem usam o valor padrão, então um pack só precisa escrever o que muda.
