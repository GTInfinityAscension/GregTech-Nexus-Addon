package com.raishxn.gtna.common.machine.multiblock.electric.bec;

import com.gregtechceu.gtceu.api.capability.recipe.FluidRecipeCapability;
import com.gregtechceu.gtceu.api.capability.recipe.IO;
import com.gregtechceu.gtceu.api.gui.fancy.ConfiguratorPanel;
import com.gregtechceu.gtceu.api.gui.widget.PhantomFluidWidget;
import com.gregtechceu.gtceu.api.machine.IMachineBlockEntity;
import com.gregtechceu.gtceu.api.machine.feature.multiblock.IMultiPart;
import com.gregtechceu.gtceu.api.machine.trait.NotifiableFluidTank;
import com.gregtechceu.gtceu.api.machine.trait.RecipeLogic;
import com.gregtechceu.gtceu.api.recipe.GTRecipe;

import com.lowdragmc.lowdraglib.gui.widget.LabelWidget;
import com.lowdragmc.lowdraglib.gui.widget.WidgetGroup;
import com.lowdragmc.lowdraglib.syncdata.annotation.DescSynced;
import com.lowdragmc.lowdraglib.syncdata.annotation.Persisted;
import com.lowdragmc.lowdraglib.syncdata.field.ManagedFieldHolder;

import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import net.minecraft.world.level.material.Fluid;
import net.minecraftforge.fluids.FluidStack;

import com.raishxn.gtna.api.bec.BECNetwork;
import com.raishxn.gtna.api.bec.CondensateType;
import com.raishxn.gtna.api.bec.IBECHatch;
import com.raishxn.gtna.common.machine.multiblock.part.bec.BECHatchPartMachine;
import org.jetbrains.annotations.NotNull;

import java.util.*;

import static com.gregtechceu.gtceu.api.GTValues.UIV;
import static com.gregtechceu.gtceu.api.GTValues.VA;

/**
 * GTNH {@code MTEBECDiode} (Bose-Einstein Condensate Maxwell Gate). While running (1A UIV) it exposes the condensate
 * of its input hatch's side to its output hatch's side, never the other way: routes leave it only through the input
 * hatch. Filters (one per condensate type) limit what passes; with none set everything passes. Fluid input hatches
 * override the filters: each fluid in them (a source fluid or the condensate itself) becomes a filter.
 */
public class BECDiodeMachine extends BECMultiblockMachine {

    protected static final ManagedFieldHolder MANAGED_FIELD_HOLDER = new ManagedFieldHolder(
            BECDiodeMachine.class, BECMultiblockMachine.MANAGED_FIELD_HOLDER);

    /** Match-context key the pattern stores the input hatch position under. */
    public static final String INPUT_HATCH = "gtna_bec_diode_input";

    @Persisted
    @DescSynced
    private final FluidStack[] filters = new FluidStack[CondensateType.VALUES.length];
    private BlockPos inputHatchPos;
    private boolean wasWorking;

    public BECDiodeMachine(IMachineBlockEntity holder, Object... args) {
        super(holder, args);
        Arrays.fill(filters, FluidStack.EMPTY);
    }

    @Override
    public ManagedFieldHolder getFieldHolder() {
        return MANAGED_FIELD_HOLDER;
    }

    @Override
    protected RecipeLogic createRecipeLogic(Object... args) {
        return new RecipeLogic(this) {

            @Override
            public @NotNull Iterator<GTRecipe> searchRecipe() {
                if (!isFormed()) return Collections.emptyIterator();
                return List.of(cycle("maxwell_gate", VA[UIV], 1, 1)).iterator();
            }

            @Override
            public void setStatus(Status status) {
                super.setStatus(status);
                boolean working = status == Status.WORKING;
                if (working != wasWorking) {
                    wasWorking = working;
                    BECNetwork.invalidate();
                }
            }
        };
    }

    @Override
    public boolean alwaysTryModifyRecipe() {
        return false;
    }

