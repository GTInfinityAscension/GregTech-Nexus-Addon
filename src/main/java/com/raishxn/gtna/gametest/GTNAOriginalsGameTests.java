package com.raishxn.gtna.gametest;

import com.gregtechceu.gtceu.api.capability.recipe.FluidRecipeCapability;
import com.gregtechceu.gtceu.api.capability.recipe.IO;
import com.gregtechceu.gtceu.api.machine.IMachineBlockEntity;
import com.gregtechceu.gtceu.api.machine.MultiblockMachineDefinition;
import com.gregtechceu.gtceu.api.machine.multiblock.MultiblockControllerMachine;
import com.gregtechceu.gtceu.api.machine.trait.NotifiableFluidTank;

import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.world.level.block.Blocks;
import net.minecraftforge.gametest.GameTestHolder;

import com.raishxn.gtna.GTNACORE;
import com.raishxn.gtna.api.capability.WirelessEnergyManager;
import com.raishxn.gtna.api.machine.feature.stellar.StellarCore;
import com.raishxn.gtna.common.data.GTNAMaterials;
import com.raishxn.gtna.common.data.GTNAOriginals;
import com.raishxn.gtna.common.machine.multiblock.originals.StellarChamberMachine;
import com.raishxn.gtna.utils.datastructure.Int128;

import java.util.UUID;

/** Original GTNA multiblocks: structures form from their previews and the special mechanics run. */
@GameTestHolder(GTNACORE.MOD_ID)
@net.minecraftforge.gametest.PrefixGameTestTemplate(false)
public final class GTNAOriginalsGameTests {

    private GTNAOriginalsGameTests() {}

    /** Places the first preview of {@code definition} at height {@code dy}; returns the controller. */
    static MultiblockControllerMachine build(GameTestHelper helper, MultiblockMachineDefinition definition, int dy) {
        var shape = definition.getMatchingShapes().get(0).getBlocks();
        MultiblockControllerMachine controller = null;
        for (int x = 0; x < shape.length; x++) {
            for (int y = 0; y < shape[x].length; y++) {
                for (int z = 0; z < shape[x][y].length; z++) {
                    var info = shape[x][y][z];
                    if (info == null || info.getBlockState().isAir()) continue;
                    var pos = new BlockPos(x, y + dy, z);
                    helper.setBlock(pos, Blocks.AIR);
                    helper.setBlock(pos, info.getBlockState());
                    if (info.getBlockState().is(definition.getBlock()))
                        controller = (MultiblockControllerMachine) ((IMachineBlockEntity) helper.getBlockEntity(pos))
                                .getMetaMachine();
                }
            }
        }
        if (controller != null) {
            var c = controller.getPos();
            for (int cx = (c.getX() - 300) >> 4; cx <= (c.getX() + 300) >> 4; cx++)
                for (int cz = (c.getZ() - 300) >> 4; cz <= (c.getZ() + 300) >> 4; cz++)
                    helper.getLevel().getChunk(cx, cz);
        }
        return controller;
    }

    private static void tick(Object machine, String method, int times) throws Exception {
        var m = machine.getClass().getDeclaredMethod(method);
        m.setAccessible(true);
        var ticker = machine.getClass().getDeclaredField("ticker");
        ticker.setAccessible(true);
        for (int i = 0; i < times; i++) {
            ticker.setInt(machine, 19);
            m.invoke(machine);
        }
    }

