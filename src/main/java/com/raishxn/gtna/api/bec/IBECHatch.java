package com.raishxn.gtna.api.bec;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;

import java.util.List;

/** A Bose-Einstein Condensate Hatch: connects through its front face, and to the BEC multiblocks it belongs to. */
public interface IBECHatch {

    BlockPos getBECPos();

    Direction getBECFacing();

    List<IBECNode> getBECControllers();
}
