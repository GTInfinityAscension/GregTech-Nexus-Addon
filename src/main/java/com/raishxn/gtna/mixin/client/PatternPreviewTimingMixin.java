package com.raishxn.gtna.mixin.client;

import com.gregtechceu.gtceu.api.gui.widget.PatternPreviewWidget;
import com.gregtechceu.gtceu.api.machine.MultiblockMachineDefinition;

import net.minecraftforge.fml.loading.FMLEnvironment;

import com.raishxn.gtna.GTNACORE;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Unique;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/** Development only: logs every multiblock preview that takes long to build (JEI builds them all on world join). */
@Mixin(value = PatternPreviewWidget.class, remap = false)
public abstract class PatternPreviewTimingMixin {

    @Unique
    private static final ThreadLocal<Long> GTNA$START = new ThreadLocal<>();

    @Inject(method = "getPatternWidget", at = @At("HEAD"))
    private static void gtna$start(MultiblockMachineDefinition definition,
                                   CallbackInfoReturnable<PatternPreviewWidget> cir) {
        if (!FMLEnvironment.production) GTNA$START.set(System.nanoTime());
    }

    @Inject(method = "getPatternWidget", at = @At("RETURN"))
    private static void gtna$end(MultiblockMachineDefinition definition,
                                 CallbackInfoReturnable<PatternPreviewWidget> cir) {
        Long start = GTNA$START.get();
        if (start == null) return;
        long ms = (System.nanoTime() - start) / 1_000_000;
        if (ms >= 100) GTNACORE.LOGGER.info("[GTNA perf] preview widget {}: {} ms", definition.getId(), ms);
    }
}
