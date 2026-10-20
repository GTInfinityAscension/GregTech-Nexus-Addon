package com.raishxn.gtna.api.machine.feature.rift;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.SplittableRandom;

/**
 * Tuning, stability and progression of the Dimensional Rift Gate (original GTNA, UIV). Plain Java, unit-tested by
 * {@code RiftCoreTest}; design in {@code docs/roadmap/design/portao-de-fenda.md}. One {@link #step} is one second.
 */
public final class RiftCore {

    public static final double LAMBDA0 = 1.5, KAPPA = 2.0, LAMBDA_PYLON = 0.4;

    /** Biomes drawn by a seed: weight, minimum depth. */
    public enum Biome {

        CRYSTAL_PLAINS(30, 0),
        MERCURY_OCEAN(20, 0),
        FORGE_WORLD(15, 0),
        SPORE_FOREST(15, 0),
        ANTIMATTER_ABYSS(8, 0),
        CIVILISATION_RELIC(7, 20),
        VOID(5, 40);

        public final int weight, minDepth;

        Biome(int weight, int minDepth) {
            this.weight = weight;
            this.minDepth = minDepth;
        }
    }

    /** Musical intervals that can be recorded as harmonics. */
    public enum Harmonic {

        OCTAVE(2, 1),
        FIFTH(3, 2),
        FOURTH(4, 3),
        MAJOR_THIRD(5, 4),
        MINOR_SIXTH(8, 5),
        MINOR_SEVENTH(9, 5),
        TRITONE(45, 32),
        MINOR_SECOND(16, 15);

        public final int p, q;

        Harmonic(int p, int q) {
            this.p = p;
            this.q = q;
        }

        /** Consonance 1 / log2(p q): simple ratios are more stable. */
        public double consonance() {
            return 1 / (Math.log(p * q) / Math.log(2));
        }
    }

    // ------------------------------------------------------------------ the open rift
    public long seed;
    public boolean open;
    public double frequency = 500, phase = 180, amplitude = 50;   // THz, degrees, percent
    public double stability;                                       // 0..100
    public int depth = 1;
    public int maxDepth = 5;
    public int probes;                                             // probes launched at this seed
    public int pylons = 4;
    public int resonantSeconds;
    public final List<Harmonic> score = new ArrayList<>();         // up to 5 harmonics loaded on the staff
    public final boolean[] collected = new boolean[Harmonic.values().length];
    public final List<long[]> atlas = new ArrayList<>();           // {seed, bestDepth, bestResonance * 1000}

    /** Hidden optimum of a seed: frequency (1..1000 THz), phase (0..360), amplitude (0..100). */
    public static double[] optimum(long seed) {
        var r = new SplittableRandom(seed);
        return new double[] { 1 + r.nextDouble() * 999, r.nextDouble() * 360, r.nextDouble() * 100 };
    }

    public static Biome biome(long seed) {
        var r = new SplittableRandom(seed ^ 0x5DEECE66DL);
        int total = Arrays.stream(Biome.values()).mapToInt(b -> b.weight).sum(), roll = r.nextInt(total);
        for (Biome b : Biome.values()) {
            roll -= b.weight;
            if (roll < 0) return b;
        }
        return Biome.CRYSTAL_PLAINS;
    }

    /** Harmonic a seed can give when held resonant. */
    public static Harmonic harmonic(long seed) {
        return switch (biome(seed)) {
            case CRYSTAL_PLAINS -> Harmonic.FIFTH;
            case SPORE_FOREST -> Harmonic.FOURTH;
            case MERCURY_OCEAN -> Harmonic.MAJOR_THIRD;
            case FORGE_WORLD -> Harmonic.MINOR_SIXTH;
            case CIVILISATION_RELIC -> Harmonic.MINOR_SEVENTH;
            case ANTIMATTER_ABYSS -> Harmonic.TRITONE;
            case VOID -> Harmonic.MINOR_SECOND;
        };
    }

