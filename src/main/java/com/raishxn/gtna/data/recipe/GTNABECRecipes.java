package com.raishxn.gtna.data.recipe;

import com.gregtechceu.gtceu.api.data.chemical.material.Material;
import com.gregtechceu.gtceu.api.data.tag.TagPrefix;
import com.gregtechceu.gtceu.api.fluids.store.FluidStorageKeys;
import com.gregtechceu.gtceu.common.data.GTItems;
import com.gregtechceu.gtceu.common.data.GTMachines;
import com.gregtechceu.gtceu.common.data.GTMaterials;
import com.gregtechceu.gtceu.common.data.GTRecipeTypes;
import com.gregtechceu.gtceu.common.data.machines.GTMultiMachines;
import com.gregtechceu.gtceu.data.recipe.CustomTags;
import com.gregtechceu.gtceu.data.recipe.builder.GTRecipeBuilder;

import net.minecraft.data.recipes.FinishedRecipe;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.tags.TagKey;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.ItemLike;
import net.minecraftforge.fluids.FluidStack;
import net.minecraftforge.registries.ForgeRegistries;

import com.raishxn.gtna.GTNACORE;
import com.raishxn.gtna.api.bec.CondensateType;
import com.raishxn.gtna.api.bec.NaniteTier;
import com.raishxn.gtna.api.data.tag.GTNATagPrefix;
import com.raishxn.gtna.common.data.*;
import com.raishxn.gtna.common.machine.multiblock.electric.bec.BECIONodeMachine;

import java.util.ArrayList;
import java.util.List;
import java.util.function.Consumer;

import static com.gregtechceu.gtceu.api.GTValues.*;
import static com.raishxn.gtna.common.data.material.GodforgeChainMaterials.*;

/**
 * Every GTNH Bose-Einstein Condensate recipe with a GTNA output: the condensate generator recipes
 * ({@code CondensateType.registerRecipes}), the Condensate Assembler recipes ({@code BECRecipes} and
 * {@code BECMetaMaterialRecipes}, GT5U 9b4c2a7), the casing assembly lines ({@code ResearchStationAssemblyLine}), the
 * Peace/Conflict forming presses, the conduit assembler recipes and the controller and hatch assembly lines
 * (NewHorizonsCoreMod {@code AssemblingLineRecipes}). Not ported, their outputs do not exist in GTNA: the UMV/UXV
 * Component Assembly Line casings and the coremod's own BEC recipes (Exo-Foundry chassis, Computation Singularity,
 * Stargate parts, circuit arrays).
 * <p>
 * Tiers: GTNH UMV → GTCEu UXV, GTNH UXV → GTCEu OpV. Substitutions (GTNA has no such item or material; following
 * G-0199 where it already decided): Proto-Halkonite → Exo-Halkonite, Hexanite → Universium, Netherite → Neutronium,
 * Titansteel / Abyssal → Tritanium / Naquadria, Black Plutonium → Plutonium-241 (in Tairitsu), Infinity Catalyst →
 * Infinity, Blue Topaz / Callisto Ice / Ledox → Duranium / Tritanium / Trinium, Irradiant Reinforced Bedrockium
 * Plate → dense Bedrockium plate, Quark Containment Casing → Neutronium Stable Casing, UIV/UMV/UXV coils and
 * superconducting solenoids → superconductor wires of the tier, Railcraft electric engine → Gravi Star, Battery Gem 4
 * → Graviton Anomaly, Field Restriction Coil T2/T4 → T3 (twice as many for T4), Compact Fusion Coil T3 → Compressed
 * Fusion Coil MK2, Naquarite Insulator Foil → Naquadah Alloy foil, APIC → HASoC, ZPM2 / ZPM5 → Ultimate / Insanely
 * Ultimate Battery, Energised Tesseract → 2 Raw Tesseracts, Space-Time Continuum Ripper / Infinity-Infused
 * Manipulator → 4 / 2 Cosmic Fabric Manipulators, combined and eternal singularities → Gravi Stars, NH Core lenses →
 * Orundum / Nether Star / Magneto Resonatic lenses, BartWorks glass → Laminated Glass, TFFT field → Quantum Tank,
 * Dimensional Bridge → Plasma Forge Bridge Casing, LSC / Lapotronic UMV unit → Power Substation / UXV Nexus Capacitor,
 * wireless hatch → 16A energy hatch, energy tunnel → 4096A laser hatch, Black Hole Compressor → 4 Implosion
 * Compressors, UV solar panel → UV solar panel cover, AE2 singularity cells → 256k cells, SuperSolarPanels
 * components → exquisite Ruby/Emerald/Sapphire, GraviSuite superconductor → UHV superconductor wire, High Energy
 * Flow Circuit → HASoC, beamline hatches → LuV fluid hatches, Electrode Detector → advanced activity detector,
 * IC2 teleporter → Quantum Eye, Steve's RF cable → advanced energy detector, Degasifier control → machine controller
 * cover, Industrial Fluid Heater → UIV Fluid Heater, Advanced Assembly Line → Assembly Line. Item casings are
 * plates. Every assembly line uses station research at 512 CWU/t.
 */
public final class GTNABECRecipes {

    private GTNABECRecipes() {}

    /** GTNH {@code TIER_TO_NANITE}: the BEC recipe "nanite tier" numbers 1..10. */
    private static final NaniteTier[] TIER_TO_NANITE = { NaniteTier.Carbon, NaniteTier.Silver, NaniteTier.Gold,
            NaniteTier.Transcendent, NaniteTier.SixPhasedCopper, NaniteTier.WhiteDwarf, NaniteTier.BlackDwarf,
            NaniteTier.Universium, NaniteTier.Eternity, NaniteTier.MagMatter };

    private static final int INGOTS = 144;
    private static final int STACKS = 64 * 144;
    private static final int SECONDS = 20;

    private static final long RECIPE_UEV = VA[UEV], RECIPE_UIV = VA[UIV], RECIPE_UMV = VA[UXV], RECIPE_UXV = VA[OpV];

    public static void register(Consumer<FinishedRecipe> provider) {
        condensateGenerators(provider);
        materials(provider);
        bootstrap(provider);
        controllers(provider);
        becCasings(provider);
        main(provider);
        godforge(provider);
        shieldingCasing(provider);
        eyeOfHarmony(provider);
        metamaterials(provider);
    }

    // ---- helpers

    private static Material sub(String gtnh) {
        return switch (gtnh) {
            case "ProtoHalkonite" -> ExoHalkonite;
            case "Hexanite" -> GTNAMaterials.Universium;
            case "Netherite" -> GTMaterials.Neutronium;
            default -> throw new IllegalArgumentException(gtnh);
        };
    }

    /** The machine of {@code tier}, or the nearest registered tier above (then below) it. */
    private static com.gregtechceu.gtceu.api.machine.MachineDefinition tiered(
                                                                              com.gregtechceu.gtceu.api.machine.MachineDefinition[] machines,
                                                                              int tier) {
        for (int t = tier; t < machines.length; t++) if (machines[t] != null) return machines[t];
        for (int t = Math.min(tier, machines.length - 1); t >= 0; t--) if (machines[t] != null) return machines[t];
        throw new IllegalStateException("no tier registered");
    }

    private record Part(TagPrefix prefix, Material material, int count) {}

    private record Tagged(TagKey<Item> tag, int count) {}

    private static Part part(TagPrefix prefix, Material material, int count) {
        return new Part(prefix, material, count);
    }

    private static Tagged circuit(TagKey<Item> tag, int count) {
        return new Tagged(tag, count);
    }

    private static ItemStack stack(ItemLike item, int count) {
        return new ItemStack(item, count);
    }

    private static ItemStack modItem(String id, int count) {
        Item item = ForgeRegistries.ITEMS.getValue(new ResourceLocation(id));
        return item == null || item == Items.AIR ? new ItemStack(GTItems.GRAVI_STAR.get(), count) :
                new ItemStack(item, count);
    }

    private static void inputs(GTRecipeBuilder builder, Object... inputs) {
        for (Object input : inputs) {
            if (input instanceof Part p) builder.inputItems(p.prefix, p.material, p.count);
            else if (input instanceof Tagged t) builder.inputItems(t.tag, t.count);
            else if (input instanceof ItemStack s) builder.inputItems(s);
            else throw new IllegalArgumentException("unsupported input " + input);
        }
    }

    private static FluidStack molten(Material material, int amount) {
        return material.getFluid(amount);
    }

    private static FluidStack plasma(Material material, int amount) {
        var fluid = material.getFluid(FluidStorageKeys.PLASMA);
        return fluid == null ? material.getFluid(amount) : new FluidStack(fluid, amount);
    }

    private static int[] shifted(int shift, int... tiers) {
        int[] out = new int[tiers.length];
        for (int i = 0; i < tiers.length; i++) out[i] = TIER_TO_NANITE[tiers[i] - 1 + shift].ordinal();
        return out;
    }

    private static int[] nanites(int... tiers) {
        return shifted(0, tiers);
    }

    /** GTNH {@code addBec}. */
    private static void bec(Consumer<FinishedRecipe> provider, String id, ItemStack output, Object[] inputs,
                            int[] nanites, FluidStack[] condensates, int duration, long eut) {
        if (nanites.length != inputs.length) throw new IllegalStateException(
                "BEC recipe " + id + ": " + inputs.length + " inputs but " + nanites.length + " nanite tiers");
        var builder = GTNARecipeType.CONDENSATE_ASSEMBLER_RECIPES.recipeBuilder(GTNACORE.id("bec/" + id))
                .outputItems(output).duration(duration).EUt(eut)
                .addData(BECIONodeMachine.NANITE_TIERS, BECIONodeMachine.encodeTiers(nanites));
        inputs(builder, inputs);
        for (FluidStack condensate : condensates) builder.inputFluids(condensate);
        builder.save(provider);
    }

    private static void assemblyLine(Consumer<FinishedRecipe> provider, String id, ItemStack research,
                                     Object[] inputs, FluidStack[] fluids, ItemStack output, int duration, long eut) {
        var builder = GTRecipeTypes.ASSEMBLY_LINE_RECIPES.recipeBuilder(GTNACORE.id("bec/" + id))
                .outputItems(output).duration(duration).EUt(eut)
                .stationResearch(b -> b.researchStack(research).CWUt(512).EUt(eut));
        inputs(builder, inputs);
        for (FluidStack fluid : fluids) builder.inputFluids(fluid);
        builder.save(provider);
    }

