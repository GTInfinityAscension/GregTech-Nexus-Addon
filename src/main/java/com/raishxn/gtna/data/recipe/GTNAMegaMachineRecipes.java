package com.raishxn.gtna.data.recipe;

import com.gregtechceu.gtceu.api.GTValues;
import com.gregtechceu.gtceu.api.data.chemical.material.stack.MaterialEntry;
import com.gregtechceu.gtceu.api.data.tag.TagPrefix;
import com.gregtechceu.gtceu.common.data.GCYMBlocks;
import com.gregtechceu.gtceu.common.data.GTBlocks;
import com.gregtechceu.gtceu.common.data.GTItems;
import com.gregtechceu.gtceu.common.data.GTMachines;
import com.gregtechceu.gtceu.common.data.GTMaterials;
import com.gregtechceu.gtceu.common.data.GTRecipeTypes;
import com.gregtechceu.gtceu.common.data.machines.GCYMMachines;
import com.gregtechceu.gtceu.common.data.machines.GTMultiMachines;
import com.gregtechceu.gtceu.data.recipe.CustomTags;
import com.gregtechceu.gtceu.data.recipe.VanillaRecipeHelper;

import net.minecraft.data.recipes.FinishedRecipe;

import com.raishxn.gtna.GTNACORE;
import com.raishxn.gtna.common.data.GTNABlocks;
import com.raishxn.gtna.common.data.GTNAMachines3;
import com.raishxn.gtna.common.data.GTNAMaterials;
import com.raishxn.gtna.common.data.GTNAMegaMachines;
import com.raishxn.gtna.common.data.GTNAPlasmaForge;

import java.util.function.Consumer;

/**
 * Controller and block recipes of the GTOCore mega multiblocks (G-0204). GTO recipes are kept where every input exists;
 * GTO-only inputs are swapped for same-tier GTCEu/GTNA ones (noted inline). Defaults only: the pack retunes them.
 */
public final class GTNAMegaMachineRecipes {

    private GTNAMegaMachineRecipes() {}

