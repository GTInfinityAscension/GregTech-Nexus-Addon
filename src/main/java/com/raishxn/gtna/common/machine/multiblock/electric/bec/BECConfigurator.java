package com.raishxn.gtna.common.machine.multiblock.electric.bec;

import com.gregtechceu.gtceu.api.gui.GuiTextures;
import com.gregtechceu.gtceu.api.gui.fancy.IFancyConfigurator;

import com.lowdragmc.lowdraglib.gui.texture.IGuiTexture;
import com.lowdragmc.lowdraglib.gui.widget.Widget;
import com.lowdragmc.lowdraglib.gui.widget.WidgetGroup;

import net.minecraft.network.chat.Component;

import java.util.function.Supplier;

/** The "parameters" window of a BEC multiblock (GTNH's parameter panel). */
record BECConfigurator(String titleKey, Supplier<WidgetGroup> widget) implements IFancyConfigurator {

    @Override
    public Component getTitle() {
        return Component.translatable(titleKey);
    }

    @Override
    public IGuiTexture getIcon() {
        return GuiTextures.BUTTON_LIST;
    }

    @Override
    public Widget createConfigurator() {
        return widget.get();
    }
}
