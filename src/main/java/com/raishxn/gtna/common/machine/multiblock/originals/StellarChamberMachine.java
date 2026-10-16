package com.raishxn.gtna.common.machine.multiblock.originals;

import com.gregtechceu.gtceu.api.capability.recipe.FluidRecipeCapability;
import com.gregtechceu.gtceu.api.capability.recipe.IO;
import com.gregtechceu.gtceu.api.capability.recipe.ItemRecipeCapability;
import com.gregtechceu.gtceu.api.data.chemical.ChemicalHelper;
import com.gregtechceu.gtceu.api.data.chemical.material.Material;
import com.gregtechceu.gtceu.api.data.tag.TagPrefix;
import com.gregtechceu.gtceu.api.machine.IMachineBlockEntity;
import com.gregtechceu.gtceu.api.machine.TickableSubscription;
import com.gregtechceu.gtceu.api.machine.multiblock.WorkableElectricMultiblockMachine;
import com.gregtechceu.gtceu.api.machine.trait.NotifiableFluidTank;
import com.gregtechceu.gtceu.api.machine.trait.NotifiableItemStackHandler;
import com.gregtechceu.gtceu.common.data.GTMaterials;

import com.lowdragmc.lowdraglib.gui.util.ClickData;
import com.lowdragmc.lowdraglib.gui.widget.ComponentPanelWidget;
import com.lowdragmc.lowdraglib.syncdata.annotation.DescSynced;
import com.lowdragmc.lowdraglib.syncdata.annotation.Persisted;
import com.lowdragmc.lowdraglib.syncdata.field.ManagedFieldHolder;

import net.minecraft.core.BlockPos;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.nbt.LongArrayTag;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.Blocks;
import net.minecraftforge.fluids.capability.IFluidHandler;

import com.gtinfinityascension.gtialib.data.Int128;
import com.raishxn.gtna.api.capability.WirelessEnergyManager;
import com.raishxn.gtna.api.machine.feature.stellar.StellarCore;
import com.raishxn.gtna.common.data.GTNAMaterials;
import com.raishxn.gtna.common.data.GTNAOriginals;
import com.raishxn.gtna.common.data.material.OriginalsMaterials;
import com.raishxn.gtna.common.item.terminal.NexusBuildCheckGuard;
import org.jetbrains.annotations.Nullable;

import java.math.BigDecimal;
import java.util.List;
import java.util.UUID;

/**
 * Stellar Containment Chamber (original GTNA, MAX). Runs {@link StellarCore} once per second: feeds mass from the
 * fluid hatches, pays the band upkeep and delivers the extracted energy to the owner's Nexus network.
 *
 * <p>
 * The degenerate core blocks at the centre are taken into the controller when the star is lit (the renderer draws
 * the star in their place) and put back when the machine is switched off, the way the Forge of Gods handles its
 * rings. Design: {@code docs/roadmap/design/camara-estelar.md}.
 */
public class StellarChamberMachine extends WorkableElectricMultiblockMachine implements StructureWatch.Host {

    protected static final ManagedFieldHolder MANAGED_FIELD_HOLDER = new ManagedFieldHolder(
            StellarChamberMachine.class, WorkableElectricMultiblockMachine.MANAGED_FIELD_HOLDER);

    /** Blocks from the controller to the centre of the sphere, along the back direction. */
    public static final int CENTER_DEPTH = 46;
    public static final int CORE_RADIUS = 7;

    private final StellarCore core = new StellarCore();

    @Persisted
    @Nullable
    private UUID networkOwner;
    /** Extraction setpoint as a power of two, EU/t = 2^setpoint. */
    @Persisted
    @DescSynced
    private int setpoint = 50;
    @Persisted
    @DescSynced
    private boolean captured;
    @DescSynced
    private double syncedMass = 1.2, syncedPeriod = 0.033, syncedDamage;
    @DescSynced
    private int syncedMode, syncedBands = 1;
    @DescSynced
    private boolean syncedMagnetar;
    @DescSynced
    private double lastEnergy;
    @DescSynced
    private boolean hasProbe;
    /** The bands were powered last second and the star is not disrupted: the renderer shows it only then. */
    @DescSynced
    private boolean running;
    /** Recent quakes {size, kind} flattened, for the seismogram tab. */
    @DescSynced
    private double[] syncedQuakes = new double[0];

