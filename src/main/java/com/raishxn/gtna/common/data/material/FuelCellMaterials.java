package com.raishxn.gtna.common.data.material;

import com.gregtechceu.gtceu.api.GTValues;
import com.gregtechceu.gtceu.api.data.chemical.material.Material;
import com.gregtechceu.gtceu.api.data.chemical.material.info.MaterialIconSet;
import com.gregtechceu.gtceu.api.data.chemical.material.info.MaterialIconType;
import com.gregtechceu.gtceu.api.fluids.FluidState;
import com.gregtechceu.gtceu.api.fluids.store.FluidStorageKey;

import com.raishxn.gtna.GTNACORE;
import com.raishxn.gtna.api.data.info.GTNAMaterialFlags;

import java.util.LinkedHashMap;
import java.util.Map;

import static com.gregtechceu.gtceu.api.data.chemical.material.info.MaterialFlags.GENERATE_FOIL;
import static com.gregtechceu.gtceu.api.data.chemical.material.info.MaterialFlags.GENERATE_PLATE;
import static com.gregtechceu.gtceu.common.data.GTMaterials.Graphene;
import static com.gregtechceu.gtceu.common.data.GTMaterials.Polytetrafluoroethylene;

/**
 * GTOCore Fuel Cell Generator content (G-0248), copied from GTOCore {@code dc4824d}: the four electrolyte fluid states
 * ({@code GTOFluidStorageKey}), the six redox-flow electrolytes and the membrane materials with their energy per mB
 * and membrane bonuses ({@code FullCellGenerator.Wrapper}, normal-difficulty values).
 */
public final class FuelCellMaterials {

    private FuelCellMaterials() {}

    public static final FluidStorageKey ENERGY_STORAGE_ANODE = key("energy_storage_anode");
    public static final FluidStorageKey ENERGY_STORAGE_CATHODE = key("energy_storage_cathode");
    public static final FluidStorageKey ENERGY_RELEASE_ANODE = key("energy_release_anode");
    public static final FluidStorageKey ENERGY_RELEASE_CATHODE = key("energy_release_cathode");

    public static Material IronChromiumElectrolyte;
    public static Material VanadiumElectrolyte;
    public static Material ZincIodideElectrolyte;
    public static Material OrganicMoleculeElectrolyte;
    public static Material SuperconductingIonElectrolyte;
    public static Material AntimatterElectrolyte;

    public static Material PolousPolyolefinSulfonate;
    public static Material PerfluorosulfonicAcidPolytetrafluoroethyleneCopolymer;
    public static Material CeOxPolyDopamineReinforcedPolytetrafluoroethylene;
    public static Material NanocrackRegulatedSelfHumidifyingCompositeMaterial;

    /** GTO {@code ELECTROLYTES_PER_MATERIAL_PER_MILLIBUCKET}, in electrolyte tier order. */
    public static final Map<Material, Long> EU_PER_MB = new LinkedHashMap<>();
    /** GTO {@code MEMBRANE_MATS}, one per electrolyte tier. */
    public static Membrane[] MEMBRANES = new Membrane[0];

    /**
     * GTO {@code MembraneBonusInfo} (normal difficulty): absorption efficiency and the decay factor applied after each
     * absorption run.
     */
    public record Membrane(int tier, Material membrane, Material electrolyte, double efficiencyBonus,
                           double decayFactor) {}

    private static FluidStorageKey key(String id) {
        return new FluidStorageKey(GTNACORE.id(id), MaterialIconType.liquid, m -> m.getName() + "_" + id,
                m -> "gtna.fluid." + id, FluidState.LIQUID, 0);
    }

    private static Material electrolyte(String id, int color) {
        return new Material.Builder(GTNACORE.id(id))
                .fluid(ENERGY_STORAGE_ANODE, FluidState.LIQUID)
                .fluid(ENERGY_STORAGE_CATHODE, FluidState.LIQUID)
                .fluid(ENERGY_RELEASE_ANODE, FluidState.LIQUID)
                .fluid(ENERGY_RELEASE_CATHODE, FluidState.LIQUID)
                .color(color).iconSet(MaterialIconSet.FLUID)
                .buildAndRegister();
    }