    // Tolerances start wide enough to find the optimum by hand (the knobs span 1..1000 THz, 0..360 deg, 0..100 %);
    // each Rift Probe narrows them, which raises the resonance the same settings reach.
    public double sigmaF() {
        return 260 * Math.pow(0.8, probes);
    }

    public double sigmaPhi() {
        return 100 * Math.pow(0.8, probes);
    }

    public double sigmaA() {
        return 45 * Math.pow(0.8, probes);
    }

    /** How close one axis is to the optimum, 0..1 (0 frequency, 1 phase, 2 amplitude): the knobs' hot/cold hint. */
    public double axisCloseness(int axis) {
        double[] o = optimum(seed);
        return switch (axis) {
            case 0 -> Math.exp(-sq((frequency - o[0]) / sigmaF()));
            case 1 -> {
                double d = Math.abs(phase - o[1]) % 360;
                yield Math.exp(-sq(Math.min(d, 360 - d) / sigmaPhi()));
            }
            default -> Math.exp(-sq((amplitude - o[2]) / sigmaA()));
        };
    }

    /** Resonance R in 0..1. */
    public double resonance() {
        double[] o = optimum(seed);
        double dphi = Math.abs(phase - o[1]) % 360;
        dphi = Math.min(dphi, 360 - dphi);
        double e = sq((frequency - o[0]) / sigmaF()) + sq(dphi / sigmaPhi()) + sq((amplitude - o[2]) / sigmaA());
        return Math.exp(-e);
    }

    /** Mean consonance of the loaded chord; 0.3 neutral. */
    public double chordConsonance() {
        if (score.isEmpty()) return 0.3;
        return score.stream().mapToDouble(Harmonic::consonance).average().orElse(0.3);
    }

    public double lambda() {
        return LAMBDA0 * (1.3 - chordConsonance());
    }

    // EN: Every recorded harmonic opens 5 more depth levels. With the five harmonics of the surface biomes the base is
    // 30: a consonant chord reaches the Relic (20) and the tritone alone reaches the Void (40).
    // PT: Cada harmônico gravado libera mais 5 níveis. Com os cinco harmônicos dos biomas de superfície a base é 30:
    // um acorde consonante chega à Relíquia (20) e o trítono sozinho chega ao Vazio (40).
    // ZH: 每记录一个谐波，深度上限增加 5。收集地表生物群系的五个谐波后基础深度为 30：协和和弦可到达遗迹（20），
    // 单独的三全音可到达虚空（40）。
    public int baseMaxDepth() {
        int recorded = 0;
        for (boolean c : collected) if (c) recorded++;
        return Math.max(maxDepth, 5 + 5 * recorded);
    }

    public int effectiveMaxDepth() {
        return (int) Math.max(1, baseMaxDepth() * Math.max(0.5, 1 + 3 * (0.3 - chordConsonance())));
    }

    /** Exotic matter (L/s) needed to hold stability at the current resonance and depth. */
    public double upkeep() {
        return (lambda() * (1 - resonance()) * (1 + depth / 10.0) + LAMBDA_PYLON * (8 - pylons)) / KAPPA;
    }

    /** Output per second (base units): R^2 D^1.5 S/100. */
    public double outputRate() {
        double r = resonance();
        return r * r * Math.pow(depth, 1.5) * stability / 100;
    }

    // ------------------------------------------------------------------ one second

    public static final class Result {

        public double output;
        public Biome biome;
        public boolean collapsed, inverted, singularity, harmonicRecorded;
    }

