package com.raishxn.gtna.common.machine.multiblock.electric;

import com.gregtechceu.gtceu.api.GTValues;
import com.gregtechceu.gtceu.api.capability.IOpticalComputationProvider;
import com.gregtechceu.gtceu.api.capability.recipe.IO;
import com.gregtechceu.gtceu.api.data.chemical.ChemicalHelper;
import com.gregtechceu.gtceu.api.data.tag.TagPrefix;
import com.gregtechceu.gtceu.api.machine.IMachineBlockEntity;
import com.gregtechceu.gtceu.api.machine.TickableSubscription;
import com.gregtechceu.gtceu.api.machine.feature.multiblock.IMultiPart;
import com.gregtechceu.gtceu.api.machine.multiblock.WorkableElectricMultiblockMachine;
import com.gregtechceu.gtceu.api.pattern.BlockPattern;
import com.gregtechceu.gtceu.api.recipe.GTRecipe;
import com.gregtechceu.gtceu.api.recipe.RecipeHelper;
import com.gregtechceu.gtceu.common.data.GTMaterials;
import com.gregtechceu.gtceu.common.machine.multiblock.part.hpca.HPCABridgePartMachine;
import com.gregtechceu.gtceu.common.machine.multiblock.part.hpca.HPCAComponentPartMachine;
import com.gregtechceu.gtceu.common.machine.multiblock.part.hpca.HPCAComputationPartMachine;
import com.gregtechceu.gtceu.common.machine.multiblock.part.hpca.HPCACoolerPartMachine;
import com.gregtechceu.gtceu.data.recipe.builder.GTRecipeBuilder;

import com.lowdragmc.lowdraglib.syncdata.annotation.DescSynced;
import com.lowdragmc.lowdraglib.syncdata.annotation.Persisted;
import com.lowdragmc.lowdraglib.syncdata.field.ManagedFieldHolder;

import net.minecraft.ChatFormatting;
import net.minecraft.core.Direction;
import net.minecraft.network.chat.Component;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.phys.BlockHitResult;

