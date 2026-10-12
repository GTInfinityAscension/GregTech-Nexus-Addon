package com.raishxn.gtna.common.data;

import com.gregtechceu.gtceu.GTCEu;
import com.gregtechceu.gtceu.api.item.tool.GTToolType;

import net.minecraft.client.renderer.RenderType;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.tags.BlockTags;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.GlassBlock;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.material.MapColor;

import com.raishxn.gtna.GTNACORE;
import com.raishxn.gtna.common.block.GTNABlockItem;
import com.raishxn.gtna.common.block.MEStorageCoreBlock;
import com.raishxn.gtna.common.block.NexusCapacitorBlock;
import com.tterrag.registrate.util.entry.BlockEntry;
import com.tterrag.registrate.util.nullness.NonNullFunction;
import com.tterrag.registrate.util.nullness.NonNullSupplier;

import java.util.function.Supplier;

import static com.raishxn.gtna.api.registry.GTNARegistry.REGISTRATE;

public class GTNABlocks {

    static {
        REGISTRATE.creativeModeTab(() -> GTNACreativeModeTabs.BLOCKS);
    }

    public static final BlockEntry<Block> BREEL_PIPE_CASING = createCasingBlock("breel_pipe_casing");
    public static final BlockEntry<Block> HYPER_PRESSURE_BREEL_CASING = createCasingBlock(
            "hyper_pressure_breel_casing");
    public static final BlockEntry<Block> STEAM_COMPACT_PIPE_CASING = createCasingBlock("steam_compact_pipe_casing");
    public static final BlockEntry<Block> STEAM_ASSEMBLY_BLOCK = createCasingBlock(
            "steam_assembly_block",
            GTNACORE.id("block/steam_assembly_block"));
    public static final BlockEntry<Block> VIBRATION_SAFE_CASING = createCasingBlock("vibration_safe_casing");
    /**
     * GTNL {@code GTNLCasings.IndustrialSteamCasing} (metaCasing02:1). Shell of the bronze-tier
     * large steam multiblocks; texture from the Modernity-GTNH pack (same author as GTNL).
     */
    public static final BlockEntry<Block> INDUSTRIAL_STEAM_CASING = createCasingBlock("industrial_steam_casing");
    /**
     * GTNL {@code GTNLCasings.AdvancedIndustrialSteamCasing} (metaCasing02:2). Shell of the steel-tier
     * (high pressure) large steam multiblocks; texture from the Modernity-GTNH pack.
     */
    public static final BlockEntry<Block> ADVANCED_INDUSTRIAL_STEAM_CASING = createCasingBlock(
            "advanced_industrial_steam_casing");
    public static final BlockEntry<Block> BRONZE_REINFORCED_WOOD = createCasingBlock("bronze_reinforced_wood");
    public static final BlockEntry<Block> BRASS_REINFORCED_WOODEN_CASING = createCasingBlock(
            "brass_reinforced_wooden_casing",
            GTNACORE.id("block/casings/brass_reinforced_wooden_casing"));
    public static final BlockEntry<Block> ALUMINIUM_BRONZE_CASING = createCasingBlock(
            "aluminium_bronze_casing",
            GTNACORE.id("block/casings/aluminium_bronze_casing"));
    public static final BlockEntry<Block> STAINLESS_EVAPORATION_CASING = createCasingBlock(
            "stainless_evaporation_casing",
            GTNACORE.id("block/casings/stainless_evaporation_casing"));
    public static final BlockEntry<Block> MULTI_FUNCTIONAL_CASING = createCasingBlock("multi_functional_casing");
    /**
     * GTOCore Inconel-625 family (ISA Mill shell, gearbox and pipe). The textures keep GTOCore's
     * relative paths, so the pipe/gearbox live under {@code block/} and the casing under
     * {@code block/casings/}.
     */
    public static final BlockEntry<Block> INCONEL_625_CASING = createCasingBlock("inconel_625_casing",
            GTNACORE.id("block/casings/inconel_625_casing"));
    public static final BlockEntry<Block> INCONEL_625_GEARBOX = createCasingBlock("inconel_625_gearbox",
            GTNACORE.id("block/inconel_625_gearbox"));
    public static final BlockEntry<Block> INCONEL_625_PIPE = createCasingBlock("inconel_625_pipe",
            GTNACORE.id("block/inconel_625_pipe"));
    public static final BlockEntry<Block> BLAZE_CASING = createTwoLayerCasingBlock("blaze_casing");
    public static final BlockEntry<Block> COLD_ICE_CASING = createTwoLayerCasingBlock("cold_ice_casing");
    public static final BlockEntry<Block> COMPONENT_ASSEMBLY_CASING_LV = createCasingBlock(
            "component_assembly_casing_lv");
    public static final BlockEntry<Block> COMPONENT_ASSEMBLY_CASING_MV = createCasingBlock(
            "component_assembly_casing_mv");
    public static final BlockEntry<Block> COMPONENT_ASSEMBLY_CASING_HV = createCasingBlock(
            "component_assembly_casing_hv");
    public static final BlockEntry<Block> COMPONENT_ASSEMBLY_CASING_EV = createCasingBlock(
            "component_assembly_casing_ev");
    public static final BlockEntry<Block> COMPONENT_ASSEMBLY_CASING_IV = createCasingBlock(
            "component_assembly_casing_iv");
    /**
     * GTOCore {@code component_assembly_line_casing_luv} (CC BY-NC-SA 4.0): the LuV member of the
     * Component Assembler casing family, reached only with the large extension formed. The texture
     * keeps GTOCore's {@code component_assembly_line} sheet with the GTNA family name.
     */
    public static final BlockEntry<Block> COMPONENT_ASSEMBLY_CASING_LUV = createCasingBlock(
            "component_assembly_casing_luv");
    /**
     * GTOCore {@code component_assembly_line_casing_zpm} (CC BY-NC-SA 4.0): the ZPM member of the
     * Component Assembler casing family, reached only with the large extension formed.
     */
    public static final BlockEntry<Block> COMPONENT_ASSEMBLY_CASING_ZPM = createCasingBlock(
            "component_assembly_casing_zpm");
    /**
     * GTOCore {@code component_assembly_line_casing_uv} (CC BY-NC-SA 4.0): the UV member of the
     * Component Assembler casing family, the top of the GTNA extension port.
     */
    public static final BlockEntry<Block> COMPONENT_ASSEMBLY_CASING_UV = createCasingBlock(
            "component_assembly_casing_uv");
    public static final BlockEntry<Block> STEEL_REINFORCED_WOOD = createCasingBlock("steel_reinforced_wood");
    public static final BlockEntry<Block> IRON_REINFORCED_WOOD = createCasingBlock("iron_reinforced_wood");
    public static final BlockEntry<Block> SOLAR_BOILING_CELL = createSolarCasingBlock("solar_boiling_cell");
    public static final BlockEntry<Block> SOLAR_HEAT_COLLECTOR_PIPE_CASING = createSolarCasingBlock(
            "solar_heat_collector_pipe_casing");
    public static final BlockEntry<Block> STRONZE_WRAPPED_CASING = createCasingBlock("stronze_wrapped_casing"); // Usando
                                                                                                                // Bronze
                                                                                                                // como
                                                                                                                // base
                                                                                                                // material
    public static final BlockEntry<Block> HYDRAULIC_ASSEMBLER_CASING = createCasingBlock("hydraulic_assembler_casing");
    public static final BlockEntry<Block> BREEL_PLATED_CASING = createCasingBlock("breel_plated_casing");
    public static final BlockEntry<Block> BOROSILICATE_GLASS_BLOCK = createGlassCasingBlock(
            "borosilicate_glass", GTNACORE.id("block/casings/borosilicate_glass"), () -> RenderType::cutoutMipped);
    public static final BlockEntry<Block> OXIDATION_RESISTANT_HASTELLOY_N_MECHANICAL_CASING = createCasingBlock(
            "oxidation_resistant_hastelloy_n_mechanical_casing",
            GTNACORE.id("block/casings/oxidation_resistant_hastelloy_n_mechanical_casing"));
    public static final BlockEntry<Block> ZIRCONIA_CERAMIC_HIGH_STRENGTH_BENDING_RESISTANCE_MECHANICAL_BLOCK = createCasingBlock(
            "zirconia_ceramic_high_strength_bending_resistance_mechanical_block",
            GTNACORE.id("block/zirconia_ceramic_high_strength_bending_resistance_mechanical_block"));
    public static final BlockEntry<Block> HIGH_STRENGTH_CONCRETE = createCasingBlock(
            "high_strength_concrete",
            GTNACORE.id("block/casings/high_strength_concrete"));
    public static final BlockEntry<Block> COBALT_OXIDE_CERAMIC_STRONG_THERMALLY_CONDUCTIVE_MECHANICAL_BLOCK = createCasingBlock(
            "cobalt_oxide_ceramic_strong_thermally_conductive_mechanical_block",
            GTNACORE.id("block/casings/cobalt_oxide_ceramic_strong_thermally_conductive_mechanical_block"));
    public static final BlockEntry<Block> LITHIUM_OXIDE_CERAMIC_HEAT_RESISTANT_SHOCK_RESISTANT_MECHANICAL_CUBE = createCasingBlock(
            "lithium_oxide_ceramic_heat_resistant_shock_resistant_mechanical_cube",
            GTNACORE.id("block/casings/lithium_oxide_ceramic_heat_resistant_shock_resistant_mechanical_cube"));
    public static final BlockEntry<Block> NAQUADAH_BOROSILICATE_GLASS = createGlassCasingBlock(
            "naquadah_borosilicate_glass",
            GTNACORE.id("block/casings/naquadah_borosilicate_glass"),
            () -> RenderType::cutoutMipped);
    public static final BlockEntry<Block> MAGTECH_CASING = createCasingBlock(
            "magtech_casing",
            GTNACORE.id("block/casings/magtech_casing"));
    public static final BlockEntry<Block> UNIVERSAL_FACTORY_CASING = createCasingBlock(
            "universal_factory_casing",
            GTNACORE.id("block/casings/universal_factory_casing"));
    public static final BlockEntry<Block> ABS_BLACK_CASING = createCasingBlock(
            "abs_black_casing",
            GTNACORE.id("block/casings/abs_black_casing"));
    public static final BlockEntry<Block> ABS_BLUE_CASING = createCasingBlock(
            "abs_blue_casing",
            GTNACORE.id("block/casings/abs_blue_casing"));
    public static final BlockEntry<Block> ABS_BROWN_CASING = createCasingBlock(
            "abs_brown_casing",
            GTNACORE.id("block/casings/abs_brown_casing"));
    public static final BlockEntry<Block> ABS_GREEN_CASING = createCasingBlock(
            "abs_green_casing",
            GTNACORE.id("block/casings/abs_green_casing"));
    public static final BlockEntry<Block> ABS_GREY_CASING = createCasingBlock(
            "abs_grey_casing",
            GTNACORE.id("block/casings/abs_grey_casing"));
    public static final BlockEntry<Block> ABS_LIME_CASING = createCasingBlock(
            "abs_lime_casing",
            GTNACORE.id("block/casings/abs_lime_casing"));
    public static final BlockEntry<Block> ABS_ORANGE_CASING = createCasingBlock(
            "abs_orange_casing",
            GTNACORE.id("block/casings/abs_orange_casing"));
    public static final BlockEntry<Block> ABS_RED_CASING = createCasingBlock(
            "abs_red_casing",
            GTNACORE.id("block/casings/abs_red_casing"));
    public static final BlockEntry<Block> ABS_WHITE_CASING = createCasingBlock(
            "abs_white_casing",
            GTNACORE.id("block/casings/abs_white_casing"));
    public static final BlockEntry<Block> ABS_YELLOW_CASING = createCasingBlock(
            "abs_yellow_casing",
            GTNACORE.id("block/casings/abs_yellow_casing"));
    public static final BlockEntry<Block> ABS_CYAN_CASING = createCasingBlock(
            "abs_cyan_casing",
            GTNACORE.id("block/casings/abs_cyan_casing"));
    public static final BlockEntry<Block> ABS_MAGENTA_CASING = createCasingBlock(
            "abs_magenta_casing",
            GTNACORE.id("block/casings/abs_magenta_casing"));
    public static final BlockEntry<Block> ABS_PINK_CASING = createCasingBlock(
            "abs_pink_casing",
            GTNACORE.id("block/casings/abs_pink_casing"));
    public static final BlockEntry<Block> ABS_PURPLE_CASING = createCasingBlock(
            "abs_purple_casing",
            GTNACORE.id("block/casings/abs_purple_casing"));
    public static final BlockEntry<Block> ABS_LIGHT_BULL_CASING = createCasingBlock(
            "abs_light_bull_casing",
            GTNACORE.id("block/casings/abs_light_bull_casing"));
    public static final BlockEntry<Block> ABS_LIGHT_GREY_CASING = createCasingBlock(
            "abs_light_grey_casing",
            GTNACORE.id("block/casings/abs_light_grey_casing"));
    public static final BlockEntry<Block> RESTRAINT_DEVICE = createCasingBlock(
            "restraint_device",
            GTNACORE.id("block/restraint_device"));
    public static final BlockEntry<Block> PROCESS_MACHINE_CASING = createCasingBlock(
            "process_machine_casing",
            GTNACORE.id("block/casings/process_machine_casing"));
    public static final BlockEntry<Block> COMPRESSOR_CONTROLLER_CASING = createCasingBlock(
            "compressor_controller_casing",
            GTNACORE.id("block/casings/compressor_controller_casing"));
    public static final BlockEntry<Block> EXTREME_DENSITY_CASING = createCasingBlock(
            "extreme_density_casing",
            GTNACORE.id("block/extreme_density_casing"));
    public static final BlockEntry<Block> GRAVITON_FIELD_CONSTRAINT_CASING = createCasingBlock(
            "graviton_field_constraint_casing");
    public static final BlockEntry<Block> ANNIHILATE_CORE = createCasingBlock("annihilate_core",
            GTNACORE.id("block/annihilate_core"));
    public static final BlockEntry<Block> HYPER_MECHANICAL_CASING = createCasingBlock("hyper_mechanical_casing");
    public static final BlockEntry<Block> HOLLOW_CASING = createCasingBlock("hollow_casing",
            GTNACORE.id("block/hollow_casing"));
    /**
     * GTOCore {@code naquadah_alloy_casing} (CC BY-NC-SA 4.0). GTO reuses the
     * {@code hyper_mechanical_casing} sheet for this block (the earlier GTNA copy pointed at the
     * water-purification {@code naquadah_reinforced_plant_casing} sheet by mistake).
     */
    public static final BlockEntry<Block> NAQUADAH_ALLOY_CASING = createCasingBlock("naquadah_alloy_casing",
            GTNACORE.id("block/casings/hyper_mechanical_casing"));
    /** GTOCore {@code iridium_casing} (CC BY-NC-SA 4.0): the Component Assembly Line shell. */
    public static final BlockEntry<Block> IRIDIUM_CASING = createCasingBlock("iridium_casing");
    public static final BlockEntry<Block> DYSON_CONTROL_TOROID = createCasingBlock("dyson_control_toroid");
    public static final BlockEntry<Block> DYSON_CONTROL_CASING = createCasingBlock("dyson_control_casing");
    public static final BlockEntry<Block> DEGENERATE_RHENIUM_CONSTRAINED_CASING = createCasingBlock(
            "degenerate_rhenium_constrained_casing");
    public static final BlockEntry<Block> DYSON_RECEIVER_CASING = createCasingBlock("dyson_receiver_casing",
            GTNACORE.id("block/casings/cosmic_detection_receiver_material_ray_absorbing_array"));
    public static final BlockEntry<Block> RHENIUM_REINFORCED_ENERGY_GLASS = createGlassCasingBlock(
            "rhenium_reinforced_energy_glass",
            GTNACORE.id("block/casings/rhenium_reinforced_energy_glass"),
            () -> RenderType::cutoutMipped);
    public static final BlockEntry<Block> ANTIMATTER_CONTAINMENT_CASING = createGlassCasingBlock(
            "antimatter_containment_casing",
            GTNACORE.id("block/casings/antimatter_containment_casing"),
            () -> RenderType::cutoutMipped);
    public static final BlockEntry<Block> DIMENSIONALLY_TRANSCENDENT_CASING = createCasingBlock(
            "dimensionally_transcendent_casing");
    public static final BlockEntry<Block> DIMENSION_INJECTION_CASING = createCasingBlock(
            "dimension_injection_casing");
    /**
     * GTNH DTPF Dimensional Bridge Casing; GTO texture. New id: {@code dimensional_bridge_casing} is an EOH legacy
     * remap.
     */
    public static final BlockEntry<Block> PLASMA_FORGE_BRIDGE_CASING = createTwoLayerCasingBlock(
            "plasma_forge_bridge_casing");
    /** GTNH Radiant Naquadah Alloy Casing (Nano Forge), Modernity-GTNH texture. */
    public static final BlockEntry<Block> RADIANT_NAQUADAH_ALLOY_CASING = createCasingBlock(
            "radiant_naquadah_alloy_casing");
    /** GT++ Cosmic Fabric Manipulator, Force Field Glass and GoodGenerator Field Restriction Coil (T3). */
    public static final BlockEntry<Block> COSMIC_FABRIC_MANIPULATOR = createCasingBlock("cosmic_fabric_manipulator");
    public static final BlockEntry<Block> FORCE_FIELD_GLASS = createGlassCasingBlock("force_field_glass",
            GTNACORE.id("block/casings/force_field_glass"), () -> RenderType::cutoutMipped);
    public static final BlockEntry<Block> FIELD_RESTRICTION_COIL_T3 = createCasingBlock("field_restriction_coil_t3");
    /** Physical GTNH Eye of Harmony components, kept separate from the published legacy casings. */
    public static final BlockEntry<Block> EYE_OF_HARMONY_BOUNDARY_CASING = GTNAEyeOfHarmonyContent.BOUNDARY_CASING;