    /** @param exotic litres of exotic matter delivered this second */
    public Result step(double exotic, SplittableRandom random) {
        Result out = new Result();
        if (!open) return out;
        double r = resonance();
        stability += KAPPA * exotic - lambda() * (1 - r) * (1 + depth / 10.0) - LAMBDA_PYLON * (8 - pylons);
        stability = Math.min(100, stability);
        out.biome = biome(seed);
        if (stability <= 0) {
            collapse();
            out.collapsed = true;
            return out;
        }
        if (r < 0.2) resonantSeconds = Math.min(0, resonantSeconds) - 1;
        else if (r >= 0.98) resonantSeconds = Math.max(0, resonantSeconds) + 1;
        else resonantSeconds = 0;
        if (resonantSeconds <= -10) {
            out.inverted = true;
            stability -= 10;
        }
        if (resonantSeconds >= 60 && random.nextDouble() < 0.05 / 60) out.singularity = true;
        if (r >= 0.9 && resonantSeconds >= 30) {
            var h = harmonic(seed);
            if (!collected[h.ordinal()]) {
                collected[h.ordinal()] = true;
                out.harmonicRecorded = true;
            }
        }
        if (depth >= out.biome.minDepth) out.output = outputRate();
        record(r);
        return out;
    }

    public void open(long newSeed) {
        seed = newSeed;
        open = true;
        stability = 50;
        depth = 1;
        probes = 0;
        resonantSeconds = 0;
    }

    public void collapse() {
        open = false;
        stability = 0;
        depth = 1;
    }

    /** Deepens the rift by one with a depth anchor. */
    public boolean deepen() {
        if (!open || depth >= effectiveMaxDepth()) return false;
        depth++;
        return true;
    }

    private void record(double r) {
        for (long[] e : atlas) {
            if (e[0] == seed) {
                e[1] = Math.max(e[1], depth);
                e[2] = Math.max(e[2], (long) (r * 1000));
                return;
            }
        }
        atlas.add(new long[] { seed, depth, (long) (r * 1000) });
    }

    /** Distance between two seeds in tuning space; linked in the atlas when below 1. */
    public static double distance(long a, long b) {
        double[] x = optimum(a), y = optimum(b);
        double dphi = Math.abs(x[1] - y[1]);
        dphi = Math.min(dphi, 360 - dphi);
        return Math.sqrt(sq((x[0] - y[0]) / 100) + sq(dphi / 36) + sq((x[2] - y[2]) / 10));
    }

    private static double sq(double v) {
        return v * v;
    }

    // ------------------------------------------------------------------ persistence

    public long[] pack() {
        long[] head = { seed, open ? 1 : 0, Double.doubleToRawLongBits(frequency), Double.doubleToRawLongBits(phase),
                Double.doubleToRawLongBits(amplitude), Double.doubleToRawLongBits(stability), depth, maxDepth, probes,
                pylons, resonantSeconds, mask(), score.size(), atlas.size() };
        long[] out = Arrays.copyOf(head, head.length + score.size() + atlas.size() * 3);
        int i = head.length;
        for (var h : score) out[i++] = h.ordinal();
        for (var e : atlas) {
            out[i++] = e[0];
            out[i++] = e[1];
            out[i++] = e[2];
        }
        return out;
    }

    private long mask() {
        long m = 0;
        for (int i = 0; i < collected.length; i++) if (collected[i]) m |= 1L << i;
        return m;
    }

    public void unpack(long[] v) {
        if (v == null || v.length < 14) return;
        seed = v[0];
        open = v[1] != 0;
        frequency = Double.longBitsToDouble(v[2]);
        phase = Double.longBitsToDouble(v[3]);
        amplitude = Double.longBitsToDouble(v[4]);
        stability = Double.longBitsToDouble(v[5]);
        depth = (int) v[6];
        maxDepth = (int) v[7];
        probes = (int) v[8];
        pylons = (int) v[9];
        resonantSeconds = (int) v[10];
        for (int i = 0; i < collected.length; i++) collected[i] = (v[11] & 1L << i) != 0;
        score.clear();
        atlas.clear();
        int i = 14;
        for (int k = 0; k < v[12] && i < v.length; k++) score.add(Harmonic.values()[(int) v[i++]]);
        for (int k = 0; k < v[13] && i + 2 < v.length; k++) atlas.add(new long[] { v[i++], v[i++], v[i++] });
    }
}
