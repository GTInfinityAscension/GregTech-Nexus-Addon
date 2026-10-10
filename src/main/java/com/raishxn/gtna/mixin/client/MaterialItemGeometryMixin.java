package com.raishxn.gtna.mixin.client;

import net.minecraft.client.renderer.block.model.BlockModel;
import net.minecraft.client.renderer.block.model.ItemModelGenerator;
import net.minecraft.client.renderer.texture.TextureAtlasSprite;
import net.minecraft.client.resources.model.Material;

import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

import java.util.function.Function;

/** Retain custom geometry inherited by GTCEu's generated material item models. */
@Mixin(ItemModelGenerator.class)
public class MaterialItemGeometryMixin {

    @Inject(method = "generateBlockModel", at = @At("RETURN"))
    private void gtna$retainMaterialEffects(Function<Material, TextureAtlasSprite> sprites, BlockModel original,
                                            CallbackInfoReturnable<BlockModel> cir) {
        var texture = original.getMaterial("layer0").texture();
        if (texture.getNamespace().equals("gtceu") &&
                texture.getPath().startsWith("item/material_sets/gtna_")) {
            var geometry = original.customData.getCustomGeometry();
            if (geometry != null) {
                cir.getReturnValue().customData.setCustomGeometry(geometry);
            }
        }
    }
}
