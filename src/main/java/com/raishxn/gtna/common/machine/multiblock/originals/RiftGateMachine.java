package com.raishxn.gtna.common.machine.multiblock.originals;

import com.gregtechceu.gtceu.api.data.chemical.ChemicalHelper;
import com.gregtechceu.gtceu.api.data.chemical.material.Material;
import com.gregtechceu.gtceu.api.data.tag.TagPrefix;
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

import com.raishxn.gtna.api.machine.feature.rift.RiftCore;
import com.raishxn.gtna.common.data.GTNAMaterials;
import com.raishxn.gtna.common.data.GTNAOriginals;

import java.util.List;
import java.util.SplittableRandom;

/**
 * Dimensional Rift Gate (original GTNA, UIV). Runs {@link RiftCore} once per second: SpaceTime from the fluid hatches
 * holds the rift stable, probes and depth anchors come from the input buses, and the rift's biome drops its
 * resources in the output buses. Design: {@code docs/roadmap/design/portao-de-fenda.md}.
 */
public class RiftGateMachine extends OriginalMachine {

    protected static final ManagedFieldHolder MANAGED_FIELD_HOLDER = new ManagedFieldHolder(RiftGateMachine.class,
            OriginalMachine.MANAGED_FIELD_HOLDER);

    public static final double CENTER_UP = 60.5, CENTER_BACK = 13.5, INNER_RADIUS = 46;
    /** EU/t of the rift field. */
    public static final double FIELD_EUT = Math.pow(2, 36);

    private final RiftCore core = new RiftCore();
    private final SplittableRandom random = new SplittableRandom();
    private double outputBuffer;

    @DescSynced
    private boolean syncedOpen;
    @DescSynced
    private double syncedStability, syncedResonance;
    @DescSynced
    private int syncedBiome, syncedCollected, syncedScore, syncedAtlasSize;
    /** Atlas entries for the GUI: seed, best depth, best resonance x1000. */
    @DescSynced
    private long[] syncedAtlas = new long[0];

    public RiftGateMachine(IMachineBlockEntity holder, Object... args) {
        super(holder, args);
    }

    @Override
    public ManagedFieldHolder getFieldHolder() {
        return MANAGED_FIELD_HOLDER;
    }

    public RiftCore core() {
        return core;
    }

    public boolean isRiftOpen() {
        return syncedOpen && isFormed() && isWorkingEnabled();
    }

    public double stability() {
        return syncedStability;
    }

    public double resonance() {
        return syncedResonance;
    }

    public boolean harmonicCollected(RiftCore.Harmonic h) {
        return (syncedCollected & 1 << h.ordinal()) != 0;
    }

    public boolean harmonicLoaded(RiftCore.Harmonic h) {
        return (syncedScore & 1 << h.ordinal()) != 0;
    }

    public long[] atlas() {
        return syncedAtlas;
    }

    public int atlasSize() {
        return syncedAtlasSize;
    }

    public RiftCore.Biome biome() {
        return RiftCore.Biome.values()[syncedBiome];
    }

    @Override
    protected void secondTick(ServerLevel level) {
        if (!core.open) {
            sync();
            return;
        }
        if (!consume(level, FIELD_EUT * 20)) {
            core.collapse();
            sync();
            return;
        }
        // A redstone signal on the Tuning Hatch drives the amplitude (0–15 -> 0–100 %).
        var tuning = hatch(OriginalHatchPartMachine.Kind.TUNING);
        if (tuning != null && tuning.signal() > 0) core.amplitude = tuning.signal() * 100.0 / 15;
        if (take(s -> s.is(GTNAOriginals.RIFT_PROBE.get()), 1) > 0) core.probes++;
        if (take(s -> s.is(GTNAOriginals.DEPTH_ANCHOR.get()), 1) > 0) core.deepen();
        var spacetime = GTNAMaterials.SpaceTime;
        long exotic = spacetime == null ? 0 :
                drain(f -> StellarChamberMachine.is(f, spacetime), (long) Math.ceil(core.upkeep() * 1000 + 1000));
        var result = core.step(exotic / 1000.0, random);
        outputBuffer += result.output * 16;
        long whole = (long) outputBuffer;
        if (whole > 0 && result.biome != null) {
            outputBuffer -= whole;
            for (var m : biomeOutputs(result.biome)) output(dust(m), whole);
        }
        if (result.singularity) output(new ItemStack(GTNAOriginals.RIFT_SINGULARITY.get()), 1);
        sync();
    }

    /** What each biome drops (GTCEu / GTNA materials as dusts). */
    public static Material[] biomeOutputs(RiftCore.Biome biome) {
        return switch (biome) {
            case CRYSTAL_PLAINS -> new Material[] { GTMaterials.CertusQuartz, GTMaterials.Silicon,
                    GTMaterials.Titanium };
            case MERCURY_OCEAN -> new Material[] { GTMaterials.Gold, GTMaterials.Thallium, GTMaterials.Cinnabar };
            case FORGE_WORLD -> new Material[] { GTMaterials.Tungsten, GTMaterials.Osmium, GTMaterials.Iridium };
            case SPORE_FOREST -> new Material[] { GTMaterials.Wood, GTMaterials.Carbon, GTMaterials.Phosphorus };
            case ANTIMATTER_ABYSS -> new Material[] { GTMaterials.Naquadah, GTMaterials.NaquadahEnriched };
            case CIVILISATION_RELIC -> new Material[] { GTMaterials.Naquadria, GTMaterials.Trinium,
                    GTMaterials.Duranium };
            case VOID -> new Material[] { GTMaterials.Neutronium,
                    GTNAMaterials.SpaceTime == null ? GTMaterials.Neutronium : GTNAMaterials.SpaceTime };
        };
    }