    @Nullable
    private TickableSubscription tick;
    private final StructureWatch watch = new StructureWatch(this);
    private int ticker;

    public StellarChamberMachine(IMachineBlockEntity holder, Object... args) {
        super(holder, args);
    }

    @Override
    public ManagedFieldHolder getFieldHolder() {
        return MANAGED_FIELD_HOLDER;
    }

    public StellarCore core() {
        return core;
    }

    // ------------------------------------------------------------------ client view

    public boolean hasSeismicProbe() {
        return hasProbe;
    }

    public double[] quakes() {
        return syncedQuakes;
    }

    /** Lit and actually running (powered bands, not disrupted); what the renderer shows. */
    public boolean isStarRunning() {
        return running && isStarLit() && syncedMode != StellarCore.Mode.DISRUPTED.ordinal();
    }

    public boolean isStarLit() {
        return captured && isFormed() && isWorkingEnabled();
    }

    public double damage() {
        return syncedDamage;
    }

    public int bandTier() {
        return syncedBands;
    }

    public double output() {
        return lastEnergy;
    }

    public double renderMass() {
        return syncedMass;
    }

    public double renderPeriod() {
        return syncedPeriod;
    }

    public boolean isBlackHole() {
        return syncedMode == StellarCore.Mode.BLACK_HOLE.ordinal();
    }

    public boolean isMagnetar() {
        return syncedMagnetar;
    }

    /** Centre of the sphere in world coordinates. */
    public BlockPos center() {
        return getPos().relative(getFrontFacing().getOpposite(), CENTER_DEPTH);
    }

    // ------------------------------------------------------------------ lifecycle

    @Override
    public StructureWatch structureWatch() {
        return watch;
    }

    /** Not re-walked on GTCEu's async thread every second: see {@link StructureWatch}. */
    @Override
    public void asyncCheckPattern(long periodID) {
        if (watch.usable()) watch.poll();
        else super.asyncCheckPattern(periodID);
    }

    @Override
    public boolean shouldOpenUI(net.minecraft.world.entity.player.Player player,
                                net.minecraft.world.InteractionHand hand,
                                net.minecraft.world.phys.BlockHitResult hit) {
        watch.opened();
        return super.shouldOpenUI(player, hand, hit);
    }

    @Override
    public void onStructureFormed() {
        super.onStructureFormed();
        watch.formed();
        tick = subscribeServerTick(tick, this::stellarTick);
    }

    @Override
    public void onStructureInvalid() {
        releaseCore();
        super.onStructureInvalid();
        watch.invalid();
        if (tick != null) {
            tick.unsubscribe();
            tick = null;
        }
    }

    @Override
    public void setWorkingEnabled(boolean enabled) {
        super.setWorkingEnabled(enabled);
        if (!enabled) releaseCore();
    }

    /** Radius (blocks from the centre) inside the hull where the star pulls entities in. */
    public static final double GRAVITY_RADIUS = 43;

    /**
     * Every tick while the star burns: entities inside the hull fall towards it, harder the closer they get (a
     * game-scale 1/r pull, capped so a player can still fly out at the edge).
     */
    private void pullEntities(ServerLevel level) {
        var c = net.minecraft.world.phys.Vec3.atCenterOf(center());
        for (var e : level.getEntitiesOfClass(net.minecraft.world.entity.Entity.class,
                new net.minecraft.world.phys.AABB(c, c).inflate(GRAVITY_RADIUS))) {
            // Players move on their own client: StellarGravityClient pulls the local player there.
            if (e instanceof net.minecraft.world.entity.player.Player) continue;
            if (pull(e, c, isBlackHole())) e.hurtMarked = true;
        }
    }

