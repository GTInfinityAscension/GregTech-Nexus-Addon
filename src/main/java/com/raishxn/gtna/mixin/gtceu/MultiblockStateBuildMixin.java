package com.raishxn.gtna.mixin.gtceu;

import com.gregtechceu.gtceu.api.pattern.MultiblockState;

import net.minecraft.core.BlockPos;
import net.minecraft.world.level.block.state.BlockState;

import com.raishxn.gtna.common.item.terminal.NexusBuildCheckGuard;
import com.raishxn.gtna.common.machine.multiblock.originals.StructureWatch;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/**
 * The terminal checks its target once after the build instead of once per placed block; the original multiblocks
 * test only the changed position ({@link StructureWatch}) instead of re-walking their whole pattern.
 */
@Mixin(value = MultiblockState.class, remap = false)
public abstract class MultiblockStateBuildMixin {

    @Inject(method = "onBlockStateChanged", at = @At("HEAD"), cancellable = true, remap = false, require = 0)
    private void gtna$deferTerminalBuildCheck(BlockPos pos, BlockState state, CallbackInfo ci) {
        var self = (MultiblockState) (Object) this;
        if (NexusBuildCheckGuard.skips(self, pos)) {
            ci.cancel();
            return;
        }
        if (!pos.equals(self.controllerPos) && self.getController() instanceof StructureWatch.Host host &&
                host.structureWatch().usable()) {
            host.structureWatch().blockChanged(pos, state);
            ci.cancel();
        }
    }
}
