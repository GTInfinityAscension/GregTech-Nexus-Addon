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
import com.raishxn.gtna.common.data.material.OriginalsMaterials;

import java.util.ArrayList;
import java.util.List;

/**
 * Kinetic Orbital Lance (original GTNA, UEV). Charges its capacitor bank from the Nexus network, fires projectiles
 * from the input buses at the selected body and queues return capsules that drop the body's materials.
 * Design: {@code docs/roadmap/design/lanca-cinetica-orbital.md}.
 */
public class LanceMachine extends OriginalMachine
                          implements com.gregtechceu.gtceu.api.machine.feature.IMachineLife {

    protected static final ManagedFieldHolder MANAGED_FIELD_HOLDER = new ManagedFieldHolder(LanceMachine.class,
            OriginalMachine.MANAGED_FIELD_HOLDER);

    /** Muzzle: up and back from the controller (tools/design/convert_originals.py). */
    public static final double MUZZLE_UP = 98, MUZZLE_BACK = 195;
    /** Bank charge rate from the network, EU per second. */
    public static final double CHARGE_PER_SECOND = Math.pow(2, 36) * 20;
    // EN: CWU/t asked from the optical computation hatch for the aim. At UEV a Supercomputing Center network gives far
    // more than 16 000; up to 2^20 the aim keeps improving (error ∝ 1/sqrt(CWU)), so far bodies reward big networks.
    // PT: CWU/t pedidos ao hatch de computação para a mira. No UEV uma rede de Supercomputing Center dá muito mais que
    // 16 000; até 2^20 a mira continua melhorando (erro ∝ 1/sqrt(CWU)), então corpos distantes premiam redes grandes.
    // ZH: 向光学计算仓请求的瞄准算力（CWU/t）。在 UEV 阶段超级计算中心网络远超 16 000；到 2^20 为止瞄准持续改善
    // （误差 ∝ 1/sqrt(CWU)），因此远处天体奖励大型网络。
    public static final int AIM_CWUT = 1 << 20;

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
    /** Whether a computation hatch is in the structure (it may still deliver nothing: no network behind it). */
    @DescSynced
    private boolean computationHatch;

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

    /** A worn or cracked liner is swapped from the Barrel Liner Hatch without taking the gun apart. */
    private void replaceWornLiner() {
        if (core.linerWear < 1) return;
        var hatch = hatch(OriginalHatchPartMachine.Kind.LINER);
        if (hatch == null) return;
        var liner = hatch.takeOne();
        if (!liner.isEmpty()) core.replaceLiner(linerLife(liner));
    }

    /** Liner life in EU: naquadah alloy 5e13, neutronium 2e14; 0 if not a liner. UEV inputs, not EV ones. */
    public static double linerLife(ItemStack stack) {
        var entry = ChemicalHelper.getMaterialEntry(stack.getItem());
        if (entry.isEmpty() || entry.tagPrefix() != TagPrefix.plateDense && entry.tagPrefix() != TagPrefix.plate)
            return 0;
        if (entry.material() == GTMaterials.NaquadahAlloy) return 5e13;
        if (entry.material() == GTMaterials.Neutronium) return 2e14;
        return 0;
    }

    /** CWU/t from the optical computation hatch; without one the aim is blind. */
    private int requestComputation() {
        // The Computation Data Reception Hatch exposes its provider as a trait/capability, not as the part itself.
        for (var part : getParts()) {
            var provider = computationProvider(part);
            if (provider == null) continue;
            computationHatch = true;
            return provider.requestCWUt(AIM_CWUT, false);
        }
        computationHatch = false;
        return 0;
    }

    @org.jetbrains.annotations.Nullable
    private static IOpticalComputationProvider computationProvider(
                                                                   com.gregtechceu.gtceu.api.machine.feature.multiblock.IMultiPart part) {
        if (part instanceof IOpticalComputationProvider provider) return provider;
        var cap = part.self().holder.self()
                .getCapability(com.gregtechceu.gtceu.api.capability.forge.GTCapability.CAPABILITY_COMPUTATION_PROVIDER);
        return cap.resolve().orElse(null);
    }

    /**
     * The gun (everything above the turret ring) is in the controller and drawn slewing to the target. It stays
     * there while the structure is broken or paused: putting 100 000 blocks back on every broken casing made the
     * clients rebuild a hundred chunk sections each time. It returns to the world only when the controller goes.
     */
    public boolean isCaptured() {
        return captured;
    }

    private java.util.Map<net.minecraft.core.BlockPos, Character> gun() {
        return CapturedParts.positions(getLevel(), "kinetic_orbital_lance", "gun", getPos(), getFrontFacing(),
                getUpwardsFacing(), isFlipped());
    }

    private void captureGun() {
        if (captured || getLevel() == null) return;
        // Each removed block would otherwise trigger a full structure check (seconds on a structure this size).
        long t0 = System.nanoTime();
        com.raishxn.gtna.common.item.terminal.NexusBuildCheckGuard.quiet(getMultiblockState(),
                () -> CapturedParts.capture(getLevel(), gun()));
        com.raishxn.gtna.GTNACORE.LOGGER.info("[GTNA perf] lance gun captured in {} ms",
                (System.nanoTime() - t0) / 1_000_000);
        captured = true;
    }

    private void releaseGun() {
        if (!captured || getLevel() == null || getLevel().isClientSide) return;
        long t0 = System.nanoTime();
        com.raishxn.gtna.common.item.terminal.NexusBuildCheckGuard.quiet(getMultiblockState(),
                () -> CapturedParts.release(getLevel(), "kinetic_orbital_lance", gun()));
        com.raishxn.gtna.GTNACORE.LOGGER.info("[GTNA perf] lance gun released in {} ms",
                (System.nanoTime() - t0) / 1_000_000);
        captured = false;
    }

    /** Development: aims at {@code b} and fits a sample bench, for screenshots. */
    public void debugShowcase(Body b) {
        target = b.ordinal();
        core.fitted.clear();
        for (int i = 0; i < 4; i++) core.fitted.add(LanceCore.Component.RAIL_SUPERCONDUCTOR);
        core.fitted.add(LanceCore.Component.COOLING_HELIUM);
        core.fitted.add(LanceCore.Component.SENSOR_TELESCOPE);
        core.fitted.add(LanceCore.Component.CAPSULE_ABLATIVE);
        syncBench();
    }

    /** Development: fires a neutronium slug at the current target with a full bank, as a real shot. */
    public void debugFire() {
        core.bankCharge = core.bankCapacity();
        var shot = core.fire(target(), Projectile.NEUTRONIUM, cwu);
        if (shot.fired) shotFlash = 0;
        if (shot.recoveredKg > 0) capsules.add(new double[] { target, shot.recoveredKg, shot.returnSeconds });
    }

    @Override
    public void onMachineRemoved() {
        releaseGun();
    }

    /** What the screen shows that the fields above do not: see {@link #view()} for the layout. */
    @DescSynced
    private double[] view = new double[0];

    public double[] view() {
        return view;
    }

    private void syncBench() {
        // view: bank, capacity, barrel K, liner wear, efficiency, accuracy, capsules, auto, loaded slug, surveys...,
        // seconds to the next capsule landing (-1 with none in flight)
        var v = new double[10 + Body.values().length];
        v[0] = core.bankCharge;
        v[1] = core.bankCapacity();
        v[2] = core.barrelTemperature;
        v[3] = core.linerWear;
        v[4] = core.efficiency();
        v[5] = core.accuracy(target(), cwu);
        v[6] = capsules.size();
        v[7] = autoFire ? 1 : 0;
        Projectile loaded = getLevel() != null && !getLevel().isClientSide ? loadedProjectile(target()) : null;
        v[8] = loaded == null ? -1 : loaded.ordinal();
        for (var b : Body.values()) v[9 + b.ordinal()] = core.survey(b);
        v[9 + Body.values().length] = capsules.stream().mapToDouble(c -> c[2]).min().orElse(-1);
        view = v;
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
    protected void idleSecond() {
        // Switched off: the shot effect ends instead of freezing on the last frame.
        shotFlash = 99;
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
        replaceWornLiner();
        // A cartridge in the Target Cartridge Hatch picks the target; cartridges take turns shot by shot.
        var cartridges = hatch(OriginalHatchPartMachine.Kind.TARGET_CARTRIDGE);
        if (cartridges != null && !cartridges.stock().get(0).isEmpty()) {
            var body = com.raishxn.gtna.common.data.GTNAOriginals.cartridgeBody(cartridges.stock().get(0));
            if (body != null && core.targetable(body)) target = body.ordinal();
        }
        Projectile projectile = loadedProjectile(target());
        if (autoFire && projectile != null && core.bankCharge >= core.bankCapacity() && core.targetable(target())) {
            if (take(s -> projectileOf(s) == projectile, 1) == 1) {
                var shot = core.fire(target(), projectile, cwu);
                if (shot.fired) {
                    shotFlash = 0;
                    if (cartridges != null) cartridges.cycle();
                }
                if (shot.recoveredKg > 0) capsules.add(new double[] { target, shot.recoveredKg, shot.returnSeconds });
            }
        }
        var unloaded = new ArrayList<double[]>();
        for (double[] c : capsules) {
            // Capsules launched before G-0272 carry the old linear flight time.
            c[2] = Math.min(c[2], LanceCore.returnSeconds(Body.values()[(int) c[0]]));
            if (--c[2] > 0) continue;
            c[1] = deliverCapsule(Body.values()[(int) c[0]], c[1]);
            if (c[1] <= 0) unloaded.add(c);
        }
        capsules.removeAll(unloaded);
        syncedYaw = target * 0.4;
        int mask = 0;
        for (var b : Body.values()) if (core.targetable(b)) mask |= 1 << b.ordinal();
        targetableMask = mask;
        syncBench();
    }

    /** Kilograms of recovered mass per dust (100 t). */
    public static final double KG_PER_DUST = 100_000;

    /**
     * Unloads a landed capsule into the output buses: one dust per {@link #KG_PER_DUST}, split over the body's
     * materials. Returns the mass still aboard; a capsule that does not fit waits instead of voiding its cargo.
     */
    private double deliverCapsule(Body body, double kg) {
        var materials = materials(body);
        long dusts = (long) (kg / KG_PER_DUST / materials.length);
        if (dusts <= 0) return 0;
        long left = 0;
        for (var m : materials) {
            var stack = ChemicalHelper.get(TagPrefix.dust, m);
            left += stack.isEmpty() ? 0 : output(stack, dusts);
        }
        return left * KG_PER_DUST;
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
            case ARROKOTH -> new Material[] { OriginalsMaterials.PrimordialTholin, GTMaterials.Nitrogen,
                    GTMaterials.Methane, GTMaterials.Carbon };
            case NEXUS_1 -> new Material[] { OriginalsMaterials.Nexium, GTMaterials.Naquadah, GTMaterials.Neutronium,
                    GTNAMaterials.SpaceTime == null ? GTMaterials.Neutronium : GTNAMaterials.SpaceTime };
        };
    }

    /** Projectile of an input stack: ingots of the projectile material. */
    public static Projectile projectileOf(ItemStack stack) {
        var entry = ChemicalHelper.getMaterialEntry(stack.getItem());
        if (entry.isEmpty() || entry.tagPrefix() != TagPrefix.ingot || entry.material() == null) return null;
        var m = entry.material();
        if (m == GTMaterials.NaquadahAlloy) return Projectile.NAQUADAH_ALLOY;
        if (m == GTMaterials.Trinium) return Projectile.TRINIUM;
        if (m == GTMaterials.Neutronium) return Projectile.NEUTRONIUM;
        if (m == GTNAMaterials.CosmicNeutronium) return Projectile.COSMIC_NEUTRONIUM;
        if (m == GTNAMaterials.WhiteDwarfMatter) return Projectile.DEGENERATE;
        if (m == OriginalsMaterials.Magnetarium) return Projectile.MAGNETAR;
        return null;
    }

    /** First projectile in the input buses that can break the target's crust. */
    private Projectile loadedProjectile(Body target) {
        Projectile[] found = { null };
        take(s -> {
            var p = projectileOf(s);
            if (p != null && found[0] == null && LanceCore.pierces(target, p)) found[0] = p;
            return false;
        }, 64);
        return found[0];
    }

    // ------------------------------------------------------------------ GUI

    @Override
    public void addDisplayText(List<Component> text) {
        OriginalMachine.displayHeader(this, text, isCaptured() && isFormed());
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
        text.add(Component.translatable(k + (cwu > 0 ? "computation" : computationHatch ? "computation_starved" :
                "computation_none"), cwu));
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
        if (data.equals("tp") || data.equals("tn")) {
            // Previous / next targetable body.
            int n = Body.values().length;
            for (int k = 1; k <= n; k++) {
                int t = Math.floorMod(target + (data.equals("tn") ? k : -k), n);
                if (core.targetable(Body.values()[t])) {
                    target = t;
                    break;
                }
            }
            syncBench();
            return;
        }
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
    public com.lowdragmc.lowdraglib.gui.modular.ModularUI createUI(net.minecraft.world.entity.player.Player player) {
        return com.raishxn.gtna.common.machine.multiblock.originals.ui.LanceScreen.create(this, player);
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
