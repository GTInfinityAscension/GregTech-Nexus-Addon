# KubeJS API

GTNA 开箱即支持 KubeJS：安装 KubeJS 后即可使用下列绑定。可直接运行的完整示例位于仓库的 [`examples/kubejs/`](https://github.com/GTInfinityAscension/GregTech-Nexus-Addon/tree/main/examples/kubejs)。

| 功能 | 脚本目录 | 用途 |
|---|---|---|
| [`gtna:multiple_recipes`](#multiple-recipes-machines) | `startup_scripts` | 可同时运行多个配方的新多方块 |
| [`GTNAServerEvents.subPatterns`](#auxiliary-modules) | `server_scripts` | 为任意多方块添加辅助模块 |
| [`GTNAStartupEvents.eyeOfHarmony`](#eye-of-harmony-planets) | `startup_scripts` | 添加或移除鸿蒙之眼的星球 |
| [`GTNAClientEvents.itemEffects`](#item-effects) | `client_scripts` | 物品图标的光环、发光边缘和着色器 |
| [`GTNAPartAbility`](#gtnapartability) | 任意 | 用于结构模式的 GTNA 仓室能力 |

## 配方

GTNA 的配方类型是 `gtna` 命名空间下的 GTCEu 配方类型，因此可以用 `event.recipes.gtna` 搭配常规的 GTCEu KubeJS 语法：

```js
ServerEvents.recipes(event => {
  event.recipes.gtna.hydraulic_manufacturing('kubejs:my_piston')
    .itemInputs('4x gtceu:bronze_plate')
    .itemOutputs('gtna:hydraulic_piston')
    .duration(100)
    .EUt(16)
})
```

每台机器的配方类型列在其[图鉴页](../../gameplay/machines/catalog/index.md)中。[研究引擎](../../gameplay/systems/research-engine.md)可以通过数据包把任意配方 id 锁在研究节点之后。

## 多配方机器 {#multiple-recipes-machines}

`gtna:multiple_recipes` 基于 `WorkableElectricMultipleRecipesMachine` 创建多方块，与工业屠宰场和集成矿石处理厂使用相同的基础。它使用 GTCEu 的多方块构建器，安装[线程仓](../../gameplay/parts/thread-hatch.md)后可同时运行多个不同配方。

```js
GTCEuStartupEvents.registry('gtceu:machine', event => {
  event.create('my_assembly_hall', 'gtna:multiple_recipes')
    .recipeType('gtceu:assembler')
    .rotationState(RotationState.NON_Y_AXIS)
    .appearanceBlock(GTBlocks.CASING_STEEL_SOLID)
    .pattern(definition => FactoryBlockPattern.start()
      .aisle('CCCCC', 'CCCCC', 'CCCCC')
      .aisle('CCCCC', 'C###C', 'CCCCC')
      .aisle('CCCCC', 'C###C', 'CCCCC')
      .aisle('CCCCC', 'C###C', 'CCCCC')
      .aisle('CCCCC', 'CC~CC', 'CCCCC')
      .where('~', Predicates.controller(Predicates.blocks(definition.get())))
      .where('C', Predicates.blocks(GTBlocks.CASING_STEEL_SOLID.get())
        .or(Predicates.autoAbilities(definition.getRecipeTypes()))
        .or(Predicates.abilities(PartAbility.MAINTENANCE).setExactLimit(1))
        .or(Predicates.abilities(GTNAPartAbility.PARALLEL_CONTROL_HATCH).setMaxGlobalLimited(1))
        .or(Predicates.abilities(GTNAPartAbility.THREAD_HATCH).setMaxGlobalLimited(1))
        .or(Predicates.abilities(GTNAPartAbility.ACCELERATE_HATCH).setMaxGlobalLimited(1))
        .or(Predicates.abilities(GTNAPartAbility.OVERCLOCK_HATCH).setMaxGlobalLimited(1)))
      .where('#', Predicates.air())
      .build())
    .workableCasingModel('gtceu:block/casings/solid/machine_casing_solid_steel',
      'gtceu:block/multiblock/implosion_compressor')
})
```

## 辅助模块 {#auxiliary-modules}

为现有多方块（GTNA 或其他模组的）添加可选的额外结构。结构从控制器的位置和朝向开始检测；其中找到的部件会并入机器。玩家看到的效果见[模块](../../gameplay/systems/modules.md)。

```js
GTNAServerEvents.subPatterns(event => {
  // 集成矿石处理厂旁的三格立柱；中间方块可以是输入总线
  event.add('gtna:integrated_ore_processor', definition => FactoryBlockPattern.start()
    .aisle('   A', 'C  A', '   A')
    .where('C', Predicates.controller(Predicates.blocks(definition.get())))
    .where('A', Predicates.blocks(GTBlocks.CASING_STAINLESS_CLEAN.get())
      .or(Predicates.abilities(PartAbility.IMPORT_ITEMS).setMaxGlobalLimited(1)))
    .where(' ', Predicates.any())
    .build(), 'gtna.machine.auxiliary_module.kubejs.item_import')
})
```

| 重载 | 含义 |
|---|---|
| `add(machineId, factory)` | 注册模块 |
| `add(machineId, factory, descriptionKey)` | 用翻译键添加一行提示 |
| `add(machineId, factory, descriptionKey, speedBonus, perfectOverclock)` | 在多配方机器上，加成仅在该模块成型时生效：`2.0` 使时长减半（合计上限 1024 倍）；`true` 在没有超频仓覆盖曲线时启用完美超频 |

## 鸿蒙之眼星球 {#eye-of-harmony-planets}

```js
GTNAStartupEvents.eyeOfHarmony(event => {
  // add(planetItem, dimension, rocketTier[, stoneDust])
  event.add('kubejs:titan_planet_block', 'mymod:titan', 5)
  event.remove('gtna:eye_of_harmony_planet_glacio')
})
```

产物为该维度中注册的 GTCEu 矿脉，并按 GTNH 规则根据火箭等级（0–9）缩放。公式见[鸿蒙之眼](../../gameplay/systems/eye-of-harmony.md)页面。

## 物品特效 {#item-effects}

```js
GTNAClientEvents.itemEffects(event => {
  event.material('gtna:advanced_nitinol').halo(0xFF66CCFF, 8).pulse(true)
  event.item('minecraft:nether_star').cosmic().colors(0xFF050418, 0xFF7FD4FF).glowEdge(0xFFFFAA00, 1.5)
  event.item('minecraft:amethyst_shard').eternal().mask('gtna:mask/cosmic').speed(0.5)
})
```

全部方法见[物品特效](../../gameplay/systems/item-effects.md)页面。每次 F3+T 都会重新运行该脚本。

## GTNAPartAbility {#gtnapartability}

| 绑定 | 仓室 |
|---|---|
| `GTNAPartAbility.THREAD_HATCH` | 线程仓 |
| `GTNAPartAbility.ACCELERATE_HATCH` | 加速仓 |
| `GTNAPartAbility.OVERCLOCK_HATCH` | 超频仓 |
| `GTNAPartAbility.OUTPUT_BOOST_HATCH` | 产出增幅仓 |
| `GTNAPartAbility.PARALLEL_CONTROL_HATCH` | GTCEu 的并行控制仓，包括 GTNA 的 UHV+ 仓（`PARALLEL_HATCH` 为别名） |

在 `Predicates.abilities(...)` 中使用，通常配合 `.setMaxGlobalLimited(1)`。