    /**
     * GTOCore {@code supercritical_turbine_casing} (CC BY-NC-SA 4.0): the wall of the non-mega
     * Supercritical Steam Turbine and of its SUPERCRITICAL module. The texture, its connected
     * texture sheet and the {@code .png.mcmeta} are copied from {@code gtocore} with the namespace
     * rewritten to {@code gtna}.
     */
    public static final BlockEntry<Block> SUPERCRITICAL_TURBINE_CASING = createCasingBlock(
            "supercritical_turbine_casing");

    /**
     * GTOCore {@code hastelloy_n_75_casing} (CC BY-NC-SA 4.0): the shell of the Industrial Flotation
     * Cell. The texture, its connected texture sheet and the {@code .png.mcmeta} are copied from
     * {@code gtocore} with the namespace rewritten to {@code gtna}.
     */
    public static final BlockEntry<Block> HASTELLOY_N_75_CASING = createCasingBlock(
            "hastelloy_n_75_casing");
    /**
     * GTOCore {@code hastelloy_n_75_gearbox} (CC BY-NC-SA 4.0): the flotation cell's central
     * gearbox. GTOCore keeps this texture under {@code block/}, not {@code block/casings/}.
     */
    public static final BlockEntry<Block> HASTELLOY_N_75_GEARBOX = createCasingBlock(
            "hastelloy_n_75_gearbox", GTNACORE.id("block/hastelloy_n_75_gearbox"));
    /** GTOCore {@code hastelloy_n_75_pipe} (CC BY-NC-SA 4.0): the cell's aeration pipe. */
    public static final BlockEntry<Block> HASTELLOY_N_75_PIPE = createCasingBlock(
            "hastelloy_n_75_pipe", GTNACORE.id("block/hastelloy_n_75_pipe"));
    /** GTOCore {@code flotation_cell} (CC BY-NC-SA 4.0): the flotation tank walls. */
    public static final BlockEntry<Block> FLOTATION_CELL = createCasingBlock(
            "flotation_cell", GTNACORE.id("block/flotation_cell"));
    /**
     * GTOCore {@code red_steel_casing} (CC BY-NC-SA 4.0): the Vacuum Drying Furnace shell. The
     * texture, its connected texture sheet and the {@code .png.mcmeta} are copied from
     * {@code gtocore} with the namespace rewritten to {@code gtna}.
     */
    public static final BlockEntry<Block> RED_STEEL_CASING = createCasingBlock(
            "red_steel_casing");