    private static Part tai(TagPrefix prefix, int count) {
        return part(prefix, Tairitsu, count);
    }

    private static Part chu(TagPrefix prefix, int count) {
        return part(prefix, Churitsu, count);
    }

    private static Part shi(TagPrefix prefix, int count) {
        return part(prefix, Shijima, count);
    }

    private static FluidStack[] uivFluids(int chromatic, int infinity, int tungsten, int solder) {
        return new FluidStack[] { molten(ChronomaticGlass, chromatic), molten(Infinity, infinity),
                molten(CelestialTungsten, tungsten), molten(MutatedLivingSolder, solder) };
    }

    // ---- 1. condensate generators (CondensateType.registerRecipes)

    private static void condensateGenerators(Consumer<FinishedRecipe> provider) {
        for (CondensateType type : CondensateType.VALUES) {
            GTNARecipeType.CONDENSATE_GENERATOR_RECIPES.recipeBuilder(GTNACORE.id("bec/entangle_" + type.id))
                    .inputFluids(type.getSourceFluid())
                    .outputFluids(type.getEntangled(type.unit))
                    .duration(type.duration).EUt(type.eut).save(provider);
        }
    }

    // ---- 2. materials GTNA did not have

    private static void materials(Consumer<FinishedRecipe> provider) {
        // Bedrockium: GTNH mines it (ore, bees); GTNA mixes its composition (SiO2 + diamond) instead. EBF and vacuum
        // freezer come from the material's blast property.
        GTRecipeTypes.MIXER_RECIPES.recipeBuilder(GTNACORE.id("bec/bedrockium_dust"))
                .inputItems(TagPrefix.dust, GTMaterials.SiliconDioxide, 64).inputItems(TagPrefix.dust,
                        GTMaterials.Diamond, 1)
                .outputItems(TagPrefix.dust, Bedrockium, 1).duration(30 * SECONDS).EUt(VA[UV]).save(provider);
        // Tairitsu (GoodGenerator mixer, circuit 6).
        GTRecipeTypes.MIXER_RECIPES.recipeBuilder(GTNACORE.id("bec/tairitsu_dust"))
                .inputItems(TagPrefix.dust, GTMaterials.Tungsten, 8)
                .inputItems(TagPrefix.dust, GTMaterials.Naquadria, 7)
                .inputItems(TagPrefix.dust, Bedrockium, 4).inputItems(TagPrefix.dust, GTMaterials.Carbon, 4)
                .inputItems(TagPrefix.dust, GTMaterials.Vanadium, 3)
                .inputItems(TagPrefix.dust, GTMaterials.Plutonium241, 1).circuitMeta(6)
                .outputItems(TagPrefix.dust, Tairitsu, 27).duration(60 * SECONDS).EUt(VA[UHV]).save(provider);
        // Inactive Cosmic Solder (GT5U TranscendentPlasmaMixerRecipes, circuit 24).
        GTNARecipeType.TRANSCENDENT_PLASMA_MIXER_RECIPES.recipeBuilder(GTNACORE.id("bec/tpm_inactive_cosmic_solder"))
                .circuitMeta(24).duration(100)
                .addData("tpm_eut", 1_073_007_39L).addData("tpm_duration", 100).addData("eu_multiplier", 1L)
                .inputFluids(GTNAMaterials.DimensionallyTranscendentResidue.getFluid(1000))
                .inputFluids(plasma(GTMaterials.Tin, 1000)).inputFluids(plasma(GTMaterials.Antimony, 1000))
                .inputFluids(plasma(GTMaterials.Lead, 1000)).inputFluids(GTNAMaterials.RawStarMatter.getFluid(25))
                .outputFluids(InactiveCosmicSolder.getFluid(4000)).save(provider);
        // Boundless Cosmic Solder: GTNH activates it in the Beamcrafter with 64 Pseudo Stars; GTNA has neither, so
        // the Plasma Forge does it with the same fluids and catalyst nanites (not consumed).
        GTNARecipeType.PLASMA_FORGE_RECIPES.recipeBuilder(GTNACORE.id("bec/boundless_cosmic_solder"))
                .notConsumable(GTNANanoForge.TRANSCENDENT_METAL_NANITES.asStack(2))
                .inputItems(GTItems.GRAVI_STAR, 16)
                .inputFluids(InactiveCosmicSolder.getFluid(160_000))
                .inputFluids(GTNAMaterials.SpaceTime.getFluid(16 * INGOTS))
                .outputFluids(BoundlessCosmicSolder.getFluid(160_000))
                .duration(2 * SECONDS).EUt(VA[ZPM]).blastFurnaceTemp(12_600).save(provider);
        // MagMatter and MHDCSM have no material recipes in GTNA; the BEC needs a few of their parts.
        for (Material m : new Material[] { GTNAMaterials.MagMatter,
                GTNAMaterials.MagnetohydrodynamicallyConstrainedStarMatter }) {
            String id = m.getName();
            GTRecipeTypes.FLUID_SOLIDFICATION_RECIPES.recipeBuilder(GTNACORE.id("bec/" + id + "_plate"))
                    .notConsumable(GTItems.SHAPE_MOLD_PLATE).inputFluids(m.getFluid(INGOTS))
                    .outputItems(TagPrefix.plate, m).duration(2 * SECONDS).EUt(VA[UXV]).save(provider);
            GTRecipeTypes.FLUID_SOLIDFICATION_RECIPES.recipeBuilder(GTNACORE.id("bec/" + id + "_nugget"))
                    .notConsumable(GTItems.SHAPE_MOLD_NUGGET).inputFluids(m.getFluid(16))
                    .outputItems(TagPrefix.nugget, m).duration(10).EUt(VA[UXV]).save(provider);
            GTRecipeTypes.EXTRUDER_RECIPES.recipeBuilder(GTNACORE.id("bec/" + id + "_rod"))
                    .inputItems(TagPrefix.plate, m).notConsumable(GTItems.SHAPE_EXTRUDER_ROD)
                    .outputItems(TagPrefix.rod, m, 2).duration(2 * SECONDS).EUt(VA[UXV]).save(provider);
            GTRecipeTypes.FORGE_HAMMER_RECIPES.recipeBuilder(GTNACORE.id("bec/" + id + "_long_rod"))
                    .inputItems(TagPrefix.rod, m, 2).outputItems(TagPrefix.rodLong, m).duration(4 * SECONDS)
                    .EUt(VA[UXV]).save(provider);
            GTRecipeTypes.EXTRUDER_RECIPES.recipeBuilder(GTNACORE.id("bec/" + id + "_ring"))
                    .inputItems(TagPrefix.plate, m).notConsumable(GTItems.SHAPE_EXTRUDER_RING)
                    .outputItems(TagPrefix.ring, m, 4).duration(2 * SECONDS).EUt(VA[UXV]).save(provider);
            GTRecipeTypes.EXTRUDER_RECIPES.recipeBuilder(GTNACORE.id("bec/" + id + "_bolt"))
                    .inputItems(TagPrefix.plate, m).notConsumable(GTItems.SHAPE_EXTRUDER_BOLT)
                    .outputItems(TagPrefix.bolt, m, 8).duration(2 * SECONDS).EUt(VA[UXV]).save(provider);
            GTRecipeTypes.LATHE_RECIPES.recipeBuilder(GTNACORE.id("bec/" + id + "_screw"))
                    .inputItems(TagPrefix.bolt, m).outputItems(TagPrefix.screw, m).duration(SECONDS)
                    .EUt(VA[UXV]).save(provider);
            GTRecipeTypes.LATHE_RECIPES.recipeBuilder(GTNACORE.id("bec/" + id + "_round"))
                    .inputItems(TagPrefix.nugget, m).outputItems(TagPrefix.round, m).duration(SECONDS)
                    .EUt(VA[UXV]).save(provider);
            GTRecipeTypes.BENDER_RECIPES.recipeBuilder(GTNACORE.id("bec/" + id + "_foil"))
                    .inputItems(TagPrefix.plate, m).circuitMeta(10).outputItems(TagPrefix.foil, m, 4)
                    .duration(2 * SECONDS).EUt(VA[UXV]).save(provider);
        }
    }

    // ---- 3. conduits, Peace/Conflict casings

    private static void bootstrap(Consumer<FinishedRecipe> provider) {
        GTRecipeTypes.FORMING_PRESS_RECIPES.recipeBuilder(GTNACORE.id("bec/peace_enforcement_casing"))
                .inputItems(TagPrefix.frameGt, Tairitsu).inputItems(TagPrefix.plate, Churitsu, 2)
                .inputFluids(molten(Shijima, 2 * INGOTS))
                .outputItems(GTNABlocks.PEACE_ENFORCEMENT_CASING.asStack()).duration(10 * SECONDS).EUt(RECIPE_UEV)
                .save(provider);
        GTRecipeTypes.FORMING_PRESS_RECIPES.recipeBuilder(GTNACORE.id("bec/conflict_inducement_casing"))
                .inputItems(TagPrefix.frameGt, Shijima).inputItems(TagPrefix.plate, Churitsu, 2)
                .inputFluids(molten(Tairitsu, 2 * INGOTS))
                .outputItems(GTNABlocks.CONFLICT_INDUCEMENT_CASING.asStack()).duration(10 * SECONDS).EUt(RECIPE_UEV)
                .save(provider);
        GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder(GTNACORE.id("bec/conduit"))
                .inputItems(com.gregtechceu.gtceu.common.data.GTBlocks.LASER_PIPES[0].asStack())
                .inputItems(TagPrefix.foil, GTMaterials.NaquadahAlloy, 4)
                .inputFluids(molten(ChronomaticGlass, INGOTS))
                .outputItems(GTNABEC.BEC_CONDUIT.asStack()).duration(5 * SECONDS).EUt(RECIPE_UEV).save(provider);
        GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder(GTNACORE.id("bec/conduit_casing"))
                .inputItems(GTNABEC.BEC_CONDUIT.asStack())
                .inputItems(com.gregtechceu.gtceu.common.data.GTBlocks.MACHINE_CASING_UV.asStack())
                .outputItems(GTNABEC.BEC_CONDUIT_CASING.asStack()).duration(SECONDS).EUt(VA[UV]).save(provider);
    }

