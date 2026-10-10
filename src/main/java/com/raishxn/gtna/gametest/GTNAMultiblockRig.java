package com.raishxn.gtna.gametest;

import com.gregtechceu.gtceu.api.GTValues;
import com.gregtechceu.gtceu.api.capability.recipe.FluidRecipeCapability;
import com.gregtechceu.gtceu.api.capability.recipe.IO;
import com.gregtechceu.gtceu.api.capability.recipe.ItemRecipeCapability;
import com.gregtechceu.gtceu.api.machine.IMachineBlockEntity;
import com.gregtechceu.gtceu.api.machine.MachineDefinition;
import com.gregtechceu.gtceu.api.machine.MetaMachine;
import com.gregtechceu.gtceu.api.machine.MultiblockMachineDefinition;
import com.gregtechceu.gtceu.api.machine.feature.IRecipeLogicMachine;
import com.gregtechceu.gtceu.api.machine.feature.multiblock.IMultiController;
import com.gregtechceu.gtceu.api.recipe.GTRecipe;
import com.gregtechceu.gtceu.api.recipe.GTRecipeType;
import com.gregtechceu.gtceu.common.block.CoilBlock;
import com.gregtechceu.gtceu.common.data.GTBlocks;
import com.gregtechceu.gtceu.common.data.GTMachines;
import com.gregtechceu.gtceu.common.data.machines.GCYMMachines;
import com.gregtechceu.gtceu.common.machine.multiblock.part.EnergyHatchPartMachine;
import com.gregtechceu.gtceu.common.machine.multiblock.part.FluidHatchPartMachine;
import com.gregtechceu.gtceu.common.machine.multiblock.part.ItemBusPartMachine;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraftforge.fluids.FluidStack;

import com.raishxn.gtna.common.data.GTNAMachines2;
import com.raishxn.gtna.common.machine.trait.GTNAMultipleRecipesLogic;

import java.util.ArrayList;
import java.util.List;

/**
 * Generic stress rig for multiblock GameTests (G-0208): builds a machine from its own preview, upgrades every preview
 * hatch to {@link #TIER}, swaps every heating coil for Tritanium, optionally turns unused hatches into a Parallel
 * Hatch and a Thread Hatch, then runs a real recipe with as many input sets as the hatches hold and checks the
 * parallel count, the duration and the outputs.
 */
final class GTNAMultiblockRig {

    static final int TIER = GTValues.UV;
    static final int TRITANIUM_COIL_K = 10800;

    final GameTestHelper helper;
    final MultiblockMachineDefinition definition;
    IMultiController controller;
    final List<ItemBusPartMachine> itemIn = new ArrayList<>();
    final List<ItemBusPartMachine> itemOut = new ArrayList<>();
    final List<FluidHatchPartMachine> fluidIn = new ArrayList<>();
    final List<FluidHatchPartMachine> fluidOut = new ArrayList<>();
    final List<EnergyHatchPartMachine> energy = new ArrayList<>();
    final List<BlockPos> fluidInPos = new ArrayList<>();
    final List<BlockPos> fluidOutPos = new ArrayList<>();
    final List<BlockPos> itemInPos = new ArrayList<>();
    final List<BlockPos> itemOutPos = new ArrayList<>();
    final List<BlockPos> allPositions = new ArrayList<>();

    private GTNAMultiblockRig(GameTestHelper helper, MultiblockMachineDefinition definition) {
        this.helper = helper;
        this.definition = definition;
    }

