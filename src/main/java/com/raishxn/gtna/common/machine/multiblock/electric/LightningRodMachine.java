package com.raishxn.gtna.common.machine.multiblock.electric;

import com.gregtechceu.gtceu.api.machine.IMachineBlockEntity;

import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LightningBolt;

/**
 * GTO {@code lightning_rod}: Arc Generator recipes (they consume EU). While working it throws a visual-only lightning
 * bolt at its rod tip every 20-200 ticks, as GTO does. GTO's tip offset comes from its sealed {@code MachineUtils}; the
 * GTNA tip is 9 blocks behind the controller and 50 up, the same numbers GTO passes.
 */
public class LightningRodMachine extends WorkableElectricMultipleRecipesMachine {

    public LightningRodMachine(IMachineBlockEntity holder) {
        super(holder);
    }

    @Override
    public boolean onWorking() {
        if (!super.onWorking()) return false;
        if (getLevel() instanceof ServerLevel level && getOffsetTimer() % level.random.nextInt(20, 200) == 0) {
            LightningBolt bolt = EntityType.LIGHTNING_BOLT.create(level);
            if (bolt != null) {
                bolt.setPos(getPos().relative(getFrontFacing().getOpposite(), 9).above(50).getCenter());
                bolt.setVisualOnly(true);
                level.addFreshEntity(bolt);
            }
        }
        return true;
    }
}