    // ---- 4. controllers and hatches (NewHorizonsCoreMod AssemblingLineRecipes)

    private static void controllers(Consumer<FinishedRecipe> provider) {
        ItemStack hull = tiered(GTMachines.HULL, UIV).asStack();
        FluidStack solder8 = molten(MutatedLivingSolder, 8 * STACKS);
        assemblyLine(provider, "nanite_detector_hatch", GTItems.COVER_ACTIVITY_DETECTOR_ADVANCED.asStack(),
                new Object[] { hull, GTItems.COVER_ACTIVITY_DETECTOR_ADVANCED.asStack(), GTItems.SENSOR_UIV.asStack(),
                        part(TagPrefix.gearSmall, Hypogen, 2), tai(TagPrefix.gear, 1), chu(TagPrefix.gear, 1),
                        shi(TagPrefix.gear, 1) },
                new FluidStack[] { molten(GTMaterials.Neutronium, 16 * INGOTS), molten(ChronomaticGlass, 32 * INGOTS),
                        molten(CelestialTungsten, 16 * INGOTS), solder8 },
                GTNABEC.NANITE_DETECTOR_HATCH.asStack(), 30 * SECONDS, RECIPE_UIV);
        assemblyLine(provider, "bec_hatch", tiered(GTMachines.FLUID_IMPORT_HATCH, LuV).asStack(),
                new Object[] { hull, tiered(GTMachines.FLUID_IMPORT_HATCH, LuV).asStack(),
                        tiered(GTMachines.FLUID_EXPORT_HATCH, LuV).asStack(), GTItems.ELECTRIC_PUMP_UIV.asStack(2),
                        part(TagPrefix.rodLong, Hypogen, 1), tai(TagPrefix.rotor, 1), chu(TagPrefix.rotor, 1),
                        shi(TagPrefix.rotor, 1) },
                new FluidStack[] { molten(Infinity, 16 * INGOTS), molten(ChronomaticGlass, 32 * INGOTS),
                        molten(CelestialTungsten, 16 * INGOTS), solder8 },
                GTNABEC.BEC_HATCH.asStack(), 30 * SECONDS, RECIPE_UIV);
        assemblyLine(provider, "condensate_detector_hatch", GTNABEC.BEC_HATCH.asStack(),
                new Object[] { hull, GTNABEC.BEC_HATCH.asStack(), GTNABEC.NANITE_DETECTOR_HATCH.asStack(),
                        tai(TagPrefix.plate, 3), chu(TagPrefix.plate, 3), shi(TagPrefix.plate, 3) },
                new FluidStack[] { molten(Churitsu, 16 * INGOTS), molten(ChronomaticGlass, 32 * INGOTS),
                        molten(CelestialTungsten, 16 * INGOTS), solder8 },
                GTNABEC.CONDENSATE_DETECTOR_HATCH.asStack(), 30 * SECONDS, RECIPE_UIV);
        assemblyLine(provider, "io_node_controller_hatch", stack(Items.LEVER, 1),
                new Object[] { hull, GTItems.QUANTUM_EYE.asStack(), GTItems.COVER_ENERGY_DETECTOR_ADVANCED.asStack(),
                        modItem("ae2:controller", 1), GTItems.COVER_MACHINE_CONTROLLER.asStack() },
                new FluidStack[] { molten(ChronomaticGlass, 32 * INGOTS), molten(Infinity, 16 * INGOTS),
                        molten(CelestialTungsten, 16 * INGOTS), solder8 },
                GTNABEC.IO_NODE_CONTROLLER_HATCH.asStack(), 30 * SECONDS, RECIPE_UIV);
        assemblyLine(provider, "line_of_sight_connector_hatch", stack(Items.BEACON, 1),
                new Object[] { hull, stack(Items.BEACON, 1), GTNABlocks.PLASMA_FORGE_BRIDGE_CASING.asStack(2),
                        GTItems.CONVEYOR_MODULE_UIV.asStack(), tai(TagPrefix.wireFine, 8), chu(TagPrefix.wireFine, 8),
                        shi(TagPrefix.wireFine, 8) },
                new FluidStack[] { molten(Hypogen, 16 * INGOTS), molten(ChronomaticGlass, 32 * INGOTS),
                        molten(CelestialTungsten, 16 * INGOTS), solder8 },
                GTNABEC.LINE_OF_SIGHT_HATCH.asStack(), 30 * SECONDS, RECIPE_UIV);
        assemblyLine(provider, "nanite_containment_bus", GTNANanoForge.CARBON_NANITES.asStack(),
                new Object[] { tiered(GTMachines.ITEM_IMPORT_BUS, UHV).asStack(),
                        tiered(GTMachines.QUANTUM_CHEST, EV).asStack(),
                        GTItems.FIELD_GENERATOR_UHV.asStack(), GTNANanoForge.CARBON_NANITES.asStack(4),
                        part(TagPrefix.plateDense, GTMaterials.NaquadahAlloy, 4),
                        part(GTNATagPrefix.superdensePlate, GTNAMaterials.CosmicNeutronium, 4) },
                new FluidStack[] { molten(MutatedLivingSolder, 2304) },
                GTNABEC.NANITE_CONTAINMENT_BUS.asStack(), 30 * SECONDS, VA[UHV]);

        FluidStack dtec = ExcitedDTEC.getFluid(1_000_000);
        assemblyLine(provider, "bec_generator", tiered(GTMachines.FLUID_HEATER, UIV).asStack(),
                new Object[] { tiered(GTMachines.FLUID_HEATER, UIV).asStack(),
                        GTNABlocks.ELECTROMAGNETICALLY_ISOLATED_CASING.asStack(4),
                        GTNAGodforgeContent.HYPOGEN_COIL.asStack(16),
                        part(TagPrefix.wireGtHex, SuperconductorUIV, 16), circuit(CustomTags.UIV_CIRCUITS, 16),
                        tai(TagPrefix.plateDense, 8), chu(TagPrefix.plateDense, 8), shi(TagPrefix.plateDense, 8),
                        GTItems.EMITTER_UIV.asStack(16), GTItems.ELECTRIC_PUMP_UIV.asStack(16),
                        GTNAItems.LASER_LENS_SPECIAL.asStack(16) },
                new FluidStack[] { molten(ChronomaticGlass, 1024 * INGOTS), molten(MutatedLivingSolder, 512 * INGOTS),
                        dtec, molten(GTNAMaterials.SpaceTime, 32 * INGOTS) },
                GTNABEC.BEC_GENERATOR.asStack(), 150 * SECONDS, RECIPE_UMV);
        assemblyLine(provider, "bec_storage", GTNAGodforgeComponents.STABLE_BOSON_CONTAINMENT_UNIT.asStack(),
                new Object[] { hull, GTNABlocks.FINE_STRUCTURE_CONSTANT_MANIPULATOR.asStack(4),
                        tiered(GTMachines.QUANTUM_TANK, UHV).asStack(8),
                        part(TagPrefix.wireGtHex, SuperconductorUIV, 16),
                        circuit(CustomTags.UIV_CIRCUITS, 32), tai(TagPrefix.plateDense, 16),
                        chu(TagPrefix.plateDense, 16), shi(TagPrefix.plateDense, 16),
                        GTNAGodforgeComponents.STABLE_BOSON_CONTAINMENT_UNIT.asStack(32) },
                new FluidStack[] { molten(ChronomaticGlass, 2048 * INGOTS), molten(MutatedLivingSolder, 1024 * INGOTS),
                        ExcitedDTEC.getFluid(2_000_000), molten(GTNAMaterials.SpaceTime, 64 * INGOTS) },
                GTNABEC.BEC_STORAGE.asStack(), 300 * SECONDS, RECIPE_UMV);
        assemblyLine(provider, "bec_assembler", GTMultiMachines.ASSEMBLY_LINE.asStack(),
                new Object[] { GTMultiMachines.ASSEMBLY_LINE.asStack(),
                        GTNABlocks.COHERENCE_PRESERVING_PLASMA_CONDUIT.asStack(4),
                        GTNABlocks.PLASMA_FORGE_BRIDGE_CASING.asStack(16),
                        part(TagPrefix.wireGtHex, SuperconductorUIV, 16), circuit(CustomTags.UIV_CIRCUITS, 16),
                        tai(TagPrefix.plateDense, 8), chu(TagPrefix.plateDense, 8), shi(TagPrefix.plateDense, 8),
                        GTItems.SENSOR_UIV.asStack(16), GTItems.ROBOT_ARM_UIV.asStack(16),
                        part(TagPrefix.lens, Orundum, 64), modItem("ae2:singularity", 8) },
                new FluidStack[] { molten(ChronomaticGlass, 1024 * INGOTS), molten(MutatedLivingSolder, 512 * INGOTS),
                        dtec, molten(GTNAMaterials.SpaceTime, 32 * INGOTS) },
                GTNABEC.BEC_ASSEMBLER.asStack(), 150 * SECONDS, RECIPE_UMV);
        assemblyLine(provider, "bec_io_node", GTItems.QUANTUM_EYE.asStack(),
                new Object[] { GTItems.QUANTUM_EYE.asStack(), GTNABlocks.COHERENCE_PRESERVING_PLASMA_CONDUIT.asStack(4),
                        GTNABlocks.PLASMA_FORGE_BRIDGE_CASING.asStack(16),
                        part(TagPrefix.wireGtHex, SuperconductorUIV, 16), circuit(CustomTags.UIV_CIRCUITS, 16),
                        tai(TagPrefix.plateDense, 8), chu(TagPrefix.plateDense, 8), shi(TagPrefix.plateDense, 8),
                        GTItems.EMITTER_UIV.asStack(8), GTItems.CONVEYOR_MODULE_UIV.asStack(8),
                        stack(GTItems.GRAVI_STAR.get(), 16), modItem("ae2:singularity", 8) },
                new FluidStack[] { molten(ChronomaticGlass, 1024 * INGOTS), molten(MutatedLivingSolder, 512 * INGOTS),
                        dtec, molten(GTNAMaterials.SpaceTime, 32 * INGOTS) },
                GTNABEC.BEC_IO_NODE.asStack(), 150 * SECONDS, RECIPE_UMV);
        assemblyLine(provider, "bec_diode", modItem("ae2:storage_bus", 1),
                new Object[] { modItem("ae2:storage_bus", 1), GTNABlocks.ELECTROMAGNETICALLY_ISOLATED_CASING.asStack(4),
                        GTItems.FLUID_REGULATOR_UIV.asStack(4), part(TagPrefix.wireGtHex, SuperconductorUIV, 16),
                        circuit(CustomTags.UIV_CIRCUITS, 8), tai(TagPrefix.plateDense, 4),
                        chu(TagPrefix.plateDense, 4), shi(TagPrefix.plateDense, 4) },
                new FluidStack[] { molten(ChronomaticGlass, 512 * INGOTS), molten(MutatedLivingSolder, 256 * INGOTS),
                        ExcitedDTEC.getFluid(500_000), molten(GTNAMaterials.SpaceTime, 16 * INGOTS) },
                GTNABEC.BEC_DIODE.asStack(), 75 * SECONDS, RECIPE_UMV);
    }