    /** Builds the preview, upgrades hatches to {@link #TIER} and coils to Tritanium. Does not form yet. */
    static GTNAMultiblockRig build(GameTestHelper helper, MultiblockMachineDefinition definition) {
        GTNAMultiblockRig rig = new GTNAMultiblockRig(helper, definition);
        var shape = definition.getMatchingShapes().get(0).getBlocks();
        for (int x = 0; x < shape.length; x++) {
            for (int y = 0; y < shape[x].length; y++) {
                for (int z = 0; z < shape[x][y].length; z++) {
                    var info = shape[x][y][z];
                    BlockPos pos = new BlockPos(x + 1, y + 1, z + 1);
                    if (info == null || info.getBlockState().isAir()) {
                        helper.setBlock(pos, Blocks.AIR);
                        continue;
                    }
                    helper.setBlock(pos, info.getBlockState());
                    rig.allPositions.add(pos);
                }
            }
        }
        for (BlockPos pos : rig.allPositions) {
            Block block = helper.getBlockState(pos).getBlock();
            if (block instanceof CoilBlock) {
                helper.setBlock(pos, GTBlocks.COIL_TRITANIUM.get());
                continue;
            }
            MetaMachine machine = machineAt(helper, pos);
            if (machine instanceof IMultiController multi && block == definition.getBlock()) {
                rig.controller = multi;
            } else if (machine instanceof com.gregtechceu.gtceu.api.machine.feature.multiblock.IMaintenanceMachine &&
                    !(machine instanceof IMultiController)) {
                        // previews pick random maintenance variants; a fresh plain hatch starts with problems: use the
                        // auto one
                        rig.replace(pos, GTMachines.AUTO_MAINTENANCE_HATCH);
                    } else
                if (machine != null && machine.getClass().getSimpleName().contains("WirelessEnergy")) {
                    rig.replace(pos, GTMachines.ENERGY_INPUT_HATCH[TIER]);
                } else if (machine != null && machine.getClass().getSimpleName().startsWith("Huge")) {
                    // Huge buses picked by the preview: standard GTCEu bus, same direction
                    String path = machine.getDefinition().getId().getPath();
                    boolean export = path.contains("export") || path.contains("output");
                    rig.replace(pos, export ? GTMachines.ITEM_EXPORT_BUS[TIER] : GTMachines.ITEM_IMPORT_BUS[TIER]);
                    (export ? rig.itemOutPos : rig.itemInPos).add(pos);
                } else if (machine instanceof ItemBusPartMachine bus) {
                    boolean in = bus.getInventory().getHandlerIO() == IO.IN;
                    rig.replace(pos, in ? GTMachines.ITEM_IMPORT_BUS[TIER] : GTMachines.ITEM_EXPORT_BUS[TIER]);
                    (in ? rig.itemInPos : rig.itemOutPos).add(pos);
                } else if (machine instanceof FluidHatchPartMachine hatch) {
                    boolean in = hatch.tank.getHandlerIO() == IO.IN;
                    rig.replace(pos, in ? GTMachines.FLUID_IMPORT_HATCH[TIER] : GTMachines.FLUID_EXPORT_HATCH[TIER]);
                    (in ? rig.fluidInPos : rig.fluidOutPos).add(pos);
                } else if (machine instanceof EnergyHatchPartMachine) {
                    rig.replace(pos, GTMachines.ENERGY_INPUT_HATCH[TIER]);
                } else if (machine instanceof com.gregtechceu.gtceu.api.capability.IParallelHatch) {
                    rig.replace(pos, GCYMMachines.PARALLEL_HATCH[TIER]);
                    rig.hasParallelHatch = true;
                } else if (machine instanceof com.raishxn.gtna.common.machine.multiblock.part.ThreadPartMachine) {
                    rig.replace(pos, GTNAMachines2.THREAD_HATCHES[TIER]);
                    rig.hasThreadHatch = true;
                }
        }
        return rig;
    }

    private void replace(BlockPos pos, MachineDefinition part) {
        MetaMachine old = machineAt(helper, pos);
        swaps.add((old == null ? "?" : old.getDefinition().getId().getPath()) + "->" + part.getId().getPath());
        Direction facing = old == null ? Direction.NORTH : old.getFrontFacing();
        helper.setBlock(pos, part.getBlock());
        MetaMachine fresh = machineAt(helper, pos);
        if (fresh != null && fresh.isFacingValid(facing)) fresh.setFrontFacing(facing);
    }

    boolean hasParallelHatch;
    boolean hasThreadHatch;
    private final java.util.Set<BlockPos> used = new java.util.HashSet<>();
    private int nextFluidHatch;

