package com.raishxn.gtna.common.machine.multiblock.originals;

import com.gregtechceu.gtceu.api.capability.IOpticalComputationProvider;
import com.gregtechceu.gtceu.api.data.chemical.ChemicalHelper;
import com.gregtechceu.gtceu.api.data.chemical.material.Material;
import com.gregtechceu.gtceu.api.data.tag.TagPrefix;
import com.gregtechceu.gtceu.api.machine.IMachineBlockEntity;
import com.gregtechceu.gtceu.common.data.GTMaterials;

import com.lowdragmc.lowdraglib.gui.util.ClickData;
import com.lowdragmc.lowdraglib.gui.widget.ComponentPanelWidget;
import com.lowdragmc.lowdraglib.syncdata.annotation.DescSynced;
import com.lowdragmc.lowdraglib.syncdata.annotation.Persisted;
import com.lowdragmc.lowdraglib.syncdata.field.ManagedFieldHolder;

import net.minecraft.nbt.CompoundTag;
import net.minecraft.nbt.ListTag;
import net.minecraft.nbt.LongArrayTag;
import net.minecraft.nbt.Tag;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.item.ItemStack;

import com.raishxn.gtna.api.machine.feature.lance.LanceCore;
import com.raishxn.gtna.api.machine.feature.lance.LanceCore.Body;
import com.raishxn.gtna.api.machine.feature.lance.LanceCore.Projectile;
import com.raishxn.gtna.common.data.GTNAMaterials;

import java.util.ArrayList;
import java.util.List;

/**
 * Kinetic Orbital Lance (original GTNA, UEV). Charges its capacitor bank from the Nexus network, fires projectiles
 * from the input buses at the selected body and queues return capsules that drop the body's materials.
 * Design: {@code docs/roadmap/design/lanca-cinetica-orbital.md}.
 */
public class LanceMachine extends OriginalMachine {

    protected static final ManagedFieldHolder MANAGED_FIELD_HOLDER = new ManagedFieldHolder(LanceMachine.class,
            OriginalMachine.MANAGED_FIELD_HOLDER);

    /** Muzzle: up and back from the controller (tools/design/convert_originals.py). */
    public static final double MUZZLE_UP = 98, MUZZLE_BACK = 195;
    /** Bank charge rate from the network, EU per second. */
    public static final double CHARGE_PER_SECOND = Math.pow(2, 36) * 20;
    /** CWU/t asked from the optical computation hatch for the aim. */
    public static final int AIM_CWUT = 16000;

    private final LanceCore core = new LanceCore();
    /** Return capsules in flight: {body, kg, seconds left}. */
    private final List<double[]> capsules = new ArrayList<>();

    @Persisted
    @DescSynced
    private int target;
    @Persisted
    private boolean autoFire = true;
    @DescSynced
    private int shotFlash;          // seconds since the last shot, for the renderer
    @DescSynced
    private double syncedYaw;
    @Persisted
    @DescSynced
    private boolean captured;
    @DescSynced
    private int targetableMask;
    /** Bench for the GUI: mass, mass budget, heat, heat budget, inductance; and fitted count per component. */
    @DescSynced
    private double[] syncedBench = new double[5];
    @DescSynced
    private int[] syncedFitted = new int[LanceCore.Component.values().length];
    @DescSynced
    private boolean syncedBenchValid;
    /** CWU/t the computation hatch delivered last second. */
    @DescSynced
    private int cwu;

    public LanceMachine(IMachineBlockEntity holder, Object... args) {
        super(holder, args);
    }

    @Override
    public ManagedFieldHolder getFieldHolder() {
        return MANAGED_FIELD_HOLDER;
    }

    public LanceCore core() {
        return core;
    }

    public int secondsSinceShot() {
        return shotFlash;
    }

    public int computation() {
        return cwu;
    }

    public double yaw() {
        return syncedYaw;
    }

    /** CWU/t from the optical computation hatch; without one the aim is blind. */
    private int requestComputation() {
        for (var part : getParts())
            if (part instanceof IOpticalComputationProvider provider) return provider.requestCWUt(AIM_CWUT, false);
        return 0;
    }

    /** The gun (everything above the turret ring) is in the controller and drawn slewing to the target. */
    public boolean isCaptured() {
        return captured && isFormed();
    }

    private java.util.Map<net.minecraft.core.BlockPos, Character> gun() {
        return CapturedParts.positions(getLevel(), "kinetic_orbital_lance", "gun", getPos(), getFrontFacing(),
                getUpwardsFacing(), isFlipped());
    }

    private void captureGun() {
        if (captured || getLevel() == null) return;
        CapturedParts.capture(getLevel(), gun());
        captured = true;
    }

    private void releaseGun() {
        if (!captured || getLevel() == null || getLevel().isClientSide) return;
        CapturedParts.release(getLevel(), "kinetic_orbital_lance", gun());
        captured = false;
    }