    /**
     * One tick of the star's gravity on an entity: a 1/r pull with drag and a terminal speed, the world's own gravity
     * cancelled inside the hull, and inside 10 blocks a field that holds entities off the star. Returns whether it
     * applied.
     */
    public static boolean pull(net.minecraft.world.entity.Entity e, net.minecraft.world.phys.Vec3 c, boolean hole) {
        if (e.isSpectator() || e.noPhysics) return false;
        var to = c.subtract(e.position());
        double d = to.length();
        if (d > GRAVITY_RADIUS || d < 1) return false;
        double a = Math.min(0.12, 0.6 * (hole ? 2.5 : 1) / d) * (d < 10 ? -1 : 1);
        var v = e.getDeltaMovement().scale(0.9).add(to.scale(a / d));
        if (!e.isNoGravity()) v = v.add(0, 0.08, 0);
        double speed = v.length();
        e.setDeltaMovement(speed > 0.9 ? v.scale(0.9 / speed) : v);
        e.fallDistance = 0;
        return true;
    }

    private void stellarTick() {
        if (getLevel() instanceof ServerLevel pulling && running && isStarLit()) pullEntities(pulling);
        if (!(getLevel() instanceof ServerLevel level) || ++ticker % 20 != 0) return;
        if (networkOwner == null) networkOwner = getOwnerUUID();
        if (!isWorkingEnabled()) return;
        Int128 upkeep = Int128.fromBigInteger(BigDecimal.valueOf(core.bandUpkeep() * 20).toBigInteger());
        boolean powered = networkOwner != null && WirelessEnergyManager.consumeEnergy(level, networkOwner, upkeep);
        running = powered;
        // The star is lit (the core taken in) only once the bands have power; until then the core stays a block.
        if (!captured && (!powered || !captureCore())) {
            sync();
            return;
        }
        double fed = feed();
        armourMagnetar();
        var known = java.util.EnumSet.copyOf(core.decoded.isEmpty() ?
                java.util.EnumSet.noneOf(StellarCore.Quake.class) : core.decoded);
        var result = core.step(Math.pow(2, setpoint), fed, false, powered);
        // Only a Seismic Probe records quakes: without one a new quake is felt but not decoded.
        boolean probe = OriginalMachine.hatchOf(getParts(), OriginalHatchPartMachine.Kind.SEISMIC_PROBE) != null;
        if (!probe && result.quake != null && !known.contains(result.quake)) {
            core.decoded.remove(result.quake);
            if (!core.seismogram.isEmpty()) core.seismogram.remove(core.seismogram.size() - 1);
        }
        hasProbe = probe;
        if (result.energy > 0 && networkOwner != null)
            WirelessEnergyManager.addEnergy(level, networkOwner,
                    Int128.fromBigInteger(BigDecimal.valueOf(result.energy).toBigInteger()));
        lastEnergy = result.energy / 20;
        output(dust(GTMaterials.Neutronium), result.neutroniumDust);
        output(dust(GTNAMaterials.WhiteDwarfMatter), result.degenerateMatter);
        // A magnetar starquake leaves a crystal of the inverted field; a collapse leaves core matter.
        if (result.quake == StellarCore.Quake.ANTI)
            output(ChemicalHelper.get(TagPrefix.gem, OriginalsMaterials.MagnetarCrystal), MAGNETAR_CRYSTALS);
        if (result.quake == StellarCore.Quake.COLLAPSE || result.collapsed)
            output(dust(OriginalsMaterials.DegenerateCoreMatter), CORE_MATTER);
        if (result.disrupted) releaseCore();
        sync();
    }

    /** What the screen shows that the fields above do not: see {@link #view()} for the layout. */
    @DescSynced
    private double[] view = new double[0];

    public double[] view() {
        return view;
    }