    /**
     * Places {@code part} on the first {@code casing} block where the structure still forms (trial and revert), so
     * the rig works whatever the pattern letters are. Returns the position or {@code null}.
     */
    BlockPos placePart(Block casing, MachineDefinition part) {
        for (BlockPos pos : allPositions) {
            if (used.contains(pos) || helper.getBlockState(pos).getBlock() != casing) continue;
            var previous = helper.getBlockState(pos);
            helper.setBlock(pos, part.getBlock());
            if (controller.checkPatternWithLock()) {
                used.add(pos);
                return pos;
            }
            helper.setBlock(pos, previous);
        }
        return null;
    }

    /** Places the IO this recipe needs (+2 item buses each way) plus optional Parallel/Thread hatches. */
    void placeIo(Block casing, int itemIn, int itemOut, int fluidIn, int fluidOut, boolean parallel,
                 boolean thread) {
        helper.assertTrue(controller.checkPatternWithLock(),
                definition.getId() + " preview must form before adding hatches: " +
                        patternError());
        require(casing, GTMachines.ITEM_IMPORT_BUS[TIER], itemIn, itemInPos);
        require(casing, GTMachines.ITEM_EXPORT_BUS[TIER], itemOut, itemOutPos);
        require(casing, GTMachines.FLUID_IMPORT_HATCH[TIER], fluidIn, fluidInPos);
        require(casing, GTMachines.FLUID_EXPORT_HATCH[TIER], fluidOut, fluidOutPos);
        if (parallel && !hasParallelHatch) {
            helper.assertTrue(placePart(casing, GCYMMachines.PARALLEL_HATCH[TIER]) != null,
                    definition.getId() + " must accept a UV Parallel Hatch");
        }
        if (thread && !hasThreadHatch) {
            helper.assertTrue(placePart(casing, GTNAMachines2.THREAD_HATCHES[TIER]) != null,
                    definition.getId() + " must accept a UV Thread Hatch");
        }
    }

    private void require(Block casing, MachineDefinition part, int wanted, List<BlockPos> have) {
        while (have.size() < wanted) {
            BlockPos pos = placePart(casing, part);
            helper.assertTrue(pos != null, definition.getId() + " has no room for another " + part.getId() +
                    " (has " + have.size() + ", wants " + wanted + ")");
            have.add(pos);
        }
    }

    /** Turns the first preview fluid input hatch into a UV Parallel Hatch (max 256). */
    boolean swapFluidInForParallelHatch() {
        if (fluidInPos.isEmpty()) return false;
        replace(fluidInPos.remove(0), GCYMMachines.PARALLEL_HATCH[TIER]);
        return true;
    }

    /** Turns the first preview fluid output hatch into a UV Thread Hatch (+3 threads). */
    boolean swapFluidOutForThreadHatch() {
        if (fluidOutPos.isEmpty()) return false;
        replace(fluidOutPos.remove(0), GTNAMachines2.THREAD_HATCHES[TIER]);
        return true;
    }

    /** Forms the structure and collects the parts. */
    void form() {
        helper.assertTrue(controller != null, definition.getId() + ": the preview has no controller");
        helper.assertTrue(controller.checkPatternWithLock(),
                definition.getId() + " must form with " + GTValues.VN[TIER] + " hatches and Tritanium coils: " +
                        patternError());
        controller.onStructureFormed();
        nextFluidHatch = 0;
        itemIn.clear();
        itemOut.clear();
        fluidIn.clear();
        fluidOut.clear();
        energy.clear();
        for (var part : controller.getParts()) {
            if (part instanceof ItemBusPartMachine bus) {
                (bus.getInventory().getHandlerIO() == IO.IN ? itemIn : itemOut).add(bus);
            } else if (part instanceof FluidHatchPartMachine hatch) {
                (hatch.tank.getHandlerIO() == IO.IN ? fluidIn : fluidOut).add(hatch);
            } else if (part instanceof EnergyHatchPartMachine hatch) {
                energy.add(hatch);
            }
        }
        helper.assertTrue(!energy.isEmpty(), definition.getId() + " formed without an energy hatch");
    }

    String patternError() {
        var error = controller.getMultiblockState().error;
        if (error == null) return "no error";
        var pos = error.getPos();
        String at = pos == null ? "?" : pos + " = " + helper.getLevel().getBlockState(pos).getBlock();
        return error.getErrorInfo().getString() + " at " + at + " swaps=" + swaps;
    }

