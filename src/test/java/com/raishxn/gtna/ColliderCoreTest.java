package com.raishxn.gtna;

import com.raishxn.gtna.api.machine.feature.collider.ColliderCore;
import com.raishxn.gtna.api.machine.feature.collider.ColliderCore.Particle;
import com.raishxn.gtna.api.machine.feature.collider.ColliderCore.Proposal;

/** Antimatter Collider Ring physics against docs/roadmap/design/anel-colisor.md. */
public final class ColliderCoreTest {

    private ColliderCoreTest() {}

    public static void main(String[] args) {
        rigidity();
        discovery();
        quench();
        penning();
        proposals();
        nexiumDipoles();
        electrons();
        persistence();
        System.out.println("[ColliderCoreTest] all cases passed");
    }

    private static void rigidity() {
        var ring = new ColliderCore();
        near(ring.maxBeamEnergyTeV(), 7.47, 0.01, "NbTi max beam energy");
        ring.magnetTier = 4;
        near(ring.maxBeamEnergyTeV(), 108, 0.01, "infinity magnet max beam energy");
    }

    private static void discovery() {
        var ring = new ColliderCore();
        check(ring.yieldOf(Particle.CHARM) == 0.1, "undiscovered yield 10%");
        ring.integrated[Particle.CHARM.ordinal()] = 9.0 / 16;
        near(ring.significance(Particle.CHARM), 3, 1e-9, "3 sigma at 9 / s^2");
        check(ring.yieldOf(Particle.CHARM) == 0.4, "evidence yield 40%");
        ring.integrated[Particle.CHARM.ordinal()] = 25.0 / 16;
        check(ring.yieldOf(Particle.CHARM) == 1, "discovery yield 100%");
    }

    private static void quench() {
        var ring = new ColliderCore();
        var r = ring.step(0.5, true);
        check(r.quench && ring.quenchCooldown > 0, "missing helium quenches the magnets");
        for (int i = 0; i < 200; i++) ring.step(1, true);
        check(ring.quenchCooldown == 0 && ring.rampSeconds > 0, "the ring recovers and ramps again");
    }

    private static void penning() {
        var ring = new ColliderCore();
        for (int i = 0; i < 100; i++) ring.step(1, true);
        check(ring.antiprotons > 0 && ring.antiprotons <= ring.trapCapacity(), "production fills the traps");
        var r = ring.step(1, false);
        check(r.annihilation && ring.antiprotons == 0 && ring.damage > 0, "unpowered traps annihilate");
    }

    private static void proposals() {
        var ring = new ColliderCore();
        ring.mode = ColliderCore.Mode.PHYSICS;
        check(ring.activeProposal == Proposal.NB3SN_MAGNET, "first proposal is the Nb3Sn magnet");
        boolean done = false;
        for (int i = 0; i < 20_000 && !done; i++) done = ring.step(1, true).proposalFinished;
        check(done && ring.magnetTier == 1, "the Nb3Sn proposal upgrades the magnets");
        check(ring.integrated[Particle.ANTIPROTON.ordinal()] > 0, "physics runs integrate luminosity");
    }

    private static void persistence() {
        var ring = new ColliderCore();
        ring.magnetTier = 2;
        ring.integrated[Particle.HIGGS.ordinal()] = 123;
        ring.proposalsDone[Proposal.VERTEX_DETECTOR.ordinal()] = true;
        var copy = new ColliderCore();
        copy.unpack(ring.pack());
        check(copy.magnetTier == 2 && copy.integrated[Particle.HIGGS.ordinal()] == 123 &&
                copy.proposalsDone[Proposal.VERTEX_DETECTOR.ordinal()], "state survives save");
    }

    private static void electrons() {
        var ring = new ColliderCore();
        ring.magnetTier = 2;
        ring.proposalsDone[ColliderCore.Proposal.LEPTON_COLLIDER.ordinal()] = true;
        check(ring.electronsUnlocked() && !ring.electronMode, "e+e- proposal unlocks electron beams, off by default");
        ring.electronMode = true;
        ring.mode = ColliderCore.Mode.PHYSICS;
        ring.activeProposal = null;
        boolean quenched = false;
        for (int i = 0; i < 60; i++) quenched |= ring.step(1, true).quench;
        check(!quenched && ring.centreOfMassGeV() <= 200, "electron beams run at 100 GeV without quenching");
        check(ring.integrated[ColliderCore.Particle.Z_BOSON.ordinal()] > 0 &&
                ring.integrated[ColliderCore.Particle.HIGGS.ordinal()] == 0, "Z reachable, Higgs above the e+e- cap");
        ring.electronMode = false;
        for (int i = 0; i < 25; i++) ring.step(1, true);
        check(ring.centreOfMassGeV() > 200, "proton beams ramp past the electron cap again");
    }

    private static void near(double v, double e, double rel, String what) {
        check(Math.abs(v - e) <= Math.abs(e) * rel, what + ": " + v + " vs " + e);
    }

    private static void nexiumDipoles() {
        var ring = new ColliderCore();
        ring.activeProposal = Proposal.NEUTRONIUM_MAGNET;
        ring.integrated[ColliderCore.Particle.HIGGS.ordinal()] = 1e9;
        boolean higgs = ring.significance(ColliderCore.Particle.HIGGS) >= 5;
        check(higgs && !ring.proposalMet(Proposal.NEUTRONIUM_MAGNET), "Higgs alone does not wind the dipoles");
        ring.nexiumWire = true;
        check(ring.proposalMet(Proposal.NEUTRONIUM_MAGNET), "Higgs plus Nexium wire closes the proposal");
    }

    private static void check(boolean ok, String what) {
        if (!ok) throw new AssertionError(what);
    }
}
