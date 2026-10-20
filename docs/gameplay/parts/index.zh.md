# 仓室与部件

GTNA 的多方块部件。每种部件只能用于接受它的结构：在 JEI/EMI 的结构预览中，把鼠标悬停在仓室位置上即可查看可放置的部件。

## 速度与并行

| 部件 | 等级 | 作用 |
|---|---|---|
| [加速仓](accelerate-hatch.md) | LV–MAX | 在常规超频之外缩短所有配方时间 |
| [超频仓](overclock-hatch.md) | UV–MAX | 让每一级超频缩短更多时间 |
| [线程仓](thread-hatch.md) | ZPM–MAX | 同时运行不同的配方 |
| [并行控制仓（UHV+）](advanced-parallel-hatch.md) | UHV–OpV | 1,024 至 262,144 并行 |

三种可调节的仓室都有一个小界面：需要让配方慢一些时，可以打开它降低效果。

## 蒸汽

| 部件 | 作用 |
|---|---|
| 无线蒸汽输入 / 输出仓 | 无需管道传输蒸汽，见[无线蒸汽网络](../systems/wireless-steam-network.md) |
| [巨型蒸汽输入 / 输出总线](huge-steam-bus.md) | 54 格的蒸汽物品总线 |

## AE2 与能量

样板总成、样板总成镜像、ME输出缓存和存储访问仓见 [ME 样板总成](../systems/pattern-buffers.md) 页面。无线能源仓和无线动力仓见 [Nexus 能量网络](../systems/nexus-energy-network.md) 页面。

## 受限部件 {#restricted-parts}

这些部件会破坏正常平衡，供创造模式建造、测试以及需要它们的整合包使用：

| 部件 | 等级 | 作用 |
|---|---|---|
| 无限输入总线 / 输入仓 | LV–MAX | 兼容的多方块读取其中的物品或流体而不消耗 |
| 产出增幅仓、产出增幅输出总线、产出增幅输出仓 | LV–MAX | 倍增配方产出：MV 及以下 25 倍，之后 50 倍、100 倍、250 倍……MAX 为 250,000 倍 |
| 无限蒸汽输入总线 | — | 无限输入总线的蒸汽版本 |
| 产出增幅蒸汽输出总线 | — | 倍增蒸汽多方块的物品产出 |

每组部件都可以在 `config/gtna/balance/restricted_items.json` 中禁用、从 JEI 隐藏或移除配方；见[配置](../../getting-started/configuration.md#restricted-items)。另有仅限创造模式、没有配方的调试部件用于测试。
