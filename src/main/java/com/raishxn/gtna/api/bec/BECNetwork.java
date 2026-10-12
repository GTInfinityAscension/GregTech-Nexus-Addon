package com.raishxn.gtna.api.bec;

import com.gregtechceu.gtceu.api.machine.IMachineBlockEntity;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.material.Fluid;

import java.util.*;

/**
 * The BEC condensate network, after GTNH's {@code BECFactoryGrid}, {@code BECFactoryNetwork} and
 * {@code GraphRouteTracker}. GTNA does not keep a global graph: each node finds the nodes it reaches by walking the
 * world (its hatches, then conduits and the hatches facing them, until another node's hatch), and caches that list
 * until the topology changes ({@link #invalidate()}: a conduit or hatch placed, broken, recoloured or unloaded, a
 * structure formed or broken, a Maxwell Gate starting or stopping). Routing between nodes is a breadth-first search
 * ordered by distance, as in GTNH; a node whose {@link IBECNode#allowsCondensateThrough} refuses a condensate is not
 * stepped into.
 */
public final class BECNetwork {

    public enum Visit {
        CONTINUE,
        SKIP,
        BREAK
    }

    private record Edge(IBECNode node, int distance) {}

    private record Cache(long version, List<Edge> edges, Set<IBECNode> component) {}

    private static long version = 0;
    private static final Map<IBECNode, Cache> CACHE = new WeakHashMap<>();

    private BECNetwork() {}

    public static synchronized void invalidate() {
        version++;
        CACHE.clear();
    }

    public static long version() {
        return version;
    }

    // ---- topology

    private static Cache cache(IBECNode node) {
        Cache cache = CACHE.get(node);
        if (cache == null || cache.version != version) {
            cache = new Cache(version, routedNeighbours(node), component(node));
            CACHE.put(node, cache);
        }
        return cache;
    }

    /** GTNH {@code MTEBECMultiblockBase.getRoutedNeighbours}: nodes reachable from the seeds, with the distance. */
    static List<Edge> routedNeighbours(IBECNode self) {
        List<Edge> out = new ArrayList<>();
        if (!self.isBECFormed()) return out;
        Level level = self.getBECLevel();
        if (level == null) return out;
        Set<Object> visited = new HashSet<>();
        for (IBECHatch seed : self.getRoutedSeeds()) {
            ArrayDeque<Object[]> queue = new ArrayDeque<>();
            queue.add(new Object[] { seed, 0 });
            while (!queue.isEmpty()) {
                Object[] curr = queue.poll();
                Object element = curr[0];
                int dist = (int) curr[1];
                if (!visited.add(element instanceof IBECHatch h ? h.getBECPos() : element)) continue;
                if (element instanceof IBECNode node) {
                    if (node != self) out.add(new Edge(node, dist));
                    continue;
                }
                for (Object next : neighbours(level, element)) queue.add(new Object[] { next, dist + 1 });
            }
        }
        return out;
    }

    /** Every node joined to this one by conduits and hatches, ignoring direction (GTNH network components). */
    static Set<IBECNode> component(IBECNode self) {
        Set<IBECNode> nodes = new LinkedHashSet<>();
        Level level = self.getBECLevel();
        if (level == null || !self.isBECFormed()) return nodes;
        nodes.add(self);
        Set<Object> visited = new HashSet<>();
        ArrayDeque<Object> queue = new ArrayDeque<>(self.getBECHatches());
        while (!queue.isEmpty()) {
            Object element = queue.poll();
            if (element instanceof IBECNode node) {
                if (nodes.add(node)) queue.addAll(node.getBECHatches());
                continue;
            }
            if (!visited.add(element instanceof IBECHatch h ? h.getBECPos() : element)) continue;
            queue.addAll(neighbours(level, element));
        }
        return nodes;
    }

