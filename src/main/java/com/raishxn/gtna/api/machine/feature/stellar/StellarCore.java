package com.raishxn.gtna.api.machine.feature.stellar;

import java.util.ArrayList;
import java.util.EnumSet;
import java.util.List;

/**
 * State and physics of the star held by the Stellar Containment Chamber. Plain Java, no Minecraft world access, so
 * the rules are unit-tested ({@code StellarCoreTest}) and documented in {@code docs/roadmap/design/camara-estelar.md}.
 *
 * <p>
 * Astrophysics is real (moment of inertia, rotational energy, accretion torque, Kepler break-up, TOV limit, Penrose
 * efficiency); only the energy scale is a game constant: {@link #EU_PER_JOULE}. One {@link #step} is one second.
 */
public final class StellarCore {

    public static final double G = 6.674e-11, C = 2.998e8, M_SUN = 1.989e30, RADIUS = 12e3;
    public static final double EU_PER_JOULE = 1e-20;
    public static final double TOV = 2.2, TOV_EXOTIC = 2.4, MAX_SPIN = 0.998;
    /** Effective dipole field of the containment bands (tesla); halved by the dipole shielding. */
    public static final double DIPOLE_FIELD = 6.7e11;
    /** Starquake stress per unit relative spin change. */
    public static final double STRESS_PER_SPIN = 1e4;

    public enum Mode {
        NEUTRON_STAR,
        BLACK_HOLE,
        DISRUPTED
    }

    /** Regions of the mass-period diagram the star has visited (each unlocks something). */
    public enum Region {
        COMMON,
        YOUNG,
        MILLISECOND,
        RECORD,
        MAGNETAR,
        TOV_EDGE,
        BLACK_HOLE
    }

    /** Starquake kinds, as in real pulsar glitch catalogs. Decoding one unlocks containment equipment. */
    public enum Quake {
        MICRO,
        CRAB,
        VELA,
        ANTI,
        COLLAPSE
    }

    public Mode mode = Mode.NEUTRON_STAR;
    public double mass = 1.2;          // solar masses
    public double period = 0.033;      // seconds
    public double stress;              // starquake stress, quake at >= 1
    public double spin;                // black hole a*, set at collapse
    public double holeEnergy;          // EU left in the black hole ergosphere
    public double damage;              // containment damage 0..100
    public double fedMass;             // total solar masses fed
    public double extracted;           // total EU extracted
    public long quakesContained;
    public int bandTier = 1;
    public boolean magnetarField;      // bands inverted (magnetar mode)
    public int magnetarSeconds;
    public final EnumSet<Region> regions = EnumSet.of(Region.COMMON);
    public final EnumSet<Quake> decoded = EnumSet.noneOf(Quake.class);
    /** Most recent quakes, newest last (for the seismogram). */
    public final List<double[]> seismogram = new ArrayList<>();

    // ------------------------------------------------------------------ physics

    public static double inertia(double massSolar) {
        return 0.4 * massSolar * M_SUN * RADIUS * RADIUS;
    }

    public double omega() {
        return 2 * Math.PI / period;
    }

    /** Rotational energy in EU. */
    public double rotationalEnergy() {
        double w = omega();
        return 0.5 * inertia(mass) * w * w * EU_PER_JOULE;
    }

    /** Kepler break-up period: below it the star sheds mass and comes apart. */
    public static double keplerPeriod(double massSolar) {
        return 2 * Math.PI * Math.sqrt(RADIUS * RADIUS * RADIUS / (G * massSolar * M_SUN));
    }

    public double tovLimit() {
        return decoded.contains(Quake.ANTI) ? TOV_EXOTIC : TOV;
    }

    /** Magnetic dipole spin-down power in EU/s. */
    public double dipoleLoss(boolean shielded) {
        double w = omega(), b = DIPOLE_FIELD * (shielded ? 0.5 : 1) * (magnetarField ? 4 : 1);
        double r6 = Math.pow(RADIUS, 6);
        return b * b * r6 * w * w * w * w / (6 * C * C * C) * EU_PER_JOULE;
    }

