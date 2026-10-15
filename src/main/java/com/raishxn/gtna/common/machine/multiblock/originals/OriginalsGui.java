package com.raishxn.gtna.common.machine.multiblock.originals;

import com.gregtechceu.gtceu.api.gui.fancy.TabsWidget;

import com.lowdragmc.lowdraglib.gui.widget.ImageWidget;
import com.lowdragmc.lowdraglib.gui.widget.Widget;
import com.lowdragmc.lowdraglib.gui.widget.WidgetGroup;

import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.network.chat.Component;
import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.api.distmarker.OnlyIn;

import com.raishxn.gtna.api.machine.feature.collider.ColliderCore;
import com.raishxn.gtna.api.machine.feature.lance.LanceCore;
import com.raishxn.gtna.api.machine.feature.stellar.StellarCore;
import com.raishxn.gtna.common.machine.multiblock.godforge.gui.GodforgeGui;
import com.raishxn.gtna.common.machine.multiblock.godforge.gui.GodforgePage;

/**
 * Graphic side tabs of the original multiblocks, on the Forge of Gods star background: the stellar chamber's
 * mass–period diagram, the collider's Standard Model board, the rift's seismograph and the lance's orbital map.
 * Everything is drawn from synced fields, so the server sends nothing extra.
 */
public final class OriginalsGui {

    public static final int W = 200, H = 140;
    private static final int GRID = 0x40FFFFFF, AXIS = 0xA0FFFFFF, CYAN = 0xFF55FFFF, GOLD = 0xFFFFAA00,
            RED = 0xFFFF5555, GREEN = 0xFF55FF55, GREY = 0xFF777777;

    private OriginalsGui() {}

    private static com.lowdragmc.lowdraglib.gui.texture.ResourceTexture texture(String name) {
        return new com.lowdragmc.lowdraglib.gui.texture.ResourceTexture("gtna:textures/gui/originals/" + name + ".png");
    }

    static void attach(TabsWidget tabs, String key, Plot.Painter painter) {
        tabs.attachSubTab(new GodforgePage("gtna.originals.gui." + key, texture("icon_" + key),
                () -> page(key, painter)));
    }

    private static Widget page(String key, Plot.Painter painter) {
        var page = new WidgetGroup(0, 0, W, H);
        // The author's tab art (tools/design/ui_proposals, "clean" variants without baked text).
        page.setBackground(texture("bg_" + key));
        page.addWidget(new ImageWidget(5, 4, W - 10, 10, GodforgeGui.text("gtna.originals.gui." + key, 0xFFAA00)));
        page.addWidget(new Plot(6, 18, W - 12, H - 24, painter));
        return page;
    }

    /** A client-side canvas. */
    public static final class Plot extends Widget {

        @FunctionalInterface
        public interface Painter {

            void paint(GuiGraphics g, int x, int y, int w, int h);
        }

        private final Painter painter;

        Plot(int x, int y, int w, int h, Painter painter) {
            super(x, y, w, h);
            this.painter = painter;
        }

        @Override
        @OnlyIn(Dist.CLIENT)
        public void drawInBackground(GuiGraphics g, int mouseX, int mouseY, float partialTicks) {
            super.drawInBackground(g, mouseX, mouseY, partialTicks);
            var p = getPosition();
            var s = getSize();
            // Opaque enough to hide the static guide lines of the background art under the live plot.
            g.fill(p.x, p.y, p.x + s.width, p.y + s.height, 0xC8100820);
            painter.paint(g, p.x, p.y, s.width, s.height);
        }
    }

    // ------------------------------------------------------------------ helpers

    private static void text(GuiGraphics g, String s, int x, int y, int colour) {
        g.drawString(Minecraft.getInstance().font, s, x, y, colour, false);
    }

    private static void text(GuiGraphics g, Component s, int x, int y, int colour) {
        g.drawString(Minecraft.getInstance().font, s, x, y, colour, false);
    }

