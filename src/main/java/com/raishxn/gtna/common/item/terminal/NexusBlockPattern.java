package com.raishxn.gtna.common.item.terminal;

import com.gregtechceu.gtceu.api.block.MetaMachineBlock;
import com.gregtechceu.gtceu.api.machine.IMachineBlockEntity;
import com.gregtechceu.gtceu.api.machine.MetaMachine;
import com.gregtechceu.gtceu.api.machine.feature.multiblock.IMultiController;
import com.gregtechceu.gtceu.api.machine.feature.multiblock.IMultiPart;
import com.gregtechceu.gtceu.api.machine.multiblock.part.MultiblockPartMachine;
import com.gregtechceu.gtceu.api.pattern.BlockPattern;
import com.gregtechceu.gtceu.api.pattern.MultiblockState;
import com.gregtechceu.gtceu.api.pattern.TraceabilityPredicate;
import com.gregtechceu.gtceu.api.pattern.predicates.SimplePredicate;
import com.gregtechceu.gtceu.api.pattern.util.RelativeDirection;

import com.lowdragmc.lowdraglib.utils.BlockInfo;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.context.BlockPlaceContext;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.minecraft.world.level.block.state.properties.DirectionProperty;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraftforge.common.MinecraftForge;
import net.minecraftforge.common.capabilities.ForgeCapabilities;
import net.minecraftforge.event.level.BlockEvent;
import net.minecraftforge.items.IItemHandler;

import com.raishxn.gtna.api.machine.multiblock.GTNASubPatterns;
import com.raishxn.gtna.api.machine.multiblock.ISubPatternMachine;
import com.raishxn.gtna.common.item.terminal.ui.BlockSelectionConfigWidget;
import com.raishxn.gtna.common.item.terminal.ui.NexusTerminalUIFactory.AutoBuildSetting;
import com.raishxn.gtna.integration.ae2.NexusAE2Link;
import it.unimi.dsi.fastutil.objects.Object2IntOpenHashMap;
import org.jetbrains.annotations.Nullable;

import java.lang.reflect.Field;
import java.util.*;

/**
 * Auto-builder of the Nexus Structure Terminal. It walks a GTCEu {@link BlockPattern} cell by cell and places the
 * blocks the terminal settings ask for: chosen repetitions of stretchable aisles, mirrored build, no-hatch mode,
 * replacement of structural blocks, demolition of cells that must be air, items from an AE2 network, and the first
 * N registered modules (sub-patterns) of the machine.
 * <p>
 * The pattern-to-world transform ({@link #toWorldOffset}), the order in which hatch limits are honoured
 * ({@link #pickCandidates}) and the final facing pass follow GTCEu Modern's own {@code BlockPattern#autoBuild}
 * (LGPL-3.0), so a structure built here is the structure GTCEu checks.
 */
public final class NexusBlockPattern {

    private static final Direction[] FACING_ORDER = { Direction.SOUTH, Direction.NORTH, Direction.WEST,
            Direction.EAST, Direction.UP, Direction.DOWN };

    private final TraceabilityPredicate[][][] cells; // [aisle][row][column]
    private final RelativeDirection[] axes;
    private final int[][] aisleRange;
    private final int[] centerOffset; // x, y, z, minZ, maxZ

    private NexusBlockPattern(TraceabilityPredicate[][][] cells, RelativeDirection[] axes, int[][] aisleRange,
                              int[] centerOffset) {
        this.cells = cells;
        this.axes = axes;
        this.aisleRange = aisleRange;
        this.centerOffset = centerOffset;
    }

    /** Reads a GTCEu pattern; returns null if its layout cannot be read. */
    @Nullable
    public static NexusBlockPattern fromBlockPattern(@Nullable BlockPattern pattern) {
        if (pattern == null) return null;
        try {
            return new NexusBlockPattern(read(pattern, "blockMatches"), pattern.structureDir,
                    pattern.aisleRepetitions, read(pattern, "centerOffset"));
        } catch (ReflectiveOperationException | ClassCastException e) {
            return null;
        }
    }

    @SuppressWarnings("unchecked")
    private static <T> T read(BlockPattern pattern, String name) throws ReflectiveOperationException {
        Field field = BlockPattern.class.getDeclaredField(name);
        field.setAccessible(true);
        return (T) field.get(pattern);
    }

