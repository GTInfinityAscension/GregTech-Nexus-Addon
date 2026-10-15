package com.raishxn.gtna;

import com.raishxn.gtna.api.machine.feature.rift.RiftCore;
import com.raishxn.gtna.api.machine.feature.rift.RiftCore.Harmonic;

import java.util.SplittableRandom;

/** Dimensional Rift Gate tuning and progression against docs/roadmap/design/portao-de-fenda.md. */
public final class RiftCoreTest {

    private RiftCoreTest() {}

    public static void main(String[] args) {
        tuning();
        consonance();
        stability();
        harmonics();
        persistence();
        System.out.println("[RiftCoreTest] all cases passed");
    }

    private static void tuning() {
        var gate = new RiftCore();
        gate.open(42);
        double[] o = RiftCore.optimum(42);
        gate.frequency = o[0];
        gate.phase = o[1];
        gate.amplitude = o[2];
        near(gate.resonance(), 1, 1e-9, "exact tuning gives R = 1");
        gate.frequency += gate.sigmaF();
        near(gate.resonance(), Math.exp(-1), 1e-6, "one sigma off gives e^-1");
        gate.probes = 3;
        check(gate.resonance() < Math.exp(-1), "probes narrow the tolerance");
    }

    private static void consonance() {
        near(Harmonic.FIFTH.consonance(), 0.387, 0.01, "fifth 3:2");
        var gate = new RiftCore();
        gate.score.add(Harmonic.FIFTH);
        gate.score.add(Harmonic.OCTAVE);
        check(gate.lambda() < RiftCore.LAMBDA0 * 1.0 && gate.effectiveMaxDepth() <= gate.maxDepth,
                "consonant chord: cheaper and shallower");
        gate.score.clear();
        gate.score.add(Harmonic.TRITONE);
        gate.score.add(Harmonic.MINOR_SECOND);
        gate.maxDepth = 40;
        check(gate.effectiveMaxDepth() > 40, "dissonant chord reaches deeper");
    }

    private static void stability() {
        var gate = new RiftCore();
        gate.open(7);
        var rnd = new SplittableRandom(1);
        boolean collapsed = false;
        for (int i = 0; i < 1000 && !collapsed; i++) collapsed = gate.step(0, rnd).collapsed;
        check(collapsed && !gate.open, "an untuned rift without exotic matter collapses");
        gate.open(7);
        double[] o = RiftCore.optimum(7);
        gate.frequency = o[0];
        gate.phase = o[1];
        gate.amplitude = o[2];
        gate.pylons = 8;
        for (int i = 0; i < 200; i++) gate.step(gate.upkeep() + 0.01, rnd);
        check(gate.open && gate.stability > 50, "a tuned rift fed with exotic matter stays open");
    }

    private static void harmonics() {
        var gate = new RiftCore();
        gate.open(99);
        double[] o = RiftCore.optimum(99);
        gate.frequency = o[0];
        gate.phase = o[1];
        gate.amplitude = o[2];
        gate.pylons = 8;
        var rnd = new SplittableRandom(2);
        boolean recorded = false;
        for (int i = 0; i < 40 && !recorded; i++) recorded = gate.step(5, rnd).harmonicRecorded;
        check(recorded && gate.collected[RiftCore.harmonic(99).ordinal()], "30 resonant seconds record the harmonic");
        check(!gate.atlas.isEmpty(), "the seed enters the atlas");
    }

    private static void persistence() {
        var gate = new RiftCore();
        gate.open(1234);
        gate.depth = 3;
        gate.score.add(Harmonic.FOURTH);
        gate.collected[Harmonic.FOURTH.ordinal()] = true;
        gate.atlas.add(new long[] { 1234, 3, 900 });
        var copy = new RiftCore();
        copy.unpack(gate.pack());
        check(copy.seed == 1234 && copy.depth == 3 && copy.score.size() == 1 &&
                copy.collected[Harmonic.FOURTH.ordinal()] &&
                copy.atlas.size() == 1, "state survives save");
    }

    private static void near(double v, double e, double tol, String what) {
        check(Math.abs(v - e) <= Math.max(tol, Math.abs(e) * tol), what + ": " + v + " vs " + e);
    }

    private static void check(boolean ok, String what) {
        if (!ok) throw new AssertionError(what);
    }
}
