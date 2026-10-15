package com.raishxn.gtna.client.renderer.machine;

import com.gregtechceu.gtceu.api.machine.multiblock.WorkableElectricMultiblockMachine;

import net.minecraft.client.Minecraft;
import net.minecraft.client.resources.sounds.AbstractTickableSoundInstance;
import net.minecraft.client.resources.sounds.SimpleSoundInstance;
import net.minecraft.core.BlockPos;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundSource;
import net.minecraft.util.RandomSource;
import net.minecraft.world.phys.Vec3;
import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.api.distmarker.OnlyIn;
import net.minecraftforge.event.TickEvent;

import com.raishxn.gtna.GTNACORE;
import com.raishxn.gtna.common.machine.multiblock.originals.ColliderRingMachine;
import com.raishxn.gtna.common.machine.multiblock.originals.LanceMachine;
import com.raishxn.gtna.common.machine.multiblock.originals.RiftGateMachine;
import com.raishxn.gtna.common.machine.multiblock.originals.StellarChamberMachine;

import java.util.HashMap;
import java.util.Map;
import java.util.function.BooleanSupplier;

/**
 * Sounds of the original multiblocks (the author's set, tools/audio): a loop while the machine runs and one-shot
 * effects on state changes seen in the synced fields (a lance shot, a collider quench, a starquake, a rift opening).
 * Machines are picked up when their renderer first runs and followed by a client tick until they unload.
 */
@OnlyIn(Dist.CLIENT)
public final class OriginalsSound {

    private static final Map<BlockPos, WorkableElectricMultiblockMachine> SEEN = new HashMap<>();
    private static final Map<BlockPos, Loop> LOOPS = new HashMap<>();
    /** Last observed value per machine, for edge detection. */
    private static final Map<BlockPos, double[]> LAST = new HashMap<>();

    private OriginalsSound() {}

    private static SoundEvent event(String name) {
        return SoundEvent.createVariableRangeEvent(GTNACORE.id("originals." + name));
    }

    /** Called from the renderers. */
    public static void track(WorkableElectricMultiblockMachine machine) {
        SEEN.putIfAbsent(machine.getPos().immutable(), machine);
    }

    public static void onClientTick(TickEvent.ClientTickEvent event) {
        if (event.phase != TickEvent.Phase.END || SEEN.isEmpty()) return;
        var level = Minecraft.getInstance().level;
        var it = SEEN.entrySet().iterator();
        while (it.hasNext()) {
            var e = it.next();
            var m = e.getValue();
            if (m.isInValid() || m.getLevel() != level) {
                it.remove();
                LAST.remove(e.getKey());
                continue;
            }
            update(e.getKey(), m);
        }
    }

    private static void update(BlockPos key, WorkableElectricMultiblockMachine m) {
        Vec3 at = Vec3.atCenterOf(key);
        if (m instanceof StellarChamberMachine s) {
            Vec3 c = Vec3.atCenterOf(s.center());
            boolean hole = s.isBlackHole();
            loop(key, hole ? "stellar_black_hole_loop" : "stellar_pulsar_loop", c, s::isStarRunning);
            double quakes = s.quakes().length;
            if (edge(key, 0, quakes) && quakes > 0) once("stellar_quake", c);
        } else if (m instanceof ColliderRingMachine c) {
            loop(key, "collider_loop", at, c::isBeamOn);
            double on = c.isBeamOn() ? 1 : 0;
            // Beam lost while the machine still runs: a quench.
            if (edge(key, 0, on) && on == 0 && c.isFormed() && c.isWorkingEnabled()) once("collider_quench", at);
        } else if (m instanceof RiftGateMachine r) {
            Vec3 c = Vec3.atCenterOf(r.offset(RiftGateMachine.CENTER_UP, RiftGateMachine.CENTER_BACK));
            loop(key, "rift_loop", c, r::isRiftOpen);
            double open = r.isRiftOpen() ? 1 : 0;
            if (edge(key, 0, open) && open == 1) once("rift_open", c);
        } else if (m instanceof LanceMachine l) {
            loop(key, "lance_charge_loop", at, () -> l.isCaptured() && l.isFormed());
            double since = l.secondsSinceShot();
            if (edge(key, 0, since) && since == 0)
                once("lance_fire", Vec3.atCenterOf(l.offset(LanceMachine.MUZZLE_UP, LanceMachine.MUZZLE_BACK)));
        }
    }

    /** Whether slot {@code i} of the machine changed since the last tick (never on the first observation). */
    private static boolean edge(BlockPos key, int i, double value) {
        double[] last = LAST.get(key);
        if (last == null) {
            LAST.put(key, new double[] { value });
            return false;
        }
        boolean changed = last[i] != value;
        last[i] = value;
        return changed;
    }

    private static void once(String name, Vec3 at) {
        Minecraft.getInstance().getSoundManager().play(new SimpleSoundInstance(event(name), SoundSource.BLOCKS, 1f,
                1f, RandomSource.create(), at.x, at.y, at.z));
    }

    private static void loop(BlockPos key, String name, Vec3 at, BooleanSupplier active) {
        var playing = LOOPS.get(key);
        if (playing != null && !playing.isStopped() && playing.name.equals(name)) return;
        if (!active.getAsBoolean()) return;
        if (playing != null) playing.end();
        var loop = new Loop(name, at, active);
        LOOPS.put(key, loop);
        Minecraft.getInstance().getSoundManager().play(loop);
    }

    private static final class Loop extends AbstractTickableSoundInstance {

        final String name;
        private final BooleanSupplier active;

        Loop(String name, Vec3 at, BooleanSupplier active) {
            super(event(name), SoundSource.BLOCKS, RandomSource.create());
            this.name = name;
            this.active = active;
            this.x = at.x;
            this.y = at.y;
            this.z = at.z;
            this.looping = true;
            this.delay = 0;
        }

        void end() {
            stop();
        }

        @Override
        public void tick() {
            if (!active.getAsBoolean()) stop();
        }
    }
}
