package com.raishxn.gtna.common.machine.multiblock.originals.ui;

import net.minecraft.client.gui.GuiGraphics;
import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.api.distmarker.OnlyIn;

import com.raishxn.gtna.api.machine.feature.lance.LanceCore.Body;

import static com.raishxn.gtna.common.machine.multiblock.originals.ui.OriginalScreen.*;

/** Pixel art of the Lance's target bodies and the animation clock of its screen (client only). */
@OnlyIn(Dist.CLIENT)
public final class LanceArt {

    public static final int[] COLOURS = { 0xFFC4C4CA, 0xFF967864, 0xFFBAAA92, 0xFF9696A0, 0xFFD2CCBA, 0xFFE2E8F4,
            0xFFE2886A, 0xFFC878FF };

    private LanceArt() {}

    /** Seconds on a client clock, for animations. */
    public static double now() {
        return (System.currentTimeMillis() % 3_600_000L) / 1000.0;
    }

    /** Draws a body of radius {@code r} centred on (cx, cy); {@code t} turns its surface features. */
    public static void body(GuiGraphics g, Body b, int cx, int cy, int r, double t, boolean lit) {
        int base = lit ? COLOURS[b.ordinal()] : dim(COLOURS[b.ordinal()], 0.35);
        int dark = dim(base, 0.7), light = lighter(base);
        switch (b) {
            case ARROKOTH -> {
                // Contact binary: two lobes, the small one in front.
                int r2 = Math.max(1, r * 2 / 3);
                disc(g, cx - r / 3, cy, r * 3 / 4, base);
                disc(g, cx + r * 2 / 3, cy - 1, r2, dark);
                return;
            }
            case PHOBOS -> {
                // Irregular: a wider, flattened shape with the Stickney crater.
                for (int y = -r * 3 / 4; y <= r * 3 / 4; y++) {
                    int half = (int) Math.round(r * Math.sqrt(Math.max(0, 1 - (y * y) / (0.56 * r * r))));
                    g.fill(cx - half, cy + y, cx + half + 1, cy + y + 1, base);
                }
                spot(g, cx, cy, r, t, 0.2, 0.3, Math.max(1, r / 3), dark);
                return;
            }
            default -> disc(g, cx, cy, r, base);
        }
        switch (b) {
            case MOON -> {
                spot(g, cx, cy, r, t, 0.0, -0.2, Math.max(1, r / 3), dark);
                spot(g, cx, cy, r, t, 2.1, 0.35, Math.max(1, r / 4), dark);
                spot(g, cx, cy, r, t, 4.0, 0.1, Math.max(1, r / 5), dark);
            }
            case VESTA -> spot(g, cx, cy, r, t, 1.0, 0.55, Math.max(1, r / 2), dark);
            case CERES -> spot(g, cx, cy, r, t, 0.5, -0.1, Math.max(1, r / 5), 0xFFF4F4FF);
            case PSYCHE -> {
                // Metal: a glint that sweeps across the surface.
                int sx = (int) Math.round(cx + r * 0.6 * Math.sin(t * 0.8)), sy = cy - r / 3;
                g.fill(sx - Math.max(1, r / 4), sy, sx + Math.max(1, r / 4) + 1, sy + Math.max(1, r / 4), light);
            }
            case EUROPA -> {
                // Lineae: reddish cracks that drift with the rotation.
                for (int k = 0; k < 3; k++) {
                    double a = t * 0.3 + k * 2.1;
                    int x0 = (int) Math.round(cx + r * 0.8 * Math.sin(a)), y0 = cy - r / 2 + k * r / 3;
                    line(g, x0 - r / 2, y0, x0 + r / 2, y0 + 1, lit ? 0xFFB4645A : dark);
                }
            }
            case NEXUS_1 -> {
                // Lattice crust and a pulse.
                for (int k = -r; k <= r; k += 3) {
                    line(g, cx + k, cy - r / 2, cx + k / 2, cy + r / 2, dark);
                }
                if (lit) glow(g, cx, cy, r + 4, 0xFFC878FF, 0.35 + 0.25 * Math.sin(t * 3));
            }
            default -> {}
        }
        g.fill(cx - r / 2, cy - r / 2, cx - r / 2 + Math.max(1, r / 3), cy - r / 2 + 1, light);
    }

    /** A crater at longitude {@code lon} + rotation, latitude {@code lat} (fraction of r); hidden on the far side. */
    private static void spot(GuiGraphics g, int cx, int cy, int r, double t, double lon, double lat, int size, int c) {
        double a = lon + t * 0.4;
        if (Math.cos(a) < 0) return;
        int sx = (int) Math.round(cx + r * 0.75 * Math.sin(a)), sy = (int) Math.round(cy + r * lat);
        disc(g, sx, sy, size, c);
    }

    /** A ring of dots turning with {@code t}. */
    public static void ring(GuiGraphics g, int cx, int cy, int r, double t, int c) {
        for (int k = 0; k < 12; k++) {
            double a = t * 1.5 + k * Math.PI / 6;
            if (k % 3 == 2) continue;
            px(g, (int) Math.round(cx + r * Math.cos(a)), (int) Math.round(cy + r * Math.sin(a)), c);
        }
    }
}