    final List<String> swaps = new ArrayList<>();

    MetaMachine machine() {
        return (MetaMachine) controller;
    }

    /**
     * First recipe of {@code type} that this rig can feed: no conditions, inputs and outputs fit the available
     * hatches, EU/t affordable for {@code sets} parallels, and the coil temperature (when given) is enough.
     */
    GTRecipe pickRecipe(GTRecipeType type, int sets, int coilTemperature) {
        return pickRecipe(type, sets, coilTemperature, false);
    }

    /** {@code anyHatches}: ignore the hatches present now (the caller places what the recipe needs). */
    GTRecipe pickRecipe(GTRecipeType type, int sets, int coilTemperature, boolean anyHatches) {
        for (GTRecipe recipe : helper.getLevel().getRecipeManager().getAllRecipesFor(type)) {
            if (!recipe.conditions.isEmpty()) continue;
            if (com.gregtechceu.gtceu.api.recipe.RecipeHelper.getRealEUt(recipe).getTotalEU() * sets > GTValues.V[TIER])
                continue;
            int temp = recipe.data.getInt("ebf_temp");
            if (temp > 0 && temp > coilTemperature) continue;
            int itemInputs = recipe.getInputContents(ItemRecipeCapability.CAP).size();
            int fluidInputs = recipe.getInputContents(FluidRecipeCapability.CAP).size();
            int itemOutputs = recipe.getOutputContents(ItemRecipeCapability.CAP).size();
            int fluidOutputs = recipe.getOutputContents(FluidRecipeCapability.CAP).size();
            if (!anyHatches) {
                if (itemInputs > 0 && itemInPos.isEmpty()) continue;
                if (fluidInputs > fluidInPos.size()) continue;
                if (itemOutputs > 0 && itemOutPos.isEmpty()) continue;
                if (fluidOutputs > fluidOutPos.size()) continue;
            } else if (fluidInputs > 3 || fluidOutputs > 4) continue;
            if (itemOutputs > 9) continue;
            if (itemInputs == 0 && fluidInputs == 0) continue;
            if (totalItemsPerSet(recipe) * sets > 2 * 16 * 64 || totalItemsOutPerSet(recipe) * sets > 2 * 16 * 64)
                continue;
            if (!inLookup(recipe)) continue;
            return recipe;
        }
        return null;
    }

    /** Whether GTCEu's recipe lookup returns this recipe from its own inputs (what a real machine search needs). */
    static boolean inLookup(GTRecipe recipe) {
        java.util.Map<com.gregtechceu.gtceu.api.capability.recipe.RecipeCapability<?>, List<Object>> own = new java.util.HashMap<>();
        for (var c : recipe.getInputContents(ItemRecipeCapability.CAP)) {
            var items = ItemRecipeCapability.CAP.of(c.content).getItems();
            if (items.length == 0) return false;
            own.computeIfAbsent(ItemRecipeCapability.CAP, k -> new ArrayList<>()).add(items[0]);
        }
        for (var c : recipe.getInputContents(FluidRecipeCapability.CAP)) {
            var fluids = FluidRecipeCapability.CAP.of(c.content).getStacks();
            if (fluids.length == 0) return false;
            own.computeIfAbsent(FluidRecipeCapability.CAP, k -> new ArrayList<>()).add(fluids[0]);
        }
        if (recipe.recipeType.db().find(own, r -> r.id.equals(recipe.id)) != null) return true;
        // ingredient objects (circuits are special DB nodes, tags expand differently)
        java.util.Map<com.gregtechceu.gtceu.api.capability.recipe.RecipeCapability<?>, List<Object>> raw = new java.util.HashMap<>();
        recipe.inputs.forEach((cap, contents) -> raw.put(cap, contents.stream().map(c -> c.content).toList()));
        return recipe.recipeType.db().find(raw, r -> r.id.equals(recipe.id)) != null;
    }

