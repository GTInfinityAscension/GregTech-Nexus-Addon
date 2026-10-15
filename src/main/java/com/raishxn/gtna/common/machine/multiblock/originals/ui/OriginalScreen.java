package com.raishxn.gtna.common.machine.multiblock.originals.ui;

import com.gregtechceu.gtceu.api.gui.GuiTextures;
import com.gregtechceu.gtceu.api.gui.UITemplate;
import com.gregtechceu.gtceu.api.machine.multiblock.WorkableElectricMultiblockMachine;

import com.lowdragmc.lowdraglib.gui.modular.ModularUI;
import com.lowdragmc.lowdraglib.gui.texture.IGuiTexture;
import com.lowdragmc.lowdraglib.gui.texture.ResourceTexture;
import com.lowdragmc.lowdraglib.gui.util.ClickData;
import com.lowdragmc.lowdraglib.gui.widget.ButtonWidget;
import com.lowdragmc.lowdraglib.gui.widget.ImageWidget;
import com.lowdragmc.lowdraglib.gui.widget.Widget;
import com.lowdragmc.lowdraglib.gui.widget.WidgetGroup;

import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.network.chat.Component;
import net.minecraft.world.entity.player.Player;
import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.api.distmarker.OnlyIn;

import com.raishxn.gtna.GTNACORE;
import com.raishxn.gtna.common.machine.multiblock.originals.OriginalsInfoPanel;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.function.BooleanSupplier;
import java.util.function.Consumer;
import java.util.function.Supplier;

/**
 * The original multiblocks' screen (UI v2, mockups in tools/design/ui_v2_pixel): a wide window with a status display
 * on top, the player inventory bottom-left and a grid of plate buttons to its right; the old tabs are panels opened
 * over the display. Static art comes from {@code textures/gui/originals_v2/<theme>/}; text, icons, bars and drawings
 * are drawn every frame from the machine's synced fields, all on whole GUI pixels like the vanilla screens.
 */
public final class OriginalScreen {

    public static final int W = 300, H = 264, Y0 = 24;
    /** Display glass inside the window. */
    public static final int DX = 4, DY = Y0 + 18, DW = 292, DH = 108;

    private OriginalScreen() {}

    // ------------------------------------------------------------------ theme

    /** Colours (ARGB) and texture folder of one machine. */
    public record Theme(String dir, int accent, int glow, int base, int line, int dim) {

        public ResourceTexture tex(String name) {
            return new ResourceTexture(
                    GTNACORE.id("textures/gui/originals_v2/" + dir + "/" + name + ".png").toString());
        }
    }

    public static final Theme LANCE = new Theme("lance", 0xFFFFAA28, 0xFFFFE2A0, 0xFF141118, 0xFF6E5434, 0xFFA89680);
    public static final Theme STELLAR = new Theme("stellar", 0xFF60B0FF, 0xFFD6ECFF, 0xFF0A0E1C, 0xFF3A548C,
            0xFF8498C4);
    public static final Theme COLLIDER = new Theme("collider", 0xFF40ECD6, 0xFFCCFFF8, 0xFF081418, 0xFF2C7874,
            0xFF78AAAA);
    public static final Theme RIFT = new Theme("rift", 0xFFC470FF, 0xFFECD6FF, 0xFF120A1C, 0xFF644096, 0xFFA088C0);
    public static final int GREEN = 0xFF55FF55, YELLOW = 0xFFFFFF55, RED = 0xFFFF5555, VIOLET = 0xFFC88CFF;

    // ------------------------------------------------------------------ navigation (client and server alike)

    /** Which panel is open; each side toggles its own copy with the same clicks. */
    public static final class Nav {

        /** The navigation of the screen opened last (dev command {@code /gtna_dev_panel}). */
        public static Nav last;

        public Nav() {
            // In singleplayer the server builds the same screen: keep the client's copy only.
            if (net.minecraftforge.fml.loading.FMLEnvironment.dist.isClient() &&
                    "Render thread".equals(Thread.currentThread().getName()))
                last = this;
        }

        public String open;
        public int selected = -1, page;

        public void toggle(String panel) {
            open = panel.equals(open) ? null : panel;
        }
    }

    // ------------------------------------------------------------------ window

    /** A painter draws a widget's content at its absolute position. */
    @FunctionalInterface
    public interface Painter {

