package com.raishxn.gtna.client;

import com.gregtechceu.gtceu.api.capability.recipe.IO;
import com.gregtechceu.gtceu.api.capability.recipe.ItemRecipeCapability;
import com.gregtechceu.gtceu.api.gui.WidgetUtils;
import com.gregtechceu.gtceu.api.recipe.GTRecipe;

import com.lowdragmc.lowdraglib.gui.widget.SlotWidget;
import com.lowdragmc.lowdraglib.gui.widget.WidgetGroup;

import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;

import com.raishxn.gtna.api.bec.NaniteTier;
import com.raishxn.gtna.common.machine.multiblock.electric.bec.BECIONodeMachine;
import com.raishxn.gtna.mixin.client.SlotWidgetTooltipAccessor;

/** Condensate Assembly XEI page: shows each item slot's nanite tier in that slot's tooltip. */
public final class CondensateNaniteSlots {

    private CondensateNaniteSlots() {}

    public static void attach(GTRecipe recipe, WidgetGroup group) {
        int[] tiers = BECIONodeMachine.nanitesOf(recipe.data);
        if (tiers.length == 0) return;
        WidgetUtils.widgetByIdForEach(group, "^%s_[0-9]+$".formatted(ItemRecipeCapability.CAP.slotName(IO.IN)),
                SlotWidget.class, slot -> {
                    int index = WidgetUtils.widgetIdIndex(slot);
                    if (index < 0 || index >= tiers.length) return;
                    var tier = NaniteTier.byOrdinal(tiers[index]);
                    var line = Component.translatable("gtna.recipe.bec_nanite_tier",
                            tier == null ? "?" : String.valueOf(tier.tier)).withStyle(ChatFormatting.LIGHT_PURPLE);
                    var previous = ((SlotWidgetTooltipAccessor) slot).gtna$getOnAddedTooltips();
                    slot.setOnAddedTooltips((widget, lines) -> {
                        if (previous != null) previous.accept(widget, lines);
                        lines.add(line);
                    });
                });
    }
}
