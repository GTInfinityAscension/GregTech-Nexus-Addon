package com.raishxn.gtna.data.recipe;

import com.gregtechceu.gtceu.api.GTValues;
import com.gregtechceu.gtceu.api.data.chemical.ChemicalHelper;
import com.gregtechceu.gtceu.api.data.chemical.material.Material;
import com.gregtechceu.gtceu.api.data.chemical.material.properties.PropertyKey;
import com.gregtechceu.gtceu.api.data.tag.TagPrefix;
import com.gregtechceu.gtceu.common.data.GTItems;
import com.gregtechceu.gtceu.common.data.GTRecipeTypes;
import com.gregtechceu.gtceu.common.data.machines.GTMultiMachines;
import com.gregtechceu.gtceu.data.recipe.CustomTags;

import net.minecraft.data.recipes.FinishedRecipe;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraftforge.fluids.FluidStack;
import net.minecraftforge.registries.ForgeRegistries;

import com.raishxn.gtna.GTNACORE;
import com.raishxn.gtna.common.data.GTNABlocks;
import com.raishxn.gtna.common.data.GTNAItems;
import com.raishxn.gtna.common.data.GTNAMachines3;
import com.raishxn.gtna.common.data.GTNAMegaMachines;
import com.raishxn.gtna.common.data.GTNARecipeDataKeys;
import com.raishxn.gtna.common.data.GTNARecipeType;
import com.raishxn.gtna.common.data.material.GodforgeChainMaterials;

import java.util.ArrayList;
import java.util.List;
import java.util.function.Consumer;

import static com.gregtechceu.gtceu.common.data.GTMaterials.*;

/**
 * GTOCore Space Elevator recipes ({@code AssemblerModule}, {@code MinerModule}, {@code DrillingModule} and the
 * controllers). GTO-only inputs are replaced by GTCEu/GTNA ones, noted next to each recipe; GTO's rocket fuels by
 * GTCEu Rocket Fuel and Ad Astra Fuel.
 */
public final class GTNASpaceElevatorRecipes {

    private static final int[] BASE_TIME = { 600, 400 };

    private GTNASpaceElevatorRecipes() {}

    public static void register(Consumer<FinishedRecipe> provider) {
        GTNARecipeType.LOOM_RECIPES.recipeBuilder(GTNACORE.id("nanotube_spool"))
                .inputItems(TagPrefix.wireFine, Graphene, 16) // GTO: carbon nanotube fine wire
                .outputItems(GTNAItems.NANOTUBE_SPOOL.asStack())
                .EUt(7680).duration(200).save(provider);
        drones(provider);
        minerModule(provider);
        drillingModule(provider);
        controllers(provider);
    }

    /** One MK of Space Drone: tool head, battery, circuits, the tier's parts, wire, plate and three fluids. */
    private record Drone(Material head, ItemStack battery, net.minecraft.tags.TagKey<Item> circuits, int tier,
                         Material wire, Material plate, Material f1, Material f2, Material f3, int eut,
                         int powerModuleTier) {}

