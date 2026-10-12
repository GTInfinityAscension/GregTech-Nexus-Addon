package com.raishxn.gtna.common.data.material;

import com.gregtechceu.gtceu.api.GTValues;
import com.gregtechceu.gtceu.api.data.chemical.material.Material;
import com.gregtechceu.gtceu.api.data.chemical.material.info.MaterialIconSet;
import com.gregtechceu.gtceu.api.fluids.FluidBuilder;

import com.raishxn.gtna.GTNACORE;
import com.raishxn.gtna.api.data.info.GTNAMaterialFlags;
import com.raishxn.gtna.common.data.GTNAMaterials;

import static com.gregtechceu.gtceu.api.data.chemical.material.info.MaterialFlags.*;

/**
 * Materials of the GTNH Forge of Gods chain (GT5-Unofficial {@code MaterialsInit}, GT++ {@code MaterialsElements}/
 * {@code MaterialsAlloy}/{@code MaterialMisc}, GoodGenerator {@code GGMaterial}): names, colours and formulas as in
 * GTNH. They are registered first so recipes can be ported and tuned afterwards (see
 * {@code docs/roadmap/forge-of-gods-material-chain.md}).
 *
 * <p>
 * No blast temperature is set and dusts do not smelt, so GTCEu creates no EBF or furnace shortcut; each material's
 * acquisition comes from its own ported recipe. Forms derived from an ingot (plates, rods, gears...) are generated
 * normally. GTNH tiers are mapped to GTCEu as UMV → UXV.
 */
public final class GodforgeChainMaterials {

    public static Material Creon;
    /** GTNH Bedrockium (BEC condensate source; recipes are GTNA adaptations, see GTNABECRecipes). */
    public static Material Bedrockium;
    /** GoodGenerator Tairitsu (W8 Nq*7 Bedrockium4 C4 V3 + Black Plutonium → Plutonium-241). */
    public static Material Tairitsu;
    /** GTNH Inactive Cosmic Solder / Boundless Cosmic Solder (BEC condensate source). */
    public static Material InactiveCosmicSolder;
    public static Material BoundlessCosmicSolder;
    public static Material Mellion;
    public static Material TranscendentMetal;
    public static Material SixPhasedCopper;
    public static Material TengamPurified;
    public static Material TengamAttuned;
    public static Material Infinity;
    public static Material Eternity;
    public static Material Ichorium;
    public static Material Shijima;
    public static Material Churitsu;
    public static Material SuperconductorUIVBase;
    public static Material SuperconductorUMVBase;
    public static Material Hypogen;
    public static Material Rhugnor;
    public static Material CelestialTungsten;
    public static Material AstralTitanium;
    public static Material ChronomaticGlass;
    public static Material Nitinol60;
    public static Material AdvancedNitinol;
    public static Material Quantum;
    public static Material DragonMetal;
    public static Material MetastableOganesson;
    public static Material Shirabon;
    public static Material AtomicSeparationCatalyst;
    public static Material Dilithium;
    public static Material Orundum;
    public static Material MagnetoResonatic;
    public static Material TengamRaw;
    public static Material DTCC;
    public static Material DTPC;
    public static Material DTRC;
    public static Material DTEC;
    public static Material DTSC;
    public static Material ExcitedDTCC;
    public static Material ExcitedDTPC;
    public static Material ExcitedDTRC;
    public static Material ExcitedDTEC;
    public static Material ExcitedDTSC;
    public static Material PhononMedium;
    public static Material PhononCrystalSolution;
    public static Material MutatedLivingSolder;
    public static Material PrimordialMatter;
    public static Material StableBaryonicMatter;
    public static Material HeavyRadox;
    /** Superconductor wires: UIV and UMV (GTCEu UXV), lossless. */
    public static Material SuperconductorUIV;
    public static Material SuperconductorUMV;
    /** GTOCore space-era alloys used as frames by the Advanced Fusion Reactor extensions (GTO MaterialSpaceEra). */
    public static Material PlatinumManganeseAntimonyHeuslerAlloy;
    public static Material OdysseyNanoSuperalloy;
    /** GTNH Stellar Alloy (Nano Forge frames). */
    public static Material StellarAlloy;
    public static Material DimensionallyShiftedSuperfluid;
    public static Material Draconium;
    public static Material AwakenedDraconium;
    public static Material CosmicNeutronium;
    public static Material ExoHalkonite;
    public static Material ChaosMatter;
    public static Material Axonium;

    private GodforgeChainMaterials() {}

