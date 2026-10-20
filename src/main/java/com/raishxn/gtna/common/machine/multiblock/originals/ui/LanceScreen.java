package com.raishxn.gtna.common.machine.multiblock.originals.ui;

import com.gregtechceu.gtceu.api.machine.multiblock.WorkableElectricMultiblockMachine;

import com.lowdragmc.lowdraglib.gui.modular.ModularUI;
import com.lowdragmc.lowdraglib.gui.util.ClickData;
import com.lowdragmc.lowdraglib.gui.widget.Widget;

import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.network.FriendlyByteBuf;
import net.minecraft.network.chat.Component;
import net.minecraft.world.entity.player.Player;
import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.api.distmarker.OnlyIn;

import com.raishxn.gtna.api.machine.feature.lance.LanceCore;
import com.raishxn.gtna.api.machine.feature.lance.LanceCore.Body;
import com.raishxn.gtna.common.machine.multiblock.originals.LanceMachine;

import static com.raishxn.gtna.common.machine.multiblock.originals.ui.OriginalScreen.*;

/** Kinetic Orbital Lance screen (UI v2): status display, Orbital Map and Barrel Bench panels, field manual. */
public final class LanceScreen {

    private static final Theme T = LANCE;
    /** Orbit radius (map units) and starting angle of each body on the Orbital Map. */
    private static final double[][] ORBITS = { { 14, 0.5 }, { 24, 2.4 }, { 34, 3.7 }, { 44, 5.3 }, { 52, 1.2 },
            { 58, 4.4 }, { 64, 2.9 }, { 70, 0.9 } };
    private static final int MAP_X = 122, MAP_Y = 92;
    /** Seconds the projectile takes to cross the main display after a shot. */
    private static final double FLIGHT = 1.2;

    private LanceScreen() {}

    public static ModularUI create(LanceMachine m, Player player) {
        Nav nav = new Nav();
        // Client clock of the last shot and the last secondsSinceShot seen, for the shot animation.
        double[] shot = { -99, 99 };
        var root = window(T, m, player, (g, x, y) -> display(g, m, x, y, shot), (g, x, y) -> {
            chip(g, T, x, y, 52, tr("formed"), m.isFormed() ? GREEN : RED);
            chip(g, T, x + 56, y, 52, tr("auto"), v(m, 7) > 0 ? T.accent() : T.dim());
        });
        root.addWidget(gridButton(T, 0, "left", "prev_target", () -> false, click -> act(m, "tp", click)));
        root.addWidget(gridButton(T, 1, "right", "next_target", () -> false, click -> act(m, "tn", click)));
        root.addWidget(gridButton(T, 2, "auto", "auto", () -> v(m, 7) > 0, click -> act(m, "a", click)));
        root.addWidget(gridButton(T, 3, "orbit", "orbit", () -> "orbit".equals(nav.open), c -> nav.toggle("orbit")));
        root.addWidget(gridButton(T, 4, "gear", "bench", () -> "bench".equals(nav.open), c -> nav.toggle("bench")));
        root.addWidget(gridButton(T, 5, "capsule", "pods", () -> v(m, 6) > 0, c -> {}));
        root.addWidget(gridButton(T, 6, "info", "info", () -> "manual".equals(nav.open), c -> nav.toggle("manual")));
        root.addWidget(powerButton(T, 7, m));
        root.addWidget(orbitPanel(m, nav));
        root.addWidget(benchPanel(m, nav));
        root.addWidget(manual(T, nav, "kinetic_orbital_lance"));
        return ui(root, m, player);
    }

    static void act(WorkableElectricMultiblockMachine m, String data, ClickData click) {
        if (!click.isRemote) m.handleDisplayClick(data, click);
    }

    static double v(LanceMachine m, int i) {
        double[] view = m.view();
        return i < view.length ? view[i] : 0;
    }

    static String tr(String key) {
        return Component.translatable("gtna.ui.o." + key).getString();
    }

    static String body(Body b) {
        return Component.translatable("gtna.machine.kinetic_orbital_lance.body." + b.name().toLowerCase())
                .getString();
    }

    // ------------------------------------------------------------------ display

