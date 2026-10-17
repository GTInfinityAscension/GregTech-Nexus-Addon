package com.raishxn.gtna.mixin.client;

import com.lowdragmc.lowdraglib.gui.widget.SlotWidget;

import net.minecraft.network.chat.Component;

import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.gen.Accessor;

import java.util.List;
import java.util.function.BiConsumer;

/** Reads the slot's extra-tooltip hook so GTNA can chain onto GTCEu's (chance, tier) instead of replacing it. */
@Mixin(value = SlotWidget.class, remap = false)
public interface SlotWidgetTooltipAccessor {

    @Accessor("onAddedTooltips")
    BiConsumer<SlotWidget, List<Component>> gtna$getOnAddedTooltips();
}