    private static void drones(Consumer<FinishedRecipe> provider) {
        // GTO wires/plates: Abyssal Alloy, Titan Steel, Adamantine, Naquadriatic Taranium, Starmetal -> GTCEu
        // superconductor-tier metals; Quantanium, Adamantium, Vibranium -> Neutronium / Duranium / Tritanium;
        // Bohrium, Meitnerium, Livermorium (fluids only in GTO) -> Iridium, Osmium, Naquadria.
        // EN: Wires need a material with a cable in GTCEu/GTNA (Duranium, Americium and Darmstadtium have none, so the
        // recipes failed to load): MK II uses Europium (UHV cable), MK V and MK VI the UXV superconductor of the
        // Godforge chain, the highest cable that exists.
        // PT: O fio precisa de um material com cabo no GTCEu/GTNA (Duranium, Americium e Darmstadtium não têm, e as
        // receitas falhavam ao carregar): o MK II usa Europium (cabo UHV), o MK V e o MK VI o supercondutor UXV da
        // cadeia do Godforge, o cabo mais alto que existe.
        // ZH: 导线需要在 GTCEu/GTNA 中拥有线缆的材料（Duranium、Americium、Darmstadtium 没有，导致配方加载失败）：
        // MK II 使用 Europium（UHV 线缆），MK V 和 MK VI 使用 Godforge 链的 UXV 超导体，即现有最高等级线缆。
        List<Drone> drones = List.of(
                new Drone(Titanium, GTItems.BATTERY_HV_LITHIUM.asStack(4), CustomTags.UV_CIRCUITS, GTValues.UV,
                        Tritanium, Darmstadtium, Manganese, Potin, Ultimet, 491520, 1),
                new Drone(TungstenSteel, GTItems.BATTERY_EV_VANADIUM.asStack(16), CustomTags.UHV_CIRCUITS,
                        GTValues.UHV, Europium, Tritanium, Neodymium, Osmiridium, HSSS, 1966080, 1),
                new Drone(HSSE, GTItems.BATTERY_IV_VANADIUM.asStack(4), CustomTags.UEV_CIRCUITS, GTValues.UEV,
                        Trinium, Neutronium, Yttrium, BlueAlloy, RTMAlloy, 7864320, 2),
                new Drone(NaquadahAlloy, GTItems.BATTERY_IV_VANADIUM.asStack(16), CustomTags.UIV_CIRCUITS,
                        GTValues.UIV, Europium, Duranium, Iridium, TungstenCarbide, RhodiumPlatedPalladium, 31457280,
                        3),
                new Drone(Duranium, GTItems.BATTERY_LuV_VANADIUM.asStack(4), CustomTags.UXV_CIRCUITS, GTValues.UXV,
                        GodforgeChainMaterials.SuperconductorUMV, Neutronium, Osmium, BlackBronze, HSSG, 125829120, 4),
                new Drone(Neutronium, GTItems.BATTERY_LuV_VANADIUM.asStack(16), CustomTags.OpV_CIRCUITS,
                        GTValues.OpV, GodforgeChainMaterials.SuperconductorUMV, Neutronium, Naquadria, SterlingSilver,
                        TitaniumTungstenCarbide,
                        503316480, 5));
        for (int i = 0; i < drones.size(); i++) {
            Drone d = drones.get(i);
            GTNARecipeType.ASSEMBLER_MODULE_RECIPES.recipeBuilder(GTNACORE.id("space_drone_mk" + (i + 1)))
                    .inputItems(TagPrefix.toolHeadDrill, d.head())
                    .inputItems(d.battery())
                    .inputItems(d.circuits(), 4)
                    .inputItems(appeng.core.definitions.AEItems.WIRELESS_RECEIVER.asItem())
                    .inputItems(part("electric_pump", d.tier()))
                    .inputItems(part("electric_piston", d.tier()))
                    .inputItems(part("electric_motor", d.tier()), 2)
                    .inputItems(part("conveyor_module", d.tier()), 2)
                    .inputItems(part("robot_arm", d.tier()), 2)
                    .inputItems(part("sensor", d.tier()))
                    .inputItems(part("emitter", d.tier()))
                    .inputItems(TagPrefix.wireGtQuadruple, d.wire(), 4)
                    .inputItems(GTItems.POWER_THRUSTER.asStack(4))
                    .inputItems(GTItems.STEEL_MINECART_WHEELS.asStack(2))
                    .inputItems(TagPrefix.spring, Steel, 4)
                    .inputItems(TagPrefix.plate, d.plate(), 8)
                    .inputFluids(SolderingAlloy.getFluid(2880))
                    .inputFluids(d.f1().getFluid(2880))
                    .inputFluids(d.f2().getFluid(2880))
                    .inputFluids(d.f3().getFluid(i == 3 ? 1000 : 2880))
                    .outputItems(GTNAItems.SPACE_DRONES.get(i).asStack())
                    .EUt(d.eut()).duration(600)
                    .addData(GTNARecipeDataKeys.POWER_MODULE_TIER, d.powerModuleTier())
                    .save(provider);
        }
    }

    /** GTCEu tiered component, e.g. {@code gtceu:uev_electric_pump}. */
    private static ItemStack part(String kind, int tier) {
        Item item = ForgeRegistries.ITEMS.getValue(new ResourceLocation("gtceu",
                GTValues.VN[tier].toLowerCase(java.util.Locale.ROOT) + "_" + kind));
        return new ItemStack(item);
    }