    /** Point {@code a} (0..1) of an arc from (x0, y0) to (x1, y1) bulging {@code h} pixels to the left. */
    private static int[] arc(int x0, int y0, int x1, int y1, double h, double a) {
        double dx = x1 - x0, dy = y1 - y0, len = Math.max(1, Math.hypot(dx, dy)), b = h * Math.sin(Math.PI * a);
        return new int[] { (int) Math.round(x0 + dx * a + dy / len * b), (int) Math.round(y0 + dy * a - dx / len * b) };
    }

    private static void display(GuiGraphics g, LanceMachine m, int x, int y, double[] shot) {
        double t = LanceArt.now();
        int cx = x + 48, cy = y + 52;
        ellipse(g, cx, cy, 34, 34, T.line(), 2);
        ellipse(g, cx, cy, 24, 24, T.line(), 2);
        glow(g, cx, cy, 14, 0xFF285AAA, 0.6);
        disc(g, cx, cy, 8, 0xFF3C78D2);
        g.fill(cx - 3, cy - 4, cx, cy - 3, 0xFF6EBE6E);
        g.fill(cx + 2, cy + 1, cx + 5, cy + 3, 0xFF6EBE6E);
        // The target, drawn as itself, orbits on the outer ring.
        Body target = m.target();
        double angle = -Math.PI / 4 + t * 0.12;
        int mx = cx + (int) Math.round(34 * Math.cos(angle)), my = cy + (int) Math.round(34 * Math.sin(angle));
        int s = m.secondsSinceShot();
        if (s == 0 && shot[1] != 0) shot[0] = t;
        shot[1] = s;
        double since = t - shot[0];
        int arcColour = since >= 0 && since <= 2 ? T.glow() : T.accent();
        for (int k = 0; k < 20; k++) {
            int[] p = arc(cx, cy, mx, my, 10, k / 19.0);
            if (k % 2 == 0) px(g, p[0], p[1], arcColour);
        }
        LanceArt.body(g, target, mx, my, 6, t, true);
        LanceArt.ring(g, mx, my, 9, t, T.accent());
        // The slug crosses the arc, then the impact flashes.
        if (since >= 0 && since < FLIGHT) {
            for (int k = 0; k < 4; k++) {
                double a = since / FLIGHT - k * 0.04;
                if (a < 0) continue;
                int[] p = arc(cx, cy, mx, my, 10, a);
                g.fill(p[0], p[1], p[0] + 2, p[1] + 2, k == 0 ? 0xFFFFFFFF : dim(T.glow(), 1 - k * 0.2));
            }
        } else if (since >= FLIGHT && since < FLIGHT + 0.8) {
            glow(g, mx, my, 12, 0xFFFFE6A0, 1 - (since - FLIGHT) / 0.8);
        }
        // Capsules on their way back, on the inner side of the arc.
        int capsules = (int) v(m, 6);
        for (int k = 0; k < Math.min(capsules, 3); k++) {
            double a = (t * 0.2 + k / 3.0) % 1;
            int[] p = arc(mx, my, cx, cy, 8, a);
            g.fill(p[0], p[1], p[0] + 2, p[1] + 2, 0xFFFFD246);
        }
        centre(g, body(target) + " " + fmtDistance(target), cx, y + 94, T.accent());

        int x0 = x + 100, w = 186;
        text(g, tr("target") + ": " + body(target), x0, y + 4, T.glow(), true);
        double survey = v(m, 9 + target.ordinal());
        right(g, tr("survey") + " " + Math.round(survey * 100) + "%", x + 286, y + 4,
                survey >= 0.99 ? GREEN : T.dim());
        double bank = v(m, 0), capacity = v(m, 1);
        String bankText = sci(bank) + " EU";
        // Time to a full bank at the network charge rate.
        if (capacity > 0 && bank < capacity)
            bankText += " · " + fmtTime((capacity - bank) / LanceMachine.CHARGE_PER_SECOND);
        bar(g, T, x0, y + 16, w, tr("bank"), bankText, capacity > 0 ? bank / capacity : 0, T.accent());
        bar(g, T, x0, y + 33, w, tr("barrel"), Math.round(v(m, 2)) + " K", (v(m, 2) - 300) / 2200, 0xFFFF643C);
        bar(g, T, x0, y + 50, w, tr("liner"), Math.round(v(m, 3) * 100) + "%", v(m, 3), 0xFFFFD246);
        int cwu = m.computation();
        bar(g, T, x0, y + 67, w, tr("aim"), cwu + " CWU/t", Math.min(1, cwu / (double) LanceMachine.AIM_CWUT),
                0xFF6ED2FF);
        int slug = (int) v(m, 8);
        String slugName = slug >= 0 ?
                Component.translatable("gtna.ui.o.slug." + LanceCore.Projectile.values()[slug].name().toLowerCase())
                        .getString() :
                target == Body.NEXUS_1 ? tr("needs_magnetar") : tr("no_slug");
        double next = v(m, 9 + Body.values().length);
        String pods = capsules + " " + tr("capsules") + (capsules > 0 && next >= 0 ?
                " · " + tr("next_capsule") + " " + fmtTime(next) : "");
        text(g, slugName, x0, y + 86, slug >= 0 ? T.dim() : 0xFFE08C5A, false);
        text(g, pods + "  " + tr("efficiency") + " " + Math.round(v(m, 4) * 100) + "%  " + tr("accuracy") + " " +
                String.format("%.2f", v(m, 5)), x0, y + 96, T.dim(), false);
    }