    static int totalItemsPerSet(GTRecipe recipe) {
        int total = 0;
        for (var content : recipe.getInputContents(ItemRecipeCapability.CAP)) {
            var items = ItemRecipeCapability.CAP.of(content.content).getItems();
            if (items.length > 0 && content.chance > 0) total += items[0].getCount();
        }
        return total;
    }

    static int totalItemsOutPerSet(GTRecipe recipe) {
        int total = 0;
        for (var content : recipe.getOutputContents(ItemRecipeCapability.CAP)) {
            var items = ItemRecipeCapability.CAP.of(content.content).getItems();
            if (items.length > 0) total += items[0].getCount();
        }
        return total;
    }

    /** Puts {@code sets} copies of the recipe's inputs into the buses and hatches (non-consumed inputs once). */
    void feed(GTRecipe recipe, int sets) {
        feed(recipe, sets, 0);
    }

    /** Feeds into input bus {@code busIndex} (its circuit slot gets the recipe's circuit). */
    void feed(GTRecipe recipe, int sets, int busIndex) {
        for (var content : recipe.getInputContents(ItemRecipeCapability.CAP)) {
            var items = ItemRecipeCapability.CAP.of(content.content).getItems();
            if (items.length == 0) continue;
            ItemStack stack = items[0].copy();
            if (com.gregtechceu.gtceu.common.item.IntCircuitBehaviour.isIntegratedCircuit(stack)) {
                // GTCEu 7.5 reads programmed circuits only from the bus circuit slot
                itemIn.get(busIndex).getCircuitInventory().setStackInSlot(0, stack.copy());
                continue;
            }
            int amount = content.chance == 0 ? stack.getCount() : stack.getCount() * sets;
            insert(stack, amount, busIndex);
        }
        for (var content : recipe.getInputContents(FluidRecipeCapability.CAP)) {
            FluidStack[] fluids = FluidRecipeCapability.CAP.of(content.content).getStacks();
            if (fluids.length == 0) continue;
            FluidStack fluid = fluids[0].copy();
            fluid.setAmount(content.chance == 0 ? fluid.getAmount() : fluid.getAmount() * sets);
            fluidIn.get(nextFluidHatch++).tank.setFluidInTank(0, fluid);
        }
    }

    private void insert(ItemStack template, int amount, int firstBus) {
        for (int b = firstBus; b < itemIn.size(); b++) {
            ItemBusPartMachine bus = itemIn.get(b);
            var storage = bus.getInventory().storage;
            for (int slot = 0; slot < storage.getSlots() && amount > 0; slot++) {
                ItemStack chunk = template.copy();
                chunk.setCount(Math.min(amount, template.getMaxStackSize()));
                ItemStack rest = storage.insertItem(slot, chunk, false);
                amount -= chunk.getCount() - rest.getCount();
            }
        }
        helper.assertTrue(amount <= 0, definition.getId() + ": the input buses cannot hold the test inputs");
    }

    /** Ticks with unlimited energy until a recipe starts; returns whether it did. */
    boolean start(int maxTicks) {
        var logic = ((IRecipeLogicMachine) controller).getRecipeLogic();
        logic.updateTickSubscription();
        for (int i = 0; i < maxTicks; i++) {
            charge();
            logic.serverTick();
            peakActive = Math.max(peakActive, activeRecipes());
            if (activeRecipes() > 0) return true;
        }
        return false;
    }

    void tick(int ticks) {
        var logic = ((IRecipeLogicMachine) controller).getRecipeLogic();
        for (int i = 0; i < ticks; i++) {
            charge();
            logic.serverTick();
            peakActive = Math.max(peakActive, activeRecipes());
        }
    }

    /** Fills every energy input container of the machine (energy hatches, laser hatches, ...). */
    private void charge() {
        var holder = (com.gregtechceu.gtceu.api.capability.recipe.IRecipeCapabilityHolder) controller;
        var handlers = holder.getCapabilitiesFlat().getOrDefault(IO.IN, java.util.Map.of())
                .get(com.gregtechceu.gtceu.api.capability.recipe.EURecipeCapability.CAP);
        if (handlers == null) return;
        for (var handler : handlers) {
            if (handler instanceof com.gregtechceu.gtceu.api.capability.IEnergyContainer container) {
                container.changeEnergy(container.getEnergyCapacity() - container.getEnergyStored());
            }
        }
    }

