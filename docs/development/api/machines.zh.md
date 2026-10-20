# 机器 API

如何制作使用 GTNA 仓室的多方块。同一台机器的 KubeJS 写法见 [KubeJS API](kubejs.md#multiple-recipes-machines) 页面。

## 支持全部 GTNA 仓室的机器

`WorkableElectricMultipleRecipesMachine` 在装有线程仓时可同时运行多个配方，并应用加速仓和超频仓。没有这个类时，线程仓不起作用。

```java
import com.gregtechceu.gtceu.GTCEu;
import com.gregtechceu.gtceu.api.data.RotationState;
import com.gregtechceu.gtceu.api.machine.MultiblockMachineDefinition;
import com.gregtechceu.gtceu.api.pattern.FactoryBlockPattern;
import com.gregtechceu.gtceu.common.data.GTBlocks;
import com.gregtechceu.gtceu.common.data.GTRecipeTypes;
import com.raishxn.gtna.api.machine.multiblock.GTNAPartAbility;
import com.raishxn.gtna.common.machine.multiblock.electric.WorkableElectricMultipleRecipesMachine;

import static com.gregtechceu.gtceu.api.machine.multiblock.PartAbility.*;
import static com.gregtechceu.gtceu.api.pattern.Predicates.*;

public class MyMachines {

    public static final MultiblockMachineDefinition THREADED_ASSEMBLER = REGISTRATE
            .multiblock("threaded_assembler", WorkableElectricMultipleRecipesMachine::new)
            .rotationState(RotationState.NON_Y_AXIS)
            .recipeType(GTRecipeTypes.ASSEMBLER_RECIPES)
            .appearanceBlock(GTBlocks.CASING_STEEL_SOLID)
            .pattern(definition -> FactoryBlockPattern.start()
                    .aisle("CCCCC", "CCCCC", "CCCCC")
                    .aisle("CCCCC", "C###C", "CCCCC")
                    .aisle("CCCCC", "C###C", "CCCCC")
                    .aisle("CCCCC", "C###C", "CCCCC")
                    .aisle("CCCCC", "CC~CC", "CCCCC")
                    .where('~', controller(blocks(definition.get())))
                    .where('C', blocks(GTBlocks.CASING_STEEL_SOLID.get())
                            .or(autoAbilities(definition.getRecipeTypes()))
                            .or(abilities(MAINTENANCE).setExactLimit(1))
                            .or(abilities(PARALLEL_HATCH).setMaxGlobalLimited(1))
                            .or(abilities(GTNAPartAbility.THREAD_HATCH).setMaxGlobalLimited(1))
                            .or(abilities(GTNAPartAbility.ACCELERATE_HATCH).setMaxGlobalLimited(1))
                            .or(abilities(GTNAPartAbility.OVERCLOCK_HATCH).setMaxGlobalLimited(1)))
                    .where('#', air())
                    .build())
            .workableCasingModel(GTCEu.id("block/casings/solid/machine_casing_solid_steel"),
                    GTCEu.id("block/multiblock/implosion_compressor"))
            .register();
}
```

`WorkableElectricMultipleRecipesMachine` 位于 `common` 而不是 `api`：实际上很稳定，但更新 GTNA 时请查看更新日志。

## 为现有机器添加模块

```java
GTNASubPatterns.register(new ResourceLocation("gtceu", "electric_blast_furnace"),
        definition -> FactoryBlockPattern.start()
                /* 以控制器为锚点的额外结构 */
                .build(),
        Component.translatable("mymod.module.tooltip"));
```

模块对机器而言是可选的，会作为 JEI/EMI 预览的额外一页显示，并在控制器物品上列出提示文字。Java 机器也可以通过实现 `ISubPatternMachine` 自行声明模块；这类模块不会出现在预览中。

## Java 还是 KubeJS？

| | Java | KubeJS |
|---|---|---|
| 适用于 | 附属模组、自定义逻辑 | 整合包 |
| 机器类 | `WorkableElectricMultipleRecipesMachine::new` | `'gtna:multiple_recipes'` |
| 能力 | `GTNAPartAbility.*` | `GTNAPartAbility.*` （绑定） |
| 配方 | `GTRecipeBuilder` / `GTNARecipeType` | `event.recipes.gtna.<type>` |
