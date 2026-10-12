package com.raishxn.gtna.common.machine.multiblock.electric.bec;

import com.gregtechceu.gtceu.api.machine.IMachineBlockEntity;
import com.gregtechceu.gtceu.api.machine.TickableSubscription;
import com.gregtechceu.gtceu.api.machine.feature.multiblock.IMultiPart;
import com.gregtechceu.gtceu.api.machine.trait.RecipeLogic;
import com.gregtechceu.gtceu.api.recipe.GTRecipe;
import com.gregtechceu.gtceu.utils.FormattingUtil;

import com.lowdragmc.lowdraglib.syncdata.annotation.DescSynced;
import com.lowdragmc.lowdraglib.syncdata.field.ManagedFieldHolder;

import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.world.level.material.Fluid;

import com.raishxn.gtna.api.bec.BECNetwork;
import com.raishxn.gtna.api.bec.CondensateStack;
import com.raishxn.gtna.api.bec.NaniteTier;
import com.raishxn.gtna.common.machine.multiblock.part.bec.LineOfSightHatchPartMachine;
import com.raishxn.gtna.common.machine.multiblock.part.bec.NaniteContainmentBusPartMachine;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.util.*;

/**
 * GTNH {@code MTEBECAssembler} (Bose-Einstein Condensate Observation Array). It crafts nothing itself: it feeds the
 * Teleportation Nodes linked to its Line-of-Sight connectors with nanites (the lowest tier among its Nanite
 * Containment Buses, at most {@value #MAX_NANITES} in total), with EU (each node's EU/t, while the array can supply
 * it) and with condensate from the network.
 */
public class BECAssemblerMachine extends BECMultiblockMachine {

    protected static final ManagedFieldHolder MANAGED_FIELD_HOLDER = new ManagedFieldHolder(
            BECAssemblerMachine.class, BECMultiblockMachine.MANAGED_FIELD_HOLDER);

    public static final int MAX_NANITES = 2048 * 15;

    /** Ordinal of the provided {@link NaniteTier}, -1 for none. */
    @DescSynced
    private int naniteTier = -1;
    @DescSynced
    private int availableNanites;
    private boolean nanitesDirty = true;
    @Nullable
    private TickableSubscription tickSubs;

    public BECAssemblerMachine(IMachineBlockEntity holder, Object... args) {
        super(holder, args);
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
                return isFormed() ? List.of(cycle("observation_array", 0, 0, 20)).iterator() :
                        Collections.emptyIterator();
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
        nanitesDirty = true;
        if (!isRemote()) tickSubs = subscribeServerTick(tickSubs, this::tick);
    }

    @Override
    public void onStructureInvalid() {
        super.onStructureInvalid();
        if (tickSubs != null) {
            tickSubs.unsubscribe();
            tickSubs = null;
        }
        for (BECIONodeMachine node : getIONodes()) node.setPowered(false);
        naniteTier = -1;
        availableNanites = 0;
    }

    public boolean isRunning() {
        return isFormed() && getRecipeLogic().isWorking();
    }

    public @Nullable NaniteTier getCurrentNaniteTier() {
        return NaniteTier.byOrdinal(naniteTier);
    }

    public int getAvailableNanites() {
        return availableNanites;
    }

    /** Teleportation Nodes whose Line-of-Sight connector is paired with one of ours. */
    public List<BECIONodeMachine> getIONodes() {
        List<BECIONodeMachine> nodes = new ArrayList<>();
        for (IMultiPart part : getParts()) {
            if (!(part instanceof LineOfSightHatchPartMachine los)) continue;
            var other = los.getConnectedHatch();
            if (other != null && other.getOwnerMachine() instanceof BECIONodeMachine node && !nodes.contains(node))
                nodes.add(node);
        }
        return nodes;
    }

    /** GTNH {@code onPostTick}: refresh nanites, then power as many nodes as the energy hatches can supply. */
    private void tick() {
        for (IMultiPart part : getParts()) {
            if (part instanceof NaniteContainmentBusPartMachine bus && bus.pollChanged()) nanitesDirty = true;
        }
        if (nanitesDirty) {
            nanitesDirty = false;
            NaniteTier lowest = null;
            long count = 0;
            for (IMultiPart part : getParts()) {
                if (!(part instanceof NaniteContainmentBusPartMachine bus)) continue;
                NaniteTier tier = bus.getNaniteTier();
                if (tier == null) continue;
                if (lowest == null || tier.ordinal() < lowest.ordinal()) lowest = tier;
                count += bus.getNaniteCount();
            }
            naniteTier = lowest == null ? -1 : lowest.ordinal();
            availableNanites = (int) Math.min(MAX_NANITES, count);
        }
        List<BECIONodeMachine> nodes = getIONodes();
        var energy = getEnergyContainer();
        long budget = energy.getInputVoltage() * energy.getInputAmperage();
        long requested = 0;
        List<BECIONodeMachine> powered = new ArrayList<>();
        for (BECIONodeMachine node : nodes) {
            node.setPowered(false);
            long request = node.getAssemblerEUt();
            if (budget >= request) {
                budget -= request;
                requested += request;
                powered.add(node);
            }
        }
        if (requested > 0) {
            long drained = energy.removeEnergy(requested);
            if (drained < requested) {
                // you really don't want to powerfail
                for (BECIONodeMachine node : powered) node.powerFail();
                return;
            }
        }
        for (BECIONodeMachine node : powered) node.setPowered(true);
    }

    public void drainCondensate(CondensateStack stack) {
        BECNetwork.drain(this, stack);
    }

    public int getSlowdowns(Collection<Fluid> valid) {
        return BECNetwork.slowdowns(this, valid);
    }

    @Override
    public void addDisplayText(List<Component> textList) {
        super.addDisplayText(textList);
        if (!isFormed()) return;
        textList.add(Component.translatable("gtna.bec.gui.providing_nanites").withStyle(ChatFormatting.GRAY));
        NaniteTier tier = getCurrentNaniteTier();
        textList.add(Component.literal("  ").append(tier == null ? Component.translatable("gtna.bec.gui.none") :
                BECIONodeMachine.describe(tier).copy().withStyle(ChatFormatting.AQUA))
                .append(Component.literal(" x ").withStyle(ChatFormatting.GRAY))
                .append(Component.literal(FormattingUtil.formatNumbers(availableNanites))
                        .withStyle(ChatFormatting.GOLD)));
        addCondensateText(textList, "gtna.bec.gui.available_condensate", BECNetwork.stored(this));
    }
}
