package com.raishxn.gtna.common.machine.multiblock.originals.ui;

import com.lowdragmc.lowdraglib.gui.modular.ModularUI;
import com.lowdragmc.lowdraglib.gui.widget.WidgetGroup;

import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.world.entity.player.Player;

import com.raishxn.gtna.api.machine.feature.stellar.StellarCore;
import com.raishxn.gtna.common.machine.multiblock.originals.StellarChamberMachine;

import static com.raishxn.gtna.common.machine.multiblock.originals.ui.LanceScreen.act;
import static com.raishxn.gtna.common.machine.multiblock.originals.ui.LanceScreen.tr;
import static com.raishxn.gtna.common.machine.multiblock.originals.ui.OriginalScreen.*;

/** Stellar Containment Chamber screen (UI v2): star display, Mass-Period and Seismogram panels, field manual. */
public final class StellarScreen {

    private static final Theme T = STELLAR;

    private StellarScreen() {}

    public static ModularUI create(StellarChamberMachine m, Player player) {
        Nav nav = new Nav();
        var root = window(T, m, player, (g, x, y) -> display(g, m, x, y), (g, x, y) -> {
            chip(g, x, y, 52, tr("star"), m.isStarRunning() ? 0xFFFFECA0 : T.dim());
            chip(g, x + 56, y, 52, tr("probe"), m.hasSeismicProbe() ? GREEN : T.dim());
            chip(g, x + 112, y, 50, "NEXUS", VIOLET);
        });
        root.addWidget(gridButton(T, 0, "minus", "less", () -> false, click -> act(m, "sp_sub", click)));
        root.addWidget(gridButton(T, 1, "plus", "more", () -> false, click -> act(m, "sp_add", click)));
        root.addWidget(gridButton(T, 2, "bolt", "magnetar", m::isMagnetar, click -> act(m, "magnetar", click)));
        root.addWidget(gridButton(T, 3, "chart", "mass_period", () -> "mp".equals(nav.open), c -> nav.toggle("mp")));
        root.addWidget(gridButton(T, 4, "wave", "seismo", () -> "quakes".equals(nav.open),
                c -> nav.toggle("quakes")));
        root.addWidget(gridButton(T, 5, "star", "star", m::isStarRunning, c -> {}));
        root.addWidget(gridButton(T, 6, "info", "info", () -> "manual".equals(nav.open), c -> nav.toggle("manual")));
        root.addWidget(powerButton(T, 7, m));
        root.addWidget(massPeriod(m, nav));
        root.addWidget(seismogram(m, nav));
        root.addWidget(manual(nav, "stellar_containment_chamber"));
        return ui(root, m, player);
    }

    static double v(StellarChamberMachine m, int i) {
        double[] view = m.view();
        return i < view.length ? view[i] : 0;
    }

    private static void display(GuiGraphics g, StellarChamberMachine m, int x, int y) {
        int cx = x + 48, cy = y + 52;
        boolean lit = m.isStarRunning(), hole = m.isBlackHole();
        if (lit && !hole) for (int k = -40; k <= 40; k++)
            if (Math.abs(k) > 8) px(g, cx + (int) Math.round(k * 0.6), cy - k, 0xFFB4D2FF);
        if (hole) {
            glow(g, cx, cy, 20, 0xFF8A4AD0, 0.7);
            disc(g, cx, cy, 8, 0xFF000000);
            ellipse(g, cx, cy, 10, 10, 0xFFE0C8FF, 0);
        } else {
            glow(g, cx, cy, 22, lit ? 0xFF3C78E6 : 0xFF1C2440, 0.7);
            glow(g, cx, cy, 14, lit ? 0xFF96C8FF : 0xFF2A3450, 0.9);
            disc(g, cx, cy, 7, lit ? 0xFFECF6FF : 0xFF3A4460);
        }
        ellipse(g, cx, cy, 28, 6, lit ? 0xFFFF963C : 0xFF4A3420, 0);
        int x0 = x + 100, w = 186;
        String state = hole ? tr("black_hole") : m.renderPeriod() < 0.01 ? tr("ms_pulsar") : tr("pulsar");
        text(g, state, x0, y + 4, T.glow(), true);
        right(g, lit ? tr("lit") : tr("dark"), x + 286, y + 4, lit ? GREEN : T.dim());
        text(g, String.format("M %.3f  P %.2fms  Pk %.2fms", m.renderMass(), m.renderPeriod() * 1000,
                StellarCore.keplerPeriod(m.renderMass()) * 1000), x0, y + 14, T.dim(), false);
        double cap = v(m, 2);
        int sp = (int) v(m, 1);
        bar(g, T, x0, y + 25, w, tr("extraction"), "2^" + sp + " EU/t",
                cap > 0 ? Math.min(1, Math.pow(2, sp) / cap) : 0, T.accent());
        bar(g, T, x0, y + 42, w, tr("crust_stress"), String.format("%.2f", v(m, 0)), v(m, 0), 0xFFFFC85A);
        bar(g, T, x0, y + 59, w, tr("damage"), String.format("%.1f%%", m.damage()), m.damage() / 100, RED);
        bar(g, T, x0, y + 76, w, tr("band_tier"), m.bandTier() + " / 4", m.bandTier() / 4.0, 0xFFAA82FF);
        text(g, tr("output") + " " + sci(m.output()) + " EU/t", x0, y + 95, T.dim(), false);
    }