    private static Material membrane(String id, int color, String formula) {
        Material material = new Material.Builder(GTNACORE.id(id))
                .polymer()
                .flags(GENERATE_FOIL, GENERATE_PLATE, GTNAMaterialFlags.GENERATE_MEMBRANE_ELECTRODE)
                .color(color).iconSet(MaterialIconSet.DULL)
                .buildAndRegister();
        material.setFormula(formula);
        return material;
    }

    public static void init() {
        IronChromiumElectrolyte = electrolyte("iron_chromium", 0xB7410E);
        VanadiumElectrolyte = electrolyte("all_vanadium", 0xFF4D00);
        ZincIodideElectrolyte = electrolyte("zinc_iodide", 0xFFFF00);
        OrganicMoleculeElectrolyte = electrolyte("organic_molecule", 0x00FF00);
        SuperconductingIonElectrolyte = electrolyte("superconducting_ion", 0x0000FF);
        AntimatterElectrolyte = electrolyte("antimatter_ion", 0x8B00FF);

        PolousPolyolefinSulfonate = membrane("polous_polyolefin_sulfonate", 0xffff00, "C3H6SO3Na");
        PerfluorosulfonicAcidPolytetrafluoroethyleneCopolymer = membrane(
                "perfluorosulfonic_acid_polytetrafluoroethylene_copolymer", 0xfd0ddf, "(C2F4)n(CF2SO3H)m");
        CeOxPolyDopamineReinforcedPolytetrafluoroethylene = membrane(
                "ce_ox_poly_dopamine_reinforced_polytetrafluoroethylene", 0x0d7f7f, "(C2F4)n(C8H11NO2)mCeOx");
        NanocrackRegulatedSelfHumidifyingCompositeMaterial = membrane(
                "nanocrack_regulated_self_humidifying_composite_material", 0x0d7f0d, "(C2F4)n(C8H11NO2)mCeOx?");
        Polytetrafluoroethylene.addFlags(GTNAMaterialFlags.GENERATE_MEMBRANE_ELECTRODE);
        Graphene.addFlags(GTNAMaterialFlags.GENERATE_MEMBRANE_ELECTRODE);

        EU_PER_MB.put(IronChromiumElectrolyte, GTValues.V[GTValues.UEV] * 2 / 1000);
        EU_PER_MB.put(VanadiumElectrolyte, GTValues.V[GTValues.UXV] / 1000);
        EU_PER_MB.put(ZincIodideElectrolyte, GTValues.V[GTValues.OpV] * 2 / 1000);
        EU_PER_MB.put(OrganicMoleculeElectrolyte, GTValues.V[GTValues.MAX] * 4 / 1000);
        EU_PER_MB.put(SuperconductingIonElectrolyte, GTValues.V[GTValues.MAX] * 32 / 1000);
        EU_PER_MB.put(AntimatterElectrolyte, GTValues.V[GTValues.MAX] * 256 / 1000);

        MEMBRANES = new Membrane[] {
                new Membrane(0, Polytetrafluoroethylene, IronChromiumElectrolyte, 1.05d, 0.992d),
                new Membrane(1, Graphene, VanadiumElectrolyte, 1.3d, 0.994d),
                new Membrane(2, PolousPolyolefinSulfonate, ZincIodideElectrolyte, 1.69d, 0.996d),
                new Membrane(3, PerfluorosulfonicAcidPolytetrafluoroethyleneCopolymer, OrganicMoleculeElectrolyte,
                        1.96d, 0.999d),
                new Membrane(4, CeOxPolyDopamineReinforcedPolytetrafluoroethylene, SuperconductingIonElectrolyte,
                        2.25d, 0.9994d),
                new Membrane(5, NanocrackRegulatedSelfHumidifyingCompositeMaterial, AntimatterElectrolyte, 2.5d,
                        1.0d) };
    }
}
