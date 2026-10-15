package com.raishxn.gtna.common.machine.multiblock.originals.ui;

import com.lowdragmc.lowdraglib.gui.modular.ModularUI;
import com.lowdragmc.lowdraglib.gui.widget.WidgetGroup;

import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.network.chat.Component;
import net.minecraft.world.entity.player.Player;

import com.raishxn.gtna.api.machine.feature.rift.RiftCore;
import com.raishxn.gtna.common.machine.multiblock.originals.RiftGateMachine;

import static com.raishxn.gtna.common.machine.multiblock.originals.ui.LanceScreen.act;
import static com.raishxn.gtna.common.machine.multiblock.originals.ui.LanceScreen.tr;
import static com.raishxn.gtna.common.machine.multiblock.originals.ui.OriginalScreen.*;

/** Dimensional Rift Gate screen (UI v2): vortex and tuning on the display, Chord and Atlas panels, manual. */
public final class RiftScreen {

    private static final Theme T = RIFT;
    private static final String[] AXES = { "f", "p", "a" };

    private RiftScreen() {}

    public static ModularUI create(RiftGateMachine m, Player player) {
        Nav nav = new Nav();
        var root = window(T, m, player, (g, x, y) -> display(g, m, x, y), (g, x, y) -> {
            chip(g, T, x, y, 52, m.isRiftOpen() ? tr("open") : tr("closed"), m.isRiftOpen() ? GREEN : T.dim());
            chip(g, T, x + 56, y, 52, tr("tuning"), T.accent());
        });
        // Knobs: -10, -1, +1, +10 per axis, on the display.
        for (int i = 0; i < 3; i++) {
            int yy = DY + 52 + i * 15;
            String ax = AXES[i];
            root.addWidget(new Plate(T, DX + 100 + 128, yy, 14, 13, "minus", null, () -> false,
                    c -> act(m, ax + "-", c)).tip("gtna.ui.o.step_down"));
            root.addWidget(new Plate(T, DX + 100 + 146, yy, 14, 13, "plus", null, () -> false,
                    c -> act(m, ax + "+", c)).tip("gtna.ui.o.step_up"));
            root.addWidget(new Plate(T, DX + 100 + 164, yy, 22, 13, "right", null, () -> false,
                    c -> act(m, ax + "++", c)).tip("gtna.ui.o.step_big"));
        }
        root.addWidget(gridButton(T, 0, "open", "open_rift", m::isRiftOpen, click -> act(m, "open", click)));
        root.addWidget(gridButton(T, 1, "close", "close_rift", () -> false, click -> act(m, "close", click)));
        root.addWidget(gridButton(T, 2, "note", "chord", () -> "chord".equals(nav.open), c -> nav.toggle("chord")));
        root.addWidget(gridButton(T, 3, "map", "atlas", () -> "atlas".equals(nav.open), c -> nav.toggle("atlas")));
        root.addWidget(gridButton(T, 4, "down", "depth", () -> v(m, 6) > 1, c -> {}));
        root.addWidget(gridButton(T, 5, "wave", "resonant", () -> m.resonance() >= 0.9, c -> {}));
        root.addWidget(gridButton(T, 6, "info", "info", () -> "manual".equals(nav.open), c -> nav.toggle("manual")));
        root.addWidget(powerButton(T, 7, m));
        root.addWidget(chord(m, nav));
        root.addWidget(atlas(m, nav));
        root.addWidget(manual(T, nav, "dimensional_rift_gate"));
        return ui(root, m, player);
    }

    static double v(RiftGateMachine m, int i) {
        double[] view = m.view();
        return i < view.length ? view[i] : 0;
    }

    private static final int[] RINGS = { 0xFF963CDC, 0xFFAA5AF0, 0xFF788CFF, 0xFF5ABEFF, 0xFFDCC8FF };

