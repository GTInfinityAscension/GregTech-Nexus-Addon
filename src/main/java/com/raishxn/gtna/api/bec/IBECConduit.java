package com.raishxn.gtna.api.bec;

import net.minecraft.world.level.block.state.BlockState;

/** A block that carries condensate (the BEC Conduit and its casing). Conduits only join conduits of the same colour. */
public interface IBECConduit {

    /** 0-15 for a dye colour, 16 when unpainted. */
    int getConduitColor(BlockState state);
}
