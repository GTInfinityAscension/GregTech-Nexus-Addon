# API de máquinas

Como fazer um multibloco que usa os hatches do GTNA. A mesma máquina em KubeJS está na página da [API KubeJS](kubejs.md#multiple-recipes-machines).

## Uma máquina com todos os hatches do GTNA

`WorkableElectricMultipleRecipesMachine` roda várias receitas de uma vez quando há um Hatch de Threads e aplica os Hatches de Aceleração e de Overclock. Sem essa classe, o Hatch de Threads não tem efeito.

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

`WorkableElectricMultipleRecipesMachine` fica em `common`, não em `api`: na prática é estável, mas confira o changelog ao atualizar o GTNA.

## Acrescentando um módulo a uma máquina existente

```java
GTNASubPatterns.register(new ResourceLocation("gtceu", "electric_blast_furnace"),
        definition -> FactoryBlockPattern.start()
                /* a estrutura extra, ancorada no controlador */
                .build(),
        Component.translatable("mymod.module.tooltip"));
```

O módulo é opcional para a máquina, aparece como página extra na prévia do JEI/EMI e mostra as linhas de tooltip no item do controlador. Máquinas Java também podem declarar módulos próprios implementando `ISubPatternMachine`; esses não aparecem na prévia.

## Java ou KubeJS?

| | Java | KubeJS |
|---|---|---|
| Use para | addons, lógica própria | modpacks |
| Classe da máquina | `WorkableElectricMultipleRecipesMachine::new` | `'gtna:multiple_recipes'` |
| Abilities | `GTNAPartAbility.*` | `GTNAPartAbility.*` (binding) |
| Receitas | `GTRecipeBuilder` / `GTNARecipeType` | `event.recipes.gtna.<type>` |
