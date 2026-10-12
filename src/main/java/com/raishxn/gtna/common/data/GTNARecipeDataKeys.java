package com.raishxn.gtna.common.data;

/**
 * Recipe data keys consumed by GTNA machines. GTCEu 7.5.3 has no shared {@code GTRecipeDataKeys}
 * holder, so the ported GTOCore keys live here; the string value is what ends up in the saved
 * recipe data, so it must match the original.
 */
public final class GTNARecipeDataKeys {

    /**
     * GTOCore ISA Mill grinding-ball tier: {@code 1} = Soapstone ball, {@code 2} = Aluminium ball.
     * Compared against {@code BallHatchPartMachine.GRINDBALL}.
     */
    public static final String GRINDBALL = "grindball";

    /**
     * GTOCore minimum cleanroom filter of the Large Incubator: {@code 1} = cleanroom filter, {@code 2} = sterile
     * filter. GTO's third level (law cleanroom) has no GTCEu filter block.
     */
    public static final String FILTER_CASING = "filter_casing";

    /** GTOCore Space Elevator Power Module tier (1-5) an Assembler Module recipe needs. */
    public static final String POWER_MODULE_TIER = "power_module_tier";

    private GTNARecipeDataKeys() {}
}
