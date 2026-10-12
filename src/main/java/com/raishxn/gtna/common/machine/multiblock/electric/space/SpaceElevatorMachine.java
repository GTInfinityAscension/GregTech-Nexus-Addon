package com.raishxn.gtna.common.machine.multiblock.electric.space;

import com.gregtechceu.gtceu.api.GTValues;
import com.gregtechceu.gtceu.api.capability.recipe.IO;
import com.gregtechceu.gtceu.api.capability.recipe.ItemRecipeCapability;
import com.gregtechceu.gtceu.api.machine.IMachineBlockEntity;
import com.gregtechceu.gtceu.api.machine.MetaMachine;
import com.gregtechceu.gtceu.api.machine.MultiblockMachineDefinition;
import com.gregtechceu.gtceu.api.machine.multiblock.WorkableElectricMultiblockMachine;
import com.gregtechceu.gtceu.api.machine.trait.RecipeLogic;
import com.gregtechceu.gtceu.api.pattern.TraceabilityPredicate;
import com.gregtechceu.gtceu.api.pattern.error.PatternStringError;
import com.gregtechceu.gtceu.api.recipe.GTRecipe;
import com.gregtechceu.gtceu.api.recipe.RecipeHelper;
import com.gregtechceu.gtceu.data.recipe.builder.GTRecipeBuilder;

import com.lowdragmc.lowdraglib.syncdata.annotation.Persisted;
import com.lowdragmc.lowdraglib.syncdata.field.ManagedFieldHolder;
import com.lowdragmc.lowdraglib.utils.BlockInfo;

import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.ItemStack;

import com.raishxn.gtna.common.data.GTNABlocks;
import com.raishxn.gtna.common.data.GTNAItems;
import org.jetbrains.annotations.Nullable;

import java.util.ArrayList;
import java.util.List;
import java.util.Set;
import java.util.function.Supplier;

/**
 * GTOCore {@code space_elevator} ({@code SpaceElevatorMachine}): above ZPM it runs a 400-tick upkeep cycle (EU of its
 * tier and {@code 128 x (tier - ZPM)} CWU/t) and, once it holds 256 Nanotube Spools fed through its input bus, drives
 * the modules standing in its twelve module slots. The Power Module MK tier (all the same) sets the modules' parallel
 * and which Assembler Module recipes they may run. Not ported: GTO's link to its space station (a 1.5x CWU bonus) and
 * the planet-teleport button (GTO's own planets).
 */
public class SpaceElevatorMachine extends WorkableElectricMultiblockMachine {

    public static final String POWER_MODULE_KEY = "gtna_power_module_tier";
    public static final String MODULES_KEY = "gtna_space_elevator_modules";
    public static final int MAX_SPOOLS = 256;

    @Persisted
    private int spoolCount;
    private int powerModuleTier;
    private final List<SpaceElevatorModuleMachine> modules = new ArrayList<>();

    public SpaceElevatorMachine(IMachineBlockEntity holder, Object... args) {
        super(holder, args);
    }

    protected static final ManagedFieldHolder MANAGED_FIELD_HOLDER = new ManagedFieldHolder(
            SpaceElevatorMachine.class, WorkableElectricMultiblockMachine.MANAGED_FIELD_HOLDER);

    @Override
    public ManagedFieldHolder getFieldHolder() {
        return MANAGED_FIELD_HOLDER;
    }

    /** Any Power Module MK I-V; all of them in one structure must be the same tier. */
    public static TraceabilityPredicate powerModules() {
        return new TraceabilityPredicate(state -> {
            int tier = GTNABlocks.spaceElevatorPowerModuleTier(state.getBlockState().getBlock());
            if (tier == 0) return false;
            Object current = state.getMatchContext().getOrPut(POWER_MODULE_KEY, tier);
            if (!current.equals(tier)) {
                state.setError(new PatternStringError("gtna.multiblock.pattern.error.power_module"));
                return false;
            }
            return true;
        }, () -> GTNABlocks.SPACE_ELEVATOR_POWER_MODULES.stream()
                .map(b -> BlockInfo.fromBlockState(b.get().defaultBlockState())).toArray(BlockInfo[]::new))
                .addTooltips(Component.translatable("gtna.multiblock.pattern.error.power_module"));
    }

    /** A module slot: one of the given module controllers, or nothing; the controllers found are remembered. */
    @SafeVarargs
    public static TraceabilityPredicate moduleSlot(Supplier<MultiblockMachineDefinition>... moduleDefinitions) {
        return new TraceabilityPredicate(state -> {
            if (state.getBlockState().isAir()) return true;
            for (var definition : moduleDefinitions) {
                if (state.getBlockState().is(definition.get().getBlock())) {
                    Set<BlockPos> found = state.getMatchContext().getOrCreate(MODULES_KEY,
                            java.util.HashSet::new);
                    found.add(state.getPos().immutable());
                    return true;
                }
            }
            return false;
        }, () -> new BlockInfo[] { BlockInfo.fromBlockState(net.minecraft.world.level.block.Blocks.AIR
                .defaultBlockState()) });
    }

