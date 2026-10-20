# Java API

面向用 Java 编写的附属模组。整合包通常只需要 [KubeJS API](kubejs.md)。

## 依赖 GTNA

正式版本的 jar 位于组织的 Maven 仓库：

```groovy
repositories {
    maven { url = 'https://gtinfinityascension.github.io/maven/' }
}

dependencies {
    modImplementation("com.raishxn.gtna:gtna:<版本>")
    modImplementation("com.gtinfinityascension:gtialib:<版本>")
}
```

GTNA 还需要类路径上有 GTCEu 7.5.3+ 和 Applied Energistics 2。运行时版本见[安装](../../getting-started/installation.md)。

## 公开包

`com.raishxn.gtna.api` 下的内容供附属模组使用。`api` 之外的类可能随时变化。

| 包 | 主要类型 | 用途 |
|---|---|---|
| `api.machine.multiblock` | `GTNAPartAbility`、`GTNASubPatterns`、`ISubPatternMachine`、`IGTNAModuleHost`、`ParallelMachine` | 仓室能力、辅助模块、并行 |
| `api.machine` | `IThreadModifierMachine`、`IZeroEnergyMachine` | 机器行为接口 |
| `api.machine.feature` | `AccelerateHatchMath`、`OverclockHatchMath`、`godforge.GodforgeMath`、`eyeofharmony.EyeOfHarmonyMath`、样板总成模式接口 | 仓室与终局系统背后的公式；wiki 中的表格来自这里 |
| `api.capability` | `WirelessEnergyManager`、`SteamWirelessNetworkManager` | 读取和修改玩家的 Nexus EU 与蒸汽余额 |
| `api.steam` | `GTNASteamBalance` | 通过一个提供器统一调整所有 GTNA 蒸汽多方块的并行和时长 |
| `api.bec` | `BECNetwork`、`CondensateType`、`NaniteTier` | 玻色-爱因斯坦凝聚态网络 |
| `api.render` | `ItemEffect`、`ItemEffectOverrides` | 物品图标特效 |
| `api.registry` | `GTNARegistry` | GTNA 的 Registrate 实例 |

## 部件能力

`GTNAPartAbility` 保存 GTNA 自己的部件位置。常用的有：

| 能力 | 仓室 |
|---|---|
| `THREAD_HATCH` | 线程仓；机器还需要实现 `IThreadModifierMachine`（例如 `WorkableElectricMultipleRecipesMachine`） |
| `ACCELERATE_HATCH` | 加速仓 |
| `OVERCLOCK_HATCH` | 超频仓 |
| `OUTPUT_BOOST_HATCH` | 产出增幅仓 |
| `STEAM_EXPORT_FLUIDS` | 无线蒸汽输出仓 |

其余能力（`BEC_HATCH`、`LINE_OF_SIGHT_HATCH`、`TUNING_HATCH`……）属于特定的 GTNA 机器。

0.6.1 起模块注册表移到了 GTIA Lib（`com.gtinfinityascension.gtialib.module.ModuleRegistry`）；`GTNASubPatterns` 仍可使用并会转发过去。`Int128` 和方块坐标工具移到了 `com.gtinfinityascension.gtialib.data`。