    private static void dot(GuiGraphics g, int x, int y, int r, int colour) {
        g.fill(x - r, y - r, x + r + 1, y + r + 1, colour);
    }

    private static void line(GuiGraphics g, int x0, int y0, int x1, int y1, int colour) {
        int n = Math.max(Math.abs(x1 - x0), Math.abs(y1 - y0));
        for (int i = 0; i <= n; i++) {
            int x = x0 + (n == 0 ? 0 : (x1 - x0) * i / n), y = y0 + (n == 0 ? 0 : (y1 - y0) * i / n);
            g.fill(x, y, x + 1, y + 1, colour);
        }
    }

    /** A rolling history sampled on the client, for trails and traces. */
    static final class Trace {

        final double[] a, b;
        int head, size;
        long last;

        Trace(int n) {
            a = new double[n];
            b = new double[n];
        }

        void sample(double x, double y, long everyMs) {
            long now = net.minecraft.Util.getMillis();
            if (size > 0 && now - last < everyMs) return;
            last = now;
            a[head] = x;
            b[head] = y;
            head = (head + 1) % a.length;
            size = Math.min(size + 1, a.length);
        }

        /** i = 0 is the oldest sample. */
        double x(int i) {
            return a[(head - size + i + a.length) % a.length];
        }

        double y(int i) {
            return b[(head - size + i + b.length) % b.length];
        }
    }

    // ------------------------------------------------------------------ stellar: mass–period diagram

    static Plot.Painter massPeriod(StellarChamberMachine m) {
        var trail = new Trace(120);
        return (g, x, y, w, h) -> {
            // log period 0.5 ms .. 1 s on X, mass 1.0 .. 2.6 M☉ on Y.
            double lo = Math.log10(5e-4), hi = 0;
            int left = x + 22, bottom = y + h - 12, pw = w - 26, ph = h - 16;
            for (double mm = 1.2; mm <= 2.6; mm += 0.2) {
                int yy = bottom - (int) ((mm - 1) / 1.6 * ph);
                g.fill(left, yy, left + pw, yy + 1, GRID);
                text(g, String.format("%.1f", mm), x, yy - 4, AXIS);
            }
            int tov = bottom - (int) ((StellarCore.TOV - 1) / 1.6 * ph);
            g.fill(left, tov, left + pw, tov + 1, RED);
            text(g, "TOV", left + pw - 18, tov - 9, RED);
            // Kepler break-up: the shortest period a neutron star of this mass survives (~0.7 ms at 1.4 M☉).
            int px = -1, py = -1;
            for (int i = 0; i <= pw; i += 2) {
                double mm = 1 + 1.6 * i / pw;
                double p = 7e-4 * Math.sqrt(1.4 / mm);
                int xx = left + (int) ((Math.log10(p) - lo) / (hi - lo) * pw);
                int yy = bottom - (int) ((mm - 1) / 1.6 * ph);
                if (px >= 0) line(g, px, py, xx, yy, GOLD);
                px = xx;
                py = yy;
            }
            text(g, "P (s)", left + pw - 24, bottom + 3, AXIS);
            text(g, "M☉", x, y, AXIS);
            trail.sample(m.renderPeriod(), m.renderMass(), 500);
            for (int i = 0; i < trail.size; i++) {
                int xx = left + (int) ((Math.log10(Math.max(5e-4, trail.x(i))) - lo) / (hi - lo) * pw);
                int yy = bottom - (int) ((Math.min(2.6, trail.y(i)) - 1) / 1.6 * ph);
                int alpha = 40 + 200 * i / Math.max(1, trail.size);
                g.fill(xx, yy, xx + 1, yy + 1, (alpha << 24) | 0x55FFFF);
            }
            if (trail.size > 0) {
                int xx = left + (int) ((Math.log10(Math.max(5e-4, m.renderPeriod())) - lo) / (hi - lo) * pw);
                int yy = bottom - (int) ((Math.min(2.6, m.renderMass()) - 1) / 1.6 * ph);
                dot(g, xx, yy, 2, m.isBlackHole() ? 0xFFAA55FF : m.isMagnetar() ? GOLD : CYAN);
            }
        };
    }