    /** Materials whose liquid uses its original GTNH/Modernity still texture (gtna:block/fluids/fluid.<id>). */
    private static final java.util.Set<String> CUSTOM_FLUIDS = java.util.Set.of("infinity", "eternity", "hypogen",
            "chronomatic_glass", "rhugnor", "dragon_metal", "primordial_matter", "phonon_crystal_solution",
            "phonon_medium", "stable_baryonic_matter");
    /** Liquids with no texture anywhere get their own colour instead of a white material tint. */
    private static final java.util.Map<String, Integer> FLUID_COLORS = java.util.Map.ofEntries(
            java.util.Map.entry("shijima", 0xc4d6f2),
            java.util.Map.entry("platinum_manganese_antimony_heusler_alloy", 0xb0bcc8),
            java.util.Map.entry("celestial_tungsten", 0x32384a),
            java.util.Map.entry("astral_titanium", 0xdca0f0),
            java.util.Map.entry("six_phased_copper", 0xff7814),
            java.util.Map.entry("shirabon", 0xc61361),
            java.util.Map.entry("quantum", 0x6ec8c8),
            java.util.Map.entry("metastable_oganesson", 0x14397f),
            java.util.Map.entry("creon", 0x460046),
            java.util.Map.entry("mellion", 0x3c0505),
            java.util.Map.entry("tengam_purified", 0xbadf70),
            java.util.Map.entry("tengam_attuned", 0xd5ff80),
            java.util.Map.entry("ichorium", 0xd37806),
            java.util.Map.entry("odyssey_nano_superalloy", 0x4c7a6a),
            java.util.Map.entry("draconium", 0x7a3099),
            java.util.Map.entry("awakened_draconium", 0xff7700),
            java.util.Map.entry("cosmic_neutronium", 0x000d1a),
            java.util.Map.entry("churitsu", 0x828282),
            java.util.Map.entry("advanced_nitinol", 0xd2b48c),
            java.util.Map.entry("nitinol_60", 0xc8c8c8),
            java.util.Map.entry("superconductor_uiv_base", 0xe558b1),
            java.util.Map.entry("superconductor_umv_base", 0xb526cd),
            java.util.Map.entry("atomic_separation_catalyst", 0xe85e0c),
            java.util.Map.entry("stellar_alloy", 0xc5ced8));

    private static FluidBuilder liquid(String id, int temperature) {
        var builder = new FluidBuilder().temperature(temperature);
        if (CUSTOM_FLUIDS.contains(id)) builder.customStill();
        Integer color = FLUID_COLORS.get(id);
        if (color != null) builder.color(color);
        return builder;
    }