    /**
     * GTOCore {@code three_proof_computer_casing} (CC BY-NC-SA 4.0): the computer wall of the
     * Component Assembler's large extension. Texture, connected sheet and {@code .png.mcmeta} copied
     * from {@code gtocore} with the namespace rewritten to {@code gtna}.
     */
    public static final BlockEntry<Block> THREE_PROOF_COMPUTER_CASING = createCasingBlock(
            "three_proof_computer_casing");
    /**
     * GTOCore {@code machining_control_casing_mk2} (CC BY-NC-SA 4.0): the sided machining-control
     * wall of the Component Assembler's large extension. Sided base sheet, connected sheet,
     * {@code .png.mcmeta} and the emissive {@code side_bloom} overlay copied from {@code gtocore}
     * with the namespace rewritten to {@code gtna}; rendered with GTCEu's
     * {@code cube_2_layer/bottom_top} model.
     */
    public static final BlockEntry<Block> MACHINING_CONTROL_CASING_MK2 = createSidedCasingBlock(
            "machining_control_casing_mk2");
    /**
     * GTOCore {@code energy_control_casing_mk2} (CC BY-NC-SA 4.0): the sided energy-control wall of
     * the Component Assembler's large extension. Same two-layer treatment as the machining casing.
     */
    public static final BlockEntry<Block> ENERGY_CONTROL_CASING_MK2 = createSidedCasingBlock(
            "energy_control_casing_mk2");
    /**
     * GTOCore {@code electric_power_transmission_casing} (CC BY-NC-SA 4.0): the power line wall of
     * the Component Assembler's large extension.
     */
    public static final BlockEntry<Block> ELECTRIC_POWER_TRANSMISSION_CASING = createCasingBlock(
            "electric_power_transmission_casing");
    /**
     * GTOCore {@code titanium_nitride_ceramic_impact_resistant_mechanical_block} (CC BY-NC-SA 4.0):
     * the impact-resistant ceramic wall of the Component Assembler extension. GTOCore keeps this
     * texture under {@code block/}, not {@code block/casings/}; the GTNA copy lives with the casings.
     */
    public static final BlockEntry<Block> TITANIUM_NITRIDE_CERAMIC_IMPACT_RESISTANT_MECHANICAL_BLOCK = createCasingBlock(
            "titanium_nitride_ceramic_impact_resistant_mechanical_block");
    /** GTOCore Component Assembly Line casings (CC BY-NC-SA 4.0). */
    public static final BlockEntry<Block> MOLECULAR_CASING = createTwoLayerCasingBlock("molecular_casing");
    public static final BlockEntry<Block> BORON_CARBIDE_CERAMIC_RADIATION_RESISTANT_MECHANICAL_CUBE = createCasingBlock(
            "boron_carbide_ceramic_radiation_resistant_mechanical_cube");
    public static final BlockEntry<Block> PRECISION_PROCESSING_MECHANICAL_CASING = createCasingBlock(
            "precision_processing_mechanical_casing");
    public static final BlockEntry<Block> ADVANCED_ASSEMBLY_LINE_UNIT = createCasingBlock(
            "advanced_assembly_line_unit");
    public static final BlockEntry<Block> CHEMICAL_CORROSION_RESISTANT_PIPE_CASING = createCasingBlock(
            "chemical_corrosion_resistant_pipe_casing");
    public static final BlockEntry<Block> MACHINE_CASING_CIRCUIT_ASSEMBLY_LINE = createCasingBlock(
            "machine_casing_circuit_assembly_line");
    public static final BlockEntry<Block> SPACETIME_ASSEMBLY_LINE_UNIT = createCasingBlock(
            "spacetime_assembly_line_unit");
    public static final BlockEntry<Block> PRESSURE_CONTAINMENT_CASING = createCasingBlock(
            "pressure_containment_casing");
    /**
     * GTOCore {@code component_assembly_line_casing_lv..uv} (CC BY-NC-SA 4.0): the tier casing
     * family of the {@code component_assembly_line}. GTNA ports LV..UV; the UHV..MAX tiers stay
     * documented as out of scope. Textures keep GTOCore's
     * {@code block/casings/component_assembly_line/} path.
     */
    public static final BlockEntry<Block> COMPONENT_ASSEMBLY_LINE_CASING_LV = createCasingBlock(
            "component_assembly_line_casing_lv",
            GTNACORE.id("block/casings/component_assembly_line/component_assembly_line_casing_lv"));
    public static final BlockEntry<Block> COMPONENT_ASSEMBLY_LINE_CASING_MV = createCasingBlock(
            "component_assembly_line_casing_mv",
            GTNACORE.id("block/casings/component_assembly_line/component_assembly_line_casing_mv"));
    public static final BlockEntry<Block> COMPONENT_ASSEMBLY_LINE_CASING_HV = createCasingBlock(
            "component_assembly_line_casing_hv",
            GTNACORE.id("block/casings/component_assembly_line/component_assembly_line_casing_hv"));
    public static final BlockEntry<Block> COMPONENT_ASSEMBLY_LINE_CASING_EV = createCasingBlock(
            "component_assembly_line_casing_ev",
            GTNACORE.id("block/casings/component_assembly_line/component_assembly_line_casing_ev"));
    public static final BlockEntry<Block> COMPONENT_ASSEMBLY_LINE_CASING_IV = createCasingBlock(
            "component_assembly_line_casing_iv",
            GTNACORE.id("block/casings/component_assembly_line/component_assembly_line_casing_iv"));
    public static final BlockEntry<Block> COMPONENT_ASSEMBLY_LINE_CASING_LUV = createCasingBlock(
            "component_assembly_line_casing_luv",
            GTNACORE.id("block/casings/component_assembly_line/component_assembly_line_casing_luv"));
    public static final BlockEntry<Block> COMPONENT_ASSEMBLY_LINE_CASING_ZPM = createCasingBlock(
            "component_assembly_line_casing_zpm",
            GTNACORE.id("block/casings/component_assembly_line/component_assembly_line_casing_zpm"));
    public static final BlockEntry<Block> COMPONENT_ASSEMBLY_LINE_CASING_UV = createCasingBlock(
            "component_assembly_line_casing_uv",
            GTNACORE.id("block/casings/component_assembly_line/component_assembly_line_casing_uv"));

