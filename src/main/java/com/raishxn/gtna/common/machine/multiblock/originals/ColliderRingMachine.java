package com.raishxn.gtna.common.machine.multiblock.originals;

import com.gregtechceu.gtceu.api.data.chemical.material.properties.PropertyKey;
import com.gregtechceu.gtceu.api.fluids.store.FluidStorageKeys;
import com.gregtechceu.gtceu.api.machine.IMachineBlockEntity;
import com.gregtechceu.gtceu.common.data.GTMaterials;

import com.lowdragmc.lowdraglib.gui.util.ClickData;
import com.lowdragmc.lowdraglib.gui.widget.ComponentPanelWidget;
import com.lowdragmc.lowdraglib.syncdata.annotation.DescSynced;
import com.lowdragmc.lowdraglib.syncdata.field.ManagedFieldHolder;

import net.minecraft.nbt.CompoundTag;
import net.minecraft.nbt.LongArrayTag;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.item.ItemStack;

import com.raishxn.gtna.api.machine.feature.collider.ColliderCore;
import com.raishxn.gtna.common.data.GTNAOriginals;

import java.util.List;

/**
 * Antimatter Collider Ring (original GTNA, UIV). Runs {@link ColliderCore} once per second: liquid helium from the
 * fluid hatches cools the magnets, the Nexus network powers magnets and Penning traps, and production runs put
 * contained particles in the output buses. Design: {@code docs/roadmap/design/anel-colisor.md}.
 */
public class ColliderRingMachine extends OriginalMachine {

    protected static final ManagedFieldHolder MANAGED_FIELD_HOLDER = new ManagedFieldHolder(ColliderRingMachine.class,
            OriginalMachine.MANAGED_FIELD_HOLDER);

    /** Ring centre: up and back from the controller (tools/design/convert_originals.py). */
    public static final double CENTER_UP = 0, CENTER_BACK = 64.5, RING_RADIUS = 60;

    private final ColliderCore core = new ColliderCore();
    private final double[] particleBuffer = new double[ColliderCore.Particle.values().length];

    @DescSynced
    private boolean syncedRunning;
    @com.lowdragmc.lowdraglib.syncdata.annotation.Persisted
    @DescSynced
    private boolean captured;
    @DescSynced
    private int syncedMode, syncedMagnet;
    @DescSynced
    private double syncedEnergyTeV, syncedLumi;
    @DescSynced
    private int syncedProposalsDone, syncedProposal = -1;
    @DescSynced
    private double syncedProposalProgress;
    @DescSynced
    private double[] syncedSigma = new double[ColliderCore.Particle.values().length];

    public ColliderRingMachine(IMachineBlockEntity holder, Object... args) {
        super(holder, args);
    }

    @Override
    public ManagedFieldHolder getFieldHolder() {
        return MANAGED_FIELD_HOLDER;
    }

    public ColliderCore core() {
        return core;
    }

    public boolean isBeamOn() {
        return syncedRunning && isFormed() && isWorkingEnabled();
    }

    /** Ring and gyroscope blocks are in the controller and drawn spinning. */
    public boolean isCaptured() {
        return captured && isFormed();
    }

    private java.util.Map<net.minecraft.core.BlockPos, Character> parts(String tag) {
        return CapturedParts.positions(getLevel(), "antimatter_collider_ring", tag, getPos(), getFrontFacing(),
                getUpwardsFacing(), isFlipped());
    }

    private void captureRings() {
        if (captured || getLevel() == null) return;
        // Each removed block would otherwise trigger a full structure check (seconds on a structure this size).
        com.raishxn.gtna.common.item.terminal.NexusBuildCheckGuard.quiet(getMultiblockState(), () -> {
            CapturedParts.capture(getLevel(), parts("ring"));
            CapturedParts.capture(getLevel(), parts("gyro"));
        });
        captured = true;
    }

    private void releaseRings() {
        if (!captured || getLevel() == null || getLevel().isClientSide) return;
        com.raishxn.gtna.common.item.terminal.NexusBuildCheckGuard.quiet(getMultiblockState(), () -> {
            CapturedParts.release(getLevel(), "antimatter_collider_ring", parts("ring"));
            CapturedParts.release(getLevel(), "antimatter_collider_ring", parts("gyro"));
        });
        captured = false;
    }

    @Override
    public void onStructureInvalid() {
        releaseRings();
        super.onStructureInvalid();
    }

    @Override
    public void setWorkingEnabled(boolean enabled) {
        super.setWorkingEnabled(enabled);
        if (!enabled) releaseRings();
    }

    /** Discovery significance of particle {@code i}, synced for the GUI. */
    public double significance(int i) {
        return syncedSigma[i];
    }

    public boolean proposalDone(int i) {
        return (syncedProposalsDone & 1 << i) != 0;
    }

    public int activeProposal() {
        return syncedProposal;
    }

    public double proposalProgress() {
        return syncedProposalProgress;
    }

    public boolean isPhysicsRun() {
        return syncedMode == ColliderCore.Mode.PHYSICS.ordinal();
    }

    public double beamEnergyShare() {
        return syncedEnergyTeV /
                Math.max(1e-9, 0.3 * ColliderCore.MAGNET_FIELD[syncedMagnet] * ColliderCore.RING_RADIUS_M / 1000);
    }

    /** EU/t of the superconducting magnets: 2^(33 + magnet tier). */
    public double magnetUpkeep() {
        return Math.pow(2, 33 + core.magnetTier);
    }