        @OnlyIn(Dist.CLIENT)
        void paint(GuiGraphics g, int x, int y);
    }

    /** The window: art, title, display painter, chip painter and the player inventory. Buttons and panels follow. */
    public static WidgetGroup window(Theme t, WorkableElectricMultiblockMachine machine, Player player,
                                     Painter display, Painter chips) {
        WidgetGroup root = new WidgetGroup(0, 0, W, H);
        root.addWidget(new ImageWidget(0, Y0, W, 240, t.tex("window")));
        root.addWidget(new Paint(0, Y0, 170, 16, (g, x, y) -> text(g, machine.getBlockState().getBlock().getName()
                .getString(), x + 8, y + 4, t.glow, true)));
        root.addWidget(new Paint(DX, DY, DW, DH, (g, x, y) -> {
            if (!machine.isFormed()) {
                centre(g, Component.translatable("gtceu.multiblock.invalid_structure").getString(), x + DW / 2,
                        y + DH / 2 - 4, RED);
                return;
            }
            display.paint(g, x, y);
        }));
        root.addWidget(new Paint(4, Y0 + 130, 166, 13, chips));
        root.addWidget(UITemplate.bindPlayerInventory(player.getInventory(), GuiTextures.SLOT, 4, Y0 + 148, true));
        return root;
    }

    public static ModularUI ui(WidgetGroup root, WorkableElectricMultiblockMachine machine, Player player) {
        return new ModularUI(W, H, machine, player).widget(root);
    }

    /** One of the eight plate buttons right of the inventory (2 columns x 4 rows, level with its slots). */
    public static Widget gridButton(Theme t, int index, String icon, String labelKey, BooleanSupplier active,
                                    Consumer<ClickData> onClick) {
        return new Plate(t, 172 + (index % 2) * 62, Y0 + 148 + (index / 2) * 19, 60, 18, icon,
                Component.translatable("gtna.ui.o." + labelKey), active, onClick)
                .tip("gtna.ui.o." + labelKey + ".tip");
    }

    /** The power button every screen has. */
    public static Widget powerButton(Theme t, int index, WorkableElectricMultiblockMachine m) {
        return gridButton(t, index, "power", "power", m::isWorkingEnabled, click -> {
            if (!click.isRemote) m.setWorkingEnabled(!m.isWorkingEnabled());
        });
    }

    /** A panel over the display while {@code nav.open} is {@code name}, with title, close box and content. */
    public static WidgetGroup panel(Theme t, Nav nav, String name, String titleKey, Painter content) {
        return panel(t, nav, name, titleKey, 292, 150, "panel", content);
    }

    /**
     * A draggable panel shown while {@code nav.open} is {@code name}; it starts centred over the display (it may be
     * wider than the window) and can be dragged anywhere by its frame.
     */
    public static WidgetGroup panel(Theme t, Nav nav, String name, String titleKey, int w, int h, String texture,
                                    Painter content) {
        var group = new com.lowdragmc.lowdraglib.gui.widget.DraggableWidgetGroup((W - w) / 2, Math.max(0, DY - 18 -
                (h - 150)), w, h) {

            @Override
            public boolean isVisible() {
                return name.equals(nav.open);
            }

            @Override
            public boolean isActive() {
                return name.equals(nav.open);
            }
        };
        group.addWidget(new ImageWidget(0, 0, w, h, t.tex(texture)));
        group.addWidget(new Paint(0, 0, w, h, (g, x, y) -> {
            text(g, Component.translatable("gtna.ui.o." + titleKey).getString(), x + 6, y + 4, t.accent, true);
            content.paint(g, x, y);
        }));
        group.addWidget(new Plate(t, w - 15, 2, 12, 11, "close", null, () -> false, click -> nav.open = null));
        return group;
    }

    // ------------------------------------------------------------------ field manual