    @GameTest(template = "empty_16", timeoutTicks = 1200, batch = "gtna_originals")
    public static void stellarChamberFormsLightsAndReleasesTheCore(GameTestHelper helper) throws Exception {
        var machine = (StellarChamberMachine) build(helper, GTNAOriginals.STELLAR_CONTAINMENT_CHAMBER, 150);
        helper.assertTrue(machine != null, "preview must contain the controller");
        long t0 = System.nanoTime();
        boolean formed = machine.checkPatternWithLock();
        long checkMs = (System.nanoTime() - t0) / 1_000_000;
        helper.assertTrue(formed, "the 93^3 sphere must form: " +
                (machine.getMultiblockState().error == null ? null :
                        machine.getMultiblockState().error.getErrorInfo().getString()));
        GTNACORE.LOGGER.info("[GTNA perf] stellar_containment_chamber pattern check: {} ms", checkMs);
        machine.onStructureFormed();

        UUID owner = UUID.randomUUID();
        var field = StellarChamberMachine.class.getDeclaredField("networkOwner");
        field.setAccessible(true);
        field.set(machine, owner);
        WirelessEnergyManager.addMaxCapacity(helper.getLevel(), owner,
                Int128.fromString("1000000000000000000000000000"));
        matrix(helper, owner);
        WirelessEnergyManager.setEnergy(helper.getLevel(), owner, Int128.fromString("1000000000000000000000000"));
        var before = WirelessEnergyManager.getEnergy(helper.getLevel(), owner).toBigInteger();

        tick(machine, "stellarTick", 1);
        BlockPos center = machine.center();
        helper.assertTrue(helper.getLevel().getBlockState(center).isAir(), "lighting the star takes the core away");
        helper.assertTrue(machine.isStarLit(), "the star is lit");

        // Feed molten star matter: the star gains mass and spins up.
        double m0 = machine.core().mass, p0 = machine.core().period;
        if (GTNAMaterials.MagnetohydrodynamicallyConstrainedStarMatter != null)
            fill(machine, GTNAMaterials.MagnetohydrodynamicallyConstrainedStarMatter.getFluid(16_000));
        tick(machine, "stellarTick", 1);
        helper.assertTrue(machine.core().mass > m0 && machine.core().period < p0,
                "feeding raises mass and spins up: " + machine.core().mass + " " + machine.core().period + " " +
                        probe(helper, machine, owner));

        long s0 = System.nanoTime();
        tick(machine, "stellarTick", 200);
        long stepUs = (System.nanoTime() - s0) / 1000 / 200;
        GTNACORE.LOGGER.info("[GTNA perf] stellar_containment_chamber second: {} us", stepUs);
        helper.assertTrue(!WirelessEnergyManager.getEnergy(helper.getLevel(), owner).toBigInteger().equals(before),
                "the network balance changes (upkeep and extraction)");
        helper.assertTrue(machine.core().mode == StellarCore.Mode.NEUTRON_STAR, "still a neutron star");

        machine.setWorkingEnabled(false);
        helper.assertTrue(helper.getLevel().getBlockState(center).is(GTNAOriginals.DEGENERATE_MATTER_CORE.get()),
                "switching off puts the core back");
        helper.assertTrue(machine.checkPatternWithLock(), "the full structure forms again");

        // Breaking a casing while the star burns (the author's Seismic Probe swap) used to recurse: every core block
        // put back re-checked the sphere and released again. It must invalidate once and give the core back.
        machine.setWorkingEnabled(true);
        tick(machine, "stellarTick", 1);
        helper.assertTrue(machine.isStarLit(), "lit again before the break");
        BlockPos casing = null;
        for (BlockPos p : machine.getMultiblockState().getCache()) {
            if (!p.equals(machine.getPos()) && helper.getLevel().getBlockEntity(p) == null &&
                    !helper.getLevel().getBlockState(p).isAir()) {
                casing = p;
                break;
            }
        }
        helper.assertTrue(casing != null, "a structure block to break");
        // Formed by hand above, so register the block-change mapping GTCEu adds when a structure forms in play.
        com.gregtechceu.gtceu.api.pattern.MultiblockWorldSavedData.getOrCreate(helper.getLevel())
                .addMapping(machine.getMultiblockState());
        long b0 = System.nanoTime();
        helper.getLevel().destroyBlock(casing, false);
        long breakMs = (System.nanoTime() - b0) / 1_000_000;
        GTNACORE.LOGGER.info("[GTNA perf] stellar_containment_chamber casing broken while lit: {} ms", breakMs);
        helper.assertTrue(!machine.isFormed(), "breaking a casing invalidates the chamber");
        helper.assertTrue(helper.getLevel().getBlockState(center).is(GTNAOriginals.DEGENERATE_MATTER_CORE.get()),
                "breaking a casing puts the core back");
        helper.assertTrue(breakMs < 10_000, "breaking a casing must not freeze the server: " + breakMs + " ms");
        helper.succeed();
    }