    // ------------------------------------------------------------------ mass-period diagram

    private static WidgetGroup massPeriod(StellarChamberMachine m, Nav nav) {
        return panel(T, nav, "mp", "mass_period_title", (g, x, y) -> {
            int x0 = x + 30, y0 = y + 20, w = 250, h = 110;
            g.fill(x0, y0, x0 + w, y0 + h, 0xFF06080F);
            // Mass 1.0..2.6 bottom to top; period 0.4..40 ms left to right (log).
            double tov = 2.2;
            int tovY = y0 + (int) (h * (1 - (tov - 1.0) / 1.6));
            for (int yy = y0; yy < tovY; yy++)
                for (int xx = x0; xx < x0 + w; xx += 3) px(g, xx + (yy % 3), yy, 0xFF5A141E);
            g.fill(x0, tovY, x0 + w, tovY + 1, RED);
            right(g, "TOV", x0 + w - 2, tovY - 9, RED);
            for (int k = 0; k <= 160; k++) {
                double mass = 1.0 + k / 100.0;
                double p = StellarCore.keplerPeriod(mass) * 1000;
                int px = x0 + (int) (w * (Math.log10(p) - Math.log10(0.4)) / 2.0);
                int py = y0 + (int) (h * (1 - (mass - 1.0) / 1.6));
                if (px >= x0 && px < x0 + w) px(g, px, py, YELLOW);
            }
            double p = Math.max(0.4, m.renderPeriod() * 1000);
            int sx = x0 + (int) Math.min(w - 1, w * (Math.log10(p) - Math.log10(0.4)) / 2.0);
            int sy = y0 + (int) (h * (1 - (Math.min(2.6, m.renderMass()) - 1.0) / 1.6));
            disc(g, sx, sy, 2, T.glow());
            ellipse(g, sx, sy, 5, 5, T.accent(), 0);
            String[] ticks = { "1.0", "1.4", "1.8", "2.2", "2.6" };
            for (int i = 0; i < ticks.length; i++) right(g, ticks[i], x0 - 3, y0 + h - 4 - i * 27, T.dim());
            centre(g, tr("spin_period"), x0 + w / 2, y0 + h + 3, T.dim());
        });
    }

    // ------------------------------------------------------------------ seismogram

    private static final String[] QUAKES = { "micro", "crab", "vela", "anti", "collapse" };

    private static WidgetGroup seismogram(StellarChamberMachine m, Nav nav) {
        return panel(T, nav, "quakes", "seismo_title", (g, x, y) -> {
            g.fill(x + 10, y + 20, x + 282, y + 74, 0xFF040A08);
            double[] q = m.quakes();
            int n = q.length / 2;
            boolean[] decoded = new boolean[QUAKES.length];
            int prev = -1;
            for (int xx = 12; xx < 280; xx++) {
                double a = 1.2 * Math.sin(xx * 0.9);
                // The last quakes as wave packets spread along the strip, newest on the right.
                for (int i = 0; i < n; i++) {
                    int at = 280 - (n - i) * Math.max(12, 260 / Math.max(1, n));
                    double size = Math.abs(q[i * 2]);
                    double amp = Math.min(24, 4 + Math.log10(size / 1e-10 + 1) * 4);
                    a += amp * Math.exp(-Math.pow((xx - at) / 5.0, 2)) * Math.sin(xx * 1.7);
                }
                int yy = y + 47 + (int) Math.round(a);
                if (prev >= 0) line(g, x + xx - 1, prev, x + xx, yy, GREEN);
                prev = yy;
            }
            for (int i = 0; i < n; i++) {
                int k = (int) q[i * 2 + 1];
                if (k >= 0 && k < decoded.length) decoded[k] = true;
            }
            if (!m.hasSeismicProbe()) centre(g, tr("no_probe"), x + 146, y + 22, RED);
            for (int i = 0; i < QUAKES.length; i++) {
                int yy = y + 80 + i * 12;
                text(g, tr("quake." + QUAKES[i]), x + 12, yy, T.glow(), true);
                text(g, decoded[i] ? tr("decoded") : tr("quake." + QUAKES[i] + ".how"), x + 110, yy,
                        decoded[i] ? GREEN : T.dim(), false);
            }
        });
    }
}
