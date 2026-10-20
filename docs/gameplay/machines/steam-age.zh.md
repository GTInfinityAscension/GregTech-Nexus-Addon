# 蒸汽时代

GTNA 把蒸汽时代变成一个完整的工厂阶段：带并行的大型蒸汽多方块、无需管道的蒸汽、完全不需要能量的机器，以及能前往其他星球的蒸汽电梯。这里的每台机器都有带结构的[图鉴页](catalog/index.md)。

## 蒸汽供应

| 机器 | 提供 |
|---|---|
| [大型蒸汽太阳能锅炉](catalog/large_steam_solar_boiler.md) | 可扩展的太阳能沸腾单元阵列，侧向最多 63 格、向后最多 125 格；产量随受到日照的单元增加。它是唯一能安装[无线蒸汽输出仓](../systems/wireless-steam-network.md)的结构 |
| [仙人掌奇观](catalog/steam_cactus_wonder.md) | 燃烧煤炭或木炭（每个 8,000 mB 蒸汽）或煤炭块（90,000 mB），每秒一个；沙地上需要长满的仙人掌 |
| [大型蒸汽储罐](catalog/large_steam_storage_tank.md) | 储存 120,000,000 mB 蒸汽，平滑锅炉输出 |
| [超维度等蒸汽锅炉](catalog/dimensionally_transcendent_steam_boiler.md) | 来自 GregTech Leisure 的超大型后期锅炉 |

然后用[无线蒸汽网络](../systems/wireless-steam-network.md)代替管道输送蒸汽。

## 大型蒸汽机器

GregTech 基础机器的蒸汽版本，移植自 GT: Not Leisure：熔炉、研磨机、合金炉、压缩机、提取机、锻造锤、车床、切割机、卷板机、压模器、线材轧机、冲压机床、筛选机、搅拌机、离心机、热力离心机、洗矿机、化学浸洗机和电路组装机。

- 它们一次处理大量物品。并行上限因机器而异，可在控制器中调低：

    | 并行 | 机器 |
    |---:|---|
    | 128 | 熔炉、破碎机 |
    | 96 | 洗矿机 |
    | 64 | 合金炉、锻造锤、搅拌机、离心机、热力离心机、浸洗机 |
    | 48 | 压缩机、提取机 |
    | 32 | 冲压机床 |
    | 16 | 车床、切割机、卷板机、压模器、线材轧机、筛选机 |
    | 4 | 电路组装机 |

- 每台都比单方块版本更快：熔炉 10 倍，洗矿机 5 倍，压缩机和冲压机床 2.5 倍，合金炉和提取机约 1.75 倍，其余 2 倍。
- **高压：**用钢制外壳代替青铜外壳建造结构（所有外壳都必须是钢制），机器速度翻倍，蒸汽消耗也翻倍。
- 使用[巨型蒸汽总线](../parts/huge-steam-bus.md)（54 格）为它们供料。

它们的配方使用 GTNA 的[液压组件](../systems/hydraulic-system.md)，可以手工制作，也可以在**蒸汽制造厂**中制作。

## 原始机器

这些机器都不消耗 EU，只有炼狱焦炉使用蒸汽。

| 机器 | 要点 |
|---|---|
| [炼狱焦炉](catalog/infernal_coke_oven.md) | 每 5 秒加速 1%，最高 10 倍；每 10 分钟增加 16 并行（8 至 256）。消耗蒸汽：6,400 L/s，每阶段再加 1,600 L/s。空闲时速度加成会衰减 |
| [超压反应堆](catalog/hyper_pressure_reactor.md) | 无需能量和蒸汽的流体反应，1 并行；紧凑型有 512 并行 |
| [跃进一号高炉](catalog/leap_forward_one_blast_furnace.md) | 可以长高的原始高炉：每增加一层并行翻倍（最高 32,000），20 秒的循环再加 20 秒 |
| [原始石炉](catalog/primitive_stone_furnace.md) | 同时运行所有熔炉配方，每个 1 刻完成 |
| [砖窑](catalog/brick_kiln.md) | 用压缩黏土和煤烧制砖块与陶瓷 |

## 专用机器

| 机器 | 作用 |
|---|---|
| [石材超级加热器](catalog/stone_superheater.md) | 蒸汽时代的超级加热配方，32 并行 |
| [蒸汽伐木机](catalog/steam_woodcutter.md) | 放入树苗，产出原木，64 并行 |
| [蒸汽圆石机](catalog/steam_cobbler.md) | 碎石机；电路选择石头种类，16 并行 |
| [蒸汽制造厂](catalog/steam_manufacturer.md) | 液压制造，16 并行；制造最大的蒸汽机器 |
| [蒸汽超级压缩机](catalog/steam_mega_compressor.md) | 256 并行；由 64 台大型蒸汽压缩机制成 |
| [古旧蒸汽门虚空采矿机](catalog/void_miner_steam_gate_aged.md) | 凭空开采粗矿；见[虚空采矿](../systems/void-mining.md) |

大多数机器都可以在控制器中调低并行。

## 蒸汽电梯

[蒸汽电梯](catalog/steam_elevator.md)是一个拥有最多 12 个模块槽位的模块化结构。安装 Ad Astra 后，*出发*会打开星球选择界面。模块只有在安装到电梯上时才工作：

| 模块 | 等级 |
|---|---|
| 飞行、信标、天气、驱怪、实体粉碎、石油钻井 | I、II、III |
| 温室种植、蒸汽动力蜂箱、育蜂、矿石处理 | 各一种 |

育蜂模块只有在安装 Productive Bees 时才存在。

## 整合包平衡

整合包可以在 Java 中通过一个入口（`GTNASteamBalance`）统一调整**所有** GTNA 蒸汽多方块的并行和时长，例如按难度区分。