    public static void register(Consumer<FinishedRecipe> provider) {
        // ---- Blocks ----
        GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder(GTNACORE.id("mega/oil_gas_transportation_pipe_casing"))
                .inputItems(TagPrefix.frameGt, GTMaterials.HSSG)
                .inputItems(TagPrefix.pipeNormalFluid, GTMaterials.NiobiumTitanium, 4)
                .inputItems(TagPrefix.plate, GTMaterials.RhodiumPlatedPalladium, 4)
                .inputItems(TagPrefix.plate, GTNAMaterials.HastelloyN75, 4)
                .inputFluids(GTNAMaterials.MarM200Steel.getFluid(576))
                .outputItems(GTNABlocks.OIL_GAS_TRANSPORTATION_PIPE_CASING.asStack())
                .EUt(480).duration(200).save(provider);
        // GTO Calcium Oxide Ceramic flakes -> Quicklime (CaO) dust.
        GTRecipeTypes.ASSEMBLER_RECIPES
                .recipeBuilder(GTNACORE.id("mega/calcium_oxide_ceramic_anti_metal_corrosion_mechanical_block"))
                .inputItems(TagPrefix.frameGt, GTMaterials.StainlessSteel)
                .inputItems(TagPrefix.plate, GTMaterials.VanadiumSteel, 2)
                .inputItems(TagPrefix.dust, GTMaterials.Quicklime, 16)
                .outputItems(GTNABlocks.CALCIUM_OXIDE_CERAMIC_ANTI_METAL_CORROSION_MECHANICAL_BLOCK.asStack())
                .EUt(30).duration(200).save(provider);
        GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder(GTNACORE.id("mega/stabilized_naquadah_water_plant_casing"))
                .inputItems(TagPrefix.frameGt, GTMaterials.Naquadah)
                .inputItems(TagPrefix.pipeTinyFluid, GTMaterials.NiobiumTitanium, 4)
                .inputItems(TagPrefix.plate, GTMaterials.NaquadahEnriched, 6)
                .inputFluids(GTMaterials.NaquadahAlloy.getFluid(288))
                .outputItems(GTNABlocks.STABILIZED_NAQUADAH_WATER_PLANT_CASING.asStack())
                .EUt(120).duration(200).save(provider);

        // ---- Controllers ----
        VanillaRecipeHelper.addShapedRecipe(provider, true, GTNACORE.id("mega/large_pyrolyse_oven"),
                GTNAMegaMachines.LARGE_PYROLYSE_OVEN.asStack(),
                "ABA", "CDC", "ABA",
                'A', new MaterialEntry(TagPrefix.plateDouble, GTMaterials.StainlessSteel),
                'B', GTItems.FIELD_GENERATOR_IV.asStack(),
                'C', new MaterialEntry(TagPrefix.pipeHugeFluid, GTMaterials.VanadiumSteel),
                'D', GTMultiMachines.PYROLYSE_OVEN.asStack());

        // GTO Large Cracker -> GTCEu Cracker; Mendelevium wire -> Europium; Tricalcium Phosphate flakes -> the
        // Calcium Oxide ceramic block; Ceruclase -> Naquadria; Abyssal Alloy -> Neutronium.
        GTRecipeTypes.ASSEMBLY_LINE_RECIPES.recipeBuilder(GTNACORE.id("mega/cracker_hub"))
                .inputItems(GTMultiMachines.CRACKER.asStack(16))
                .inputItems(GTNAMegaMachines.LARGE_PYROLYSE_OVEN.asStack(16))
                .inputItems(GTBlocks.COIL_TRITANIUM.asStack(64))
                .inputItems(GTItems.ELECTRIC_PUMP_UHV.asStack(32))
                .inputItems(GTItems.EMITTER_UHV.asStack(16))
                .inputItems(GTItems.SENSOR_UHV.asStack(16))
                .inputItems(CustomTags.UIV_CIRCUITS, 4)
                .inputItems(TagPrefix.wireGtOctal, GTMaterials.Europium, 64)
                .inputItems(GTNABlocks.CALCIUM_OXIDE_CERAMIC_ANTI_METAL_CORROSION_MECHANICAL_BLOCK.asStack(64))
                .inputFluids(
                        com.raishxn.gtna.common.data.material.GodforgeChainMaterials.MutatedLivingSolder.getFluid(2304))
                .inputFluids(GTMaterials.Naquadria.getFluid(2304))
                .inputFluids(GTNAMaterials.MarM200Steel.getFluid(2304))
                .inputFluids(GTMaterials.Neutronium.getFluid(2304))
                .outputItems(GTNAMegaMachines.CRACKER_HUB.asStack())
                .EUt(GTValues.VA[GTValues.UEV]).duration(800)
                .stationResearch(b -> b.researchStack(GTMultiMachines.CRACKER.asStack()).CWUt(256))
                .save(provider);

        // GTO UHV Brewery/Fermenter -> UV (GTCEu's single blocks stop at UV); Mithril spring -> Europium.
        GTRecipeTypes.ASSEMBLY_LINE_RECIPES.recipeBuilder(GTNACORE.id("mega/mega_brewer"))
                .inputItems(GTMachines.BREWERY[GTValues.UV].asStack(16))
                .inputItems(GTMachines.FERMENTER[GTValues.UV].asStack(16))
                .inputItems(GTItems.ELECTRIC_PUMP_UEV.asStack(32))
                .inputItems(TagPrefix.spring, GTMaterials.Europium, 16)
                .inputItems(TagPrefix.pipeQuadrupleFluid, GTMaterials.VanadiumSteel, 32)
                .inputItems(CustomTags.UEV_CIRCUITS, 32)
                .inputItems(TagPrefix.wireGtQuadruple, GTMaterials.RutheniumTriniumAmericiumNeutronate, 4)
                .inputItems(TagPrefix.plateDouble, GTMaterials.Naquadah, 32)
                .inputFluids(GTMaterials.SolderingAlloy.getFluid(2304))
                .inputFluids(
                        com.raishxn.gtna.common.data.material.GodforgeChainMaterials.MutatedLivingSolder.getFluid(2304))
                .inputFluids(GTMaterials.MolybdenumDisilicide.getFluid(2304))
                .inputFluids(GTMaterials.CobaltBrass.getFluid(2304))
                .outputItems(GTNAMegaMachines.MEGA_BREWER.asStack())
                .EUt(1966080).duration(1000)
                .stationResearch(b -> b.researchStack(GCYMMachines.LARGE_BREWER.asStack()).CWUt(512)
                        .EUt(GTValues.VA[GTValues.UIV]))
                .save(provider);

        // GTO UEV Voltage Coil -> UV coil; Abyssal Alloy cable -> Europium wire; Titan Steel -> Naquadah.
        GTRecipeTypes.ASSEMBLY_LINE_RECIPES.recipeBuilder(GTNACORE.id("mega/mega_vacuum_drying_furnace"))
                .inputItems(GTNAMachines3.VACUUM_DRYING_FURNACE.asStack(16))
                .inputItems(GTItems.VOLTAGE_COIL_UV.asStack(64))
                .inputItems(GTItems.EMITTER_UEV.asStack(16))
                .inputItems(GTItems.SENSOR_UEV.asStack(16))
                .inputItems(GTItems.ELECTRIC_PUMP_UEV.asStack(32))
                .inputItems(GTItems.ELECTRIC_PISTON_UEV.asStack(16))
                .inputItems(CustomTags.UIV_CIRCUITS, 16)
                .inputItems(TagPrefix.wireGtHex, GTMaterials.Europium, 16)
                .inputItems(TagPrefix.pipeNormalFluid, GTMaterials.Neutronium, 16)
                .inputItems(TagPrefix.plateDouble, GTMaterials.Naquadah, 16)
                .inputFluids(GTMaterials.Neutronium.getFluid(2304))
                .inputFluids(
                        com.raishxn.gtna.common.data.material.GodforgeChainMaterials.MutatedLivingSolder.getFluid(2304))
                .outputItems(GTNAMegaMachines.MEGA_VACUUM_DRYING_FURNACE.asStack())
                .EUt(GTValues.VA[GTValues.UEV]).duration(800)
                .stationResearch(b -> b.researchStack(GTNAMachines3.VACUUM_DRYING_FURNACE.asStack()).CWUt(256))
                .save(provider);

        // GTO Hastelloy X-78 -> Hastelloy X (gear -> Osmiridium); Quantanium small gear -> Osmiridium.
        GTRecipeTypes.ASSEMBLY_LINE_RECIPES.recipeBuilder(GTNACORE.id("mega/giant_flotation_tank"))
                .inputItems(GTMachines.HULL[GTValues.UEV].asStack())
                .inputItems(GTNAMachines3.INDUSTRIAL_FLOTATION_CELL.asStack(16))
                .inputItems(TagPrefix.plateDouble, GTMaterials.HastelloyX, 8)
                .inputItems(TagPrefix.plateDouble, GTMaterials.IncoloyMA956, 8)
                .inputItems(CustomTags.UEV_CIRCUITS, 16)
                .inputItems(CustomTags.UIV_CIRCUITS, 16)
                .inputItems(GTItems.ELECTRIC_PUMP_LuV.asStack(2))
                .inputItems(TagPrefix.gearSmall, GTMaterials.Osmiridium, 64)
                .inputItems(TagPrefix.gear, GTMaterials.Osmiridium, 16)
                .inputItems(TagPrefix.foil, GTMaterials.TungstenSteel, 32)
                .inputItems(TagPrefix.cableGtQuadruple, GTMaterials.VanadiumGallium, 4)
                .inputFluids(GTMaterials.SolderingAlloy.getFluid(5760))
                .inputFluids(GTMaterials.Lubricant.getFluid(6000))
                .inputFluids(GTMaterials.WatertightSteel.getFluid(1152))
                .outputItems(GTNAMegaMachines.GIANT_FLOTATION_TANK.asStack())
                .EUt(30720).duration(2400)
                .stationResearch(b -> b.researchStack(GTNAMachines3.INDUSTRIAL_FLOTATION_CELL.asStack()).CWUt(320))
                .save(provider);

        // ---- Lote 2 ----
        // GTO Lafium double plate -> Naquadah Alloy; Seaborgium (no fluid in GTCEu) -> Naquadria.
        GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder(GTNACORE.id("mega/amprosium_active_casing"))
                .inputItems(TagPrefix.frameGt, GTMaterials.Neutronium)
                .inputItems(TagPrefix.pipeNormalFluid, GTMaterials.Europium, 4)
                .inputItems(TagPrefix.plateDouble, GTMaterials.NaquadahAlloy, 4)
                .inputItems(TagPrefix.plate, GTMaterials.Neutronium, 8)
                .inputFluids(GTMaterials.Naquadria.getFluid(576))
                .outputItems(GTNABlocks.AMPROSIUM_ACTIVE_CASING.asStack())
                .EUt(480).duration(200).save(provider);
        GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder(GTNACORE.id("mega/amprosium_gearbox"))
                .inputItems(TagPrefix.plate, GTMaterials.Neutronium, 4)
                .inputItems(TagPrefix.gear, GTMaterials.Neutronium, 2)
                .inputItems(TagPrefix.frameGt, GTMaterials.Neutronium)
                .circuitMeta(4)
                .outputItems(GTNABlocks.AMPROSIUM_GEARBOX.asStack())
                .EUt(16).duration(50).save(provider);

        // GTO Assembler recipe of the Large Incubator, unchanged.
        GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder(GTNACORE.id("mega/large_incubator"))
                .inputItems(com.raishxn.gtna.common.data.GTNAMachines3.INCUBATOR.asStack())
                .inputItems(GTItems.FIELD_GENERATOR_LuV.asStack(4))
                .inputItems(GTItems.SENSOR_LuV.asStack(4))
                .inputItems(GTItems.FLUID_REGULATOR_LuV.asStack(4))
                .inputItems(TagPrefix.wireGtOctal, GTMaterials.IndiumTinBariumTitaniumCuprate, 4)
                .inputItems(GTBlocks.CASING_LAMINATED_GLASS.asStack(16))
                .inputFluids(GTMaterials.Polytetrafluoroethylene.getFluid(1440))
                .outputItems(GTNAMegaMachines.LARGE_INCUBATOR.asStack())
                .EUt(122880).duration(800).save(provider);
        // GTO GlassRecipe for the tiered glasses GTNA lacked; GTO-only metals replaced (Enderium -> Darmstadtium,
        // Heavy Quark Degenerate Matter -> Quark-Gluon Plasma).
        tieredGlass(provider, GTValues.EV, GTMaterials.Titanium, GTNABlocks.TITANIUM_BOROSILICATE_GLASS);
        tieredGlass(provider, GTValues.UV, GTMaterials.Tritanium, GTNABlocks.TRITANIUM_BOROSILICATE_GLASS);
        tieredGlass(provider, GTValues.UEV, GTMaterials.Darmstadtium, GTNABlocks.ENDERIUM_BOROSILICATE_GLASS);
        tieredGlass(provider, GTValues.UXV, com.raishxn.gtna.common.data.GTNAMaterials.QuarkGluonPlasma,
                GTNABlocks.QUARKS_BOROSILICATE_GLASS);
        tieredGlass(provider, GTValues.OpV, com.raishxn.gtna.common.data.GTNAMaterials.Draconium,
                GTNABlocks.DRACONIUM_BOROSILICATE_GLASS);
        tieredGlass(provider, GTValues.MAX, com.raishxn.gtna.common.data.GTNAMaterials.CosmicNeutronium,
                GTNABlocks.COSMIC_NEUTRONIUM_BOROSILICATE_GLASS);

        // GTO suprachronal_assembly_line -> Nyarlathotep's Tentacle. GTO-only inputs replaced: Infinite Cell
        // Component -> Quantum Chest ZPM, Advanced/Circuit Assembly Line -> Assembly Line / UV Circuit Assembler,
        // Precision Circuit Assembly Robot MK3 -> UEV Robot Arm, Dalisenite -> Neutronium; research on the Assembly
        // Line (GTO's Assembler Module is not ported).
        GTRecipeTypes.ASSEMBLY_LINE_RECIPES.recipeBuilder(GTNACORE.id("mega/nyarlathoteps_tentacle"))
                .inputItems(GTMachines.QUANTUM_CHEST[GTValues.ZPM].asStack(64))
                .inputItems(GTMultiMachines.ASSEMBLY_LINE.asStack(64))
                .inputItems(GTMachines.CIRCUIT_ASSEMBLER[GTValues.UV].asStack(64))
                .inputItems(GTNABlocks.SPACETIME_ASSEMBLY_LINE_CASING.asStack(16))
                .inputItems(GTNABlocks.SPACETIME_ASSEMBLY_LINE_UNIT.asStack(16))
                .inputItems(GTNABlocks.MOLECULAR_COIL.asStack(32))
                .inputItems(GTItems.EMITTER_UEV.asStack(32))
                .inputItems(GTItems.SENSOR_UEV.asStack(32))
                .inputItems(GTItems.ROBOT_ARM_UEV.asStack(64))
                .inputItems(CustomTags.UIV_CIRCUITS, 64)
                .inputItems(GTItems.ULTIMATE_BATTERY.asStack())
                .inputItems(TagPrefix.plateDouble, GTMaterials.Neutronium, 32)
                .inputFluids(GTMaterials.BorosilicateGlass.getFluid(3204))
                .inputFluids(GTMaterials.SiliconeRubber.getFluid(5760))
                .inputFluids(GTMaterials.UraniumTriplatinum.getFluid(1296))
                .inputFluids(GTMaterials.Stellite100.getFluid(5184))
                .outputItems(GTNAMegaMachines.NYARLATHOTEPS_TENTACLE.asStack())
                .EUt(7864320).duration(3200)
                .stationResearch(r -> r.researchStack(GTMultiMachines.ASSEMBLY_LINE.asStack()).CWUt(256)
                        .EUt(7864320))
                .save(provider);

        // GTO sintering_furnace AL recipe -> Giant Sintering Array. GTO-only inputs: High Durability Compound Steel
        // rod -> HSS-S; NM chips -> UHV circuits; GTO Sintering Furnace -> 64 Electric Blast Furnaces; Titan Steel /
        // Trinium-Titanium foil -> Tritanium / Trinium. Research on the Electric Blast Furnace.
        GTRecipeTypes.ASSEMBLY_LINE_RECIPES.recipeBuilder(GTNACORE.id("mega/giant_sintering_array"))
                .inputItems(CustomTags.UEV_CIRCUITS, 16)
                .inputItems(GTItems.FIELD_GENERATOR_UHV.asStack(16))
                .inputItems(GTItems.SENSOR_UHV.asStack(8))
                .inputItems(GTItems.EMITTER_UHV.asStack(8))
                .inputItems(TagPrefix.gear, GTMaterials.TitaniumTungstenCarbide, 32)
                .inputItems(TagPrefix.rod, GTMaterials.HSSS, 64)
                .inputItems(CustomTags.UHV_CIRCUITS, 64)
                .inputItems(GTMultiMachines.ELECTRIC_BLAST_FURNACE.asStack(64))
                .inputItems(TagPrefix.foil, GTMaterials.Aluminium, 64)
                .inputItems(TagPrefix.foil, GTMaterials.Ruridit, 64)
                .inputItems(TagPrefix.foil, GTMaterials.Tritanium, 64)
                .inputItems(TagPrefix.foil, GTMaterials.Trinium, 64)
                .inputFluids(GTMaterials.Nichrome.getFluid(10000))
                .inputFluids(GTMaterials.RTMAlloy.getFluid(10000))
                .inputFluids(GTMaterials.HSSG.getFluid(10000))
                .inputFluids(GTMaterials.Neutronium.getFluid(7288))
                .outputItems(GTNAMegaMachines.GIANT_SINTERING_ARRAY.asStack())
                .EUt(GTValues.VA[GTValues.UHV]).duration(800)
                .stationResearch(r -> r.researchStack(GTMultiMachines.ELECTRIC_BLAST_FURNACE.asStack()).CWUt(256)
                        .EUt(GTValues.VA[GTValues.UHV]))
                .save(provider);
        // GTO integrated_vapor_deposition_system AL recipe. GTO's CVD/PVD single blocks -> UV Chemical Reactors and
        // UV Laser Engravers; Enderium pipe -> Naquadah; Ignatius plate -> Neutronium; Quantanium -> Naquadria.
        GTRecipeTypes.ASSEMBLY_LINE_RECIPES.recipeBuilder(GTNACORE.id("mega/integrated_vapor_deposition_system"))
                .inputItems(GTMachines.CHEMICAL_REACTOR[GTValues.UV].asStack(16))
                .inputItems(GTMachines.LASER_ENGRAVER[GTValues.UV].asStack(16))
                .inputItems(GTItems.FLUID_REGULATOR_UEV.asStack(32))
                .inputItems(GTItems.ROBOT_ARM_UEV.asStack(8))
                .inputItems(GTItems.FIELD_GENERATOR_UEV.asStack(8))
                .inputItems(GTItems.SENSOR_UEV.asStack(16))
                .inputItems(TagPrefix.pipeNormalFluid, GTMaterials.Naquadah, 32)
                .inputItems(CustomTags.UIV_CIRCUITS, 8)
                .inputItems(TagPrefix.plateDouble, GTMaterials.Neutronium, 32)
                .inputFluids(com.raishxn.gtna.common.data.material.GodforgeChainMaterials.MutatedLivingSolder
                        .getFluid(2304))
                .inputFluids(GTMaterials.Naquadria.getFluid(2304))
                .outputItems(GTNAMegaMachines.INTEGRATED_VAPOR_DEPOSITION_SYSTEM.asStack())
                .EUt(2097152).duration(800)
                .stationResearch(r -> r.researchStack(GTBlocks.CLEANROOM_GLASS.asStack()).CWUt(256).EUt(2097152))
                .save(provider);

        // GTO Dyson Sphere. GTO-only inputs replaced: Precision Assembler -> Assembly Line, Vibrant Photovoltaic
        // Block -> UV Solar panels are absent in GTCEu, so UEV Field Generators; Gelid Cryotheum -> liquid helium;
        // Orichalcum -> Trinium; Atomic Archives -> UXV circuits; Echoite hex wire -> Europium; Vibranium ->
        // Neutronium; MFPC / Hexaphase Copper / coolant cells / batteries -> UIV parts.
        GTRecipeTypes.ASSEMBLY_LINE_RECIPES.recipeBuilder(GTNACORE.id("mega/dyson_swarm_module"))
                .inputItems(TagPrefix.frameGt, GTMaterials.NaquadahEnriched, 16)
                .inputItems(GTItems.FIELD_GENERATOR_UEV.asStack(4))
                .inputItems(GTItems.SENSOR_UEV.asStack())
                .inputItems(GTItems.EMITTER_UEV.asStack())
                .inputFluids(com.raishxn.gtna.common.data.material.GodforgeChainMaterials.MutatedLivingSolder
                        .getFluid(20000))
                .inputFluids(GTMaterials.Helium.getFluid(com.gregtechceu.gtceu.api.fluids.store.FluidStorageKeys.LIQUID,
                        20000))
                .inputFluids(GTMaterials.Neutronium.getFluid(18432))
                .inputFluids(GTMaterials.Trinium.getFluid(18432))
                .outputItems(com.raishxn.gtna.common.data.GTNAItems.DYSON_SWARM_MODULE.asStack(64))
                .EUt(31457280).duration(800)
                .stationResearch(r -> r.researchStack(GTItems.FIELD_GENERATOR_UEV.asStack()).CWUt(512)
                        .EUt(31457280))
                .save(provider);
        com.raishxn.gtna.common.data.GTNARecipeType.DYSON_SPHERE_RECIPES
                .recipeBuilder(GTNACORE.id("dyson_sphere/launch"))
                .inputItems(com.raishxn.gtna.common.data.GTNAItems.DYSON_SWARM_MODULE.asStack(64))
                .CWUt(512).duration(200).EUt(GTValues.VA[GTValues.UIV])
                .save(provider);
        GTRecipeTypes.ASSEMBLY_LINE_RECIPES.recipeBuilder(GTNACORE.id("mega/dyson_sphere_launch_silo"))
                .inputItems(CustomTags.UXV_CIRCUITS, 64)
                .inputItems(GTNABlocks.DYSON_CONTROL_TOROID.asStack(4))
                .inputItems(GTNABlocks.DYSON_DEPLOYMENT_CORE.asStack(4))
                .inputItems(GTNABlocks.DYSON_DEPLOYMENT_MAGNET.asStack(4))
                .inputItems(CustomTags.UXV_CIRCUITS, 32)
                .inputItems(GTItems.EMITTER_UIV.asStack(64))
                .inputItems(TagPrefix.wireGtHex, GTMaterials.Europium, 32)
                .inputItems(TagPrefix.plateDouble, GTMaterials.Neutronium, 16)
                .inputItems(GTItems.FIELD_GENERATOR_UIV.asStack(16))
                .inputItems(GTItems.EMITTER_UIV.asStack(64))
                .inputFluids(GTMaterials.Helium.getFluid(com.gregtechceu.gtceu.api.fluids.store.FluidStorageKeys.LIQUID,
                        12800))
                .inputFluids(GTMaterials.RutheniumTriniumAmericiumNeutronate.getFluid(30576))
                .inputFluids(com.raishxn.gtna.common.data.material.GodforgeChainMaterials.MutatedLivingSolder
                        .getFluid(8000))
                .outputItems(GTNAMegaMachines.DYSON_SPHERE_LAUNCH_SILO.asStack())
                .EUt(33554431).duration(1600)
                .stationResearch(r -> r.researchStack(GTNABlocks.DYSON_DEPLOYMENT_CORE.asStack()).CWUt(512)
                        .EUt(31457280))
                .save(provider);
        GTRecipeTypes.ASSEMBLY_LINE_RECIPES.recipeBuilder(GTNACORE.id("mega/dyson_sphere_receiving_station"))
                .inputItems(GTMachines.DIODE[GTValues.UIV].asStack(4))
                .inputItems(GTItems.SENSOR_UIV.asStack(16))
                .inputItems(GTNABlocks.DYSON_CONTROL_TOROID.asStack(4))
                .inputItems(GTBlocks.SUPERCONDUCTING_COIL.asStack(64))
                .inputItems(CustomTags.UXV_CIRCUITS, 16)
                .inputItems(TagPrefix.wireGtHex, GTMaterials.Europium, 32)
                .inputItems(TagPrefix.plateDouble, GTMaterials.Neutronium, 16)
                .inputFluids(com.raishxn.gtna.common.data.material.GodforgeChainMaterials.MutatedLivingSolder
                        .getFluid(12000))
                .inputFluids(GTMaterials.Helium.getFluid(com.gregtechceu.gtceu.api.fluids.store.FluidStorageKeys.LIQUID,
                        12800))
                .inputFluids(GTMaterials.Europium.getFluid(576000))
                .inputFluids(GTMaterials.MercuryBariumCalciumCuprate.getFluid(576000))
                .outputItems(GTNAMegaMachines.DYSON_SPHERE_RECEIVING_STATION.asStack())
                .EUt(31457280).duration(1600)
                .stationResearch(r -> r.researchStack(GTNABlocks.DYSON_RECEIVER_CASING.asStack()).CWUt(512)
                        .EUt(31457280))
                .save(provider);

        // GTO Vanilla.java shaped recipe of the Reaction Furnace, unchanged.
        com.gregtechceu.gtceu.data.recipe.VanillaRecipeHelper.addShapedRecipe(provider, true,
                GTNACORE.id("mega/reaction_furnace"), GTNAMegaMachines.REACTION_FURNACE.asStack(),
                "ABA", "CDC", "BAB",
                'A', GTMachines.ELECTRIC_FURNACE[GTValues.MV].asStack(), 'B', GTMachines.GOLD_DRUM.asStack(),
                'C', new com.gregtechceu.gtceu.api.data.chemical.material.stack.MaterialEntry(TagPrefix.cableGtOctal,
                        GTMaterials.Iron),
                'D', GTMachines.CHEMICAL_REACTOR[GTValues.LV].asStack());

        // GTO mega_mixer -> Kerr-Newman Homogenizer. Quantanium curved plate -> double Naquadah plate; High
        // Durability Compound Steel -> HSS-S; Orichalcum -> Trinium (GTO-only materials).
        GTRecipeTypes.ASSEMBLY_LINE_RECIPES.recipeBuilder(GTNACORE.id("mega/kerr_newman_homogenizer"))
                .inputItems(GTMachines.MIXER[GTValues.UHV].asStack(16))
                .inputItems(GTItems.ELECTRIC_PUMP_UEV.asStack(16))
                .inputItems(GTItems.ELECTRIC_MOTOR_UEV.asStack(16))
                .inputItems(GTItems.ROBOT_ARM_UEV.asStack(16))
                .inputItems(GTItems.SENSOR_UEV.asStack(8))
                .inputItems(CustomTags.UIV_CIRCUITS, 8)
                .inputItems(TagPrefix.rodLong, GTMaterials.Osmium, 32)
                .inputItems(TagPrefix.rodLong, GTMaterials.Europium, 32)
                .inputItems(TagPrefix.plateDouble, GTMaterials.Naquadah, 32)
                .inputFluids(com.raishxn.gtna.common.data.material.GodforgeChainMaterials.MutatedLivingSolder
                        .getFluid(1000))
                .inputFluids(GTMaterials.HSSS.getFluid(1000))
                .inputFluids(GTMaterials.Trinium.getFluid(1000))
                .outputItems(GTNAMegaMachines.KERR_NEWMAN_HOMOGENIZER.asStack())
                .EUt(2097152).duration(800)
                .stationResearch(r -> r.researchStack(GCYMMachines.LARGE_MIXER.asStack()).CWUt(256).EUt(2097152))
                .save(provider);

        // GTO UHV single blocks -> UV; Titan Steel wire -> Europium; Quantum Metal -> Naquadah; Mithril -> Trinium.
        GTRecipeTypes.ASSEMBLY_LINE_RECIPES.recipeBuilder(GTNACORE.id("mega/phase_change_cube"))
                .inputItems(GTMachines.EXTRACTOR[GTValues.UV].asStack(16))
                .inputItems(GTMachines.FLUID_SOLIDIFIER[GTValues.UV].asStack(16))
                .inputItems(GTItems.ELECTRIC_PISTON_UEV.asStack(32))
                .inputItems(GTItems.ELECTRIC_PUMP_UEV.asStack(64))
                .inputItems(CustomTags.UIV_CIRCUITS, 32)
                .inputItems(TagPrefix.wireGtHex, GTMaterials.Europium, 16)
                .inputItems(TagPrefix.plateDouble, GTMaterials.Naquadah, 16)
                .inputItems(TagPrefix.plateDouble, GTMaterials.HastelloyX, 32)
                .inputFluids(com.raishxn.gtna.common.data.material.GodforgeChainMaterials.MutatedLivingSolder
                        .getFluid(2304))
                .inputFluids(GTMaterials.Naquadria.getFluid(4608))
                .inputFluids(GTMaterials.Plutonium239.getFluid(4608))
                .inputFluids(GTMaterials.Trinium.getFluid(4608))
                .outputItems(GTNAMegaMachines.PHASE_CHANGE_CUBE.asStack())
                .EUt(7864320).duration(800)
                .stationResearch(b -> b.researchStack(GCYMMachines.LARGE_EXTRACTOR.asStack()).CWUt(256)
                        .EUt(7864320))
                .save(provider);

        // GTO Fluxed Electrum / Grisium plates -> Europium / Tritanium; Artherium-Tin -> Naquadah Alloy.
        GTRecipeTypes.ASSEMBLY_LINE_RECIPES.recipeBuilder(GTNACORE.id("mega/engraving_laser_plant"))
                .inputItems(GTMachines.LASER_ENGRAVER[GTValues.UV].asStack(8))
                .inputItems(GTItems.EMITTER_UHV.asStack(8))
                .inputItems(GTItems.ELECTRIC_PISTON_UHV.asStack(8))
                .inputItems(GTItems.SENSOR_UHV.asStack(8))
                .inputItems(GTItems.ROBOT_ARM_UHV.asStack(8))
                .inputItems(GTItems.ELECTRIC_PUMP_UHV.asStack(8))
                .inputItems(TagPrefix.rod, GTNAMaterials.Stellite, 32)
                .inputItems(CustomTags.UEV_CIRCUITS, 8)
                .inputItems(TagPrefix.plate, GTMaterials.Europium, 32)
                .inputItems(TagPrefix.plate, GTMaterials.Tritanium, 32)
                .inputItems(TagPrefix.plateDouble, GTMaterials.TitaniumCarbide, 16)
                .inputItems(TagPrefix.plateDouble, GTMaterials.TitaniumTungstenCarbide, 16)
                .inputFluids(GTNAMaterials.Indalloy140.getFluid(2592))
                .inputFluids(GTMaterials.NaquadahAlloy.getFluid(1296))
                .inputFluids(com.raishxn.gtna.common.data.material.GodforgeChainMaterials.MutatedLivingSolder
                        .getFluid(1296))
                .inputFluids(GTMaterials.SolderingAlloy.getFluid(2880))
                .outputItems(GTNAMegaMachines.ENGRAVING_LASER_PLANT.asStack())
                .EUt(491520).duration(1200)
                .stationResearch(b -> b.researchStack(GCYMMachines.LARGE_ENGRAVING_LASER.asStack()).CWUt(64)
                        .EUt(491520))
                .save(provider);

        GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder(GTNACORE.id("mega/infinity_fluid_drilling_rig"))
                .inputItems(GTMachines.HULL[GTValues.UV].asStack())
                .inputItems(TagPrefix.frameGt, GTMaterials.Ruridit, 4)
                .inputItems(CustomTags.UV_CIRCUITS, 4)
                .inputItems(GTItems.ELECTRIC_MOTOR_UV.asStack(4))
                .inputItems(GTItems.ELECTRIC_PUMP_UV.asStack(4))
                .inputItems(TagPrefix.gear, GTMaterials.Neutronium, 4)
                .circuitMeta(2)
                .outputItems(GTNAMegaMachines.INFINITY_FLUID_DRILLING_RIG.asStack())
                .EUt(GTValues.VA[GTValues.UV]).duration(400).save(provider);

        // GTL KubeJS recipe (GregTech Leisure 1.4.5.1); GTO Evaporation Plant is the GTNA port.
        GTRecipeTypes.ASSEMBLY_LINE_RECIPES.recipeBuilder(GTNACORE.id("mega/mega_distillery"))
                .inputItems(GTMultiMachines.DISTILLATION_TOWER.asStack(16))
                .inputItems(GTNAMachines3.EVAPORATION_PLANT.asStack(16))
                .inputItems(TagPrefix.pipeHugeFluid, GTMaterials.TungstenSteel, 8)
                .inputItems(GTItems.ELECTRIC_PUMP_UHV.asStack(16))
                .inputItems(GTItems.SENSOR_UEV.asStack(4))
                .inputItems(CustomTags.UIV_CIRCUITS, 4)
                .inputItems(TagPrefix.wireGtHex, GTMaterials.AnnealedCopper, 32)
                .inputItems(TagPrefix.plate, GTMaterials.WatertightSteel, 32)
                .inputFluids(GTMaterials.SolderingAlloy.getFluid(1152))
                .inputFluids(GTNAMaterials.Indalloy140.getFluid(1152))
                .inputFluids(GTMaterials.StainlessSteel.getFluid(2304))
                .inputFluids(GTMaterials.PolyvinylChloride.getFluid(2880))
                .outputItems(GTNAMegaMachines.MEGA_DISTILLERY.asStack())
                .EUt(GTValues.VA[GTValues.UHV]).duration(800)
                .stationResearch(b -> b.researchStack(GCYMMachines.LARGE_DISTILLERY.asStack()).CWUt(600)
                        .EUt(GTValues.VA[GTValues.UHV]))
                .save(provider);

        // ---- Lote 3 ----
        // GTO Copper nanites -> Quantum Star; dense RhodiumPlatedPalladium/NaquadahAlloy -> double plates;
        // RTAN double plate -> Tritanium; Astatine/Actinium (no fluid in GTCEu) -> Naquadah/Europium.
        GTRecipeTypes.ASSEMBLY_LINE_RECIPES.recipeBuilder(GTNACORE.id("mega/super_blast_smelter"))
                .inputItems(TagPrefix.frameGt, GTMaterials.TungstenCarbide, 64)
                .inputItems(GCYMMachines.MEGA_BLAST_FURNACE.asStack(64))
                .inputItems(GTNAMachines3.MEGA_ALLOY_BLAST_SMELTER.asStack(64))
                .inputItems(GTItems.FIELD_GENERATOR_UV.asStack(64))
                .inputItems(GTItems.FLUID_REGULATOR_IV.asStack(64))
                .inputItems(CustomTags.UEV_CIRCUITS, 64)
                .inputItems(GTItems.QUANTUM_STAR.asStack(16))
                .inputItems(TagPrefix.wireGtHex, GTMaterials.RutheniumTriniumAmericiumNeutronate, 64)
                .inputItems(TagPrefix.plateDense, GTMaterials.TungstenSteel, 14)
                .inputItems(TagPrefix.plateDouble, GTMaterials.RhodiumPlatedPalladium, 14)
                .inputItems(TagPrefix.plateDouble, GTMaterials.NaquadahAlloy, 14)
                .inputItems(TagPrefix.plateDense, GTMaterials.Darmstadtium, 14)
                .inputItems(TagPrefix.plateDouble, GTMaterials.Gallium, 64)
                .inputItems(TagPrefix.plateDouble, GTMaterials.Chromium, 64)
                .inputItems(TagPrefix.plateDouble, GTMaterials.Cobalt, 64)
                .inputItems(TagPrefix.plateDouble, GTMaterials.Tritanium, 64)
                .inputFluids(GTMaterials.Cobalt.getFluid(5760))
                .inputFluids(GTMaterials.Niobium.getFluid(5760))
                .inputFluids(GTMaterials.Naquadah.getFluid(5760))
                .inputFluids(GTMaterials.Europium.getFluid(5760))
                .outputItems(GTNAMegaMachines.SUPER_BLAST_SMELTER.asStack())
                .EUt(1966080).duration(1200)
                .stationResearch(b -> b.researchStack(GTMultiMachines.MULTI_SMELTER.asStack()).CWUt(256)
                        .EUt(1966080))
                .save(provider);

        VanillaRecipeHelper.addShapedRecipe(provider, true, GTNACORE.id("mega/large_cracker"),
                GTNAMegaMachines.LARGE_CRACKER.asStack(),
                "ABA", "CDC", "ABA",
                'A', GTItems.FIELD_GENERATOR_LuV.asStack(),
                'B', CustomTags.UV_CIRCUITS,
                'C', new MaterialEntry(TagPrefix.spring, GTMaterials.Naquadah),
                'D', GTMultiMachines.CRACKER.asStack());

        // GTO Precision Circuit Assembly Robot -> UV Robot Arm; Lafium plate -> Tritanium; YBCO screw -> HSS-S;
        // RTM long rod -> Ultimet; Nobelium/Lawrencium -> Naquadria/Americium; research Precision Assembler ->
        // GCYM Large Assembler.
        GTRecipeTypes.ASSEMBLY_LINE_RECIPES.recipeBuilder(GTNACORE.id("mega/integrated_assembler"))
                .inputItems(GCYMMachines.LARGE_ASSEMBLER.asStack(32))
                .inputItems(GTItems.ROBOT_ARM_UV.asStack(16))
                .inputItems(GTItems.FLUID_REGULATOR_UHV.asStack(32))
                .inputItems(GTItems.ROBOT_ARM_UHV.asStack(64))
                .inputItems(CustomTags.UIV_CIRCUITS, 32)
                .inputItems(TagPrefix.screw, GTMaterials.TungstenCarbide, 64)
                .inputItems(TagPrefix.screw, GTMaterials.HSSS, 64)
                .inputItems(TagPrefix.screw, GTMaterials.RhodiumPlatedPalladium, 64)
                .inputItems(TagPrefix.screw, GTMaterials.NaquadahAlloy, 64)
                .inputItems(TagPrefix.rodLong, GTMaterials.Ultimet, 32)
                .inputItems(TagPrefix.rodLong, GTMaterials.TungstenCarbide, 32)
                .inputItems(TagPrefix.rodLong, GTMaterials.HSLASteel, 32)
                .inputItems(TagPrefix.rodLong, GTMaterials.NaquadahAlloy, 32)
                .inputItems(TagPrefix.plate, GTMaterials.Tritanium, 16)
                .inputItems(TagPrefix.plateDouble, GTMaterials.Iridium, 8)
                .inputFluids(com.raishxn.gtna.common.data.material.GodforgeChainMaterials.MutatedLivingSolder
                        .getFluid(5760))
                .inputFluids(GTMaterials.Kanthal.getFluid(5760))
                .inputFluids(GTMaterials.Naquadria.getFluid(2880))
                .inputFluids(GTMaterials.Americium.getFluid(2880))
                .outputItems(GTNAMegaMachines.INTEGRATED_ASSEMBLER.asStack())
                .EUt(1966080).duration(800)
                .stationResearch(b -> b.researchStack(GCYMMachines.LARGE_ASSEMBLER.asStack()).CWUt(128)
                        .EUt(1966080))
                .save(provider);

        // ---- Lote 4: blocos compartilhados ----
        GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder(GTNACORE.id("mega/high_pressure_resistant_casing"))
                .inputItems(TagPrefix.frameGt, GTNAMaterials.HastelloyN)
                .inputItems(TagPrefix.rotor, GTMaterials.HastelloyC276)
                .inputItems(TagPrefix.plateDouble, GTMaterials.HastelloyX, 6)
                .inputFluids(GTMaterials.Polytetrafluoroethylene.getFluid(288))
                .outputItems(GTNABlocks.HIGH_PRESSURE_RESISTANT_CASING.asStack())
                .EUt(480).duration(200).save(provider);
        GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder(GTNACORE.id("mega/mc_nylon_tensile_mechanical_shell"))
                .inputItems(TagPrefix.frameGt, GTMaterials.BlueSteel)
                .inputItems(TagPrefix.plate, GTMaterials.Polycaprolactam, 6)
                .circuitMeta(6)
                .outputItems(GTNABlocks.MC_NYLON_TENSILE_MECHANICAL_SHELL.asStack())
                .EUt(16).duration(50).save(provider);
        // GTO Lafium plates -> Naquadah Alloy.
        GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder(GTNACORE.id("mega/lafium_mechanical_casing"))
                .inputItems(TagPrefix.frameGt, GTMaterials.NaquadahEnriched)
                .inputItems(TagPrefix.plate, GTMaterials.NaquadahAlloy, 6)
                .circuitMeta(6)
                .outputItems(GTNABlocks.LAFIUM_MECHANICAL_CASING.asStack())
                .EUt(16).duration(50).save(provider);
        // GTO GlassRecipe.addGlass(UHV, Neutronium): Borosilicate Glass + 1152 mB.
        GTRecipeTypes.FLUID_SOLIDFICATION_RECIPES.recipeBuilder(GTNACORE.id("mega/amprosium_borosilicate_glass"))
                .inputItems(GTNABlocks.BOROSILICATE_GLASS_BLOCK.asStack())
                .inputFluids(GTMaterials.Neutronium.getFluid(1152))
                .outputItems(GTNABlocks.AMPROSIUM_BOROSILICATE_GLASS.asStack())
                .EUt(GTValues.VA[GTValues.UHV]).duration(200).save(provider);

        // GTO UHV Cutter -> UV; Neutron Pile -> Neutron Reflector; Enderium / Carbon Nanotubes / Liquid Crystal
        // Kevlar -> Naquadria / Polybenzimidazole / Tritanium.
        GTRecipeTypes.ASSEMBLY_LINE_RECIPES.recipeBuilder(GTNACORE.id("mega/neutronium_wire_cutting"))
                .inputItems(GTMachines.CUTTER[GTValues.UV].asStack(16))
                .inputItems(GTItems.NEUTRON_REFLECTOR.asStack(16))
                .inputItems(GTItems.ROBOT_ARM_UEV.asStack(16))
                .inputItems(GTItems.ELECTRIC_MOTOR_UEV.asStack(32))
                .inputItems(GTItems.CONVEYOR_MODULE_UEV.asStack(16))
                .inputItems(GTItems.EMITTER_UEV.asStack(16))
                .inputItems(GTItems.GRAVI_STAR.asStack(16))
                .inputItems(CustomTags.UIV_CIRCUITS, 16)
                .inputFluids(GTMaterials.Naquadria.getFluid(2304))
                .inputFluids(com.raishxn.gtna.common.data.material.GodforgeChainMaterials.MutatedLivingSolder
                        .getFluid(2304))
                .inputFluids(GTMaterials.Polybenzimidazole.getFluid(2304))
                .inputFluids(GTMaterials.Tritanium.getFluid(2304))
                .outputItems(GTNAMegaMachines.NEUTRONIUM_WIRE_CUTTING.asStack())
                .EUt(2097152).duration(800)
                .stationResearch(b -> b.researchStack(GCYMMachines.LARGE_CUTTER.asStack()).CWUt(256))
                .save(provider);

        // GTO UHV Centrifuge -> UV; Orichalcum long rod -> Naquadah Alloy; Osmiridium restrictive pipe -> Duranium
        // fluid pipe; Dysprosium / Moscovium -> Europium / Naquadria.
        GTRecipeTypes.ASSEMBLY_LINE_RECIPES.recipeBuilder(GTNACORE.id("mega/holy_separator"))
                .inputItems(GTMachines.CENTRIFUGE[GTValues.UV].asStack(16))
                .inputItems(GTItems.ROBOT_ARM_UEV.asStack(64))
                .inputItems(CustomTags.UIV_CIRCUITS, 64)
                .inputItems(TagPrefix.gear, GTMaterials.Neutronium, 32)
                .inputItems(TagPrefix.gearSmall, GTMaterials.RhodiumPlatedPalladium, 64)
                .inputItems(TagPrefix.rodLong, GTMaterials.NaquadahAlloy, 32)
                .inputItems(TagPrefix.pipeHugeFluid, GTMaterials.Duranium, 16)
                .inputItems(TagPrefix.plate, GTMaterials.Naquadria, 16)
                .inputFluids(com.raishxn.gtna.common.data.material.GodforgeChainMaterials.MutatedLivingSolder
                        .getFluid(1440))
                .inputFluids(GTMaterials.Europium.getFluid(2880))
                .inputFluids(GTMaterials.Rhodium.getFluid(2880))
                .inputFluids(GTMaterials.Naquadria.getFluid(2880))
                .outputItems(GTNAMegaMachines.HOLY_SEPARATOR.asStack())
                .EUt(7864320).duration(1000)
                .stationResearch(b -> b.researchStack(GCYMMachines.LARGE_CENTRIFUGE.asStack()).CWUt(256)
                        .EUt(7864320))
                .save(provider);

        GTRecipeTypes.ASSEMBLY_LINE_RECIPES.recipeBuilder(GTNACORE.id("mega/superconducting_electromagnetism"))
                .inputItems(GCYMMachines.LARGE_ELECTROLYZER.asStack(16))
                .inputItems(GCYMMachines.LARGE_ELECTROMAGNET.asStack(16))
                .inputItems(GTItems.EMITTER_UV.asStack(32))
                .inputItems(CustomTags.UEV_CIRCUITS, 64)
                .inputItems(TagPrefix.wireFine, GTMaterials.UraniumRhodiumDinaquadide, 64)
                .inputItems(TagPrefix.wireFine, GTMaterials.UraniumRhodiumDinaquadide, 64)
                .inputItems(TagPrefix.wireFine, GTMaterials.UraniumRhodiumDinaquadide, 64)
                .inputItems(TagPrefix.wireFine, GTMaterials.UraniumRhodiumDinaquadide, 64)
                .inputItems(TagPrefix.plateDouble, GTMaterials.Tantalum, 8)
                .inputItems(TagPrefix.plateDouble, GTMaterials.Silver, 8)
                .inputItems(TagPrefix.plateDouble, GTMaterials.Silicon, 8)
                .inputItems(TagPrefix.plateDouble, GTMaterials.Ruthenium, 8)
                .inputFluids(GTNAMaterials.Indalloy140.getFluid(2880))
                .inputFluids(com.raishxn.gtna.common.data.material.GodforgeChainMaterials.MutatedLivingSolder
                        .getFluid(2880))
                .inputFluids(GTMaterials.SolderingAlloy.getFluid(5760))
                .inputFluids(GTMaterials.EnrichedNaquadahTriniumEuropiumDuranide.getFluid(5760))
                .outputItems(GTNAMegaMachines.SUPERCONDUCTING_ELECTROMAGNETISM.asStack())
                .EUt(7864320).duration(1200)
                .stationResearch(b -> b.researchStack(GTNABlocks.IMPROVED_SUPERCONDUCTOR_COIL.asStack()).CWUt(256)
                        .EUt(7864320))
                .save(provider);

        // GTO UHV Arc Furnace -> UV; Adamantine wire -> Europium; Highly Insulating Foil -> Polybenzimidazole foil;
        // MgO ceramic flakes -> MgO ceramic block (GTNA); Carbon Nanotubes / Titan Precision Steel -> Polybenzimidazole
        // /
        // Naquadah Alloy.
        GTRecipeTypes.ASSEMBLY_LINE_RECIPES.recipeBuilder(GTNACORE.id("mega/magnetic_energy_reaction_furnace"))
                .inputItems(CustomTags.UIV_CIRCUITS, 32)
                .inputItems(GTMachines.ARC_FURNACE[GTValues.UV].asStack(32))
                .inputItems(TagPrefix.wireGtHex, GTMaterials.Europium, 4)
                .inputItems(TagPrefix.wireGtHex, GTMaterials.RutheniumTriniumAmericiumNeutronate, 4)
                .inputItems(GTItems.EMITTER_UEV.asStack(16))
                .inputItems(GTMachines.HI_AMP_TRANSFORMER_2A[GTValues.UEV].asStack(4))
                .inputItems(GTMachines.HI_AMP_TRANSFORMER_4A[GTValues.UEV].asStack(4))
                .inputItems(GTMachines.TRANSFORMER[GTValues.UEV].asStack(4))
                .inputItems(TagPrefix.plate, GTMaterials.Polybenzimidazole, 16)
                .inputItems(TagPrefix.foil, GTMaterials.Polycaprolactam, 32)
                .inputItems(GTNABlocks.MAGNESIUM_OXIDE_CERAMIC_HIGH_TEMPERATURE_INSULATION_MECHANICAL_BLOCK.asStack(16))
                .inputFluids(com.raishxn.gtna.common.data.material.GodforgeChainMaterials.MutatedLivingSolder
                        .getFluid(10000))
                .inputFluids(GTMaterials.Polybenzimidazole.getFluid(8128))
                .inputFluids(GTMaterials.Antimony.getFluid(8128))
                .inputFluids(GTMaterials.NaquadahAlloy.getFluid(8128))
                .outputItems(GTNAMegaMachines.MAGNETIC_ENERGY_REACTION_FURNACE.asStack())
                .EUt(4194303).duration(800)
                .stationResearch(b -> b.researchStack(GTMachines.ARC_FURNACE[GTValues.UV].asStack()).CWUt(288)
                        .EUt(7680))
                .save(provider);

        // GTO UEV Canner -> UV; Lafium -> Naquadah Alloy; Orichalcum / Mithril plasma -> Nickel / Iron plasma.
        GTRecipeTypes.ASSEMBLY_LINE_RECIPES.recipeBuilder(GTNACORE.id("mega/particle_stream_matrix_filling_machine"))
                .inputItems(GTMachines.CANNER[GTValues.UV].asStack(16))
                .inputItems(GTItems.ROBOT_ARM_UEV.asStack(16))
                .inputItems(GTItems.ELECTRIC_PISTON_UEV.asStack(32))
                .inputItems(GTItems.ELECTRIC_PUMP_UEV.asStack(64))
                .inputItems(TagPrefix.plateDouble, GTMaterials.NaquadahAlloy, 32)
                .inputItems(TagPrefix.plateDouble, GTMaterials.Naquadria, 32)
                .inputItems(CustomTags.UIV_CIRCUITS, 32)
                .inputFluids(GTMaterials.Naquadria.getFluid(4608))
                .inputFluids(GTMaterials.Nickel.getFluid(com.gregtechceu.gtceu.api.fluids.store.FluidStorageKeys.PLASMA,
                        2304))
                .inputFluids(GTMaterials.Iron.getFluid(com.gregtechceu.gtceu.api.fluids.store.FluidStorageKeys.PLASMA,
                        2304))
                .inputFluids(GTMaterials.Darmstadtium.getFluid(4608))
                .outputItems(GTNAMegaMachines.PARTICLE_STREAM_MATRIX_FILLING_MACHINE.asStack())
                .EUt(7864320).duration(800)
                .stationResearch(b -> b.researchStack(GTMachines.CANNER[GTValues.UV].asStack()).CWUt(256)
                        .EUt(7864320))
                .save(provider);

        // ---- G-0210 ----
        // GTO High Durability Compound Steel screws / Naquadah nanites -> Neutronium screws / Quantum Star.
        GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder(GTNACORE.id("mega/hyper_core"))
                .inputItems(TagPrefix.screw, GTMaterials.Naquadria, 16)
                .inputItems(TagPrefix.frameGt, GTMaterials.Naquadria, 4)
                .inputItems(TagPrefix.plate, GTMaterials.Naquadria, 4)
                .inputItems(GTItems.FIELD_GENERATOR_UEV.asStack(2))
                .inputItems(GTItems.QUANTUM_STAR.asStack())
                .inputItems(GTItems.SENSOR_UEV.asStack())
                .inputItems(GTItems.EMITTER_UEV.asStack())
                .inputItems(CustomTags.UEV_CIRCUITS)
                .inputFluids(com.raishxn.gtna.common.data.material.GodforgeChainMaterials.MutatedLivingSolder
                        .getFluid(288))
                .outputItems(GTNABlocks.HYPER_CORE.asStack())
                .cleanroom(com.gregtechceu.gtceu.api.machine.multiblock.CleanroomType.CLEANROOM)
                .EUt(7864320).duration(400).save(provider);
        // GTO Pikyonium plates -> Osmiridium.
        GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder(GTNACORE.id("mega/pikyonium_machine_casing"))
                .inputItems(TagPrefix.frameGt, GTMaterials.HastelloyX)
                .inputItems(TagPrefix.plate, GTMaterials.Osmiridium, 6)
                .circuitMeta(6)
                .outputItems(GTNABlocks.PIKYONIUM_MACHINE_CASING.asStack())
                .EUt(16).duration(50).save(provider);
        GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder(GTNACORE.id("mega/high_strength_support_spindle"))
                .inputItems(TagPrefix.frameGt, GTMaterials.BlackSteel)
                .inputItems(TagPrefix.plateDouble, GTMaterials.RhodiumPlatedPalladium, 8)
                .inputItems(TagPrefix.rodLong, GTMaterials.Naquadah, 8)
                .inputFluids(GTMaterials.Concrete.getFluid(2304))
                .outputItems(GTNABlocks.HIGH_STRENGTH_SUPPORT_SPINDLE.asStack())
                .EUt(480).duration(200).save(provider);
        GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder(GTNACORE.id("mega/quantum_glass"))
                .inputItems(GTBlocks.CASING_LAMINATED_GLASS.asStack())
                .inputItems(GTNABlocks.MOLECULAR_CASING.asStack())
                .inputFluids(GTMaterials.Trinium.getFluid(1000))
                .outputItems(GTNABlocks.QUANTUM_GLASS.asStack())
                .EUt(524288).duration(400).save(provider);

        // GTO UHV Circuit Assembler -> UV; nanites -> Quantum Star; Ceruclase plates -> Naquadria; Mithril -> Trinium.
        GTRecipeTypes.ASSEMBLY_LINE_RECIPES.recipeBuilder(GTNACORE.id("mega/nanites_circuit_assembly_factory"))
                .inputItems(GTMachines.CIRCUIT_ASSEMBLER[GTValues.UV].asStack(16))
                .inputItems(GTItems.QUANTUM_STAR.asStack(16))
                .inputItems(GTItems.SENSOR_UEV.asStack(16))
                .inputItems(GTItems.FIELD_GENERATOR_UEV.asStack(16))
                .inputItems(GTItems.ROBOT_ARM_UEV.asStack(16))
                .inputItems(CustomTags.UIV_CIRCUITS, 16)
                .inputItems(TagPrefix.plate, GTMaterials.Naquadria, 32)
                .inputFluids(GTMaterials.Trinium.getFluid(1000))
                .inputFluids(com.raishxn.gtna.common.data.material.GodforgeChainMaterials.MutatedLivingSolder
                        .getFluid(1000))
                .outputItems(GTNAMegaMachines.NANITES_CIRCUIT_ASSEMBLY_FACTORY.asStack())
                .EUt(2097152).duration(800)
                .stationResearch(b -> b.researchStack(GTMachines.CIRCUIT_ASSEMBLER[GTValues.UV].asStack()).CWUt(256))
                .save(provider);

        // GTO UHV Wiremill/Loom -> UV Wiremill x32; Abyssal Alloy wire -> Europium.
        GTRecipeTypes.ASSEMBLY_LINE_RECIPES.recipeBuilder(GTNACORE.id("mega/mega_wiremill"))
                .inputItems(GTMachines.WIREMILL[GTValues.UV].asStack(32))
                .inputItems(GTItems.ELECTRIC_MOTOR_UEV.asStack(64))
                .inputItems(GTItems.ROBOT_ARM_UEV.asStack(4))
                .inputItems(CustomTags.UIV_CIRCUITS, 4)
                .inputItems(TagPrefix.wireGtHex, GTMaterials.Europium, 8)
                .inputItems(TagPrefix.plateDouble, GTMaterials.Germanium, 32)
                .inputItems(TagPrefix.plateDouble, GTMaterials.MaragingSteel300, 16)
                .inputFluids(com.raishxn.gtna.common.data.material.GodforgeChainMaterials.MutatedLivingSolder
                        .getFluid(2304))
                .inputFluids(GTMaterials.Niobium.getFluid(4608))
                .inputFluids(GTMaterials.TantalumCarbide.getFluid(4608))
                .inputFluids(GTMaterials.Tritanium.getFluid(4608))
                .outputItems(GTNAMegaMachines.MEGA_WIREMILL.asStack())
                .EUt(7864320).duration(800)
                .stationResearch(b -> b.researchStack(GCYMMachines.LARGE_WIREMILL.asStack()).CWUt(256).EUt(7864320))
                .save(provider);

        // GTO UEV Autoclave + Large Crystallization Chamber -> UV Autoclave x32; Adamantium rotor -> Chromium;
        // Neutronium nanites -> Quantum Star; Titan Steel cable -> Europium wire.
        GTRecipeTypes.ASSEMBLY_LINE_RECIPES.recipeBuilder(GTNACORE.id("mega/crystal_builder"))
                .inputItems(GTMachines.AUTOCLAVE[GTValues.UV].asStack(32))
                .inputItems(GTItems.EMITTER_UHV.asStack(32))
                .inputItems(GTItems.ELECTRIC_PUMP_UHV.asStack(64))
                .inputItems(TagPrefix.rotor, GTMaterials.Chromium, 32)
                .inputItems(GTItems.QUANTUM_STAR.asStack(16))
                .inputItems(CustomTags.UEV_CIRCUITS, 32)
                .inputItems(TagPrefix.wireGtOctal, GTMaterials.Europium, 16)
                .inputItems(TagPrefix.plateDouble, GTMaterials.Tritanium, 32)
                .inputFluids(GTMaterials.Lanthanum.getFluid(2304))
                .inputFluids(GTMaterials.CobaltBrass.getFluid(5760))
                .inputFluids(GTMaterials.BatteryAlloy.getFluid(5760))
                .inputFluids(GTMaterials.MolybdenumDisilicide.getFluid(1296))
                .outputItems(GTNAMegaMachines.CRYSTAL_BUILDER.asStack())
                .EUt(7864320).duration(600)
                .stationResearch(b -> b.researchStack(GCYMMachines.LARGE_AUTOCLAVE.asStack()).CWUt(256).EUt(7864320))
                .save(provider);

        // ---- G-0243 ----
        VanillaRecipeHelper.addShapedRecipe(provider, true, GTNACORE.id("mega/iridium_pipe_casing"),
                GTNABlocks.IRIDIUM_PIPE_CASING.asStack(), "ABA", "BCB", "ABA",
                'A', new MaterialEntry(TagPrefix.plate, GTMaterials.Iridium),
                'B', new MaterialEntry(TagPrefix.pipeNormalFluid, GTMaterials.Iridium),
                'C', new MaterialEntry(TagPrefix.frameGt, GTMaterials.Iridium));
        GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder(GTNACORE.id("mega/iridium_gearbox"))
                .inputItems(TagPrefix.plate, GTMaterials.Iridium, 4)
                .inputItems(TagPrefix.gear, GTMaterials.Iridium, 2)
                .inputItems(TagPrefix.frameGt, GTMaterials.Iridium)
                .circuitMeta(4)
                .outputItems(GTNABlocks.IRIDIUM_GEARBOX.asStack())
                .EUt(16).duration(50).save(provider);
        // GTO Laser Cooling Unit -> UV Electric Pump; UHV Voltage Coil -> UV; Zirconium Carbide -> Tungsten Carbide;
        // Fluxed Electrum / Zeron-100 double plates -> Rhodium-Plated Palladium / Naquadah Alloy.
        GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder(GTNACORE.id("mega/laser_cooling_casing"))
                .inputItems(TagPrefix.frameGt, GTMaterials.HSSE)
                .inputItems(GTItems.ELECTRIC_PUMP_UV.asStack())
                .inputItems(GTItems.VOLTAGE_COIL_UV.asStack(2))
                .inputItems(TagPrefix.plate, GTMaterials.TungstenCarbide, 6)
                .inputItems(TagPrefix.plateDouble, GTMaterials.RhodiumPlatedPalladium, 2)
                .inputItems(TagPrefix.plateDouble, GTMaterials.NaquadahAlloy, 4)
                .inputFluids(GTMaterials.SolderingAlloy.getFluid(576))
                .outputItems(GTNABlocks.LASER_COOLING_CASING.asStack())
                .EUt(1966080).duration(200).save(provider);
        // GTO Laser Diode -> UV Emitter; same swaps as the Laser Cooling Casing.
        GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder(GTNACORE.id("mega/high_energy_laser_emitter"))
                .inputItems(TagPrefix.frameGt, GTMaterials.Trinium)
                .inputItems(GCYMBlocks.CASING_LASER_SAFE_ENGRAVING.asStack())
                .inputItems(GTItems.EMITTER_UHV.asStack(4))
                .inputItems(TagPrefix.lens, GTMaterials.Ruby)
                .inputItems(GTItems.EMITTER_UV.asStack())
                .inputItems(GTItems.VOLTAGE_COIL_UV.asStack())
                .inputItems(TagPrefix.plate, GTMaterials.TungstenCarbide, 6)
                .inputItems(TagPrefix.plateDouble, GTMaterials.RhodiumPlatedPalladium, 2)
                .inputItems(TagPrefix.plateDouble, GTMaterials.NaquadahAlloy, 4)
                .inputFluids(GTMaterials.SolderingAlloy.getFluid(576))
                .outputItems(GTNABlocks.HIGH_ENERGY_LASER_EMITTER.asStack())
                .EUt(480).duration(2222).save(provider);

        // GTO UHV Lathe -> UV; Laser Diode -> UV Emitter; Mendelevium -> Europium; Pedot / High Durability Compound
        // Steel -> Polybenzimidazole / Tritanium.
        GTRecipeTypes.ASSEMBLY_LINE_RECIPES.recipeBuilder(GTNACORE.id("mega/high_energy_laser_lathe"))
                .inputItems(GTMachines.LATHE[GTValues.UV].asStack(16))
                .inputItems(GTItems.CONVEYOR_MODULE_UEV.asStack(16))
                .inputItems(GTItems.EMITTER_UEV.asStack(32))
                .inputItems(GTItems.SENSOR_UEV.asStack(8))
                .inputItems(GTItems.EMITTER_UV.asStack(32))
                .inputItems(CustomTags.UIV_CIRCUITS, 8)
                .inputItems(TagPrefix.rod, GTMaterials.Plutonium241, 32)
                .inputItems(TagPrefix.plateDouble, GTMaterials.Europium, 32)
                .inputFluids(GTMaterials.Polybenzimidazole.getFluid(2304))
                .inputFluids(com.raishxn.gtna.common.data.material.GodforgeChainMaterials.MutatedLivingSolder
                        .getFluid(2304))
                .inputFluids(GTMaterials.Tritanium.getFluid(2304))
                .inputFluids(GTMaterials.TitaniumTungstenCarbide.getFluid(2304))
                .outputItems(GTNAMegaMachines.HIGH_ENERGY_LASER_LATHE.asStack())
                .EUt(2097152).duration(800)
                .stationResearch(b -> b.researchStack(GTMachines.LATHE[GTValues.UV].asStack()).CWUt(256)
                        .EUt(2097152))
                .save(provider);

        // GTO UHV Compressor + Gas Compressor -> UV Compressor x24; Ceruclase / Quicksilver -> Naquadria / Osmiridium;
        // High Durability Compound Steel -> Tritanium.
        GTRecipeTypes.ASSEMBLY_LINE_RECIPES.recipeBuilder(GTNACORE.id("mega/extreme_compressor"))
                .inputItems(GTMachines.COMPRESSOR[GTValues.UV].asStack(24))
                .inputItems(GTItems.ELECTRIC_PUMP_UEV.asStack(8))
                .inputItems(GTItems.ELECTRIC_PISTON_UEV.asStack(16))
                .inputItems(GTItems.ROBOT_ARM_UEV.asStack(8))
                .inputItems(GTItems.CONVEYOR_MODULE_UEV.asStack(7))
                .inputItems(CustomTags.UIV_CIRCUITS, 8)
                .inputItems(TagPrefix.plateDouble, GTMaterials.Naquadria, 32)
                .inputItems(TagPrefix.plateDouble, GTMaterials.Osmiridium, 32)
                .inputFluids(com.raishxn.gtna.common.data.material.GodforgeChainMaterials.MutatedLivingSolder
                        .getFluid(2304))
                .inputFluids(GTMaterials.Tritanium.getFluid(2304))
                .outputItems(GTNAMegaMachines.EXTREME_COMPRESSOR.asStack())
                .EUt(2097152).duration(800)
                .stationResearch(b -> b.researchStack(GCYMMachines.LARGE_MATERIAL_PRESS.asStack()).CWUt(256))
                .save(provider);

        // ---- G-0244 ----
        // GTO Zylon block / Quantanium gears / PEEK foil -> Neutronium block / Rhodium-Plated Palladium gears / PBI
        // plates.
        GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder(GTNACORE.id("mega/sps_casing"))
                .inputItems(TagPrefix.block, GTMaterials.Neutronium)
                .inputItems(GTNABlocks.RESTRAINT_DEVICE.asStack())
                .inputItems(CustomTags.UEV_CIRCUITS, 4)
                .inputItems(TagPrefix.gearSmall, GTMaterials.RhodiumPlatedPalladium, 4)
                .inputItems(TagPrefix.wireGtHex, GTMaterials.Europium)
                .inputItems(TagPrefix.plate, GTMaterials.Polybenzimidazole, 16)
                .inputFluids(com.raishxn.gtna.common.data.material.GodforgeChainMaterials.MutatedLivingSolder
                        .getFluid(576))
                .outputItems(GTNABlocks.SPS_CASING.asStack())
                .EUt(7864320).duration(800).save(provider);
        // GTO Inconel-792 / Pikyonium plates -> Inconel-625 / Osmiridium.
        GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder(GTNACORE.id("mega/space_elevator_mechanical_casing"))
                .inputItems(TagPrefix.frameGt, GTMaterials.HSSG)
                .inputItems(TagPrefix.plate, GTNAMaterials.Inconel625, 6)
                .inputItems(TagPrefix.plateDouble, GTMaterials.Osmiridium, 6)
                .circuitMeta(6)
                .outputItems(GTNABlocks.SPACE_ELEVATOR_MECHANICAL_CASING.asStack())
                .EUt(16).duration(50).save(provider);
        GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder(GTNACORE.id("mega/engineering_mechanical_casing"))
                .inputItems(TagPrefix.frameGt, GTMaterials.Ruridit)
                .inputItems(TagPrefix.plateDense, GTMaterials.Steel, 4)
                .inputFluids(GTMaterials.ReinforcedEpoxyResin.getFluid(2304))
                .outputItems(GTNABlocks.ENGINEERING_MECHANICAL_CASING.asStack())
                .EUt(480).duration(200).save(provider);
        // GTO PEEK plates -> Polybenzimidazole.
        GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder(GTNACORE.id("mega/peek_wear_resistant_mechanical_housing"))
                .inputItems(TagPrefix.frameGt, GTMaterials.Steel)
                .inputItems(TagPrefix.plate, GTMaterials.Polybenzimidazole, 6)
                .circuitMeta(6)
                .outputItems(GTNABlocks.PEEK_WEAR_RESISTANT_MECHANICAL_HOUSING.asStack())
                .EUt(16).duration(50).save(provider);
        GTRecipeTypes.ARC_FURNACE_RECIPES.recipeBuilder(GTNACORE.id("mega/industrial_frameless_glass"))
                .inputItems(GTBlocks.CASING_TEMPERED_GLASS.asStack(4))
                .inputFluids(GTMaterials.Silicon.getFluid(144))
                .outputItems(GTNABlocks.INDUSTRIAL_FRAMELESS_GLASS.asStack(4))
                .EUt(GTValues.VA[GTValues.MV]).duration(200).save(provider);

        // GTO ZPM Quantum Chest/Tank, UIV parts, Uruium nanites, Arceus/Hastelloy alloys and Transition Mix ->
        // GTNA DTPF, Infinity / Astral Titanium plates, Hassium and Trinium; research from the DTPF (GTO: Stellar
        // Forge, not ported).
        GTRecipeTypes.ASSEMBLY_LINE_RECIPES.recipeBuilder(GTNACORE.id("mega/hyperdimensional_plasma_fusion_core"))
                .inputItems(GTNAPlasmaForge.PLASMA_FORGE.asStack(4))
                .inputItems(GTMachines.QUANTUM_CHEST[GTValues.ZPM].asStack(16))
                .inputItems(GTMachines.QUANTUM_TANK[GTValues.ZPM].asStack(16))
                .inputItems(GTItems.FIELD_GENERATOR_UIV.asStack(16))
                .inputItems(GTItems.ELECTRIC_PUMP_UIV.asStack(8))
                .inputItems(TagPrefix.plate,
                        com.raishxn.gtna.common.data.material.GodforgeChainMaterials.AstralTitanium,
                        64)
                .inputItems(TagPrefix.plateDouble, GTMaterials.Neutronium, 32)
                .inputFluids(com.raishxn.gtna.common.data.material.GodforgeChainMaterials.MutatedLivingSolder
                        .getFluid(12960))
                .inputFluids(GTMaterials.Trinium.getFluid(5760))
                .inputFluids(GTMaterials.Neutronium.getFluid(5760))
                .outputItems(GTNAMegaMachines.HYPERDIMENSIONAL_PLASMA_FUSION_CORE.asStack())
                .EUt(31457280).duration(4000)
                .stationResearch(b -> b.researchStack(GTNAPlasmaForge.PLASMA_FORGE.asStack()).CWUt(4096)
                        .EUt(31457280))
                .save(provider);

        // GTO UHV Packer/Unpacker -> UV Packer x16; Inconel-625 / Hastelloy-N75 screws -> Inconel-625 / HSS-S;
        // Gold/Osmium nanites -> Quantum Star; Kevlar / Carbon Nanotubes -> Polybenzimidazole /
        // Polytetrafluoroethylene.
        GTRecipeTypes.ASSEMBLY_LINE_RECIPES.recipeBuilder(GTNACORE.id("mega/gemini_containment_system"))
                .inputItems(CustomTags.UEV_CIRCUITS, 16)
                .inputItems(GTMachines.PACKER[GTValues.UV].asStack(16))
                .inputItems(TagPrefix.screw, GTNAMaterials.Inconel625, 64)
                .inputItems(TagPrefix.screw, GTMaterials.HSSS, 64)
                .inputItems(TagPrefix.wireGtOctal, GTMaterials.EnrichedNaquadahTriniumEuropiumDuranide, 16)
                .inputItems(GTItems.QUANTUM_STAR.asStack(16))
                .inputItems(GTItems.ROBOT_ARM_UHV.asStack(64))
                .inputItems(GTItems.FIELD_GENERATOR_UHV.asStack(16))
                .inputItems(GTItems.ELECTRIC_MOTOR_UHV.asStack(16))
                .inputFluids(com.raishxn.gtna.common.data.material.GodforgeChainMaterials.MutatedLivingSolder
                        .getFluid(10000))
                .inputFluids(GTMaterials.Polybenzimidazole.getFluid(16000))
                .inputFluids(GTMaterials.Polytetrafluoroethylene.getFluid(16000))
                .outputItems(GTNAMegaMachines.GEMINI_CONTAINMENT_SYSTEM.asStack())
                .EUt(2097152).duration(800)
                .stationResearch(b -> b.researchStack(GTMachines.PACKER[GTValues.UV].asStack()).CWUt(256))
                .save(provider);

        // GTO UHV/UEV Voltage Coils, nanotube wires and Enderite -> UV Voltage Coils, Europium fine wire and Naquadah
        // Alloy wire; Depleted Uranium Alloy / Tanmolyium / Titanium Dioxide Nanotubes -> Tungstensteel /
        // Molybdenum / Titanium.
        GTRecipeTypes.ASSEMBLY_LINE_RECIPES.recipeBuilder(GTNACORE.id("mega/giant_electrochemical_workstation"))
                .inputItems(GCYMMachines.LARGE_ELECTROLYZER.asStack(16))
                .inputItems(CustomTags.UEV_CIRCUITS, 64)
                .inputItems(GTItems.EMITTER_UHV.asStack(16))
                .inputItems(GTItems.VOLTAGE_COIL_UV.asStack(32))
                .inputItems(TagPrefix.wireFine, GTMaterials.Europium, 64)
                .inputItems(TagPrefix.plateDouble, GTMaterials.RhodiumPlatedPalladium, 64)
                .inputItems(TagPrefix.plateDouble, GTMaterials.HSSS, 64)
                .inputItems(TagPrefix.plateDouble, GTMaterials.Platinum, 64)
                .inputItems(TagPrefix.wireGtDouble, GTMaterials.NaquadahAlloy, 64)
                .inputFluids(GTMaterials.TungstenSteel.getFluid(5576))
                .inputFluids(GTMaterials.Molybdenum.getFluid(4000))
                .inputFluids(GTNAMaterials.Tantalloy61.getFluid(5000))
                .inputFluids(GTMaterials.Titanium.getFluid(5000))
                .outputItems(GTNAMegaMachines.GIANT_ELECTROCHEMICAL_WORKSTATION.asStack())
                .EUt(GTValues.VA[GTValues.UHV]).duration(800)
                .stationResearch(b -> b.researchStack(GCYMMachines.LARGE_ELECTROLYZER.asStack()).CWUt(256))
                .save(provider);

        // ---- G-0245 ----
        // Desulfurizer recipes, 1:1 from GTO.
        var desulf = com.raishxn.gtna.common.data.GTNARecipeType.DESULFURIZER_RECIPES;
        Object[][] fuels = {
                { "naphtha", GTMaterials.SulfuricNaphtha, GTMaterials.Naphtha, 12000 },
                { "light_fuel", GTMaterials.SulfuricLightFuel, GTMaterials.LightFuel, 12000 },
                { "heavy_fuel", GTMaterials.SulfuricHeavyFuel, GTMaterials.HeavyFuel, 12000 },
                { "gas", GTMaterials.SulfuricGas, GTMaterials.RefineryGas, 16000 },
                { "natural_gas", GTMaterials.NaturalGas, GTMaterials.RefineryGas, 16000 } };
        for (Object[] fuel : fuels) {
            int amount = (int) fuel[3];
            desulf.recipeBuilder(GTNACORE.id((String) fuel[0]))
                    .inputFluids(((com.gregtechceu.gtceu.api.data.chemical.material.Material) fuel[1]).getFluid(amount))
                    .outputItems(TagPrefix.dust, GTMaterials.Sulfur)
                    .outputFluids(
                            ((com.gregtechceu.gtceu.api.data.chemical.material.Material) fuel[2]).getFluid(amount))
                    .EUt(30).duration(120).save(provider);
        }
        // Loom: the AE2 dense cables from GTO (its plant/algae fibre recipes use GTO-only items).
        var loom = com.raishxn.gtna.common.data.GTNARecipeType.LOOM_RECIPES;
        for (String cable : new String[] { "covered", "smart" }) {
            loom.recipeBuilder(GTNACORE.id("fluix_" + cable + "_dense_cable"))
                    .inputItems(
                            new net.minecraft.world.item.ItemStack(net.minecraftforge.registries.ForgeRegistries.ITEMS
                                    .getValue(new net.minecraft.resources.ResourceLocation("ae2",
                                            "fluix_" + cable + "_cable")),
                                    4))
                    .outputItems(
                            new net.minecraft.world.item.ItemStack(net.minecraftforge.registries.ForgeRegistries.ITEMS
                                    .getValue(new net.minecraft.resources.ResourceLocation("ae2",
                                            "fluix_" + cable + "_dense_cable"))))
                    .EUt(32).duration(5).save(provider);
        }
        // Rare Earth Centrifugal: GTO Rare Earth Metal dust -> GTCEu Rare Earth dust.
        com.raishxn.gtna.common.data.GTNARecipeType.RARE_EARTH_CENTRIFUGAL_RECIPES
                .recipeBuilder(GTNACORE.id("rare_earth"))
                .inputItems(TagPrefix.dust, GTMaterials.RareEarth)
                .outputItems(TagPrefix.dustSmall, GTMaterials.Lanthanum)
                .outputItems(TagPrefix.dustSmall, GTMaterials.Cerium)
                .outputItems(TagPrefix.dustSmall, GTMaterials.Neodymium)
                .outputItems(TagPrefix.dustSmall, GTMaterials.Samarium)
                .outputItems(TagPrefix.dustSmall, GTMaterials.Europium)
                .outputItems(TagPrefix.dustSmall, GTMaterials.Gadolinium)
                .outputItems(TagPrefix.dustSmall, GTMaterials.Yttrium)
                .EUt(491520).duration(200).save(provider);

        // Blocks. GTO composites / structural steels -> nearest GTCEu alloys (noted per block).
        // GTO Tungsten Fiber Cobalt / SiC Fiber Titanium composites, GRCop-84 -> Tungsten Carbide, Titanium
        // Carbide, Copper.
        GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder(GTNACORE.id("mega/smelting_control_casing"))
                .inputItems(TagPrefix.frameGt, GTMaterials.Naquadah)
                .inputItems(TagPrefix.plate, GTMaterials.TungstenCarbide, 4)
                .inputItems(TagPrefix.plate, GTMaterials.TitaniumCarbide, 2)
                .inputItems(CustomTags.LuV_CIRCUITS)
                .inputFluids(GTMaterials.Copper.getFluid(576))
                .outputItems(GTNABlocks.SMELTING_CONTROL_CASING.asStack())
                .EUt(16).duration(50).save(provider);
        // GTO Structural Steel Q690 / Tungsten Alloy YG10 -> Steel / Tungsten Carbide.
        GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder(GTNACORE.id("mega/stable_base_casing"))
                .inputItems(TagPrefix.plate, GTMaterials.Steel, 2)
                .inputItems(TagPrefix.plate, GTMaterials.TungstenCarbide, 4)
                .inputItems(TagPrefix.frameGt, GTMaterials.TungstenSteel)
                .outputItems(GTNABlocks.STABLE_BASE_CASING.asStack())
                .EUt(16).duration(50).save(provider);
        // GTO Inconel-242 plates -> Inconel-625.
        GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder(GTNACORE.id("mega/insulation_tile_mechanical_block"))
                .inputItems(TagPrefix.frameGt, GTMaterials.Ultimet)
                .inputItems(TagPrefix.pipeSmallFluid, GTMaterials.Copper, 10)
                .inputItems(TagPrefix.plate, GTNAMaterials.Inconel625, 6)
                .circuitMeta(6)
                .outputItems(GTNABlocks.INSULATION_TILE_MECHANICAL_BLOCK.asStack())
                .EUt(16).duration(50).save(provider);
        // GTO GlassRecipe: borosilicate glass + 1152 mB HSS-S in the solidifier.
        GTRecipeTypes.FLUID_SOLIDFICATION_RECIPES.recipeBuilder(GTNACORE.id("mega/hsss_borosilicate_glass"))
                .inputItems(GTBlocks.CASING_TEMPERED_GLASS.asStack())
                .inputFluids(GTMaterials.HSSS.getFluid(1152))
                .outputItems(GTNABlocks.HSSS_BOROSILICATE_GLASS.asStack())
                .EUt(GTValues.VA[GTValues.LuV]).duration(200).save(provider);
        // GTO Advanced Stellar Containment Casing, Vibramantium, Legendarium, Heavy Quark Matter, Celestial Tungsten
        // -> Molecular Casing, Neutronium, Europium wire, Astral Titanium and Trinium.
        GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder(GTNACORE.id("mega/ultimate_stellar_containment_casing"))
                .inputItems(GTNABlocks.MOLECULAR_CASING.asStack())
                .inputItems(GTItems.FIELD_GENERATOR_UEV.asStack())
                .inputItems(TagPrefix.screw, GTMaterials.Neutronium, 8)
                .inputItems(TagPrefix.wireGtQuadruple, GTMaterials.Europium)
                .inputItems(TagPrefix.plate,
                        com.raishxn.gtna.common.data.material.GodforgeChainMaterials.AstralTitanium,
                        8)
                .inputFluids(GTMaterials.Trinium.getFluid(144))
                .outputItems(GTNABlocks.ULTIMATE_STELLAR_CONTAINMENT_CASING.asStack())
                .EUt(31457280).duration(460).save(provider);
        // GTO Amprosium -> Neutronium (as for the other Amprosium blocks).
        GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder(GTNACORE.id("mega/amprosium_casing"))
                .inputItems(TagPrefix.frameGt, GTMaterials.Neutronium)
                .inputItems(TagPrefix.plate, GTMaterials.Neutronium, 6)
                .circuitMeta(6)
                .outputItems(GTNABlocks.AMPROSIUM_CASING.asStack())
                .EUt(16).duration(50).save(provider);

        // Controllers.
        VanillaRecipeHelper.addShapedRecipe(provider, true, GTNACORE.id("mega/desulfurizer"),
                GTNAMegaMachines.DESULFURIZER.asStack(), "ABA", "CDC", "ABA",
                'A', GTItems.ELECTRIC_PUMP_HV.asStack(), 'B', GTItems.ELECTRIC_MOTOR_HV.asStack(),
                'C', CustomTags.EV_CIRCUITS, 'D', GTMachines.HULL[GTValues.HV].asStack());
        // GTO UHV Laser Engraver -> UV; Neutronium nanites -> Quantum Star; Quantanium -> Trinium; PEEK / Pikyonium /
        // Abyssal Alloy -> Polybenzimidazole / Osmiridium / Neutronium.
        GTRecipeTypes.ASSEMBLY_LINE_RECIPES.recipeBuilder(GTNACORE.id("mega/dimensional_focus_engraving_array"))
                .inputItems(GTMachines.LASER_ENGRAVER[GTValues.UV].asStack(16))
                .inputItems(GTItems.QUANTUM_STAR.asStack(16))
                .inputItems(GTItems.FIELD_GENERATOR_UEV.asStack(32))
                .inputItems(GTItems.EMITTER_UEV.asStack(64))
                .inputItems(CustomTags.UIV_CIRCUITS, 32)
                .inputItems(TagPrefix.rod, GTMaterials.Trinium, 16)
                .inputItems(TagPrefix.plateDouble, GTMaterials.Neutronium, 32)
                .inputFluids(com.raishxn.gtna.common.data.material.GodforgeChainMaterials.MutatedLivingSolder
                        .getFluid(28800))
                .inputFluids(GTMaterials.Polybenzimidazole.getFluid(28800))
                .inputFluids(GTMaterials.Osmiridium.getFluid(4608))
                .inputFluids(GTMaterials.Neutronium.getFluid(4608))
                .outputItems(GTNAMegaMachines.DIMENSIONAL_FOCUS_ENGRAVING_ARRAY.asStack())
                .EUt(7864320).duration(1600)
                .stationResearch(b -> b.researchStack(GTNAMegaMachines.ENGRAVING_LASER_PLANT.asStack()).CWUt(256)
                        .EUt(7864320))
                .save(provider);
        // GTO Stellar Forge, UIV furnaces, Transcendent battery, Vibranium/Vibramantium, Germanium Tungsten Nitride,
        // Abyssal Alloy -> DTPF, UV furnaces, Astral Titanium, Neutronium, Tungsten Carbide.
        GTRecipeTypes.ASSEMBLY_LINE_RECIPES
                .recipeBuilder(GTNACORE.id("mega/star_ultimate_material_forge_factory"))
                .inputItems(GTNAPlasmaForge.PLASMA_FORGE.asStack(4))
                .inputItems(GTMachines.ELECTRIC_FURNACE[GTValues.UV].asStack(4))
                .inputItems(GTMachines.ARC_FURNACE[GTValues.UV].asStack(4))
                .inputItems(GTMachines.ALLOY_SMELTER[GTValues.UV].asStack(4))
                .inputItems(GTItems.ELECTRIC_PUMP_UIV.asStack(16))
                .inputItems(GTItems.SENSOR_UXV.asStack(4))
                .inputItems(CustomTags.UXV_CIRCUITS, 16)
                .inputItems(GTNABlocks.CONTAINMENT_FIELD_GENERATOR.asStack(8))
                .inputItems(GTNABlocks.HYPER_CORE.asStack(8))
                .inputItems(TagPrefix.plate,
                        com.raishxn.gtna.common.data.material.GodforgeChainMaterials.AstralTitanium,
                        64)
                .inputItems(TagPrefix.plateDouble, GTMaterials.Neutronium, 32)
                .inputFluids(GTMaterials.IncoloyMA956.getFluid(5760))
                .inputFluids(GTMaterials.TungstenCarbide.getFluid(5760))
                .inputFluids(GTMaterials.Neutronium.getFluid(5760))
                .inputFluids(GTMaterials.TitaniumCarbide.getFluid(5760))
                .outputItems(GTNAMegaMachines.STAR_ULTIMATE_MATERIAL_FORGE_FACTORY.asStack())
                .EUt(31457280).duration(1200)
                .stationResearch(b -> b.researchStack(GTNABlocks.ULTIMATE_STELLAR_CONTAINMENT_CASING.asStack())
                        .CWUt(1024).EUt(31457280))
                .save(provider);
        // GTO UHV Loom, Mithril/Adamantine wire, Lemurite, Infuscolium/Quantanium gears, Kevlar -> UV Wiremill,
        // Europium / Naquadah Alloy wire, Tritanium, Rhodium-Plated Palladium / Osmiridium gears, Polybenzimidazole.
        GTRecipeTypes.ASSEMBLY_LINE_RECIPES.recipeBuilder(GTNACORE.id("mega/hand_of_arachne"))
                .inputItems(CustomTags.UIV_CIRCUITS, 16)
                .inputItems(GTMachines.WIREMILL[GTValues.UV].asStack(16))
                .inputItems(TagPrefix.wireGtSingle, GTMaterials.Europium, 64)
                .inputItems(TagPrefix.wireGtSingle, GTMaterials.NaquadahAlloy, 64)
                .inputItems(TagPrefix.plateDouble, GTMaterials.HastelloyC276, 16)
                .inputItems(TagPrefix.plateDouble, GTMaterials.Tritanium, 8)
                .inputItems(TagPrefix.gearSmall, GTMaterials.RhodiumPlatedPalladium, 16)
                .inputItems(TagPrefix.gearSmall, GTMaterials.Osmiridium, 8)
                .inputFluids(GTMaterials.Polybenzimidazole.getFluid(2304))
                .inputFluids(GTMaterials.TantalumCarbide.getFluid(4608))
                .inputFluids(GTMaterials.Cobalt.getFluid(9216))
                .outputItems(GTNAMegaMachines.HAND_OF_ARACHNE.asStack())
                .EUt(16777215).duration(720)
                .stationResearch(b -> b.researchStack(GTMachines.WIREMILL[GTValues.UV].asStack()).CWUt(256))
                .save(provider);
        // GTO Mithril long rods / Stellite plates -> Naquadah Alloy / Osmiridium.
        GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder(GTNACORE.id("mega/rare_earth_centrifugal"))
                .inputItems(TagPrefix.plate, GTMaterials.Europium, 8)
                .inputItems(GTItems.ELECTRIC_MOTOR_UHV.asStack(16))
                .inputItems(TagPrefix.gear, GTMaterials.HSSS, 16)
                .inputItems(TagPrefix.rodLong, GTMaterials.NaquadahAlloy, 8)
                .inputItems(TagPrefix.plate, GTMaterials.HSSE, 16)
                .inputItems(TagPrefix.wireFine, GTMaterials.Naquadria, 64)
                .inputItems(CustomTags.UHV_CIRCUITS, 4)
                .inputItems(TagPrefix.plate, GTMaterials.Osmiridium, 32)
                .inputFluids(GTMaterials.SolderingAlloy.getFluid(1296))
                .outputItems(GTNAMegaMachines.RARE_EARTH_CENTRIFUGAL.asStack())
                .EUt(7864320).duration(1000).save(provider);
        // GTO UHV Rolling/Cluster -> UV Bender x16; Orichalcum / Lemurite / High Durability Compound Steel ->
        // Naquadah Alloy / Tritanium; research from the GCYM Large Material Press (the GTO Large Rolling).
        GTRecipeTypes.ASSEMBLY_LINE_RECIPES.recipeBuilder(GTNACORE.id("mega/heavy_rolling"))
                .inputItems(GTMachines.BENDER[GTValues.UV].asStack(16))
                .inputItems(GTItems.CONVEYOR_MODULE_UEV.asStack(16))
                .inputItems(GTItems.ELECTRIC_PISTON_UEV.asStack(8))
                .inputItems(GTItems.ELECTRIC_MOTOR_UEV.asStack(8))
                .inputItems(CustomTags.UIV_CIRCUITS, 8)
                .inputItems(TagPrefix.rodLong, GTMaterials.NaquadahAlloy, 16)
                .inputItems(TagPrefix.plateDouble, GTMaterials.Tritanium, 16)
                .inputFluids(GTMaterials.Tritanium.getFluid(2304))
                .inputFluids(com.raishxn.gtna.common.data.material.GodforgeChainMaterials.MutatedLivingSolder
                        .getFluid(2304))
                .inputFluids(GTMaterials.Indium.getFluid(2304))
                .inputFluids(GTMaterials.SolderingAlloy.getFluid(2304))
                .outputItems(GTNAMegaMachines.HEAVY_ROLLING.asStack())
                .EUt(2097152).duration(800)
                .stationResearch(b -> b.researchStack(GCYMMachines.LARGE_MATERIAL_PRESS.asStack()).CWUt(256))
                .save(provider);

        // ---- G-0246 ----
        GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder(GTNACORE.id("mega/high_energy_ultraviolet_emitter_casing"))
                .inputItems(TagPrefix.frameGt, GTMaterials.Tritanium)
                .inputItems(GTItems.EMITTER_UV.asStack())
                .inputItems(TagPrefix.plate, GTMaterials.Naquadria, 4)
                .inputFluids(
                        GTMaterials.Titanium.getFluid(com.gregtechceu.gtceu.api.fluids.store.FluidStorageKeys.PLASMA,
                                576))
                .outputItems(GTNABlocks.HIGH_ENERGY_ULTRAVIOLET_EMITTER_CASING.asStack())
                .EUt(7680).duration(200).save(provider);
        GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder(GTNACORE.id("mega/pps_corrosion_resistant_mechanical_housing"))
                .inputItems(TagPrefix.frameGt, GTMaterials.Polytetrafluoroethylene)
                .inputItems(TagPrefix.plate, GTMaterials.PolyphenyleneSulfide, 6)
                .circuitMeta(6)
                .outputItems(GTNABlocks.PPS_CORROSION_RESISTANT_MECHANICAL_HOUSING.asStack())
                .EUt(16).duration(50).save(provider);
        GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder(GTNACORE.id("mega/plasma_heater_casing"))
                .inputItems(TagPrefix.frameGt, GTMaterials.Trinium)
                .inputItems(GTItems.VOLTAGE_COIL_LuV.asStack(2))
                .inputItems(TagPrefix.plate, GTMaterials.Rhenium, 2)
                .inputItems(TagPrefix.screw, GTMaterials.Tungsten, 8)
                .inputItems(TagPrefix.plate, GTMaterials.Trinium, 4)
                .inputFluids(GTMaterials.Osmiridium.getFluid(288))
                .outputItems(GTNABlocks.PLASMA_HEATER_CASING.asStack())
                .EUt(120).duration(200).save(provider);
        // GTO Trinaquadalloy double plates -> Naquadah Alloy.
        GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder(GTNACORE.id("mega/gravity_stabilization_casing"))
                .inputItems(TagPrefix.frameGt, GTMaterials.Neutronium)
                .inputItems(GTItems.GRAVI_STAR.asStack())
                .inputItems(GTItems.NEUTRON_REFLECTOR.asStack(2))
                .inputItems(TagPrefix.plateDouble, GTMaterials.NaquadahAlloy, 5)
                .inputFluids(GTMaterials.Neutronium.getFluid(576))
                .outputItems(GTNABlocks.GRAVITY_STABILIZATION_CASING.asStack())
                .EUt(480).duration(400).save(provider);

        // GTO UHV Arc Generator, End Steel wire, MgO flakes, Ruby/Hui circuits, Lemurite, Quicksilver/Mithril ->
        // UV Arc Furnace, Europium wire, MgO ceramic block, UV/UHV circuits, Tritanium, Naquadah Alloy.
        GTRecipeTypes.ASSEMBLY_LINE_RECIPES.recipeBuilder(GTNACORE.id("mega/lightning_rod"))
                .inputItems(GTMachines.ARC_FURNACE[GTValues.UV].asStack(16))
                .inputItems(TagPrefix.wireGtHex, GTMaterials.Europium, 64)
                .inputItems(GTNABlocks.MAGNESIUM_OXIDE_CERAMIC_HIGH_TEMPERATURE_INSULATION_MECHANICAL_BLOCK.asStack(32))
                .inputItems(CustomTags.UHV_CIRCUITS, 32)
                .inputItems(CustomTags.UIV_CIRCUITS, 16)
                .inputItems(TagPrefix.plate, GTMaterials.Tritanium, 32)
                .inputFluids(com.raishxn.gtna.common.data.material.GodforgeChainMaterials.MutatedLivingSolder
                        .getFluid(2304))
                .inputFluids(GTMaterials.NaquadahAlloy.getFluid(2304))
                .inputFluids(GTMaterials.Naquadria.getFluid(2304))
                .outputItems(GTNAMegaMachines.LIGHTNING_ROD.asStack())
                .EUt(2097152).duration(800)
                .stationResearch(b -> b.researchStack(GCYMMachines.LARGE_ARC_SMELTER.asStack()).CWUt(256))
                .save(provider);
        // GTO Chemical Plant, Iridium/Silver nanites, Grisium, Indalloy -> Large Chemical Reactor, Gold nanites,
        // Naquadah Alloy, Indium; research from a UV Circuit Assembler (GTO: its own circuit board).
        GTRecipeTypes.ASSEMBLY_LINE_RECIPES.recipeBuilder(GTNACORE.id("mega/pcb_factory"))
                .inputItems(TagPrefix.frameGt, GTMaterials.Neutronium, 4)
                .inputItems(GTMachines.CIRCUIT_ASSEMBLER[GTValues.UV].asStack(4))
                .inputItems(GTMultiMachines.LARGE_CHEMICAL_REACTOR.asStack(4))
                .inputItems(CustomTags.UHV_CIRCUITS, 16)
                .inputItems(GTItems.ROBOT_ARM_UV.asStack(16))
                .inputItems(GTItems.ELECTRIC_PUMP_UV.asStack(16))
                .inputItems(GTItems.SENSOR_UV.asStack(4))
                .inputItems(GTItems.EMITTER_UV.asStack(4))
                .inputItems(GTItems.FIELD_GENERATOR_UV.asStack())
                .inputItems(com.raishxn.gtna.common.data.GTNANanoForge.GOLD_NANITES.asStack(2))
                .inputItems(TagPrefix.plateDouble, GTMaterials.NaquadahAlloy, 16)
                .inputFluids(GTMaterials.SolderingAlloy.getFluid(2592))
                .inputFluids(GTMaterials.BismuthBronze.getFluid(2582))
                .inputFluids(GTMaterials.Indium.getFluid(1440))
                .inputFluids(GTMaterials.NaquadahEnriched.getFluid(1296))
                .outputItems(GTNAMegaMachines.PCB_FACTORY.asStack())
                .EUt(491520).duration(600)
                .stationResearch(b -> b.researchStack(GTMachines.CIRCUIT_ASSEMBLER[GTValues.UV].asStack()).CWUt(32)
                        .EUt(491520))
                .save(provider);
        // GTO UXV-tier Adamantine/Titan Steel/Arceus parts, lepton trap and scintillator -> Neutronium/Tritanium,
        // UXV emitters and sensors kept, Fusion Coils; Tairitsu/Cinobite -> Trinium/Naquadria.
        GTRecipeTypes.ASSEMBLY_LINE_RECIPES.recipeBuilder(GTNACORE.id("mega/space_probe_surface_reception"))
                .inputItems(TagPrefix.plateDouble, GTMaterials.Neutronium, 12)
                .inputItems(TagPrefix.gear, GTMaterials.Neutronium, 12)
                .inputItems(TagPrefix.plateDouble, GTMaterials.Tritanium, 16)
                .inputItems(CustomTags.UXV_CIRCUITS, 4)
                .inputItems(GTItems.EMITTER_UXV.asStack(4))
                .inputItems(GTItems.SENSOR_UXV.asStack(4))
                .inputItems(TagPrefix.rod, com.raishxn.gtna.common.data.material.GodforgeChainMaterials.AstralTitanium,
                        16)
                .inputItems(GTBlocks.FUSION_COIL.asStack(2))
                .inputFluids(com.raishxn.gtna.common.data.material.GodforgeChainMaterials.MutatedLivingSolder
                        .getFluid(864))
                .inputFluids(GTMaterials.Trinium.getFluid(1296))
                .inputFluids(GTMaterials.SolderingAlloy.getFluid(1296))
                .inputFluids(GTMaterials.Naquadria.getFluid(864))
                .outputItems(GTNAMegaMachines.SPACE_PROBE_SURFACE_RECEPTION.asStack())
                .EUt(GTValues.VA[GTValues.UXV]).duration(800)
                .stationResearch(b -> b.researchStack(GTItems.SENSOR_UXV.asStack()).CWUt(1024))
                .save(provider);
        // GTO Plasma Condenser, laser containers/lasers -> UV Vacuum Freezers, UV Emitters; the double plates of
        // non-dense GTCEu metals -> Naquadah Alloy / Osmiridium / Rhodium-Plated Palladium.
        GTRecipeTypes.ASSEMBLY_LINE_RECIPES.recipeBuilder(GTNACORE.id("mega/compound_extreme_cooling_unit"))
                .inputItems(TagPrefix.frameGt, GTMaterials.HSSE, 64)
                .inputItems(GCYMMachines.MEGA_VACUUM_FREEZER.asStack(16))
                .inputItems(GTNABlocks.LASER_COOLING_CASING.asStack(64))
                .inputItems(GTItems.EMITTER_UV.asStack(64))
                .inputItems(GTItems.FLUID_REGULATOR_UHV.asStack(64))
                .inputItems(GTItems.EMITTER_UEV.asStack(16))
                .inputItems(CustomTags.UIV_CIRCUITS, 16)
                .inputItems(TagPrefix.plateDouble, GTMaterials.NaquadahAlloy, 64)
                .inputItems(TagPrefix.plateDouble, GTMaterials.Osmiridium, 64)
                .inputItems(TagPrefix.plateDouble, GTMaterials.RhodiumPlatedPalladium, 64)
                .inputFluids(com.raishxn.gtna.common.data.material.GodforgeChainMaterials.MutatedLivingSolder
                        .getFluid(4608))
                .outputItems(GTNAMegaMachines.COMPOUND_EXTREME_COOLING_UNIT.asStack())
                .EUt(GTValues.VA[GTValues.UEV]).duration(1200)
                .stationResearch(b -> b.researchStack(GCYMMachines.MEGA_VACUUM_FREEZER.asStack()).CWUt(512))
                .save(provider);

        // ---- G-0247 ----
        // GTO Naquadah / Enriched Naquadah double plates -> Naquadria / Neutronium.
        GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder(GTNACORE.id("mega/enhance_hyper_mechanical_casing"))
                .inputItems(TagPrefix.frameGt, GTMaterials.Naquadria)
                .inputItems(TagPrefix.plateDouble, GTMaterials.NaquadahAlloy, 2)
                .inputItems(TagPrefix.plateDouble, GTMaterials.Naquadria, 2)
                .inputItems(TagPrefix.plateDouble, GTMaterials.Neutronium, 2)
                .inputFluids(GTMaterials.Naquadria.getFluid(576))
                .outputItems(GTNABlocks.ENHANCE_HYPER_MECHANICAL_CASING.asStack())
                .EUt(16).duration(50).save(provider);
        // GTO Reinforced Echo Shard (Deeper Darker) -> 4 vanilla Echo Shards; HSS-E double plates -> HSS-S.
        GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder(GTNACORE.id("mega/echo_casing"))
                .inputItems(TagPrefix.frameGt, GTMaterials.Europium)
                .inputItems(new net.minecraft.world.item.ItemStack(net.minecraft.world.item.Items.ECHO_SHARD, 4))
                .inputItems(TagPrefix.plateDouble, GTMaterials.HSSS, 6)
                .outputItems(GTNABlocks.ECHO_CASING.asStack())
                .EUt(30).duration(200).save(provider);
        // GTO NM chips, Orichalcum/Enderite, Naquadah nanites, Indalloy -> UV parts, Naquadria / Neutronium, Gold
        // nanites, Indium.
        GTRecipeTypes.ASSEMBLY_LINE_RECIPES.recipeBuilder(GTNACORE.id("mega/hyper_reactor"))
                .inputItems(GTItems.ULTRA_HIGH_POWER_INTEGRATED_CIRCUIT.asStack(64))
                .inputItems(CustomTags.UEV_CIRCUITS, 4)
                .inputItems(GTItems.ELECTRIC_PUMP_UEV.asStack(2))
                .inputItems(GTItems.FIELD_GENERATOR_UEV.asStack(2))
                .inputItems(TagPrefix.plateDouble, GTMaterials.Naquadria, 4)
                .inputItems(TagPrefix.plateDouble, GTMaterials.Neutronium, 4)
                .inputItems(TagPrefix.gear, GTMaterials.Naquadria, 8)
                .inputItems(com.raishxn.gtna.common.data.GTNANanoForge.GOLD_NANITES.asStack(16))
                .inputItems(TagPrefix.screw, GTMaterials.Naquadria, 32)
                .inputItems(GTItems.ULTIMATE_BATTERY.asStack())
                .inputFluids(GTMaterials.Indium.getFluid(1296))
                .inputFluids(GTMaterials.SolderingAlloy.getFluid(1296))
                .inputFluids(com.raishxn.gtna.common.data.material.GodforgeChainMaterials.MutatedLivingSolder
                        .getFluid(864))
                .outputItems(GTNAMegaMachines.HYPER_REACTOR.asStack())
                .EUt(GTValues.VA[GTValues.UEV]).duration(1200)
                .stationResearch(b -> b.researchStack(GTItems.ULTIMATE_BATTERY.asStack()).CWUt(512))
                .save(provider);
        // GTO NM/PM chips, Taranium, Infuscolium nanites, Transcendent battery, Tairitsu -> UHPIC, Trinium, Neutronium
        // nanites, a Hyper Reactor, Trinium fluid.
        GTRecipeTypes.ASSEMBLY_LINE_RECIPES.recipeBuilder(GTNACORE.id("mega/advanced_hyper_reactor"))
                .inputItems(GTNAMegaMachines.HYPER_REACTOR.asStack())
                .inputItems(GTItems.ULTRA_HIGH_POWER_INTEGRATED_CIRCUIT.asStack(64))
                .inputItems(CustomTags.UXV_CIRCUITS, 4)
                .inputItems(GTItems.ELECTRIC_PUMP_UIV.asStack(2))
                .inputItems(GTItems.FIELD_GENERATOR_UIV.asStack(2))
                .inputItems(TagPrefix.plateDouble, GTMaterials.Seaborgium, 8)
                .inputItems(TagPrefix.plateDouble, GTMaterials.Tritanium, 8)
                .inputItems(TagPrefix.gear, GTMaterials.Naquadria, 16)
                .inputItems(TagPrefix.screw, GTMaterials.Naquadria, 64)
                .inputItems(com.raishxn.gtna.common.data.GTNANanoForge.NEUTRONIUM_NANITES.asStack(64))
                .inputFluids(GTMaterials.Trinium.getFluid(2304))
                .inputFluids(GTMaterials.SolderingAlloy.getFluid(1296))
                .inputFluids(GTMaterials.Indium.getFluid(1296))
                .outputItems(GTNAMegaMachines.ADVANCED_HYPER_REACTOR.asStack())
                .EUt(GTValues.VA[GTValues.UXV]).duration(1200)
                .stationResearch(b -> b.researchStack(GTNAMegaMachines.HYPER_REACTOR.asStack()).CWUt(2048))
                .save(provider);

        // ---- G-0248: Fuel Cell Generator (GTO FuelCell + membrane electrodes) ----
        fuelCell(provider);
        supercomputing(provider);
        // GTO has no recipe for the Analysis & Research Center (its research system is dev-only): GTNA's own, one tier
        // above GTCEu's Research Station.
        GTRecipeTypes.ASSEMBLY_LINE_RECIPES.recipeBuilder(GTNACORE.id("mega/analysis_and_research_center"))
                .inputItems(com.gregtechceu.gtceu.common.data.machines.GTResearchMachines.RESEARCH_STATION.asStack(2))
                .inputItems(GTBlocks.ADVANCED_COMPUTER_CASING.asStack(16))
                .inputItems(GTBlocks.COMPUTER_HEAT_VENT.asStack(16))
                .inputItems(CustomTags.UV_CIRCUITS, 8)
                .inputItems(GTItems.SENSOR_UV.asStack(4))
                .inputItems(GTItems.EMITTER_UV.asStack(4))
                .inputItems(GTItems.TOOL_DATA_MODULE.asStack(4))
                .inputItems(GTBlocks.OPTICAL_PIPES[0].asStack(32))
                .inputFluids(GTMaterials.SolderingAlloy.getFluid(2304))
                .inputFluids(GTMaterials.Polybenzimidazole.getFluid(1152))
                .outputItems(GTNAMegaMachines.ANALYSIS_AND_RESEARCH_CENTER.asStack())
                .EUt(GTValues.VA[GTValues.UV]).duration(800)
                .stationResearch(b -> b
                        .researchStack(com.gregtechceu.gtceu.common.data.machines.GTResearchMachines.RESEARCH_STATION
                                .asStack())
                        .CWUt(64))
                .save(provider);
        // G-0250: GTO Neural Matrix / Bioware Mainframe / Optical Processing Core / Exotic wafers / nanotube wires /
        // integrated control cores / Really Max battery / Wood's Glass / Abyssal Alloy -> Data Modules, Optical
        // Mainframes, Optical Computers, Advanced SoC wafers, Europium / Trinium fine wire, UEV field generators,
        // Ultimate batteries, Polybenzimidazole, Tritanium; research from the Data Bank (GTO: its Bio Data Hatch).
        GTRecipeTypes.ASSEMBLY_LINE_RECIPES.recipeBuilder(GTNACORE.id("mega/data_center"))
                .inputItems(com.gregtechceu.gtceu.common.data.machines.GTResearchMachines.DATA_BANK.asStack(16))
                .inputItems(GTItems.TOOL_DATA_MODULE.asStack(64))
                .inputItems(com.raishxn.gtna.common.data.GTNACircuits.OPTICAL_MAINFRAME.asStack(32))
                .inputItems(com.raishxn.gtna.common.data.GTNACircuits.OPTICAL_COMPUTER.asStack(16))
                .inputItems(GTItems.ADVANCED_SYSTEM_ON_CHIP_WAFER.asStack(64))
                .inputItems(GTBlocks.OPTICAL_PIPES[0].asStack(64))
                .inputItems(GTBlocks.OPTICAL_PIPES[0].asStack(64))
                .inputItems(TagPrefix.wireFine, GTMaterials.Europium, 64)
                .inputItems(TagPrefix.wireFine, GTMaterials.Trinium, 64)
                .inputItems(GTItems.FIELD_GENERATOR_UEV.asStack(8))
                .inputItems(GTItems.ULTIMATE_BATTERY.asStack(8))
                .inputFluids(com.raishxn.gtna.common.data.material.GodforgeChainMaterials.MutatedLivingSolder
                        .getFluid(144 << 6))
                .inputFluids(GTMaterials.Polybenzimidazole.getFluid(144 << 6))
                .inputFluids(GTMaterials.Tritanium.getFluid(144 << 6))
                .inputFluids(GTMaterials.Neutronium.getFluid(144 << 6))
                .outputItems(GTNAMegaMachines.DATA_CENTER.asStack())
                .EUt(GTValues.VA[GTValues.UEV]).duration(400)
                .stationResearch(b -> b
                        .researchStack(
                                com.gregtechceu.gtceu.common.data.machines.GTResearchMachines.DATA_BANK.asStack())
                        .CWUt(512).EUt(GTValues.VA[GTValues.UEV]))
                .save(provider);
    }