    @GameTest(template = "empty_16", timeoutTicks = 100, batch = "gtna_originals")
    public static void stellarChamberPatternHasTheCore(GameTestHelper helper) {
        var aisles = com.raishxn.gtna.common.data.multiblock.GTNAMultiBlockFileReader
                .loadAisles("stellar_containment_chamber");
        int core = 0, controllers = 0;
        for (String[] aisle : aisles) for (String row : aisle) for (char c : row.toCharArray()) {
            if (c == 'D') core++;
            if (c == '~') controllers++;
        }
        helper.assertTrue(aisles.length == 93 && controllers == 1, "93 aisles and one controller");
        helper.assertTrue(core == 1419, "core sphere of radius 7: " + core);
        helper.succeed();
    }

    // ------------------------------------------------------------------ shared for the OriginalMachine subclasses

    private static void seconds(com.raishxn.gtna.common.machine.multiblock.originals.OriginalMachine machine, int n)
                                                                                                                     throws Exception {
        var m = com.raishxn.gtna.common.machine.multiblock.originals.OriginalMachine.class.getDeclaredMethod(
                "secondTick",
                net.minecraft.server.level.ServerLevel.class);
        m.setAccessible(true);
        for (int i = 0; i < n; i++) m.invoke(machine, machine.getLevel());
    }

    private static UUID power(GameTestHelper helper,
                              com.raishxn.gtna.common.machine.multiblock.originals.OriginalMachine machine)
                                                                                                            throws Exception {
        UUID owner = UUID.randomUUID();
        var f = com.raishxn.gtna.common.machine.multiblock.originals.OriginalMachine.class
                .getDeclaredField("networkOwner");
        f.setAccessible(true);
        f.set(machine, owner);
        WirelessEnergyManager.addMaxCapacity(helper.getLevel(), owner,
                Int128.fromString("1000000000000000000000000000"));
        matrix(helper, owner);
        WirelessEnergyManager.setEnergy(helper.getLevel(), owner, Int128.fromString("100000000000000000000000000"));
        return owner;
    }

    private static <M extends MultiblockControllerMachine> M formed(GameTestHelper helper,
                                                                    MultiblockMachineDefinition d,
                                                                    String name) {
        @SuppressWarnings("unchecked")
        M machine = (M) build(helper, d, 150);
        helper.assertTrue(machine != null, name + ": preview must contain the controller");
        long t0 = System.nanoTime();
        boolean ok = machine.checkPatternWithLock();
        GTNACORE.LOGGER.info("[GTNA perf] {} pattern check: {} ms", name, (System.nanoTime() - t0) / 1_000_000);
        helper.assertTrue(ok, name + " must form: " + (machine.getMultiblockState().error == null ? null :
                machine.getMultiblockState().error.getErrorInfo().getString() + " at " +
                        machine.getMultiblockState().error.getPos()));
        machine.onStructureFormed();
        return machine;
    }

    private static void fill(MultiblockControllerMachine machine, net.minecraftforge.fluids.FluidStack fluid) {
        var seen = new StringBuilder();
        for (var part : machine.getParts()) {
            seen.append(part.getClass().getSimpleName()).append(' ');
            for (var handlers : part.getRecipeHandlers()) {
                seen.append(handlers.getHandlerIO()).append(' ');
                if (handlers.isValid(IO.IN))
                    for (var h : handlers.getCapability(FluidRecipeCapability.CAP))
                        if (h instanceof NotifiableFluidTank tank) {
                            tank.setFluidInTank(0, fluid.copy());
                            GTNACORE.LOGGER.info("[GTNA test] filled {} -> {}", fluid.getAmount(),
                                    tank.getFluidInTank(0).getAmount());
                            return;
                        }
            }
        }
        throw new AssertionError("no fluid input hatch among parts: " + seen);
    }

    private static void give(MultiblockControllerMachine machine, net.minecraft.world.item.ItemStack stack) {
        for (var part : machine.getParts())
            for (var handlers : part.getRecipeHandlers())
                if (handlers.isValid(IO.IN))
                    for (var h : handlers
                            .getCapability(com.gregtechceu.gtceu.api.capability.recipe.ItemRecipeCapability.CAP))
                        if (h instanceof com.gregtechceu.gtceu.api.machine.trait.NotifiableItemStackHandler items) {
                            items.storage.setStackInSlot(0, stack.copy());
                            return;
                        }
    }