    int peakActive;

    int activeRecipes() {
        var logic = ((IRecipeLogicMachine) controller).getRecipeLogic();
        if (logic instanceof GTNAMultipleRecipesLogic multi) return multi.getActiveRecipeCount();
        return logic.isWorking() ? 1 : 0;
    }

    /** Total parallels across every running recipe. */
    int runningParallels() {
        var logic = ((IRecipeLogicMachine) controller).getRecipeLogic();
        if (logic instanceof GTNAMultipleRecipesLogic multi) {
            return multi.getActiveRecipes().stream().mapToInt(active -> active.recipe.parallels).sum();
        }
        return logic.getLastRecipe() == null ? 0 : logic.getLastRecipe().parallels;
    }

    /** Longest remaining duration among running recipes. */
    int runningDuration() {
        var logic = ((IRecipeLogicMachine) controller).getRecipeLogic();
        if (logic instanceof GTNAMultipleRecipesLogic multi) {
            return multi.getActiveRecipes().stream().mapToInt(active -> active.maxProgress).max().orElse(0);
        }
        return logic.getDuration();
    }

    String status() {
        var logic = ((IRecipeLogicMachine) controller).getRecipeLogic();
        StringBuilder parts = new StringBuilder();
        for (var part : controller.getParts()) parts.append(part.getClass().getSimpleName()).append(',');
        String tier = machine() instanceof com.gregtechceu.gtceu.api.machine.feature.ITieredMachine tiered ?
                GTValues.VN[tiered.getTier()] : "?";
        return "status=" + logic.getStatus() + " failures=" + logic.getFailureReasons() + " tier=" + tier +
                " parts=[" + parts + "] in=" + dumpOut();
    }

    long outputCount(ItemStack stack) {
        long total = 0;
        for (ItemBusPartMachine bus : itemOut) {
            var storage = bus.getInventory().storage;
            for (int slot = 0; slot < storage.getSlots(); slot++) {
                ItemStack inSlot = storage.getStackInSlot(slot);
                if (ItemStack.isSameItemSameTags(inSlot, stack)) total += inSlot.getCount();
            }
        }
        return total;
    }

    String dumpOut() {
        StringBuilder out = new StringBuilder("[");
        for (ItemBusPartMachine bus : itemOut) {
            var storage = bus.getInventory().storage;
            for (int slot = 0; slot < storage.getSlots(); slot++) {
                if (!storage.getStackInSlot(slot).isEmpty()) out.append(storage.getStackInSlot(slot)).append(' ');
            }
        }
        for (ItemBusPartMachine bus : itemIn) {
            var storage = bus.getInventory().storage;
            out.append("| in:");
            for (int slot = 0; slot < storage.getSlots(); slot++) {
                if (!storage.getStackInSlot(slot).isEmpty()) out.append(storage.getStackInSlot(slot)).append(' ');
            }
        }
        return out.append(']').toString();
    }

    long fluidOutputAmount(FluidStack fluid) {
        long total = 0;
        for (FluidHatchPartMachine hatch : fluidOut) {
            for (int tank = 0; tank < hatch.tank.getTanks(); tank++) {
                FluidStack inTank = hatch.tank.getFluidInTank(tank);
                if (inTank.isFluidEqual(fluid)) total += inTank.getAmount();
            }
        }
        return total;
    }