    private void sync() {
        // view: crust stress, extraction setpoint (2^n EU/t), extraction cap (EU/t), magnetar seconds
        view = new double[] { core.stress, setpoint, core.extractionCap(), core.magnetarSeconds };
        syncedMass = core.mass;
        syncedPeriod = core.period;
        syncedDamage = core.damage;
        syncedMode = core.mode.ordinal();
        syncedBands = core.bandTier;
        syncedMagnetar = core.magnetarField;
        double[] q = new double[core.seismogram.size() * 2];
        for (int i = 0; i < core.seismogram.size(); i++) {
            q[i * 2] = core.seismogram.get(i)[0];
            q[i * 2 + 1] = core.seismogram.get(i)[1];
        }
        syncedQuakes = q;
        markDirty();
    }

    // ------------------------------------------------------------------ the core blocks

    private List<BlockPos> corePositions() {
        BlockPos c = center();
        var out = new java.util.ArrayList<BlockPos>();
        for (int x = -CORE_RADIUS; x <= CORE_RADIUS; x++)
            for (int y = -CORE_RADIUS; y <= CORE_RADIUS; y++)
                for (int z = -CORE_RADIUS; z <= CORE_RADIUS; z++)
                    if (x * x + y * y + z * z <= CORE_RADIUS * CORE_RADIUS) out.add(c.offset(x, y, z));
        return out;
    }

    /** Development: fills the degenerate core (the terminal leaves it as air, the pattern accepts both). */
    public void debugFillCore() {
        var level = getLevel();
        if (level == null || captured) return;
        var state = GTNAOriginals.DEGENERATE_MATTER_CORE.get().defaultBlockState();
        NexusBuildCheckGuard.quiet(getMultiblockState(), () -> {
            for (BlockPos p : corePositions()) level.setBlock(p, state, 2);
        });
    }

    /** Takes the degenerate core into the controller; all of it must be in place. */
    private boolean captureCore() {
        var level = getLevel();
        if (level == null) return false;
        var block = GTNAOriginals.DEGENERATE_MATTER_CORE.get();
        var positions = corePositions();
        for (BlockPos p : positions) if (!level.getBlockState(p).is(block)) return false;
        captured = true;
        // Each changed block would otherwise re-check the whole 93-block sphere.
        NexusBuildCheckGuard.quiet(getMultiblockState(),
                () -> {
                    for (BlockPos p : positions) level.setBlock(p, Blocks.AIR.defaultBlockState(), 2);
                });
        return true;
    }

    /** Puts the core back (where there is air) when the star goes dark. */
    private void releaseCore() {
        var level = getLevel();
        if (!captured || level == null || level.isClientSide) return;
        var state = GTNAOriginals.DEGENERATE_MATTER_CORE.get().defaultBlockState();
        // Cleared first: a structure check fired by these block changes would call back in here (it used to recurse
        // once per core block, a full sphere check each time: minutes of frozen server).
        captured = false;
        NexusBuildCheckGuard.quiet(getMultiblockState(), () -> {
            for (BlockPos p : corePositions()) if (level.getBlockState(p).isAir()) level.setBlock(p, state, 2);
        });
    }

    // ------------------------------------------------------------------ feed and output

    /** Solar masses per mB of each feed fluid. Packs can change the table. */
    public static double feedValue(net.minecraft.world.level.material.Fluid fluid) {
        if (is(fluid, GTNAMaterials.MagnetohydrodynamicallyConstrainedStarMatter)) return 1e-7;
        if (is(fluid, GTNAMaterials.WhiteDwarfMatter)) return 1e-8;
        if (is(fluid, GTNAMaterials.RawStarMatter)) return 1e-9;
        if (is(fluid, GTMaterials.Neutronium)) return 1e-10;
        return 0;
    }