    // ------------------------------------------------------------------ collider: Standard Model board

    static Plot.Painter standardModel(ColliderRingMachine m) {
        return (g, x, y, w, h) -> {
            var particles = ColliderCore.Particle.values();
            int cols = 5, cw = w / cols, chh = (h - 4) / 2;
            for (int i = 0; i < particles.length; i++) {
                int cx = x + (i % cols) * cw + 2, cy = y + (i / cols) * chh + 2;
                double z = m.significance(i);
                int colour = z >= 5 ? GREEN : z >= 3 ? GOLD : GREY;
                g.fill(cx, cy, cx + cw - 4, cy + chh - 4, (colour & 0x00FFFFFF) | 0x30000000);
                g.renderOutline(cx, cy, cw - 4, chh - 4, colour);
                text(g, Component.translatable("gtna.machine.antimatter_collider_ring.particle." +
                        particles[i].name().toLowerCase()), cx + 2, cy + 2, 0xFFFFFFFF);
                text(g, String.format("%.0f GeV", particles[i].thresholdGeV), cx + 2, cy + 13, AXIS);
                int bar = (int) (Math.min(5, z) / 5 * (cw - 8));
                g.fill(cx + 2, cy + chh - 14, cx + 2 + bar, cy + chh - 10, colour);
                text(g, String.format("%.1fσ", z), cx + 2, cy + chh - 24, colour);
            }
        };
    }

    // ------------------------------------------------------------------ rift: seismograph

    static Plot.Painter seismograph(RiftGateMachine m) {
        var trace = new Trace(160);
        return (g, x, y, w, h) -> {
            trace.sample(m.stability(), m.resonance(), 250);
            int mid = y + h / 2;
            for (int k = 1; k < 4; k++) g.fill(x, y + h * k / 4, x + w, y + h * k / 4 + 1, GRID);
            long t = net.minecraft.Util.getMillis();
            int px = -1, py = -1;
            for (int i = 0; i < trace.size; i++) {
                int xx = x + (int) ((double) i / (trace.a.length - 1) * (w - 1));
                double instability = 1 - Math.max(0, Math.min(100, trace.x(i))) / 100;
                double wiggle = Math.sin(i * 1.7 + t / 90.0) * Math.sin(i * 0.31);
                int yy = mid - (int) (wiggle * instability * (h / 2 - 4));
                if (px >= 0) line(g, px, py, xx, yy, m.isRiftOpen() ? CYAN : GREY);
                px = xx;
                py = yy;
            }
            int bar = (int) (Math.max(0, Math.min(1, m.resonance())) * (w - 60));
            text(g, "Ψ", x + 2, y + h - 10, GOLD);
            g.fill(x + 12, y + h - 8, x + 12 + bar, y + h - 4, GOLD);
            text(g, String.format("%.0f%%", m.stability()), x + w - 30, y + 2, m.stability() > 50 ? GREEN : RED);
            text(g, Component.translatable("gtna.machine.dimensional_rift_gate.biome." +
                    m.biome().name().toLowerCase()), x + 2, y + 2, AXIS);
        };
    }

    // ------------------------------------------------------------------ lance: orbital map

