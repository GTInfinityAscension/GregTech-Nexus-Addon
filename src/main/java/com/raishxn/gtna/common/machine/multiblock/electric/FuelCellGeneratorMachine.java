package com.raishxn.gtna.common.machine.multiblock.electric;

import com.gregtechceu.gtceu.api.capability.IEnergyContainer;
import com.gregtechceu.gtceu.api.capability.recipe.EURecipeCapability;
import com.gregtechceu.gtceu.api.capability.recipe.FluidRecipeCapability;
import com.gregtechceu.gtceu.api.capability.recipe.IO;
import com.gregtechceu.gtceu.api.capability.recipe.ItemRecipeCapability;
import com.gregtechceu.gtceu.api.data.chemical.ChemicalHelper;
import com.gregtechceu.gtceu.api.data.chemical.material.Material;
import com.gregtechceu.gtceu.api.machine.IMachineBlockEntity;
import com.gregtechceu.gtceu.api.machine.MetaMachine;
import com.gregtechceu.gtceu.api.machine.multiblock.WorkableElectricMultiblockMachine;
import com.gregtechceu.gtceu.api.misc.EnergyContainerList;
import com.gregtechceu.gtceu.api.recipe.GTRecipe;
import com.gregtechceu.gtceu.api.recipe.RecipeHelper;
import com.gregtechceu.gtceu.api.recipe.content.ContentModifier;
import com.gregtechceu.gtceu.api.recipe.modifier.ModifierFunction;
import com.gregtechceu.gtceu.api.recipe.modifier.ParallelLogic;
import com.gregtechceu.gtceu.common.data.GTMaterials;
import com.gregtechceu.gtceu.data.recipe.builder.GTRecipeBuilder;

import com.lowdragmc.lowdraglib.syncdata.annotation.Persisted;
import com.lowdragmc.lowdraglib.syncdata.field.ManagedFieldHolder;

import net.minecraft.network.chat.Component;
import net.minecraft.world.item.ItemStack;

import com.raishxn.gtna.api.data.tag.GTNATagPrefix;
import com.raishxn.gtna.common.data.GTNARecipeType;
import com.raishxn.gtna.common.data.material.FuelCellMaterials;
import com.raishxn.gtna.common.data.material.FuelCellMaterials.Membrane;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.util.ArrayList;
import java.util.List;

/**
 * GTOCore {@code FullCellGenerator} (normal difficulty): three modes on one structure.
 * <ul>
 * <li><b>Absorption</b>: a fuel plus liquid oxygen charges a released electrolyte into its storage state. The best
 * membrane electrode in the inputs sets the efficiency ({@link Membrane#efficiencyBonus()}), multiplied by the
 * running decay; each run multiplies the decay by the membrane's factor. While idle, 600 mB of Distilled Water per
 * tick recovers {@link #DECAY_RECOVERY} of the lost efficiency.</li>
 * <li><b>Transfer</b>: moves charge between electrolytes (recipe {@code efficiency}).</li>
 * <li><b>Release</b>: discharges a charged electrolyte into EU, up to {@link #MAX_RELEASE_PARALLEL} parallel; each run
 * has a {@link #MEMBRANE_DAMAGE_CHANCE} chance to use up the membrane.</li>
 * </ul>
 * GTO's Ion Activity Sensor part is not ported.
 */
public class FuelCellGeneratorMachine extends WorkableElectricMultiblockMachine {

    protected static final ManagedFieldHolder MANAGED_FIELD_HOLDER = new ManagedFieldHolder(
            FuelCellGeneratorMachine.class, WorkableElectricMultiblockMachine.MANAGED_FIELD_HOLDER);

    public static final int MAX_RELEASE_PARALLEL = 50;
    public static final double MEMBRANE_DAMAGE_CHANCE = 0.0035d;
    public static final double DECAY_RECOVERY = 0.15d;
    public static final int RECOVERY_WATER = 600;

    @Persisted
    private double bonusEfficiency = 1.0d;
    @Persisted
    private double accumulatedDecay = 1.0d;

    public FuelCellGeneratorMachine(IMachineBlockEntity holder) {
        super(holder);
    }

    @Override
    public ManagedFieldHolder getFieldHolder() {
        return MANAGED_FIELD_HOLDER;
    }

    @Override
    public void onLoad() {
        super.onLoad();
        if (!isRemote()) subscribeServerTick(this::recoverWhileIdle);
    }