    @Override
    public void onStructureFormed() {
        super.onStructureFormed();
        Object tier = getMultiblockState().getMatchContext().get(POWER_MODULE_KEY);
        powerModuleTier = tier instanceof Integer t ? t : 1;
        bindModules();
    }

    @Override
    public void onStructureInvalid() {
        super.onStructureInvalid();
        unbindModules();
        powerModuleTier = 0;
    }

    @Override
    public void onUnload() {
        super.onUnload();
        unbindModules();
    }

    private void bindModules() {
        unbindModules();
        Set<BlockPos> positions = getMultiblockState().getMatchContext().getOrDefault(MODULES_KEY, Set.of());
        for (BlockPos pos : positions) {
            if (MetaMachine.getMachine(getLevel(), pos) instanceof SpaceElevatorModuleMachine module) {
                module.setHost(this);
                modules.add(module);
            }
        }
    }

    private void unbindModules() {
        for (var module : modules) module.setHost(null);
        modules.clear();
    }

    public int getPowerModuleTier() {
        return powerModuleTier;
    }

    public int getSpoolCount() {
        return spoolCount;
    }

    /** Whether the elevator is running above ZPM with all its spools, so its modules may work. */
    public boolean isOperational() {
        return isFormed() && getRecipeLogic().isWorking() && getTier() > GTValues.ZPM && spoolCount >= MAX_SPOOLS;
    }

    /** Takes Nanotube Spools from the input buses until the elevator holds {@link #MAX_SPOOLS}. */
    private void takeSpools() {
        if (spoolCount >= MAX_SPOOLS) return;
        for (var part : getParts()) {
            for (var handlerList : part.getRecipeHandlers()) {
                if (!handlerList.isValid(IO.IN)) continue;
                for (var handler : handlerList.getCapability(ItemRecipeCapability.CAP)) {
                    if (!(handler instanceof com.gregtechceu.gtceu.api.machine.trait.NotifiableItemStackHandler items))
                        continue;
                    for (int slot = 0; slot < items.getSlots() && spoolCount < MAX_SPOOLS; slot++) {
                        ItemStack stack = items.getStackInSlot(slot);
                        if (stack.isEmpty() || !stack.is(GTNAItems.NANOTUBE_SPOOL.get())) continue;
                        int taken = Math.min(stack.getCount(), MAX_SPOOLS - spoolCount);
                        items.extractItemInternal(slot, taken, false);
                        spoolCount += taken;
                    }
                }
            }
        }
    }

    @Nullable
    GTRecipe upkeepRecipe() {
        if (getTier() <= GTValues.ZPM) return null;
        GTRecipe recipe = GTRecipeBuilder.ofRaw().duration(400)
                .CWUt(128 * (getTier() - GTValues.ZPM))
                .EUt(GTValues.VA[getTier()])
                .buildRawRecipe();
        return RecipeHelper.matchContents(this, recipe).isSuccess() ? recipe : null;
    }

    @Override
    protected RecipeLogic createRecipeLogic(Object... args) {
        return new Logic(this);
    }

    @Override
    public void addDisplayText(List<Component> textList) {
        super.addDisplayText(textList);
        if (!isFormed()) return;
        if (spoolCount < MAX_SPOOLS) {
            textList.add(Component.translatable("gtna.machine.space_elevator.spools", spoolCount, MAX_SPOOLS));
        }
        textList.add(Component.translatable("gtna.machine.space_elevator.power_module", powerModuleTier));
        textList.add(Component.translatable("gtna.machine.space_elevator.modules",
                modules.stream().filter(SpaceElevatorModuleMachine::isFormed).count()));
    }

    /** Builds the upkeep cycle instead of looking a recipe up. */
    static final class Logic extends RecipeLogic {

        Logic(SpaceElevatorMachine machine) {
            super(machine);
        }

        private SpaceElevatorMachine elevator() {
            return (SpaceElevatorMachine) machine;
        }

        @Override
        public void findAndHandleRecipe() {
            lastRecipe = null;
            elevator().takeSpools();
            GTRecipe recipe = elevator().upkeepRecipe();
            if (recipe != null) setupRecipe(recipe);
        }

        @Override
        public void onRecipeFinish() {
            machine.afterWorking();
            elevator().takeSpools();
            GTRecipe next = elevator().upkeepRecipe();
            if (next != null) {
                setupRecipe(next);
                return;
            }
            setStatus(Status.IDLE);
            progress = 0;
            duration = 0;
        }
    }
}
