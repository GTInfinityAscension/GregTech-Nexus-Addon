package com.raishxn.gtna.api.bec;

import net.minecraft.world.level.material.Fluid;

/** Mutable fluid + long amount, the role of GTNH's {@code IAEFluidStack} in the BEC network. */
public final class CondensateStack {

    public final Fluid fluid;
    public long amount;

    public CondensateStack(Fluid fluid, long amount) {
        this.fluid = fluid;
        this.amount = amount;
    }
}
