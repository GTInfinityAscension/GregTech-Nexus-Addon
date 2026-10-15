package com.raishxn.gtna;

import com.raishxn.gtna.api.machine.feature.stellar.StellarCore;

/** Stellar Containment Chamber physics against the values in docs/roadmap/design/camara-estelar.md. */
public final class StellarCoreTest {

    private StellarCoreTest() {}

    public static void main(String[] args) {
        energy();
        limits();
        spinDown();
        spinUp();
        collapse();
        quakes();
        nbt();
        System.out.println("[StellarCoreTest] all cases passed");
    }

    private static void energy() {
        var star = new StellarCore();
        star.mass = 1.4;
        star.period = 0.0016;
        near(star.rotationalEnergy(), 1.24e25, 0.01, "millisecond pulsar E_rot");
        star.mass = 1.2;
        star.period = 0.033;
        near(star.rotationalEnergy(), 2.49e22, 0.01, "starting star E_rot");
    }

    private static void limits() {
        near(StellarCore.keplerPeriod(1.4) * 1000, 0.606, 0.01, "Kepler break-up at 1.4");
        near(StellarCore.penroseEfficiency(0.998), 0.271, 0.01, "Penrose efficiency at a=0.998");
        var star = new StellarCore();
        check(star.extractionCap() == Math.pow(2, 56) / 2, "cap halved before the millisecond region");
        star.regions.add(StellarCore.Region.MILLISECOND);
        check(star.extractionCap() == Math.pow(2, 56), "tier 1 cap 2^56");
    }

    private static void spinDown() {
        var star = new StellarCore();
        star.mass = 1.4;
        star.period = 0.0016;
        star.regions.add(StellarCore.Region.MILLISECOND);
        double before = star.rotationalEnergy();
        var r = star.step(Math.pow(2, 56), 0, false, true);
        check(r.energy > 0 && star.period > 0.0016, "extraction slows the star");
        check(star.rotationalEnergy() < before, "extraction lowers E_rot");
        check(r.neutroniumDust >= 0, "crust mining output");
    }

    private static void spinUp() {
        var star = new StellarCore();
        double p0 = star.period, m0 = star.mass;
        star.step(0, 1e-3, false, true);
        check(star.period < p0, "accretion spins the star up");
        near(star.mass, m0 + 0.85e-3, 1e-6, "85% of fed mass is kept");
    }

    private static void collapse() {
        var star = new StellarCore();
        star.mass = 2.199;
        star.period = 0.002;
        var r = star.step(0, 0.01, false, true);
        check(r.collapsed && star.mode == StellarCore.Mode.BLACK_HOLE, "crossing TOV collapses the star");
        check(star.spin > 0 && star.holeEnergy > 0, "black hole keeps spin and extractable energy");
        double e = star.holeEnergy;
        var r2 = star.step(Math.pow(2, 62), 0, false, true);
        check(r2.energy > 0 && star.holeEnergy < e, "ergosphere extraction drains the hole");
    }

    private static void quakes() {
        var star = new StellarCore();
        star.mass = 1.4;
        star.period = 0.003;
        star.regions.add(StellarCore.Region.MILLISECOND);
        StellarCore.Quake seen = null;
        for (int i = 0; i < 2000 && seen == null; i++) seen = star.step(Math.pow(2, 56), 0, false, true).quake;
        check(seen != null, "steady extraction eventually quakes");
        check(star.decoded.contains(seen) && !star.seismogram.isEmpty(), "quake decoded and recorded");
        check(star.bandTier >= 2 || seen != StellarCore.Quake.MICRO, "micro quake unlocks tier 2 bands");
    }

    private static void nbt() {
        var star = new StellarCore();
        star.mass = 1.7;
        star.period = 0.004;
        star.decoded.add(StellarCore.Quake.CRAB);
        star.regions.add(StellarCore.Region.YOUNG);
        star.seismogram.add(new double[] { 5e-8, 1 });
        var copy = new StellarCore();
        copy.unpack(star.pack());
        check(copy.mass == 1.7 && copy.period == 0.004, "mass and period survive save");
        check(copy.decoded.contains(StellarCore.Quake.CRAB) && copy.regions.contains(StellarCore.Region.YOUNG),
                "decoded quakes and regions survive save");
        check(copy.seismogram.size() == 1, "seismogram survives save");
    }

    private static void near(double value, double expected, double relative, String what) {
        check(Math.abs(value - expected) <= Math.abs(expected) * relative, what + ": " + value + " vs " + expected);
    }

    private static void check(boolean ok, String what) {
        if (!ok) throw new AssertionError(what);
    }
}
