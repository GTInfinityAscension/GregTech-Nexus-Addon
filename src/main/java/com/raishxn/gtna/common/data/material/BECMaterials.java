package com.raishxn.gtna.common.data.material;

import com.gregtechceu.gtceu.api.data.chemical.material.Material;
import com.gregtechceu.gtceu.api.data.chemical.material.info.MaterialIconSet;
import com.gregtechceu.gtceu.api.fluids.FluidBuilder;

import com.raishxn.gtna.GTNACORE;
import com.raishxn.gtna.api.bec.CondensateType;

import java.util.Set;

import static com.gregtechceu.gtceu.api.data.chemical.material.info.MaterialFlags.DISABLE_DECOMPOSITION;

/**
 * GTNH {@code CondensateType.registerFluids}: one entangled Bose-Einstein condensate gas per type
 * ({@code gtna:entangled_<id>}). Types whose source fluid has its own texture reuse it
 * ({@code fluid.entangled_<id>.png}, copied from the source); the rest are tinted gas.
 */
public final class BECMaterials {

    private static final Set<String> TEXTURED = Set.of("chromaticglass", "hypogen", "infinity", "magmatter",
            "mhdcsm", "phononmedium", "quarkgluonplasma", "spacetime", "universium", "eternity");

    private static final java.util.Map<String, String> ENGLISH = java.util.Map.ofEntries(
            java.util.Map.entry("neutronium", "Neutronium"),
            java.util.Map.entry("cosmicneutronium", "Cosmic Neutronium"),
            java.util.Map.entry("bedrockium", "Bedrockium"), java.util.Map.entry("chromaticglass", "Chromatic Glass"),
            java.util.Map.entry("celestialtungsten", "Celestial Tungsten"), java.util.Map.entry("infinity", "Infinity"),
            java.util.Map.entry("hypogen", "Hypogen"), java.util.Map.entry("transcendentmetal", "Transcendent Metal"),
            java.util.Map.entry("dimshiftedsuperfluid", "Dim. Shifted Superfluid"),
            java.util.Map.entry("phononmedium", "Lossless Phonon Transfer Medium"),
            java.util.Map.entry("quarkgluonplasma", "Degenerate Quark Gluon Plasma"),
            java.util.Map.entry("spacetime", "SpaceTime"), java.util.Map.entry("time", "Tachyon Rich"),
            java.util.Map.entry("space", "Spatially Enlarged"), java.util.Map.entry("cosmicsolder", "Cosmic Solder"),
            java.util.Map.entry("mhdcsm", "MHDCSM"), java.util.Map.entry("magmatter", "MagMatter"),
            java.util.Map.entry("universium", "Universium"), java.util.Map.entry("eternity", "Eternity"));

    private BECMaterials() {}

    public static void init() {
        // Part forms the BEC recipes need (GTNH generates them for every metal).
        var forms = new com.gregtechceu.gtceu.api.data.chemical.material.info.MaterialFlag[] {
                com.gregtechceu.gtceu.api.data.chemical.material.info.MaterialFlags.GENERATE_PLATE,
                com.gregtechceu.gtceu.api.data.chemical.material.info.MaterialFlags.GENERATE_ROD,
                com.gregtechceu.gtceu.api.data.chemical.material.info.MaterialFlags.GENERATE_LONG_ROD,
                com.gregtechceu.gtceu.api.data.chemical.material.info.MaterialFlags.GENERATE_BOLT_SCREW,
                com.gregtechceu.gtceu.api.data.chemical.material.info.MaterialFlags.GENERATE_ROUND,
                com.gregtechceu.gtceu.api.data.chemical.material.info.MaterialFlags.GENERATE_RING,
                com.gregtechceu.gtceu.api.data.chemical.material.info.MaterialFlags.GENERATE_FOIL,
                com.gregtechceu.gtceu.api.data.chemical.material.info.MaterialFlags.GENERATE_FINE_WIRE,
                com.gregtechceu.gtceu.api.data.chemical.material.info.MaterialFlags.GENERATE_GEAR,
                com.gregtechceu.gtceu.api.data.chemical.material.info.MaterialFlags.GENERATE_SMALL_GEAR,
                com.gregtechceu.gtceu.api.data.chemical.material.info.MaterialFlags.GENERATE_ROTOR,
                com.gregtechceu.gtceu.api.data.chemical.material.info.MaterialFlags.GENERATE_FRAME,
                com.gregtechceu.gtceu.api.data.chemical.material.info.MaterialFlags.GENERATE_DENSE };
        for (Material m : new Material[] { GodforgeChainMaterials.Churitsu, GodforgeChainMaterials.Shijima,
                GodforgeChainMaterials.SixPhasedCopper, GodforgeChainMaterials.Hypogen,
                GodforgeChainMaterials.ExoHalkonite, GodforgeChainMaterials.TranscendentMetal,
                GodforgeChainMaterials.Eternity, GodforgeChainMaterials.Shirabon,
                com.raishxn.gtna.common.data.GTNAMaterials.Universium,
                com.raishxn.gtna.common.data.GTNAMaterials.SpaceTime,
                com.raishxn.gtna.common.data.GTNAMaterials.WhiteDwarfMatter,
                com.raishxn.gtna.common.data.GTNAMaterials.BlackDwarfMatter,
                com.raishxn.gtna.common.data.GTNAMaterials.MagnetohydrodynamicallyConstrainedStarMatter,
                com.raishxn.gtna.common.data.GTNAMaterials.MagMatter }) {
            m.addFlags(forms);
        }
        for (Material m : new Material[] { com.raishxn.gtna.common.data.GTNAMaterials.Universium,
                com.raishxn.gtna.common.data.GTNAMaterials.SpaceTime, GodforgeChainMaterials.Shirabon,
                com.raishxn.gtna.common.data.GTNAMaterials.CosmicNeutronium }) {
            m.addFlags(com.raishxn.gtna.api.data.info.GTNAMaterialFlags.GENERATE_SUPERDENSE);
        }
        for (CondensateType type : CondensateType.VALUES) {
            Material source = type.getSource();
            int color = source.getMaterialRGB() == 0xffffff ? 0xc8c8ff : source.getMaterialRGB();
            FluidBuilder gas = new FluidBuilder().temperature(1).color(color);
            if (TEXTURED.contains(type.id)) gas.customStill();
            type.entangled = new Material.Builder(GTNACORE.id("entangled_" + type.id))
                    .langValue("Entangled " + ENGLISH.get(type.id) + " Bose-Einstein Condensate")
                    .gas(gas)
                    .color(color).iconSet(MaterialIconSet.FLUID)
                    .flags(DISABLE_DECOMPOSITION)
                    .buildAndRegister();
        }
    }
}
