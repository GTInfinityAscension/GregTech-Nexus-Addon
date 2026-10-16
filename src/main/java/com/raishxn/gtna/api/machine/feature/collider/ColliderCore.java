package com.raishxn.gtna.api.machine.feature.collider;

import java.util.Arrays;

/**
 * Beam physics and progression of the Antimatter Collider Ring (original GTNA, UIV). Plain Java, unit-tested by
 * {@code ColliderCoreTest}; design in {@code docs/roadmap/design/anel-colisor.md}.
 *
 * <p>
 * Real accelerator formulas (magnetic rigidity p = 0.3 B rho, luminosity, 5-sigma discovery); a game factor
 * {@link #GAME_LUMINOSITY} turns real luminosity into something reachable in hours. One {@link #step} is one second.
 */
public final class ColliderCore {

    public static final double RING_RADIUS_M = 60 * 50;           // 60 blocks at 50 m per block
    public static final double REVOLUTION_HZ = 2.998e8 / (2 * Math.PI * RING_RADIUS_M);
    public static final double GAME_LUMINOSITY = 1e5;               // fb^-1 per second = L * 1e-39 * this
    public static final double[] MAGNET_FIELD = { 8.3, 12, 20, 45, 120 };
    public static final String[] MAGNET_NAMES = { "NbTi", "Nb3Sn", "REBCO", "neutronium", "infinity" };

    /** Particles in discovery order: name, threshold E_cm (GeV), signal / sqrt(background) per sqrt(fb^-1). */
    public enum Particle {

        ANTIPROTON(5.6, 50),
        KAON(1.0, 30),
        LAMBDA(2.5, 8),
        CHARM(10, 4),
        BOTTOM(40, 1.5),
        W_BOSON(161, 0.6),
        Z_BOSON(182, 0.8),
        HIGGS(250, 0.08),
        TOP(346, 0.15),
        X_NEXUS(4800, 0.02);

        public final double thresholdGeV, strength;

        Particle(double thresholdGeV, double strength) {
            this.thresholdGeV = thresholdGeV;
            this.strength = strength;
        }
    }

    /** Beam-time committee proposals: what they ask for and what they deliver. */
    public enum Proposal {
        NB3SN_MAGNET,
        VERTEX_DETECTOR,
        STOCHASTIC_COOLING,
        CRYO_PENNING,
        REBCO_MAGNET,
        LEPTON_COLLIDER,
        HEAVY_IONS,
        NEUTRONIUM_MAGNET,
        BEYOND_STANDARD_MODEL
    }

    public enum Mode {
        PRODUCTION,
        PHYSICS
    }

    // ------------------------------------------------------------------ state
    public Mode mode = Mode.PRODUCTION;
    public int magnetTier;                  // index into MAGNET_FIELD
    public int bunches = 100;
    public double protonsPerBunch = 1e11;
    public double beamSizeMicron = 20;
    public int trapTier = 1;
    public double antiprotons;              // stored in the Penning traps
    public double rampSeconds;              // time spent ramping the main ring (20 s to full energy)
    public double heliumLevel = 1;          // 0..1 of the cryo plant
    public int quenchCooldown;
    public double damage;
    public final double[] integrated = new double[Particle.values().length];   // fb^-1 above threshold
    public final boolean[] proposalsDone = new boolean[Proposal.values().length];
    public Proposal activeProposal = Proposal.NB3SN_MAGNET;
    /** Set by the machine each second: Nexium wire for the tier-4 dipoles is waiting in the input buses. */
    public boolean nexiumWire;
    public double proposalProgress;          // fb^-1 delivered to the active proposal
    public boolean electronMode, heavyIonMode;

    // ------------------------------------------------------------------ physics

    public double field() {
        return MAGNET_FIELD[magnetTier];
    }

    /** Maximum beam energy in TeV: p = 0.3 B rho (GeV/c with B in T, rho in m). */
    public double maxBeamEnergyTeV() {
        return 0.3 * field() * RING_RADIUS_M / 1000;
    }

