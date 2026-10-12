package com.raishxn.gtna.api.bec;

import net.minecraft.world.level.Level;
import net.minecraft.world.level.material.Fluid;

import java.util.List;

/**
 * A formed BEC multiblock on the network (GTNH {@code NotableBECFactoryElement}). Condensate is routed between nodes;
 * conduits and hatches only carry it.
 */
public interface IBECNode {

    Level getBECLevel();

    boolean isBECFormed();

    /** Every BEC Hatch of the structure. */
    List<? extends IBECHatch> getBECHatches();

    /** Hatches routes leave this node through (GTNH {@code getRoutedDiscoverySeeds}); the Diode narrows this. */
    default List<? extends IBECHatch> getRoutedSeeds() {
        return getBECHatches();
    }

    default boolean allowsCondensateThrough(Fluid condensate) {
        return true;
    }
}
