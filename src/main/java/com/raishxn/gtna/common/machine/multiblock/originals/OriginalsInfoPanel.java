package com.raishxn.gtna.common.machine.multiblock.originals;

import com.lowdragmc.lowdraglib.gui.texture.ColorRectTexture;
import com.lowdragmc.lowdraglib.gui.texture.IGuiTexture;
import com.lowdragmc.lowdraglib.gui.widget.DraggableScrollableWidgetGroup;
import com.lowdragmc.lowdraglib.gui.widget.Widget;
import com.lowdragmc.lowdraglib.gui.widget.WidgetGroup;

import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.api.distmarker.OnlyIn;

import com.raishxn.gtna.client.renderer.GTNATextures;
import com.raishxn.gtna.common.machine.multiblock.godforge.gui.GodforgeGui;
import com.raishxn.gtna.common.machine.multiblock.godforge.gui.GodforgeGui.WrappedText;
import org.jetbrains.annotations.Nullable;

import java.util.HashMap;
import java.util.Map;

/**
 * How-it-works panel of the original multiblocks, in the style of the Forge of Gods' general info: purple section
 * headers, gold text, green formulas and a clickable table of contents. Opened from the GTNA logo of the machine
 * screen; it lives only on the client (no widget sync), like the logo itself.
 */
public final class OriginalsInfoPanel extends WidgetGroup {

    private static final String KEY = "gtna.originals.info.";
    /** Per machine: sections of {header, line keys}; a line key starting with '=' is a formula. */
    private static final Map<String, String[][]> SECTIONS = new HashMap<>();

    static {
        SECTIONS.put("stellar_containment_chamber", new String[][] {
                { "overview", "overview.1" },
                { "build", "build.1", "build.2" },
                { "power", "power.1", "=power.2", "power.3", "=power.4" },
                { "feeding", "feeding.1", "=feeding.2", "feeding.3" },
                { "quakes", "quakes.1", "quakes.2", "quakes.3" },
                { "limits", "limits.1", "=limits.2", "limits.3" } });
        SECTIONS.put("antimatter_collider_ring", new String[][] {
                { "overview", "overview.1" },
                { "build", "build.1", "build.2" },
                { "power", "=power.1", "=power.2", "power.3" },
                { "modes", "modes.1", "modes.2", "=modes.3" },
                { "proposals", "proposals.1", "proposals.2" } });
        SECTIONS.put("dimensional_rift_gate", new String[][] {
                { "overview", "overview.1" },
                { "build", "build.1" },
                { "power", "=power.1", "power.2", "=power.3" },
                { "tuning", "tuning.1", "=tuning.2", "=tuning.3", "tuning.4" },
                { "harmonics", "harmonics.1", "harmonics.2" } });
        SECTIONS.put("kinetic_orbital_lance", new String[][] {
                { "overview", "overview.1" },
                { "build", "build.1", "build.2" },
                { "power", "power.1", "=power.2", "power.3", "=power.4" },
                { "targets", "targets.1", "targets.2" },
                { "bench", "bench.1", "bench.2" } });
    }

    /** Whether the machine with this id path has a panel. */
    public static boolean has(String machine) {
        return SECTIONS.containsKey(machine);
    }

    /** The panel of the screen opened last (dev command {@code /gtna_dev_info}). */
    @Nullable
    public static OriginalsInfoPanel last;