    /** Neighbours of a hatch (its formed controllers and what its front touches) or a conduit position. */
    private static List<Object> neighbours(Level level, Object element) {
        List<Object> out = new ArrayList<>();
        if (element instanceof IBECHatch hatch) {
            for (IBECNode controller : hatch.getBECControllers()) if (controller.isBECFormed()) out.add(controller);
            Direction facing = hatch.getBECFacing();
            BlockPos front = hatch.getBECPos().relative(facing);
            if (!level.isLoaded(front)) return out;
            BlockState state = level.getBlockState(front);
            if (state.getBlock() instanceof IBECConduit) out.add(front.immutable());
            else {
                IBECHatch other = hatchAt(level, front);
                if (other != null && other.getBECFacing() == facing.getOpposite()) out.add(other);
            }
        } else if (element instanceof BlockPos pos) {
            BlockState state = level.getBlockState(pos);
            if (!(state.getBlock() instanceof IBECConduit conduit)) return out;
            int color = conduit.getConduitColor(state);
            for (Direction dir : Direction.values()) {
                BlockPos next = pos.relative(dir);
                if (!level.isLoaded(next)) continue;
                BlockState nextState = level.getBlockState(next);
                if (nextState.getBlock() instanceof IBECConduit other) {
                    if (other.getConduitColor(nextState) == color) out.add(next.immutable());
                    continue;
                }
                IBECHatch hatch = hatchAt(level, next);
                if (hatch != null && hatch.getBECFacing() == dir.getOpposite()) out.add(hatch);
            }
        }
        return out;
    }

    public static IBECHatch hatchAt(Level level, BlockPos pos) {
        return level.getBlockEntity(pos) instanceof IMachineBlockEntity mbe &&
                mbe.getMetaMachine() instanceof IBECHatch hatch ? hatch : null;
    }

    /** True if a conduit at {@code pos} would connect toward {@code dir} (for the conduit model). */
    public static boolean connects(Level level, BlockPos pos, Direction dir, int color) {
        BlockPos next = pos.relative(dir);
        BlockState state = level.getBlockState(next);
        if (state.getBlock() instanceof IBECConduit other) return other.getConduitColor(state) == color;
        IBECHatch hatch = hatchAt(level, next);
        return hatch != null && hatch.getBECFacing() == dir.getOpposite();
    }

    /**
     * Test hook: fixes a node's routed neighbours (each at {@code distance}) and its network component, skipping the
     * world walk, until the next {@link #invalidate()}.
     */
    public static synchronized void putTestEdges(IBECNode node, List<IBECNode> neighbours, int distance,
                                                 Set<IBECNode> component) {
        List<Edge> edges = new ArrayList<>();
        for (IBECNode n : neighbours) edges.add(new Edge(n, distance));
        CACHE.put(node, new Cache(version, edges, component));
    }

    // ---- routing (GraphRouteTracker.iterateNetworkBFS)

    public interface Visitor {

        Visit visit(IBECNode node, int distance);
    }

    public static void iterate(IBECNode start, Visitor visitor) {
        TreeMap<Integer, ArrayDeque<IBECNode>> queue = new TreeMap<>();
        Map<IBECNode, Integer> pending = new HashMap<>();
        Set<IBECNode> visited = new HashSet<>();
        queue.computeIfAbsent(0, k -> new ArrayDeque<>()).add(start);
        while (!queue.isEmpty()) {
            var first = queue.firstEntry();
            IBECNode node = first.getValue().poll();
            int distance = first.getKey();
            if (first.getValue().isEmpty()) queue.remove(distance);
            if (!visited.add(node)) continue;
            Visit result = visitor.visit(node, distance);
            if (result == Visit.BREAK) break;
            if (result == Visit.SKIP) continue;
            for (Edge edge : cache(node).edges) {
                if (visited.contains(edge.node)) continue;
                queue.computeIfAbsent(distance + edge.distance, k -> new ArrayDeque<>()).add(edge.node);
            }
        }
    }