    // ---- 5. BEC casings: assembly line (ResearchStationAssemblyLine) and BEC (addBECCasingRecipes)

    private static void becCasings(Consumer<FinishedRecipe> provider) {
        Material halk = sub("ProtoHalkonite");
        assemblyLine(provider, "electromagnetically_isolated_casing", GTNABlocks.NEUTRONIUM_STABLE_CASING.asStack(),
                new Object[] { GTNABlocks.NEUTRONIUM_STABLE_CASING.asStack(6), tai(TagPrefix.frameGt, 24),
                        chu(TagPrefix.frameGt, 24), shi(TagPrefix.frameGt, 24),
                        part(TagPrefix.plateDense, Bedrockium, 16), part(TagPrefix.foil, halk, 32),
                        tai(TagPrefix.plate, 8), chu(TagPrefix.screw, 64), shi(TagPrefix.bolt, 64),
                        GTItems.FIELD_GENERATOR_UEV.asStack(2), part(TagPrefix.screw, SixPhasedCopper, 48),
                        part(TagPrefix.screw, Hypogen, 48) },
                uivFluids(384 * INGOTS, 48 * INGOTS, 48 * INGOTS, 16 * INGOTS),
                GTNABlocks.ELECTROMAGNETICALLY_ISOLATED_CASING.asStack(16), 30 * SECONDS, RECIPE_UIV);
        assemblyLine(provider, "coherence_preserving_plasma_conduit", GTNABlocks.PEACE_ENFORCEMENT_CASING.asStack(),
                new Object[] { GTNABlocks.QUARK_PIPE.asStack(2), GTNABlocks.PEACE_ENFORCEMENT_CASING.asStack(12),
                        part(TagPrefix.pipeHugeFluid, GTMaterials.Neutronium, 6),
                        GTNAGodforgeComponents.ELECTROMAGNET_TENGAM.asStack(),
                        part(TagPrefix.wireGtQuadruple, SuperconductorUIV, 4), part(TagPrefix.rod, halk, 8),
                        tai(TagPrefix.foil, 16), chu(TagPrefix.plate, 8), shi(TagPrefix.screw, 32),
                        GTItems.ELECTRIC_PUMP_UIV.asStack(3), part(TagPrefix.rotor, SixPhasedCopper, 6),
                        part(TagPrefix.rotor, Hypogen, 6) },
                uivFluids(384 * INGOTS, 48 * INGOTS, 48 * INGOTS, 16 * INGOTS),
                GTNABlocks.COHERENCE_PRESERVING_PLASMA_CONDUIT.asStack(8), 60 * SECONDS, RECIPE_UIV);
        assemblyLine(provider, "fine_structure_constant_manipulator", GTNABlocks.CONFLICT_INDUCEMENT_CASING.asStack(),
                new Object[] { GTNABlocks.CONFLICT_INDUCEMENT_CASING.asStack(12),
                        GTNABlocks.ELECTROMAGNETICALLY_ISOLATED_CASING.asStack(3),
                        part(TagPrefix.wireGtQuadruple, SuperconductorUIV, 4), part(TagPrefix.rodLong, halk, 4),
                        tai(TagPrefix.wireFine, 32), chu(TagPrefix.foil, 16), shi(TagPrefix.screw, 32),
                        stack(GTItems.GRAVI_STAR.get(), 8), part(TagPrefix.ring, halk, 8), tai(TagPrefix.foil, 16),
                        chu(TagPrefix.gearSmall, 4), shi(TagPrefix.round, 36), GTItems.SENSOR_UIV.asStack(2),
                        GTItems.EMITTER_UIV.asStack(2), part(TagPrefix.gearSmall, SixPhasedCopper, 6),
                        part(TagPrefix.gearSmall, Hypogen, 6) },
                uivFluids(384 * INGOTS, 48 * INGOTS, 48 * INGOTS, 16 * INGOTS),
                GTNABlocks.FINE_STRUCTURE_CONSTANT_MANIPULATOR.asStack(8), 30 * SECONDS, RECIPE_UIV);
        assemblyLine(provider, "condensate_guidance_coil", stack(GTNABlocks.COMPRESSED_FUSION_COIL_MK2.get(), 1),
                new Object[] { GTNABlocks.COMPRESSED_FUSION_COIL_MK2.asStack(2), tai(TagPrefix.frameGt, 2),
                        chu(TagPrefix.frameGt, 2), shi(TagPrefix.frameGt, 2),
                        part(TagPrefix.wireGtQuadruple, SuperconductorUIV, 2), part(TagPrefix.rodLong, halk, 2),
                        tai(TagPrefix.wireFine, 16), chu(TagPrefix.foil, 8), shi(TagPrefix.screw, 16),
                        part(TagPrefix.foil, GTMaterials.NaquadahAlloy, 6),
                        part(TagPrefix.wireFine, SixPhasedCopper, 12), part(TagPrefix.wireFine, Hypogen, 12) },
                uivFluids(384 * INGOTS, 24 * INGOTS, 24 * INGOTS, 24 * INGOTS),
                GTNABlocks.CONDENSATE_GUIDANCE_COIL.asStack(), 15 * SECONDS, RECIPE_UIV);
        assemblyLine(provider, "condensate_transformative_coil", GTNABlocks.CONDENSATE_GUIDANCE_COIL.asStack(),
                new Object[] { GTNABlocks.FIELD_RESTRICTION_COIL_T3.asStack(2), part(TagPrefix.frameGt,
                        ChronomaticGlass, 6), part(TagPrefix.wireGtDouble, SuperconductorUIV, 6),
                        stack(GTItems.HIGHLY_ADVANCED_SOC.get(), 6), GTItems.EMITTER_UHV.asStack(4),
                        tai(TagPrefix.rod, 4), chu(TagPrefix.foil, 2), shi(TagPrefix.plate, 2),
                        GTItems.SENSOR_UHV.asStack(4), tai(TagPrefix.plate, 4), chu(TagPrefix.plate, 2),
                        shi(TagPrefix.bolt, 32), GTItems.FIELD_GENERATOR_UHV.asStack(2), tai(TagPrefix.rodLong, 4),
                        chu(TagPrefix.ring, 2), shi(TagPrefix.plateDouble, 4) },
                uivFluids(384 * INGOTS, 24 * INGOTS, 24 * INGOTS, 24 * INGOTS),
                GTNABlocks.CONDENSATE_TRANSFORMATIVE_COIL.asStack(), 30 * SECONDS, RECIPE_UIV);
        assemblyLine(provider, "electromagnetic_waveguide", GTNABlocks.ANTIMATTER_CONTAINMENT_CASING.asStack(),
                new Object[] { GTNABlocks.ANTIMATTER_CONTAINMENT_CASING.asStack(6),
                        part(TagPrefix.wireGtQuadruple, SuperconductorUIV, 2), part(TagPrefix.rodLong, halk, 2),
                        tai(TagPrefix.wireFine, 16), chu(TagPrefix.foil, 8), shi(TagPrefix.screw, 16),
                        chu(TagPrefix.plate, 6), GTItems.FIELD_GENERATOR_UEV.asStack(2) },
                uivFluids(768 * INGOTS, 12 * INGOTS, 12 * INGOTS, 4 * INGOTS),
                GTNABlocks.ELECTROMAGNETIC_WAVEGUIDE.asStack(8), 120 * SECONDS, RECIPE_UIV);

        // addBECCasingRecipes: the BEC makes the same casings cheaper once it runs.
        FluidStack[] cit = { CondensateType.ChromaticGlass.getEntangled(256 * INGOTS),
                CondensateType.Infinity.getEntangled(32 * INGOTS),
                CondensateType.CelestialTungsten.getEntangled(32 * INGOTS) };
        bec(provider, "electromagnetically_isolated_casing", GTNABlocks.ELECTROMAGNETICALLY_ISOLATED_CASING.asStack(16),
                new Object[] { GTNABlocks.NEUTRONIUM_STABLE_CASING.asStack(4), tai(TagPrefix.frameGt, 16),
                        chu(TagPrefix.frameGt, 16), shi(TagPrefix.frameGt, 16), GTNABEC.SHIELDING[0].asStack(8),
                        GTItems.FIELD_GENERATOR_UEV.asStack(1), part(TagPrefix.screw, SixPhasedCopper, 32),
                        part(TagPrefix.screw, Hypogen, 32) },
                nanites(4, 1, 1, 1, 3, 2, 1, 1), cit, 1200 * SECONDS, RECIPE_UIV);
        bec(provider, "coherence_preserving_plasma_conduit",
                GTNABlocks.COHERENCE_PRESERVING_PLASMA_CONDUIT.asStack(8),
                new Object[] { GTNABlocks.QUARK_PIPE.asStack(1), GTNABlocks.PEACE_ENFORCEMENT_CASING.asStack(8),
                        part(TagPrefix.pipeHugeFluid, GTMaterials.Neutronium, 4),
                        GTNAGodforgeComponents.ELECTROMAGNET_TENGAM.asStack(), GTNABEC.ENERGY_CONDUIT[0].asStack(4),
                        GTItems.ELECTRIC_PUMP_UIV.asStack(2), part(TagPrefix.rotor, SixPhasedCopper, 4),
                        part(TagPrefix.rotor, Hypogen, 4) },
                nanites(4, 1, 1, 2, 1, 3, 1, 1), cit, 1200 * SECONDS, RECIPE_UIV);
        bec(provider, "fine_structure_constant_manipulator",
                GTNABlocks.FINE_STRUCTURE_CONSTANT_MANIPULATOR.asStack(8),
                new Object[] { GTNABlocks.CONFLICT_INDUCEMENT_CASING.asStack(8),
                        GTNABlocks.ELECTROMAGNETICALLY_ISOLATED_CASING.asStack(2), GTNABEC.WAVEGUIDE[0].asStack(4),
                        GTNABEC.ELECTROGRAVITIC_VALVE[0].asStack(4), GTItems.SENSOR_UIV.asStack(),
                        GTItems.EMITTER_UIV.asStack(), part(TagPrefix.gearSmall, SixPhasedCopper, 4),
                        part(TagPrefix.gearSmall, Hypogen, 4) },
                nanites(3, 4, 1, 1, 3, 2, 1, 1), cit, 600 * SECONDS, RECIPE_UIV);
        FluidStack[] cit16 = { CondensateType.ChromaticGlass.getEntangled(256 * INGOTS),
                CondensateType.Infinity.getEntangled(16 * INGOTS),
                CondensateType.CelestialTungsten.getEntangled(16 * INGOTS) };
        bec(provider, "condensate_guidance_coil", GTNABlocks.CONDENSATE_GUIDANCE_COIL.asStack(),
                new Object[] { GTNABlocks.COMPRESSED_FUSION_COIL_MK2.asStack(1), tai(TagPrefix.frameGt, 1),
                        chu(TagPrefix.frameGt, 1), shi(TagPrefix.frameGt, 1), GTNABEC.WAVEGUIDE[0].asStack(2),
                        part(TagPrefix.foil, GTMaterials.NaquadahAlloy, 4),
                        part(TagPrefix.wireFine, SixPhasedCopper, 8), part(TagPrefix.wireFine, Hypogen, 8) },
                nanites(3, 1, 1, 1, 4, 2, 1, 1), cit16, 150 * SECONDS, RECIPE_UIV);
        bec(provider, "condensate_transformative_coil", GTNABlocks.CONDENSATE_TRANSFORMATIVE_COIL.asStack(),
                new Object[] { GTNABlocks.FIELD_RESTRICTION_COIL_T3.asStack(1),
                        part(TagPrefix.frameGt, ChronomaticGlass, 4),
                        part(TagPrefix.wireGtDouble, SuperconductorUIV, 4),
                        stack(GTItems.HIGHLY_ADVANCED_SOC.get(), 4), GTNABEC.SENSOR_ARRAY[0].asStack(2),
                        GTNABEC.RESONANCE_CHAMBER[0].asStack(2), GTNABEC.FIELD_MANIPULATOR[0].asStack(2) },
                nanites(2, 1, 2, 1, 3, 3, 4), cit16, 300 * SECONDS, RECIPE_UIV);
        bec(provider, "electromagnetic_waveguide", GTNABlocks.ELECTROMAGNETIC_WAVEGUIDE.asStack(8),
                new Object[] { GTNABlocks.ANTIMATTER_CONTAINMENT_CASING.asStack(4), GTNABEC.WAVEGUIDE[0].asStack(2),
                        chu(TagPrefix.plate, 4), GTItems.FIELD_GENERATOR_UEV.asStack() },
                nanites(3, 4, 1, 1), new FluidStack[] { CondensateType.ChromaticGlass.getEntangled(512 * INGOTS),
                        CondensateType.Infinity.getEntangled(8 * INGOTS),
                        CondensateType.CelestialTungsten.getEntangled(8 * INGOTS) },
                240 * SECONDS, RECIPE_UIV);
    }

