package com.raishxn.gtna.common.block;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.DyeItem;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.context.BlockPlaceContext;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.LevelAccessor;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.BooleanProperty;
import net.minecraft.world.level.block.state.properties.IntegerProperty;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.Shapes;
import net.minecraft.world.phys.shapes.VoxelShape;

import com.raishxn.gtna.api.bec.BECNetwork;
import com.raishxn.gtna.api.bec.IBECConduit;

import java.util.EnumMap;
import java.util.Map;

/**
 * GTNH {@code MTEPipeBEC} ("Bose-Einstein Condensate Conduit") and its full-block casing. A conduit joins conduits of
 * the same colour and BEC Hatches whose front faces it. Right-click with a dye to paint it; with an empty hand while
 * sneaking to clear the paint.
 */
public class BECConduitBlock extends Block implements IBECConduit {

    public static final IntegerProperty COLOR = IntegerProperty.create("color", 0, 16);
    public static final Map<Direction, BooleanProperty> SIDES = new EnumMap<>(Direction.class);

    static {
        for (Direction dir : Direction.values()) SIDES.put(dir, BooleanProperty.create(dir.getName()));
    }

    private final boolean full;
    private final Map<BlockState, VoxelShape> shapes = new java.util.HashMap<>();

    public BECConduitBlock(Properties properties, boolean full) {
        super(properties);
        this.full = full;
        BlockState state = stateDefinition.any().setValue(COLOR, 16);
        for (BooleanProperty side : SIDES.values()) state = state.setValue(side, false);
        registerDefaultState(state);
    }

    public boolean isFull() {
        return full;
    }

    @Override
    protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) {
        builder.add(COLOR);
        SIDES.values().forEach(builder::add);
    }

    @Override
    public int getConduitColor(BlockState state) {
        return state.getValue(COLOR);
    }

    private BlockState withConnections(BlockState state, Level level, BlockPos pos) {
        int color = state.getValue(COLOR);
        for (Direction dir : Direction.values())
            state = state.setValue(SIDES.get(dir), BECNetwork.connects(level, pos, dir, color));
        return state;
    }

    @Override
    public BlockState getStateForPlacement(BlockPlaceContext context) {
        return withConnections(defaultBlockState(), context.getLevel(), context.getClickedPos());
    }

    @Override
    public BlockState updateShape(BlockState state, Direction dir, BlockState neighbor, LevelAccessor level,
                                  BlockPos pos, BlockPos neighborPos) {
        if (level instanceof Level real) {
            BECNetwork.invalidate();
            return state.setValue(SIDES.get(dir), BECNetwork.connects(real, pos, dir, state.getValue(COLOR)));
        }
        return state;
    }

    @Override
    public void neighborChanged(BlockState state, Level level, BlockPos pos, Block block, BlockPos from,
                                boolean moving) {
        super.neighborChanged(state, level, pos, block, from, moving);
        BlockState updated = withConnections(state, level, pos);
        if (updated != state) level.setBlock(pos, updated, Block.UPDATE_CLIENTS);
        BECNetwork.invalidate();
    }

    @Override
    public void onPlace(BlockState state, Level level, BlockPos pos, BlockState old, boolean moving) {
        super.onPlace(state, level, pos, old, moving);
        BECNetwork.invalidate();
    }

    @Override
    public void onRemove(BlockState state, Level level, BlockPos pos, BlockState newState, boolean moving) {
        super.onRemove(state, level, pos, newState, moving);
        BECNetwork.invalidate();
    }

    @Override
    @SuppressWarnings("deprecation")
    public InteractionResult use(BlockState state, Level level, BlockPos pos, Player player, InteractionHand hand,
                                 BlockHitResult hit) {
        ItemStack held = player.getItemInHand(hand);
        int color = -1;
        if (held.getItem() instanceof DyeItem dye) color = dye.getDyeColor().getId();
        else if (held.isEmpty() && player.isShiftKeyDown()) color = 16;
        if (color < 0 || state.getValue(COLOR) == color) return InteractionResult.PASS;
        if (!level.isClientSide) {
            level.setBlock(pos, withConnections(state.setValue(COLOR, color), level, pos), Block.UPDATE_ALL);
            for (Direction dir : Direction.values()) level.neighborChanged(pos.relative(dir), this, pos);
            BECNetwork.invalidate();
        }
        return InteractionResult.sidedSuccess(level.isClientSide);
    }

    @Override
    @SuppressWarnings("deprecation")
    public VoxelShape getShape(BlockState state, BlockGetter level, BlockPos pos, CollisionContext context) {
        if (full) return Shapes.block();
        return shapes.computeIfAbsent(state, s -> {
            VoxelShape shape = Block.box(2, 2, 2, 14, 14, 14);
            for (Direction dir : Direction.values()) {
                if (!s.getValue(SIDES.get(dir))) continue;
                shape = Shapes.or(shape, switch (dir) {
                    case DOWN -> Block.box(2, 0, 2, 14, 2, 14);
                    case UP -> Block.box(2, 14, 2, 14, 16, 14);
                    case NORTH -> Block.box(2, 2, 0, 14, 14, 2);
                    case SOUTH -> Block.box(2, 2, 14, 14, 14, 16);
                    case WEST -> Block.box(0, 2, 2, 2, 14, 14);
                    case EAST -> Block.box(14, 2, 2, 16, 14, 14);
                });
            }
            return shape;
        });
    }
}