    private static ItemStack dust(Material m) {
        return m == null ? ItemStack.EMPTY : ChemicalHelper.get(TagPrefix.dust, m);
    }

    private void sync() {
        syncedOpen = core.open;
        syncedStability = core.stability;
        syncedResonance = core.open ? core.resonance() : 0;
        syncedBiome = RiftCore.biome(core.seed).ordinal();
        int collected = 0, score = 0;
        for (var h : RiftCore.Harmonic.values()) {
            if (core.collected[h.ordinal()]) collected |= 1 << h.ordinal();
            if (core.score.contains(h)) score |= 1 << h.ordinal();
        }
        syncedCollected = collected;
        syncedScore = score;
        syncedAtlasSize = core.atlas.size();
        int n = Math.min(64, core.atlas.size());
        long[] atlas = new long[n * 3];
        for (int i = 0; i < n; i++) System.arraycopy(core.atlas.get(core.atlas.size() - n + i), 0, atlas, i * 3, 3);
        syncedAtlas = atlas;
    }

    // ------------------------------------------------------------------ GUI

    @Override
    public void addDisplayText(List<Component> text) {
        super.addDisplayText(text);
        if (!isFormed()) return;
        String k = "gtna.machine.dimensional_rift_gate.";
        if (!core.open) {
            text.add(ComponentPanelWidget.withButton(Component.translatable(k + "open"), "open"));
        } else {
            text.add(Component.translatable(k + "seed", Long.toHexString(core.seed).toUpperCase()));
            text.add(Component.translatable(k + "biome",
                    Component.translatable(k + "biome." + biome().name().toLowerCase())));
            text.add(knob(k + "frequency", String.format("%.1f", core.frequency), "f"));
            text.add(knob(k + "phase", String.format("%.0f", core.phase), "p"));
            text.add(knob(k + "amplitude", String.format("%.0f", core.amplitude), "a"));
            text.add(Component.translatable(k + "resonance", String.format("%.3f", syncedResonance)));
            text.add(Component.translatable(k + "stability", String.format("%.1f", syncedStability)));
            text.add(Component.translatable(k + "depth", core.depth, core.effectiveMaxDepth()));
            text.add(Component.translatable(k + "upkeep", String.format("%.2f", core.upkeep())));
            text.add(ComponentPanelWidget.withButton(Component.translatable(k + "close"), "close"));
        }
        var chord = Component.translatable(k + "score");
        for (var h : RiftCore.Harmonic.values()) {
            if (!core.collected[h.ordinal()]) continue;
            boolean loaded = core.score.contains(h);
            chord.append(" ").append(ComponentPanelWidget.withButton(
                    Component.literal((loaded ? "§b" : "§8") + h.p + ":" + h.q), "h" + h.ordinal()));
        }
        text.add(chord);
        text.add(Component.translatable(k + "atlas", core.atlas.size()));
    }

    private static Component knob(String key, String value, String id) {
        return Component.translatable(key, value).append(" ")
                .append(ComponentPanelWidget.withButton(Component.literal("§c[--]"), id + "--")).append(" ")
                .append(ComponentPanelWidget.withButton(Component.literal("§c[-]"), id + "-")).append(" ")
                .append(ComponentPanelWidget.withButton(Component.literal("§a[+]"), id + "+")).append(" ")
                .append(ComponentPanelWidget.withButton(Component.literal("§a[++]"), id + "++"));
    }

    @Override
    public void handleDisplayClick(String data, ClickData click) {
        if (click.isRemote) return;
        double big = data.endsWith("++") || data.endsWith("--") ? 10 : 1;
        double sign = data.contains("+") ? 1 : -1;
        switch (data.charAt(0)) {
            case 'o' -> {
                if ("open".equals(data)) core.open(random.nextLong());
            }
            case 'c' -> core.collapse();
            case 'f' -> core.frequency = clamp(core.frequency + sign * big, 1, 1000);
            case 'p' -> core.phase = ((core.phase + sign * big) % 360 + 360) % 360;
            case 'a' -> core.amplitude = clamp(core.amplitude + sign * big, 0, 100);
            case 'h' -> {
                var h = RiftCore.Harmonic.values()[Integer.parseInt(data.substring(1))];
                if (!core.score.remove(h) && core.score.size() < 5) core.score.add(h);
            }
            default -> {
                return;
            }
        }
        sync();
    }

    private static double clamp(double v, double lo, double hi) {
        return Math.max(lo, Math.min(hi, v));
    }

    @Override
    public void attachSideTabs(com.gregtechceu.gtceu.api.gui.fancy.TabsWidget sideTabs) {
        super.attachSideTabs(sideTabs);
        OriginalsGui.attach(sideTabs, "seismograph", OriginalsGui.seismograph(this));
        OriginalsGui.attach(sideTabs, "atlas", OriginalsGui.atlas(this));
    }

    // ------------------------------------------------------------------ persistence

    @Override
    public void saveCustomPersistedData(CompoundTag tag, boolean forDrop) {
        super.saveCustomPersistedData(tag, forDrop);
        tag.put("gtna_rift", new LongArrayTag(core.pack()));
    }

    @Override
    public void loadCustomPersistedData(CompoundTag tag) {
        super.loadCustomPersistedData(tag);
        core.unpack(tag.getLongArray("gtna_rift"));
        sync();
    }
}
