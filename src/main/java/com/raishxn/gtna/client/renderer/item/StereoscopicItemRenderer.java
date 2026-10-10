package com.raishxn.gtna.client.renderer.item;

import com.gregtechceu.gtceu.api.item.MaterialBlockItem;
import com.gregtechceu.gtceu.api.item.TagPrefixItem;

import net.minecraft.world.item.ItemStack;
import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.api.distmarker.OnlyIn;

import com.raishxn.gtna.common.data.material.GodforgeChainMaterials;
import com.raishxn.gtna.common.data.material.GodforgeIconSets;

/**
 * Checks whether an item stack should receive the stereoscopic 3D rotating transformation in GUI render passes.
 * Mirrors GTLCore and GTOCore's stereoscopic item behavior for Transcendent Metal.
 */
@OnlyIn(Dist.CLIENT)
public final class StereoscopicItemRenderer {

    private StereoscopicItemRenderer() {}

    public static boolean isStereoscopic(ItemStack stack) {
        if (stack.isEmpty()) return false;
        var item = stack.getItem();
        if (item instanceof TagPrefixItem tagItem) {
            return tagItem.material.getMaterialIconSet() == GodforgeIconSets.TRANSCENDENT_METAL ||
                    tagItem.material == GodforgeChainMaterials.TranscendentMetal;
        }
        if (item instanceof MaterialBlockItem blockItem) {
            return blockItem.material.getMaterialIconSet() == GodforgeIconSets.TRANSCENDENT_METAL ||
                    blockItem.material == GodforgeChainMaterials.TranscendentMetal;
        }
        return false;
    }
}