    /** GTO {@code FuelCell.init} and the membrane electrode assembler recipes. */
    private static void fuelCell(Consumer<FinishedRecipe> provider) {
        // GTO catalysts (Nickel / Platinum / TiO2 nanotubes / Rh-Re-Nq ...) -> dusts of the same element.
        var catalysts = new com.gregtechceu.gtceu.api.data.chemical.material.Material[] { GTMaterials.Nickel,
                GTMaterials.Platinum, GTMaterials.Titanium, GTMaterials.Rhodium, GTMaterials.Cerium,
                GTMaterials.Naquadah };
        var membranes = com.raishxn.gtna.common.data.material.FuelCellMaterials.MEMBRANES;
        for (int i = 0; i < membranes.length; i++) {
            var membrane = membranes[i].membrane();
            GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder(GTNACORE.id(membrane.getName() + "_membrane_electrode"))
                    .inputItems(TagPrefix.foil, membrane, 16)
                    .inputItems(TagPrefix.dust, catalysts[i], 4)
                    .inputItems(new net.minecraft.world.item.ItemStack(net.minecraft.world.item.Items.SPONGE))
                    .inputFluids(GTMaterials.Polycaprolactam.getFluid(144))
                    .outputItems(com.raishxn.gtna.api.data.tag.GTNATagPrefix.membraneElectrode, membrane)
                    .EUt(8168).duration(600).save(provider);
        }

        var storageA = com.raishxn.gtna.common.data.material.FuelCellMaterials.ENERGY_STORAGE_ANODE;
        var storageC = com.raishxn.gtna.common.data.material.FuelCellMaterials.ENERGY_STORAGE_CATHODE;
        var releaseA = com.raishxn.gtna.common.data.material.FuelCellMaterials.ENERGY_RELEASE_ANODE;
        var releaseC = com.raishxn.gtna.common.data.material.FuelCellMaterials.ENERGY_RELEASE_CATHODE;
        var electrolytes = new java.util.ArrayList<>(
                com.raishxn.gtna.common.data.material.FuelCellMaterials.EU_PER_MB.entrySet());
        for (int i = 0; i < electrolytes.size(); i++) {
            var material = electrolytes.get(i).getKey();
            long euPerMb = electrolytes.get(i).getValue();
            var membrane = com.gregtechceu.gtceu.api.data.chemical.ChemicalHelper
                    .get(com.raishxn.gtna.api.data.tag.GTNATagPrefix.membraneElectrode, membranes[i].membrane());
            com.raishxn.gtna.common.data.GTNARecipeType.FUEL_CELL_ENERGY_RELEASE_RECIPES
                    .recipeBuilder(GTNACORE.id(material.getName() + "_release"))
                    .notConsumable(membrane.copy())
                    .inputFluids(material.getFluid(storageA, 20))
                    .inputFluids(material.getFluid(storageC, 20))
                    .outputFluids(material.getFluid(releaseA, 19))
                    .outputFluids(material.getFluid(releaseC, 19))
                    .EUt(-euPerMb * 5).duration(20).save(provider);
            for (var other : electrolytes) {
                var material2 = other.getKey();
                if (material2 == material) continue;
                long partial1 = euPerMb >> 8;
                long partial2 = other.getValue() >> 8;
                com.raishxn.gtna.common.data.GTNARecipeType.FUEL_CELL_ENERGY_TRANSFER_RECIPES
                        .recipeBuilder(GTNACORE.id(material.getName() + "_to_" + material2.getName() + "_absorption"))
                        .notConsumable(membrane.copyWithCount(2))
                        .inputFluids(material.getFluid(storageA, (int) (20 * partial2)))
                        .inputFluids(material.getFluid(storageC, (int) (20 * partial2)))
                        .inputFluids(material2.getFluid(releaseA, (int) (19 * partial1)))
                        .inputFluids(material2.getFluid(releaseC, (int) (19 * partial1)))
                        .outputFluids(material2.getFluid(storageA, (int) (19 * partial1)))
                        .outputFluids(material2.getFluid(storageC, (int) (19 * partial1)))
                        .outputFluids(material.getFluid(releaseA, (int) (19 * partial2)))
                        .outputFluids(material.getFluid(releaseC, (int) (19 * partial2)))
                        .EUt(1).duration(20)
                        .addData("efficiency",
                                (float) partial1 / partial2 * other.getValue() / euPerMb * 0.95f)
                        .save(provider);
            }
        }

        // Absorption: GTO feeds its jetpack fuels; GTNA feeds the GTCEu combustion fuels with the energy GTCEu gives
        // them (duration x 32 EU/t per amount, GTCEu FuelRecipes). Equal liquid oxygen, as in GTO.
        Object[][] fuels = { { GTMaterials.Naphtha, 1, 10 }, { GTMaterials.SulfuricLightFuel, 4, 5 },
                { GTMaterials.Methanol, 4, 8 }, { GTMaterials.Ethanol, 1, 6 }, { GTMaterials.Octane, 2, 5 },
                { GTMaterials.BioDiesel, 1, 8 }, { GTMaterials.LightFuel, 1, 10 }, { GTMaterials.Diesel, 1, 15 },
                { GTMaterials.CetaneBoostedDiesel, 2, 45 }, { GTMaterials.RocketFuel, 16, 125 },
                { GTMaterials.Gasoline, 1, 50 }, { GTMaterials.HighOctaneGasoline, 1, 100 },
                { GTMaterials.Toluene, 1, 10 } };
        var membraneTag = net.minecraft.tags.TagKey.create(net.minecraft.core.registries.Registries.ITEM,
                new net.minecraft.resources.ResourceLocation("forge", "membrane_electrodes"));
        for (Object[] fuel : fuels) {
            var material = (com.gregtechceu.gtceu.api.data.chemical.material.Material) fuel[0];
            int amount = (int) fuel[1];
            long energy = (long) (int) fuel[2] * GTValues.V[GTValues.LV];
            com.raishxn.gtna.common.data.GTNARecipeType.FUEL_CELL_ENERGY_ABSORPTION_RECIPES
                    .recipeBuilder(GTNACORE.id(material.getName()))
                    .notConsumable(net.minecraft.world.item.crafting.Ingredient.of(membraneTag))
                    .inputFluids(
                            GTMaterials.Oxygen.getFluid(com.gregtechceu.gtceu.api.fluids.store.FluidStorageKeys.LIQUID,
                                    amount))
                    .inputFluids(material.getFluid(amount))
                    .EUt(1).duration(20)
                    .addData("converted_energy", energy)
                    .save(provider);
        }

        // GTO Chemical Energy Devourer -> GTCEu Large Combustion Engine.
        GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder(GTNACORE.id("mega/fuel_cell_generator"))
                .inputItems(GTNABlocks.IRIDIUM_CASING.asStack(4))
                .inputItems(GTMultiMachines.LARGE_COMBUSTION_ENGINE.asStack())
                .inputItems(com.raishxn.gtna.api.data.tag.GTNATagPrefix.membraneElectrode,
                        GTMaterials.Polytetrafluoroethylene, 16)
                .inputItems(GTItems.ENGRAVED_LAPOTRON_CHIP.asStack(8))
                .inputItems(GTBlocks.HERMETIC_CASING_EV.asStack(4))
                .inputItems(GTBlocks.HERMETIC_CASING_IV.asStack(4))
                .inputItems(CustomTags.LuV_CIRCUITS, 4)
                .inputItems(GTItems.ELECTRIC_PUMP_IV.asStack(8))
                .inputItems(TagPrefix.wireGtQuadruple, GTMaterials.SamariumIronArsenicOxide, 4)
                .inputFluids(GTMaterials.SolderingAlloy.getFluid(4000))
                .outputItems(GTNAMegaMachines.FUEL_CELL_GENERATOR.asStack())
                .EUt(7680).duration(1200).save(provider);
        // GTO Stainless Steel double plates -> plates (GTCEu has no Stainless Steel double plate).
        GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder(GTNACORE.id("mega/flocculation_casing"))
                .inputItems(TagPrefix.frameGt, GTMaterials.StainlessSteel)
                .inputItems(TagPrefix.pipeTinyFluid, GTMaterials.Tungsten, 4)
                .inputItems(TagPrefix.plate, GTMaterials.StainlessSteel, 12)
                .inputFluids(GTMaterials.Polytetrafluoroethylene.getFluid(288))
                .outputItems(GTNABlocks.FLOCCULATION_CASING.asStack())
                .EUt(120).duration(200).save(provider);
    }

