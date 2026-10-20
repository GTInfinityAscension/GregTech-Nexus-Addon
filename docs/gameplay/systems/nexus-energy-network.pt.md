# Rede de energia Nexus

A rede de EU sem fio do GTNA. Geradores mandam EU para um saldo pessoal e as máquinas tiram dele, a qualquer distância, sem cabos. O multibloco **Nexus Flux Matrix** define quanto a rede consegue guardar.

![Nexus Flux Matrix](../../assets/machines/nexus_flux_matrix.webp){ loading=lazy }

## Peças

| Peça | O que faz |
|---|---|
| [Nexus Flux Matrix](../machines/catalog/nexus_flux_matrix.md) | o armazenamento: os Nexus Capacitors definem a capacidade |
| Hatch de Energia sem Fio | tira EU da rede para um multibloco. De LV a MAX, de 1A a 1.048.576A (potências de 4) |
| Hatch Dínamo sem Fio | manda o EU de um gerador para a rede. Mesmos tiers e amperagens |
| Terminal Wireless de Entrada / Saída da Rede Nexus | peças de multibloco que cobram o EU de uma receita direto da rede, ou mandam o EU gerado direto para ela, até 9,2 × 10¹⁸ EU por operação |
| [Matriz de Geradores](../machines/catalog/generator_array.md) | roda até quatro geradores do GTCEu e manda a saída para a rede |
| Nexus Linker | liga hatches a uma rede que não é sua |
| Quantum Network Terminal | monitor de mão: EU guardado, entrada, saída e perda por tick, conexões |

O buffer interno de um hatch guarda `V × 64 × A` EU. Todo hatch **se liga ao jogador que o colocou**: no single player não há nada para ligar.

## A Flux Matrix

A Matrix é uma moldura de 7 × 7 cujo meio se repete de 2 a 30 camadas. Cada camada leva 25 Nexus Capacitors, então uma Matrix tem de 50 a **750** capacitores.

- A **capacidade** é a soma dos capacitores.
- A **eficiência** e o número de **transferência** usam o tier médio dos capacitores (ou o maior, com `machines.nexusFluxMatrix.useHighestTierForEfficiency`).
- **750 capacitores MAX** deixam a rede ilimitada: sem teto de capacidade nem de transferência.
- A energia depositada continua no seu saldo mesmo se a Matrix for quebrada.

| Capacitor | EU por bloco | Transferência (EU/t) | Funciona entre dimensões |
|---|---:|---:|:---:|
| LV | 160.000 | 2.000 | não |
| MV | 1.500.000 | 8.000 | não |
| HV | 10.000.000 | 32.000 | não |
| EV | 50.000.000 | 128.000 | sim |
| IV | 250.000.000 | 512.000 | sim |
| LuV | 1,5 × 10⁹ | 2.048.000 | sim |
| ZPM | 1,5 × 10¹⁰ | 8.192.000 | sim |
| UV | 1,5 × 10¹¹ | 32.768.000 | sim |
| UHV | 3 × 10¹² | 131.072.000 | sim |
| UEV | 5 × 10¹³ | 524.288.000 | sim |
| UIV | 9 × 10¹⁴ | 2.097.152.000 | sim |
| UXV | 1,5 × 10¹⁶ | 8.388.608.000 | sim |
| OpV | 2,5 × 10¹⁷ | 33.554.432.000 | sim |
| MAX | 5 × 10¹⁸ | 5 × 10²³ | sim |

Os valores são o padrão de `config/gtna/balance/nexus_flux_matrix.json`; um modpack pode mudar qualquer um. Com tier médio abaixo de EV, os hatches só alcançam a rede na mesma dimensão da Matrix. O número de transferência limita o que uma Matriz de Geradores manda por tick.

## Perda

O arquivo de balanceamento também escolhe **onde a energia se perde**:

| `lossApplication` | Comportamento |
|---|---|
| `LEGACY` (padrão) | sem perda na rede. A Matriz de Geradores mantém a própria perda de 5%. A GUI da Matrix mostra uma eficiência de 85% (LV) a 100% (MAX) só como informação |
| `MATRIX_INPUT_ONCE` | cada depósito perde uma porcentagem definida pelo tier médio dos capacitores: 5% LV, 4% MV, 3% HV, 2% EV, 1% IV, 0% a partir de LuV. A rede só funciona com uma Matrix formada |
| `NO_LOSS` | nada se perde |

A perda é cobrada uma vez, quando o EU entra na rede, com conta exata: as frações passam para o próximo depósito em vez de sumirem no arredondamento.

## Montando

1. Construa a Nexus Flux Matrix e encha o meio com capacitores.
2. Ponha Hatches Dínamo sem Fio nos geradores (ou monte uma Matriz de Geradores).
3. Ponha Hatches de Energia sem Fio nas máquinas.
4. Veja o saldo no Quantum Network Terminal ou no HUD (`client.wirelessEnergyHud`).

Para usar a rede de um amigo: **Shift + clique direito** na Matrix dele com o Nexus Linker para copiar, depois **clique direito** em cada hatch. **Shift + clique direito** num hatch desfaz a ligação.
