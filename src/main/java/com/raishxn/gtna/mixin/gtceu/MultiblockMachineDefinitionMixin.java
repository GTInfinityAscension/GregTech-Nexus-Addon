package com.raishxn.gtna.mixin.gtceu;

import com.gregtechceu.gtceu.api.machine.MultiblockMachineDefinition;
import com.gregtechceu.gtceu.api.pattern.BlockPattern;
import com.gregtechceu.gtceu.api.pattern.MultiblockShapeInfo;

import com.raishxn.gtna.api.machine.multiblock.GTNASubPatterns;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Unique;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

import java.util.ArrayList;
import java.util.List;

/**
 * Adds each registered module (sub-pattern) as an extra page in the multiblock's JEI/XEI preview, so
 * the structure of an attachable module can be previewed next to the main multiblock.
 */
@Mixin(MultiblockMachineDefinition.class)
public abstract class MultiblockMachineDefinitionMixin {

    /**
     * GTCEu rebuilds every preview shape on each call (a full 3D walk of the pattern: 2.8 s for the Kinetic Orbital
     * Lance). Patterns do not change at runtime, so the result is kept per definition.
     */
    @Unique
    private volatile List<MultiblockShapeInfo> gtna$shapes;

    @Inject(method = "getMatchingShapes", at = @At("HEAD"), cancellable = true, remap = false)
    private void gtna$cachedShapes(CallbackInfoReturnable<List<MultiblockShapeInfo>> cir) {
        var cached = gtna$shapes;
        if (cached != null) cir.setReturnValue(cached);
    }

    @Inject(method = "getMatchingShapes", at = @At("RETURN"), cancellable = true, remap = false)
    private void gtna$appendModuleShapes(CallbackInfoReturnable<List<MultiblockShapeInfo>> cir) {
        MultiblockMachineDefinition self = (MultiblockMachineDefinition) (Object) this;
        List<BlockPattern> subPatterns = GTNASubPatterns.get(self);
        if (subPatterns.isEmpty()) {
            gtna$shapes = List.copyOf(cir.getReturnValue());
            cir.setReturnValue(gtna$shapes);
            return;
        }
        List<MultiblockShapeInfo> shapes = new ArrayList<>(cir.getReturnValue());
        for (BlockPattern sub : subPatterns) {
            if (sub == null) {
                continue;
            }
            int[] repetitions = new int[sub.aisleRepetitions.length];
            for (int i = 0; i < repetitions.length; i++) {
                repetitions[i] = sub.aisleRepetitions[i][0];
            }
            shapes.add(new MultiblockShapeInfo(sub.getPreview(repetitions)));
        }
        gtna$shapes = List.copyOf(shapes);
        cir.setReturnValue(gtna$shapes);
    }
}