    private static FluidStack[] fuels() {
        // EN: Look Ad Astra's fuel up by ID so worlds still load without Ad Astra (dev runClient crashed).
        // PT: Busca o combustível do Ad Astra pelo ID para o mundo abrir sem o Ad Astra (o runClient travava).
        // ZH: 按 ID 查找 Ad Astra 燃料，使未安装 Ad Astra 时世界也能加载（开发客户端曾崩溃）。
        var adAstraFuel = ForgeRegistries.FLUIDS.getValue(new ResourceLocation("ad_astra", "fuel"));
        if (adAstraFuel == null || adAstraFuel == net.minecraft.world.level.material.Fluids.EMPTY)
            return new FluidStack[] { RocketFuel.getFluid(10000) };
        return new FluidStack[] { RocketFuel.getFluid(10000), new FluidStack(adAstraFuel, 6000) };
    }

    // EN: Without Ad Astra (dev runClient) the research falls back to the module connector instead of crashing.
    // PT: Sem o Ad Astra (runClient de dev) a pesquisa usa o conector de módulo em vez de travar.
    // ZH: 未安装 Ad Astra（开发客户端）时，研究物品改用模块连接器，避免崩溃。
    private static ItemStack researchItem() {
        Item rocket = ForgeRegistries.ITEMS.getValue(new ResourceLocation("ad_astra", "tier_4_rocket"));
        return rocket == null || rocket == net.minecraft.world.item.Items.AIR ? GTNABlocks.MODULE_CONNECTOR.asStack() :
                new ItemStack(rocket);
    }

    private record Ore(int amount, Material material) {}

    private static Ore ore(int amount, Material material) {
        return new Ore(amount, material);
    }

    private static void minerModule(Consumer<FinishedRecipe> provider) {
        // GTO groups 1-20; ores the pack doesn't have (GTO-only or no ore form) are left out of a group.
        Ore[][] groups = {
                { ore(280, Tetrahedrite), ore(140, Copper), ore(60, Bentonite), ore(40, Magnetite), ore(40, Olivine),
                        ore(20, GlauconiteSand) },
                { ore(180, Almandine), ore(120, Pyrope), ore(60, Sapphire), ore(60, GreenSapphire), ore(70, Stibnite),
                        ore(120, Uraninite) },
                { ore(90, Bastnasite), ore(30, Molybdenum), ore(60, Goethite), ore(240, YellowLimonite),
                        ore(240, Hematite), ore(120, Malachite) },
                { ore(120, Soapstone), ore(80, Talc), ore(80, GlauconiteSand), ore(40, Pentlandite),
                        ore(30, Neodymium), ore(60, Monazite) },
                { ore(180, Redstone), ore(120, Ruby), ore(60, Grossular), ore(40, Spessartine), ore(20, Tantalite) },
                { ore(250, Chalcopyrite), ore(10, Zeolite), ore(10, Cassiterite), ore(50, Realgar), ore(60, Cinnabar) },
                { ore(120, Saltpeter), ore(80, Diatomite), ore(80, Electrotine), ore(40, Alunite), ore(240, Coal) },
                { ore(90, Beryllium), ore(120, Emerald), ore(40, Chalcopyrite), ore(160, Iron), ore(160, Pyrite),
                        ore(160, Copper) },
                { ore(60, Grossular), ore(40, Pyrolusite), ore(20, Tantalite), ore(240, Magnetite),
                        ore(160, VanadiumMagnetite), ore(80, Gold) },
                { ore(120, Lazurite), ore(80, Sodalite), ore(80, Lapis), ore(40, Calcite), ore(150, Wulfenite) },
                { ore(120, Galena), ore(80, Silver), ore(40, Lead), ore(100, Molybdenite), ore(50, Molybdenum),
                        ore(50, Powellite) },
                { ore(60, YellowLimonite), ore(60, Kyanite), ore(40, Mica), ore(40, Bauxite),
                        ore(20, Pollucite) },
                { ore(80, CertusQuartz), ore(90, Goethite), ore(160, Cassiterite), ore(60, Hematite), ore(30, Gold) },
                { ore(40, Barite), ore(120, GarnetRed), ore(80, GarnetYellow), ore(80, Amethyst), ore(40, Opal) },
                { ore(210, BlueTopaz), ore(140, Topaz), ore(240, BasalticMineralSand), ore(160, GraniticMineralSand),
                        ore(160, FullersEarth), ore(80, Gypsum) },
                { ore(150, RockSalt), ore(10, Salt), ore(50, Lepidolite), ore(50, Spodumene), ore(140, Chalcocite),
                        ore(70, Bornite) },
                { ore(180, Redstone), ore(120, Ruby), ore(60, Cinnabar), ore(240, NetherQuartz), ore(80, Quartzite) },
                { ore(120, Apatite), ore(80, TricalciumPhosphate), ore(40, Pyrochlore), ore(300, Sulfur),
                        ore(200, Pyrite), ore(100, Sphalerite) },
                { ore(180, Magnetite), ore(120, VanadiumMagnetite), ore(240, CassiteriteSand), ore(160, GarnetSand),
                        ore(160, Asbestos), ore(80, Diatomite) },
                { ore(240, Oilsands), ore(60, Gold), ore(160, Bauxite), ore(80, Ilmenite), ore(80, Aluminium) } };
        FluidStack[] fuels = fuels();
        for (int group = 0; group < groups.length; group++) {
            List<ItemStack> outputs = new ArrayList<>();
            for (Ore o : groups[group]) {
                if (!o.material().hasProperty(PropertyKey.ORE)) continue;
                ItemStack stack = ChemicalHelper.get(TagPrefix.ore, o.material(), o.amount());
                if (!stack.isEmpty()) outputs.add(stack);
            }
            if (outputs.isEmpty()) continue;
            for (int drone = 0; drone < 6; drone++) {
                for (int fuel = 0; fuel < fuels.length; fuel++) {
                    var builder = GTNARecipeType.MINER_MODULE_RECIPES
                            .recipeBuilder(GTNACORE.id("space_ore_" + (group + 1) + "_" + drone + "_" + fuel))
                            .notConsumable(GTNAItems.SPACE_DRONES.get(drone).asStack(16))
                            .circuitMeta(group + 1)
                            .inputFluids(fuels[fuel])
                            .EUt(GTValues.VA[GTValues.UV + drone])
                            .duration(BASE_TIME[fuel] >> drone);
                    for (ItemStack out : outputs) builder.outputItems(out.copy());
                    builder.save(provider);
                }
            }
        }
    }

