package com.raishxn.gtna.common.machine.multiblock.part.bec;

import com.gregtechceu.gtceu.api.machine.IMachineBlockEntity;
import com.gregtechceu.gtceu.api.machine.feature.multiblock.IMultiController;
import com.gregtechceu.gtceu.api.machine.multiblock.part.MultiblockPartMachine;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;

import com.raishxn.gtna.api.bec.BECNetwork;
import com.raishxn.gtna.api.bec.IBECHatch;
import com.raishxn.gtna.api.bec.IBECNode;

import java.util.ArrayList;
import java.util.List;

/**
 * GTNH {@code MTEHatchBEC} (Bose-Einstein Condensate Hatch): joins a BEC multiblock to the conduit network through its
 * front face.
 */
public class BECHatchPartMachine extends MultiblockPartMachine implements IBECHatch {

    public BECHatchPartMachine(IMachineBlockEntity holder) {
        super(holder);
    }

    @Override
    public BlockPos getBECPos() {
        return getPos();
    }

    @Override
    public Direction getBECFacing() {
        return getFrontFacing();
    }

    @Override
    public List<IBECNode> getBECControllers() {
        List<IBECNode> out = new ArrayList<>();
        for (IMultiController controller : getControllers()) if (controller instanceof IBECNode node) out.add(node);
        return out;
    }

    @Override
    public void onLoad() {
        super.onLoad();
        BECNetwork.invalidate();
    }

    @Override
    public void onUnload() {
        super.onUnload();
        BECNetwork.invalidate();
    }

    @Override
    public void onRotated(Direction oldFacing, Direction newFacing) {
        super.onRotated(oldFacing, newFacing);
        BECNetwork.invalidate();
    }

    @Override
    public void addedToController(IMultiController controller) {
        super.addedToController(controller);
        BECNetwork.invalidate();
    }

    @Override
    public void removedFromController(IMultiController controller) {
        super.removedFromController(controller);
        BECNetwork.invalidate();
    }

    @Override
    public boolean canShared() {
        return false;
    }
}