    public static final BlockEntry<MEStorageCoreBlock> T1_ME_STORAGE_CORE = createMEStorageCore(1, false);
    public static final BlockEntry<MEStorageCoreBlock> T2_ME_STORAGE_CORE = createMEStorageCore(2, false);
    public static final BlockEntry<MEStorageCoreBlock> T3_ME_STORAGE_CORE = createMEStorageCore(3, false);
    public static final BlockEntry<MEStorageCoreBlock> T4_ME_STORAGE_CORE = createMEStorageCore(4, false);
    public static final BlockEntry<MEStorageCoreBlock> T5_ME_STORAGE_CORE = createMEStorageCore(5, false);
    public static final BlockEntry<MEStorageCoreBlock> T1_CRAFTING_STORAGE_CORE = createMEStorageCore(1, true);
    public static final BlockEntry<MEStorageCoreBlock> T2_CRAFTING_STORAGE_CORE = createMEStorageCore(2, true);
    public static final BlockEntry<MEStorageCoreBlock> T3_CRAFTING_STORAGE_CORE = createMEStorageCore(3, true);
    public static final BlockEntry<MEStorageCoreBlock> T4_CRAFTING_STORAGE_CORE = createMEStorageCore(4, true);
    public static final BlockEntry<MEStorageCoreBlock> T5_CRAFTING_STORAGE_CORE = createMEStorageCore(5, true);

    public static final BlockEntry<NexusCapacitorBlock> NEXUS_CAPACITOR_LV = createCapacitorBlock("nexus_capacitor_lv",
            1, 160_000L);
    public static final BlockEntry<NexusCapacitorBlock> NEXUS_CAPACITOR_MV = createCapacitorBlock("nexus_capacitor_mv",
            2, 1_500_000L);
    public static final BlockEntry<NexusCapacitorBlock> NEXUS_CAPACITOR_HV = createCapacitorBlock("nexus_capacitor_hv",
            3, 10_000_000L);
    public static final BlockEntry<NexusCapacitorBlock> NEXUS_CAPACITOR_EV = createCapacitorBlock("nexus_capacitor_ev",
            4, 50_000_000L);
    public static final BlockEntry<NexusCapacitorBlock> NEXUS_CAPACITOR_IV = createCapacitorBlock("nexus_capacitor_iv",
            5, 250_000_000L);
    public static final BlockEntry<NexusCapacitorBlock> NEXUS_CAPACITOR_LUV = createCapacitorBlock(
            "nexus_capacitor_luv", 6, 1_500_000_000L);
    public static final BlockEntry<NexusCapacitorBlock> NEXUS_CAPACITOR_ZPM = createCapacitorBlock(
            "nexus_capacitor_zpm", 7, 15_000_000_000L);
    public static final BlockEntry<NexusCapacitorBlock> NEXUS_CAPACITOR_UV = createCapacitorBlock("nexus_capacitor_uv",
            8, 150_000_000_000L);
    public static final BlockEntry<NexusCapacitorBlock> NEXUS_CAPACITOR_UHV = createCapacitorBlock(
            "nexus_capacitor_uhv", 9, 3_000_000_000_000L);
    public static final BlockEntry<NexusCapacitorBlock> NEXUS_CAPACITOR_UEV = createCapacitorBlock(
            "nexus_capacitor_uev", 10, 50_000_000_000_000L);
    public static final BlockEntry<NexusCapacitorBlock> NEXUS_CAPACITOR_UIV = createCapacitorBlock(
            "nexus_capacitor_uiv", 11, 900_000_000_000_000L);
    public static final BlockEntry<NexusCapacitorBlock> NEXUS_CAPACITOR_UXV = createCapacitorBlock(
            "nexus_capacitor_uxv", 12, 15_000_000_000_000_000L);
    public static final BlockEntry<NexusCapacitorBlock> NEXUS_CAPACITOR_OPV = createCapacitorBlock(
            "nexus_capacitor_opv", 13, 250_000_000_000_000_000L);
    public static final BlockEntry<NexusCapacitorBlock> NEXUS_CAPACITOR_MAX = createCapacitorBlock(
            "nexus_capacitor_max", 14, 5_000_000_000_000_000_000L);