    @Override
    protected void secondTick(ServerLevel level) {
        var helium = GTMaterials.Helium.getProperty(PropertyKey.FLUID).getStorage().get(FluidStorageKeys.LIQUID);
        double demand = core.heliumDemand() * 1000;
        long got = helium == null ? 0 : drain(f -> f.isSame(helium), (long) Math.ceil(demand));
        boolean magnets = consume(level, magnetUpkeep() * 20);
        boolean traps = consume(level, core.trapUpkeepEUt() * 20);
        double share = magnets ? Math.min(1, got / Math.max(1, demand)) : 0;
        // Physics runs need a detector: without one the collisions happen but nothing is recorded.
        boolean blind = core.mode == ColliderCore.Mode.PHYSICS &&
                hatch(OriginalHatchPartMachine.Kind.DETECTOR) == null;
        double[] integrated = blind ? core.integrated.clone() : null;
        double progress = core.proposalProgress;
        var result = core.step(share, traps);
        if (blind) {
            System.arraycopy(integrated, 0, core.integrated, 0, integrated.length);
            if (!result.proposalFinished) core.proposalProgress = progress;
        }
        // Without a Beam Dump the quenched beam hits the ring: twice the recovery time.
        if (result.quench && hatch(OriginalHatchPartMachine.Kind.BEAM_DUMP) == null) core.quenchCooldown *= 2;
        for (var p : ColliderCore.Particle.values()) {
            particleBuffer[p.ordinal()] += result.produced[p.ordinal()];
            long whole = (long) particleBuffer[p.ordinal()];
            if (whole > 0) {
                particleBuffer[p.ordinal()] -= whole - output(new ItemStack(GTNAOriginals.particle(p)), whole);
            }
        }
        // Full traps are emptied into antiproton cells, 1e11 antiprotons each.
        long cells = (long) (core.antiprotons / 1e11);
        if (cells > 0) {
            long left = output(new ItemStack(GTNAOriginals.ANTIPROTON_CELL.get()), cells);
            core.antiprotons -= (cells - left) * 1e11;
        }
        syncedRunning = !result.quench && core.quenchCooldown == 0;
        if (syncedRunning) captureRings();
        syncedMode = core.mode.ordinal();
        syncedMagnet = core.magnetTier;
        syncedEnergyTeV = core.centreOfMassGeV() / 2000;
        syncedLumi = core.luminosity();
        var sigma = new double[syncedSigma.length];
        for (var p : ColliderCore.Particle.values()) sigma[p.ordinal()] = core.significance(p);
        syncedSigma = sigma;
        int done = 0;
        for (int i = 0; i < core.proposalsDone.length; i++) if (core.proposalsDone[i]) done |= 1 << i;
        syncedProposalsDone = done;
        syncedProposal = core.activeProposal == null ? -1 : core.activeProposal.ordinal();
        syncedProposalProgress = core.proposalProgress;
    }

    // ------------------------------------------------------------------ GUI

    @Override
    public void addDisplayText(List<Component> text) {
        super.addDisplayText(text);
        if (!isFormed()) return;
        String k = "gtna.machine.antimatter_collider_ring.";
        text.add(ComponentPanelWidget
                .withButton(Component.translatable(k + (isPhysicsRun() ? "mode_physics" : "mode_production")), "mode"));
        text.add(Component.translatable(k + "magnet", ColliderCore.MAGNET_NAMES[syncedMagnet],
                String.format("%.1f", ColliderCore.MAGNET_FIELD[syncedMagnet])));
        text.add(Component.translatable(k + "energy", String.format("%.2f", syncedEnergyTeV)));
        text.add(Component.translatable(k + "lumi", String.format("%.2e", syncedLumi)));
        text.add(Component.translatable(k + "helium", String.format("%.0f", core.heliumLevel * 100)));
        if (core.quenchCooldown > 0) text.add(Component.translatable(k + "quench", core.quenchCooldown));
        text.add(Component.translatable(k + "traps", String.format("%.2e", core.antiprotons),
                String.format("%.2e", core.trapCapacity())));
        if (core.activeProposal != null)
            text.add(Component.translatable(k + "proposal",
                    Component.translatable(k + "proposal." + core.activeProposal.name().toLowerCase())));
        for (var p : ColliderCore.Particle.values()) {
            double z = core.significance(p);
            String colour = z >= 5 ? "§a" : z >= 3 ? "§e" : "§7";
            text.add(Component.literal(colour + " ▸ ")
                    .append(Component.translatable(k + "particle." + p.name().toLowerCase()))
                    .append(Component.literal(String.format(" %s%.2fσ", colour, z))));
        }
    }

    @Override
    public void handleDisplayClick(String data, ClickData click) {
        if (click.isRemote || !"mode".equals(data)) return;
        core.mode = core.mode == ColliderCore.Mode.PHYSICS ? ColliderCore.Mode.PRODUCTION : ColliderCore.Mode.PHYSICS;
        syncedMode = core.mode.ordinal();
    }

    @Override
    public void attachSideTabs(com.gregtechceu.gtceu.api.gui.fancy.TabsWidget sideTabs) {
        super.attachSideTabs(sideTabs);
        OriginalsGui.attach(sideTabs, "standard_model", OriginalsGui.standardModel(this));
        OriginalsGui.attach(sideTabs, "committee", OriginalsGui.committee(this));
    }

    // ------------------------------------------------------------------ persistence

    @Override
    public void saveCustomPersistedData(CompoundTag tag, boolean forDrop) {
        super.saveCustomPersistedData(tag, forDrop);
        tag.put("gtna_collider", new LongArrayTag(bits(core.pack())));
    }

    @Override
    public void loadCustomPersistedData(CompoundTag tag) {
        super.loadCustomPersistedData(tag);
        long[] v = tag.getLongArray("gtna_collider");
        if (v.length > 0) core.unpack(doubles(v));
    }
}
