package com.raishxn.gtna.mixin.client;

import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.entity.ItemRenderer;
import net.minecraft.client.resources.model.BakedModel;
import net.minecraft.world.item.ItemDisplayContext;
import net.minecraft.world.item.ItemStack;

import com.mojang.blaze3d.vertex.PoseStack;
import com.raishxn.gtna.client.renderer.effect.ItemEffectRenderer;
import com.raishxn.gtna.client.renderer.material.UniversiumRenderer;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Unique;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/** Draws GTNA item effects around the icon, once per render call even when the model has several passes. */
@Mixin(ItemRenderer.class)
public class ItemEffectRendererMixin {

    @Unique
    private boolean gtna$behindRendered;
    @Unique
    private boolean gtna$overRendered;

    @Inject(method = "render", at = @At("HEAD"))
    private void gtna$beginItem(ItemStack stack, ItemDisplayContext context, boolean left, PoseStack pose,
                                MultiBufferSource buffers, int light, int overlay, BakedModel model,
                                CallbackInfo ci) {
        gtna$behindRendered = false;
        gtna$overRendered = false;
    }

    @Inject(method = "render",
            at = @At(value = "INVOKE",
                     target = "Lnet/minecraft/client/renderer/entity/ItemRenderer;renderModelLists(Lnet/minecraft/client/resources/model/BakedModel;Lnet/minecraft/world/item/ItemStack;IILcom/mojang/blaze3d/vertex/PoseStack;Lcom/mojang/blaze3d/vertex/VertexConsumer;)V"))
    private void gtna$renderBehind(ItemStack stack, ItemDisplayContext context, boolean left, PoseStack pose,
                                   MultiBufferSource buffers, int light, int overlay, BakedModel model,
                                   CallbackInfo ci) {
        if (!gtna$behindRendered) {
            gtna$behindRendered = true;
            ItemEffectRenderer.renderBehind(stack, context, model, pose, buffers, overlay);
        }
    }

    @Inject(method = "render",
            at = @At(value = "INVOKE",
                     target = "Lnet/minecraft/client/renderer/entity/ItemRenderer;renderModelLists(Lnet/minecraft/client/resources/model/BakedModel;Lnet/minecraft/world/item/ItemStack;IILcom/mojang/blaze3d/vertex/PoseStack;Lcom/mojang/blaze3d/vertex/VertexConsumer;)V",
                     shift = At.Shift.AFTER))
    private void gtna$renderOver(ItemStack stack, ItemDisplayContext context, boolean left, PoseStack pose,
                                 MultiBufferSource buffers, int light, int overlay, BakedModel model,
                                 CallbackInfo ci) {
        if (!gtna$overRendered) {
            gtna$overRendered = true;
            ItemEffectRenderer.renderOver(stack, context, model, pose, buffers);
            UniversiumRenderer.renderItem(stack, context, model, pose, buffers);
        }
    }
}