    @Override
    public void onStructureFormed() {
        super.onStructureFormed();
        inputHatchPos = getMultiblockState().getMatchContext().get(INPUT_HATCH);
    }

    @Override
    public void onStructureInvalid() {
        super.onStructureInvalid();
        inputHatchPos = null;
    }

    /** GTNH {@code getRoutedDiscoverySeeds}: only the input hatch, and only while running. */
    @Override
    public List<? extends IBECHatch> getRoutedSeeds() {
        if (!wasWorking || inputHatchPos == null) return List.of();
        for (IMultiPart part : getParts())
            if (part instanceof BECHatchPartMachine hatch && hatch.getPos().equals(inputHatchPos))
                return List.of(hatch);
        return List.of();
    }

    @Override
    public boolean allowsCondensateThrough(Fluid condensate) {
        boolean hasFilter = false;
        for (FluidStack filter : filters) {
            if (filter.isEmpty()) continue;
            if (filter.getFluid() == condensate) return true;
            hasFilter = true;
        }
        return !hasFilter;
    }

    @Override
    public boolean onWorking() {
        if (!super.onWorking()) return false;
        deriveFiltersFromInputHatches();
        return true;
    }

    /** GTNH {@code deriveFiltersFromInputHatches}. */
    private void deriveFiltersFromInputHatches() {
        var tanks = getCapabilitiesFlat(IO.IN, FluidRecipeCapability.CAP);
        if (tanks.isEmpty()) return;
        EnumSet<CondensateType> present = EnumSet.noneOf(CondensateType.class);
        for (var handler : tanks) {
            if (!(handler instanceof NotifiableFluidTank tank)) continue;
            for (int i = 0; i < tank.getTanks(); i++) {
                FluidStack stack = tank.getFluidInTank(i);
                if (stack.isEmpty()) continue;
                CondensateType type = CondensateType.getCondensateTypeBySource(stack.getFluid());
                if (type == null) type = CondensateType.getCondensateType(stack.getFluid());
                if (type != null) present.add(type);
            }
        }
        boolean changed = false;
        int slot = 0;
        for (CondensateType type : present) {
            if (filters[slot].isEmpty() || filters[slot].getFluid() != type.getEntangledFluid()) {
                filters[slot] = new FluidStack(type.getEntangledFluid(), 1);
                changed = true;
            }
            slot++;
        }
        for (; slot < filters.length; slot++) {
            if (!filters[slot].isEmpty()) {
                filters[slot] = FluidStack.EMPTY;
                changed = true;
            }
        }
        if (changed) BECNetwork.invalidate();
    }

    public void setFilter(int slot, FluidStack fluid) {
        filters[slot] = fluid == null || fluid.isEmpty() || CondensateType.getCondensateType(fluid.getFluid()) == null ?
                FluidStack.EMPTY : new FluidStack(fluid.getFluid(), 1);
        BECNetwork.invalidate();
    }

    public FluidStack getFilter(int slot) {
        return filters[slot];
    }

    @Override
    public void addDisplayText(List<Component> textList) {
        super.addDisplayText(textList);
        if (isFormed()) addCondensateText(textList, "gtna.bec.gui.available_condensate", BECNetwork.stored(this));
    }

    @Override
    public void attachConfigurators(ConfiguratorPanel panel) {
        super.attachConfigurators(panel);
        panel.attachConfigurators(new BECConfigurator("gtna.bec.gui.parameters", () -> {
            var group = new WidgetGroup(0, 0, 4 + 20 * 7, 24 + 20 * 3);
            group.addWidget(new LabelWidget(4, 4, "gtna.bec.gui.filters"));
            for (int i = 0; i < filters.length; i++) {
                int slot = i;
                group.addWidget(new PhantomFluidWidget(null, 0, 4 + 20 * (i % 7), 18 + 20 * (i / 7), 18, 18,
                        () -> filters[slot], f -> setFilter(slot, f)).setShowAmount(false));
            }
            return group;
        }));
    }
}