    // ---- 6. BECRecipes.run (Transdimensional Alignment Matrix; CoAL casings not ported)

    private static void main(Consumer<FinishedRecipe> provider) {
        bec(provider, "transdimensional_alignment_matrix", GTNABEC.TRANSDIMENSIONAL_ALIGNMENT_MATRIX.asStack(),
                new Object[] { GTNAEyeOfHarmonyContent.BOUNDARY_CASING.asStack(),
                        GTNABlocks.COSMIC_FABRIC_MANIPULATOR.asStack(16), GTItems.ROBOT_ARM_UXV.asStack(64),
                        GTItems.SENSOR_UXV.asStack(16), GTItems.FIELD_GENERATOR_UXV.asStack(4),
                        GTNAGodforgeComponents.INSANELY_ULTIMATE_BATTERY.asStack(),
                        GTNAGodforgeComponents.TESSERACT.asStack(64),
                        GTNANanoForge.TRANSCENDENT_METAL_NANITES.asStack(16),
                        part(TagPrefix.plateDense, GTMaterials.Flerovium, 64),
                        part(TagPrefix.plateDense, MetastableOganesson, 32), GTNABEC.SENSOR_ARRAY[0].asStack(32),
                        GTNABEC.FIELD_MANIPULATOR[0].asStack(32) },
                nanites(1, 2, 4, 4, 4, 3, 2, 4, 1, 1, 2, 3),
                new FluidStack[] { CondensateType.SpaceTime.getEntangled(192 * INGOTS),
                        CondensateType.DimensionallyShiftedSuperfluid.getEntangled(10_000),
                        CondensateType.Space.getEntangled(32 * INGOTS) },
                600 * SECONDS, RECIPE_UMV);
    }

    // ---- 7. addGodforgeRecipes

    private static void godforge(Consumer<FinishedRecipe> provider) {
        var confinement = GTNAGodforgeContent.MAGNETIC_CONFINEMENT_CASING;
        var boundless = GTNAGodforgeContent.BOUNDLESS_STRUCTURE_CASING;
        bec(provider, "magnetic_confinement_casing", confinement.asStack(12),
                new Object[] { part(TagPrefix.frameGt, TranscendentMetal, 12),
                        part(TagPrefix.block, MagnetoResonatic, 16), part(TagPrefix.plateDense, TengamAttuned, 32),
                        part(TagPrefix.plate, Creon, 16), part(TagPrefix.screw, Hypogen, 8),
                        part(TagPrefix.screw, SixPhasedCopper, 8),
                        GTNAGodforgeComponents.SUPERCONDUCTOR_COMPOSITE.asStack(), GTItems.EMITTER_UIV.asStack(2),
                        GTNAGodforgeComponents.ELECTROMAGNET_TENGAM.asStack() },
                nanites(1, 2, 1, 1, 1, 1, 2, 3, 4),
                new FluidStack[] { CondensateType.Hypogen.getEntangled(4 * INGOTS),
                        CondensateType.CelestialTungsten.getEntangled(32 * INGOTS) },
                1800 * SECONDS, RECIPE_UIV);
        bec(provider, "boundless_structure_casing", boundless.asStack(2),
                new Object[] { part(TagPrefix.frameGt, Mellion, 24), part(TagPrefix.frameGt, SixPhasedCopper, 24),
                        part(TagPrefix.frameGt, TranscendentMetal, 12), part(TagPrefix.frameGt, AstralTitanium, 12),
                        part(TagPrefix.plate, Creon, 9),
                        GTNAGodforgeComponents.STABLE_BOSON_CONTAINMENT_UNIT.asStack(2),
                        GTItems.FIELD_GENERATOR_UEV.asStack(3), stack(GTItems.GRAVI_STAR.get(), 6) },
                nanites(1, 1, 1, 1, 2, 2, 4, 3),
                new FluidStack[] { CondensateType.Hypogen.getEntangled(4 * INGOTS),
                        CondensateType.Neutronium.getEntangled(32 * INGOTS) },
                300 * SECONDS, RECIPE_UIV);
        bec(provider, "guidance_casing", GTNAGodforgeContent.GUIDANCE_CASING.asStack(2),
                new Object[] { boundless.asStack(2), stack(GTItems.ULTIMATE_BATTERY.get(), 2),
                        GTNABlocks.COSMIC_FABRIC_MANIPULATOR.asStack(2), GTItems.FIELD_GENERATOR_UEV.asStack(3),
                        GTItems.EMITTER_UIV.asStack(4), part(TagPrefix.plate, Creon, 9),
                        part(TagPrefix.gear, Creon, 12), part(TagPrefix.gearSmall, Mellion, 12) },
                nanites(1, 2, 2, 4, 3, 1, 1, 1),
                new FluidStack[] { CondensateType.Hypogen.getEntangled(4 * INGOTS),
                        CondensateType.CosmicNeutronium.getEntangled(32 * INGOTS) },
                300 * SECONDS, RECIPE_UIV);
        bec(provider, "gravitational_lens", GTNAGodforgeContent.GRAVITATIONAL_LENS.asStack(2),
                new Object[] { GTNABlocks.QUANTUM_GLASS.asStack(12),
                        stack(com.gregtechceu.gtceu.common.data.GTBlocks.CASING_LAMINATED_GLASS.get(), 12),
                        GTNABlocks.FORCE_FIELD_GLASS.asStack(12),
                        GTNAGodforgeComponents.STABLE_BOSON_CONTAINMENT_UNIT.asStack(6),
                        part(TagPrefix.lens, MagnetoResonatic, 9), part(TagPrefix.lens, Orundum, 9),
                        part(TagPrefix.lens, GTMaterials.NetherStar, 9), part(TagPrefix.lens, MagnetoResonatic, 9),
                        part(TagPrefix.plate, Rhugnor, 24), part(TagPrefix.rodLong, Creon, 33),
                        part(TagPrefix.rodLong, Mellion, 9), part(TagPrefix.rodLong, SixPhasedCopper, 9),
                        part(GTNATagPrefix.superdensePlate, AdvancedNitinol, 24) },
                nanites(3, 3, 2, 4, 1, 1, 1, 1, 1, 1, 1, 1, 2),
                new FluidStack[] { CondensateType.ChromaticGlass.getEntangled(243 * INGOTS) }, 300 * SECONDS,
                RECIPE_UIV);
        var coil = GTNABlocks.FIELD_RESTRICTION_COIL_T3;
        var anomaly = GTNAGodforgeComponents.GRAVITON_ANOMALY;
        var lens = GTNAItems.LASER_LENS_SPECIAL;
        bec(provider, "remote_graviton_flow_modulator", GTNAGodforgeContent.REMOTE_GRAVITON_FLOW_MODULATOR.asStack(3),
                new Object[] { confinement.asStack(3), coil.asStack(1), part(TagPrefix.plate, Creon, 16),
                        part(TagPrefix.gearSmall, Mellion, 8), anomaly.asStack(2), lens.asStack(4),
                        GTItems.EMITTER_UIV.asStack(4), circuit(CustomTags.UEV_CIRCUITS, 16),
                        GTNANanoForge.SILVER_NANITES.asStack(2), part(TagPrefix.plate, SuperconductorUIVBase, 32) },
                nanites(1, 2, 1, 1, 1, 1, 3, 4, 2, 3),
                new FluidStack[] { CondensateType.ChromaticGlass.getEntangled(32 * INGOTS),
                        CondensateType.Infinity.getEntangled(32 * INGOTS) },
                450 * SECONDS, RECIPE_UIV);
        bec(provider, "medial_graviton_flow_modulator", GTNAGodforgeContent.MEDIAL_GRAVITON_FLOW_MODULATOR.asStack(),
                new Object[] { confinement.asStack(1), coil.asStack(2), part(TagPrefix.plateDense, Creon, 8),
                        part(TagPrefix.gear, Mellion, 4), part(TagPrefix.frameGt, SuperconductorUIVBase, 32),
                        anomaly.asStack(4), lens.asStack(8), GTItems.EMITTER_UXV.asStack(4),
                        circuit(CustomTags.UXV_CIRCUITS, 8), GTNANanoForge.SILVER_NANITES.asStack(2),
                        GTNANanoForge.GOLD_NANITES.asStack(2), GTNABEC.WAVEGUIDE[0].asStack(4) },
                nanites(1, 1, 1, 1, 1, 2, 3, 3, 3, 2, 2, 4),
                new FluidStack[] { CondensateType.ChromaticGlass.getEntangled(64 * INGOTS),
                        CondensateType.Infinity.getEntangled(32 * INGOTS),
                        CondensateType.TranscendentMetal.getEntangled(32 * INGOTS) },
                300 * SECONDS, RECIPE_UMV);
        bec(provider, "central_graviton_flow_modulator", GTNAGodforgeContent.CENTRAL_GRAVITON_FLOW_MODULATOR.asStack(),
                new Object[] { confinement.asStack(1), coil.asStack(8), part(GTNATagPrefix.superdensePlate, Creon, 8),
                        part(TagPrefix.gear, Mellion, 64), GTNABlocks.COSMIC_FABRIC_MANIPULATOR.asStack(32),
                        anomaly.asStack(8), lens.asStack(8), circuit(CustomTags.MAX_CIRCUITS, 4),
                        GTItems.EMITTER_OpV.asStack(4), GTNABEC.WAVEGUIDE[1].asStack(64),
                        GTNABEC.ENERGY_CONDUIT[1].asStack(64), GTNABEC.ENERGY_CONDUIT[2].asStack(8),
                        GTNANanoForge.SILVER_NANITES.asStack(8), GTNANanoForge.GOLD_NANITES.asStack(8),
                        GTNANanoForge.SIX_PHASED_COPPER_NANITES.asStack(8),
                        GTNANanoForge.UNIVERSIUM_NANITES.asStack(8) },
                nanites(1, 3, 2, 2, 4, 2, 1, 7, 8, 6, 6, 9, 2, 3, 5, 8),
                new FluidStack[] { CondensateType.ChromaticGlass.getEntangled(256 * INGOTS),
                        CondensateType.Infinity.getEntangled(32 * INGOTS),
                        CondensateType.BoundlessCosmicSolder.getEntangled(20_000),
                        CondensateType.Eternity.getEntangled(128 * INGOTS) },
                300 * SECONDS, RECIPE_UXV);
        bec(provider, "harmonic_phonon_transmission_conduit",
                GTNAGodforgeContent.HARMONIC_PHONON_TRANSMISSION_CONDUIT.asStack(2),
                new Object[] { part(TagPrefix.frameGt, TranscendentMetal, 2), part(TagPrefix.rodLong, Creon, 18),
                        tiered(GTMachines.QUANTUM_TANK, UHV).asStack(2), GTNAGodforgeComponents.TESSERACT.asStack(12),
                        GTNAGodforgeComponents.RELATIVISTIC_HEAT_CAPACITOR.asStack(6),
                        GTNAGodforgeComponents.THERMAL_SUPERCONDUCTOR.asStack(9),
                        GTItems.FIELD_GENERATOR_UEV.asStack(6), part(TagPrefix.bolt, SixPhasedCopper, 36) },
                nanites(1, 1, 2, 3, 4, 3, 2, 1),
                new FluidStack[] { CondensateType.Hypogen.getEntangled(32 * INGOTS),
                        CondensateType.PhononMedium.getEntangled(2_000),
                        CondensateType.CelestialTungsten.getEntangled(16 * INGOTS) },
                300 * SECONDS, RECIPE_UXV);
    }