    @Override
    public void onStructureInvalid() {
        releaseGun();
        super.onStructureInvalid();
    }

    @Override
    public void setWorkingEnabled(boolean enabled) {
        super.setWorkingEnabled(enabled);
        if (!enabled) releaseGun();
    }

    private void syncBench() {
        syncedBench = new double[] { core.totalMass(), core.massBudget(), core.totalHeat(), core.heatBudget(),
                core.inductance() };
        int[] fitted = new int[LanceCore.Component.values().length];
        for (var c : core.fitted) fitted[c.ordinal()]++;
        syncedFitted = fitted;
        syncedBenchValid = core.benchValid();
    }

    public double[] bench() {
        return syncedBench;
    }

    public int fitted(LanceCore.Component c) {
        return syncedFitted[c.ordinal()];
    }

    public boolean benchValid() {
        return syncedBenchValid;
    }

    public boolean isTargetable(Body b) {
        return (targetableMask & 1 << b.ordinal()) != 0;
    }

    public Body target() {
        return Body.values()[target];
    }

    @Override
    protected void secondTick(ServerLevel level) {
        shotFlash = Math.min(shotFlash + 1, 99);
        captureGun();
        core.cool(Math.pow(2, 34) * 20);
        double room = core.bankCapacity() - core.bankCharge;
        if (room > 0) {
            double charge = Math.min(room, CHARGE_PER_SECOND);
            if (consume(level, charge)) core.bankCharge += charge;
        }
        cwu = requestComputation();
        Projectile projectile = loadedProjectile();
        if (autoFire && projectile != null && core.bankCharge >= core.bankCapacity() && core.targetable(target())) {
            if (take(s -> projectileOf(s) == projectile, 1) == 1) {
                var shot = core.fire(target(), projectile, cwu);
                if (shot.fired) shotFlash = 0;
                if (shot.recoveredKg > 0) capsules.add(new double[] { target, shot.recoveredKg, shot.returnSeconds });
            }
        }
        var landed = new ArrayList<double[]>();
        for (double[] c : capsules) if (--c[2] <= 0) landed.add(c);
        for (double[] c : landed) {
            capsules.remove(c);
            deliverCapsule(Body.values()[(int) c[0]], c[1]);
        }
        syncedYaw = target * 0.4;
        int mask = 0;
        for (var b : Body.values()) if (core.targetable(b)) mask |= 1 << b.ordinal();
        targetableMask = mask;
        syncBench();
    }

    /** One dust per tonne recovered, split over the body's materials. */
    private void deliverCapsule(Body body, double kg) {
        var materials = materials(body);
        long dusts = (long) Math.max(1, kg / 1000);
        for (var m : materials) {
            var stack = ChemicalHelper.get(TagPrefix.dust, m);
            if (!stack.isEmpty()) output(stack, Math.max(1, dusts / materials.length));
        }
    }

    public static Material[] materials(Body body) {
        return switch (body) {
            case MOON -> new Material[] { GTMaterials.Iron, GTMaterials.Titanium, GTMaterials.Aluminium,
                    GTMaterials.Helium3 };
            case PHOBOS -> new Material[] { GTMaterials.Carbon, GTMaterials.Nickel, GTMaterials.Iron };
            case VESTA -> new Material[] { GTMaterials.Iron, GTMaterials.Magnesium, GTMaterials.Chromium,
                    GTMaterials.Platinum };
            case CERES -> new Material[] { GTMaterials.Magnesium, GTMaterials.Sodium, GTMaterials.Ammonia };
            case PSYCHE -> new Material[] { GTMaterials.Iron, GTMaterials.Nickel, GTMaterials.Iridium,
                    GTMaterials.Osmium, GTMaterials.Gold };
            case EUROPA -> new Material[] { GTMaterials.Magnesium, GTMaterials.Sulfur, GTMaterials.Deuterium };
            case ARROKOTH -> new Material[] { GTMaterials.Nitrogen, GTMaterials.Methane, GTMaterials.Carbon };
            case NEXUS_1 -> new Material[] { GTMaterials.Naquadah, GTMaterials.Neutronium,
                    GTNAMaterials.SpaceTime == null ? GTMaterials.Neutronium : GTNAMaterials.SpaceTime };
        };
    }

    /** Projectile of an input stack: ingots of the projectile material. */
    public static Projectile projectileOf(ItemStack stack) {
        var entry = ChemicalHelper.getMaterialEntry(stack.getItem());
        if (entry.isEmpty() || entry.tagPrefix() != TagPrefix.ingot || entry.material() == null) return null;
        var m = entry.material();
        if (m == GTMaterials.Tungsten) return Projectile.TUNGSTEN;
        if (m == GTMaterials.TungstenCarbide) return Projectile.TUNGSTEN_CARBIDE;
        if (m == GTMaterials.Osmiridium) return Projectile.OSMIRIDIUM;
        if (m == GTMaterials.Neutronium) return Projectile.NEUTRONIUM;
        if (m == GTNAMaterials.WhiteDwarfMatter) return Projectile.DEGENERATE;
        return null;
    }