    private static void drillingModule(Consumer<FinishedRecipe> provider) {
        Material[] gases = { Hydrogen, Helium, Nitrogen, Methane, SulfurDioxide, CarbonDioxide, NitrogenDioxide,
                Ammonia, Chlorine, Fluorine, CarbonMonoxide };
        FluidStack[] fuels = fuels();
        for (int gas = 0; gas < gases.length; gas++) {
            for (int drone = 0; drone < 6; drone++) {
                for (int fuel = 0; fuel < fuels.length; fuel++) {
                    GTNARecipeType.DRILLING_MODULE_RECIPES
                            .recipeBuilder(GTNACORE.id("space_fluid_" + (gas + 1) + "_" + drone + "_" + fuel))
                            .notConsumable(GTNAItems.SPACE_DRONES.get(drone).asStack(16))
                            .circuitMeta(gas + 1)
                            .inputFluids(fuels[fuel])
                            .outputFluids(gases[gas].getFluid(1000000))
                            .EUt(GTValues.VA[GTValues.UV + drone])
                            .duration(BASE_TIME[fuel] >> drone)
                            .save(provider);
                }
            }
        }
    }

    private static void controllers(Consumer<FinishedRecipe> provider) {
        // GTO space_elevator AL recipe. Carbon nanites -> Graphene foil; Mendelevium / Nobelium / Lawrencium (GTO
        // fluids) -> Americium / Plutonium-239 / Naquadria; Pikyonium / Orichalcum double plates ->
        // Neutronium / Trinium; research on Ad Astra's tier 4 rocket.
        GTRecipeTypes.ASSEMBLY_LINE_RECIPES.recipeBuilder(GTNACORE.id("mega/space_elevator"))
                .inputItems(GTItems.GRAVITATION_ENGINE.asStack(16))
                .inputItems(GTItems.FIELD_GENERATOR_UV.asStack(8))
                .inputItems(CustomTags.UHV_CIRCUITS, 8)
                .inputItems(CustomTags.UV_CIRCUITS, 16)
                .inputItems(CustomTags.ZPM_CIRCUITS, 32)
                .inputItems(CustomTags.LuV_CIRCUITS, 64)
                .inputItems(GTNABlocks.MODULE_CONNECTOR.asStack(4))
                .inputItems(TagPrefix.wireGtHex, IndiumTinBariumTitaniumCuprate, 32)
                .inputItems(TagPrefix.wireGtHex, UraniumRhodiumDinaquadide, 16)
                .inputItems(TagPrefix.wireGtHex, EnrichedNaquadahTriniumEuropiumDuranide, 8)
                .inputItems(TagPrefix.pipeHugeRestrictive, Americium, 48)
                .inputItems(TagPrefix.pipeHugeFluid, Duranium, 48)
                .inputItems(TagPrefix.foil, Graphene, 64)
                .inputItems(TagPrefix.plateDouble, Neutronium, 32)
                .inputItems(TagPrefix.plateDouble, Trinium, 16)
                .inputFluids(SolderingAlloy.getFluid(4096))
                .inputFluids(Americium.getFluid(4096))
                .inputFluids(Plutonium239.getFluid(4096))
                .inputFluids(Naquadria.getFluid(4096))
                .outputItems(GTNAMegaMachines.SPACE_ELEVATOR.asStack())
                .EUt(491520).duration(1600)
                .stationResearch(r -> r.researchStack(researchItem()).CWUt(64).EUt(491520))
                .save(provider);
        // GTO assembler_module: Pikyonium -> Neutronium; Artherium-Tin -> Naquadah Alloy; research on the AL.
        GTRecipeTypes.ASSEMBLY_LINE_RECIPES.recipeBuilder(GTNACORE.id("mega/assembler_module"))
                .inputItems(GTNABlocks.ADVANCED_ASSEMBLY_LINE_UNIT.asStack(4))
                .inputItems(GTItems.EMITTER_UV.asStack(4))
                .inputItems(GTItems.SENSOR_UV.asStack(4))
                .inputItems(GTItems.ROBOT_ARM_UV.asStack(4))
                .inputItems(GTItems.CONVEYOR_MODULE_UV.asStack(4))
                .inputItems(CustomTags.UHV_CIRCUITS, 4)
                .inputItems(TagPrefix.wireGtHex, EnrichedNaquadahTriniumEuropiumDuranide, 4)
                .inputItems(TagPrefix.plateDouble, Neutronium, 8)
                .inputFluids(SolderingAlloy.getFluid(2880))
                .inputFluids(NaquadahAlloy.getFluid(2880))
                .outputItems(GTNAMegaMachines.ASSEMBLER_MODULE.asStack())
                .EUt(491520).duration(1200)
                .stationResearch(r -> r.researchStack(GTMultiMachines.ASSEMBLY_LINE.asStack()).CWUt(256)
                        .EUt(491520))
                .save(provider);
        // GTO resource_collection_module: Large Void Miner -> LuV Large Miner; Stellite gear kept (GTNA material).
        GTRecipeTypes.ASSEMBLY_LINE_RECIPES.recipeBuilder(GTNACORE.id("mega/resource_collection_module"))
                .inputItems(GTMultiMachines.LARGE_MINER[GTValues.LuV].asStack())
                .inputItems(GTNAMachines3.VOID_FLUID_DRILLING_RIG.asStack())
                .inputItems(GTItems.ROBOT_ARM_UV.asStack(4))
                .inputItems(TagPrefix.gear, com.raishxn.gtna.common.data.GTNAMaterials.Stellite, 16)
                .inputItems(GTItems.CONVEYOR_MODULE_UV.asStack(4))
                .inputItems(CustomTags.UHV_CIRCUITS, 4)
                .inputItems(TagPrefix.wireGtHex, EnrichedNaquadahTriniumEuropiumDuranide, 4)
                .inputItems(TagPrefix.plateDouble, Neutronium, 8)
                .inputFluids(SolderingAlloy.getFluid(2880))
                .inputFluids(NaquadahAlloy.getFluid(2880))
                .outputItems(GTNAMegaMachines.RESOURCE_COLLECTION_MODULE.asStack())
                .EUt(491520).duration(1200)
                .stationResearch(r -> r.researchStack(GTMultiMachines.LARGE_MINER[GTValues.LuV].asStack())
                        .CWUt(256).EUt(491520))
                .save(provider);
    }
}
