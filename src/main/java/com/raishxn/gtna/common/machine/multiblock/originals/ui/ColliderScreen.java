package com.raishxn.gtna.common.machine.multiblock.originals.ui;

import com.lowdragmc.lowdraglib.gui.modular.ModularUI;
import com.lowdragmc.lowdraglib.gui.widget.WidgetGroup;

import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.network.chat.Component;
import net.minecraft.world.entity.player.Player;

import com.raishxn.gtna.api.machine.feature.collider.ColliderCore;
import com.raishxn.gtna.common.machine.multiblock.originals.ColliderRingMachine;

import static com.raishxn.gtna.common.machine.multiblock.originals.ui.LanceScreen.act;
import static com.raishxn.gtna.common.machine.multiblock.originals.ui.LanceScreen.tr;
import static com.raishxn.gtna.common.machine.multiblock.originals.ui.OriginalScreen.*;

/** Antimatter Collider Ring screen (UI v2): ring display, Standard Model and Committee panels, field manual. */
public final class ColliderScreen {

    private static final Theme T = COLLIDER;
    private static final String[] SYMBOLS = { "p", "K", "L", "c", "b", "W", "Z", "H", "t", "X" };

    private ColliderScreen() {}

    public static ModularUI create(ColliderRingMachine m, Player player) {
        Nav nav = new Nav();
        var root = window(T, m, player, (g, x, y) -> display(g, m, x, y), (g, x, y) -> {
            chip(g, x, y, 52, tr("beam"), m.isBeamOn() ? GREEN : RED);
            chip(g, x + 56, y, 52, tr("dump"), v(m, 4) > 0 ? GREEN : T.dim());
            chip(g, x + 112, y, 50, "NEXUS", VIOLET);
        });
        root.addWidget(gridButton(T, 0, "swap", "mode", m::isPhysicsRun, click -> act(m, "mode", click)));
        root.addWidget(gridButton(T, 1, "atom", "model", () -> "model".equals(nav.open), c -> nav.toggle("model")));
        root.addWidget(gridButton(T, 2, "list", "committee", () -> "board".equals(nav.open),
                c -> nav.toggle("board")));
        root.addWidget(gridButton(T, 3, "ring", "traps", () -> false, c -> {}));
        root.addWidget(gridButton(T, 4, "snow", "cryo", () -> v(m, 0) >= 0.999, c -> {}));
        root.addWidget(gridButton(T, 5, "orbit", "ring", m::isCaptured, c -> {}));
        root.addWidget(gridButton(T, 6, "info", "info", () -> "manual".equals(nav.open), c -> nav.toggle("manual")));
        root.addWidget(powerButton(T, 7, m));
        root.addWidget(model(m, nav));
        root.addWidget(committee(m, nav));
        root.addWidget(manual(nav, "antimatter_collider_ring"));
        return ui(root, m, player);
    }

    static double v(ColliderRingMachine m, int i) {
        double[] view = m.view();
        return i < view.length ? view[i] : 0;
    }

    private static void display(GuiGraphics g, ColliderRingMachine m, int x, int y) {
        int cx = x + 48, cy = y + 52;
        int ring = m.isBeamOn() ? T.accent() : T.line();
        ellipse(g, cx, cy, 34, 34, ring, 0);
        ellipse(g, cx, cy, 33, 33, dim(ring, 0.5), 0);
        // Bunches running round the ring while the beam is on.
        double spin = m.isBeamOn() ? (System.currentTimeMillis() % 4000) / 4000.0 * 2 * Math.PI : 0;
        for (int k = 0; k < 16; k++) {
            double a = k * Math.PI / 8 + spin;
            int bx = (int) Math.round(cx + 34 * Math.cos(a)), by = (int) Math.round(cy + 34 * Math.sin(a));
            g.fill(bx - 1, by - 1, bx + 2, by + 2, 0xFFE6FFFA);
        }
        glow(g, cx, cy, 9, 0xFFFF50DC, m.isBeamOn() ? 0.9 : 0.3);
        disc(g, cx, cy, 3, 0xFFFFDCFA);
        int x0 = x + 100, w = 186;
        text(g, m.isPhysicsRun() ? tr("physics_run") : tr("production_run"), x0, y + 4, T.glow(), true);
        right(g, String.format("%.1f TeV", m.energyTeV() * 2), x + 286, y + 4, T.accent());
        text(g, ColliderCore.MAGNET_NAMES[Math.min(m.magnetTier(), ColliderCore.MAGNET_NAMES.length - 1)] + " " +
                ColliderCore.MAGNET_FIELD[Math.min(m.magnetTier(), ColliderCore.MAGNET_FIELD.length - 1)] + " T  L " +
                String.format("%.2e", m.luminosity()), x0, y + 14, T.dim(), false);
        bar(g, T, x0, y + 25, w, tr("ramp"), Math.min(100, Math.round(v(m, 6) * 5)) + "%",
                Math.min(1, v(m, 6) / 20), T.accent());
        bar(g, T, x0, y + 42, w, tr("helium"), Math.round(v(m, 0) * 100) + "%", v(m, 0), 0xFF96DCFF);
        bar(g, T, x0, y + 59, w, tr("traps"), sci(v(m, 1)), v(m, 2) > 0 ? v(m, 1) / v(m, 2) : 0, 0xFFFF50DC);
        int p = m.activeProposal();
        String prop = p < 0 ? tr("all_done") :
                Component.translatable("gtna.machine.antimatter_collider_ring.proposal." +
                        ColliderCore.Proposal.values()[p].name().toLowerCase()).getString();
        bar(g, T, x0, y + 76, w, tr("proposal"), Math.round(m.proposalProgress() * 10) / 10.0 + " fb",
                Math.min(1, m.proposalProgress() / 40), YELLOW);
        text(g, prop, x0, y + 95, T.dim(), false);
        if (v(m, 3) > 0) right(g, tr("quench") + " " + (int) v(m, 3) + " s", x + 286, y + 95, RED);
    }