    private Projectile loadedProjectile() {
        Projectile[] found = { null };
        take(s -> {
            var p = projectileOf(s);
            if (p != null && found[0] == null) found[0] = p;
            return false;
        }, 64);
        return found[0];
    }

    // ------------------------------------------------------------------ GUI

    @Override
    public void addDisplayText(List<Component> text) {
        super.addDisplayText(text);
        if (!isFormed()) return;
        String k = "gtna.machine.kinetic_orbital_lance.";
        var targets = Component.translatable(k + "target");
        for (var b : Body.values()) {
            String c = b.ordinal() == target ? "§b" : core.targetable(b) ? "§7" : "§8";
            targets.append(" ").append(ComponentPanelWidget.withButton(
                    Component.literal(c + "[").append(Component.translatable(k + "body." + b.name().toLowerCase()))
                            .append("]"),
                    "t" + b.ordinal()));
        }
        text.add(targets);
        text.add(Component.translatable(k + "survey", String.format("%.1f", core.survey(target()) * 100)));
        text.add(Component.translatable(k + "bank", String.format("%.2e", core.bankCharge),
                String.format("%.2e", core.bankCapacity())));
        text.add(Component.translatable(k + "barrel", String.format("%.0f", core.barrelTemperature),
                String.format("%.0f", core.linerWear * 100)));
        text.add(Component.translatable(k + "efficiency", String.format("%.2f", core.efficiency()),
                String.format("%.2f", core.accuracy(target(), cwu))));
        text.add(Component.translatable(k + (cwu > 0 ? "computation" : "computation_none"), cwu));
        text.add(Component.translatable(k + "capsules", capsules.size()));
        var bench = Component.translatable(k + "bench");
        for (var c : LanceCore.Component.values()) {
            if (!core.unlocked(c)) continue;
            long n = core.fitted.stream().filter(f -> f == c).count();
            bench.append(" ").append(ComponentPanelWidget.withButton(Component.literal((n > 0 ? "§a" : "§8") +
                    c.name().toLowerCase() + (n > 1 ? "×" + n : "")), "c" + c.ordinal()));
        }
        text.add(bench);
        text.add(Component.translatable(k + (core.benchValid() ? "bench_ok" : "bench_invalid")));
        text.add(ComponentPanelWidget.withButton(Component.translatable(k + (autoFire ? "auto_on" : "auto_off")),
                "auto"));
    }

    @Override
    public void handleDisplayClick(String data, ClickData click) {
        if (click.isRemote || data.isEmpty()) return;
        switch (data.charAt(0)) {
            case 't' -> {
                int t = Integer.parseInt(data.substring(1));
                if (core.targetable(Body.values()[t])) target = t;
            }
            case 'c' -> {
                var c = LanceCore.Component.values()[Integer.parseInt(data.substring(1))];
                // Rails stack up to eight; other slots toggle.
                if (c.slot == LanceCore.Slot.RAIL &&
                        core.fitted.stream().filter(f -> f.slot == LanceCore.Slot.RAIL).count() < 8 &&
                        !click.isShiftClick)
                    core.fitted.add(c);
                else core.fitted.remove(c);
                if (c.slot != LanceCore.Slot.RAIL) core.fitted.removeIf(f -> f.slot == c.slot && f != c);
            }
            case 'a' -> autoFire = !autoFire;
            default -> {}
        }
        syncBench();
    }

    @Override
    public void attachSideTabs(com.gregtechceu.gtceu.api.gui.fancy.TabsWidget sideTabs) {
        super.attachSideTabs(sideTabs);
        OriginalsGui.attach(sideTabs, "orbital_map", OriginalsGui.orbitalMap(this));
        OriginalsGui.attach(sideTabs, "bench", OriginalsGui.bench(this));
    }

    // ------------------------------------------------------------------ persistence

    @Override
    public void saveCustomPersistedData(CompoundTag tag, boolean forDrop) {
        super.saveCustomPersistedData(tag, forDrop);
        tag.put("gtna_lance", new LongArrayTag(bits(core.pack())));
        var list = new ListTag();
        for (double[] c : capsules) list.add(new LongArrayTag(bits(c)));
        tag.put("gtna_lance_capsules", list);
    }

    @Override
    public void loadCustomPersistedData(CompoundTag tag) {
        super.loadCustomPersistedData(tag);
        long[] v = tag.getLongArray("gtna_lance");
        if (v.length > 0) core.unpack(doubles(v));
        capsules.clear();
        for (Tag t : tag.getList("gtna_lance_capsules", Tag.TAG_LONG_ARRAY))
            capsules.add(doubles(((LongArrayTag) t).getAsLongArray()));
    }
}