    public OriginalsInfoPanel(String machine, int width, int height) {
        super(0, 0, width, height);
        last = this;
        setBackground(GodforgeGui.tex("background_white_glow"));
        setVisible(false);
        setActive(false);
        String[][] sections = SECTIONS.get(machine);
        String prefix = KEY + machine + ".";
        int textW = width - 22;
        addWidget(new WrappedText(6, 6, textW - 30, 10, () -> Component.translatable(KEY + "title")
                .withStyle(ChatFormatting.GOLD, ChatFormatting.BOLD), false, 1f));
        addWidget(new Click(width - 44, 4, 40, 12, () -> Component.translatable(KEY + "close"), this::toggle));
        var scroll = new DraggableScrollableWidgetGroup(6, 20, width - 12, height - 26);
        scroll.setYScrollBarWidth(3).setYBarStyle(IGuiTexture.EMPTY, new ColorRectTexture(0x80FFFFFF));
        int y = 0;
        scroll.addWidget(new WrappedText(0, y, textW, 10, () -> Component.translatable(KEY + "toc")
                .withStyle(ChatFormatting.AQUA, ChatFormatting.BOLD), false, 1f));
        y += 13;
        int tocY = y;
        y += sections.length * 11 + 8;
        for (int s = 0; s < sections.length; s++) {
            String[] section = sections[s];
            final int target = y;
            Component header = Component.translatable(prefix + section[0]).withStyle(ChatFormatting.DARK_PURPLE,
                    ChatFormatting.BOLD, ChatFormatting.UNDERLINE);
            Component entry = Component.literal("› ").append(Component.translatable(prefix + section[0]))
                    .withStyle(ChatFormatting.AQUA);
            scroll.addWidget(new Click(0, tocY + s * 11, textW, 10, () -> entry,
                    () -> scroll.setScrollYOffset(target)));
            scroll.addWidget(new WrappedText(0, y, textW, 10, () -> header, false, 1f));
            y += 14;
            for (int i = 1; i < section.length; i++) {
                boolean formula = section[i].startsWith("=");
                Component line = Component.translatable(prefix + (formula ? section[i].substring(1) : section[i]))
                        .withStyle(formula ? ChatFormatting.GREEN : ChatFormatting.GOLD);
                int h = height(line, textW);
                scroll.addWidget(new WrappedText(formula ? 6 : 0, y, textW - (formula ? 6 : 0), h, () -> line,
                        false, 1f));
                y += h + 6;
            }
            y += 4;
        }
        addWidget(scroll);
    }

    /** Wrapped height; only the client can measure, the integrated server just reserves one line. */
    private static int height(Component text, int width) {
        if (!com.lowdragmc.lowdraglib.LDLib.isRemote()) return 9;
        var font = net.minecraft.client.Minecraft.getInstance().font;
        return Math.max(1, font.split(text, width).size()) * font.lineHeight;
    }

    public void toggle() {
        boolean open = !isVisible();
        setVisible(open);
        setActive(open);
    }

    /** Swallows clicks over the open panel so the machine screen under it does not react. */
    @Override
    @OnlyIn(Dist.CLIENT)
    public boolean mouseClicked(double mouseX, double mouseY, int button) {
        return super.mouseClicked(mouseX, mouseY, button) || isMouseOverElement(mouseX, mouseY);
    }

    /** The GTNA logo of an original's screen: opens and closes the panel. */
    public static Widget logoButton(int x, int y, OriginalsInfoPanel panel) {
        var logo = new Click(x, y, GTNATextures.LOGO_SIZE, GTNATextures.LOGO_SIZE, null, panel::toggle);
        logo.setBackground(GTNATextures.LOGO);
        logo.setHoverTooltips(Component.translatable(KEY + "hint"));
        return logo;
    }

    /** Client-only clickable text or image: no server round trip, the panel is purely informative. */
    private static final class Click extends Widget {

        @Nullable
        private final java.util.function.Supplier<Component> text;
        private final Runnable action;

        Click(int x, int y, int w, int h, @Nullable java.util.function.Supplier<Component> text, Runnable action) {
            super(x, y, w, h);
            this.text = text;
            this.action = action;
        }

        @Override
        @OnlyIn(Dist.CLIENT)
        public void drawInBackground(net.minecraft.client.gui.GuiGraphics g, int mouseX, int mouseY,
                                     float partialTicks) {
            super.drawInBackground(g, mouseX, mouseY, partialTicks);
            if (text == null) return;
            var p = getPosition();
            var font = net.minecraft.client.Minecraft.getInstance().font;
            var t = text.get();
            if (isMouseOverElement(mouseX, mouseY)) t = t.copy().withStyle(ChatFormatting.UNDERLINE);
            g.drawString(font, t, p.x, p.y + 1, 0xFFFFFF, false);
        }

        @Override
        @OnlyIn(Dist.CLIENT)
        public boolean mouseClicked(double mouseX, double mouseY, int button) {
            if (!isMouseOverElement(mouseX, mouseY)) return false;
            action.run();
            playButtonClickSound();
            return true;
        }
    }
}
