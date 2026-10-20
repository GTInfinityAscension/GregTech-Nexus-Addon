# 配置

GTNA 有两类设置：

- **`config/gtna.yaml`**：玩法、客户端以及每台机器的开关。每个选项也会出现在游戏内配置菜单中，并附有注释。
- **`config/gtna/balance/*.json`**：供整合包使用的平衡数值。启动时读取；修改后请重启游戏或服务器。

## `config/gtna.yaml`

### gameplay

| 选项 | 默认值 | 作用 |
|---|---|---|
| `modDifficulty` | `NORMAL` | `JOURNEY` 启用受限的实用物品；`NORMAL` 保持禁用 |
| `selfRestraint` | `false` | 禁用 GTNA 中类似作弊的受限物品 |
| `researchTree` | `true` | [研究树](../gameplay/systems/research-engine.md)（K 键、界面、命令）；没有节点的整合包可以关闭 |

### client

| 选项 | 默认值 | 作用 |
|---|---|---|
| `disableFlyInertia` | `true` | 在空中停止移动时取消飞行惯性 |
| `wirelessSteamHud` | `false` | 无线蒸汽 HUD：余额、流量和已连接的仓室 |
| `wirelessSteamHudX`、`wirelessSteamHudY` | `5`、`75` | HUD 位置，0 至 100（屏幕百分比） |
| `wirelessSteamHudHistorySeconds` | `60` | HUD 曲线显示的历史秒数，0 为隐藏 |
| `wirelessEnergyHud` | `false` | Nexus 能量 HUD |
| `wirelessEnergyHudX`、`wirelessEnergyHudY` | `5`、`60` | 其位置 |
| `itemHalo`、`itemGlowEdge`、`itemShaderEffects` | `true` | [物品特效](../gameplay/systems/item-effects.md) |
| `itemEffectSpeed` | `100` | 物品特效动画速度，0 至 400 % |

### machines

| 选项 | 默认值 | 作用 |
|---|---|---|
| `accelerateHatchEnergyCost` | `1.5` | [加速仓](../gameplay/parts/accelerate-hatch.md)工作时的 EU 倍率 |
| `bufferDrivenMachineMode` | `true` | 允许[样板总成](../gameplay/systems/pattern-buffers.md)在 GTCEu 机器空闲时切换其模式 |
| `nexusPlannerEnabled` | `true` | Nexus ME超核心网络的合成规划器 |
| `solarBoilerSteamPerCell` | `4000` | 大型蒸汽太阳能锅炉中每个受日照单元每 20 刻产出的蒸汽 |
| `nexusFluxMatrix.useHighestTierForEfficiency` | `false` | 通量矩阵改用电容的最高等级而非平均等级 |

### wirelessSteam {#wireless-steam}

| 选项 | 默认值 | 作用 |
|---|---|---|
| `enabled` | `true` | [无线蒸汽网络](../gameplay/systems/wireless-steam-network.md)总开关 |
| `bronzeInputBuffer` | `100000` | 青铜输入仓储罐，mB |
| `steelInputBuffer` | `2147483647` | 钢制输入仓储罐 |
| `bronzeOutputBuffer` | `128000000` | 青铜输出仓储罐 |
| `steelOutputBuffer` | `2147483647` | 钢制输出仓储罐 |
| `bronzeTransferRate`、`steelTransferRate` | `2147483647` | 可选的每刻传输上限；默认每刻转移整个储罐 |

### restrictedItems {#restricted-items}

| 选项 | 默认值 | 作用 |
|---|---|---|
| `hideFromJei` | `true` | 受限物品被禁用时，从 JEI 和创造模式物品栏中隐藏 |
| `disableRecipes` | `false` | 移除受限物品的配方 |
| `disableUsage` | `false` | 完全禁止受限物品，下方允许的组除外 |
| `allowInfinityCovers`、`allowOutputBoostParts`、`allowInfiniteInputParts`、`allowQuantumCosmicNexusArmor`、`allowRealityRipper` | `true` | 允许对应的组 |

### machineToggles 与 hatchToggles

每个机器系列、每个仓室系列各有一个 `true`/`false` 开关（例如 `largeSteamFurnace`、`eyeOfHarmony`、`threadHatches`、`mePatternBuffer`）。关闭的条目**不会被注册**：只能在创建世界之前修改，否则已放置的方块会消失。

## 平衡文件：`config/gtna/balance/`

| 文件 | 控制内容 | 页面 |
|---|---|---|
| `machines.json` | 古旧蒸汽门虚空采矿机的加成 | [虚空采矿](../gameplay/systems/void-mining.md) |
| `hatches.json` | 线程仓、加速仓、超频仓和产出增幅仓的各等级数值 | [仓室与部件](../gameplay/parts/index.md) |
| `nexus_flux_matrix.json` | 各等级电容的容量与传输、损耗策略 | [Nexus 能量网络](../gameplay/systems/nexus-energy-network.md) |
| `pattern_buffers.json` | 每种样板总成的槽位数（1 至 540） | [ME 样板总成](../gameplay/systems/pattern-buffers.md) |
| `pattern_buffer_capacity_history.json` | 曾经使用过的最大槽位数；请与世界一起保存 | 同上 |
| `electric_void_miner.json` | 电力虚空采矿机的消耗、上限和并行 | [虚空采矿](../gameplay/systems/void-mining.md) |
| `void_fluid_drill.json` | 虚空流体钻机的程序和并行 | 同上 |
| `universal_factory.json` | 通用工厂的并行、线程和预热 | [图鉴](../gameplay/machines/catalog/universal_factory.md) |
| `restricted_items.json` | 每组：是否启用、是否在 JEI 中隐藏、是否移除配方 | [仓室与部件](../gameplay/parts/index.md#restricted-parts) |

受限组默认值：无限覆盖板、Quantum Cosmic Nexus 盔甲和 Reality Ripper 为**关闭**；无限输入部件和产出增幅部件为**开启**。

缺少的键会使用默认值，因此整合包只需写出要修改的数值。