    public void autoBuild(Player player, MultiblockState state, AutoBuildSetting setting, ItemStack terminal) {
        new Build(player, state, setting, terminal).run(this);
        int wanted = setting.getModuleBuild();
        IMultiController controller = state.getController();
        if (wanted <= 0 || controller == null) return;
        List<BlockPattern> modules = new ArrayList<>(GTNASubPatterns.get(controller.self().getDefinition()));
        if (controller.self() instanceof ISubPatternMachine host) modules.addAll(host.gtna$getSubPatterns());
        for (BlockPattern module : modules.subList(0, Math.min(wanted, modules.size()))) {
            NexusBlockPattern sub = fromBlockPattern(module);
            if (sub != null) new Build(player, state, setting, terminal).run(sub);
        }
    }

    /** How many times each aisle is laid: the setting, clamped to the aisle's allowed range. */
    private int[] repetitions(AutoBuildSetting setting) {
        int[] counts = new int[cells.length];
        for (int i = 0; i < cells.length; i++) {
            int min = aisleRange[i][0], max = aisleRange[i][1];
            counts[i] = min == max ? min : Math.max(min, Math.min(max, setting.getRepetitions()));
        }
        return counts;
    }

    /** One auto-build run. Holds the per-run state so the pattern itself stays immutable. */
    private static final class Build {

        private final Player player;
        private final Level level;
        private final MultiblockState state;
        private final AutoBuildSetting setting;
        private final ItemStack terminal;
        private final IMultiController controller;
        private final BlockPos origin;
        private final Direction front;
        private final Direction up;
        private final boolean mirrored;
        /** Every cell the structure owns, with what ended up there (a block state or a machine). */
        private final Map<BlockPos, Object> structure = new HashMap<>();
        private final Set<BlockPos> placed = new HashSet<>();
        private final Map<MetaMachineBlock, Boolean> partBlocks = new HashMap<>();
        /** Candidates of cells without hatch limits never change during a run; huge structures reuse them. */
        private final Map<TraceabilityPredicate, List<ItemStack>> plainCells = new IdentityHashMap<>();

        Build(Player player, MultiblockState state, AutoBuildSetting setting, ItemStack terminal) {
            this.player = player;
            this.level = player.level();
            this.state = state;
            this.setting = setting;
            this.terminal = terminal;
            this.controller = state.getController();
            this.origin = controller.self().getPos();
            this.front = controller.self().getFrontFacing();
            this.up = controller.self().getUpwardsFacing();
            this.mirrored = setting.isMirrorBuild() || controller.self().isFlipped();
        }

        void run(NexusBlockPattern pattern) {
            state.clean();
            structure.put(origin, controller);
            Object2IntOpenHashMap<SimplePredicate> perLayer = state.getLayerCount();
            int[] repeat = pattern.repetitions(setting);
            int z = -pattern.centerOffset[4];
            for (int aisle = 0; aisle < pattern.cells.length; aisle++) {
                for (int copy = 0; copy < repeat[aisle]; copy++, z++) {
                    perLayer.clear();
                    TraceabilityPredicate[][] rows = pattern.cells[aisle];
                    for (int row = 0; row < rows.length; row++) {
                        for (int col = 0; col < rows[row].length; col++) {
                            TraceabilityPredicate cell = rows[row][col];
                            if (cell.common.contains(SimplePredicate.ANY)) continue; // "don't care" space
                            BlockPos pos = origin.offset(pattern.toWorldOffset(col - pattern.centerOffset[0],
                                    row - pattern.centerOffset[1], z, front, up, mirrored));
                            state.update(pos, cell);
                            if (!pos.equals(origin)) fill(pos, cell);
                        }
                    }
                }
            }
            orientPlacedBlocks();
        }