    // GTOCore blocks of the Advanced Fusion Reactor and its four extensions (G-0191, CC BY-NC-SA 4.0 textures).
    public static final BlockEntry<Block> ACCELERATED_PIPELINE = createCasingBlock("accelerated_pipeline");
    public static final BlockEntry<Block> ACCELERATOR_MAGNETIC_CONSTRAINED_RAIL_CASING = createTwoLayerCasingBlock(
            "accelerator_magnetic_constrained_rail_casing");
    public static final BlockEntry<Block> ACCELERATOR_OBSERVATION_GLASS = createGlassCasingBlock(
            "accelerator_observation_glass", GTNACORE.id("block/casings/accelerator_observation_glass"),
            () -> RenderType::translucent);
    public static final BlockEntry<Block> ACCELERATOR_PROTECTION_CASING = createCasingBlock(
            "accelerator_protection_casing");
    public static final BlockEntry<Block> ADVANCED_COMPRESSED_FUSION_COIL = createCasingBlock(
            "advanced_compressed_fusion_coil");
    public static final BlockEntry<Block> AMPROSIUM_PIPE_CASING = createCasingBlock("amprosium_pipe_casing");
    public static final BlockEntry<Block> ANTIFREEZE_HEATPROOF_MACHINE_CASING = createCasingBlock(
            "antifreeze_heatproof_machine_casing");
    public static final BlockEntry<Block> COMPRESSED_FUSION_COIL = createCasingBlock("compressed_fusion_coil");
    public static final BlockEntry<Block> COMPRESSED_FUSION_COIL_MK2 = createCasingBlock("compressed_fusion_coil_mk2");
    public static final BlockEntry<Block> COMPRESSED_FUSION_COIL_MK2_PROTOTYPE = createCasingBlock(
            "compressed_fusion_coil_mk2_prototype");
    public static final BlockEntry<Block> CONTAINMENT_FIELD_GENERATOR = createCasingBlock(
            "containment_field_generator");
    public static final BlockEntry<Block> COOLANT_PIPE_CASING = createCasingBlock("coolant_pip_casing");
    public static final BlockEntry<Block> ELECTRON_PERMEABLE_AMPROSIUM_COATED_GLASS = createGlassCasingBlock(
            "electron_permeable_amprosium_coated_glass",
            GTNACORE.id("block/casings/electron_permeable_amprosium_coated_glass"), () -> RenderType::translucent);
    public static final BlockEntry<Block> FISSION_REACTOR_CASING = createCasingBlock("fission_reactor_casing");
    public static final BlockEntry<Block> FUSION_CASING_MK4 = createCasingBlock("fusion_casing_mk4");
    public static final BlockEntry<Block> FUSION_CASING_MK5 = createCasingBlock("fusion_casing_mk5");
    public static final BlockEntry<Block> HERMETIC_CASING_UEV = createHermeticCasingBlock("uev_hermetic_casing", "uev");
    public static final BlockEntry<Block> HIGH_PRESSURE_GAS_STORAGE_TANKS_CASING = createCasingBlock(
            "high_pressure_gas_storage_tanks_casing");
    public static final BlockEntry<Block> HIGH_PRESSURE_PIPE_CASING = createCasingBlock("high_pressure_pipe_casing");
    public static final BlockEntry<Block> HIGH_STRENGTH_SUPPORT_MECHANICAL_CASING = createCasingBlock(
            "high_strength_support_mechanical_casing");
    public static final BlockEntry<Block> IMPROVED_SUPERCONDUCTOR_COIL = createCasingBlock(
            "improved_superconductor_coil");
    public static final BlockEntry<Block> LASER_CASING = createGlassCasingBlock("laser_casing",
            GTNACORE.id("block/casings/laser_casing"), () -> RenderType::translucent);
    public static final BlockEntry<Block> MACHINING_CONTROL_CASING_MK3 = createSidedCasingBlock(
            "machining_control_casing_mk3");
    public static final BlockEntry<Block> MAGNESIUM_OXIDE_CERAMIC_HIGH_TEMPERATURE_INSULATION_MECHANICAL_BLOCK = createCasingBlock(
            "magnesium_oxide_ceramic_high_temperature_insulation_mechanical_block");
    public static final BlockEntry<Block> MOLECULAR_COIL = createColumnCasingBlock("molecular_coil");
    public static final BlockEntry<Block> NAQUADAH_REINFORCED_PLANT_CASING = createCasingBlock(
            "naquadah_reinforced_plant_casing");
    public static final BlockEntry<Block> NEUTRONIUM_STABLE_CASING = createCasingBlock("neutronium_stable_casing");
    public static final BlockEntry<Block> OPTICAL_RESONANCE_CHAMBER = createTwoLayerCasingBlock(
            "optical_resonance_chamber");
    public static final BlockEntry<Block> PBI_RADIATION_RESISTANT_MECHANICAL_ENCLOSURE = createCasingBlock(
            "pbi_radiation_resistant_mechanical_enclosure");
    public static final BlockEntry<Block> PLASMA_FIELD_GLASS = createGlassCasingBlock("plasma_field_glass",
            GTNACORE.id("block/casings/plasma_field_glass"), () -> RenderType::translucent);
    public static final BlockEntry<Block> RADIATION_ABSORBENT_CASING = createCasingBlock("radiation_absorbent_casing");
    public static final BlockEntry<Block> STRENGTHEN_THE_BASE_BLOCK = createCasingBlock("strengthen_the_base_block");
    public static final BlockEntry<Block> STRONTIUM_CARBONATE_CERAMIC_RAY_ABSORBING_MECHANICAL_CUBE = createCasingBlock(
            "strontium_carbonate_ceramic_ray_absorbing_mechanical_cube");
    public static final BlockEntry<Block> VACUUM_CHAMBER_BEAM_BLOCK = createCasingBlock("vacuum_chamber_beam_block");
    // GTOCore blocks of the Cracker Hub and the Giant Flotation Tank (CC BY-NC-SA 4.0, original textures).
    public static final BlockEntry<Block> OIL_GAS_TRANSPORTATION_PIPE_CASING = createCasingBlock(
            "oil_gas_transportation_pipe_casing");
    public static final BlockEntry<Block> CALCIUM_OXIDE_CERAMIC_ANTI_METAL_CORROSION_MECHANICAL_BLOCK = createCasingBlock(
            "calcium_oxide_ceramic_anti_metal_corrosion_mechanical_block");
    public static final BlockEntry<Block> STABILIZED_NAQUADAH_WATER_PLANT_CASING = createBottomTopCasingBlock(
            "stabilized_naquadah_water_plant_casing");
    // GTOCore Amprosium (= Neutronium) blocks of the Phase Change Cube and the Engraving Laser Plant.
    public static final BlockEntry<Block> AMPROSIUM_ACTIVE_CASING = createCasingBlock("amprosium_active_casing");
    public static final BlockEntry<Block> AMPROSIUM_GEARBOX = createCasingBlock("amprosium_gearbox");
    // GTOCore shared casings of ROADMAP §4 (G-0207).
    public static final BlockEntry<Block> HIGH_PRESSURE_RESISTANT_CASING = createCasingBlock(
            "high_pressure_resistant_casing");
    public static final BlockEntry<Block> MC_NYLON_TENSILE_MECHANICAL_SHELL = createCasingBlock(
            "mc_nylon_tensile_mechanical_shell");
    public static final BlockEntry<Block> LAFIUM_MECHANICAL_CASING = createCasingBlock("lafium_mechanical_casing");
    public static final BlockEntry<Block> AMPROSIUM_BOROSILICATE_GLASS = createGlassCasingBlock(
            "amprosium_borosilicate_glass", GTNACORE.id("block/casings/amprosium_borosilicate_glass"),
            () -> RenderType::cutoutMipped);
    // GTOCore blocks of G-0209.
    public static final BlockEntry<Block> TRANSCENDENTALLY_AMPLIFIED_MAGNETIC_CONFINEMENT_CASING = createCasingBlock(
            "transcendentally_amplified_magnetic_confinement_casing");
    public static final BlockEntry<Block> SPEEDING_PIPE = createColumnCasingBlock("speeding_pipe");
    // GTOCore shared blocks of G-0210. GTO's Hyper Core is an active block; GTNA keeps its glowing two-layer look.
    public static final BlockEntry<Block> HYPER_CORE = createTwoLayerCasingBlock("hyper_core");
    public static final BlockEntry<Block> PIKYONIUM_MACHINE_CASING = createCasingBlock("pikyonium_machine_casing");
    public static final BlockEntry<Block> HIGH_STRENGTH_SUPPORT_SPINDLE = createCasingBlock(
            "high_strength_support_spindle");
    public static final BlockEntry<Block> QUANTUM_GLASS = createGlassCasingBlock("quantum_glass",
            GTNACORE.id("block/casings/quantum_glass"), () -> RenderType::cutoutMipped);
    // G-0243: GTO blocks for the High Energy Laser Lathe and the Extreme Compressor.
    public static final BlockEntry<Block> IRIDIUM_PIPE_CASING = createCasingBlock("iridium_pipe_casing");
    public static final BlockEntry<Block> IRIDIUM_GEARBOX = createCasingBlock("iridium_gearbox");
    public static final BlockEntry<Block> LASER_COOLING_CASING = createCasingBlock("laser_cooling_casing");
    public static final BlockEntry<Block> HIGH_ENERGY_LASER_EMITTER = createCasingBlock("high_energy_laser_emitter");
    // G-0244: GTO blocks for the Hyperdimensional Plasma Fusion Core, Gemini Containment System and Giant
    // Electrochemical Workstation.
    public static final BlockEntry<Block> SPS_CASING = createCasingBlock("sps_casing");
    public static final BlockEntry<Block> SPACE_ELEVATOR_MECHANICAL_CASING = createCasingBlock(
            "space_elevator_mechanical_casing");
    public static final BlockEntry<Block> ENGINEERING_MECHANICAL_CASING = createCasingBlock(
            "engineering_mechanical_casing");
    public static final BlockEntry<Block> PEEK_WEAR_RESISTANT_MECHANICAL_HOUSING = createCasingBlock(
            "peek_wear_resistant_mechanical_housing");
    public static final BlockEntry<Block> INDUSTRIAL_FRAMELESS_GLASS = createGlassCasingBlock(
            "industrial_frameless_glass", GTNACORE.id("block/casings/industrial_frameless_glass"),
            () -> RenderType::cutoutMipped);
    // G-0245: GTO blocks for the Desulfurizer, Star Ultimate Material Forge and Heavy Rolling.
    public static final BlockEntry<Block> SMELTING_CONTROL_CASING = createCasingBlock("smelting_control_casing");
    public static final BlockEntry<Block> STABLE_BASE_CASING = createCasingBlock("stable_base_casing");
    public static final BlockEntry<Block> INSULATION_TILE_MECHANICAL_BLOCK = createCasingBlock(
            "insulation_tile_mechanical_block");
    public static final BlockEntry<Block> HSSS_BOROSILICATE_GLASS = createGlassCasingBlock("hsss_borosilicate_glass",
            GTNACORE.id("block/casings/hsss_borosilicate_glass"), () -> RenderType::cutoutMipped);
    /** GTO tier-3 Stellar Containment Casing; GTO texture {@code stellar_containment_casing}. */
    public static final BlockEntry<Block> ULTIMATE_STELLAR_CONTAINMENT_CASING = createCasingBlock(
            "ultimate_stellar_containment_casing");
    /** GTO Amprosium Casing; GTO texture {@code neutronium_casing}. */
    public static final BlockEntry<Block> AMPROSIUM_CASING = createCasingBlock("amprosium_casing");
    // G-0246: GTO blocks for the PCB Factory.
    public static final BlockEntry<Block> GRAVITY_STABILIZATION_CASING = createCasingBlock(
            "gravity_stabilization_casing");
    public static final BlockEntry<Block> PPS_CORROSION_RESISTANT_MECHANICAL_HOUSING = createCasingBlock(
            "pps_corrosion_resistant_mechanical_housing");
    public static final BlockEntry<Block> PLASMA_HEATER_CASING = createCasingBlock("plasma_heater_casing");
    public static final BlockEntry<Block> HIGH_ENERGY_ULTRAVIOLET_EMITTER_CASING = createCasingBlock(
            "high_energy_ultraviolet_emitter_casing");
    // G-0247: GTO blocks for the Hyper Reactors.
    public static final BlockEntry<Block> ENHANCE_HYPER_MECHANICAL_CASING = createCasingBlock(
            "enhance_hyper_mechanical_casing");
    public static final BlockEntry<Block> ECHO_CASING = createCasingBlock("echo_casing");
    // G-0248: GTO block of the Fuel Cell Generator.
    public static final BlockEntry<Block> FLOCCULATION_CASING = createCasingBlock("flocculation_casing");
    // G-0249: GTO computer casings (Supercomputing Center tiers) and tier glasses. The GTO active state of the
    // biocomputer casing and vents is not ported (static base texture).
    public static final BlockEntry<Block> BIOCOMPUTER_CASING = createCasingBlock("biocomputer_casing",
            GTNACORE.id("block/casings/about_computer/biocomputer_shell"));
    public static final BlockEntry<Block> PHASE_CHANGE_BIOCOMPUTER_COOLING_VENTS = createCasingBlock(
            "phase_change_biocomputer_cooling_vents",
            GTNACORE.id("block/casings/about_computer/phase_change_biocomputer_cooling_vents"));
    public static final BlockEntry<Block> GRAVITON_COMPUTER_CASING = createCasingBlock("graviton_computer_casing",
            GTNACORE.id("block/casings/about_computer/graviton_computer_casing"));
    public static final BlockEntry<Block> ANTI_ENTROPY_COMPUTER_CONDENSATION_MATRIX = createCasingBlock(
            "anti_entropy_computer_condensation_matrix",
            GTNACORE.id("block/casings/about_computer/anti_entropy_computer_condensation_matrix"));
    public static final BlockEntry<Block> TUNGSTEN_BOROSILICATE_GLASS = createGlassCasingBlock(
            "tungsten_borosilicate_glass", GTNACORE.id("block/casings/tungsten_borosilicate_glass"),
            () -> RenderType::cutoutMipped);
    // GTO tiered borosilicate glasses (GTOBlocks.createTierGlassCasings); the tiers live in GTNAGlassTiers.
    // GTNH Nano Forge tier 4 (BlockCasings13 metas 5-9, Advanced Iridium, Nanite Shielding Glass); Modernity-GTNH art.
    public static final BlockEntry<Block> PRECISION_FIELD_SYNC_CASING = createCasingBlock(
            "precision_field_sync_casing", GTNACORE.id("block/casings/nano_forge/precision_field_sync_casing"));
    public static final BlockEntry<Block> MAGNETIC_ANCHOR_CASING = createCasingBlock("magnetic_anchor_casing",
            GTNACORE.id("block/casings/nano_forge/magnetic_anchor_casing"));
    public static final BlockEntry<Block> FIELD_ENERGY_ABSORBER_CASING = createCasingBlock(
            "field_energy_absorber_casing", GTNACORE.id("block/casings/nano_forge/field_energy_absorber_casing"));
    public static final BlockEntry<Block> LOADBEARING_DISTRIBUTION_CASING = createCasingBlock(
            "loadbearing_distribution_casing", GTNACORE.id("block/casings/nano_forge/loadbearing_distribution_casing"));
    public static final BlockEntry<Block> NANITE_FRAMEWORK = createCasingBlock("nanite_framework",
            GTNACORE.id("block/casings/nano_forge/nanite_framework"));
    public static final BlockEntry<Block> ADVANCED_IRIDIUM_CASING = createCasingBlock("advanced_iridium_casing",
            GTNACORE.id("block/casings/nano_forge/advanced_iridium_casing"));
    public static final BlockEntry<Block> NANITE_SHIELDING_GLASS = createGlassCasingBlock("nanite_shielding_glass",
            GTNACORE.id("block/casings/nano_forge/nanite_shielding_glass"), () -> RenderType::cutoutMipped);