    private static String fmtDistance(Body b) {
        return b.distanceMm >= 1e4 ? String.format("%.1e Mm", b.distanceMm) : Math.round(b.distanceMm) + " Mm";
    }

    static String fmtTime(double seconds) {
        long s = (long) Math.ceil(seconds);
        if (s < 120) return s + " s";
        return s < 7200 ? s / 60 + " min " + s % 60 + " s" : s / 3600 + " h " + s % 3600 / 60 + " min";
    }

    // ------------------------------------------------------------------ orbital map

    /** Angle of body {@code i} at time {@code t}: inner bodies go round faster (Kepler, T ∝ r^1.5). */
    private static double bodyAngle(int i, double t) {
        return ORBITS[i][1] + t * 0.05 / Math.pow(ORBITS[i][0] / ORBITS[0][0], 1.5);
    }

    private static int bodyX(int i, double t) {
        return (int) Math.round(MAP_X + ORBITS[i][0] * 1.7 * Math.cos(bodyAngle(i, t)));
    }

    private static int bodyY(int i, double t) {
        return (int) Math.round(MAP_Y + ORBITS[i][0] * 1.0 * Math.sin(bodyAngle(i, t)));
    }

    private static com.lowdragmc.lowdraglib.gui.widget.WidgetGroup orbitPanel(LanceMachine m, Nav nav) {
        var panel = panel(T, nav, "orbit", "orbit_map_title", 380, 170, "panel_wide", (g, x, y) -> {
            double t = LanceArt.now();
            int cx = x + MAP_X, cy = y + MAP_Y;
            for (double[] o : ORBITS) ellipse(g, cx, cy, o[0] * 1.7, o[0] * 1.0, T.line(), 1);
            glow(g, cx, cy, 12, 0xFFFFC850, 0.7 + 0.15 * Math.sin(t * 2));
            disc(g, cx, cy, 5, 0xFFFFF0AA);
            int sel = nav.selected >= 0 ? nav.selected : m.target().ordinal();
            int ti = m.target().ordinal();
            // Firing line to the target, with dots marching outwards.
            int tx = x + bodyX(ti, t), ty = y + bodyY(ti, t);
            double len = Math.hypot(tx - cx, ty - cy);
            for (int k = 0; k < len / 6; k++) {
                double a = (k + t * 2 % 1) * 6 / len;
                if (a > 1) break;
                px(g, (int) Math.round(cx + (tx - cx) * a), (int) Math.round(cy + (ty - cy) * a), T.accent());
            }
            // Labels: the selected and the targeted body first; a label that would cover another one is left out,
            // and one that would run into the card goes on the left of its body.
            var font = net.minecraft.client.Minecraft.getInstance().font;
            var placed = new java.util.ArrayList<int[]>();
            Body[] order = Body.values().clone();
            java.util.Arrays.sort(order,
                    java.util.Comparator.comparingInt(o -> o.ordinal() == sel ? 0 : o.ordinal() == ti ? 1 : 2));
            for (Body b : order) {
                int i = b.ordinal();
                boolean ok = m.isTargetable(b);
                int bx = x + bodyX(i, t), by = y + bodyY(i, t);
                LanceArt.body(g, b, bx, by, b == Body.PHOBOS ? 2 : 3, t, ok);
                if (i == ti) ellipse(g, bx, by, 6, 6, T.accent(), 0);
                if (i == sel) LanceArt.ring(g, bx, by, 8, t, T.glow());
                String name = body(b);
                int w = font.width(name), lx = bx + 7 + w > x + 240 ? bx - 7 - w : bx + 7, ly = by - 4;
                boolean free = true;
                for (int[] r : placed) free &= lx + w < r[0] || lx > r[2] || ly + 8 < r[1] || ly > r[3];
                if (!free && i != sel && i != ti) continue;
                placed.add(new int[] { lx, ly, lx + w, ly + 8 });
                text(g, name, lx, ly, ok ? T.glow() : T.dim(), ok);
            }
            // Card of the selected body.
            Body b = Body.values()[sel];
            int kx = x + 244;
            T.tex("card_wide").draw(g, 0, 0, kx, y + 17, 130, 148);
            text(g, body(b), kx + 5, y + 23, T.accent(), true);
            LanceArt.body(g, b, kx + 112, y + 30, 8, t, m.isTargetable(b));
            String[][] rows = { { tr("survey"), Math.round(v(m, 9 + sel) * 100) + "%" },
                    { tr("distance"), fmtDistance(b) }, { tr("hardness"), b.hardnessMJ + " MJ/kg" },
                    { tr("return"), fmtTime(LanceCore.returnSeconds(b)) }, { tr("yields"), yields(b) } };
            for (int i = 0; i < rows.length; i++) {
                text(g, rows[i][0], kx + 5, y + 43 + i * 12, T.dim(), false);
                right(g, rows[i][1], kx + 126, y + 43 + i * 12, T.glow());
            }
            if (!m.isTargetable(b)) {
                centre(g, tr("locked"), kx + 65, y + 110, RED);
                var parents = new StringBuilder();
                for (Body p : b.parents) parents.append(parents.length() > 0 ? " + " : "").append(body(p));
                centre(g, tr("needs_survey") + " " + parents, kx + 65, y + 122, T.dim());
            } else if (b == Body.NEXUS_1) {
                centre(g, tr("needs_magnetar"), kx + 65, y + 116, T.dim());
            }
        });
        panel.addWidget(new MapClick(nav));
        panel.addWidget(new Plate(T, 248, 146, 122, 16, "orbit", Component.translatable("gtna.ui.o.set_target"),
                () -> nav.selected < 0 || nav.selected == m.target().ordinal(),
                click -> act(m, "t" + (nav.selected < 0 ? m.target().ordinal() : nav.selected), click)));
        return panel;
    }