    public static void init() {
        Creon = metal("creon", "Creon", 0xffffff, GodforgeIconSets.CREON, true, true).setFormula("⸎");
        Mellion = metal("mellion", "Mellion", 0xffffff, GodforgeIconSets.MELLION, false, true);
        TranscendentMetal = metal("transcendent_metal", "Transcendent Metal", 0xffffff,
                GodforgeIconSets.TRANSCENDENT_METAL, false, true).setFormula("TsЖ");
        SixPhasedCopper = metal("six_phased_copper", "Six-Phased Copper", 0xffffff,
                GodforgeIconSets.SIX_PHASED_COPPER, true, true).setFormula("✢");
        TengamPurified = metal("tengam_purified", "Purified Tengam", 0xffffff, GodforgeIconSets.TENGAM_PURIFIED,
                false, false).setFormula("M");
        TengamAttuned = metal("tengam_attuned", "Attuned Tengam", 0xffffff, GodforgeIconSets.TENGAM_ATTUNED, false,
                false).setFormula("M");
        Infinity = metal("infinity", "Infinity", 0xffffff, GodforgeIconSets.INFINITY, true, true).setFormula("If*");
        Eternity = metal("eternity", "Eternity", 0xffffff, GodforgeIconSets.ETERNITY, false, true).setFormula("En⦼");
        Ichorium = metal("ichorium", "Ichorium", 0xffffff, GodforgeIconSets.ICHORIUM, true, false).setFormula("IcMa");
        Shijima = metal("shijima", "Shijima", 0xffffff, GodforgeIconSets.SHIJIMA, false, false).setFormula("静寂");
        Churitsu = metal("churitsu", "Churitsu", 0xffffff, GodforgeIconSets.CHURITSU, false, false).setFormula("中立");
        SuperconductorUIVBase = metal("superconductor_uiv_base", "Superconductor Base UIV", 0xffffff,
                GodforgeIconSets.SUPERCONDUCTOR_UIV_BASE, false, false).setFormula("(C₁₄Os₁₁O₇Ag₃SpH₂O)₄?₁");
        SuperconductorUMVBase = metal("superconductor_umv_base", "Superconductor Base UMV", 0xffffff,
                GodforgeIconSets.SUPERCONDUCTOR_UMV_BASE, false, false);
        Hypogen = metal("hypogen", "Hypogen", 0xffffff, GodforgeIconSets.HYPOGEN, true, false).setFormula("Hy⚶");
        Rhugnor = metal("rhugnor", "Rhugnor", 0xffffff, GodforgeIconSets.RHUGNOR, true, false).setFormula("Fs⚶");
        CelestialTungsten = metal("celestial_tungsten", "Celestial Tungsten", 0xffffff,
                GodforgeIconSets.CELESTIAL_TUNGSTEN, true, false).setFormula("✦◆✦");
        AstralTitanium = metal("astral_titanium", "Astral Titanium", 0xffffff,
                GodforgeIconSets.ASTRAL_TITANIUM, true, false).setFormula("✧◇✧");
        ChronomaticGlass = metal("chronomatic_glass", "Chromatic Glass", 0xffffff, GodforgeIconSets.CHROMATIC_GLASS,
                false, false)
                .setFormula("⌘☯☯⌘");
        Nitinol60 = metal("nitinol_60", "Nitinol 60", 0xffffff, GodforgeIconSets.NITINOL_60, false, false)
                .setFormula("Ni4Ti6");
        AdvancedNitinol = metal("advanced_nitinol", "Advanced Nitinol", 0xffffff, GodforgeIconSets.ADVANCED_NITINOL,
                false, false)
                .setFormula("⚷⚙⚷ Ni4Ti6");
        Quantum = metal("quantum", "Quantum", 0xffffff, GodforgeIconSets.QUANTUM, false, false);
        DragonMetal = metal("dragon_metal", "Dragonblood", 0xffffff, GodforgeIconSets.DRAGON_METAL, true, false)
                .setFormula("۞");
        MetastableOganesson = metal("metastable_oganesson", "Metastable Oganesson", 0xffffff,
                GodforgeIconSets.METASTABLE_OGANESSON, false, false).setFormula("Og*");
        Shirabon = metal("shirabon", "Shirabon", 0xffffff, GodforgeIconSets.SHIRABON, false, false).setFormula("Sh⏧");
        AtomicSeparationCatalyst = metal("atomic_separation_catalyst", "Atomic Separation Catalyst", 0xffffff,
                GodforgeIconSets.ATOMIC_SEPARATION_CATALYST, false, false);
        Dilithium = gem("dilithium", "Dilithium", 0xfffafa, MaterialIconSet.DIAMOND, false).setFormula("∳Li∳Li∳");
        Orundum = gem("orundum", "Orundum", 0xcd2626, MaterialIconSet.DIAMOND, true).setFormula("Or");
        MagnetoResonatic = gem("magneto_resonatic", "Magneto Resonatic", 0xdd77ff, MaterialIconSet.MAGNETIC, false);
        TengamRaw = dust("tengam_raw", "Raw Tengam", 0xa0bf60, MaterialIconSet.ROUGH).setFormula("M");
        DTCC = fluid("dimensionally_transcendent_crude_catalyst", "Dimensionally Transcendent Crude Catalyst",
                0x0a1414);
        DTPC = fluid("dimensionally_transcendent_prosaic_catalyst", "Dimensionally Transcendent Prosaic Catalyst",
                0x0a1414);
        DTRC = fluid("dimensionally_transcendent_resplendent_catalyst",
                "Dimensionally Transcendent Resplendent Catalyst", 0x0a1414);
        DTEC = fluid("dimensionally_transcendent_exotic_catalyst", "Dimensionally Transcendent Exotic Catalyst",
                0x0a1414);
        DTSC = fluid("dimensionally_transcendent_stellar_catalyst", "Dimensionally Transcendent Stellar Catalyst",
                0x0a1414).setFormula("Stellar");
        ExcitedDTCC = fluid("excited_dtcc", "Excited Dimensionally Transcendent Crude Catalyst", 0x0a1414);
        ExcitedDTPC = fluid("excited_dtpc", "Excited Dimensionally Transcendent Prosaic Catalyst", 0x233b29);
        ExcitedDTRC = fluid("excited_dtrc", "Excited Dimensionally Transcendent Resplendent Catalyst", 0x261438);
        ExcitedDTEC = fluid("excited_dtec", "Excited Dimensionally Transcendent Exotic Catalyst", 0xf0f029);
        ExcitedDTSC = fluid("excited_dtsc", "Excited Dimensionally Transcendent Stellar Catalyst", 0x7e4b0b)
                .setFormula("[-Stellar-Stellar-]");
        PhononMedium = fluid("phonon_medium", "Lossless Phonon Transfer Medium", 0xffffff);
        PhononCrystalSolution = fluid("phonon_crystal_solution", "Saturated Phononic Crystal Solution", 0xffffff)
                .setFormula("〄");
        MutatedLivingSolder = fluid("mutated_living_solder", "Mutated Living Solder", 0x936d9b)
                .setFormula("?Sn?Bi?If?");
        PrimordialMatter = fluid("primordial_matter", "Liquid Primordial Matter", 0xffffff);
        StableBaryonicMatter = fluid("stable_baryonic_matter", "Stabilised Baryonic Matter", 0xffffff);
        HeavyRadox = fluid("heavy_radox", "Heavy Radox", 0x730073);
        SuperconductorUIV = superconductor("superconductor_uiv", "Superconductor UIV", 0xe558b1, GTValues.UIV);
        // GTO composes Odyssey with Trinium, Naquadria, Molybdenum and nano-scale yttria/alumina; GTNA keeps the three
        // metals GTCEu has. Both keep GTO's blast temperatures, so the EBF recipes come from the composition.
        PlatinumManganeseAntimonyHeuslerAlloy = alloy("platinum_manganese_antimony_heusler_alloy",
                "Platinum-Manganese-Antimony Heusler Alloy", 0xffffff,
                GodforgeIconSets.PLATINUM_MANGANESE_ANTIMONY_HEUSLER_ALLOY, 13_000,
                com.gregtechceu.gtceu.common.data.GTMaterials.Platinum, 1,
                com.gregtechceu.gtceu.common.data.GTMaterials.Manganese, 1,
                com.gregtechceu.gtceu.common.data.GTMaterials.Antimony, 1).setFormula("PtMnSb");
        OdysseyNanoSuperalloy = alloy("odyssey_nano_superalloy", "Odyssey Nano Superalloy", 0xffffff,
                GodforgeIconSets.ODYSSEY, 15_000,
                com.gregtechceu.gtceu.common.data.GTMaterials.Trinium, 14,
                com.gregtechceu.gtceu.common.data.GTMaterials.Naquadria, 8,
                com.gregtechceu.gtceu.common.data.GTMaterials.Molybdenum, 17);
        Draconium = GTNAMaterials.Draconium = metal("draconium", "Draconium", 0xffffff,
                GodforgeIconSets.DRACONIUM, false, false).setFormula("Dc");
        AwakenedDraconium = GTNAMaterials.AwakenedDraconium = metal("awakened_draconium", "Awakened Draconium",
                0xffffff, GodforgeIconSets.AWAKENED_DRACONIUM, true, true).setFormula("✵Dc✵");
        CosmicNeutronium = GTNAMaterials.CosmicNeutronium = metal("cosmic_neutronium", "Cosmic Neutronium",
                0xffffff, GodforgeIconSets.COSMIC_NEUTRONIUM, true, true).setFormula("SpNt");
        ExoHalkonite = GTNAMaterials.ExoHalkonite = metal("exo_halkonite", "Exo-Halkonite",
                0xffffff, GodforgeIconSets.EXO_HALKONITE, true, true).setFormula("Hk⚶");
        ChaosMatter = GTNAMaterials.ChaosMatter = metal("chaos_matter", "Chaos Matter",
                0xffffff, GodforgeIconSets.CHAOS_MATTER, true, true).setFormula("✦Ch✦");
        Axonium = GTNAMaterials.Axonium = metal("axonium", "Axonium",
                0xffffff, GodforgeIconSets.AXONIUM, true, true).setFormula("Ax⊛");
        DimensionallyShiftedSuperfluid = fluid("dimensionally_shifted_superfluid", "Dimensionally Shifted Superfluid",
                0x2a1d4f);
        StellarAlloy = metal("stellar_alloy", "Stellar Alloy", 0xffffff, GodforgeIconSets.STELLAR_ALLOY, false, false)
                .setFormula("✦Nt₄Nq₂Ke₂✦");
        SuperconductorUMV = superconductor("superconductor_umv", "Superconductor UMV", 0xb526cd, GTValues.UXV);
    }

