package com.raishxn.gtna.common.data.material;

import com.gregtechceu.gtceu.api.data.chemical.material.Material;
import com.gregtechceu.gtceu.api.data.chemical.material.info.MaterialIconSet;

import com.raishxn.gtna.GTNACORE;

import static com.gregtechceu.gtceu.api.data.chemical.material.info.MaterialFlags.DISABLE_DECOMPOSITION;
import static com.gregtechceu.gtceu.common.data.GTMaterials.Naquadah;
import static com.gregtechceu.gtceu.common.data.GTMaterials.NaquadahEnriched;

/**
 * Fuels of the naquadah reactor ladder (Large Naquadah Reactor, Naquadah HyperReactor), as GTOCore defines them
 * ({@code MaterialB}, commit {@code dc4824d}). GTNA ships a simple Large Chemical Reactor recipe for each; modpacks
 * replace them with their own chain.
 */
public final class NaquadahFuelMaterials {

    private NaquadahFuelMaterials() {}

    public static Material NaquadahFuel;
    public static Material EnrichedNaquadahFuel;

    public static void init() {
        NaquadahFuel = new Material.Builder(GTNACORE.id("naquadah_fuel")).langValue("Naquadah Fuel").fluid()
                .color(0x292929).components(Naquadah, 1).iconSet(MaterialIconSet.DULL)
                .flags(DISABLE_DECOMPOSITION).buildAndRegister();
        EnrichedNaquadahFuel = new Material.Builder(GTNACORE.id("enriched_naquadah_fuel"))
                .langValue("Enriched Naquadah Fuel").fluid().color(0x1f2a1f).components(NaquadahEnriched, 1)
                .iconSet(MaterialIconSet.DULL).flags(DISABLE_DECOMPOSITION).buildAndRegister();
    }
}
