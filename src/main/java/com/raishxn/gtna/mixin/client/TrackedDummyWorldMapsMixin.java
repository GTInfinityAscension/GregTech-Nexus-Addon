package com.raishxn.gtna.mixin.client;

import com.lowdragmc.lowdraglib.utils.BlockInfo;
import com.lowdragmc.lowdraglib.utils.TrackedDummyWorld;

import net.minecraft.core.BlockPos;
import net.minecraft.world.level.block.entity.BlockEntity;

import com.gtinfinityascension.gtialib.data.BlockPosHashing;
import org.spongepowered.asm.mixin.Final;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Mutable;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

import java.util.Map;

/**
 * Multiblock preview worlds hold every block of the structure in these maps and look them up for each neighbour of
 * each block while the scene compiles; with vanilla {@code BlockPos} hashing a large structure takes seconds. See
 * {@link BlockPosHashing}.
 */
@Mixin(value = TrackedDummyWorld.class, remap = false)
public abstract class TrackedDummyWorldMapsMixin {

    @Shadow
    @Final
    @Mutable
    public Map<BlockPos, BlockInfo> renderedBlocks;
    @Shadow
    @Final
    @Mutable
    public Map<BlockPos, BlockEntity> blockEntities;

    @Inject(method = "<init>*", at = @At("RETURN"))
    private void gtna$fastMaps(CallbackInfo ci) {
        renderedBlocks = BlockPosHashing.newMap();
        blockEntities = BlockPosHashing.newMap();
    }
}