    // GTNH BEC casings (BlockCasingsBEC metas 0-6 and the Electromagnetic Waveguide glass), GT5U art.
    public static final BlockEntry<Block> COHERENCE_PRESERVING_PLASMA_CONDUIT = createCasingBlock(
            "coherence_preserving_plasma_conduit",
            GTNACORE.id("block/casings/bec/coherence_preserving_plasma_conduit"));
    public static final BlockEntry<Block> ELECTROMAGNETICALLY_ISOLATED_CASING = createCasingBlock(
            "electromagnetically_isolated_casing",
            GTNACORE.id("block/casings/bec/electromagnetically_isolated_casing"));
    public static final BlockEntry<Block> FINE_STRUCTURE_CONSTANT_MANIPULATOR = createCasingBlock(
            "fine_structure_constant_manipulator",
            GTNACORE.id("block/casings/bec/fine_structure_constant_manipulator"));
    public static final BlockEntry<Block> CONFLICT_INDUCEMENT_CASING = createCasingBlock("conflict_inducement_casing",
            GTNACORE.id("block/casings/bec/conflict_inducement_casing"));
    public static final BlockEntry<Block> PEACE_ENFORCEMENT_CASING = createCasingBlock("peace_enforcement_casing",
            GTNACORE.id("block/casings/bec/peace_enforcement_casing"));
    public static final BlockEntry<Block> CONDENSATE_TRANSFORMATIVE_COIL = createCasingBlock(
            "condensate_transformative_coil", GTNACORE.id("block/casings/bec/condensate_transformative_coil"));
    public static final BlockEntry<Block> CONDENSATE_GUIDANCE_COIL = createCasingBlock("condensate_guidance_coil",
            GTNACORE.id("block/casings/bec/condensate_guidance_coil"));
    public static final BlockEntry<Block> ELECTROMAGNETIC_WAVEGUIDE = createGlassCasingBlock(
            "electromagnetic_waveguide",
            GTNACORE.id("block/casings/bec/electromagnetic_waveguide"), () -> RenderType::cutoutMipped);

    // GTO blocks of the Dyson Sphere and the Space Elevator.
    public static final BlockEntry<Block> SPACE_ELEVATOR_INTERNAL_SUPPORT = createPlainSidedCasingBlock(
            "space_elevator_internal_support");
    public static final BlockEntry<Block> DYSON_DEPLOYMENT_MAGNET = createPlainSidedCasingBlock(
            "dyson_deployment_magnet");
    public static final BlockEntry<Block> DYSON_DEPLOYMENT_CORE = createCasingBlock("dyson_deployment_core",
            GTNACORE.id("block/casings/dyson_deployment_core"));
    public static final BlockEntry<Block> DYSON_DEPLOYMENT_CASING = createCasingBlock("dyson_deployment_casing",
            GTNACORE.id("block/casings/dyson_deployment_casing"));
    public static final BlockEntry<com.gregtechceu.gtceu.api.block.ActiveBlock> SPACE_ELEVATOR_SUPPORT = createActiveCasing(
            "space_elevator_support", "block/variant/space_elevator_support");
    public static final BlockEntry<Block> SPACE_ELEVATOR_MODULE_BASE = createPlainSidedCasingBlock(
            "space_elevator_module_base");
    public static final BlockEntry<Block> MODULE_CONNECTOR = createCasingBlock("module_connector",
            GTNACORE.id("block/module_connector"));
    public static final BlockEntry<com.gregtechceu.gtceu.api.block.ActiveBlock> SPACE_ELEVATOR_POWER_CORE = createActiveCasing(
            "space_elevator_power_core", "block/variant/space_elevator_power_core");
    /** GTO Space Elevator Power Modules MK I-V; their tier is {@link #spaceElevatorPowerModuleTier}. */
    public static final java.util.List<BlockEntry<com.gregtechceu.gtceu.api.block.ActiveBlock>> SPACE_ELEVATOR_POWER_MODULES = java.util.stream.IntStream
            .rangeClosed(1, 5)
            .mapToObj(tier -> createActiveCasing("space_elevator_power_module_" + tier,
                    "block/variant/space_elevator_power_module_" + tier))
            .toList();

    /** MK tier (1-5) of a Space Elevator Power Module block, or 0. */
    public static int spaceElevatorPowerModuleTier(Block block) {
        for (int i = 0; i < SPACE_ELEVATOR_POWER_MODULES.size(); i++) {
            if (SPACE_ELEVATOR_POWER_MODULES.get(i).get() == block) return i + 1;
        }
        return 0;
    }