    /** Penrose efficiency of a Kerr black hole: the share of its mass-energy that can be extracted. */
    public static double penroseEfficiency(double a) {
        return 1 - Math.sqrt((1 + Math.sqrt(1 - a * a)) / 2);
    }

    /** Extraction cap in EU/t: 2^(55 + band tier) for a neutron star, 2^62 for a black hole. */
    public double extractionCap() {
        if (mode == Mode.BLACK_HOLE) return Math.pow(2, 62);
        double cap = Math.pow(2, 55 + bandTier);
        return regions.contains(Region.MILLISECOND) ? cap : cap / 2;
    }

    /** Continuous EU/t the bands draw from the network. */
    public double bandUpkeep() {
        return Math.pow(2, 40 + 2 * bandTier);
    }

    public double bandCapacity() {
        return 1e15 * Math.pow(10, bandTier);
    }

    // ------------------------------------------------------------------ one second

    /** What a {@link #step} produced. */
    public static final class Result {

        public double energy;          // EU delivered this second
        public long neutroniumDust;
        public long degenerateMatter;
        public Quake quake;            // quake this second, or null
        public boolean collapsed, disrupted, containmentFailed;
    }

    /**
     * Advances one second.
     *
     * @param requestEUt   extraction setpoint in EU/t
     * @param fedSolar     solar masses fed this second
     * @param shielded     dipole shielding installed
     * @param bandsPowered whether the band upkeep was paid
     */
    public Result step(double requestEUt, double fedSolar, boolean shielded, boolean bandsPowered) {
        Result out = new Result();
        if (mode == Mode.DISRUPTED) return out;
        if (mode == Mode.BLACK_HOLE) {
            double want = Math.min(requestEUt, extractionCap()) * 20;
            double got = Math.min(want, holeEnergy);
            holeEnergy -= got;
            extracted += got;
            out.energy = got;
            return out;
        }
        double w0 = omega();
        // Accretion: mass and angular momentum (recycled pulsar spin-up); 15% leaves as binding energy.
        if (fedSolar > 0) {
            double j = inertia(mass) * w0;
            double dj = fedSolar * M_SUN * Math.sqrt(G * mass * M_SUN * RADIUS);
            double binding = fedSolar * 0.15 * M_SUN * C * C * EU_PER_JOULE * 1e-6;
            mass += fedSolar * 0.85;
            fedMass += fedSolar;
            double w = (j + dj) / inertia(mass);
            period = 2 * Math.PI / w;
            out.energy += binding;
        }
        // Extraction and dipole braking come out of the rotational energy.
        double e = rotationalEnergy();
        double want = Math.min(requestEUt, extractionCap()) * 20;
        double loss = dipoleLoss(shielded);
        double taken = Math.min(want, Math.max(0, e - loss));
        e = Math.max(e - taken - loss, 1);
        period = 2 * Math.PI / Math.sqrt(2 * e / (inertia(mass) * EU_PER_JOULE));
        out.energy += taken;
        extracted += taken;
        out.neutroniumDust = (long) (taken / 20 / Math.pow(2, 52));
        // Starquakes from the change of spin.
        double rel = Math.abs(omega() - w0) / w0;
        stress += STRESS_PER_SPIN * rel;
        if (stress >= 1) {
            stress = 0;
            out.quake = classify(fedSolar, rel);
            double size = switch (out.quake) {
                case MICRO -> 5e-9;
                case CRAB -> 5e-8;
                case VELA -> 1.1e-6;
                case ANTI -> -3e-7;
                case COLLAPSE -> 1e-4;
            };
            double quakeEnergy = Math.abs(size) * 1e-6 / 1e-7 * rotationalEnergy() * 1e-6;
            out.degenerateMatter = (long) Math.min(Long.MAX_VALUE, quakeEnergy / 1e18);
            if (!bandsPowered || quakeEnergy > bandCapacity()) damage = Math.min(100, damage + 10);
            else quakesContained++;
            decoded.add(out.quake);
            seismogram.add(new double[] { size, out.quake.ordinal() });
            if (seismogram.size() > 64) seismogram.remove(0);
            unlockBands();
        }
        if (!bandsPowered) damage = Math.min(100, damage + 0.05);
        if (damage >= 100) {
            out.containmentFailed = true;
            mass *= 0.9;
            damage = 0;
        }
        // Magnetar: bands inverted for 10 minutes.
        magnetarSeconds = magnetarField ? magnetarSeconds + 1 : 0;
        updateRegions(fedSolar > 0);
        // Collapse and break-up.
        if (mass > tovLimit()) {
            collapse();
            out.collapsed = true;
        } else if (period < keplerPeriod(mass)) {
            mode = Mode.DISRUPTED;
            out.disrupted = true;
            out.degenerateMatter += (long) (mass * 1e6);
        }
        return out;
    }