    /** Inventories in the connected network, reachable or not (GTNH {@code getComponents(BECInventory.class)}). */
    public static List<BECInventory> inventories(IBECNode start) {
        List<BECInventory> out = new ArrayList<>();
        for (IBECNode node : cache(start).component) if (node instanceof BECInventory inv) out.add(inv);
        return out;
    }

    public static Set<IBECNode> nodes(IBECNode start) {
        return Collections.unmodifiableSet(cache(start).component);
    }

    // ---- BECFactoryNetwork

    public static void drain(IBECNode drainer, CondensateStack request) {
        iterate(drainer, (node, d) -> {
            if (!node.allowsCondensateThrough(request.fluid)) return Visit.SKIP;
            if (node instanceof BECInventory inv) inv.removeCondensate(request);
            return request.amount > 0 ? Visit.CONTINUE : Visit.BREAK;
        });
    }

    public static void inject(IBECNode start, CondensateStack input) {
        LinkedHashSet<BECInventory> inventories = new LinkedHashSet<>();
        iterate(start, (node, d) -> {
            if (!node.allowsCondensateThrough(input.fluid)) return Visit.SKIP;
            if (node instanceof BECInventory inv) inventories.add(inv);
            return Visit.CONTINUE;
        });
        if (inventories.isEmpty()) return;
        double totalCapacity = 0;
        for (BECInventory inv : inventories) totalCapacity += inv.getCondensateCapacity();
        int remaining = inventories.size();
        for (BECInventory inv : inventories) {
            long split;
            if (remaining == 1) split = input.amount;
            else if (totalCapacity <= 0) split = (long) Math.ceil((double) input.amount / remaining);
            else {
                double weight = inv.getCondensateCapacity() / totalCapacity;
                totalCapacity -= inv.getCondensateCapacity();
                split = (long) Math.ceil(input.amount * weight);
            }
            split = Math.min(split, input.amount);
            remaining--;
            CondensateStack copy = new CondensateStack(input.fluid, split);
            input.amount -= split;
            inv.addCondensate(copy);
            input.amount += copy.amount;
        }
    }

    public static long stored(IBECNode start, Fluid condensate) {
        LinkedHashSet<BECInventory> inventories = new LinkedHashSet<>();
        iterate(start, (node, d) -> {
            if (!node.allowsCondensateThrough(condensate)) return Visit.SKIP;
            if (node instanceof BECInventory inv) inventories.add(inv);
            return Visit.CONTINUE;
        });
        long sum = 0;
        for (BECInventory inv : inventories) sum += inv.getContents().getLong(condensate);
        return sum;
    }

    /** Condensate reachable from {@code start}, per fluid. */
    public static CondensateList stored(IBECNode start) {
        Set<Fluid> contained = new HashSet<>();
        for (BECInventory inv : inventories(start)) contained.addAll(inv.getContents().keySet());
        CondensateList list = new CondensateList();
        for (Fluid condensate : contained) {
            long amount = stored(start, condensate);
            if (amount > 0) list.addTo(condensate, amount);
        }
        return list;
    }

    /** GTNH {@code getSlowdowns}: unrequested condensates reachable from the drainer. */
    public static int slowdowns(IBECNode drainer, Collection<Fluid> valid) {
        Set<Fluid> contained = new HashSet<>();
        for (BECInventory inv : inventories(drainer)) contained.addAll(inv.getContents().keySet());
        valid.forEach(contained::remove);
        if (contained.isEmpty()) return 0;
        int contaminants = 0;
        for (Fluid condensate : contained) {
            boolean[] found = { false };
            iterate(drainer, (node, d) -> {
                if (!node.allowsCondensateThrough(condensate)) return Visit.SKIP;
                if (node instanceof BECInventory inv && inv.getContents().getLong(condensate) > 0) {
                    found[0] = true;
                    return Visit.BREAK;
                }
                return Visit.CONTINUE;
            });
            if (found[0]) contaminants++;
        }
        return contaminants;
    }
}
