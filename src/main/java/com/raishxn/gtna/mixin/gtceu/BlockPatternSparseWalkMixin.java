package com.raishxn.gtna.mixin.gtceu;

import com.gregtechceu.gtceu.api.block.ActiveBlock;
import com.gregtechceu.gtceu.api.machine.IMachineBlockEntity;
import com.gregtechceu.gtceu.api.machine.feature.multiblock.IMultiPart;
import com.gregtechceu.gtceu.api.pattern.BlockPattern;
import com.gregtechceu.gtceu.api.pattern.MultiblockState;
import com.gregtechceu.gtceu.api.pattern.TraceabilityPredicate;
import com.gregtechceu.gtceu.api.pattern.error.PatternError;
import com.gregtechceu.gtceu.api.pattern.error.PatternStringError;
import com.gregtechceu.gtceu.api.pattern.error.SinglePredicateError;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;

import it.unimi.dsi.fastutil.longs.Long2ObjectOpenHashMap;
import it.unimi.dsi.fastutil.longs.LongOpenHashSet;
import org.spongepowered.asm.mixin.Final;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.Unique;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

import java.util.HashMap;
import java.util.HashSet;

/**
 * Structure check of huge fixed-size patterns without visiting their empty cells.
 *
 * <p>
 * {@code BlockPattern.checkPatternAt} visits every cell of the pattern's bounding box, including the {@code any()}
 * cells around the structure, and for each one reads the world (block entity, block state) and stores an IO entry.
 * For a sparse pattern such as the Kinetic Orbital Lance that is 4.5 million cells for 171 000 blocks, in every
 * structure check and in every multiblock preview. For patterns without repeatable aisles (where the search for the
 * first aisle cannot shift) this runs the same walk, in the same order and with the same effects for every
 * structure cell, but skips {@code any()} cells: they always match, are never cached and never collect parts.
 * GTCEu's own walk still runs for every other pattern.
 *
 * <p>
 * Walk adapted from GTCEu 7.5.3 {@code BlockPattern.checkPatternAt} (LGPL-3.0).
 */
@Mixin(value = BlockPattern.class, remap = false)
public abstract class BlockPatternSparseWalkMixin {

    /** Bounding boxes above this many cells take the sparse walk. */
    @Unique
    private static final int GTNA$SPARSE_CELLS = 200_000;

    @Shadow
    @Final
    public int[][] aisleRepetitions;
    @Shadow
    @Final
    protected TraceabilityPredicate[][][] blockMatches;
    @Shadow
    @Final
    protected int fingerLength;
    @Shadow
    @Final
    protected int thumbLength;
    @Shadow
    @Final
    protected int palmLength;
    @Shadow
    @Final
    protected int[] centerOffset;
    @Shadow
    protected int[] formedRepetitionCount;

    @Shadow
    protected abstract BlockPos setActualRelativeOffset(int x, int y, int z, Direction facing,
                                                        Direction upwardsFacing, boolean isFlipped);

    @Unique
    private Boolean gtna$sparse;

    @Unique
    private boolean gtna$sparse() {
        if (gtna$sparse == null) {
            boolean fixed = (long) fingerLength * thumbLength * palmLength > GTNA$SPARSE_CELLS;
            for (int[] r : aisleRepetitions) fixed &= r[0] == 1 && r[1] == 1;
            gtna$sparse = fixed;
        }
        return gtna$sparse;
    }

    @Inject(method = "checkPatternAt(Lcom/gregtechceu/gtceu/api/pattern/MultiblockState;Lnet/minecraft/core/BlockPos;Lnet/minecraft/core/Direction;Lnet/minecraft/core/Direction;ZZ)Z",
            at = @At("HEAD"),
            cancellable = true)
    private void gtna$sparseWalk(MultiblockState worldState, BlockPos centerPos, Direction frontFacing,
                                 Direction upwardsFacing, boolean isFlipped, boolean savePredicate,
                                 CallbackInfoReturnable<Boolean> cir) {
        if (gtna$sparse()) cir.setReturnValue(gtna$walk(worldState, centerPos, frontFacing, upwardsFacing, isFlipped,
                savePredicate));
    }

    @Unique
    private boolean gtna$walk(MultiblockState worldState, BlockPos centerPos, Direction frontFacing,
                              Direction upwardsFacing, boolean isFlipped, boolean savePredicate) {
        worldState.clean();
        var matchContext = worldState.getMatchContext();
        var globalCount = worldState.getGlobalCount();
        var layerCount = worldState.getLayerCount();
        // Without repeatable aisles the first aisle cannot start anywhere else: aisle c sits at minZ + c.
        for (int c = 0, z = -centerOffset[4]; c < fingerLength; c++, z++) {
            layerCount.clear();
            for (int b = 0, y = -centerOffset[1]; b < thumbLength; b++, y++) {
                for (int a = 0, x = -centerOffset[0]; a < palmLength; a++, x++) {
                    TraceabilityPredicate predicate = blockMatches[c][b][a];
                    if (predicate.isAny()) continue;
                    worldState.setError(null);
                    BlockPos pos = setActualRelativeOffset(x, y, z, frontFacing, upwardsFacing, isFlipped)
                            .offset(centerPos.getX(), centerPos.getY(), centerPos.getZ());
                    if (!worldState.update(pos, predicate)) return false;
                    worldState.addPosCache(pos);
                    if (savePredicate) matchContext.getOrCreate("predicates", HashMap::new).put(pos, predicate);
                    boolean canPartShared = true;
                    if (worldState.getTileEntity() instanceof IMachineBlockEntity machineBlockEntity &&
                            machineBlockEntity.getMetaMachine() instanceof IMultiPart part) {
                        if (part.isFormed() && !part.canShared() && !part.hasController(worldState.controllerPos)) {
                            canPartShared = false;
                            worldState.setError(new PatternStringError("multiblocked.pattern.error.share"));
                        } else {
                            matchContext.getOrCreate("parts", HashSet::new).add(part);
                        }
                    }
                    if (worldState.getBlockState().getBlock() instanceof ActiveBlock) {
                        matchContext.getOrCreate("vaBlocks", LongOpenHashSet::new)
                                .add(worldState.getPos().asLong());
                    }
                    if (!predicate.test(worldState) || !canPartShared) {
                        if (!worldState.hasError()) worldState.setError(new PatternError());
                        return false;
                    }
                    matchContext.getOrCreate("ioMap", Long2ObjectOpenHashMap::new).put(worldState.getPos().asLong(),
                            worldState.io);
                }
            }
            for (var entry : layerCount.object2IntEntrySet()) {
                if (entry.getIntValue() < entry.getKey().minLayerCount) {
                    worldState.setError(new SinglePredicateError(entry.getKey(), 3));
                    return false;
                }
            }
            formedRepetitionCount[c] = 1;
        }
        for (var entry : globalCount.object2IntEntrySet()) {
            if (entry.getIntValue() < entry.getKey().minCount) {
                worldState.setError(new SinglePredicateError(entry.getKey(), 1));
                return false;
            }
        }
        worldState.setError(null);
        worldState.setNeededFlip(isFlipped);
        return true;
    }
}