    /** Any form of the material: liquid, molten, gas or plasma. */
    public static boolean is(net.minecraft.world.level.material.Fluid fluid, @Nullable Material material) {
        if (material == null ||
                !material.hasProperty(com.gregtechceu.gtceu.api.data.chemical.material.properties.PropertyKey.FLUID))
            return false;
        var storage = material
                .getProperty(com.gregtechceu.gtceu.api.data.chemical.material.properties.PropertyKey.FLUID)
                .getStorage();
        for (var key : new com.gregtechceu.gtceu.api.fluids.store.FluidStorageKey[] {
                com.gregtechceu.gtceu.api.fluids.store.FluidStorageKeys.LIQUID,
                com.gregtechceu.gtceu.api.fluids.store.FluidStorageKeys.MOLTEN,
                com.gregtechceu.gtceu.api.fluids.store.FluidStorageKeys.GAS,
                com.gregtechceu.gtceu.api.fluids.store.FluidStorageKeys.PLASMA }) {
            var f = storage.get(key);
            if (f != null && f.isSame(fluid)) return true;
        }
        return false;
    }

    /** Solar masses of one item in the Mass Injector: the material's fluid value times 144 mB. */
    public static double itemFeedValue(ItemStack stack) {
        var entry = ChemicalHelper.getMaterialEntry(stack.getItem());
        if (entry.isEmpty() || entry.material() == null || !entry.material().hasFluid()) return 0;
        if (entry.tagPrefix() != TagPrefix.dust && entry.tagPrefix() != TagPrefix.ingot) return 0;
        return feedValue(entry.material().getFluid()) * 144;
    }

    private double feed() {
        double total = 0;
        var injector = OriginalMachine.hatchOf(getParts(), OriginalHatchPartMachine.Kind.MASS_INJECTOR);
        if (injector != null) {
            var stock = injector.stock();
            for (int i = 0; i < stock.size(); i++) {
                double value = itemFeedValue(stock.get(i));
                if (value > 0) total += value * injector.take(i, 64).getCount();
            }
        }
        for (var part : getParts()) {
            for (var handlers : part.getRecipeHandlers()) {
                if (!handlers.isValid(IO.IN)) continue;
                for (var handler : handlers.getCapability(FluidRecipeCapability.CAP)) {
                    if (!(handler instanceof NotifiableFluidTank tank)) continue;
                    for (int t = 0; t < tank.getTanks(); t++) {
                        var fluid = tank.getFluidInTank(t);
                        double value = feedValue(fluid.getFluid());
                        if (value <= 0 || fluid.isEmpty()) continue;
                        total += value * fluid.getAmount();
                        tank.drainInternal(fluid.copy(), IFluidHandler.FluidAction.EXECUTE);
                    }
                }
            }
        }
        return total;
    }

    /** Magnetar Crystals from one magnetar (ANTI) starquake. */
    public static final long MAGNETAR_CRYSTALS = 4;
    /** Degenerate Core Matter dusts from a collapse. */
    public static final long CORE_MATTER = 64;
    /** Seconds of magnetar field one Forgecore plate holds. */
    public static final int ARMOUR_SECONDS = 60;

    /**
     * The inverted field tears the crust unless Forgecore plates in the Mass Injector take the load: one plate per
     * {@link #ARMOUR_SECONDS}. Without one the field drops and the crust takes the hit, so the 600 s that a magnetar
     * starquake needs take ten plates.
     */
    private void armourMagnetar() {
        if (!core.magnetarField || core.magnetarSeconds % ARMOUR_SECONDS != 0) return;
        var injector = OriginalMachine.hatchOf(getParts(), OriginalHatchPartMachine.Kind.MASS_INJECTOR);
        if (injector != null) {
            var stock = injector.stock();
            for (int i = 0; i < stock.size(); i++) {
                if (isArmour(stock.get(i)) && !injector.take(i, 1).isEmpty()) return;
            }
        }
        core.magnetarField = false;
        core.magnetarSeconds = 0;
        core.damage = Math.min(100, core.damage + 10);
    }

    public static boolean isArmour(ItemStack stack) {
        var entry = ChemicalHelper.getMaterialEntry(stack.getItem());
        return entry.tagPrefix() == TagPrefix.plate && entry.material() == OriginalsMaterials.Forgecore;
    }

    private static ItemStack dust(@Nullable Material material) {
        return material == null ? ItemStack.EMPTY : ChemicalHelper.get(TagPrefix.dust, material);
    }