    /**
     * Click on the moving bodies: picks the body nearest to the cursor where it is drawn now, and tells the server
     * (which builds its own screen) so "Set target" aims at the same body.
     */
    private static final class MapClick extends Widget {

        private static final int X = 2, Y = 18;
        private final Nav nav;

        MapClick(Nav nav) {
            super(X, Y, 240, 148);
            this.nav = nav;
        }

        @Override
        @OnlyIn(Dist.CLIENT)
        public boolean mouseClicked(double mouseX, double mouseY, int button) {
            if (!isMouseOverElement(mouseX, mouseY)) return false;
            double t = LanceArt.now();
            int ox = getPositionX() - X, oy = getPositionY() - Y, best = -1;
            double bestD = 8;
            for (int i = 0; i < ORBITS.length; i++) {
                double d = Math.hypot(mouseX - ox - bodyX(i, t), mouseY - oy - bodyY(i, t));
                if (d < bestD) {
                    bestD = d;
                    best = i;
                }
            }
            if (best < 0) return false;
            int chosen = best;
            nav.selected = chosen;
            writeClientAction(1, buf -> buf.writeVarInt(chosen));
            return true;
        }

        @Override
        public void handleClientAction(int id, FriendlyByteBuf buffer) {
            if (id == 1) nav.selected = Math.max(-1, Math.min(ORBITS.length - 1, buffer.readVarInt()));
            else super.handleClientAction(id, buffer);
        }
    }

    private static String yields(Body b) {
        var sb = new StringBuilder();
        for (var mat : LanceMachine.materials(b)) {
            if (mat == null) continue;
            String sym = mat.getChemicalFormula();
            if (sym == null || sym.isEmpty() || sym.length() > 4) sym = mat.getName().substring(0, 2);
            if (sb.length() + sym.length() > 16) break;
            sb.append(sb.length() > 0 ? " " : "").append(sym);
        }
        return sb.toString();
    }

    // ------------------------------------------------------------------ barrel bench