    private void recoverWhileIdle() {
        if (!isFormed() || !getRecipeLogic().isIdle() || accumulatedDecay >= 1.0d) return;
        GTRecipe water = GTRecipeBuilder.ofRaw()
                .inputFluids(GTMaterials.DistilledWater.getFluid(RECOVERY_WATER)).buildRawRecipe();
        if (RecipeHelper.handleRecipeIO(this, water, IO.IN, getRecipeLogic().getChanceCaches()).isSuccess()) {
            accumulatedDecay += (1.0d - accumulatedDecay) * DECAY_RECOVERY;
        }
    }

    public double getAccumulatedDecay() {
        return accumulatedDecay;
    }

    public void setAccumulatedDecay(double decay) {
        accumulatedDecay = decay;
    }

    @Override
    public boolean isGenerator() {
        return getRecipeType() == GTNARecipeType.FUEL_CELL_ENERGY_RELEASE_RECIPES;
    }

    /** Generator mode reads the dynamo/laser outputs, the charging modes the energy inputs. */
    @Override
    public EnergyContainerList getEnergyContainer() {
        List<IEnergyContainer> containers = new ArrayList<>();
        for (var handler : getCapabilitiesFlat(isGenerator() ? IO.OUT : IO.IN, EURecipeCapability.CAP)) {
            if (handler instanceof IEnergyContainer container) containers.add(container);
        }
        return new EnergyContainerList(containers);
    }

    @Override
    public void setActiveRecipeType(int activeRecipeType) {
        super.setActiveRecipeType(activeRecipeType);
        energyContainer = null;
    }

    /** The highest-tier membrane electrode present in the input buses, or null. */
    @Nullable
    public Membrane bestMembrane() {
        for (int i = FuelCellMaterials.MEMBRANES.length - 1; i >= 0; i--) {
            Membrane membrane = FuelCellMaterials.MEMBRANES[i];
            ItemStack stack = ChemicalHelper.get(GTNATagPrefix.membraneElectrode, membrane.membrane());
            GTRecipe probe = GTRecipeBuilder.ofRaw().inputItems(stack).buildRawRecipe();
            if (RecipeHelper.matchRecipe(this, probe).isSuccess()) return membrane;
        }
        return null;
    }

    /** Recipe modifier of all three modes (GTO {@code getRealRecipe}). */
    public static ModifierFunction recipeModifier(@NotNull MetaMachine machine, @NotNull GTRecipe recipe) {
        if (!(machine instanceof FuelCellGeneratorMachine cell)) return ModifierFunction.NULL;
        var type = recipe.recipeType;
        if (type == GTNARecipeType.FUEL_CELL_ENERGY_RELEASE_RECIPES) {
            int parallel = ParallelLogic.getParallelAmountWithoutEU(machine, recipe, MAX_RELEASE_PARALLEL);
            return parallel(parallel);
        } else if (type == GTNARecipeType.FUEL_CELL_ENERGY_TRANSFER_RECIPES) {
            if (recipe.data.getFloat("efficiency") <= 0) return ModifierFunction.NULL;
            int parallel = ParallelLogic.getParallelAmount(machine, recipe, Integer.MAX_VALUE);
            return parallel(parallel);
        } else if (type == GTNARecipeType.FUEL_CELL_ENERGY_ABSORPTION_RECIPES) {
            return cell.absorption(recipe);
        }
        return ModifierFunction.IDENTITY;
    }

    private static ModifierFunction parallel(int parallel) {
        if (parallel <= 0) return ModifierFunction.NULL;
        if (parallel == 1) return ModifierFunction.IDENTITY;
        return ModifierFunction.builder()
                .inputModifier(ContentModifier.multiplier(parallel))
                .outputModifier(ContentModifier.multiplier(parallel))
                .eutMultiplier(parallel)
                .parallels(parallel)
                .build();
    }