    private void output(ItemStack stack, long amount) {
        if (stack.isEmpty() || amount <= 0) return;
        for (var part : getParts()) {
            for (var handlers : part.getRecipeHandlers()) {
                if (!handlers.isValid(IO.OUT)) continue;
                for (var handler : handlers.getCapability(ItemRecipeCapability.CAP)) {
                    if (!(handler instanceof NotifiableItemStackHandler items)) continue;
                    while (amount > 0) {
                        var piece = stack.copyWithCount((int) Math.min(64, amount));
                        var rest = items.storage.insertItem(firstSlot(items, piece), piece, false);
                        long moved = piece.getCount() - rest.getCount();
                        if (moved == 0) break;
                        amount -= moved;
                    }
                    if (amount <= 0) return;
                }
            }
        }
    }

    private static int firstSlot(NotifiableItemStackHandler items, ItemStack stack) {
        for (int i = 0; i < items.storage.getSlots(); i++)
            if (items.storage.insertItem(i, stack, true).getCount() < stack.getCount()) return i;
        return 0;
    }

    // ------------------------------------------------------------------ GUI

    @Override
    public void addDisplayText(List<Component> text) {
        OriginalMachine.displayHeader(this, text, running);
        if (!isFormed()) return;
        String key = "gtna.machine.stellar_containment_chamber.";
        text.add(Component.translatable(key + (captured ? "lit" : "dark")));
        text.add(Component.translatable(key + "mass", String.format("%.4f", syncedMass)));
        text.add(Component.translatable(key + "period", String.format("%.3f", syncedPeriod * 1000)));
        text.add(Component.translatable(key + "kepler",
                String.format("%.3f", StellarCore.keplerPeriod(syncedMass) * 1000)));
        text.add(Component.translatable(key + "bands", syncedBands));
        text.add(Component.translatable(key + "damage", String.format("%.1f", syncedDamage)));
        text.add(Component.translatable(key + "output", String.format("%.3e", lastEnergy)));
        text.add(Component.translatable(key + "setpoint", setpoint)
                .append(" ").append(ComponentPanelWidget.withButton(Component.literal("§c[-]"), "sp_sub"))
                .append(" ").append(ComponentPanelWidget.withButton(Component.literal("§a[+]"), "sp_add")));
        text.add(ComponentPanelWidget.withButton(
                Component.translatable(key + (syncedMagnetar ? "magnetar_on" : "magnetar_off")),
                "magnetar"));
        if (isBlackHole()) text.add(Component.translatable(key + "black_hole"));
    }

    @Override
    public void handleDisplayClick(String data, ClickData click) {
        if (click.isRemote) return;
        switch (data) {
            case "sp_sub" -> setpoint = Math.max(40, setpoint - 1);
            case "sp_add" -> setpoint = Math.min(62, setpoint + 1);
            case "magnetar" -> core.magnetarField = !core.magnetarField;
            default -> {
                return;
            }
        }
        sync();
    }

    @Override
    public com.lowdragmc.lowdraglib.gui.modular.ModularUI createUI(net.minecraft.world.entity.player.Player player) {
        return com.raishxn.gtna.common.machine.multiblock.originals.ui.StellarScreen.create(this, player);
    }

    // ------------------------------------------------------------------ persistence

    @Override
    public void saveCustomPersistedData(CompoundTag tag, boolean forDrop) {
        super.saveCustomPersistedData(tag, forDrop);
        double[] packed = core.pack();
        long[] bits = new long[packed.length];
        for (int i = 0; i < packed.length; i++) bits[i] = Double.doubleToRawLongBits(packed[i]);
        tag.put("gtna_stellar_core", new LongArrayTag(bits));
    }

    @Override
    public void loadCustomPersistedData(CompoundTag tag) {
        super.loadCustomPersistedData(tag);
        long[] bits = tag.getLongArray("gtna_stellar_core");
        if (bits.length == 0) return;
        double[] packed = new double[bits.length];
        for (int i = 0; i < bits.length; i++) packed[i] = Double.longBitsToDouble(bits[i]);
        core.unpack(packed);
        sync();
    }
}
