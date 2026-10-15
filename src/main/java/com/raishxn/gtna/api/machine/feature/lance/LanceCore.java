package com.raishxn.gtna.api.machine.feature.lance;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/**
 * Shot physics, aim, barrel and progression (survey + barrel bench) of the Kinetic Orbital Lance (original GTNA,
 * UEV). Plain Java, unit-tested by {@code LanceCoreTest}; design in
 * {@code docs/roadmap/design/lanca-cinetica-orbital.md}.
 */
public final class LanceCore {

    public static final double J_PER_EU = 1000;          // 1 EU = 1 kJ inside the machine
    public static final double C = 2.998e8;
    public static final double TARGET_RADIUS = 5000;     // m
    public static final double BARREL_HEAT_CAPACITY = 2e9; // EU per K

    /** Target bodies: distance (Mm), hardness (MJ/kg), characteristic survey mass (kg), parents. */
    public enum Body {

        MOON(384, 2.0, 1e6),
        PHOBOS(78, 1.2, 2e6, MOON),
        VESTA(1.7e5, 3.5, 8e6, PHOBOS),
        CERES(4.1e5, 1.5, 8e6, PHOBOS),
        PSYCHE(3.7e5, 6.0, 5e7, VESTA),
        EUROPA(6.3e5, 2.8, 5e7, CERES),
        ARROKOTH(6.6e6, 0.9, 2e8, EUROPA),
        NEXUS_1(7.5e6, 9.5, 1e9, PSYCHE, ARROKOTH);

        public final double distanceMm, hardnessMJ, surveyMass;
        public final Body[] parents;

        Body(double distanceMm, double hardnessMJ, double surveyMass, Body... parents) {
            this.distanceMm = distanceMm;
            this.hardnessMJ = hardnessMJ;
            this.surveyMass = surveyMass;
            this.parents = parents;
        }
    }

    public enum Projectile {

        TUNGSTEN(50),
        TUNGSTEN_CARBIDE(80),
        OSMIRIDIUM(120),
        NEUTRONIUM(400),
        DEGENERATE(1200);

        public final double mass;

        Projectile(double mass) {
            this.mass = mass;
        }
    }

    public enum Regime {
        FRAGMENTATION,
        IMPACT_MELT,
        VAPORISATION,
        RELATIVISTIC
    }

    /** Bench components: slot, efficiency, mass (t), heat, unlocked by the mother lode of a body. */
    public enum Component {

        RAIL_CU_NB(Slot.RAIL, 0.02, 40, 3, null),
        RAIL_SUPERCONDUCTOR(Slot.RAIL, 0.04, 60, 1, Body.PHOBOS),
        RAIL_GRAPHENE(Slot.RAIL, 0.07, 140, 2, Body.PSYCHE),
        COOLING_HELIUM(Slot.COOLING, 2, 30, -10, Body.CERES),
        COOLING_SUPERCONDUCTOR(Slot.COOLING, 4, 60, -25, Body.EUROPA),
        COOLING_PLASMA_ICE(Slot.COOLING, 8, 90, -60, Body.ARROKOTH),
        SENSOR_TELESCOPE(Slot.SENSOR, 0.7, 10, 2, Body.MOON),
        SENSOR_INTERFEROMETER(Slot.SENSOR, 0.35, 40, 2, Body.EUROPA),
        SENSOR_LENS(Slot.SENSOR, 0.175, 80, 2, Body.ARROKOTH),
        CAPSULE_ABLATIVE(Slot.CAPSULE, 0.75, 0, 0, Body.CERES),
        CAPSULE_MAGNETIC(Slot.CAPSULE, 0.85, 0, 0, Body.PSYCHE),
        CAPSULE_FOLD(Slot.CAPSULE, 0.95, 0, 0, Body.NEXUS_1),
        SALVO_SPLITTER(Slot.SALVO, 2, 50, 5, Body.VESTA);

        public final Slot slot;
        public final double value, mass, heat;
        public final Body unlock;

        Component(Slot slot, double value, double mass, double heat, Body unlock) {
            this.slot = slot;
            this.value = value;
            this.mass = mass;
            this.heat = heat;
            this.unlock = unlock;
        }
    }

    public enum Slot {
        RAIL,
        COOLING,
        SENSOR,
        CAPSULE,
        SALVO
    }

    // ------------------------------------------------------------------ state
    public final double[] recovered = new double[Body.values().length];   // kg recovered per body
    public final List<Component> fitted = new ArrayList<>();             // bench loadout
    public int capacitorRings = 1;
    public double bankCharge;                                            // EU
    public double barrelTemperature = 300;                               // K
    public double linerWear;                                             // 0..1
    public double linerLife = 5e13;                                      // EU of a tungsten carbide liner

    // ------------------------------------------------------------------ survey and map

    public double survey(Body b) {
        return 1 - Math.exp(-recovered[b.ordinal()] / b.surveyMass);
    }

    /** A body is targetable when every parent is surveyed to 100% (99% counts). */
    public boolean targetable(Body b) {
        for (Body p : b.parents) if (survey(p) < 0.99) return false;
        return true;
    }

    public boolean unlocked(Component c) {
        return c.unlock == null || survey(c.unlock) >= 0.99;
    }

    // ------------------------------------------------------------------ bench

    public double bankCapacity() {
        return 4e12 * Math.pow(2, capacitorRings - 1);
    }