    // ---- 8. runLateRecipes: Singularity Shielding Casing (replaces the provisional G-0199 assembly line)

    private static void shieldingCasing(Consumer<FinishedRecipe> provider) {
        bec(provider, "singularity_shielding_casing", GTNAGodforgeContent.SINGULARITY_SHIELDING_CASING.asStack(6),
                new Object[] { part(TagPrefix.frameGt, SixPhasedCopper, 4),
                        part(GTNATagPrefix.superdensePlate, Bedrockium, 256), part(TagPrefix.plate, Quantum, 16),
                        part(TagPrefix.frameGt, Infinity, 4),
                        part(GTNATagPrefix.superdensePlate, GTMaterials.Neutronium,
                                2),
                        stack(GTItems.GRAVI_STAR.get(), 8), part(TagPrefix.rodLong, SuperconductorUIVBase, 8),
                        part(TagPrefix.plate, Creon, 16), part(TagPrefix.plate, Mellion, 16),
                        part(TagPrefix.rodLong, SuperconductorUIVBase, 8), stack(GTItems.GRAVI_STAR.get(), 16),
                        part(GTNATagPrefix.superdensePlate, TranscendentMetal, 2),
                        part(TagPrefix.frameGt, GTMaterials.Tritanium, 4), part(TagPrefix.plate, ExoHalkonite, 16),
                        part(GTNATagPrefix.superdensePlate, GTNAMaterials.CosmicNeutronium, 2),
                        part(TagPrefix.frameGt, GTMaterials.Naquadria, 4) },
                nanites(1, 2, 1, 1, 2, 4, 3, 1, 1, 3, 4, 2, 1, 1, 2, 1),
                new FluidStack[] { CondensateType.Hypogen.getEntangled(4 * INGOTS),
                        CondensateType.Infinity.getEntangled(2 * STACKS),
                        CondensateType.CelestialTungsten.getEntangled(32 * STACKS),
                        CondensateType.Neutronium.getEntangled(32 * STACKS) },
                300 * SECONDS, RECIPE_UMV);
    }

    // ---- 9. addEyeOfHarmonyRecipes (an extra route next to GTNA's own EOH progression)

    private static final int[] BOLT_TIER = { 1, 2, 2, 2, 3, 3, 3, 4, 4 };
    private static final int[] BOLT_POS = { 0, 0, 1, 2, 0, 1, 2, 0, 1 };
    private static final int[] EOH_TIMES = { 2_000_000, 3_000_000, 4_000_000, 5_000_000, 100_000, 120_000, 140_000,
            160_000, 180_000 };

    private static Material tierMat(int t) {
        return switch (t) {
            case 0 -> sub("Netherite");
            case 1 -> sub("ProtoHalkonite");
            case 2 -> SixPhasedCopper;
            case 3 -> TranscendentMetal;
            case 4 -> Mellion;
            case 5 -> Creon;
            case 6 -> GTNAMaterials.SpaceTime;
            case 7 -> sub("Hexanite");
            default -> Eternity;
        };
    }

    private static FluidStack cosmicSolder(int tier) {
        return tier == 0 ? CondensateType.TranscendentMetal.getEntangled(69 * INGOTS) :
                CondensateType.BoundlessCosmicSolder.getEntangled(10_000 * tier);
    }