    /** A formed Nexus Flux Matrix in this dimension, as a player's network has. */
    private static void matrix(GameTestHelper helper, UUID owner) {
        var network = com.raishxn.gtna.common.data.NexusEnergyNetwork.get(helper.getLevel());
        network.setMatrixStats(owner, 750, 14, 1.0, Int128.fromString("100000000000000000000000000000"), true);
        network.setMatrixDimension(owner, helper.getLevel().dimension());
    }

    /** Fluid amounts in the input hatches, the owner's balance and a direct consume probe, for failure messages. */
    private static String probe(GameTestHelper helper, MultiblockControllerMachine machine, UUID owner) {
        var sb = new StringBuilder("tanks=");
        for (var part : machine.getParts())
            for (var handlers : part.getRecipeHandlers())
                if (handlers.isValid(IO.IN))
                    for (var h : handlers.getCapability(FluidRecipeCapability.CAP))
                        if (h instanceof NotifiableFluidTank tank)
                            for (int i = 0; i < tank.getTanks(); i++)
                                sb.append(tank.getFluidInTank(i).getFluid()).append(':')
                                        .append(tank.getFluidInTank(i).getAmount()).append(' ');
        sb.append(" balance=").append(WirelessEnergyManager.getEnergy(helper.getLevel(), owner));
        sb.append(" cap=").append(WirelessEnergyManager.getMaxCapacity(helper.getLevel(), owner));
        sb.append(" consume1=").append(WirelessEnergyManager.consumeEnergy(helper.getLevel(), owner, new Int128(1)));
        return sb.toString();
    }

    private static long outputs(MultiblockControllerMachine machine) {
        long n = 0;
        for (var part : machine.getParts())
            for (var handlers : part.getRecipeHandlers())
                if (handlers.isValid(IO.OUT))
                    for (var h : handlers
                            .getCapability(com.gregtechceu.gtceu.api.capability.recipe.ItemRecipeCapability.CAP))
                        if (h instanceof com.gregtechceu.gtceu.api.machine.trait.NotifiableItemStackHandler items)
                            for (int i = 0; i < items.storage.getSlots(); i++)
                                n += items.storage.getStackInSlot(i).getCount();
        return n;
    }

    @GameTest(template = "empty_16", timeoutTicks = 1200, batch = "gtna_originals")
    public static void colliderFormsCoolsAndCollides(GameTestHelper helper) throws Exception {
        com.raishxn.gtna.common.machine.multiblock.originals.ColliderRingMachine ring = formed(helper,
                GTNAOriginals.ANTIMATTER_COLLIDER_RING, "antimatter_collider_ring");
        UUID owner = power(helper, ring);
        var helium = com.gregtechceu.gtceu.common.data.GTMaterials.Helium.getFluid(
                com.gregtechceu.gtceu.api.fluids.store.FluidStorageKeys.LIQUID, 64_000);
        fill(ring, helium);
        // The first second captures the ring and gyroscopes (two pattern walks); time it apart from the steady state.
        long t0 = System.nanoTime();
        seconds(ring, 1);
        GTNACORE.LOGGER.info("[GTNA perf] antimatter_collider_ring capture: {} ms",
                (System.nanoTime() - t0) / 1_000_000);
        t0 = System.nanoTime();
        seconds(ring, 29);
        GTNACORE.LOGGER.info("[GTNA perf] antimatter_collider_ring second: {} us",
                (System.nanoTime() - t0) / 1000 / 29);
        helper.assertTrue(ring.core().quenchCooldown == 0 && ring.core().rampSeconds > 0,
                "helium keeps the beam on: helium=" + ring.core().heliumLevel + " quench=" +
                        ring.core().quenchCooldown + " " + probe(helper, ring, owner));
        helper.assertTrue(ring.core().antiprotons > 0 || outputs(ring) > 0, "production run makes particles");
        helper.assertTrue(ring.hatch(
                com.raishxn.gtna.common.machine.multiblock.originals.OriginalHatchPartMachine.Kind.BEAM_DUMP) != null,
                "the preview places a Beam Dump");
        helper.assertTrue(ring.hatch(
                com.raishxn.gtna.common.machine.multiblock.originals.OriginalHatchPartMachine.Kind.DETECTOR) != null,
                "the preview places a Collision Detector Hatch");
        ring.core().mode = com.raishxn.gtna.api.machine.feature.collider.ColliderCore.Mode.PHYSICS;
        fill(ring, helium);
        seconds(ring, 10);
        helper.assertTrue(ring.core().integrated[0] > 0, "physics run integrates luminosity");
        helper.succeed();
    }