    /** Current centre-of-mass energy in GeV (counter-rotating beams of equal energy). */
    public double centreOfMassGeV() {
        double ramp = Math.min(1, rampSeconds / 20.0);
        return 2 * (150 + (maxBeamEnergyTeV() * 1000 - 150) * ramp);
    }

    /** Luminosity in cm^-2 s^-1: f_rev n_b N^2 / (4 pi sigma^2). */
    public double luminosity() {
        double sigmaCm = beamSizeMicron * 1e-4;
        return REVOLUTION_HZ * bunches * protonsPerBunch * protonsPerBunch / (4 * Math.PI * sigmaCm * sigmaCm);
    }

    /** Significance of a particle: (s / sqrt b) sqrt(integrated luminosity). */
    public double significance(Particle p) {
        return p.strength * Math.sqrt(integrated[p.ordinal()]) *
                (proposalsDone[Proposal.VERTEX_DETECTOR.ordinal()] ? Math.sqrt(2) : 1);
    }

    /** Production yield of a particle: 10% before evidence, 40% with 3 sigma, 100% after discovery. */
    public double yieldOf(Particle p) {
        double z = significance(p);
        return z >= 5 ? 1 : z >= 3 ? 0.4 : 0.1;
    }

    /** Liquid helium per second the magnets need. */
    public double heliumDemand() {
        return 0.5 * Math.pow(2, magnetTier) * (proposalsDone[Proposal.CRYO_PENNING.ordinal()] ? 0.6 : 1);
    }

    public double trapCapacity() {
        return 1e12 * Math.pow(4, trapTier - 1);
    }

    public double trapUpkeepEUt() {
        return Math.pow(2, trapTier + 20);
    }

    /** Synchrotron radiation load relative to the cryo capacity (dominant only for electron beams). */
    public double synchrotronLoad() {
        double e = centreOfMassGeV() / 2;
        double gammaRatio = electronMode ? e / 0.000511 : e / 0.938;
        return Math.pow(gammaRatio / 1e5, 4) * (electronMode ? 1 : 1e-12);
    }

    // ------------------------------------------------------------------ one second

    public static final class Result {

        public final double[] produced = new double[Particle.values().length];
        public boolean quench, annihilation, proposalFinished;
        public double annihilationJoules;
    }

    /**
     * @param helium      share of the helium demand delivered (0..1)
     * @param trapPowered Penning trap upkeep paid
     */
    public Result step(double helium, boolean trapPowered) {
        Result out = new Result();
        heliumLevel = helium;
        if (!trapPowered && antiprotons > 0) {
            out.annihilation = true;
            out.annihilationJoules = antiprotons * 2 * 1.67e-27 * 9e16;
            damage = Math.min(100, damage + Math.min(50, Math.log10(1 + out.annihilationJoules)));
            antiprotons = 0;
            return out;
        }
        if (quenchCooldown > 0) {
            quenchCooldown--;
            rampSeconds = 0;
            return out;
        }
        if (helium < 0.999 || synchrotronLoad() > 1) {
            out.quench = true;
            quenchCooldown = 60 * (magnetTier + 1);
            rampSeconds = 0;
            return out;
        }
        rampSeconds++;
        double fb = luminosity() * 1e-39 * GAME_LUMINOSITY;
        double ecm = centreOfMassGeV();
        for (Particle p : Particle.values()) {
            if (ecm < p.thresholdGeV) continue;
            if (p == Particle.X_NEXUS && !proposalsDone[Proposal.HEAVY_IONS.ordinal()]) continue;
            if (mode == Mode.PHYSICS) integrated[p.ordinal()] += fb;
            else out.produced[p.ordinal()] = fb * 1e3 * yieldOf(p) / (1 + p.ordinal());
        }
        if (mode == Mode.PRODUCTION) {
            double pbar = out.produced[Particle.ANTIPROTON.ordinal()] * 1e9 *
                    (proposalsDone[Proposal.STOCHASTIC_COOLING.ordinal()] ? 3 : 1);
            antiprotons = Math.min(trapCapacity(), antiprotons + pbar);
        } else if (activeProposal != null) {
            proposalProgress += fb;
            if (proposalMet(activeProposal)) {
                complete(activeProposal);
                out.proposalFinished = true;
            }
        }
        return out;
    }

