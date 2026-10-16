package com.raishxn.gtna.gametest;

import com.gregtechceu.gtceu.api.machine.IMachineBlockEntity;
import com.gregtechceu.gtceu.api.machine.MultiblockMachineDefinition;
import com.gregtechceu.gtceu.api.machine.multiblock.MultiblockControllerMachine;
import com.gregtechceu.gtceu.api.registry.GTRegistries;
import com.gregtechceu.gtceu.common.data.machines.GTMultiMachines;

import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.world.level.block.Blocks;
import net.minecraftforge.gametest.GameTestHolder;
import net.minecraftforge.gametest.PrefixGameTestTemplate;

import com.raishxn.gtna.GTNACORE;
import com.raishxn.gtna.api.capability.WirelessEnergyManager;
import com.raishxn.gtna.api.machine.multiblock.GTNAStructureRefresh;
import com.raishxn.gtna.api.machine.multiblock.IGTNAModuleHost;
import com.raishxn.gtna.common.data.GTNAOriginals;
import com.raishxn.gtna.common.data.NexusEnergyNetwork;
import com.raishxn.gtna.common.machine.multiblock.originals.LanceMachine;
import com.raishxn.gtna.common.machine.multiblock.originals.OriginalMachine;
import com.raishxn.gtna.utils.datastructure.Int128;

import java.math.BigInteger;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

/**
 * Checks for what players have reported or would otherwise have to test by hand: GTNA's global mixins must not stop
 * GTCEu's own multiblocks from forming, an optional GTNA module must not unform its host, and the originals must draw
 * their power from the owner's Nexus network.
 */
@GameTestHolder(GTNACORE.MOD_ID)
@PrefixGameTestTemplate(false)
public class GTNAPlayerFacingGameTests {

    /** Larger previews are covered by their own tests; this sweep keeps to normal-sized machines. */
    private static final int MAX_SIDE = 40;

    private static List<BlockPos> place(GameTestHelper helper, MultiblockMachineDefinition def, BlockPos origin,
                                        MultiblockControllerMachine[] controller) {
        var shape = def.getMatchingShapes().get(0).getBlocks();
        List<BlockPos> placed = new ArrayList<>();
        for (int x = 0; x < shape.length; x++)
            for (int y = 0; y < shape[x].length; y++)
                for (int z = 0; z < shape[x][y].length; z++) {
                    var info = shape[x][y][z];
                    if (info == null || info.getBlockState().isAir()) continue;
                    BlockPos pos = origin.offset(x, y, z);
                    helper.setBlock(pos, info.getBlockState());
                    placed.add(pos);
                    if (info.getBlockState().is(def.getBlock()) &&
                            helper.getBlockEntity(pos) instanceof IMachineBlockEntity be &&
                            be.getMetaMachine() instanceof MultiblockControllerMachine m)
                        controller[0] = m;
                }
        return placed;
    }

    /** Player report (0.5.2 and 0.5.5): "with GTNA, the vanilla multiblocks say the structure is incomplete". */
    @GameTest(template = "empty_16", timeoutTicks = 6000, batch = "gtna_player_facing")
    public static void everyGtceuMultiblockFormsFromItsPreview(GameTestHelper helper) {
        List<String> failures = new ArrayList<>();
        int checked = 0;
        BlockPos origin = new BlockPos(1, 1, 1);
        for (var machine : GTRegistries.MACHINES) {
            if (!(machine instanceof MultiblockMachineDefinition def) ||
                    !"gtceu".equals(def.getId().getNamespace()))
                continue;
            var shapes = def.getMatchingShapes();
            if (shapes.isEmpty()) continue;
            var blocks = shapes.get(0).getBlocks();
            if (blocks.length > MAX_SIDE || blocks[0].length > MAX_SIDE || blocks[0][0].length > MAX_SIDE) continue;
            var controller = new MultiblockControllerMachine[1];
            List<BlockPos> placed;
            try {
                placed = place(helper, def, origin, controller);
            } catch (RuntimeException e) {
                failures.add(def.getId().getPath() + " (preview: " + e + ")");
                continue;
            }
            checked++;
            if (controller[0] == null) failures.add(def.getId().getPath() + " (no controller in preview)");
            else if (!controller[0].checkPatternWithLock()) {
                var error = controller[0].getMultiblockState().error;
                failures.add(def.getId().getPath() + " (" + (error == null ? "?" :
                        error.getErrorInfo().getString() + " at " + error.getPos()) + ")");
            }
            for (BlockPos pos : placed) helper.setBlock(pos, Blocks.AIR);
        }
        GTNACORE.LOGGER.info("[GTNA player-facing] {} GTCEu multiblocks checked, failures: {}", checked, failures);
        helper.assertTrue(checked > 20, "only " + checked + " GTCEu multiblocks were checked");
        helper.assertTrue(failures.isEmpty(), "GTCEu multiblocks that no longer form: " + failures);
        helper.succeed();
    }