    private static Material.Builder builder(String id, String lang, int color, MaterialIconSet icon) {
        return new Material.Builder(GTNACORE.id(id)).langValue(lang).color(color).iconSet(icon);
    }

    private static Material metal(String id, String lang, int color, MaterialIconSet icon, boolean plasma,
                                  boolean superdense) {
        var builder = builder(id, lang, color, icon).ingot().liquid(liquid(id, 10_000))
                .flags(GENERATE_PLATE, GENERATE_DENSE, GENERATE_ROD, GENERATE_LONG_ROD, GENERATE_GEAR,
                        GENERATE_SMALL_GEAR, GENERATE_BOLT_SCREW, GENERATE_FRAME, GENERATE_FINE_WIRE, GENERATE_FOIL,
                        GENERATE_RING, GENERATE_SPRING, NO_SMELTING, DISABLE_DECOMPOSITION);
        if (plasma) builder.plasma();
        if (superdense) builder.flags(GTNAMaterialFlags.GENERATE_SUPERDENSE);
        return builder.buildAndRegister();
    }

    private static Material gem(String id, String lang, int color, MaterialIconSet icon, boolean liquid) {
        var builder = builder(id, lang, color, icon).gem()
                .flags(GENERATE_PLATE, GENERATE_LENS, NO_SMELTING, DISABLE_DECOMPOSITION);
        if (liquid) builder.liquid(new FluidBuilder().temperature(3_000));
        return builder.buildAndRegister();
    }