    private static void eyeOfHarmony(Consumer<FinishedRecipe> provider) {
        var shielding = GTNAGodforgeContent.SINGULARITY_SHIELDING_CASING;
        var temporal = GTNAEyeOfHarmonyContent.TEMPORAL_CASING;
        var spatial = GTNAEyeOfHarmonyContent.SPATIAL_CASING;
        var boundary = GTNAEyeOfHarmonyContent.BOUNDARY_CASING;
        Material hexanite = sub("Hexanite");
        int casingTime = 40_000 * SECONDS;
        Object[] casingCommon = { shielding.asStack(32), part(TagPrefix.plateDense, sub("ProtoHalkonite"), 32),
                part(TagPrefix.block, hexanite, 8), GTNANanoForge.NEUTRONIUM_NANITES.asStack(48),
                part(GTNATagPrefix.superdensePlate, Bedrockium, 2),
                part(GTNATagPrefix.superdensePlate, GTNAMaterials.CosmicNeutronium, 2),
                part(GTNATagPrefix.superdensePlate, Shirabon, 2), part(GTNATagPrefix.superdensePlate, Infinity, 2),
                GTItems.COVER_SOLAR_PANEL_UV.asStack() };
        List<Object> temporalIn = new ArrayList<>(List.of(casingCommon));
        temporalIn.addAll(List.of(tiered(GTMachines.WORLD_ACCELERATOR, UV).asStack(4),
                part(TagPrefix.wireGtSingle, GTMaterials.RutheniumTriniumAmericiumNeutronate, 64),
                GTNAGodforgeComponents.TESSERACT.asStack(2)));
        bec(provider, "reinforced_temporal_structure_casing", temporal.asStack(4), temporalIn.toArray(),
                nanites(4, 1, 1, 2, 1, 1, 4, 1, 1, 1, 1, 2),
                new FluidStack[] { CondensateType.Neutronium.getEntangled(512 * INGOTS),
                        CondensateType.CosmicNeutronium.getEntangled(512 * INGOTS),
                        CondensateType.Bedrockium.getEntangled(256 * INGOTS),
                        CondensateType.Time.getEntangled(10 * INGOTS) },
                casingTime, RECIPE_UMV);
        List<Object> spatialIn = new ArrayList<>(List.of(casingCommon));
        spatialIn.addAll(List.of(tiered(GTMachines.QUANTUM_CHEST, IV).asStack(),
                part(TagPrefix.wireGtSingle, GTMaterials.RutheniumTriniumAmericiumNeutronate, 64),
                GTNAGodforgeComponents.TESSERACT.asStack(2)));
        bec(provider, "reinforced_spatial_structure_casing", spatial.asStack(4), spatialIn.toArray(),
                nanites(4, 1, 1, 2, 1, 1, 4, 1, 1, 1, 1, 2),
                new FluidStack[] { CondensateType.Neutronium.getEntangled(512 * INGOTS),
                        CondensateType.CosmicNeutronium.getEntangled(512 * INGOTS),
                        CondensateType.Bedrockium.getEntangled(256 * INGOTS),
                        CondensateType.Space.getEntangled(10 * INGOTS) },
                casingTime, RECIPE_UMV);
        bec(provider, "infinite_spacetime_boundary_casing", boundary.asStack(1),
                new Object[] { GTMultiMachines.POWER_SUBSTATION.asStack(), GTItems.COVER_SOLAR_PANEL_UV.asStack(),
                        GTNABlocks.NEXUS_CAPACITOR_UXV.asStack(), part(TagPrefix.wireGtHex, SuperconductorUMV, 4),
                        GTMultiMachines.ACTIVE_TRANSFORMER.asStack(16),
                        tiered(GTMachines.ENERGY_INPUT_HATCH_16A, UXV).asStack(4),
                        tiered(GTMachines.LASER_INPUT_HATCH_4096, UXV).asStack(),
                        stack(GTItems.HIGHLY_ADVANCED_SOC.get(), 64), part(TagPrefix.plate, MetastableOganesson, 6),
                        part(TagPrefix.plate, GTMaterials.Duranium, 6), part(TagPrefix.plate, GTMaterials.Tritanium, 6),
                        part(TagPrefix.plate, GTMaterials.Trinium, 6), part(TagPrefix.screw, MetastableOganesson, 6),
                        part(TagPrefix.screw, GTMaterials.Duranium, 6), part(TagPrefix.screw, GTMaterials.Tritanium, 6),
                        part(TagPrefix.screw, GTMaterials.Trinium, 6) },
                nanites(4, 1, 2, 1, 1, 3, 4, 3, 1, 1, 1, 1, 1, 1, 1, 1),
                new FluidStack[] { CondensateType.Neutronium.getEntangled(1024 * INGOTS),
                        CondensateType.CosmicNeutronium.getEntangled(1024 * INGOTS),
                        CondensateType.Bedrockium.getEntangled(256 * INGOTS),
                        CondensateType.SpaceTime.getEntangled(128 * INGOTS) },
                casingTime, RECIPE_UMV);

        // Time Acceleration Field Generators T0-T8
        for (int t = 0; t < 9; t++) {
            int tp1 = t + 1;
            Object[] inputs = { temporal.asStack(1), GTNAGodforgeContent.MEDIAL_GRAVITON_FLOW_MODULATOR.asStack(),
                    stack(GTItems.COVER_SOLAR_PANEL_UV.get(), tp1),
                    tiered(GTMachines.WORLD_ACCELERATOR, UV).asStack(4 * tp1),
                    circuit(CustomTags.OpV_CIRCUITS, tp1), part(TagPrefix.gemExquisite, GTMaterials.Ruby, 64),
                    part(TagPrefix.gemExquisite, GTMaterials.Emerald, 64),
                    part(TagPrefix.gemExquisite, GTMaterials.Sapphire, 64), GTNABEC.ENERGY_CONDUIT[0].asStack(tp1),
                    GTNABEC.WAVE_FOCUS[BOLT_TIER[t] - 1].asStack(new int[] { 1, 4, 16 }[BOLT_POS[t]]),
                    GTNABEC.ELECTROGRAVITIC_VALVE[0].asStack(2 * tp1), GTNABEC.WAVEGUIDE[0].asStack(tp1),
                    stack(GTItems.ENERGY_CLUSTER.get(), tp1), part(TagPrefix.ring, hexanite, 4 * tp1),
                    part(TagPrefix.gearSmall, hexanite, 4 * tp1), part(TagPrefix.gear, tierMat(t), tp1) };
            bec(provider, "time_acceleration_field_generator_" + t,
                    GTNAEyeOfHarmonyContent.ACCELERATION_FIELDS[t].asStack(), inputs,
                    shifted(BOLT_TIER[t] - 1, 2, 2, 2, 2, 2, 1, 1, 1, 3, 4, 3, 3, 4, 1, 1, 1),
                    new FluidStack[] { cosmicSolder(t), CondensateType.Time.getEntangled(10 * tp1 * INGOTS),
                            CondensateType.SpaceTime.getEntangled(10 * INGOTS),
                            CondensateType.CosmicNeutronium.getEntangled(20 * tp1 * INGOTS) },
                    EOH_TIMES[t], RECIPE_UMV);
        }
        // Spacetime Compression Field Generators T0-T8
        for (int t = 0; t < 9; t++) {
            int tp1 = t + 1;
            Object[] inputs = { spatial.asStack(1), GTMultiMachines.IMPLOSION_COMPRESSOR.asStack(4),
                    modItem("ae2:item_storage_cell_256k", 1), modItem("ae2:fluid_storage_cell_256k", 1),
                    GTNABlocks.COSMIC_FABRIC_MANIPULATOR.asStack(new int[] { 1, 2, 4 }[t / 3] * (t % 3 + 1)),
                    GTNABEC.SHIELDING[0].asStack(4 * tp1),
                    GTNABEC.RESONANCE_CHAMBER[BOLT_TIER[t] - 1].asStack(new int[] { 1, 4, 16 }[BOLT_POS[t]]),
                    circuit(CustomTags.OpV_CIRCUITS, tp1), shielding.asStack(4 * tp1),
                    part(TagPrefix.frameGt, hexanite, tp1), part(TagPrefix.rodLong, hexanite, 2 * tp1),
                    part(TagPrefix.plateDense, tierMat(t), tp1), part(GTNATagPrefix.superdensePlate, hexanite, tp1),
                    part(GTNATagPrefix.superdensePlate, GTNAMaterials.CosmicNeutronium, tp1),
                    part(GTNATagPrefix.superdensePlate, Infinity, tp1),
                    part(GTNATagPrefix.superdensePlate, TranscendentMetal, tp1) };
            bec(provider, "spacetime_compression_field_generator_" + t,
                    GTNAEyeOfHarmonyContent.COMPRESSION_FIELDS[t].asStack(), inputs,
                    shifted(BOLT_TIER[t] - 1, 3, 3, 2, 4, 2, 2, 4, 3, 2, 2, 1, 1, 1, 1, 1, 1),
                    new FluidStack[] { cosmicSolder(t), CondensateType.Space.getEntangled(10 * tp1 * INGOTS),
                            CondensateType.SpaceTime.getEntangled(10 * INGOTS),
                            CondensateType.Neutronium.getEntangled(20 * tp1 * INGOTS) },
                    EOH_TIMES[t], RECIPE_UMV);
        }
        // Stabilisation Field Generators T0-T8
        int[] sensorTier = { 1, 1, 2, 2, 2, 3, 3, 3, 4 };
        int[] sensorQty = { 1, 1, 1, 1, 4, 1, 1, 4, 1 };
        int[] manipulatorQty = { 1, 2, 8 };
        for (int t = 0; t < 9; t++) {
            int tp1 = t + 1;
            Object[] inputs = { GTNAEyeOfHarmonyContent.ACCELERATION_FIELDS[t].asStack(),
                    GTNAEyeOfHarmonyContent.COMPRESSION_FIELDS[t].asStack(), boundary.asStack(1),
                    circuit(CustomTags.OpV_CIRCUITS, tp1), part(TagPrefix.frameGt, GTMaterials.Neutronium, 4 * tp1),
                    part(TagPrefix.frameGt, SuperconductorUIVBase, 4 * tp1),
                    part(TagPrefix.frameGt, SuperconductorUIVBase, 4 * tp1),
                    part(TagPrefix.frameGt, SuperconductorUMVBase, 4 * tp1),
                    part(TagPrefix.wireGtQuadruple, GTMaterials.RutheniumTriniumAmericiumNeutronate, 2 * tp1),
                    part(TagPrefix.wireGtQuadruple, SuperconductorUIV, 2 * tp1),
                    part(TagPrefix.wireGtQuadruple, SuperconductorUIV, 2 * tp1),
                    part(TagPrefix.wireGtQuadruple, SuperconductorUMV, 2 * tp1),
                    GTNABEC.SENSOR_ARRAY[sensorTier[t] - 1].asStack(sensorQty[t]),
                    GTNABEC.FIELD_MANIPULATOR[BOLT_TIER[t] - 1].asStack(manipulatorQty[BOLT_POS[t]]),
                    part(TagPrefix.screw, hexanite, 4 * tp1), part(TagPrefix.rodLong, tierMat(t), 4 * tp1) };
            bec(provider, "stabilisation_field_generator_" + t,
                    GTNAEyeOfHarmonyContent.STABILISATION_FIELDS[t].asStack(), inputs,
                    shifted(BOLT_TIER[t] - 1, 3, 3, 3, 2, 1, 1, 1, 1, 2, 2, 2, 2, 4, 4, 1, 1),
                    new FluidStack[] { cosmicSolder(t), CondensateType.Time.getEntangled(10 * tp1 * INGOTS),
                            CondensateType.Space.getEntangled(10 * tp1 * INGOTS),
                            CondensateType.SpaceTime.getEntangled(10 * INGOTS) },
                    EOH_TIMES[t], RECIPE_UMV);
        }
        // Astral Array Fabricator
        bec(provider, "astral_array_fabricator", GTNAEyeOfHarmonyContent.ASTRAL_ARRAY_FABRICATOR.asStack(),
                new Object[] { GTNAEyeOfHarmonyContent.COMPRESSION_FIELDS[8].asStack(64),
                        GTNAEyeOfHarmonyContent.COMPRESSION_FIELDS[8].asStack(64),
                        GTNAEyeOfHarmonyContent.COMPRESSION_FIELDS[8].asStack(10),
                        GTNAEyeOfHarmonyContent.STABILISATION_FIELDS[8].asStack(48),
                        GTNAEyeOfHarmonyContent.ACCELERATION_FIELDS[8].asStack(64),
                        GTNAEyeOfHarmonyContent.ACCELERATION_FIELDS[8].asStack(64),
                        GTNAEyeOfHarmonyContent.ACCELERATION_FIELDS[8].asStack(40), boundary.asStack(32),
                        temporal.asStack(64), spatial.asStack(64), GTNANanoForge.WHITE_DWARF_MATTER_NANITES.asStack(2),
                        GTNANanoForge.BLACK_DWARF_MATTER_NANITES.asStack(2),
                        GTNABEC.TRANSDIMENSIONAL_ALIGNMENT_MATRIX.asStack(), GTNABEC.SHIELDING[2].asStack(16),
                        GTNABEC.ELECTROGRAVITIC_VALVE[2].asStack(16), GTNABEC.FIELD_MANIPULATOR[3].asStack(32) },
                nanites(6, 6, 6, 8, 6, 6, 6, 3, 1, 1, 2, 9, 10, 4, 5, 7),
                new FluidStack[] { CondensateType.BoundlessCosmicSolder.getEntangled(1_024_000),
                        CondensateType.Space.getEntangled(3_640 * INGOTS),
                        CondensateType.SpaceTime.getEntangled(3_640 * INGOTS),
                        CondensateType.Eternity.getEntangled(1_820 * INGOTS) },
                7200 * SECONDS, RECIPE_UXV);
    }