    private Quake classify(double fedSolar, double rel) {
        if (mass > tovLimit() - 0.02) return Quake.COLLAPSE;
        if (magnetarField && magnetarSeconds >= 600) return Quake.ANTI;
        if (fedSolar > 0 && rel > 1e-4) return Quake.VELA;
        if (rel > 2e-5) return Quake.CRAB;
        return Quake.MICRO;
    }

    private void unlockBands() {
        int tier = 1;
        if (decoded.contains(Quake.MICRO)) tier = 2;
        if (decoded.contains(Quake.VELA)) tier = 3;
        if (tier == 3 && regions.contains(Region.RECORD)) tier = 4;
        bandTier = Math.max(bandTier, tier);
    }

    private void updateRegions(boolean feeding) {
        double ms = period * 1000;
        if (ms < 30) regions.add(Region.YOUNG);
        if (ms < 10 && (feeding || fedMass > 0)) regions.add(Region.MILLISECOND);
        if (ms < 1.4) regions.add(Region.RECORD);
        if (magnetarSeconds >= 600) regions.add(Region.MAGNETAR);
        if (mass > 2.1) regions.add(Region.TOV_EDGE);
        unlockBands();
    }

    private void collapse() {
        double j = inertia(mass) * omega();
        spin = Math.min(MAX_SPIN, j * C / (G * Math.pow(mass * M_SUN, 2)));
        holeEnergy = penroseEfficiency(spin) * mass * M_SUN * C * C * EU_PER_JOULE;
        mode = Mode.BLACK_HOLE;
        regions.add(Region.BLACK_HOLE);
        decoded.add(Quake.COLLAPSE);
    }

    // ------------------------------------------------------------------ persistence

    /** Packs the whole state into numbers (the machine stores them in NBT). */
    public double[] pack() {
        int r = 0, q = 0;
        for (var region : regions) r |= 1 << region.ordinal();
        for (var quake : decoded) q |= 1 << quake.ordinal();
        double[] head = { mode.ordinal(), mass, period, stress, spin, holeEnergy, damage, fedMass, extracted,
                quakesContained, bandTier, magnetarField ? 1 : 0, magnetarSeconds, r, q, seismogram.size() };
        double[] out = java.util.Arrays.copyOf(head, head.length + seismogram.size() * 2);
        for (int i = 0; i < seismogram.size(); i++) {
            out[head.length + i * 2] = seismogram.get(i)[0];
            out[head.length + i * 2 + 1] = seismogram.get(i)[1];
        }
        return out;
    }

    public void unpack(double[] v) {
        if (v == null || v.length < 16) return;
        mode = Mode.values()[(int) v[0]];
        mass = v[1];
        period = v[2];
        stress = v[3];
        spin = v[4];
        holeEnergy = v[5];
        damage = v[6];
        fedMass = v[7];
        extracted = v[8];
        quakesContained = (long) v[9];
        bandTier = (int) v[10];
        magnetarField = v[11] != 0;
        magnetarSeconds = (int) v[12];
        regions.clear();
        decoded.clear();
        for (var region : Region.values()) if (((int) v[13] & 1 << region.ordinal()) != 0) regions.add(region);
        for (var quake : Quake.values()) if (((int) v[14] & 1 << quake.ordinal()) != 0) decoded.add(quake);
        seismogram.clear();
        for (int i = 0; i < (int) v[15] && 16 + i * 2 + 1 < v.length; i++)
            seismogram.add(new double[] { v[16 + i * 2], v[17 + i * 2] });
    }
}
