package com.raishxn.gtna.api.bec;

import com.gregtechceu.gtceu.api.data.chemical.material.Material;
import com.gregtechceu.gtceu.common.data.GTMaterials;

import net.minecraft.world.level.material.Fluid;
import net.minecraftforge.fluids.FluidStack;

import com.raishxn.gtna.common.data.GTNAMaterials;
import com.raishxn.gtna.common.data.material.GodforgeChainMaterials;
import org.jetbrains.annotations.Nullable;

import java.util.function.Supplier;

import static com.gregtechceu.gtceu.api.GTValues.*;

/**
 * GTNH {@code CondensateType}: one entangled Bose-Einstein condensate per source material. The condensate is only made
 * by the BEC Entanglement Apparatus from the source's fluid ({@code unit} mB of source → {@code unit} mB of
 * condensate) and only moves through the BEC network. GTNH tiers map to GTCEu's: UMV → UXV, UXV → OpV. GTNA registers
 * each entangled fluid as a gas material
 * ({@code gtna:entangled_<id>}, see {@code BECMaterials}).
 */
public enum CondensateType {

    // spotless:off
    Neutronium("neutronium", () -> GTMaterials.Neutronium, 144, 30 * 20, VA[UEV]),
    CosmicNeutronium("cosmicneutronium", () -> GTNAMaterials.CosmicNeutronium, 144, 30 * 20, VA[UEV]),
    Bedrockium("bedrockium", () -> GodforgeChainMaterials.Bedrockium, 144, 30 * 20, VA[UEV]),
    ChromaticGlass("chromaticglass", () -> GodforgeChainMaterials.ChronomaticGlass, 144, 30 * 20, VA[UIV]),
    CelestialTungsten("celestialtungsten", () -> GodforgeChainMaterials.CelestialTungsten, 144, 30 * 20, VA[UIV]),
    Infinity("infinity", () -> GodforgeChainMaterials.Infinity, 144, 30 * 20, VA[UXV]),
    Hypogen("hypogen", () -> GodforgeChainMaterials.Hypogen, 144, 60 * 20, VA[OpV]),
    TranscendentMetal("transcendentmetal", () -> GodforgeChainMaterials.TranscendentMetal, 144, 60 * 20, VA[OpV]),
    DimensionallyShiftedSuperfluid("dimshiftedsuperfluid", () -> GodforgeChainMaterials.DimensionallyShiftedSuperfluid,
            1000, 60 * 20, VA[UXV]),
    PhononMedium("phononmedium", () -> GodforgeChainMaterials.PhononMedium, 1000, 90 * 20, VA[UXV]),
    QuarkGluonPlasma("quarkgluonplasma", () -> GTNAMaterials.QuarkGluonPlasma, 1000, 120 * 20, VA[UXV]),
    SpaceTime("spacetime", () -> GTNAMaterials.SpaceTime, 144, 120 * 20, VA[OpV]),
    Time("time", () -> GTNAMaterials.Time, 144, 120 * 20, VA[OpV]),
    Space("space", () -> GTNAMaterials.Space, 144, 120 * 20, VA[OpV]),
    BoundlessCosmicSolder("cosmicsolder", () -> GodforgeChainMaterials.BoundlessCosmicSolder, 1000, 120 * 20, VA[OpV]),
    MHDCSM("mhdcsm", () -> GTNAMaterials.MagnetohydrodynamicallyConstrainedStarMatter, 144, 180 * 20, 4 * VA[OpV]),
    MagMatter("magmatter", () -> GTNAMaterials.MagMatter, 144, 180 * 20, 4 * VA[OpV]),
    Universium("universium", () -> GTNAMaterials.Universium, 144, 180 * 20, 4 * VA[OpV]),
    Eternity("eternity", () -> GodforgeChainMaterials.Eternity, 144, 180 * 20, 4 * VA[OpV]);
    // spotless:on

    public static final CondensateType[] VALUES = values();

    public final String id;
    private final Supplier<Material> source;
    public final int unit;
    public final int duration;
    public final long eut;
    /** Set by {@code BECMaterials.register()}. */
    public Material entangled;

    CondensateType(String id, Supplier<Material> source, int unit, int duration, long eut) {
        this.id = id;
        this.source = source;
        this.unit = unit;
        this.duration = duration;
        this.eut = eut;
    }

    public Material getSource() {
        return source.get();
    }

    /** The source fluid (molten metal or the material's fluid), {@code unit} mB. */
    public FluidStack getSourceFluid() {
        return getSource().getFluid(unit);
    }

    public Fluid getEntangledFluid() {
        return entangled.getFluid();
    }

    /** As in GTNH, amounts must be multiples of half the unit. */
    public FluidStack getEntangled(int amount) {
        if (amount % (unit / 2) != 0) throw new IllegalArgumentException(
                "amount " + amount + " of condensate " + id + " is not a multiple of half its unit " + unit);
        return entangled.getFluid(amount);
    }

    public static @Nullable CondensateType getCondensateType(Fluid fluid) {
        for (CondensateType type : VALUES) if (type.entangled != null && type.getEntangledFluid() == fluid) return type;
        return null;
    }

    public static @Nullable CondensateType getCondensateTypeBySource(Fluid fluid) {
        for (CondensateType type : VALUES) if (type.getSource().getFluid() == fluid) return type;
        return null;
    }
}
