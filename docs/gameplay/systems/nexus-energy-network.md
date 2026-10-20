# Nexus energy network

GTNA's wireless EU network. Generators push EU into a personal balance and machines pull from it, at any distance, with no cables. The **Nexus Flux Matrix** multiblock sets how much the network can hold.

![Nexus Flux Matrix](../../assets/machines/nexus_flux_matrix.webp){ loading=lazy }

## Parts

| Part | What it does |
|---|---|
| [Nexus Flux Matrix](../machines/catalog/nexus_flux_matrix.md) | the storage: its Nexus Capacitors set the capacity |
| Wireless Energy Hatch | pulls EU from the network into a multiblock. LV to MAX, 1A to 1,048,576A (powers of 4) |
| Wireless Dynamo Hatch | pushes a generator's EU into the network. Same tiers and amperages |
| Wireless Energy Network Input / Output Terminal | multiblock parts that charge a recipe's EU straight from the network, or send generated EU straight to it, up to 9.2 × 10¹⁸ EU per run |
| [Generator Array](../machines/catalog/generator_array.md) | runs up to four GTCEu generators and sends their output to the network |
| Nexus Linker | links hatches to a network that is not yours |
| Quantum Network Terminal | handheld monitor: stored EU, input, output and loss per tick, connections |

A hatch's internal buffer holds `V × 64 × A` EU. Every hatch **binds to the player who placed it**: there is nothing to link in single player.

## The Flux Matrix

The Matrix is a 7 × 7 frame whose middle repeats from 2 to 30 layers. Each layer holds 25 Nexus Capacitors, so a Matrix has 50 to **750** capacitors.

- **Capacity** is the sum of the capacitors.
- **Efficiency** and the **transfer** number use the average capacitor tier (or the highest one, with `machines.nexusFluxMatrix.useHighestTierForEfficiency`).
- **750 MAX capacitors** make the network unlimited: no capacity cap and no transfer cap.
- Energy you deposit stays as your balance even if the Matrix is broken.

| Capacitor | EU per block | Transfer (EU/t) | Works across dimensions |
|---|---:|---:|:---:|
| LV | 160,000 | 2,000 | no |
| MV | 1,500,000 | 8,000 | no |
| HV | 10,000,000 | 32,000 | no |
| EV | 50,000,000 | 128,000 | yes |
| IV | 250,000,000 | 512,000 | yes |
| LuV | 1.5 × 10⁹ | 2,048,000 | yes |
| ZPM | 1.5 × 10¹⁰ | 8,192,000 | yes |
| UV | 1.5 × 10¹¹ | 32,768,000 | yes |
| UHV | 3 × 10¹² | 131,072,000 | yes |
| UEV | 5 × 10¹³ | 524,288,000 | yes |
| UIV | 9 × 10¹⁴ | 2,097,152,000 | yes |
| UXV | 1.5 × 10¹⁶ | 8,388,608,000 | yes |
| OpV | 2.5 × 10¹⁷ | 33,554,432,000 | yes |
| MAX | 5 × 10¹⁸ | 5 × 10²³ | yes |

Values are the defaults of `config/gtna/balance/nexus_flux_matrix.json`; a modpack can change any of them. Below EV average tier, hatches only reach the network from the Matrix's own dimension. The transfer number caps what a Generator Array sends per tick.

## Loss

The balance file also picks **where energy is lost**:

| `lossApplication` | Behaviour |
|---|---|
| `LEGACY` (default) | no loss on the network. The Generator Array keeps its own 5% loss. The Matrix GUI shows an efficiency from 85% (LV) to 100% (MAX) as information |
| `MATRIX_INPUT_ONCE` | each deposit loses a percentage set by the average capacitor tier: 5% LV, 4% MV, 3% HV, 2% EV, 1% IV, 0% from LuV. The network only works while a Matrix is formed |
| `NO_LOSS` | nothing is lost |

The loss is charged once, when EU enters the network, with exact accounting: fractions carry over to the next deposit instead of being rounded away.

## Setting it up

1. Build the Nexus Flux Matrix and fill its middle with capacitors.
2. Put Wireless Dynamo Hatches on generators (or build a Generator Array).
3. Put Wireless Energy Hatches on machines.
4. Check the balance with the Quantum Network Terminal or the HUD (`client.wirelessEnergyHud`).

To use a friend's network: **Shift + right-click** their Matrix with the Nexus Linker to copy it, then **right-click** each hatch. **Shift + right-click** a hatch to unbind it.
