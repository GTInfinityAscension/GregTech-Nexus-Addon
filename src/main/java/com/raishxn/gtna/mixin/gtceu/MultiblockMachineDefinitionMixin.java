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

import java.lang.ref.SoftReference;
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
    // EN: Soft reference: EMI builds the shapes of all ~250 multiblocks when it reloads, and keeping them all strongly
    // made a 1.5 GB client run out of memory. The JVM now drops them under memory pressure and they are rebuilt.
    // PT: Referência fraca (soft): o EMI monta as formas dos ~250 multiblocos ao recarregar, e guardar todas de forma
    // forte fazia um cliente de 1,5 GB ficar sem memória. Agora a JVM as descarta quando falta memória e elas são
    // refeitas.
    // ZH: 软引用：EMI 重新加载时会构建约 250 个多方块的全部形状，强引用全部保留会让 1.5 GB 的客户端内存溢出。
    // 现在内存紧张时 JVM 会释放它们，需要时再重建。
    @Unique
    private volatile SoftReference<List<MultiblockShapeInfo>> gtna$shapes;

    @Inject(method = "getMatchingShapes", at = @At("HEAD"), cancellable = true, remap = false)
    private void gtna$cachedShapes(CallbackInfoReturnable<List<MultiblockShapeInfo>> cir) {
        var ref = gtna$shapes;
        var cached = ref == null ? null : ref.get();
        if (cached != null) cir.setReturnValue(cached);
    }

    @Inject(method = "getMatchingShapes", at = @At("RETURN"), cancellable = true, remap = false)
    private void gtna$appendModuleShapes(CallbackInfoReturnable<List<MultiblockShapeInfo>> cir) {
        MultiblockMachineDefinition self = (MultiblockMachineDefinition) (Object) this;
        List<BlockPattern> subPatterns = GTNASubPatterns.get(self);
        if (subPatterns.isEmpty()) {
            var shapes = List.copyOf(cir.getReturnValue());
            gtna$shapes = new SoftReference<>(shapes);
            cir.setReturnValue(shapes);
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
        var result = List.copyOf(shapes);
        gtna$shapes = new SoftReference<>(result);
        cir.setReturnValue(result);
    }
}