    static Plot.Painter orbitalMap(LanceMachine m) {
        return (g, x, y, w, h) -> {
            int cx = x + w / 2, cy = y + h / 2, rMax = Math.min(w, h) / 2 - 6;
            dot(g, cx, cy, 3, 0xFF3399FF);
            var bodies = LanceCore.Body.values();
            double lo = Math.log10(50), hi = Math.log10(1e7);
            long t = net.minecraft.Util.getMillis();
            for (var b : bodies) {
                int r = (int) ((Math.log10(b.distanceMm) - lo) / (hi - lo) * rMax) + 6;
                for (int a = 0; a < 360; a += 6) {
                    double rad = Math.toRadians(a);
                    g.fill(cx + (int) (Math.cos(rad) * r), cy + (int) (Math.sin(rad) * r),
                            cx + (int) (Math.cos(rad) * r) + 1, cy + (int) (Math.sin(rad) * r) + 1, GRID);
                }
                double ang = b.ordinal() * 0.9 + t / (4000.0 * (1 + b.ordinal()));
                int bx = cx + (int) (Math.cos(ang) * r), by = cy + (int) (Math.sin(ang) * r);
                boolean selected = b == m.target();
                int colour = selected ? CYAN : m.isTargetable(b) ? 0xFFDDDDDD : GREY;
                dot(g, bx, by, selected ? 2 : 1, colour);
                if (selected) {
                    line(g, cx, cy, bx, by, 0x8055FFFF);
                    text(g, Component.translatable("gtna.machine.kinetic_orbital_lance.body." +
                            b.name().toLowerCase()), bx + 4, by - 4, CYAN);
                }
            }
            text(g, m.computation() + " CWU/t", x + 2, y + h - 10, m.computation() > 0 ? GREEN : RED);
        };
    }

    // ------------------------------------------------------------------ collider: beam-time committee

    static Plot.Painter committee(ColliderRingMachine m) {
        return (g, x, y, w, h) -> {
            var proposals = ColliderCore.Proposal.values();
            int row = (h - 2) / proposals.length;
            for (int i = 0; i < proposals.length; i++) {
                int yy = y + 1 + i * row;
                boolean done = m.proposalDone(i), active = m.activeProposal() == i;
                int colour = done ? GREEN : active ? GOLD : GREY;
                g.fill(x + 2, yy + 2, x + 8, yy + 8, colour);
                text(g, Component.translatable("gtna.machine.antimatter_collider_ring.proposal." +
                        proposals[i].name().toLowerCase()), x + 12, yy + 1, colour);
                if (active) {
                    int bar = (int) (Math.min(1, m.proposalProgress() / 40) * 50);
                    g.renderOutline(x + w - 54, yy + 2, 52, 6, GOLD);
                    g.fill(x + w - 53, yy + 3, x + w - 53 + bar, yy + 7, GOLD);
                }
            }
        };
    }

    // ------------------------------------------------------------------ rift: constellation atlas

    static Plot.Painter atlas(RiftGateMachine m) {
        return (g, x, y, w, h) -> {
            // Harmonics as a chord wheel: collected ones lit, the loaded score joined by lines.
            var harmonics = com.raishxn.gtna.api.machine.feature.rift.RiftCore.Harmonic.values();
            int cx = x + 40, cy = y + h / 2, r = Math.min(36, h / 2 - 8);
            int[][] pts = new int[harmonics.length][];
            for (int i = 0; i < harmonics.length; i++) {
                double a = 2 * Math.PI * i / harmonics.length - Math.PI / 2;
                pts[i] = new int[] { cx + (int) (Math.cos(a) * r), cy + (int) (Math.sin(a) * r) };
            }
            int prev = -1;
            for (int i = 0; i < harmonics.length; i++) {
                if (!m.harmonicLoaded(harmonics[i])) continue;
                if (prev >= 0) line(g, pts[prev][0], pts[prev][1], pts[i][0], pts[i][1], 0xA055FFFF);
                prev = i;
            }
            for (int i = 0; i < harmonics.length; i++) {
                var hm = harmonics[i];
                int colour = m.harmonicLoaded(hm) ? CYAN : m.harmonicCollected(hm) ? 0xFFDDDDDD : GREY;
                dot(g, pts[i][0], pts[i][1], 2, colour);
                text(g, hm.p + ":" + hm.q, pts[i][0] - 8, pts[i][1] + 4, colour);
            }
            // Charted rifts as stars: position from the seed, size from depth, brightness from resonance.
            int ax = x + 86, aw = w - 90;
            g.renderOutline(ax, y + 2, aw, h - 14, GRID);
            long[] atlas = m.atlas();
            for (int i = 0; i + 2 < atlas.length; i += 3) {
                long seed = atlas[i];
                int sx = ax + 2 + (int) Math.floorMod(seed, (long) Math.max(1, aw - 4));
                int sy = y + 4 + (int) Math.floorMod(seed >>> 20, (long) Math.max(1, h - 18));
                int bright = 80 + (int) Math.min(175, atlas[i + 2] / 6);
                dot(g, sx, sy, (int) Math.min(2, atlas[i + 1] / 4), 0xFF000000 | bright << 16 | bright << 8 | 255);
            }
            text(g, Component.translatable("gtna.machine.dimensional_rift_gate.atlas", m.atlasSize()), ax,
                    y + h - 10, AXIS);
        };
    }

