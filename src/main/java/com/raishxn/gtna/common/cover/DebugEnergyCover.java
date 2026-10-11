package com.raishxn.gtna.common.cover;

import com.gregtechceu.gtceu.api.capability.ICoverable;
import com.gregtechceu.gtceu.api.capability.IEnergyContainer;
import com.gregtechceu.gtceu.api.cover.CoverBehavior;
import com.gregtechceu.gtceu.api.cover.CoverDefinition;
import com.gregtechceu.gtceu.api.machine.MetaMachine;
import com.gregtechceu.gtceu.api.machine.TickableSubscription;

import net.minecraft.MethodsReturnNonnullByDefault;
import net.minecraft.core.Direction;

import org.jetbrains.annotations.Nullable;

import javax.annotation.ParametersAreNonnullByDefault;

/**
 * Debug Energy Cover, for testing: keeps the energy buffer of the machine it is attached to full every tick. Works on
 * any GregTech machine with an energy buffer (singleblocks, generators, batteries, hatches). Creative only.
 */
@ParametersAreNonnullByDefault
@MethodsReturnNonnullByDefault
public class DebugEnergyCover extends CoverBehavior {

    private TickableSubscription subscription;

    public DebugEnergyCover(CoverDefinition definition, ICoverable coverHolder, Direction attachedSide) {
        super(definition, coverHolder, attachedSide);
    }

    @Override
    public boolean canAttach() {
        return super.canAttach() && container() != null;
    }

    /** The machine's own energy buffer, read from its traits so no side or cover filtering gets in the way. */
    private @Nullable IEnergyContainer container() {
        MetaMachine machine = MetaMachine.getMachine(coverHolder.getLevel(), coverHolder.getPos());
        if (machine == null) return null;
        for (var trait : machine.getTraits()) {
            if (trait instanceof IEnergyContainer energy && energy.getEnergyCapacity() > 0) return energy;
        }
        return null;
    }

    @Override
    public void onLoad() {
        super.onLoad();
        subscription = coverHolder.subscribeServerTick(subscription, this::update);
    }

    @Override
    public void onRemoved() {
        super.onRemoved();
        if (subscription != null) {
            subscription.unsubscribe();
            subscription = null;
        }
    }

    public void update() {
        var container = container();
        if (container == null) return;
        long missing = container.getEnergyCapacity() - container.getEnergyStored();
        if (missing > 0) container.changeEnergy(missing);
    }
}
