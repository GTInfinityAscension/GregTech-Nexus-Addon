package com.raishxn.gtna.common.machine.multiblock.part.bec;

import com.gregtechceu.gtceu.api.gui.GuiTextures;

import com.lowdragmc.lowdraglib.gui.texture.GuiTextureGroup;
import com.lowdragmc.lowdraglib.gui.texture.TextTexture;
import com.lowdragmc.lowdraglib.gui.widget.ButtonWidget;
import com.lowdragmc.lowdraglib.gui.widget.LabelWidget;
import com.lowdragmc.lowdraglib.gui.widget.Widget;

import java.util.function.Supplier;

/** Small widgets shared by the BEC hatches' settings panels. */
final class BECUi {

    private BECUi() {}

    static Widget label(int x, int y, Supplier<String> text) {
        return new LabelWidget(x, y, text);
    }

    /** A button showing {@code text}; {@code onServerClick} runs on the server only. */
    static Widget button(int x, int y, int width, Supplier<String> text, Runnable onServerClick) {
        return new ButtonWidget(x, y, width, 14,
                new GuiTextureGroup(GuiTextures.BUTTON, new TextTexture(text).setWidth(width)),
                click -> {
                    if (!click.isRemote) onServerClick.run();
                });
    }
}