    private static Material dust(String id, String lang, int color, MaterialIconSet icon) {
        return builder(id, lang, color, icon).dust().flags(DISABLE_DECOMPOSITION).buildAndRegister();
    }

    private static Material fluid(String id, String lang, int color) {
        return builder(id, lang, color, MaterialIconSet.FLUID).liquid(liquid(id, 300))
                .flags(DISABLE_DECOMPOSITION).buildAndRegister();
    }

    private static Material alloy(String id, String lang, int color, MaterialIconSet icon, int blast,
                                  Object... components) {
        return builder(id, lang, color, icon).ingot().liquid(liquid(id, blast))
                .components(components).blastTemp(blast)
                .flags(GENERATE_PLATE, GENERATE_FRAME, GENERATE_ROD, GENERATE_LONG_ROD, GENERATE_GEAR,
                        GENERATE_SMALL_GEAR, DISABLE_DECOMPOSITION)
                .buildAndRegister();
    }

    /** GTNH BEC materials GTNA did not have. */
    public static void initBEC() {
        Bedrockium = builder("bedrockium", "Bedrockium", 0x272727, MaterialIconSet.METALLIC).ingot()
                .liquid(liquid("bedrockium", 9_900)).blastTemp(9_900)
                .flags(GENERATE_PLATE, GENERATE_DENSE, GENERATE_ROD, GENERATE_FRAME, NO_SMELTING,
                        DISABLE_DECOMPOSITION, GTNAMaterialFlags.GENERATE_SUPERDENSE)
                .buildAndRegister();
        Tairitsu = builder("tairitsu", "Tairitsu", 0x363636, MaterialIconSet.SHINY).ingot()
                .liquid(liquid("tairitsu", 7_400)).blastTemp(7_400)
                .components(com.gregtechceu.gtceu.common.data.GTMaterials.Tungsten, 8,
                        com.gregtechceu.gtceu.common.data.GTMaterials.Naquadria, 7, Bedrockium, 4,
                        com.gregtechceu.gtceu.common.data.GTMaterials.Carbon, 4,
                        com.gregtechceu.gtceu.common.data.GTMaterials.Vanadium, 3,
                        com.gregtechceu.gtceu.common.data.GTMaterials.Plutonium241, 1)
                .flags(GENERATE_PLATE, GENERATE_DENSE, GENERATE_ROD, GENERATE_LONG_ROD, GENERATE_GEAR,
                        GENERATE_SMALL_GEAR, GENERATE_BOLT_SCREW, GENERATE_FRAME, GENERATE_FINE_WIRE, GENERATE_FOIL,
                        GENERATE_RING, GENERATE_ROTOR, GENERATE_ROUND, DISABLE_DECOMPOSITION)
                .buildAndRegister();
        InactiveCosmicSolder = fluid("inactive_cosmic_solder", "Inactive Cosmic Solder", 0x9a9aa8);
        BoundlessCosmicSolder = fluid("boundless_cosmic_solder", "Boundless Cosmic Solder", 0xfaf6ff)
                .setFormula("✧✦✧✦✧");
    }

    private static Material alloy(String id, String lang, int color, int blast, Object... components) {
        return alloy(id, lang, color, MaterialIconSet.METALLIC, blast, components);
    }

    private static Material superconductor(String id, String lang, int color, int tier) {
        return builder(id, lang, color, MaterialIconSet.SHINY).ingot().liquid(new FluidBuilder().temperature(1))
                .cableProperties(GTValues.V[tier], 4, 0, true)
                .flags(GENERATE_FINE_WIRE, NO_SMELTING, DISABLE_DECOMPOSITION).buildAndRegister();
    }
}
