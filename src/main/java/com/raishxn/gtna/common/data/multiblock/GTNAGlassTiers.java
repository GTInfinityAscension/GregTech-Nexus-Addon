package com.raishxn.gtna.common.data.multiblock;

import com.gregtechceu.gtceu.api.GTValues;
import com.gregtechceu.gtceu.api.pattern.TraceabilityPredicate;
import com.gregtechceu.gtceu.api.pattern.error.PatternStringError;
import com.gregtechceu.gtceu.common.data.GTBlocks;

import com.lowdragmc.lowdraglib.utils.BlockInfo;

import net.minecraft.network.chat.Component;
import net.minecraft.world.level.block.Block;

import com.raishxn.gtna.common.data.GTNABlocks;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.function.Supplier;

/**
 * Tiered glass of GTOCore ({@code GTOPredicates.glass()}, {@code GTOBlocks.createTierGlassCasings}): every glass
 * block of a structure must be the same kind, and its voltage tier is kept in the match context under
 * {@link #KEY} so the machine can cap its tier with it.
 */
public final class GTNAGlassTiers {

    public static final String KEY = "gtna_glass_tier";

    private static Map<Supplier<? extends Block>, Integer> tiers;

    private GTNAGlassTiers() {}

    /** Glass block -> voltage tier, lowest first (the order JEI/EMI previews use). */
    public static Map<Supplier<? extends Block>, Integer> tiers() {
        if (tiers == null) {
            var map = new LinkedHashMap<Supplier<? extends Block>, Integer>();
            map.put(GTBlocks.CASING_TEMPERED_GLASS, GTValues.MV);
            map.put(GTNABlocks.BOROSILICATE_GLASS_BLOCK, GTValues.HV);
            map.put(GTNABlocks.TITANIUM_BOROSILICATE_GLASS, GTValues.EV);
            map.put(GTNABlocks.TUNGSTEN_BOROSILICATE_GLASS, GTValues.IV);
            map.put(GTNABlocks.HSSS_BOROSILICATE_GLASS, GTValues.LuV);
            map.put(GTNABlocks.NAQUADAH_BOROSILICATE_GLASS, GTValues.ZPM);
            map.put(GTNABlocks.TRITANIUM_BOROSILICATE_GLASS, GTValues.UV);
            map.put(GTNABlocks.AMPROSIUM_BOROSILICATE_GLASS, GTValues.UHV);
            map.put(GTNABlocks.ENDERIUM_BOROSILICATE_GLASS, GTValues.UEV);
            map.put(GTNABlocks.TARANIUM_BOROSILICATE_GLASS, GTValues.UIV);
            map.put(GTNABlocks.QUARKS_BOROSILICATE_GLASS, GTValues.UXV);
            map.put(GTNABlocks.DRACONIUM_BOROSILICATE_GLASS, GTValues.OpV);
            map.put(GTNABlocks.COSMIC_NEUTRONIUM_BOROSILICATE_GLASS, GTValues.MAX);
            tiers = map;
        }
        return tiers;
    }

    /** Any tiered glass; all glass blocks of one structure must match. */
    public static TraceabilityPredicate glass() {
        return new TraceabilityPredicate(state -> {
            var blockState = state.getBlockState();
            for (var entry : tiers().entrySet()) {
                if (blockState.is(entry.getKey().get())) {
                    Object current = state.getMatchContext().getOrPut(KEY, entry.getValue());
                    if (!current.equals(entry.getValue())) {
                        state.setError(new PatternStringError("gtna.multiblock.pattern.error.glass"));
                        return false;
                    }
                    return true;
                }
            }
            return false;
        }, () -> tiers().keySet().stream().map(s -> BlockInfo.fromBlockState(s.get().defaultBlockState()))
                .toArray(BlockInfo[]::new))
                .addTooltips(Component.translatable("gtna.multiblock.pattern.error.glass"));
    }
}
