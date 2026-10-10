package com.raishxn.gtna.common.machine.multiblock.electric;

import com.gregtechceu.gtceu.api.machine.IMachineBlockEntity;
import com.gregtechceu.gtceu.api.recipe.GTRecipe;
import com.gregtechceu.gtceu.api.recipe.OverclockingLogic;

import net.minecraft.core.BlockPos;
import net.minecraft.world.level.Level;

import earth.terrarium.adastra.api.planets.PlanetApi;
import org.jetbrains.annotations.Nullable;

/**
 * GTO {@code SpaceProbeSurfaceReceptionMachine}: works only in space (Ad Astra) and only while the 9x9 area above its
 * dish sees the sky (checked every second, 8 blocks behind and 28 up, the numbers GTO passes). GTO's Dyson Sphere
 * bonus is not ported (no Dyson Sphere in GTNA). Perfect overclock comes from the recipe modifier.
 */
public class SpaceProbeSurfaceReceptionMachine extends WorkableElectricMultipleRecipesMachine {

    public SpaceProbeSurfaceReceptionMachine(IMachineBlockEntity holder) {
        super(holder);
    }

    /** GTO {@code perfectOverclocking}. */
    @Override
    public OverclockingLogic getOverclockingLogic() {
        return OverclockingLogic.PERFECT_OVERCLOCK;
    }

    public boolean inSpace() {
        Level level = getLevel();
        return level != null && PlanetApi.API.isSpace(level);
    }

    /** The 9x9 area above the dish sees the sky. */
    public boolean dishSeesSky() {
        Level level = getLevel();
        if (level == null) return false;
        BlockPos dish = getPos().relative(getFrontFacing().getOpposite(), 8).above(28);
        for (int i = -4; i < 5; i++) {
            for (int j = -4; j < 5; j++) {
                if (!level.canSeeSky(dish.offset(i, 0, j))) return false;
            }
        }
        return true;
    }

    @Override
    public boolean beforeWorking(@Nullable GTRecipe recipe) {
        return inSpace() && dishSeesSky() && super.beforeWorking(recipe);
    }

    /** Checked every second; a covered dish stops the recipe (GTCEu interrupts it). */
    @Override
    public boolean onWorking() {
        if (!super.onWorking()) return false;
        return getOffsetTimer() % 20 != 0 || dishSeesSky();
    }
}
