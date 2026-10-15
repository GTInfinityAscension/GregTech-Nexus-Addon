package com.raishxn.gtna.mixin.gtceu;

import com.gregtechceu.gtceu.api.pattern.BlockPattern;

import com.raishxn.gtna.utils.BlockPosHashing;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.ModifyVariable;

import java.util.Map;

/**
 * {@code BlockPattern.getPreview} (the shape every multiblock preview starts from) maps every cell of the bounding
 * box by {@code BlockPos} in a {@code HashMap}; vanilla's position hash collides heavily, so huge structures turn the
 * buckets into trees (seconds for the lance). The same map with a mixed 64-bit hash.
 */
@Mixin(value = BlockPattern.class, remap = false)
public abstract class BlockPatternPreviewMapMixin {

    @ModifyVariable(method = "getPreview", at = @At("STORE"), ordinal = 0)
    private Map<?, ?> gtna$fastPreviewMap(Map<?, ?> blocks) {
        return blocks.isEmpty() ? BlockPosHashing.newMap() : blocks;
    }
}