    public double massBudget() {
        return 600 + 200 * capacitorRings;
    }

    public double heatBudget() {
        return 40 + 20 * capacitorRings;
    }

    public double totalMass() {
        return fitted.stream().mapToDouble(c -> c.mass).sum();
    }

    public double totalHeat() {
        return fitted.stream().mapToDouble(c -> c.heat).sum();
    }

    /** Inductance share: each rail adds 1/8 of the bank limit. */
    public double inductance() {
        return fitted.stream().filter(c -> c.slot == Slot.RAIL).count() / 8.0;
    }

    public boolean benchValid() {
        return totalMass() <= massBudget() && totalHeat() <= heatBudget() && inductance() <= 1 &&
                fitted.stream().allMatch(this::unlocked) &&
                Arrays.stream(Slot.values()).filter(s -> s != Slot.RAIL)
                        .allMatch(s -> fitted.stream().filter(c -> c.slot == s).count() <= 1);
    }

    public double efficiency() {
        double sum = fitted.stream().filter(c -> c.slot == Slot.RAIL).mapToDouble(c -> c.value).sum();
        return Math.min(0.85, 0.35 + sum * (1 - 0.5 * inductance()));
    }

    private double best(Slot slot, double fallback) {
        return fitted.stream().filter(c -> c.slot == slot).mapToDouble(c -> c.value).findFirst().orElse(fallback);
    }

    public double aimFactor() {
        return best(Slot.SENSOR, 1);
    }

    public double recovery() {
        return best(Slot.CAPSULE, 0.6);
    }

    public int salvo() {
        return (int) best(Slot.SALVO, 1);
    }

    public double barrelHeatCapacity() {
        return BARREL_HEAT_CAPACITY * best(Slot.COOLING, 1);
    }

    // ------------------------------------------------------------------ the shot

    /** Pointing error (rad) and accuracy against the body. */
    public double accuracy(Body b, double cwu) {
        double theta = 1e-9 * aimFactor() / Math.sqrt(Math.max(cwu, 1) / 1000) +
                2e-10 * Math.max(0, barrelTemperature - 300) / 100;
        return Math.max(0, 1 - b.distanceMm * 1e6 * theta / TARGET_RADIUS);
    }

    public static Regime regime(double specificEnergy, Body b) {
        double h = b.hardnessMJ * 1e6;
        if (specificEnergy >= 5000 * h) return Regime.RELATIVISTIC;
        if (specificEnergy >= 200 * h) return Regime.VAPORISATION;
        if (specificEnergy >= 10 * h) return Regime.IMPACT_MELT;
        return Regime.FRAGMENTATION;
    }

    public static final class Shot {

        public boolean fired, misfire;
        public double velocity, beta, recoveredKg, returnSeconds;
        public Regime regime;
    }

    /** Fires the whole bank at {@code b}. */
    public Shot fire(Body b, Projectile p, double cwu) {
        Shot s = new Shot();
        if (!targetable(b) || !benchValid() || bankCharge <= 0) return s;
        double energy = bankCharge;
        bankCharge = 0;
        s.fired = true;
        double eta = efficiency();
        linerWear += energy / linerLife;
        barrelTemperature += (1 - eta) * energy / barrelHeatCapacity();
        if (linerWear >= 1 || barrelTemperature > 2500) {
            s.misfire = true;
            linerWear = 1;
            barrelTemperature += 400;
            return s;
        }
        int n = salvo();
        double perShot = energy / n;
        double specific = eta * perShot * J_PER_EU / p.mass;
        s.velocity = Math.sqrt(2 * specific);
        s.beta = s.velocity / C;
        s.regime = regime(specific, b);
        double fragmented = 0.2 * eta * perShot * J_PER_EU / (b.hardnessMJ * 1e6) * n;
        s.recoveredKg = fragmented * recovery() * accuracy(b, cwu);
        recovered[b.ordinal()] += s.recoveredKg;
        s.returnSeconds = 2 * b.distanceMm * 1e6 / 30000 / 600;
        return s;
    }

    /** Barrel cooling per second. */
    public void cool(double coolantEU) {
        barrelTemperature = Math.max(300, barrelTemperature - coolantEU / barrelHeatCapacity());
    }

    public void replaceLiner(double life) {
        linerWear = 0;
        linerLife = life;
    }

    // ------------------------------------------------------------------ persistence

    public double[] pack() {
        double[] head = { capacitorRings, bankCharge, barrelTemperature, linerWear, linerLife, fitted.size() };
        double[] out = Arrays.copyOf(head, head.length + recovered.length + fitted.size());
        System.arraycopy(recovered, 0, out, head.length, recovered.length);
        for (int i = 0; i < fitted.size(); i++) out[head.length + recovered.length + i] = fitted.get(i).ordinal();
        return out;
    }

    public void unpack(double[] v) {
        if (v == null || v.length < 6 + recovered.length) return;
        capacitorRings = (int) v[0];
        bankCharge = v[1];
        barrelTemperature = v[2];
        linerWear = v[3];
        linerLife = v[4];
        System.arraycopy(v, 6, recovered, 0, recovered.length);
        fitted.clear();
        for (int i = 0; i < (int) v[5] && 6 + recovered.length + i < v.length; i++)
            fitted.add(Component.values()[(int) v[6 + recovered.length + i]]);
    }
}