    /**
     * GTO {@code NewResearchSystem} computer recipes (G-0249). GTO Abyssal Alloy -> Neutronium, Orichalcum ->
     * Tritanium, Neural Matrix -> Data Module, Wetware SoC -> Advanced SoC; GWCA (GTO recipe not found) mirrors NICH
     * one
     * tier up on the Graviton Computer Casing. MFPC inputs are kept: the pack provides MFPC.
     */
    private static void supercomputing(Consumer<FinishedRecipe> provider) {
        var rtan = GTMaterials.RutheniumTriniumAmericiumNeutronate;
        GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder(GTNACORE.id("mega/biocomputer_casing"))
                .inputItems(GTBlocks.ADVANCED_COMPUTER_CASING.asStack())
                .inputItems(CustomTags.UHV_CIRCUITS, 2)
                .inputItems(TagPrefix.wireFine, GTMaterials.Titanium, 64)
                .inputItems(TagPrefix.wireFine, GTMaterials.Neutronium, 64)
                .inputItems(TagPrefix.wireGtSingle, rtan, 16)
                .outputItems(GTNABlocks.BIOCOMPUTER_CASING.asStack())
                .EUt(GTValues.VA[GTValues.UV]).duration(400).save(provider);
        GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder(GTNACORE.id("mega/phase_change_biocomputer_cooling_vents"))
                .inputItems(GTNABlocks.BIOCOMPUTER_CASING.asStack())
                .inputItems(GTItems.ELECTRIC_MOTOR_UHV.asStack(2))
                .inputItems(TagPrefix.ingot, com.raishxn.gtna.common.data.material.ResearchMaterials.BasicMFPC, 64)
                .inputItems(TagPrefix.pipeTinyFluid, GTMaterials.Neutronium, 16)
                .inputItems(TagPrefix.plate, GTMaterials.Tritanium, 16)
                .inputItems(TagPrefix.wireGtSingle, rtan, 16)
                .outputItems(GTNABlocks.PHASE_CHANGE_BIOCOMPUTER_COOLING_VENTS.asStack())
                .EUt(GTValues.VA[GTValues.UV]).duration(400).save(provider);
        // GTO Nano-Strengthened Shape Memory Alloy frame / Trinium-Titanium / Enderite -> Tritanium / Trinium /
        // Europium.
        GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder(GTNACORE.id("mega/graviton_computer_casing"))
                .inputItems(GTBlocks.ADVANCED_COMPUTER_CASING.asStack())
                .inputItems(CustomTags.UIV_CIRCUITS, 2)
                .inputItems(GTNABlocks.RESTRAINT_DEVICE.asStack(4))
                .inputItems(TagPrefix.frameGt, GTMaterials.Tritanium)
                .inputItems(TagPrefix.plateDense, GTMaterials.NaquadahAlloy, 16)
                .inputItems(TagPrefix.wireFine, GTMaterials.Trinium, 64)
                .inputItems(TagPrefix.wireFine, GTMaterials.Europium, 64)
                .outputItems(GTNABlocks.GRAVITON_COMPUTER_CASING.asStack())
                .EUt(GTValues.VA[GTValues.UEV]).duration(300).save(provider);
        GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder(GTNACORE.id("mega/anti_entropy_computer_condensation_matrix"))
                .inputItems(GTNABlocks.GRAVITON_COMPUTER_CASING.asStack())
                .inputItems(GTItems.ELECTRIC_MOTOR_UEV.asStack(2))
                .inputItems(TagPrefix.block, com.raishxn.gtna.common.data.material.ResearchMaterials.CascadeMFPC, 16)
                .inputItems(TagPrefix.pipeTinyFluid, GTMaterials.Neutronium, 32)
                .inputItems(TagPrefix.plate, GTMaterials.Tritanium, 32)
                .inputItems(TagPrefix.wireGtSingle, rtan, 32)
                .outputItems(GTNABlocks.ANTI_ENTROPY_COMPUTER_CONDENSATION_MATRIX.asStack())
                .EUt(GTValues.VA[GTValues.UEV]).duration(400).save(provider);
        // GTO GlassRecipe: borosilicate glass + molten metal in the solidifier (Tungsten / Tritanium for Taranium).
        GTRecipeTypes.FLUID_SOLIDFICATION_RECIPES.recipeBuilder(GTNACORE.id("mega/tungsten_borosilicate_glass"))
                .inputItems(GTBlocks.CASING_TEMPERED_GLASS.asStack())
                .inputFluids(GTMaterials.Tungsten.getFluid(1152))
                .outputItems(GTNABlocks.TUNGSTEN_BOROSILICATE_GLASS.asStack())
                .EUt(GTValues.VA[GTValues.IV]).duration(200).save(provider);
        GTRecipeTypes.FLUID_SOLIDFICATION_RECIPES.recipeBuilder(GTNACORE.id("mega/taranium_borosilicate_glass"))
                .inputItems(GTNABlocks.AMPROSIUM_BOROSILICATE_GLASS.asStack())
                .inputFluids(GTMaterials.Tritanium.getFluid(1152))
                .outputItems(GTNABlocks.TARANIUM_BOROSILICATE_GLASS.asStack())
                .EUt(GTValues.VA[GTValues.UIV]).duration(200).save(provider);

        component(provider, "nich", 3, GTNABlocks.BIOCOMPUTER_CASING.asStack(), CustomTags.UV_CIRCUITS,
                CustomTags.UEV_CIRCUITS, GTItems.FIELD_GENERATOR_UHV.asStack(), GTItems.EMITTER_UHV.asStack(),
                com.raishxn.gtna.common.data.material.ResearchMaterials.BasicMFPC, GTValues.UHV);
        component(provider, "gwca", 4, GTNABlocks.GRAVITON_COMPUTER_CASING.asStack(), CustomTags.UEV_CIRCUITS,
                CustomTags.UIV_CIRCUITS, GTItems.FIELD_GENERATOR_UEV.asStack(), GTItems.EMITTER_UEV.asStack(),
                com.raishxn.gtna.common.data.material.ResearchMaterials.CascadeMFPC, GTValues.UEV);

        // GTO Sterling Silver restrictive pipes -> Tungstensteel huge fluid pipes.
        GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder(GTNACORE.id("mega/thermal_conductor_hatch"))
                .inputItems(GTMachines.HULL[GTValues.LuV].asStack())
                .inputItems(TagPrefix.ingot, com.raishxn.gtna.common.data.material.ResearchMaterials.BasicMFPC, 16)
                .inputItems(TagPrefix.pipeHugeFluid, GTMaterials.TungstenSteel, 8)
                .inputItems(GTItems.ROBOT_ARM_LuV.asStack(8))
                .inputFluids(GTMaterials.SodiumPotassium.getFluid(2880))
                .outputItems(com.raishxn.gtna.common.data.GTNAResearchMachines.THERMAL_CONDUCTOR_HATCH.asStack())
                .EUt(GTValues.VA[GTValues.LuV]).duration(200).save(provider);

        // GTO Wetware SoC / Indalloy -> Advanced SoC / Indium.
        GTRecipeTypes.ASSEMBLY_LINE_RECIPES.recipeBuilder(GTNACORE.id("mega/supercomputing_center"))
                .inputItems(com.gregtechceu.gtceu.common.data.machines.GTResearchMachines.NETWORK_SWITCH.asStack(16))
                .inputItems(GTItems.TOOL_DATA_MODULE.asStack(8))
                .inputItems(GTBlocks.OPTICAL_PIPES[0].asStack(64))
                .inputItems(GTBlocks.OPTICAL_PIPES[0].asStack(64))
                .inputItems(TagPrefix.wireGtOctal, GTMaterials.EnrichedNaquadahTriniumEuropiumDuranide, 32)
                .inputItems(GTItems.COVER_SCREEN.asStack(32))
                .inputItems(GTItems.ADVANCED_SYSTEM_ON_CHIP.asStack(32))
                .inputItems(TagPrefix.plate, GTMaterials.Neutronium, 32)
                .inputFluids(com.raishxn.gtna.common.data.material.GodforgeChainMaterials.MutatedLivingSolder
                        .getFluid(2304))
                .inputFluids(GTMaterials.Indium.getFluid(2304))
                .inputFluids(GTMaterials.Osmiridium.getFluid(2304))
                .inputFluids(GTMaterials.Ruridit.getFluid(2304))
                .outputItems(GTNAMegaMachines.SUPERCOMPUTING_CENTER.asStack())
                .EUt(2097152).duration(400)
                .stationResearch(b -> b.researchStack(
                        com.gregtechceu.gtceu.common.data.machines.GTResearchMachines.HPCA_ACTIVE_COOLER_COMPONENT
                                .asStack())
                        .CWUt(128))
                .save(provider);
    }