    // GTO blocks of the Kerr-Newman Homogenizer.
    public static final BlockEntry<Block> SHIELDED_ACCELERATOR = createCasingBlock("shielded_accelerator",
            GTNACORE.id("block/shielded_accelerator"));
    public static final BlockEntry<Block> BIOACTIVE_MECHANICAL_CASING = createCasingBlock(
            "bioactive_mechanical_casing", GTNACORE.id("block/casings/bioactive_mechanical_casing"));
    public static final BlockEntry<com.gregtechceu.gtceu.api.block.ActiveBlock> ADVANCED_FUSION_COIL = createActiveCasing(
            "advanced_fusion_coil", "block/variant/advanced_fusion_coil");
    public static final BlockEntry<com.gregtechceu.gtceu.api.block.ActiveBlock> ACCELERATOR_ELECTROMAGNETIC_COIL_CONSTRAINT_CASING_UHV = createActiveCasing(
            "accelerator_electromagnetic_coil_constraint_casing_uhv",
            "block/casings/accelerator/accelerator_electromagnetic_coil_constraint_casing_uhv");
    // GTO blocks of Nyarlathotep's Tentacle. The Uruium coil is a plain casing here (GTNA has no GTO coil types).
    public static final BlockEntry<Block> URUIUM_COIL_BLOCK = createCasingBlock("uruium_coil_block",
            GTNACORE.id("block/coil/uruium_coil_block"));
    public static final BlockEntry<Block> SPACETIME_ASSEMBLY_LINE_CASING = createCasingBlock(
            "spacetime_assembly_line_casing", GTNACORE.id("block/spacetime_assembly_line_casing"));
    public static final BlockEntry<Block> QUARK_PIPE = createCasingBlock("quark_pipe", GTNACORE.id("block/quark_pipe"));
    public static final BlockEntry<Block> TARANIUM_BOROSILICATE_GLASS = createGlassCasingBlock(
            "taranium_borosilicate_glass", GTNACORE.id("block/casings/taranium_borosilicate_glass"),
            () -> RenderType::cutoutMipped);
    public static final BlockEntry<Block> TITANIUM_BOROSILICATE_GLASS = createGlassCasingBlock(
            "titanium_borosilicate_glass", GTNACORE.id("block/casings/titanium_borosilicate_glass"),
            () -> RenderType::cutoutMipped);
    public static final BlockEntry<Block> TRITANIUM_BOROSILICATE_GLASS = createGlassCasingBlock(
            "tritanium_borosilicate_glass", GTNACORE.id("block/casings/tritanium_borosilicate_glass"),
            () -> RenderType::cutoutMipped);
    public static final BlockEntry<Block> ENDERIUM_BOROSILICATE_GLASS = createGlassCasingBlock(
            "enderium_borosilicate_glass", GTNACORE.id("block/casings/enderium_borosilicate_glass"),
            () -> RenderType::cutoutMipped);
    public static final BlockEntry<Block> QUARKS_BOROSILICATE_GLASS = createGlassCasingBlock(
            "quarks_borosilicate_glass", GTNACORE.id("block/casings/quarks_borosilicate_glass"),
            () -> RenderType::cutoutMipped);
    public static final BlockEntry<Block> DRACONIUM_BOROSILICATE_GLASS = createGlassCasingBlock(
            "draconium_borosilicate_glass", GTNACORE.id("block/casings/draconium_borosilicate_glass"),
            () -> RenderType::cutoutMipped);
    public static final BlockEntry<Block> COSMIC_NEUTRONIUM_BOROSILICATE_GLASS = createGlassCasingBlock(
            "cosmic_neutronium_borosilicate_glass", GTNACORE.id("block/casings/cosmic_neutronium_borosilicate_glass"),
            () -> RenderType::cutoutMipped);

    public static BlockEntry<Block> createCasingBlock(String name) {
        return createCasingBlock(name, Block::new, GTNACORE.id("block/casings/" + name), () -> Blocks.IRON_BLOCK,
                () -> RenderType::solid);
    }

    public static BlockEntry<Block> createCasingBlock(String name, ResourceLocation texture) {
        return createCasingBlock(name, Block::new, texture, () -> Blocks.IRON_BLOCK, () -> RenderType::solid);
    }

    /**
     * A GTOCore-style sided control casing: one texture for the top face and one for the sides, under
     * {@code block/casings/sided/<name>/}. GTNA's {@link #createCasingBlock} only emits cube-all
     * models, so this helper reproduces the sided blockstate with the same tags and item-model
     * conventions.
     */
    /**
     * GTOCore two-layer (bloom) casing: the base texture plus the emissive {@code _bloom} overlay,
     * both connected through their {@code .png.mcmeta} (CC BY-NC-SA 4.0 from GTOCore). GTCEu's
     * {@code cube_2_layer/all} parent renders the pair, exactly like the original.
     */
    public static BlockEntry<Block> createTwoLayerCasingBlock(String name) {
        ResourceLocation base = GTNACORE.id("block/casings/" + name);
        ResourceLocation bloom = GTNACORE.id("block/casings/" + name + "_bloom");
        return REGISTRATE.block(name, Block::new)
                .initialProperties(() -> Blocks.IRON_BLOCK)
                .properties(p -> p
                        .mapColor(MapColor.METAL)
                        .strength(5.0f, 6.0f)
                        .sound(SoundType.METAL)
                        .requiresCorrectToolForDrops()
                        .isValidSpawn((state, level, pos, ent) -> false))
                .addLayer(() -> RenderType::cutoutMipped)
                .blockstate((ctx, prov) -> prov.simpleBlock(ctx.get(),
                        prov.models().withExistingParent(ctx.getName(), GTCEu.id("block/cube_2_layer/all"))
                                .texture("bot_all", base)
                                .texture("top_all", bloom)))
                .tag(GTToolType.WRENCH.harvestTags.get(0), BlockTags.MINEABLE_WITH_PICKAXE)
                .item(GTNABlockItem::new)
                .model((ctx, prov) -> prov.withExistingParent(ctx.getName(), prov.modLoc("block/" + ctx.getName())))
                .build()
                .register();
    }

    public static BlockEntry<Block> createSidedCasingBlock(String name) {
        ResourceLocation side = GTNACORE.id("block/casings/sided/" + name + "/side");
        ResourceLocation top = GTNACORE.id("block/casings/sided/" + name + "/top");
        ResourceLocation bloom = GTNACORE.id("block/casings/sided/" + name + "/side_bloom");
        return REGISTRATE.block(name, Block::new)
                .initialProperties(() -> Blocks.IRON_BLOCK)
                .properties(p -> p
                        .mapColor(MapColor.METAL)
                        .strength(5.0f, 6.0f)
                        .sound(SoundType.METAL)
                        .requiresCorrectToolForDrops()
                        .isValidSpawn((state, level, pos, ent) -> false))
                .addLayer(() -> RenderType::cutoutMipped)
                .blockstate((ctx, prov) -> prov.simpleBlock(ctx.get(),
                        prov.models().withExistingParent(ctx.getName(), GTCEu.id("block/cube_2_layer/bottom_top"))
                                .texture("bot_side", side)
                                .texture("bot_top", top)
                                .texture("bot_bottom", top)
                                .texture("top_side", bloom)
                                .texture("top_top", top)
                                .texture("top_bottom", top)))
                .tag(GTToolType.WRENCH.harvestTags.get(0), BlockTags.MINEABLE_WITH_PICKAXE)
                .item(GTNABlockItem::new)
                .model((ctx, prov) -> prov.withExistingParent(ctx.getName(), prov.modLoc("block/" + ctx.getName())))
                .build()
                .register();
    }

    @SuppressWarnings("all")
    public static BlockEntry<Block> createCasingBlock(String name,
                                                      NonNullFunction<BlockBehaviour.Properties, Block> blockSupplier,
                                                      ResourceLocation texture,
                                                      NonNullSupplier<? extends Block> properties,
                                                      Supplier<Supplier<RenderType>> type) {
        return REGISTRATE.block(name, blockSupplier)
                .initialProperties(properties)
                .properties(p -> p
                        .mapColor(MapColor.METAL)
                        .strength(5.0f, 6.0f)
                        .sound(SoundType.METAL)
                        .requiresCorrectToolForDrops()
                        .isValidSpawn((state, level, pos, ent) -> false))
                .addLayer(type)
                .blockstate((ctx, prov) -> prov.simpleBlock(ctx.get(), prov.models().cubeAll(ctx.getName(), texture)))
                .tag(GTToolType.WRENCH.harvestTags.get(0), BlockTags.MINEABLE_WITH_PICKAXE)
                .item(GTNABlockItem::new)
                .model((ctx, prov) -> {
                    if ("borosilicate_glass".equals(ctx.getName())) {
                        prov.withExistingParent(ctx.getName(), new ResourceLocation("minecraft", "block/cube_all"))
                                .texture("all", prov.modLoc("block/casings/borosilicate_glass_inventory"));
                    } else {
                        prov.withExistingParent(ctx.getName(), prov.modLoc("block/" + ctx.getName()));
                    }
                })
                .build()
                .register();
    }

    /** GTOCore cube-column casing: {@code block/casings/<name>/side} and {@code /top}. */
    public static BlockEntry<Block> createColumnCasingBlock(String name) {
        return REGISTRATE.block(name, Block::new)
                .initialProperties(() -> Blocks.IRON_BLOCK)
                .properties(p -> p.mapColor(MapColor.METAL).strength(5.0f, 6.0f).sound(SoundType.METAL)
                        .requiresCorrectToolForDrops().isValidSpawn((state, level, pos, ent) -> false))
                .addLayer(() -> RenderType::solid)
                .blockstate((ctx, prov) -> prov.simpleBlock(ctx.get(), prov.models().cubeColumn(ctx.getName(),
                        GTNACORE.id("block/casings/" + name + "/side"), GTNACORE.id("block/casings/" + name + "/top"))))
                .tag(GTToolType.WRENCH.harvestTags.get(0), BlockTags.MINEABLE_WITH_PICKAXE)
                .item(GTNABlockItem::new)
                .model((ctx, prov) -> prov.withExistingParent(ctx.getName(), prov.modLoc("block/" + ctx.getName())))
                .build()
                .register();
    }

