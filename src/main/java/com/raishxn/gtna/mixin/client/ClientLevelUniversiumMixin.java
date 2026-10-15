package com.raishxn.gtna.mixin.client;

import net.minecraft.client.multiplayer.ClientLevel;
import net.minecraft.core.BlockPos;
import net.minecraft.world.level.block.state.BlockState;

import com.raishxn.gtna.client.renderer.material.UniversiumRenderer;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/** Every client block change reaches the Universium star field at once (placing a block shows it immediately). */
@Mixin(ClientLevel.class)
public abstract class ClientLevelUniversiumMixin {

    @Inject(method = "sendBlockUpdated", at = @At("TAIL"))
    private void gtna$trackUniversium(BlockPos pos, BlockState oldState, BlockState newState, int flags,
                                      CallbackInfo ci) {
        UniversiumRenderer.blockChanged(pos, newState);
    }
}