    private static WidgetGroup model(ColliderRingMachine m, Nav nav) {
        return panel(T, nav, "model", "standard_model_title", (g, x, y) -> {
            var parts = ColliderCore.Particle.values();
            for (int i = 0; i < parts.length; i++) {
                int px = x + 8 + (i % 5) * 56, py = y + 18 + (i / 5) * 64;
                double z = m.significance(i);
                int col = z >= 5 ? GREEN : z >= 3 ? YELLOW : T.dim();
                T.tex("card").draw(g, 0, 0, px, py, 52, 60);
                g.pose().pushPose();
                g.pose().translate(px + 26 - net.minecraft.client.Minecraft.getInstance().font.width(SYMBOLS[i]),
                        py + 5, 0);
                g.pose().scale(2, 2, 1);
                g.drawString(net.minecraft.client.Minecraft.getInstance().font, SYMBOLS[i], 0, 0, col, true);
                g.pose().popPose();
                String name = Component.translatable("gtna.machine.antimatter_collider_ring.particle." +
                        parts[i].name().toLowerCase()).getString();
                var font = net.minecraft.client.Minecraft.getInstance().font;
                while (font.width(name) > 48 && name.length() > 2) name = name.substring(0, name.length() - 1);
                centre(g, name, px + 26, py + 28, T.glow());
                centre(g, String.format("%.1f", z) + "σ", px + 26, py + 39, col);
                g.fill(px + 6, py + 51, px + 46, py + 54, 0xFF141414);
                g.fill(px + 6, py + 51, px + 6 + (int) (40 * Math.min(1, z / 5)), py + 54, col);
            }
        });
    }

    private static WidgetGroup committee(ColliderRingMachine m, Nav nav) {
        return panel(T, nav, "board", "committee_title", (g, x, y) -> {
            var props = ColliderCore.Proposal.values();
            for (int i = 0; i < props.length; i++) {
                int yy = y + 18 + i * 14;
                boolean done = m.proposalDone(i), active = m.activeProposal() == i;
                int col = done ? GREEN : active ? T.accent() : T.dim();
                g.fill(x + 8, yy, x + 284, yy + 12, i % 2 == 0 ? 0xFF0C1618 : 0xFF000000);
                String n = Component.translatable("gtna.machine.antimatter_collider_ring.proposal." +
                        props[i].name().toLowerCase()).getString();
                var font = net.minecraft.client.Minecraft.getInstance().font;
                while (font.width(n) > 112 && n.length() > 2) n = n.substring(0, n.length() - 1);
                text(g, n, x + 12, yy + 2, col, done || active);
                text(g, tr("ask." + props[i].name().toLowerCase()), x + 128, yy + 2, T.dim(), false);
                double f = done ? 1 : active ? Math.min(1, m.proposalProgress() / 40) : 0;
                g.fill(x + 200, yy + 4, x + 246, yy + 8, 0xFF1E1E1E);
                g.fill(x + 200, yy + 4, x + 200 + (int) (46 * f), yy + 8, col);
                right(g, done ? tr("done") : active ? tr("active") : "", x + 282, yy + 2, col);
            }
        });
    }
}