        private void fill(BlockPos pos, TraceabilityPredicate cell) {
            BlockState existing = level.getBlockState(pos);
            if (setting.isDemolitionMode() && mustBeAir(cell)) {
                demolish(pos, existing);
                return;
            }
            boolean replacing = false;
            if (!existing.isAir()) {
                if (!setting.isReplaceMode() || isMachinePartOrController(pos)) {
                    keep(pos, existing, cell);
                    return;
                }
                replacing = true;
            }
            List<ItemStack> wanted = candidates(cell);
            if (replacing && wanted.stream().anyMatch(stack -> stack.is(existing.getBlock().asItem()))) return;
            ItemStack old = replacing ? new ItemStack(existing.getBlock().asItem()) : ItemStack.EMPTY;
            if (replacing && !player.isCreative() && !old.isEmpty() &&
                    player.getInventory().getSlotWithRemainingSpace(old) < 0 &&
                    player.getInventory().getFreeSlot() < 0) {
                return; // nowhere to put the block being replaced
            }
            ItemStack block = takeBlock(wanted);
            if (block == null) return;
            if (replacing) {
                level.removeBlock(pos, true);
                if (!player.isCreative() && !old.isEmpty()) player.getInventory().add(old);
            }
            BlockPlaceContext context = new BlockPlaceContext(level, player, InteractionHand.MAIN_HAND, block,
                    BlockHitResult.miss(player.getEyePosition(0), Direction.UP, pos));
            if (((BlockItem) block.getItem()).place(context).consumesAction()) {
                placed.add(pos);
            } else if (!player.isCreative() && !player.getInventory().add(block)) {
                player.drop(block, false); // the block was already taken from the inventory or the AE2 network
            }
            structure.put(pos, level.getBlockEntity(pos) instanceof IMachineBlockEntity machine ?
                    machine.getMetaMachine() : level.getBlockState(pos));
        }

        private void keep(BlockPos pos, BlockState existing, TraceabilityPredicate cell) {
            structure.put(pos, existing);
            cell.limited.forEach(limit -> limit.testLimited(state));
        }

        private static boolean mustBeAir(TraceabilityPredicate cell) {
            return cell.limited.isEmpty() && cell.common.size() == 1 && cell.common.contains(SimplePredicate.AIR);
        }

        private void demolish(BlockPos pos, BlockState existing) {
            if (existing.isAir() || existing.getDestroySpeed(level, pos) < 0) return;
            if (!level.mayInteract(player, pos) || !player.mayBuild()) return;
            if (MinecraftForge.EVENT_BUS.post(new BlockEvent.BreakEvent(level, pos, existing, player))) return;
            level.destroyBlock(pos, !player.isCreative(), player);
        }

        private boolean isMachinePartOrController(BlockPos pos) {
            MetaMachine machine = MetaMachine.getMachine(level, pos);
            return machine instanceof IMultiPart || machine instanceof IMultiController;
        }

        /** The items that may go in this cell, after hatch limits, no-hatch mode and the terminal's block picks. */
        private List<ItemStack> candidates(TraceabilityPredicate cell) {
            if (cell.limited.isEmpty()) return plainCells.computeIfAbsent(cell, this::resolveCandidates);
            return resolveCandidates(cell);
        }

        private List<ItemStack> resolveCandidates(TraceabilityPredicate cell) {
            List<BlockInfo> options = pickCandidates(cell);
            if (setting.isNoHatchMode()) options.removeIf(this::isPart);
            return BlockSelectionConfigWidget.applySelections(options.toArray(BlockInfo[]::new), terminal);
        }

        /**
         * Same priority as GTCEu: first a limited predicate still below its per-layer minimum, then one below its
         * global minimum, otherwise every limited predicate that has room left plus the common ones.
         */
        private List<BlockInfo> pickCandidates(TraceabilityPredicate cell) {
            Object2IntOpenHashMap<SimplePredicate> perLayer = state.getLayerCount();
            Object2IntOpenHashMap<SimplePredicate> global = state.getGlobalCount();
            for (SimplePredicate limit : cell.limited) {
                if (limit.minLayerCount > 0 && allowed(limit) && below(perLayer, limit, limit.minLayerCount,
                        limit.maxLayerCount)) {
                    perLayer.addTo(limit, 1);
                    return options(limit);
                }
            }
            for (SimplePredicate limit : cell.limited) {
                if (limit.minCount > 0 && allowed(limit) && below(global, limit, limit.minCount, limit.maxCount)) {
                    global.addTo(limit, 1);
                    return options(limit);
                }
            }
            List<BlockInfo> all = new ArrayList<>();
            for (SimplePredicate limit : cell.limited) {
                if (!allowed(limit) || full(perLayer, limit, limit.maxLayerCount) ||
                        full(global, limit, limit.maxCount)) {
                    continue;
                }
                perLayer.addTo(limit, 1);
                global.addTo(limit, 1);
                all.addAll(options(limit));
            }
            for (SimplePredicate common : cell.common) {
                // With several choices, no-hatch mode drops the ones that are only hatches.
                if (cell.common.size() > 1 && !allowed(common)) continue;
                all.addAll(options(common));
            }
            return all;
        }