    /** Whether a proposal's request is fulfilled. */
    public boolean proposalMet(Proposal p) {
        return switch (p) {
            case NB3SN_MAGNET -> proposalProgress >= 5 && maxBeamEnergyTeV() >= 7;
            case VERTEX_DETECTOR -> significance(Particle.CHARM) >= 5;
            case STOCHASTIC_COOLING -> proposalProgress >= 20;
            case CRYO_PENNING -> antiprotons >= 1e13 || proposalProgress >= 40;
            case REBCO_MAGNET -> significance(Particle.W_BOSON) >= 5 && significance(Particle.Z_BOSON) >= 5;
            case LEPTON_COLLIDER -> significance(Particle.BOTTOM) >= 5;
            case HEAVY_IONS -> significance(Particle.TOP) >= 5;
            case NEUTRONIUM_MAGNET -> nexiumWire && significance(Particle.HIGGS) >= 5;
            case BEYOND_STANDARD_MODEL -> significance(Particle.X_NEXUS) >= 3;
        };
    }

    private void complete(Proposal p) {
        proposalsDone[p.ordinal()] = true;
        proposalProgress = 0;
        switch (p) {
            case NB3SN_MAGNET -> magnetTier = Math.max(magnetTier, 1);
            case STOCHASTIC_COOLING -> bunches = Math.max(bunches, 1000);
            case CRYO_PENNING -> trapTier = Math.max(trapTier, 3);
            case REBCO_MAGNET -> magnetTier = Math.max(magnetTier, 2);
            case LEPTON_COLLIDER -> electronMode = true;
            case HEAVY_IONS -> heavyIonMode = true;
            case NEUTRONIUM_MAGNET -> magnetTier = Math.max(magnetTier, 3);
            case BEYOND_STANDARD_MODEL -> magnetTier = 4;
            case VERTEX_DETECTOR -> beamSizeMicron = Math.min(beamSizeMicron, 16);
        }
        activeProposal = null;
        for (Proposal next : Proposal.values()) {
            if (!proposalsDone[next.ordinal()]) {
                activeProposal = next;
                break;
            }
        }
    }

    // ------------------------------------------------------------------ persistence

    public double[] pack() {
        int done = 0;
        for (int i = 0; i < proposalsDone.length; i++) if (proposalsDone[i]) done |= 1 << i;
        double[] head = { mode.ordinal(), magnetTier, bunches, protonsPerBunch, beamSizeMicron, trapTier, antiprotons,
                rampSeconds, heliumLevel, quenchCooldown, damage, done,
                activeProposal == null ? -1 : activeProposal.ordinal(), proposalProgress, electronMode ? 1 : 0,
                heavyIonMode ? 1 : 0 };
        double[] out = Arrays.copyOf(head, head.length + integrated.length);
        System.arraycopy(integrated, 0, out, head.length, integrated.length);
        return out;
    }

    public void unpack(double[] v) {
        if (v == null || v.length < 16) return;
        mode = Mode.values()[(int) v[0]];
        magnetTier = (int) v[1];
        bunches = (int) v[2];
        protonsPerBunch = v[3];
        beamSizeMicron = v[4];
        trapTier = (int) v[5];
        antiprotons = v[6];
        rampSeconds = v[7];
        heliumLevel = v[8];
        quenchCooldown = (int) v[9];
        damage = v[10];
        for (int i = 0; i < proposalsDone.length; i++) proposalsDone[i] = ((int) v[11] & 1 << i) != 0;
        activeProposal = v[12] < 0 ? null : Proposal.values()[(int) v[12]];
        proposalProgress = v[13];
        electronMode = v[14] != 0;
        heavyIonMode = v[15] != 0;
        for (int i = 0; i < integrated.length && 16 + i < v.length; i++) integrated[i] = v[16 + i];
    }
}