    /** The how-it-works manual: chapters on the left, one page on the right, prev / next. */
    public static WidgetGroup manual(Nav nav, String machineId) {
        String[][] sections = OriginalsInfoPanel.sections(machineId);
        WidgetGroup group = new com.lowdragmc.lowdraglib.gui.widget.DraggableWidgetGroup(4, 0, 292, 200) {

            @Override
            public boolean isVisible() {
                return "manual".equals(nav.open);
            }

            @Override
            public boolean isActive() {
                return "manual".equals(nav.open);
            }
        };
        group.addWidget(new ImageWidget(0, 0, 292, 200, tex("manual", "slate")));
        String prefix = "gtna.originals.info." + machineId + ".";
        group.addWidget(new Paint(0, 0, 292, 200, (g, x, y) -> {
            text(g, Component.translatable("gtna.ui.o.manual").getString() + " - " +
                    Component.translatable("block.gtna." + machineId).getString(), x + 8, y + 18, 0xFFE8E8EC, true);
            if (sections.length == 0) return;
            int page = Math.min(nav.page, sections.length - 1);
            String[] sec = sections[page];
            text(g, Component.translatable(prefix + sec[0]).getString(), x + 82, y + 35, 0xFFF0BA28, true);
            var font = Minecraft.getInstance().font;
            int ly = y + 49;
            for (int i = 1; i < sec.length && ly < y + 176; i++) {
                boolean formula = sec[i].startsWith("=");
                var line = Component.translatable(prefix + (formula ? sec[i].substring(1) : sec[i]));
                var lines = font.split(line, 198);
                if (formula) g.fill(x + 80, ly - 2, x + 284, ly + lines.size() * 10, 0xFF0A1A0E);
                for (var l : lines) {
                    if (ly >= y + 176) break;
                    g.drawString(font, l, x + 82, ly, formula ? GREEN : 0xFFE0E0E4, false);
                    ly += 10;
                }
                ly += 4;
            }
            text(g, "< " + Component.translatable("gtna.ui.o.prev").getString(), x + 82, y + 180,
                    page > 0 ? 0xFFF0BA28 : 0xFF6A6C70, false);
            String next = Component.translatable("gtna.ui.o.next").getString() + " >";
            text(g, next, x + 280 - Minecraft.getInstance().font.width(next), y + 180,
                    page < sections.length - 1 ? 0xFFF0BA28 : 0xFF6A6C70, false);
        }));
        for (int i = 0; i < Math.min(9, sections.length); i++) {
            final int k = i;
            String title = sections[i][0];
            group.addWidget(new Tab(6, 32 + i * 18, k, nav, Component.translatable(prefix + title)));
        }
        group.addWidget(new ButtonWidget(80, 176, 60, 14, IGuiTexture.EMPTY,
                click -> nav.page = Math.max(0, nav.page - 1)));
        group.addWidget(new ButtonWidget(222, 176, 64, 14, IGuiTexture.EMPTY,
                click -> nav.page = Math.min(sections.length - 1, nav.page + 1)));
        group.addWidget(new Plate(LANCE, 276, 2, 12, 11, "close", null, () -> false, click -> nav.open = null));
        return group;
    }

    private static ResourceTexture tex(String dir, String name) {
        return new ResourceTexture(GTNACORE.id("textures/gui/originals_v2/" + dir + "/" + name + ".png").toString());
    }

    /** A chapter tab of the manual. */
    private static final class Tab extends ButtonWidget {

        private final int index;
        private final Nav nav;
        private final Component title;

        Tab(int x, int y, int index, Nav nav, Component title) {
            super(x, y, 66, 15, IGuiTexture.EMPTY, null);
            this.index = index;
            this.nav = nav;
            this.title = title;
            setOnPressCallback(click -> nav.page = index);
        }

        @Override
        @OnlyIn(Dist.CLIENT)
        public void drawInBackground(GuiGraphics g, int mouseX, int mouseY, float partialTicks) {
            var p = getPosition();
            boolean on = nav.page == index;
            tex("manual", on ? "tab_on" : "tab").draw(g, mouseX, mouseY, p.x, p.y, 66, 15);
            var font = Minecraft.getInstance().font;
            String s = (index + 1) + " " + title.getString();
            while (font.width(s) > 60 && s.length() > 3) s = s.substring(0, s.length() - 1);
            g.drawString(font, s, p.x + 4, p.y + 4, on ? 0xFF18140A : 0xFF9A9EA4, !on);
        }
    }

    // ------------------------------------------------------------------ widgets

    /** Draws a painter; no input. */
    public static final class Paint extends Widget {

        private final Painter painter;

        public Paint(int x, int y, int w, int h, Painter painter) {
            super(x, y, w, h);
            this.painter = painter;
        }

        @Override
        @OnlyIn(Dist.CLIENT)
        public void drawInBackground(GuiGraphics g, int mouseX, int mouseY, float partialTicks) {
            var p = getPosition();
            painter.paint(g, p.x, p.y);
        }
    }