    /** GTO {@code make_nich_*}: empty, computing, cooling and bridge components of one family. */
    private static void component(Consumer<FinishedRecipe> provider, String family, int tier,
                                  net.minecraft.world.item.ItemStack casing,
                                  net.minecraft.tags.TagKey<net.minecraft.world.item.Item> emptyCircuit,
                                  net.minecraft.tags.TagKey<net.minecraft.world.item.Item> circuit,
                                  net.minecraft.world.item.ItemStack fieldGenerator,
                                  net.minecraft.world.item.ItemStack emitter,
                                  com.gregtechceu.gtceu.api.data.chemical.material.Material mfpc, int voltage) {
        var empty = tier == 3 ? com.raishxn.gtna.common.data.GTNAResearchMachines.NICH_EMPTY_COMPONENT :
                com.raishxn.gtna.common.data.GTNAResearchMachines.GWCA_EMPTY_COMPONENT;
        var computing = tier == 3 ? com.raishxn.gtna.common.data.GTNAResearchMachines.NICH_COMPUTING_COMPONENTS :
                com.raishxn.gtna.common.data.GTNAResearchMachines.GWCA_COMPUTING_COMPONENTS;
        var cooling = tier == 3 ? com.raishxn.gtna.common.data.GTNAResearchMachines.NICH_COOLING_COMPONENTS :
                com.raishxn.gtna.common.data.GTNAResearchMachines.GWCA_COOLING_COMPONENTS;
        var helium = GTMaterials.Helium.getFluid(com.gregtechceu.gtceu.api.fluids.store.FluidStorageKeys.LIQUID,
                8000);
        var cleanroom = com.gregtechceu.gtceu.api.machine.multiblock.CleanroomType.CLEANROOM;
        GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder(GTNACORE.id("mega/" + family + "_empty_component"))
                .inputItems(casing).inputItems(emptyCircuit, 2).inputItems(GTItems.TOOL_DATA_MODULE.asStack())
                .inputFluids(helium).outputItems(empty.asStack())
                .cleanroom(cleanroom).EUt(GTValues.VA[voltage]).duration(200).save(provider);
        GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder(GTNACORE.id("mega/" + family + "_computing_components"))
                .inputItems(empty.asStack()).inputItems(circuit, 8).inputItems(fieldGenerator)
                .inputFluids(helium).outputItems(computing.asStack())
                .cleanroom(cleanroom).EUt(GTValues.VA[voltage]).duration(200).save(provider);
        GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder(GTNACORE.id("mega/" + family + "_cooling_components"))
                .inputItems(empty.asStack()).inputItems(TagPrefix.block, mfpc, 64)
                .inputItems(TagPrefix.pipeTinyFluid, GTMaterials.Neutronium, 8)
                .inputItems(TagPrefix.plate, GTMaterials.Tritanium, 32)
                .outputItems(cooling.asStack())
                .cleanroom(cleanroom).EUt(GTValues.VA[voltage]).duration(200).save(provider);
        if (tier == 3) {
            GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder(GTNACORE.id("mega/nich_bridge_component"))
                    .inputItems(empty.asStack()).inputItems(circuit, 2).inputItems(emitter)
                    .inputItems(GTBlocks.OPTICAL_PIPES[0].asStack(32))
                    .inputFluids(helium)
                    .outputItems(com.raishxn.gtna.common.data.GTNAResearchMachines.NICH_BRIDGE_COMPONENT.asStack())
                    .cleanroom(cleanroom).EUt(GTValues.VA[voltage]).duration(200).save(provider);
        }
    }

    private static void tieredGlass(java.util.function.Consumer<net.minecraft.data.recipes.FinishedRecipe> provider,
                                    int tier, com.gregtechceu.gtceu.api.data.chemical.material.Material material,
                                    com.tterrag.registrate.util.entry.BlockEntry<?> glass) {
        GTRecipeTypes.FLUID_SOLIDFICATION_RECIPES
                .recipeBuilder(GTNACORE.id("mega/" + glass.getId().getPath()))
                .inputItems(GTNABlocks.BOROSILICATE_GLASS_BLOCK.asStack())
                .inputFluids(material.getFluid(1152))
                .outputItems(glass.asStack())
                .EUt(GTValues.VA[tier]).duration(200).save(provider);
    }
}