    /** The EBF without GTNA's optional heatproof shell is formed, stays formed after a forced check, has 0 modules. */
    @GameTest(template = "empty_16", timeoutTicks = 200, batch = "gtna_player_facing")
    public static void ebfWithoutItsOptionalModuleStaysFormed(GameTestHelper helper) {
        var controller = new MultiblockControllerMachine[1];
        place(helper, GTMultiMachines.ELECTRIC_BLAST_FURNACE, new BlockPos(4, 1, 4), controller);
        var ebf = controller[0];
        helper.assertTrue(ebf != null, "the EBF preview has a controller");
        helper.assertTrue(GTNAStructureRefresh.refresh(ebf, false), "the EBF forms without its module");
        helper.assertTrue(GTNAStructureRefresh.refresh(ebf, true), "a forced check keeps it formed");
        helper.assertTrue(ebf.isFormed(), "the EBF is formed");
        helper.assertTrue(((IGTNAModuleHost) ebf).gtna$formedModuleCount() == 0, "no module is counted");
        helper.assertTrue(!ebf.getParts().isEmpty(), "the EBF keeps its hatches");
        helper.succeed();
    }

    private static UUID owner(GameTestHelper helper, OriginalMachine machine, String eu) throws Exception {
        UUID owner = UUID.randomUUID();
        var f = OriginalMachine.class.getDeclaredField("networkOwner");
        f.setAccessible(true);
        f.set(machine, owner);
        var level = helper.getLevel();
        WirelessEnergyManager.addMaxCapacity(level, owner, Int128.fromString("1000000000000000000000000000"));
        WirelessEnergyManager.setEnergy(level, owner, Int128.fromString(eu));
        return owner;
    }

    private static void seconds(OriginalMachine machine, int n) throws Exception {
        var m = OriginalMachine.class.getDeclaredMethod("secondTick", net.minecraft.server.level.ServerLevel.class);
        m.setAccessible(true);
        for (int i = 0; i < n; i++) m.invoke(machine, machine.getLevel());
    }

    /**
     * Player report: "it does not take energy from the wireless network". Charging the bank must take exactly the
     * charged amount from the owner's network and show up in the Nexus terminal as the lance's direct draw.
     */
    @GameTest(template = "empty_16", timeoutTicks = 2400, batch = "gtna_originals")
    public static void lanceChargesItsBankFromTheNexusNetwork(GameTestHelper helper) throws Exception {
        LanceMachine lance = (LanceMachine) GTNAOriginalsGameTests.build(helper, GTNAOriginals.KINETIC_ORBITAL_LANCE,
                150);
        helper.assertTrue(lance != null && lance.checkPatternWithLock(), "the lance forms");
        var level = helper.getLevel();
        var network = NexusEnergyNetwork.get(level);

        // No owner: nothing is charged.
        lance.core().bankCharge = 0;
        seconds(lance, 1);
        helper.assertTrue(lance.core().bankCharge == 0, "without a network owner the bank stays empty");

        UUID owner = owner(helper, lance, "100000000000000000000000000");
        // GTNAOriginalsGameTests' matrix: the network only transfers with a formed Nexus matrix.
        var matrix = GTNAOriginalsGameTests.class.getDeclaredMethod("matrix", GameTestHelper.class, UUID.class);
        matrix.setAccessible(true);
        matrix.invoke(null, helper, owner);
        BigInteger before = network.getExactEnergy(owner);
        seconds(lance, 3);
        BigInteger taken = before.subtract(network.getExactEnergy(owner));
        BigInteger charged = BigInteger.valueOf((long) lance.core().bankCharge);
        helper.assertTrue(taken.signum() > 0, "the network pays for the bank: taken " + taken);
        helper.assertTrue(taken.subtract(charged).abs().compareTo(BigInteger.valueOf(1000)) < 0,
                "taken " + taken + " equals the bank charge " + charged);
        var debit = network.getLastDirectDebit(owner);
        helper.assertTrue(debit != null && debit.machineType().equals("kinetic_orbital_lance") &&
                debit.source().pos().equals(lance.getPos()),
                "the Nexus terminal sees the lance's draw: " + debit);

        // An empty network: the bank stops charging and nothing goes negative.
        WirelessEnergyManager.setEnergy(level, owner, Int128.ZERO());
        double bank = lance.core().bankCharge;
        seconds(lance, 2);
        helper.assertTrue(lance.core().bankCharge == bank, "an empty network charges nothing");
        helper.assertTrue(network.getExactEnergy(owner).signum() == 0, "the balance never goes negative");
        helper.succeed();
    }
}
