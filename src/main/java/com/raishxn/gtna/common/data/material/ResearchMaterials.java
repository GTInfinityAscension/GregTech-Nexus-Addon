package com.raishxn.gtna.common.data.material;

import com.gregtechceu.gtceu.api.data.chemical.material.Material;
import com.gregtechceu.gtceu.api.data.chemical.material.info.MaterialIconSet;

import com.raishxn.gtna.GTNACORE;

/**
 * GTOCore MFPC coolants of the Supercomputing Center (G-0249), copied from GTOCore {@code dc4824d}: the fresh and the
 * spent ("invalidation") Basic / Cascade MFPC, as ingots, nuggets and blocks.
 */
public final class ResearchMaterials {

    private ResearchMaterials() {}

    public static Material BasicMFPC;
    public static Material CascadeMFPC;
    public static Material InvalidationBasicMFPC;
    public static Material InvalidationCascadeMFPC;

    private static Material mfpc(String id, int color) {
        return new Material.Builder(GTNACORE.id(id)).polymer().color(color).iconSet(MaterialIconSet.DULL)
                .buildAndRegister();
    }

    public static void init() {
        BasicMFPC = mfpc("basic_mfpc", 0xC0C0C0);
        CascadeMFPC = mfpc("cascade_mfpc", 0x303030);
        InvalidationBasicMFPC = mfpc("invalidation_basic_mfpc", 0xC0C0C0);
        InvalidationCascadeMFPC = mfpc("invalidation_cascade_mfpc", 0x303030);
    }
}