        private static boolean below(Object2IntOpenHashMap<SimplePredicate> counts, SimplePredicate limit, int min,
                                     int max) {
            int count = counts.getInt(limit);
            return count < min && (max == -1 || count < max);
        }

        private static boolean full(Object2IntOpenHashMap<SimplePredicate> counts, SimplePredicate limit, int max) {
            return max != -1 && counts.containsKey(limit) && counts.getInt(limit) == max;
        }

        private static List<BlockInfo> options(SimplePredicate predicate) {
            BlockInfo[] infos = predicate.candidates == null ? null : predicate.candidates.get();
            return infos == null ? new ArrayList<>() : new ArrayList<>(Arrays.asList(infos));
        }

        /** In no-hatch mode a predicate counts only if it offers at least one block that is not a hatch. */
        private boolean allowed(SimplePredicate predicate) {
            if (!setting.isNoHatchMode()) return true;
            List<BlockInfo> infos = options(predicate);
            return infos.isEmpty() || infos.stream().anyMatch(info -> !isPart(info));
        }

        private boolean isPart(BlockInfo info) {
            return info.getBlockState().getBlock() instanceof MetaMachineBlock block &&
                    partBlocks.computeIfAbsent(block, Build::createsPart);
        }

        private static boolean createsPart(MetaMachineBlock block) {
            try {
                var definition = block.getDefinition();
                var entity = (IMachineBlockEntity) definition.getBlockEntityType().create(BlockPos.ZERO,
                        block.defaultBlockState());
                return definition.createMetaMachine(entity) instanceof MultiblockPartMachine;
            } catch (RuntimeException e) {
                return false;
            }
        }

        /** One block item for the cell: from the AE2 network, then the inventory (and containers in it). */
        @Nullable
        private ItemStack takeBlock(List<ItemStack> wanted) {
            if (player.isCreative()) {
                return wanted.stream().filter(s -> s.getItem() instanceof BlockItem).findFirst().map(ItemStack::copy)
                        .orElse(null);
            }
            if (setting.isUseAE() && NexusAE2Link.isAE2Available()) {
                ItemStack fromNetwork = NexusAE2Link.extractItem(terminal, level, player, wanted);
                if (fromNetwork != null && fromNetwork.getItem() instanceof BlockItem) return fromNetwork;
            }
            IItemHandler inventory = player.getCapability(ForgeCapabilities.ITEM_HANDLER).orElse(null);
            return inventory == null ? null : takeFrom(inventory, wanted, 0);
        }

        @Nullable
        private static ItemStack takeFrom(IItemHandler handler, List<ItemStack> wanted, int depth) {
            for (int slot = 0; slot < handler.getSlots(); slot++) {
                ItemStack stack = handler.getStackInSlot(slot);
                if (stack.isEmpty()) continue;
                if (stack.getItem() instanceof BlockItem &&
                        wanted.stream().anyMatch(w -> ItemStack.isSameItemSameTags(w, stack))) {
                    ItemStack one = handler.extractItem(slot, 1, false);
                    if (!one.isEmpty()) return one;
                }
                IItemHandler inner = depth < 2 ? stack.getCapability(ForgeCapabilities.ITEM_HANDLER).orElse(null) :
                        null;
                if (inner != null) {
                    ItemStack found = takeFrom(inner, wanted, depth + 1);
                    if (found != null) return found;
                }
            }
            return null;
        }

