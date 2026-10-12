package com.raishxn.gtna.common.machine.multiblock.electric.space;

import com.gregtechceu.gtceu.api.GTValues;
import com.gregtechceu.gtceu.api.machine.IMachineBlockEntity;
import com.gregtechceu.gtceu.api.machine.MetaMachine;
import com.gregtechceu.gtceu.api.machine.multiblock.WorkableElectricMultiblockMachine;
import com.gregtechceu.gtceu.api.recipe.GTRecipe;
import com.gregtechceu.gtceu.api.recipe.content.ContentModifier;
import com.gregtechceu.gtceu.api.recipe.modifier.ModifierFunction;
import com.gregtechceu.gtceu.api.recipe.modifier.ParallelLogic;

import net.minecraft.network.chat.Component;

import com.raishxn.gtna.common.data.GTNARecipeDataKeys;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.util.List;

/**
 * GTOCore {@code SpaceElevatorModuleMachine}: a module only works while its Space Elevator runs above ZPM with all
 * its spools. Parallel {@code 4^(Power Module tier - 1)}, duration {@code x sqrt(1 / (elevator tier - ZPM))}, and the
 * Assembler Module refuses recipes whose {@link GTNARecipeDataKeys#POWER_MODULE_TIER} is above the elevator's.
 */
public class SpaceElevatorModuleMachine extends WorkableElectricMultiblockMachine {

    private final boolean checksPowerModuleTier;
    @Nullable
    private SpaceElevatorMachine host;

    public SpaceElevatorModuleMachine(IMachineBlockEntity holder, boolean checksPowerModuleTier) {
        super(holder);
        this.checksPowerModuleTier = checksPowerModuleTier;
    }

    public void setHost(@Nullable SpaceElevatorMachine host) {
        this.host = host;
    }

    @Nullable
    public SpaceElevatorMachine getHost() {
        return host;
    }

    public boolean isConnected() {
        return host != null && host.isOperational();
    }

    /** {@code 4^(power module tier - 1)}. */
    public static int moduleParallel(int powerModuleTier) {
        int exponent = Math.max(0, powerModuleTier - 1);
        return exponent >= 15 ? Integer.MAX_VALUE : 1 << (2 * exponent);
    }

    public static ModifierFunction recipeModifier(MetaMachine machine, @NotNull GTRecipe recipe) {
        if (!(machine instanceof SpaceElevatorModuleMachine module) || !module.isConnected()) {
            return ModifierFunction.NULL;
        }
        var host = module.host;
        if (module.checksPowerModuleTier &&
                recipe.data.getInt(GTNARecipeDataKeys.POWER_MODULE_TIER) > host.getPowerModuleTier()) {
            return ModifierFunction.NULL;
        }
        int parallel = ParallelLogic.getParallelAmount(machine, recipe, moduleParallel(host.getPowerModuleTier()));
        double duration = Math.sqrt(1.0 / Math.max(1, host.getTier() - GTValues.ZPM));
        return ModifierFunction.builder()
                .modifyAllContents(ContentModifier.multiplier(parallel))
                .eutMultiplier(parallel).parallels(parallel).durationMultiplier(duration).build();
    }

    @Override
    public boolean onWorking() {
        // GTO checks every 10 ticks that the elevator still powers the module.
        if (getOffsetTimer() % 10 == 0 && !isConnected()) return false;
        return super.onWorking();
    }

    @Override
    public void addDisplayText(List<Component> textList) {
        super.addDisplayText(textList);
        if (!isFormed()) return;
        textList.add(Component.translatable(isConnected() ? "gtna.machine.space_elevator_module.connected" :
                "gtna.machine.space_elevator_module.not_connected"));
    }
}