    /** Swallows clicks over an open panel. */
    public static final class Blocker extends Widget {

        public Blocker(int x, int y, int w, int h) {
            super(x, y, w, h);
        }

        @Override
        @OnlyIn(Dist.CLIENT)
        public boolean mouseClicked(double mouseX, double mouseY, int button) {
            return isMouseOverElement(mouseX, mouseY);
        }
    }

    /** Chamfered plate button: texture by state, a 9 x 9 pixel icon, an optional label, a tooltip. */
    public static class Plate extends ButtonWidget {

        private final Theme theme;
        private final String icon;
        private final Component label;
        private final BooleanSupplier active;

        public Plate(Theme t, int x, int y, int w, int h, String icon, Component label, BooleanSupplier active,
                     Consumer<ClickData> onClick) {
            super(x, y, w, h, IGuiTexture.EMPTY, onClick);
            this.theme = t;
            this.icon = icon;
            this.label = label;
            this.active = active;
        }

        public Plate tip(String key) {
            setHoverTooltips(Component.translatable(key));
            return this;
        }

        @Override
        @OnlyIn(Dist.CLIENT)
        public void drawInBackground(GuiGraphics g, int mouseX, int mouseY, float partialTicks) {
            var p = getPosition();
            var s = getSize();
            boolean on = active.getAsBoolean();
            String base = s.width >= 50 ? "plate" : s.width >= 20 ? "wide" : "small";
            theme.tex(on && !base.equals("wide") ? base + "_on" : base).draw(g, mouseX, mouseY, p.x, p.y, s.width,
                    s.height);
            int colour = on ? theme.accent : isMouseOverElement(mouseX, mouseY) ? theme.glow : theme.dim;
            if (label != null) {
                Icons.draw(g, icon, p.x + 4, p.y + (s.height - 9) / 2, colour);
                g.drawString(Minecraft.getInstance().font, label, p.x + 16, p.y + (s.height - 8) / 2 + 1,
                        on ? theme.glow : theme.dim, true);
            } else {
                Icons.draw(g, icon, p.x + (s.width - 9) / 2, p.y + (s.height - 9) / 2, colour);
            }
        }
    }

    // ------------------------------------------------------------------ pixel drawing (GUI pixels, no smoothing)

    @OnlyIn(Dist.CLIENT)
    public static void px(GuiGraphics g, int x, int y, int c) {
        g.fill(x, y, x + 1, y + 1, c);
    }

    @OnlyIn(Dist.CLIENT)
    public static void text(GuiGraphics g, String s, int x, int y, int c, boolean shadow) {
        g.drawString(Minecraft.getInstance().font, s, x, y, c, shadow);
    }

    @OnlyIn(Dist.CLIENT)
    public static void right(GuiGraphics g, String s, int x, int y, int c) {
        g.drawString(Minecraft.getInstance().font, s, x - Minecraft.getInstance().font.width(s), y, c, false);
    }

    @OnlyIn(Dist.CLIENT)
    public static void centre(GuiGraphics g, String s, int x, int y, int c) {
        g.drawString(Minecraft.getInstance().font, s, x - Minecraft.getInstance().font.width(s) / 2, y, c, false);
    }

    /** Label left, value right, a 4 px bar below with a lighter top row. */
    @OnlyIn(Dist.CLIENT)
    public static void bar(GuiGraphics g, Theme t, int x, int y, int w, String label, String value, double frac,
                           int colour) {
        text(g, label, x, y, t.dim, false);
        right(g, value, x + w, y, t.glow);
        g.fill(x, y + 9, x + w, y + 13, 0xFF0E0C10);
        int f = (int) ((w - 2) * Math.max(0, Math.min(1, frac)));
        if (f > 0) {
            g.fill(x + 1, y + 10, x + 1 + f, y + 12, colour);
            g.fill(x + 1, y + 10, x + 1 + f, y + 11, lighter(colour));
        }
    }

    @OnlyIn(Dist.CLIENT)
    public static void chip(GuiGraphics g, int x, int y, int w, String s, int colour) {
        g.fill(x, y, x + w, y + 13, 0xFF0C0A0E);
        g.fill(x + 1, y + 1, x + w - 1, y + 12, 0xFF000000);
        g.fill(x + 1, y + 1, x + 2, y + 12, colour);
        centre(g, s, x + w / 2 + 1, y + 3, colour);
    }