    @GameTest(template = "empty_16", timeoutTicks = 1200, batch = "gtna_originals")
    public static void riftGateFormsTunesAndHolds(GameTestHelper helper) throws Exception {
        com.raishxn.gtna.common.machine.multiblock.originals.RiftGateMachine gate = formed(helper,
                GTNAOriginals.DIMENSIONAL_RIFT_GATE, "dimensional_rift_gate");
        UUID owner = power(helper, gate);
        var core = gate.core();
        core.open(12345);
        double[] o = com.raishxn.gtna.api.machine.feature.rift.RiftCore.optimum(12345);
        core.frequency = o[0];
        core.phase = o[1];
        core.amplitude = o[2];
        if (GTNAMaterials.SpaceTime != null) fill(gate, GTNAMaterials.SpaceTime.getFluid(64_000));
        seconds(gate, 20);
        helper.assertTrue(core.open && core.stability > 0,
                "a tuned rift with SpaceTime stays open: " + core.stability + " " + probe(helper, gate, owner));
        helper.assertTrue(!core.atlas.isEmpty(), "the seed is recorded in the atlas");
        helper.succeed();
    }

    @GameTest(template = "empty_16", timeoutTicks = 2400, batch = "gtna_originals")
    public static void lanceFormsFiresAndReturnsCapsules(GameTestHelper helper) throws Exception {
        com.raishxn.gtna.common.machine.multiblock.originals.LanceMachine lance = formed(helper,
                GTNAOriginals.KINETIC_ORBITAL_LANCE, "kinetic_orbital_lance");
        // The incremental checks rely on the layout covering exactly what GTCEu's walk visits.
        var layout = lance.structureWatch().layout().positionSet();
        var walked = lance.getMultiblockState().cache;
        helper.assertTrue(layout.size() > 100_000 && layout.containsAll(walked),
                "layout " + layout.size() + " covers the walked " + walked.size());
        power(helper, lance);
        var core = lance.core();
        core.bankCharge = core.bankCapacity();
        give(lance, com.gregtechceu.gtceu.api.data.chemical.ChemicalHelper.get(
                com.gregtechceu.gtceu.api.data.tag.TagPrefix.ingot,
                com.gregtechceu.gtceu.common.data.GTMaterials.NaquadahAlloy, 4));
        seconds(lance, 1);
        helper.assertTrue(lance.secondsSinceShot() == 0, "a full bank with a naquadah alloy slug fires");
        helper.assertTrue(core.recovered[0] > 0, "the Moon shot recovers mass");
        seconds(lance, 45);
        helper.assertTrue(outputs(lance) > 0, "the capsule returns with lunar material");

        // A worn liner is swapped from the Barrel Liner Hatch.
        var liners = lance
                .hatch(com.raishxn.gtna.common.machine.multiblock.originals.OriginalHatchPartMachine.Kind.LINER);
        helper.assertTrue(liners != null, "the preview places a Barrel Liner Hatch");
        var liner = com.gregtechceu.gtceu.api.data.chemical.ChemicalHelper.get(
                com.gregtechceu.gtceu.api.data.tag.TagPrefix.plate,
                com.gregtechceu.gtceu.common.data.GTMaterials.Neutronium, 1);
        helper.assertTrue(!liner.isEmpty() && liners.insert(liner.copy()).isEmpty(),
                "the hatch accepts a neutronium liner: " + liner);
        core.linerWear = 1;
        seconds(lance, 1);
        // A Target Cartridge picks the next target.
        var carts = lance.hatch(
                com.raishxn.gtna.common.machine.multiblock.originals.OriginalHatchPartMachine.Kind.TARGET_CARTRIDGE);
        helper.assertTrue(carts != null, "the preview places a Target Cartridge Hatch");
        carts.insert(new net.minecraft.world.item.ItemStack(GTNAOriginals.cartridge(
                com.raishxn.gtna.api.machine.feature.lance.LanceCore.Body.MOON)));
        helper.assertTrue(core.linerWear < 1 && core.linerLife == 2e14,
                "the neutronium liner replaces the worn one: wear=" + core.linerWear + " life=" + core.linerLife);
        helper.succeed();
    }
}