    private static void display(GuiGraphics g, RiftGateMachine m, int x, int y) {
        int cx = x + 48, cy = y + 52;
        boolean open = m.isRiftOpen();
        double turn = open ? (System.currentTimeMillis() % 6000) / 6000.0 : 0;
        for (int k = 0; k < 5; k++) {
            int r = 34 - k * 6;
            int c = open ? RINGS[k] : dim(RINGS[k], 0.3);
            ellipse(g, cx, cy, r, r, c, k % 2 == 0 ? 0 : 2);
            if (open) {
                double a = turn * 2 * Math.PI * (k % 2 == 0 ? 1 : -1) + k;
                disc(g, (int) Math.round(cx + r * Math.cos(a)), (int) Math.round(cy + r * Math.sin(a)), 1, 0xFFFFFFFF);
            }
        }
        disc(g, cx, cy, 6, 0xFF06000E);
        ellipse(g, cx, cy, 6, 6, open ? 0xFFFFFFFF : T.dim(), 0);
        int x0 = x + 100, w = 186;
        text(g, open ? tr("rift_open") : tr("rift_closed"), x0, y + 4, T.glow(), true);
        if (open) right(g, Component.translatable("gtna.machine.dimensional_rift_gate.biome." +
                m.biome().name().toLowerCase()).getString(), x + 286, y + 4, T.accent());
        bar(g, T, x0, y + 16, w, tr("resonance"), String.format("%.3f", m.resonance()), m.resonance(), T.accent());
        bar(g, T, x0, y + 33, w, tr("stability"), Math.round(m.stability()) + " / 100", m.stability() / 100,
                0xFF6EE696);
        String[] labels = { tr("freq"), tr("phase"), tr("ampl") };
        String[] values = { String.format("%.1f", v(m, 0)), String.format("%.0f", v(m, 1)),
                String.format("%.0f", v(m, 2)) };
        for (int i = 0; i < 3; i++) {
            int yy = y + 52 + i * 15;
            text(g, labels[i], x0, yy + 2, T.dim(), false);
            text(g, values[i], x0 + 34, yy + 2, T.glow(), false);
            double close = v(m, 3 + i);
            int on = (int) Math.round(close * 5);
            for (int k = 0; k < 5; k++) {
                int c = k < on ? (close > 0.8 ? GREEN : close > 0.4 ? YELLOW : RED) : 0xFF3C304C;
                g.fill(x0 + 74 + k * 7, yy + 3, x0 + 79 + k * 7, yy + 9, c);
            }
        }
        text(g, "SpaceTime " + String.format("%.1f", v(m, 8)) + " L/s, " + tr("depth") + " " + (int) v(m, 6) + "/" +
                (int) v(m, 7), x0, y + 97, T.dim(), false);
    }

    // ------------------------------------------------------------------ chord wheel

    private static final int WX = 80, WY = 82, WR = 44;

    private static int hx(int i) {
        return (int) Math.round(WX + WR * Math.cos(-Math.PI / 2 + i * Math.PI / 4));
    }

    private static int hy(int i) {
        return (int) Math.round(WY + WR * Math.sin(-Math.PI / 2 + i * Math.PI / 4));
    }

    private static WidgetGroup chord(RiftGateMachine m, Nav nav) {
        var panel = panel(T, nav, "chord", "chord_title", (g, x, y) -> {
            var hs = RiftCore.Harmonic.values();
            int prev = -1, first = -1;
            for (int i = 0; i < hs.length; i++) {
                if (!m.harmonicLoaded(hs[i])) continue;
                if (prev >= 0) line(g, x + hx(prev), y + hy(prev), x + hx(i), y + hy(i), 0xFF6ED2FF);
                else first = i;
                prev = i;
            }
            if (first >= 0 && prev != first) line(g, x + hx(prev), y + hy(prev), x + hx(first), y + hy(first),
                    0xFF6ED2FF);
            double consonance = 0;
            int loaded = 0, recorded = 0;
            for (int i = 0; i < hs.length; i++) {
                boolean rec = m.harmonicCollected(hs[i]), load = m.harmonicLoaded(hs[i]);
                if (rec) recorded++;
                if (load) {
                    loaded++;
                    consonance += hs[i].consonance();
                }
                disc(g, x + hx(i), y + hy(i), 4, load ? 0xFFFFFFFF : rec ? 0xFF2C2040 : 0xFF140E1E);
                ellipse(g, x + hx(i), y + hy(i), 4, 4, rec ? T.accent() : dim(T.accent(), 0.4), 0);
                String n = hs[i].p + ":" + hs[i].q;
                if (hx(i) >= WX) text(g, n, x + hx(i) + 7, y + hy(i) - 4, rec ? T.glow() : T.dim(), rec);
                else right(g, n, x + hx(i) - 6, y + hy(i) - 4, rec ? T.glow() : T.dim());
            }
            T.tex("card").draw(g, 0, 0, x + 150, y + 18, 138, 128);
            String[][] rows = { { tr("loaded"), loaded + " / 5" },
                    { tr("consonance"), String.format("%.2f", loaded > 0 ? consonance / loaded : 0.3) },
                    { tr("recorded"), recorded + " / 8" }, { tr("max_depth"), String.valueOf((int) v(m, 7)) } };
            for (int i = 0; i < rows.length; i++) {
                text(g, rows[i][0], x + 155, y + 24 + i * 12, T.dim(), false);
                right(g, rows[i][1], x + 284, y + 24 + i * 12, T.glow());
            }
            centre(g, tr("chord_hint1"), x + 219, y + 96, T.dim());
            centre(g, tr("chord_hint2"), x + 219, y + 106, T.dim());
        });
        for (int i = 0; i < 8; i++) {
            final int k = i;
            panel.addWidget(hit(hx(i) - 5, hy(i) - 5, 11, 11, click -> act(m, "h" + k, click)));
        }
        return panel;
    }