    @OnlyIn(Dist.CLIENT)
    public static void disc(GuiGraphics g, int cx, int cy, int r, int c) {
        for (int y = -r; y <= r; y++) {
            int half = (int) Math.round(Math.sqrt(Math.max(0, r * r - y * y)));
            g.fill(cx - half, cy + y, cx + half + 1, cy + y + 1, c);
        }
    }

    @OnlyIn(Dist.CLIENT)
    public static void ellipse(GuiGraphics g, int cx, int cy, double rx, double ry, int c, int dotted) {
        int n = (int) (2 * Math.PI * Math.max(rx, ry) * 1.5);
        for (int k = 0; k < n; k++) {
            if (dotted > 0 && (k / dotted) % 2 == 1) continue;
            double a = 2 * Math.PI * k / n;
            px(g, (int) Math.round(cx + rx * Math.cos(a)), (int) Math.round(cy + ry * Math.sin(a)), c);
        }
    }

    private static final double[][] BAYER = { { 0, 8, 2, 10 }, { 12, 4, 14, 6 }, { 3, 11, 1, 9 }, { 15, 7, 13, 5 } };

    /** A glow as an ordered-dither falloff, pixel-art light without blur. */
    @OnlyIn(Dist.CLIENT)
    public static void glow(GuiGraphics g, int cx, int cy, int r, int c, double strength) {
        for (int y = -r; y <= r; y++)
            for (int x = -r; x <= r; x++) {
                double d = Math.hypot(x, y) / r;
                if (d >= 1) continue;
                if (Math.pow(1 - d, 1.6) * strength > BAYER[Math.floorMod(cy + y, 4)][Math.floorMod(cx + x, 4)] / 16)
                    px(g, cx + x, cy + y, c);
            }
    }

    /** Bresenham line. */
    @OnlyIn(Dist.CLIENT)
    public static void line(GuiGraphics g, int x0, int y0, int x1, int y1, int c) {
        int dx = Math.abs(x1 - x0), dy = -Math.abs(y1 - y0), sx = x0 < x1 ? 1 : -1, sy = y0 < y1 ? 1 : -1;
        int err = dx + dy;
        for (int guard = 0; guard < 4000; guard++) {
            px(g, x0, y0, c);
            if (x0 == x1 && y0 == y1) return;
            int e2 = 2 * err;
            if (e2 >= dy) {
                err += dy;
                x0 += sx;
            }
            if (e2 <= dx) {
                err += dx;
                y0 += sy;
            }
        }
    }

    public static int lighter(int c) {
        int a = c >>> 24, r = Math.min(255, ((c >> 16) & 255) + 60), gg = Math.min(255, ((c >> 8) & 255) + 60),
                b = Math.min(255, (c & 255) + 60);
        return a << 24 | r << 16 | gg << 8 | b;
    }

    public static int dim(int c, double f) {
        int r = (int) (((c >> 16) & 255) * f), gg = (int) (((c >> 8) & 255) * f), b = (int) ((c & 255) * f);
        return 0xFF000000 | r << 16 | gg << 8 | b;
    }

    public static String sci(double v) {
        return v >= 1e5 || (v > 0 && v < 0.01) ? String.format("%.2e", v) : String.format("%.1f", v);
    }

    // ------------------------------------------------------------------ 9 x 9 icons

    /** Pixel icons of the plate buttons, as in the mockups. */
    public static final class Icons {

        private static final Map<String, String[]> ICONS = new HashMap<>();