    /**
     * GTO {@code getAbsorptionRecipe}: the energy the fuel stores is spread over the electrolyte present (both
     * released states), which moves to its storage states in the same amount.
     */
    private ModifierFunction absorption(GTRecipe recipe) {
        Membrane membrane = bestMembrane();
        if (membrane == null) {
            return ModifierFunction.cancel(Component.translatable("gtna.machine.fuel_cell.no_membrane"));
        }
        double efficiency = membrane.efficiencyBonus() * accumulatedDecay;
        long energyPerRun = (long) (recipe.data.getLong("converted_energy") * efficiency);
        if (energyPerRun <= 0) return ModifierFunction.NULL;

        for (var entry : FuelCellMaterials.EU_PER_MB.entrySet()) {
            Material electrolyte = entry.getKey();
            long euPerMb = entry.getValue();
            long available = Math.min(amount(electrolyte, FuelCellMaterials.ENERGY_RELEASE_ANODE),
                    amount(electrolyte, FuelCellMaterials.ENERGY_RELEASE_CATHODE));
            if (available <= 0) continue;
            long maxRuns = available * euPerMb / energyPerRun;
            int parallel = ParallelLogic.getParallelAmount(this, recipe, (int) Math.min(Integer.MAX_VALUE, maxRuns));
            if (parallel <= 0) return ModifierFunction.NULL;
            long moved = parallel * energyPerRun / euPerMb;
            if (moved <= 0) return ModifierFunction.NULL;
            return original -> {
                GTRecipe scaled = parallel(parallel).apply(original);
                if (scaled == null) return null;
                GTRecipe charged = GTRecipeBuilder.ofRaw()
                        .inputFluids(electrolyte.getFluid(FuelCellMaterials.ENERGY_RELEASE_ANODE, (int) moved))
                        .inputFluids(electrolyte.getFluid(FuelCellMaterials.ENERGY_RELEASE_CATHODE, (int) moved))
                        .outputFluids(electrolyte.getFluid(FuelCellMaterials.ENERGY_STORAGE_ANODE, (int) moved))
                        .outputFluids(electrolyte.getFluid(FuelCellMaterials.ENERGY_STORAGE_CATHODE, (int) moved))
                        .buildRawRecipe();
                GTRecipe result = scaled.copy();
                append(result.inputs, charged.inputs);
                append(result.outputs, charged.outputs);
                return result;
            };
        }
        return ModifierFunction.cancel(Component.translatable("gtna.machine.fuel_cell.no_electrolyte"));
    }

    private static void append(java.util.Map<com.gregtechceu.gtceu.api.capability.recipe.RecipeCapability<?>, List<com.gregtechceu.gtceu.api.recipe.content.Content>> target,
                               java.util.Map<com.gregtechceu.gtceu.api.capability.recipe.RecipeCapability<?>, List<com.gregtechceu.gtceu.api.recipe.content.Content>> extra) {
        extra.forEach((cap, contents) -> {
            List<com.gregtechceu.gtceu.api.recipe.content.Content> list = new ArrayList<>(
                    target.getOrDefault(cap, List.of()));
            list.addAll(contents);
            target.put(cap, list);
        });
    }

    private long amount(Material electrolyte, com.gregtechceu.gtceu.api.fluids.store.FluidStorageKey key) {
        var fluid = electrolyte.getFluid(key);
        long total = 0;
        for (var handler : getCapabilitiesFlat(IO.IN, FluidRecipeCapability.CAP)) {
            for (Object content : handler.getContents()) {
                if (content instanceof net.minecraftforge.fluids.FluidStack stack && stack.getFluid() == fluid) {
                    total += stack.getAmount();
                }
            }
        }
        return total;
    }

    @Override
    public boolean beforeWorking(@Nullable GTRecipe recipe) {
        if (!super.beforeWorking(recipe)) return false;
        if (recipe == null) return true;
        if (recipe.recipeType == GTNARecipeType.FUEL_CELL_ENERGY_ABSORPTION_RECIPES) {
            Membrane membrane = bestMembrane();
            if (membrane != null) {
                bonusEfficiency = membrane.efficiencyBonus() * accumulatedDecay;
                accumulatedDecay *= membrane.decayFactor();
            }
        } else if (recipe.recipeType == GTNARecipeType.FUEL_CELL_ENERGY_TRANSFER_RECIPES) {
            bonusEfficiency = recipe.data.getFloat("efficiency") * 0.25d;
        } else if (recipe.recipeType == GTNARecipeType.FUEL_CELL_ENERGY_RELEASE_RECIPES &&
                getLevel() != null && getLevel().random.nextDouble() < MEMBRANE_DAMAGE_CHANCE) {
                    for (var content : recipe.getInputContents(ItemRecipeCapability.CAP)) {
                        var items = ItemRecipeCapability.CAP.of(content.content).getItems();
                        if (items.length == 0) continue;
                        GTRecipe damage = GTRecipeBuilder.ofRaw().inputItems(items[0].copy()).buildRawRecipe();
                        RecipeHelper.handleRecipeIO(this, damage, IO.IN, getRecipeLogic().getChanceCaches());
                        break;
                    }
                }
        return true;
    }

    @Override
    public void afterWorking() {
        super.afterWorking();
        bonusEfficiency = 1.0d;
    }

    @Override
    public void addDisplayText(List<Component> textList) {
        super.addDisplayText(textList);
        if (isFormed() && !isGenerator()) {
            textList.add(Component.translatable("gtna.machine.fuel_cell.efficiency",
                    String.format("%.2f%%", bonusEfficiency * 100)));
            textList.add(Component.translatable("gtna.machine.fuel_cell.decay",
                    String.format("%.4f%%", (1 - accumulatedDecay) * 100)));
        }
    }
}
