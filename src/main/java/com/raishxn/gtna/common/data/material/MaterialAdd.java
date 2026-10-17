package com.raishxn.gtna.common.data.material;

import com.gregtechceu.gtceu.api.data.chemical.material.properties.*;

import com.raishxn.gtna.api.data.info.GTNAMaterialFlags;

import static com.gregtechceu.gtceu.api.data.chemical.material.info.MaterialFlags.*;
import static com.gregtechceu.gtceu.common.data.GTMaterials.*;

public class MaterialAdd {

    public static void init() {
        // Stock GTCEu declares these elements without item forms. The GTL vein catalog needs
        // dust fallbacks for its fork-only ores; do not generate extra worldgen ore blocks.
        // Ytterbium, Thallium, Erbium, Hafnium, Rhenium and Gadolinium are by-products of the ported ore and stellar
        // recipes (front_pro, stellar_superheavy_synthesis, rare_earth); without a dust form those recipes failed.
        for (var material : new com.gregtechceu.gtceu.api.data.chemical.material.Material[] {
                Rubidium, Strontium, Tellurium, Zirconium, Ytterbium, Thallium, Erbium, Hafnium, Rhenium,
                Gadolinium }) {
            if (!material.hasProperty(PropertyKey.DUST)) material.setProperty(PropertyKey.DUST, new DustProperty());
        }
        // EN: Forms the BEC / Eye of Harmony / Godforge recipes ask for; without them EMI showed empty slots.
        // PT: Formas pedidas pelas receitas de BEC / Eye of Harmony / Godforge; sem elas o EMI mostrava slots vazios.
        // ZH: BEC / 和谐之眼 / 神之锻炉配方所需的形态；缺失时 EMI 显示空槽位。
        if (!Praseodymium.hasProperty(PropertyKey.DUST)) Praseodymium.setProperty(PropertyKey.DUST, new DustProperty());
        for (var material : new com.gregtechceu.gtceu.api.data.chemical.material.Material[] {
                Rhenium, Seaborgium, Germanium }) {
            if (!material.hasProperty(PropertyKey.DUST)) material.setProperty(PropertyKey.DUST, new DustProperty());
            if (!material.hasProperty(PropertyKey.INGOT))
                material.setProperty(PropertyKey.INGOT, new IngotProperty());
            material.addFlags(GENERATE_PLATE);
        }
        Seaborgium.addFlags(GENERATE_DENSE);
        Germanium.addFlags(GENERATE_DENSE);
        Neutronium.addFlags(GENERATE_DENSE, GENERATE_RING, GENERATE_SMALL_GEAR, GENERATE_SPRING, GENERATE_FINE_WIRE,
                GTNAMaterialFlags.GENERATE_SUPERDENSE);
        Tritanium.addFlags(GENERATE_DENSE);
        Osmiridium.addFlags(GENERATE_DENSE);
        Flerovium.addFlags(GENERATE_DENSE);
        Duranium.addFlags(GENERATE_DENSE);
        NaquadahEnriched.addFlags(GENERATE_FRAME);
        VanadiumSteel.addFlags(GENERATE_FRAME);
        Trinium.addFlags(GENERATE_FINE_WIRE);
        Titanium.addFlags(GENERATE_FINE_WIRE);
        RutheniumTriniumAmericiumNeutronate.addFlags(GENERATE_FINE_WIRE);
        Graphene.addFlags(GENERATE_FINE_WIRE);
        HastelloyC276.addFlags(GENERATE_ROTOR);
        TitaniumTungstenCarbide.addFlags(GENERATE_GEAR);
        if (GodforgeChainMaterials.AdvancedNitinol != null)
            GodforgeChainMaterials.AdvancedNitinol.addFlags(GTNAMaterialFlags.GENERATE_SUPERDENSE);
        Bronze.addFlags(GENERATE_SPRING_SMALL, GENERATE_SPRING);
        Beryllium.addFlags(GENERATE_ROD, GENERATE_FRAME);
        // GTOCore's Cold Ice Freezer auxiliary tower is framed in Naquadah; GTCEu 7.5.3 does not
        // generate that frame, so the flag is restored here (same as Beryllium above).
        Naquadah.addFlags(GENERATE_FRAME);
        // GTOCore's Component Assembler extension is framed in Trinium; GTOCore adds the frame flag
        // to the GTCEu material and GTCEu 7.5.3 does not generate it.
        Trinium.addFlags(GENERATE_FRAME);
        // Same situation for the component_assembly_line's Naquadria frame ring.
        Naquadria.addFlags(GENERATE_FRAME);
        // Multi-plate items used by the ported GTNL recipes (triple/quadruple/quintuple plates).
        Steel.addFlags(GTNAMaterialFlags.GENERATE_TRIPLE_PLATE, GTNAMaterialFlags.GENERATE_QUADRUPLE_PLATE,
                GTNAMaterialFlags.GENERATE_QUINTUPLE_PLATE);
        // GTOCore ISA Mill MILLED products: the exact material list from classified/IsaMill.java.
        Grossular.addFlags(GTNAMaterialFlags.GENERATE_MILLED);
        Almandine.addFlags(GTNAMaterialFlags.GENERATE_MILLED);
        Chalcopyrite.addFlags(GTNAMaterialFlags.GENERATE_MILLED);
        NaquadahEnriched.addFlags(GTNAMaterialFlags.GENERATE_MILLED);
        Platinum.addFlags(GTNAMaterialFlags.GENERATE_MILLED);
        Redstone.addFlags(GTNAMaterialFlags.GENERATE_MILLED);
        Monazite.addFlags(GTNAMaterialFlags.GENERATE_MILLED);
        Pentlandite.addFlags(GTNAMaterialFlags.GENERATE_MILLED);
        Nickel.addFlags(GTNAMaterialFlags.GENERATE_MILLED);
        Spessartine.addFlags(GTNAMaterialFlags.GENERATE_MILLED);
        Pyrope.addFlags(GTNAMaterialFlags.GENERATE_MILLED);
        Sphalerite.addFlags(GTNAMaterialFlags.GENERATE_MILLED);
    }
}