        /** Turns placed blocks and parts towards a side that is not part of the structure, as GTCEu does. */
        private void orientPlacedBlocks() {
            structure.forEach((pos, content) -> {
                if (content instanceof IMultiController) return;
                if (content instanceof MetaMachine machine) {
                    orient(pos, machine.getBlockState(), side -> isOpen(pos, side) && machine.isFacingValid(side));
                } else if (content instanceof BlockState blockState && placed.contains(pos)) {
                    orient(pos, blockState, side -> isOpen(pos, side));
                }
            });
        }

        private boolean isOpen(BlockPos pos, Direction side) {
            Object neighbour = structure.get(pos.relative(side));
            return neighbour == null || neighbour instanceof BlockState s && s.isAir();
        }

        private void orient(BlockPos pos, BlockState blockState, java.util.function.Predicate<Direction> open) {
            DirectionProperty property;
            boolean horizontal;
            if (blockState.hasProperty(BlockStateProperties.FACING)) {
                property = BlockStateProperties.FACING;
                horizontal = false;
            } else if (blockState.hasProperty(BlockStateProperties.HORIZONTAL_FACING)) {
                property = BlockStateProperties.HORIZONTAL_FACING;
                horizontal = true;
            } else {
                return;
            }
            List<Direction> order = new ArrayList<>();
            if (front != null && !(horizontal && front.getAxis() == Direction.Axis.Y)) order.add(front);
            for (Direction side : FACING_ORDER) {
                if (!(horizontal && side.getAxis() == Direction.Axis.Y)) order.add(side);
            }
            Direction chosen = order.stream().filter(open).findFirst().orElse(Direction.NORTH);
            level.setBlock(pos, blockState.setValue(property, chosen), 3);
        }
    }

    /**
     * Pattern coordinates (column, row, aisle) relative to the controller, turned into a world offset for the
     * controller's front/up facing and flip. This is the transform GTCEu's BlockPattern uses (LGPL-3.0), kept
     * identical so built structures always pass GTCEu's own check.
     */
    private BlockPos toWorldOffset(int x, int y, int z, Direction facing, Direction upwardsFacing, boolean flipped) {
        int[] local = { x, y, z };
        int[] world = new int[3];
        boolean vertical = facing == Direction.UP || facing == Direction.DOWN;
        Direction reference = vertical ? (facing == Direction.DOWN ? upwardsFacing : upwardsFacing.getOpposite()) :
                facing;
        for (int i = 0; i < 3; i++) {
            switch (axes[i].getActualDirection(reference)) {
                case UP -> world[1] = local[i];
                case DOWN -> world[1] = -local[i];
                case WEST -> world[0] = -local[i];
                case EAST -> world[0] = local[i];
                case NORTH -> world[2] = -local[i];
                case SOUTH -> world[2] = local[i];
            }
        }
        if (vertical) {
            int sx = upwardsFacing.getStepX(), sz = upwardsFacing.getStepZ();
            if (sx == 0) rotate(world, 2, sz > 0);
            else rotate(world, 0, sx > 0);
            if (flipped) world[upwardsFacing.getAxis() == Direction.Axis.Z ? 0 : 2] *= -1;
        } else {
            if (upwardsFacing.getAxis() == Direction.Axis.X) {
                Direction side = upwardsFacing == Direction.EAST ? facing.getClockWise() :
                        facing.getCounterClockWise();
                if (side.getStepX() == 0) rotate(world, 2, side.getStepZ() < 0);
                else rotate(world, 0, side.getStepX() < 0);
            } else if (upwardsFacing == Direction.SOUTH) {
                world[1] = -world[1];
                world[facing.getStepX() == 0 ? 0 : 2] *= -1;
            }
            if (flipped) {
                if (upwardsFacing.getAxis() == Direction.Axis.Z) {
                    world[facing.getAxis() == Direction.Axis.Z ? 0 : 2] *= -1;
                } else {
                    world[1] = -world[1];
                }
            }
        }
        return new BlockPos(world[0], world[1], world[2]);
    }

    /**
     * Swaps the vertical axis with horizontal axis {@code h}: positive = (h, y) -> (y, -h); otherwise (-y, h).
     */
    private static void rotate(int[] v, int h, boolean positive) {
        int horizontal = v[h];
        v[h] = positive ? v[1] : -v[1];
        v[1] = positive ? -horizontal : horizontal;
    }
}