    // ------------------------------------------------------------------ seed atlas

    private static WidgetGroup atlas(RiftGateMachine m, Nav nav) {
        var panel = panel(T, nav, "atlas", "atlas_title", (g, x, y) -> {
            long[] a = m.atlas();
            int n = a.length / 3;
            int sel = nav.selected >= 0 && nav.selected < n ? nav.selected : n - 1;
            int px0 = -1, py0 = -1;
            for (int i = 0; i < n; i++) {
                int px = x + atlasX(a[i * 3]), py = y + atlasY(a[i * 3]);
                if (px0 >= 0 && i % 2 == 1) line(g, px0, py0, px, py, T.line());
                px0 = px;
                py0 = py;
            }
            for (int i = 0; i < n; i++) {
                int px = x + atlasX(a[i * 3]), py = y + atlasY(a[i * 3]);
                double r = a[i * 3 + 2] / 1000.0;
                int c = r > 0.9 ? GREEN : r > 0.5 ? YELLOW : VIOLET;
                g.fill(px - 1, py - 1, px + 2, py + 2, c);
                if (i == sel) ellipse(g, px, py, 5, 5, 0xFFFFFFFF, 0);
            }
            T.tex("card").draw(g, 0, 0, x + 190, y + 18, 98, 128);
            if (n == 0) {
                centre(g, tr("atlas_empty"), x + 239, y + 60, T.dim());
                return;
            }
            long seed = a[sel * 3];
            text(g, Long.toHexString(seed).toUpperCase().substring(0, Math.min(8, Long.toHexString(seed).length())),
                    x + 195, y + 23, T.accent(), true);
            String biome = Component.translatable("gtna.machine.dimensional_rift_gate.biome." +
                    RiftCore.biome(seed).name().toLowerCase()).getString();
            var font = net.minecraft.client.Minecraft.getInstance().font;
            while (font.width(biome) > 56 && biome.length() > 2) biome = biome.substring(0, biome.length() - 1);
            String[][] rows = { { tr("biome"), biome },
                    { tr("best_r"), String.format("%.3f", a[sel * 3 + 2] / 1000.0) },
                    { tr("depth"), String.valueOf(a[sel * 3 + 1]) },
                    { tr("note"), RiftCore.harmonic(seed).p + ":" + RiftCore.harmonic(seed).q } };
            for (int i = 0; i < rows.length; i++) {
                text(g, rows[i][0], x + 195, y + 37 + i * 11, T.dim(), false);
                right(g, rows[i][1], x + 284, y + 37 + i * 11, T.glow());
            }
            centre(g, m.atlasSize() + " " + tr("seeds"), x + 239, y + 130, T.dim());
        });
        for (int i = 0; i < 64; i++) {
            final int k = i;
            panel.addWidget(new com.lowdragmc.lowdraglib.gui.widget.ButtonWidget(0, 0, 1, 1,
                    com.lowdragmc.lowdraglib.gui.texture.IGuiTexture.EMPTY, c -> nav.selected = k) {

                @Override
                public boolean isVisible() {
                    return k < m.atlas().length / 3;
                }

                @Override
                @net.minecraftforge.api.distmarker.OnlyIn(net.minecraftforge.api.distmarker.Dist.CLIENT)
                public boolean isMouseOverElement(double mouseX, double mouseY) {
                    long[] a = m.atlas();
                    if (k >= a.length / 3) return false;
                    var p = getParent().getPosition();
                    return Math.abs(mouseX - (p.x + atlasX(a[k * 3]))) <= 4 &&
                            Math.abs(mouseY - (p.y + atlasY(a[k * 3]))) <= 4;
                }
            });
        }
        return panel;
    }

    private static int atlasX(long seed) {
        return 14 + (int) Math.floorMod(seed * 2654435761L >>> 7, 168);
    }

    private static int atlasY(long seed) {
        return 22 + (int) Math.floorMod(seed * 40503L >>> 11, 118);
    }
}