    // ------------------------------------------------------------------ lance: workbench

    static Plot.Painter bench(LanceMachine m) {
        return (g, x, y, w, h) -> {
            double[] b = m.bench();
            String[] names = { "kg", "MJ", "L" };
            double[][] bars = { { b[0], b[1] }, { b[2], b[3] }, { b[4], 1 } };
            for (int i = 0; i < 3; i++) {
                int yy = y + 2 + i * 12;
                double share = bars[i][1] <= 0 ? 0 : bars[i][0] / bars[i][1];
                int colour = share > 1 ? RED : share > 0.85 ? GOLD : GREEN;
                text(g, names[i], x + 2, yy, AXIS);
                g.renderOutline(x + 20, yy, w - 70, 8, GRID);
                g.fill(x + 21, yy + 1, x + 21 + (int) (Math.min(1, share) * (w - 72)), yy + 7, colour);
                text(g, String.format("%.0f%%", share * 100), x + w - 44, yy, colour);
            }
            int yy = y + 40, col = 0;
            for (var c : LanceCore.Component.values()) {
                int n = m.fitted(c);
                int cx = x + 2 + col * (w / 2);
                text(g, (n > 0 ? "▣ " : "□ ") + c.name().toLowerCase() + (n > 1 ? " ×" + n : ""), cx, yy,
                        n > 0 ? CYAN : GREY);
                if (++col == 2) {
                    col = 0;
                    yy += 10;
                }
            }
            text(g, Component.translatable("gtna.machine.kinetic_orbital_lance." +
                    (m.benchValid() ? "bench_ok" : "bench_invalid")), x + 2, y + h - 10,
                    m.benchValid() ? GREEN : RED);
        };
    }

    // ------------------------------------------------------------------ stellar: seismogram

    static Plot.Painter quakes(StellarChamberMachine m) {
        return (g, x, y, w, h) -> {
            if (!m.hasSeismicProbe()) {
                text(g, Component.translatable("gtna.originals.gui.no_probe"), x + 4, y + h / 2 - 4, RED);
                return;
            }
            double[] q = m.quakes();
            int n = q.length / 2, mid = y + h / 2 + 4;
            g.fill(x, mid, x + w, mid + 1, GRID);
            var kinds = StellarCore.Quake.values();
            for (int i = 0; i < n; i++) {
                int xx = x + 4 + i * (w - 8) / 64;
                int amp = (int) Math.min(h / 2 - 6, 4 + q[i * 2] * (h / 2 - 6));
                int kind = (int) q[i * 2 + 1];
                int colour = kind == StellarCore.Quake.ANTI.ordinal() ? 0xFFAA55FF : kind == 0 ? CYAN : GOLD;
                line(g, xx, mid - amp, xx, mid + amp, colour);
            }
            if (n > 0) text(g, kinds[(int) q[n * 2 - 1]].name().toLowerCase(), x + 2, y + 2, AXIS);
        };
    }
}
