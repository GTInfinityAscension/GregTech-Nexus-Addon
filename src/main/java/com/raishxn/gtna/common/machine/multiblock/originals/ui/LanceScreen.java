package com.raishxn.gtna.common.machine.multiblock.originals.ui;

import com.gregtechceu.gtceu.api.machine.multiblock.WorkableElectricMultiblockMachine;

import com.lowdragmc.lowdraglib.gui.modular.ModularUI;
import com.lowdragmc.lowdraglib.gui.util.ClickData;

import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.network.chat.Component;
import net.minecraft.world.entity.player.Player;

import com.raishxn.gtna.api.machine.feature.lance.LanceCore;
import com.raishxn.gtna.api.machine.feature.lance.LanceCore.Body;
import com.raishxn.gtna.common.machine.multiblock.originals.LanceMachine;

import static com.raishxn.gtna.common.machine.multiblock.originals.ui.OriginalScreen.*;

/** Kinetic Orbital Lance screen (UI v2): status display, Orbital Map and Barrel Bench panels, field manual. */
public final class LanceScreen {

    private static final Theme T = LANCE;
    /** Orbit radius (map units) and angle of each body on the Orbital Map. */
    private static final double[][] ORBITS = { { 14, 0.5 }, { 24, 2.4 }, { 34, 3.7 }, { 44, 5.3 }, { 52, 1.2 },
            { 58, 4.4 }, { 64, 2.9 }, { 70, 0.9 } };
    private static final int MAP_X = 122, MAP_Y = 92;

    private LanceScreen() {}

