# Machines API

How to make a multiblock that uses GTNA's hatches. The same machine in KubeJS is on the [KubeJS API](kubejs.md#multiple-recipes-machines) page.

## A machine with every GTNA hatch

`WorkableElectricMultipleRecipesMachine` runs several recipes at once when a Thread Hatch is present, and applies the Accelerate and Overclock Hatches. Without that class, a Thread Hatch has no effect.

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

`WorkableElectricMultipleRecipesMachine` is in `common`, not `api`: it is stable in practice, but check the changelog when you update GTNA.

## Adding a module to an existing machine

```java
GTNASubPatterns.register(new ResourceLocation("gtceu", "electric_blast_furnace"),
        definition -> FactoryBlockPattern.start()
                /* the extra structure, anchored at the controller */
                .build(),
        Component.translatable("mymod.module.tooltip"));
```

The module is optional for the machine, shows as an extra page in the JEI/EMI preview and lists the tooltip lines on the controller item. Java machines can also declare modules themselves by implementing `ISubPatternMachine`; those do not appear in the preview.

## Java or KubeJS?

| | Java | KubeJS |
|---|---|---|
| Use for | addons, custom logic | modpacks |
| Machine class | `WorkableElectricMultipleRecipesMachine::new` | `'gtna:multiple_recipes'` |
| Abilities | `GTNAPartAbility.*` | `GTNAPartAbility.*` (binding) |
| Recipes | `GTRecipeBuilder` / `GTNARecipeType` | `event.recipes.gtna.<type>` |