    /** GTOCore cube-bottom-top casing: {@code block/casings/<name>} on the sides, {@code <name>_top} on both caps. */
    public static BlockEntry<Block> createBottomTopCasingBlock(String name) {
        return REGISTRATE.block(name, Block::new)
                .initialProperties(() -> Blocks.IRON_BLOCK)
                .properties(p -> p.mapColor(MapColor.METAL).strength(5.0f, 6.0f).sound(SoundType.METAL)
                        .requiresCorrectToolForDrops().isValidSpawn((state, level, pos, ent) -> false))
                .addLayer(() -> RenderType::solid)
                .blockstate((ctx, prov) -> prov.simpleBlock(ctx.get(), prov.models().cubeBottomTop(ctx.getName(),
                        GTNACORE.id("block/casings/" + name), GTNACORE.id("block/casings/" + name + "_top"),
                        GTNACORE.id("block/casings/" + name + "_top"))))
                .tag(GTToolType.WRENCH.harvestTags.get(0), BlockTags.MINEABLE_WITH_PICKAXE)
                .item(GTNABlockItem::new)
                .model((ctx, prov) -> prov.withExistingParent(ctx.getName(), prov.modLoc("block/" + ctx.getName())))
                .build()
                .register();
    }

    /** GTOCore hermetic casing above UHV: GTCEu's hermetic model over the tier's voltage casing. */
    public static BlockEntry<Block> createHermeticCasingBlock(String name, String tier) {
        return REGISTRATE.block(name, Block::new)
                .initialProperties(() -> Blocks.IRON_BLOCK)
                .properties(p -> p.mapColor(MapColor.METAL).strength(5.0f, 6.0f).sound(SoundType.METAL)
                        .requiresCorrectToolForDrops().isValidSpawn((state, level, pos, ent) -> false))
                .addLayer(() -> RenderType::cutoutMipped)
                .blockstate((ctx, prov) -> prov.simpleBlock(ctx.get(),
                        prov.models().withExistingParent(ctx.getName(), GTCEu.id("block/hermetic_casing"))
                                .texture("bot_bottom", GTCEu.id("block/casings/voltage/" + tier + "/bottom"))
                                .texture("bot_side", GTCEu.id("block/casings/voltage/" + tier + "/side"))
                                .texture("bot_top", GTCEu.id("block/casings/voltage/" + tier + "/top"))
                                .texture("top_side",
                                        GTCEu.id("block/casings/hermetic_casing/hermetic_casing_overlay"))))
                .tag(GTToolType.WRENCH.harvestTags.get(0), BlockTags.MINEABLE_WITH_PICKAXE)
                .item(GTNABlockItem::new)
                .model((ctx, prov) -> prov.withExistingParent(ctx.getName(), prov.modLoc("block/" + ctx.getName())))
                .build()
                .register();
    }

    private static BlockEntry<Block> createSolarCasingBlock(String name) {
        return REGISTRATE.block(name, Block::new)
                .initialProperties(() -> Blocks.IRON_BLOCK)
                .properties(p -> p.mapColor(MapColor.METAL).strength(5.0f, 6.0f).sound(SoundType.METAL)
                        .requiresCorrectToolForDrops())
                .addLayer(() -> RenderType::solid)
                .blockstate((ctx, prov) -> {
                    prov.simpleBlock(ctx.get(), prov.models().cube(ctx.getName(),
                            prov.modLoc("block/casings/" + name), // down
                            prov.modLoc("block/overlay/block/solar_boiling_cell_top_overlay"), // up
                            prov.modLoc("block/casings/" + name), // north
                            prov.modLoc("block/casings/" + name), // south
                            prov.modLoc("block/casings/" + name), // east
                            prov.modLoc("block/casings/" + name)  // west
                    ).texture("particle", prov.modLoc("block/casings/" + name)));
                })
                .tag(GTToolType.WRENCH.harvestTags.get(0), BlockTags.MINEABLE_WITH_PICKAXE)
                .item(GTNABlockItem::new)

                .build()
                .register();
    }

    /** Plain sided casing ({@code block/casings/<name>/side|top}, no bloom layer), like GTO's sided casings. */
    private static BlockEntry<Block> createPlainSidedCasingBlock(String name) {
        ResourceLocation side = GTNACORE.id("block/casings/" + name + "/side");
        ResourceLocation top = GTNACORE.id("block/casings/" + name + "/top");
        return REGISTRATE.block(name, Block::new)
                .initialProperties(() -> Blocks.IRON_BLOCK)
                .properties(p -> p.mapColor(MapColor.METAL).strength(5.0f, 6.0f).sound(SoundType.METAL)
                        .requiresCorrectToolForDrops().isValidSpawn((state, level, pos, ent) -> false))
                .addLayer(() -> RenderType::cutoutMipped)
                .blockstate((ctx, prov) -> prov.simpleBlock(ctx.get(),
                        prov.models().cubeBottomTop(ctx.getName(), side, top, top)))
                .tag(GTToolType.WRENCH.harvestTags.get(0), BlockTags.MINEABLE_WITH_PICKAXE)
                .item(GTNABlockItem::new)
                .model((ctx, prov) -> prov.withExistingParent(ctx.getName(), prov.modLoc("block/" + ctx.getName())))
                .build()
                .register();
    }

    /** GTCEu {@code GTBlocks.createActiveCasing}: models {@code <path>.json} and {@code <path>_active.json}. */
    private static BlockEntry<com.gregtechceu.gtceu.api.block.ActiveBlock> createActiveCasing(String name,
                                                                                              String modelPath) {
        return REGISTRATE.block(name, com.gregtechceu.gtceu.api.block.ActiveBlock::new)
                .initialProperties(() -> Blocks.IRON_BLOCK)
                .addLayer(() -> RenderType::cutoutMipped)
                .blockstate(com.gregtechceu.gtceu.common.data.models.GTModels
                        .createActiveModel(GTNACORE.id(modelPath)))
                .tag(com.gregtechceu.gtceu.data.recipe.CustomTags.MINEABLE_WITH_CONFIG_VALID_PICKAXE_WRENCH)
                .item(net.minecraft.world.item.BlockItem::new)
                .model((ctx, prov) -> prov.withExistingParent(prov.name(ctx), GTNACORE.id(modelPath)))
                .build()
                .register();
    }

    private static BlockEntry<Block> createGlassCasingBlock(String name, ResourceLocation texture,
                                                            Supplier<Supplier<RenderType>> type) {
        return createCasingBlock(name, GlassBlock::new, texture, () -> Blocks.GLASS, type);
    }

    private static BlockEntry<MEStorageCoreBlock> createMEStorageCore(int tier, boolean craftingCore) {
        String name = "t" + tier + (craftingCore ? "_crafting_storage_core" : "_me_storage_core");
        String texture = "block/casings/" + (craftingCore ? "crafting_storage_core" : "me_storage_core") + "/t" + tier;
        return REGISTRATE.block(name, p -> new MEStorageCoreBlock(p, tier, craftingCore))
                .initialProperties(() -> Blocks.IRON_BLOCK)
                .properties(p -> p
                        .mapColor(MapColor.METAL)
                        .strength(5.0f, 6.0f)
                        .sound(SoundType.METAL)
                        .requiresCorrectToolForDrops()
                        .isValidSpawn((state, level, pos, ent) -> false))
                .addLayer(() -> RenderType::solid)
                .blockstate((ctx, prov) -> prov.simpleBlock(ctx.get(), prov.models().cubeAll(ctx.getName(),
                        GTNACORE.id(texture))))
                .tag(GTToolType.WRENCH.harvestTags.get(0), BlockTags.MINEABLE_WITH_PICKAXE)
                .item(GTNABlockItem::new)
                .build()
                .register();
    }

    public static BlockEntry<NexusCapacitorBlock> createCapacitorBlock(String name, int tier, long capacity) {
        return REGISTRATE.block(name, properties -> new NexusCapacitorBlock(properties, tier, capacity))
                .initialProperties(() -> Blocks.IRON_BLOCK)
                .properties(p -> p
                        .mapColor(MapColor.METAL)
                        .strength(5.0f, 6.0f)
                        .sound(SoundType.METAL)
                        .requiresCorrectToolForDrops()
                        .isValidSpawn((state, level, pos, ent) -> false))
                .addLayer(() -> RenderType::solid)
                .blockstate((ctx, prov) -> prov.simpleBlock(ctx.get(),
                        prov.models().cubeAll(ctx.getName(),
                                GTNACORE.id("block/wireless_energy_unit/" + name.replace("nexus_capacitor_", "")))))
                .tag(GTToolType.WRENCH.harvestTags.get(0), BlockTags.MINEABLE_WITH_PICKAXE)
                .item(GTNABlockItem::new)
                .build()
                .register();
    }
}
