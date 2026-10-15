package com.raishxn.gtna.mixin.client;

import com.gregtechceu.gtceu.api.gui.widget.PatternPreviewWidget;

import com.lowdragmc.lowdraglib.utils.BlockInfo;

import net.minecraft.core.BlockPos;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;

import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Unique;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Redirect;

import java.util.IdentityHashMap;
import java.util.Map;

/**
 * Multiblock preview (JEI/EMI page, built for every multiblock on world join): GTCEu puts every cell of the
 * structure's bounding box in its block map, air included. For the Kinetic Orbital Lance that is 4.5 million entries
 * for 171 000 blocks, then one ItemStack each to count materials. Air is left out (the preview level reads absent
 * positions as air anyway) and the material item of a block without a block entity is computed once per state.
 */
@Mixin(value = PatternPreviewWidget.class, remap = false)
public abstract class PatternPreviewAirMixin {

    @Unique
    private static final Map<BlockState, ItemStack> GTNA$CLONES = new IdentityHashMap<>();

    @Redirect(method = "initializePattern",
              at = @At(value = "INVOKE",
                       target = "Ljava/util/Map;put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;"))
    private Object gtna$skipAir(Map<Object, Object> map, Object pos, Object info) {
        if (info instanceof BlockInfo block && block.getBlockState().isAir() && !block.hasBlockEntity()) return null;
        return map.put(pos, info);
    }

    @Redirect(method = "gatherBlockDrops",
              at = @At(value = "INVOKE",
                       target = "Lnet/minecraft/world/level/block/Block;getCloneItemStack(Lnet/minecraft/world/level/BlockGetter;Lnet/minecraft/core/BlockPos;Lnet/minecraft/world/level/block/state/BlockState;)Lnet/minecraft/world/item/ItemStack;",
                       remap = true))
    private ItemStack gtna$cachedClone(Block block, BlockGetter level, BlockPos pos, BlockState state) {
        if (state.hasBlockEntity()) return block.getCloneItemStack(level, pos, state);
        synchronized (GTNA$CLONES) {
            return GTNA$CLONES.computeIfAbsent(state, s -> block.getCloneItemStack(level, pos, s)).copy();
        }
    }
}