    private static final LanceCore.Slot[] SLOTS = LanceCore.Slot.values();

    private static com.lowdragmc.lowdraglib.gui.widget.WidgetGroup benchPanel(LanceMachine m, Nav nav) {
        var panel = panel(T, nav, "bench", "bench_title", (g, x, y) -> {
            // Barrel with the rail sockets, lit as rails are fitted; a charge pulse runs along the lit rails.
            int rails = 0;
            for (var c : LanceCore.Component.values()) if (c.slot == LanceCore.Slot.RAIL) rails += m.fitted(c);
            g.fill(x + 12, y + 30, x + 280, y + 38, 0xFF463C3C);
            g.fill(x + 12, y + 30, x + 280, y + 31, 0xFF6E6464);
            int pulse = (int) (LanceArt.now() * 6) % 10;
            for (int k = 0; k < 8; k++) {
                int c = k < rails ? (k == pulse ? 0xFFFFE696 : 0xFFFFB43C) : 0xFF362E32;
                g.fill(x + 18 + k * 33, y + 21, x + 42 + k * 33, y + 27, c);
                g.fill(x + 18 + k * 33, y + 41, x + 42 + k * 33, y + 47, c);
                if (k < rails) {
                    g.fill(x + 18 + k * 33, y + 21, x + 42 + k * 33, y + 22, 0xFFFFE696);
                    g.fill(x + 18 + k * 33, y + 41, x + 42 + k * 33, y + 42, 0xFFFFE696);
                }
            }
            centre(g, rails + "/8 " + tr("rails") + "  " + tr("efficiency") + " " + Math.round(v(m, 4) * 100) + "%",
                    x + 146, y + 51, T.dim());
            for (int s = 0; s < SLOTS.length; s++)
                centre(g, tr("slot." + SLOTS[s].name().toLowerCase()), x + 36 + s * 55, y + 62, T.accent());
            double[] b = m.bench();
            if (b.length >= 5) {
                bar(g, T, x + 12, y + 122, 128, tr("mass"), Math.round(b[0]) + "/" + Math.round(b[1]) + " t",
                        b[1] > 0 ? b[0] / b[1] : 0, b[0] > b[1] ? RED : T.accent());
                bar(g, T, x + 152, y + 122, 128, tr("heat"), Math.round(b[2]) + "/" + Math.round(b[3]),
                        b[3] > 0 ? b[2] / b[3] : 0, b[2] > b[3] ? RED : 0xFFFF643C);
            }
            right(g, m.benchValid() ? tr("bench_ok") : tr("bench_bad"), x + 270, y + 4,
                    m.benchValid() ? GREEN : RED);
        });
        // One plate per component, in its slot's column.
        int[] row = new int[SLOTS.length];
        for (var c : LanceCore.Component.values()) {
            int col = c.slot.ordinal(), r = row[col]++;
            String name = Component.translatable("gtna.ui.o.part." + c.name().toLowerCase()).getString();
            panel.addWidget(new Plate(T, 10 + col * 55, 72 + r * 15, 52, 13, "gear", null, () -> m.fitted(c) > 0,
                    click -> act(m, "c" + c.ordinal(), click)) {

                @Override
                @net.minecraftforge.api.distmarker.OnlyIn(net.minecraftforge.api.distmarker.Dist.CLIENT)
                public void drawInBackground(GuiGraphics g, int mouseX, int mouseY, float partialTicks) {
                    var p = getPosition();
                    boolean fitted = m.fitted(c) > 0;
                    boolean unlocked = m.isTargetable(Body.MOON) && (c.unlock == null ||
                            v(m, 9 + c.unlock.ordinal()) >= 0.99);
                    T.tex(fitted ? "small_on" : "small").draw(g, mouseX, mouseY, p.x, p.y, 52, 13);
                    String s = name + (m.fitted(c) > 1 ? " x" + m.fitted(c) : "");
                    var font = net.minecraft.client.Minecraft.getInstance().font;
                    while (font.width(s) > 48 && s.length() > 2) s = s.substring(0, s.length() - 1);
                    g.drawString(font, s, p.x + 3, p.y + 3, fitted ? T.glow() : unlocked ? T.dim() : 0xFF5A5050,
                            false);
                }
            }.tip("gtna.ui.o.part." + c.name().toLowerCase() + ".tip"));
        }
        return panel;
    }
}