    public static ModularUI create(LanceMachine m, Player player) {
        Nav nav = new Nav();
        var root = window(T, m, player, (g, x, y) -> display(g, m, x, y), (g, x, y) -> {
            chip(g, x, y, 52, tr("formed"), m.isFormed() ? GREEN : RED);
            chip(g, x + 56, y, 52, tr("auto"), v(m, 7) > 0 ? T.accent() : T.dim());
            chip(g, x + 112, y, 50, "NEXUS", VIOLET);
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
        root.addWidget(manual(nav, "kinetic_orbital_lance"));
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

    private static void display(GuiGraphics g, LanceMachine m, int x, int y) {
        int cx = x + 48, cy = y + 52;
        ellipse(g, cx, cy, 34, 34, T.line(), 2);
        ellipse(g, cx, cy, 24, 24, T.line(), 2);
        glow(g, cx, cy, 14, 0xFF285AAA, 0.6);
        disc(g, cx, cy, 8, 0xFF3C78D2);
        g.fill(cx - 3, cy - 4, cx, cy - 3, 0xFF6EBE6E);
        int mx = cx + 24, my = cy - 24;
        disc(g, mx, my, 5, 0xFFBEBEC4);
        ellipse(g, mx, my, 9, 9, T.accent(), 2);
        // The shot arc, lit for two seconds after a shot.
        int arc = m.secondsSinceShot() <= 2 ? T.glow() : T.accent();
        for (int k = 0; k < 20; k++) {
            double a = k / 19.0;
            px(g, (int) Math.round(cx + 8 + (mx - cx - 8) * a),
                    (int) Math.round(cy - 6 - (cy - 6 - my) * a - 10 * Math.sin(Math.PI * a)), arc);
        }
        Body target = m.target();
        centre(g, body(target) + " " + fmtDistance(target), cx, y + 94, T.accent());
        int x0 = x + 100, w = 186;
        text(g, tr("target") + ": " + body(target), x0, y + 4, T.glow(), true);
        double survey = v(m, 9 + target.ordinal());
        right(g, tr("survey") + " " + Math.round(survey * 100) + "%", x + 286, y + 4,
                survey >= 0.99 ? GREEN : T.dim());
        bar(g, T, x0, y + 16, w, tr("bank"), sci(v(m, 0)) + " EU", v(m, 1) > 0 ? v(m, 0) / v(m, 1) : 0, T.accent());
        bar(g, T, x0, y + 33, w, tr("barrel"), Math.round(v(m, 2)) + " K", (v(m, 2) - 300) / 2200, 0xFFFF643C);
        bar(g, T, x0, y + 50, w, tr("liner"), Math.round(v(m, 3) * 100) + "%", v(m, 3), 0xFFFFD246);
        int cwu = m.computation();
        bar(g, T, x0, y + 67, w, tr("aim"), cwu + " CWU/t", Math.min(1, cwu / 16000.0), 0xFF6ED2FF);
        int slug = (int) v(m, 8);
        String slugName = slug < 0 ? tr("no_slug") :
                Component.translatable("gtna.ui.o.slug." + LanceCore.Projectile.values()[slug].name().toLowerCase())
                        .getString();
        text(g, slugName + ", " + (int) v(m, 6) + " " + tr("capsules"), x0, y + 86, T.dim(), false);
        text(g, tr("efficiency") + " " + Math.round(v(m, 4) * 100) + "%  " + tr("accuracy") + " " +
                String.format("%.2f", v(m, 5)), x0, y + 96, T.dim(), false);
    }

    private static String fmtDistance(Body b) {
        return b.distanceMm >= 1e4 ? String.format("%.1e Mm", b.distanceMm) : Math.round(b.distanceMm) + " Mm";
    }

    // ------------------------------------------------------------------ orbital map

    private static int bodyX(int i) {
        return (int) Math.round(MAP_X + ORBITS[i][0] * 1.7 * Math.cos(ORBITS[i][1]));
    }

    private static int bodyY(int i) {
        return (int) Math.round(MAP_Y + ORBITS[i][0] * 1.0 * Math.sin(ORBITS[i][1]));
    }

    private static final int[] BODY_COLOURS = { 0xFFC4C4CA, 0xFF967864, 0xFFBAAA92, 0xFF9696A0, 0xFFD2CCBA, 0xFFE2E8F4,
            0xFFE2886A, 0xFFC878FF };

    private static com.lowdragmc.lowdraglib.gui.widget.WidgetGroup orbitPanel(LanceMachine m, Nav nav) {
        var panel = panel(T, nav, "orbit", "orbit_map_title", 380, 170, "panel_wide", (g, x, y) -> {
            int cx = x + MAP_X, cy = y + MAP_Y;
            for (double[] o : ORBITS) ellipse(g, cx, cy, o[0] * 1.7, o[0] * 1.0, T.line(), 1);
            glow(g, cx, cy, 12, 0xFFFFC850, 0.8);
            disc(g, cx, cy, 5, 0xFFFFF0AA);
            int sel = nav.selected >= 0 ? nav.selected : m.target().ordinal();
            for (Body b : Body.values()) {
                int i = b.ordinal();
                boolean ok = m.isTargetable(b);
                int bx = x + bodyX(i), by = y + bodyY(i);
                int c = ok ? BODY_COLOURS[i] : dim(BODY_COLOURS[i], 0.35);
                g.fill(bx - 2, by - 2, bx + 3, by + 3, c);
                g.fill(bx - 1, by - 1, bx + 2, by, lighter(c));
                if (i == m.target().ordinal()) ellipse(g, bx, by, 5, 5, T.accent(), 0);
                if (i == sel) {
                    g.fill(bx - 5, by - 6, bx + 6, by - 5, T.glow());
                    g.fill(bx - 5, by + 6, bx + 6, by + 7, T.glow());
                }
                text(g, body(b), bx + 6, by - 4, ok ? T.glow() : T.dim(), ok);
            }
            // Card of the selected body.
            Body b = Body.values()[sel];
            int kx = x + 244;
            T.tex("card_wide").draw(g, 0, 0, kx, y + 17, 130, 148);
            text(g, body(b), kx + 5, y + 23, T.accent(), true);
            String[][] rows = { { tr("survey"), Math.round(v(m, 9 + sel) * 100) + "%" },
                    { tr("distance"), fmtDistance(b) }, { tr("hardness"), b.hardnessMJ + " MJ/kg" },
                    { tr("return"), returnTime(b) }, { tr("yields"), yields(b) } };
            for (int i = 0; i < rows.length; i++) {
                text(g, rows[i][0], kx + 5, y + 37 + i * 12, T.dim(), false);
                right(g, rows[i][1], kx + 126, y + 37 + i * 12, T.glow());
            }
            if (!m.isTargetable(b)) centre(g, tr("locked"), kx + 65, y + 110, RED);
        });
        for (Body b : Body.values()) {
            int i = b.ordinal();
            panel.addWidget(hit(bodyX(i) - 4, bodyY(i) - 4, 9, 9, click -> nav.selected = i));
        }
        panel.addWidget(new Plate(T, 248, 146, 122, 16, "orbit", Component.translatable("gtna.ui.o.set_target"),
                () -> nav.selected < 0 || nav.selected == m.target().ordinal(),
                click -> act(m, "t" + (nav.selected < 0 ? m.target().ordinal() : nav.selected), click)));
        return panel;
    }

    private static String returnTime(Body b) {
        long s = Math.round(2 * b.distanceMm * 1e6 / 30000 / 600);
        return s < 120 ? s + " s" : s < 7200 ? s / 60 + " min" : s / 3600 + " h " + s % 3600 / 60 + " min";
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
            // Barrel with the rail sockets, lit as rails are fitted.
            int rails = 0;
            for (var c : LanceCore.Component.values()) if (c.slot == LanceCore.Slot.RAIL) rails += m.fitted(c);
            g.fill(x + 12, y + 30, x + 280, y + 38, 0xFF463C3C);
            g.fill(x + 12, y + 30, x + 280, y + 31, 0xFF6E6464);
            for (int k = 0; k < 8; k++) {
                int c = k < rails ? 0xFFFFB43C : 0xFF362E32;
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
                        b[1] > 0 ? b[0] / b[1] : 0, T.accent());
                bar(g, T, x + 152, y + 122, 128, tr("heat"), Math.round(b[2]) + "/" + Math.round(b[3]),
                        b[3] > 0 ? b[2] / b[3] : 0, 0xFFFF643C);
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