        static {
            put("left", "....#....", "...##....", "..###....", ".####....", "#####....", ".####....", "..###....",
                    "...##....", "....#....");
            put("right", "....#....", "....##...", "....###..", "....####.", "....#####", "....####.", "....###..",
                    "....##...", "....#....");
            put("auto", ".#######.", "#.......#", "#..###..#", "#.#...#.#", "#.#####.#", "#.#...#.#", "#.#...#.#",
                    "#.......#", ".#######.");
            put("orbit", "..#####..", ".#.....#.", "#...#...#", "#..###..#", "#.#####.#", "#..###..#", "#...#...#",
                    ".#.....#.", "..#####..");
            put("gear", "...#.#...", ".#.###.#.", "..#####..", "###...###", ".##.#.##.", "###...###", "..#####..",
                    ".#.###.#.", "...#.#...");
            put("capsule", "...###...", "..#####..", "..#####..", "..#####..", "..#####..", ".#######.", ".#.###.#.",
                    "#...#...#", ".........");
            put("info", "...###...", "...###...", ".........", "..####...", "...###...", "...###...", "...###...",
                    "..#####..", ".........");
            put("power", "....#....", ".#..#..#.", "#...#...#", "#...#...#", "#.......#", "#.......#", "#.......#",
                    ".#.....#.", "..#####..");
            put("minus", ".........", ".........", ".........", ".........", "#########", ".........", ".........",
                    ".........", ".........");
            put("plus", "....#....", "....#....", "....#....", "....#....", "#########", "....#....", "....#....",
                    "....#....", "....#....");
            put("bolt", "....###..", "...###...", "..###....", ".#######.", "....###..", "...###...", "..###....",
                    ".##......", "#........");
            put("chart", "#........", "#......#.", "#.....#..", "#..#.#...", "#.#.#....", "##.......", "#........",
                    "#########", ".........");
            put("wave", ".........", ".........", "....#....", "...#.#...", "#.#...#.#", ".#.....#.", ".........",
                    ".........", ".........");
            put("star", "....#....", "....#....", "...###...", "#########", ".#######.", "..#####..", ".###.###.",
                    ".##...##.", "#.......#");
            put("swap", "..#......", ".##......", "#########", ".##......", "..#...#..", "......##.", "#########",
                    "......##.", "......#..");
            put("atom", "#.......#", ".#.....#.", "..#####..", "..#.#.#..", "..##.##..", "..#.#.#..", "..#####..",
                    ".#.....#.", "#.......#");
            put("list", "##.######", ".........", "##.######", ".........", "##.######", ".........", "##.######",
                    ".........", ".........");
            put("open", "..#####..", ".#.....#.", "#..###..#", "#.#...#.#", "#.#.#.#.#", "#.#...#.#", "#..###..#",
                    ".#.....#.", "..#####..");
            put("close", "#.......#", ".#.....#.", "..#...#..", "...#.#...", "....#....", "...#.#...", "..#...#..",
                    ".#.....#.", "#.......#");
            put("note", "....####.", "....#..#.", "....#..#.", "....#..#.", "....#..#.", "..###.##.", ".####.##.",
                    ".###.....", ".........");
            put("map", "#...#...#", "#..##..##", "#.#.#.#.#", "##..##..#", "#...#...#", "#...#...#", "#...#...#",
                    "#...#...#", ".........");
            put("down", "....#....", "....#....", "....#....", "....#....", "#...#...#", ".#..#..#.", "..#.#.#..",
                    "...###...", "....#....");
            put("snow", "....#....", ".#..#..#.", "..#.#.#..", "...###...", "#########", "...###...", "..#.#.#..",
                    ".#..#..#.", "....#....");
            put("ring", "..#####..", ".#.....#.", "#.......#", "#.......#", "#.......#", "#.......#", "#.......#",
                    ".#.....#.", "..#####..");
        }

        private static void put(String name, String... rows) {
            ICONS.put(name, rows);
        }

        @OnlyIn(Dist.CLIENT)
        public static void draw(GuiGraphics g, String name, int x, int y, int colour) {
            String[] rows = ICONS.get(name);
            if (rows == null) return;
            for (int j = 0; j < rows.length; j++) {
                String row = rows[j];
                int start = -1;
                for (int i = 0; i <= row.length(); i++) {
                    boolean on = i < row.length() && row.charAt(i) == '#';
                    if (on && start < 0) start = i;
                    if (!on && start >= 0) {
                        g.fill(x + start, y + j, x + i, y + j + 1, colour);
                        start = -1;
                    }
                }
            }
        }
    }

    /** Several widgets built from a list (keeps the per-machine builders short). */
    public static void addAll(WidgetGroup root, List<? extends Widget> widgets) {
        for (var w : widgets) root.addWidget(w);
    }

    public static <T> List<T> list() {
        return new ArrayList<>();
    }

    /** A click region with no art (bodies on the map, harmonics on the wheel...). */
    public static ButtonWidget hit(int x, int y, int w, int h, Consumer<ClickData> onClick) {
        return new ButtonWidget(x, y, w, h, IGuiTexture.EMPTY, onClick);
    }

    /** Lazily computed value for painters (client side). */
    public static <T> Supplier<T> memo(Supplier<T> s) {
        return s;
    }
}