    // ---- 10. BECMetaMaterialRecipes

    private static void metamaterials(Consumer<FinishedRecipe> provider) {
        int[] baseAmounts = { 1, 2, 4, 8 };
        int baseDuration = 300 * SECONDS;
        Material[] other3 = { sub("ProtoHalkonite"), sub("Hexanite"),
                GTNAMaterials.MagnetohydrodynamicallyConstrainedStarMatter };
        Material[] black3 = { Tairitsu, TranscendentMetal, GTNAMaterials.BlackDwarfMatter };
        Material[] gray3 = { Churitsu, GTNAMaterials.SpaceTime, Eternity };
        Material[] white3 = { Shijima, GTNAMaterials.WhiteDwarfMatter, GTNAMaterials.MagMatter };
        Material[] black4 = { Tairitsu, Hypogen, Shirabon, GTNAMaterials.SpaceTime };
        Material[] gray4 = { Churitsu, GTNAMaterials.WhiteDwarfMatter, GTNAMaterials.BlackDwarfMatter,
                GTNAMaterials.MagnetohydrodynamicallyConstrainedStarMatter };
        Material[] white4 = { Shijima, sub("ProtoHalkonite"), sub("Hexanite"), Eternity };
        long[] euts3 = { RECIPE_UIV, RECIPE_UMV, RECIPE_UXV };
        long[] euts4 = { RECIPE_UEV, RECIPE_UIV, RECIPE_UMV, RECIPE_UXV };

        for (int t = 0; t < 3; t++) {
            int[] n3 = { 4 + 2 * t, 1 + 2 * t, 1 + 2 * t, 3 + 2 * t, 1 + 2 * t };
            int[] amounts = { 2, 4, 8 };
            bec(provider, "metamaterial_shielding_" + (t + 1), GTNABEC.SHIELDING[t].asStack(),
                    new Object[] { part(TagPrefix.plateDense, Bedrockium, baseAmounts[t + 1]),
                            part(TagPrefix.foil, other3[t], 4), part(TagPrefix.plate, black3[t], 1),
                            part(TagPrefix.screw, gray3[t], 8), part(TagPrefix.bolt, white3[t], 8) },
                    nanites(n3), new FluidStack[] { CondensateType.ChromaticGlass.getEntangled(amounts[t] * 144),
                            CondensateType.TranscendentMetal.getEntangled(amounts[t] * 144) },
                    baseDuration, euts3[t]);

            Object coil = t == 0 ? part(TagPrefix.wireGtQuadruple, SuperconductorUIV, 1) :
                    t == 1 ? part(TagPrefix.wireGtQuadruple, SuperconductorUMV, 1) :
                            part(TagPrefix.wireGtOctal, SuperconductorUMV, 1);
            int[] chromaticWg = { 4, 6, 8 }, tmWg = { 0, 2, 4 };
            bec(provider, "metamaterial_waveguide_" + (t + 1), GTNABEC.WAVEGUIDE[t].asStack(),
                    new Object[] { coil, part(TagPrefix.rodLong, other3[t], 1), part(TagPrefix.wireFine, black3[t], 8),
                            part(TagPrefix.foil, gray3[t], 4), part(TagPrefix.screw, white3[t], 8) },
                    nanites(n3),
                    t == 0 ? new FluidStack[] { CondensateType.ChromaticGlass.getEntangled(chromaticWg[t] * 144) } :
                            new FluidStack[] { CondensateType.ChromaticGlass.getEntangled(chromaticWg[t] * 144),
                                    CondensateType.TranscendentMetal.getEntangled(tmWg[t] * 144) },
                    baseDuration, euts3[t]);

            Object superconductor = t == 0 ? part(TagPrefix.wireGtQuadruple, SuperconductorUIV, 1) :
                    t == 1 ? part(TagPrefix.wireGtQuadruple, SuperconductorUMV, 1) :
                            GTNAGodforgeComponents.THERMAL_SUPERCONDUCTOR.asStack();
            int[] chromaticEc = { 4, 8, 16 };
            bec(provider, "metamaterial_energy_conduit_" + (t + 1), GTNABEC.ENERGY_CONDUIT[t].asStack(),
                    new Object[] { superconductor, part(TagPrefix.rod, other3[t], 2),
                            part(TagPrefix.foil, black3[t], 4),
                            part(TagPrefix.plate, gray3[t], 2), part(TagPrefix.screw, white3[t], 8) },
                    nanites(n3),
                    t == 0 ? new FluidStack[] { CondensateType.ChromaticGlass.getEntangled(chromaticEc[t] * 144) } :
                            new FluidStack[] { CondensateType.ChromaticGlass.getEntangled(chromaticEc[t] * 144),
                                    CondensateType.TranscendentMetal.getEntangled(tmWg[t] * 144) },
                    baseDuration, euts3[t]);

            int[] dss = { 1, 2, 4 };
            bec(provider, "metamaterial_electrogravitic_valve_" + (t + 1), GTNABEC.ELECTROGRAVITIC_VALVE[t].asStack(),
                    new Object[] { stack(GTItems.GRAVI_STAR.get(), baseAmounts[t + 1]),
                            part(TagPrefix.ring, other3[t], 2), part(TagPrefix.foil, black3[t], 4),
                            part(TagPrefix.gearSmall, gray3[t], 1), part(TagPrefix.round, white3[t], 9) },
                    nanites(n3), new FluidStack[] { CondensateType.ChromaticGlass.getEntangled(chromaticEc[t] * 144),
                            CondensateType.DimensionallyShiftedSuperfluid.getEntangled(dss[t] * 1000) },
                    baseDuration, euts3[t]);
        }

        int[] chromatic4 = { 8, 12, 16, 24 }, infinity4 = { 4, 6, 8, 12 }, solder4 = { 1, 2, 3, 4 };
        var emitters = new ItemStack[] { GTItems.EMITTER_UHV.asStack(2), GTItems.EMITTER_UEV.asStack(2),
                GTItems.EMITTER_UIV.asStack(2), GTItems.EMITTER_UXV.asStack(2) };
        var sensors = new ItemStack[] { GTItems.SENSOR_UHV.asStack(2), GTItems.SENSOR_UEV.asStack(2),
                GTItems.SENSOR_UIV.asStack(2), GTItems.SENSOR_UXV.asStack(2) };
        var fieldGens = new ItemStack[] { GTItems.FIELD_GENERATOR_UHV.asStack(), GTItems.FIELD_GENERATOR_UEV.asStack(),
                GTItems.FIELD_GENERATOR_UIV.asStack(), GTItems.FIELD_GENERATOR_UXV.asStack() };
        for (int t = 0; t < 4; t++) {
            int[] n4 = { 4 + t, 1 + t, 2 + t, 1 + t };
            FluidStack[] c4 = t == 0 ?
                    new FluidStack[] { CondensateType.ChromaticGlass.getEntangled(chromatic4[t] * 144),
                            CondensateType.Infinity.getEntangled(infinity4[t] * 144),
                            CondensateType.TranscendentMetal.getEntangled(2 * 144) } :
                    new FluidStack[] { CondensateType.ChromaticGlass.getEntangled(chromatic4[t] * 144),
                            CondensateType.Infinity.getEntangled(infinity4[t] * 144),
                            CondensateType.BoundlessCosmicSolder.getEntangled(solder4[t] * 1000) };
            bec(provider, "metamaterial_wave_focus_" + (t + 1), GTNABEC.WAVE_FOCUS[t].asStack(),
                    new Object[] { GTNAGodforgeContent.GRAVITATIONAL_LENS.asStack(), part(TagPrefix.ring, black4[t], 2),
                            part(TagPrefix.ring, gray4[t], 1), part(TagPrefix.screw, white4[t], 2) },
                    nanites(n4), c4, baseDuration, euts4[t]);
            bec(provider, "metamaterial_resonance_chamber_" + (t + 1), GTNABEC.RESONANCE_CHAMBER[t].asStack(),
                    new Object[] { emitters[t], part(TagPrefix.rod, black4[t], 2), part(TagPrefix.foil, gray4[t], 1),
                            part(TagPrefix.plate, white4[t], 1) },
                    nanites(n4), c4, baseDuration, euts4[t]);
            bec(provider, "metamaterial_sensor_array_" + (t + 1), GTNABEC.SENSOR_ARRAY[t].asStack(),
                    new Object[] { sensors[t], part(TagPrefix.plate, black4[t], 2), part(TagPrefix.plate, gray4[t], 1),
                            part(TagPrefix.bolt, white4[t], 16) },
                    nanites(n4), c4, baseDuration, euts4[t]);
            bec(provider, "metamaterial_field_manipulator_" + (t + 1), GTNABEC.FIELD_MANIPULATOR[t].asStack(),
                    new Object[] { fieldGens[t], part(TagPrefix.rodLong, black4[t], 2),
                            part(TagPrefix.ring, gray4[t], 1),
                            part(TagPrefix.plateDouble, white4[t], 2) },
                    nanites(n4), c4, baseDuration, euts4[t]);
        }
    }
}