import com.raishxn.gtna.api.machine.multiblock.GTNAStructureRefresh;
import com.raishxn.gtna.common.data.GTNACircuits;
import com.raishxn.gtna.common.data.GTNAMegaMachines;
import com.raishxn.gtna.common.data.material.ResearchMaterials;
import com.raishxn.gtna.common.machine.multiblock.part.research.ExResearchPartMachine;
import com.raishxn.gtna.common.machine.multiblock.part.research.ThermalConductorHatchPartMachine;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.util.Collection;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * GTOCore {@code SupercomputingCenterMachine}: a tiered HPCA. Tier 1 takes GTCEu HPCA components, tier 2 NICH and
 * tier 3 GWCA; each tier has its own computer casing, heat vent and minimum glass (built into the tier's pattern).
 * Every {@link #CYCLE} ticks it pays the components' upkeep (a quarter at tier 1) and, when cooling is needed, PCB
 * Coolant (tier 1) or liquid Helium (tiers 2-3, returned as gas); while paid it supplies its CWU/t. Cooling below
 * demand damages computation components after each cycle. At tiers 2-3 the CWU/t multiplier decays and is restored by
 * MFPC coolant in the Thermal Conductor Hatch (GTO formula).
 * <p>
 * GTO picks the tier from a Bioware / Supracausal Mainframe in a controller slot; GTNA has neither, so the tier is
 * chosen with a screwdriver and tiers 2 and 3 need an Optical / Exotic Mainframe in an input bus (not consumed).
 */
public class SupercomputingCenterMachine extends WorkableElectricMultiblockMachine
                                         implements IOpticalComputationProvider {

    protected static final ManagedFieldHolder MANAGED_FIELD_HOLDER = new ManagedFieldHolder(
            SupercomputingCenterMachine.class, WorkableElectricMultiblockMachine.MANAGED_FIELD_HOLDER);

    public static final int CYCLE = 20;
    public static final int MODIFICATION_BASE = 10000;
    /** GTO {@code N_MFPCs}: multiplier points restored per item, per GTO item order. */
    private static final int[] MFPC_POINTS = { 5400, 1800, 600, 200, 66, 22, 1 };

    @Persisted
    @DescSynced
    private int machineTier = 1;
    @Persisted
    private int maxCWUtModification = MODIFICATION_BASE;

    private boolean incompatible;
    private boolean canBridge;
    private int maxCWUt;
    private int coolingRequired;
    private int coolingProvided;
    private int coolantAmount;
    private long upkeepEUt;
    private boolean active;
    private long allocatedCWUt;
    private long cachedCWUt;
    private long lastTick = -1;
    @Nullable
    private ThermalConductorHatchPartMachine thermalHatch;
    @Nullable
    private TickableSubscription tickSubs;

    public SupercomputingCenterMachine(IMachineBlockEntity holder) {
        super(holder);
    }

    @Override
    public ManagedFieldHolder getFieldHolder() {
        return MANAGED_FIELD_HOLDER;
    }

    public int getMachineTier() {
        return machineTier;
    }

    public void setMachineTier(int tier) {
        machineTier = Math.max(1, Math.min(3, tier));
    }

    @Override
    public BlockPattern getPattern() {
        return GTNAMegaMachines.supercomputingPattern(machineTier, getDefinition());
    }

    @Override
    protected InteractionResult onScrewdriverClick(Player player, InteractionHand hand, Direction gridSide,
                                                   BlockHitResult hitResult) {
        if (isRemote()) return InteractionResult.SUCCESS;
        setMachineTier(machineTier % 3 + 1);
        player.sendSystemMessage(Component.translatable("gtna.machine.supercomputing_center.tier", machineTier));
        GTNAStructureRefresh.refresh(this, true);
        return InteractionResult.CONSUME;
    }

    /** The mainframe tiers 2 and 3 need in an input bus (GTO: Bioware / Supracausal). */
    @Nullable
    public static Item requiredMainframe(int tier) {
        return tier == 2 ? GTNACircuits.OPTICAL_MAINFRAME.get() : tier == 3 ? GTNACircuits.EXOTIC_MAINFRAME.get() :
                null;
    }

    @Override
    public void onStructureFormed() {
        super.onStructureFormed();
        scan();
        tickSubs = subscribeServerTick(tickSubs, this::tick);
    }

    @Override
    public void onStructureInvalid() {
        super.onStructureInvalid();
        thermalHatch = null;
        maxCWUtModification = MODIFICATION_BASE;
        active = false;
        if (tickSubs != null) {
            tickSubs.unsubscribe();
            tickSubs = null;
        }
    }

    /** GTO {@code changed}: reads the components and works out upkeep, CWU/t and cooling. */
    public void scan() {
        incompatible = false;
        canBridge = machineTier == 3;
        maxCWUt = 0;
        coolingRequired = 0;
        coolingProvided = 0;
        coolantAmount = 0;
        upkeepEUt = 0;
        thermalHatch = null;
        int maxCoolant = 0;
        int passiveCooling = 0;
        for (IMultiPart part : getParts()) {
            if (part instanceof ThermalConductorHatchPartMachine hatch && thermalHatch == null) thermalHatch = hatch;
            if (!(part instanceof HPCAComponentPartMachine component)) continue;
            upkeepEUt += component.getMaxEUt();
            if (component instanceof ExResearchPartMachine ex) {
                if (ex.getTier() - 1 != machineTier) {
                    incompatible = true;
                    return;
                }
                if (ex instanceof ExResearchPartMachine.Bridge) canBridge = true;
                if (ex instanceof ExResearchPartMachine.Computation c && !c.isDamaged()) {
                    maxCWUt += c.getCWUPerTick();
                    coolingRequired += c.getCoolingPerTick();
                }
                if (ex instanceof ExResearchPartMachine.Cooler c) {
                    coolingProvided += c.getCoolingAmount();
                    maxCoolant += c.getMaxCoolantPerTick();
                }
            } else {
                if (machineTier > 1) {
                    incompatible = true;
                    return;
                }
                if (component instanceof HPCABridgePartMachine) canBridge = true;
                if (component instanceof HPCAComputationPartMachine c && !c.isDamaged()) {
                    maxCWUt += c.getCWUPerTick();
                    coolingRequired += c.getCoolingPerTick();
                }
                if (component instanceof HPCACoolerPartMachine c) {
                    coolingProvided += c.getCoolingAmount();
                    if (!c.isActiveCooler()) passiveCooling += c.getCoolingAmount();
                    maxCoolant += c.getMaxCoolantPerTick();
                }
            }
        }
        if (coolingProvided > passiveCooling) {
            double ratio = (double) maxCoolant / (coolingProvided - passiveCooling);
            coolantAmount = (int) Math.ceil(Math.max(0, coolingRequired - passiveCooling) * ratio);
        }
        if (machineTier == 1) upkeepEUt /= 4;
    }

    /** The coolant and mainframe check paid each cycle (GTO {@code runRecipe}, without its EU). */
    private GTRecipe cycleRecipe() {
        var builder = GTRecipeBuilder.ofRaw();
        Item mainframe = requiredMainframe(machineTier);
        if (mainframe != null) builder.notConsumable(new ItemStack(mainframe));
        if (coolantAmount > 0) {
            if (machineTier == 1) {
                builder.inputFluids(GTMaterials.PCBCoolant.getFluid(coolantAmount * CYCLE));
            } else {
                builder.inputFluids(GTMaterials.Helium.getFluid(
                        com.gregtechceu.gtceu.api.fluids.store.FluidStorageKeys.LIQUID, coolantAmount * CYCLE));
                builder.outputFluids(GTMaterials.Helium.getFluid(coolantAmount * CYCLE));
            }
        }
        return builder.buildRawRecipe();
    }

    private void tick() {
        long timer = getOffsetTimer();
        if (timer != lastTick) {
            lastTick = timer;
            cachedCWUt = allocatedCWUt;
            allocatedCWUt = 0;
        }
        if (timer % 10 == 0) updateModification();
        if (timer % CYCLE != 0) return;
        active = false;
        if (incompatible || upkeepEUt <= 0 || !isWorkingEnabled()) return;
        long energy = upkeepEUt * CYCLE;
        var container = getEnergyContainer();
        if (container.getEnergyStored() < energy) return;
        GTRecipe cycle = cycleRecipe();
        if (!RecipeHelper.matchRecipe(this, cycle).isSuccess()) return;
        RecipeHelper.handleRecipeIO(this, cycle, IO.IN, getRecipeLogic().getChanceCaches());
        RecipeHelper.handleRecipeIO(this, cycle, IO.OUT, getRecipeLogic().getChanceCaches());
        container.removeEnergy(energy);
        active = true;
        damageWhenOverheated();
    }

    /** GTO {@code afterWorking}: missing cooling damages computation components. */
    private void damageWhenOverheated() {
        if (coolingRequired <= coolingProvided || getLevel() == null) return;
        int damage = coolingRequired - coolingProvided;
        boolean changed = false;
        for (IMultiPart part : getParts()) {
            if (part instanceof HPCAComponentPartMachine component && component.canBeDamaged() &&
                    !component.isDamaged()) {
                damage -= getLevel().random.nextInt(256);
                component.setDamaged(true);
                changed = true;
            }
            if (damage <= 0) break;
        }
        if (changed) scan();
    }

    /** GTO {@code maxCWUtModificationUpdate}. */
    private void updateModification() {
        if (machineTier <= 1) {
            maxCWUtModification = MODIFICATION_BASE;
            return;
        }
        int max = machineTier == 2 ? 40000 : 160000;
        maxCWUtModification -= (int) ((Math.pow(maxCWUtModification - 4000, 2) / 500000) *
                (0.8 / (Math.log(maxCWUtModification + 600000) - Math.log(10000))));
        if (maxCWUtModification <= max && thermalHatch != null) {
            var storage = thermalHatch.getInventory().storage;
            Map<Item, Item> spent = mfpcs();
            List<Item> order = List.copyOf(spent.keySet());
            for (int i = 0; i < storage.getSlots() && maxCWUtModification < max; i++) {
                ItemStack stack = storage.getStackInSlot(i);
                int index = order.indexOf(stack.getItem());
                if (index < 0) continue;
                int used = Math.min(stack.getCount(), (max - maxCWUtModification) / MFPC_POINTS[index] + 1);
                storage.setStackInSlot(i, stack.copyWithCount(stack.getCount() - used));
                maxCWUtModification += MFPC_POINTS[index] * used;
                ItemStack result = new ItemStack(spent.get(stack.getItem()), used);
                for (int j = 0; j < storage.getSlots() && !result.isEmpty(); j++) {
                    result = storage.insertItem(j, result, false);
                }
            }
        }
        if (maxCWUtModification < 8000) maxCWUtModification = 8000;
    }

    /**
     * Fresh MFPC item -> its spent form, in GTO's order (block, ingot, nugget; Cascade before Basic), then Ice Shard.
     */
    private static Map<Item, Item> mfpcs() {
        Map<Item, Item> map = new LinkedHashMap<>();
        for (TagPrefix prefix : new TagPrefix[] { TagPrefix.block, TagPrefix.ingot, TagPrefix.nugget }) {
            map.put(ChemicalHelper.get(prefix, ResearchMaterials.CascadeMFPC).getItem(),
                    ChemicalHelper.get(prefix, ResearchMaterials.InvalidationCascadeMFPC).getItem());
            map.put(ChemicalHelper.get(prefix, ResearchMaterials.BasicMFPC).getItem(),
                    ChemicalHelper.get(prefix, ResearchMaterials.InvalidationBasicMFPC).getItem());
        }
        map.put(earth.terrarium.adastra.common.registry.ModItems.ICE_SHARD.get(),
                ChemicalHelper.get(TagPrefix.dustTiny, GTMaterials.Ice).getItem());
        return map;
    }

    public long adjustedMaxCWUt() {
        return (long) maxCWUt * maxCWUtModification / MODIFICATION_BASE;
    }

    public boolean isComputing() {
        return active && !incompatible;
    }

    @Override
    public int requestCWUt(int cwut, boolean simulate, @NotNull Collection<IOpticalComputationProvider> seen) {
        seen.add(this);
        if (!isComputing()) return 0;
        long available = Math.max(0, adjustedMaxCWUt() - allocatedCWUt);
        int given = (int) Math.min(cwut, available);
        if (!simulate) allocatedCWUt += given;
        return given;
    }

    @Override
    public int getMaxCWUt(@NotNull Collection<IOpticalComputationProvider> seen) {
        seen.add(this);
        return isComputing() ? (int) Math.min(Integer.MAX_VALUE, adjustedMaxCWUt()) : 0;
    }

    @Override
    public boolean canBridge(@NotNull Collection<IOpticalComputationProvider> seen) {
        seen.add(this);
        return !incompatible && canBridge;
    }

    public int getRawMaxCWUt() {
        return maxCWUt;
    }

    public long getUpkeepEUt() {
        return upkeepEUt;
    }

    public int getCoolantAmount() {
        return coolantAmount;
    }

    public boolean isIncompatible() {
        return incompatible;
    }

    @Override
    public void addDisplayText(List<Component> textList) {
        super.addDisplayText(textList);
        if (!isFormed()) return;
        textList.add(Component.translatable("gtna.machine.supercomputing_center.tier", machineTier));
        if (incompatible) {
            textList.add(Component.translatable("gtna.machine.supercomputing_center.incompatible")
                    .withStyle(ChatFormatting.RED));
            return;
        }
        textList.add(Component.translatable(canBridge ? "gtceu.multiblock.hpca.info_bridging_enabled" :
                "gtceu.multiblock.hpca.info_bridging_disabled")
                .withStyle(canBridge ? ChatFormatting.GREEN : ChatFormatting.RED));
        textList.add(Component.translatable("gtceu.multiblock.energy_consumption", upkeepEUt,
                GTValues.VNF[com.gregtechceu.gtceu.utils.GTUtil.getTierByVoltage(Math.max(1, upkeepEUt))]));
        textList.add(Component.translatable("gtceu.multiblock.hpca.computation",
                Component.literal(cachedCWUt + " / " + adjustedMaxCWUt() + " CWU/t").withStyle(ChatFormatting.AQUA)));
        textList.add(Component.translatable("gtna.machine.supercomputing_center.modification",
                String.format("%.2f", maxCWUtModification / (double) MODIFICATION_BASE)));
        textList.add(Component.translatable("gtceu.multiblock.hpca.info_max_coolant_required",
                Component.literal(coolingRequired + " / " + coolingProvided + "  " + coolantAmount)
                        .withStyle(ChatFormatting.AQUA)));
    }
}
