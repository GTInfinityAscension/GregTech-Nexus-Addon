package com.raishxn.gtna;

import com.raishxn.gtna.api.machine.feature.lance.LanceCore;
import com.raishxn.gtna.api.machine.feature.lance.LanceCore.Body;
import com.raishxn.gtna.api.machine.feature.lance.LanceCore.Component;
import com.raishxn.gtna.api.machine.feature.lance.LanceCore.Projectile;

/** Kinetic Orbital Lance against docs/roadmap/design/lanca-cinetica-orbital.md. */
public final class LanceCoreTest {

    private LanceCoreTest() {}

    public static void main(String[] args) {
        shot();
        aim();
        survey();
        bench();
        barrel();
        persistence();
        System.out.println("[LanceCoreTest] all cases passed");
    }

    private static void shot() {
        var lance = new LanceCore();
        lance.bankCharge = 1e12;
        var s = lance.fire(Body.MOON, Projectile.TUNGSTEN, 1000);
        near(s.velocity / 1000, 3742, 0.01, "tungsten at 1e12 EU, eta 0.35");
        check(s.regime == LanceCore.Regime.RELATIVISTIC || s.regime == LanceCore.Regime.VAPORISATION,
                "7e9 J/kg against the Moon vaporises or better: " + s.regime);
        check(s.recoveredKg > 0 && lance.bankCharge == 0, "the shot recovers mass and empties the bank");
    }

    private static void aim() {
        var lance = new LanceCore();
        near(lance.accuracy(Body.PSYCHE, 1000), 0.926, 0.01, "Psyche accuracy at 1000 CWU");
        check(lance.accuracy(Body.NEXUS_1, 1000) == 0, "Nexus-1 is out of reach without computation");
        lance.barrelTemperature = 900;
        check(lance.accuracy(Body.PSYCHE, 16000) < lance.accuracy(Body.PSYCHE, 1000) + 1, "hot barrel drifts");
    }

    private static void survey() {
        var lance = new LanceCore();
        check(lance.targetable(Body.MOON) && !lance.targetable(Body.PHOBOS), "only the Moon at the start");
        lance.recovered[Body.MOON.ordinal()] = Body.MOON.surveyMass * Math.log(100);
        check(lance.survey(Body.MOON) >= 0.99 && lance.targetable(Body.PHOBOS), "a full Moon survey opens Phobos");
        check(!lance.targetable(Body.NEXUS_1), "Nexus-1 needs Psyche and Arrokoth");
    }

    private static void bench() {
        var lance = new LanceCore();
        for (int i = 0; i < 5; i++) lance.fitted.add(Component.RAIL_CU_NB);
        check(lance.benchValid() && lance.efficiency() > 0.35, "copper rails raise efficiency");
        lance.fitted.add(Component.RAIL_SUPERCONDUCTOR);
        check(!lance.benchValid(), "superconductor rails need the Phobos mother lode");
        lance.fitted.clear();
        for (int i = 0; i < 9; i++) lance.fitted.add(Component.RAIL_CU_NB);
        check(!lance.benchValid(), "nine rails exceed the inductance");
    }

    private static void barrel() {
        var lance = new LanceCore();
        lance.linerLife = 1e12;
        lance.bankCharge = 1e12;
        var s = lance.fire(Body.MOON, Projectile.TUNGSTEN, 1000);
        check(s.misfire && lance.linerWear >= 1, "a worn-out liner misfires");
        lance.replaceLiner(5e13);
        lance.cool(1e15);
        check(lance.linerWear == 0 && lance.barrelTemperature < 1000, "maintenance restores the barrel");
    }

    private static void persistence() {
        var lance = new LanceCore();
        lance.recovered[Body.VESTA.ordinal()] = 123;
        lance.fitted.add(Component.SALVO_SPLITTER);
        lance.capacitorRings = 3;
        var copy = new LanceCore();
        copy.unpack(lance.pack());
        check(copy.recovered[Body.VESTA.ordinal()] == 123 && copy.fitted.get(0) == Component.SALVO_SPLITTER &&
                copy.capacitorRings == 3, "state survives save");
    }

    private static void near(double v, double e, double rel, String what) {
        check(Math.abs(v - e) <= Math.abs(e) * rel, what + ": " + v + " vs " + e);
    }

    private static void check(boolean ok, String what) {
        if (!ok) throw new AssertionError(what);
    }
}