    /**
     * Full stress run: feeds {@code sets} input sets, starts, checks the parallel count equals
     * {@code min(limit, sets)}, finishes the recipe and checks the first guaranteed output scaled by the parallels.
     */
    String diagnose(GTRecipe recipe) {
        var holder = (com.gregtechceu.gtceu.api.capability.recipe.IRecipeCapabilityHolder) controller;
        boolean found = false;
        var it = recipe.recipeType.searchRecipe(holder, r -> true);
        int seen = 0;
        while (it.hasNext() && seen++ < 200) {
            var r = it.next();
            if (r != null && r.id.equals(recipe.id)) found = true;
        }
        var match = com.gregtechceu.gtceu.api.recipe.RecipeHelper.matchContents(holder, recipe);
        StringBuilder inputs = new StringBuilder(" inputs=");
        for (var c : recipe.getInputContents(ItemRecipeCapability.CAP)) {
            var items = ItemRecipeCapability.CAP.of(c.content).getItems();
            inputs.append(items.length > 0 ? items[0] : "?").append("/c").append(c.chance).append(' ')
                    .append(c.content.getClass().getSimpleName()).append(' ');
        }
        for (var c : recipe.getInputContents(FluidRecipeCapability.CAP)) {
            var f = FluidRecipeCapability.CAP.of(c.content).getStacks();
            inputs.append(f.length > 0 ? f[0].getAmount() + "mB " + f[0].getFluid() : "?").append(' ');
        }
        StringBuilder flat = new StringBuilder(" flatIN=");
        holder.getCapabilitiesFlat().getOrDefault(IO.IN, java.util.Map.of()).forEach((cap, handlers) -> {
            flat.append(cap.name).append(':');
            for (var h : handlers) flat.append(h.getContents()).append(';');
        });
        java.util.Map<com.gregtechceu.gtceu.api.capability.recipe.RecipeCapability<?>, List<Object>> own = new java.util.HashMap<>();
        for (var c : recipe.getInputContents(ItemRecipeCapability.CAP))
            own.computeIfAbsent(ItemRecipeCapability.CAP, k -> new ArrayList<>())
                    .add(ItemRecipeCapability.CAP.of(c.content).getItems()[0]);
        for (var c : recipe.getInputContents(FluidRecipeCapability.CAP))
            own.computeIfAbsent(FluidRecipeCapability.CAP, k -> new ArrayList<>())
                    .add(FluidRecipeCapability.CAP.of(c.content).getStacks()[0]);
        var direct = recipe.recipeType.db().find(own, r -> true);
        flat.append(" directDB=").append(direct == null ? "null" : direct.id);
        return inputs.toString() + flat + " search=" + found + "(" + seen + ") match=" + match.isSuccess() + " " +
                match.reason();
    }

    void runAndCheck(GTRecipe recipe, int sets, int limit) {
        feed(recipe, sets);
        helper.assertTrue(start(40), definition.getId() + " must start " + recipe.id + "; " + status() +
                diagnose(recipe));
        int expected = Math.min(limit, sets);
        int parallels = runningParallels();
        helper.assertTrue(parallels == expected, definition.getId() + " running " + recipe.id + " with " + sets +
                " input sets must reach " + expected + " parallels, got " + parallels);
        int duration = runningDuration();
        helper.assertTrue(duration > 0 && duration <= recipe.duration,
                definition.getId() + ": overclocked duration must be in (0, " + recipe.duration + "], got " +
                        duration);
        tick(duration + 5);
        for (var content : recipe.getOutputContents(ItemRecipeCapability.CAP)) {
            if (content.chance < content.maxChance) continue;
            var items = ItemRecipeCapability.CAP.of(content.content).getItems();
            if (items.length == 0) continue;
            long got = outputCount(items[0]);
            long want = (long) items[0].getCount() * parallels;
            helper.assertTrue(got >= want, definition.getId() + " must output " + want + "x " + items[0] +
                    " from " + parallels + " parallels of " + recipe.id + ", found " + got + "; buses=" + dumpOut() +
                    " " + status());
            break;
        }
        for (var content : recipe.getOutputContents(FluidRecipeCapability.CAP)) {
            if (content.chance < content.maxChance) continue;
            FluidStack[] fluids = FluidRecipeCapability.CAP.of(content.content).getStacks();
            if (fluids.length == 0) continue;
            long got = fluidOutputAmount(fluids[0]);
            long want = (long) fluids[0].getAmount() * parallels;
            helper.assertTrue(got >= want, definition.getId() + " must output " + want + " mB " +
                    fluids[0].getDisplayName().getString() + ", found " + got);
            break;
        }
    }

    static MetaMachine machineAt(GameTestHelper helper, BlockPos pos) {
        return helper.getBlockEntity(pos) instanceof IMachineBlockEntity holder ? holder.getMetaMachine() : null;
    }
}
