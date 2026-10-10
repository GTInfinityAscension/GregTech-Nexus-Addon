package com.raishxn.gtna.mixin.client;

import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.entity.ItemRenderer;
import net.minecraft.client.resources.model.BakedModel;
import net.minecraft.world.item.ItemDisplayContext;
import net.minecraft.world.item.ItemStack;

import com.mojang.blaze3d.vertex.PoseStack;
import com.raishxn.gtna.client.renderer.material.UniversiumRenderer;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Unique;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

@Mixin(ItemRenderer.class)
public class UniversiumItemRendererMixin {

    @Unique
    private boolean gtna$universiumRendered;

    @Inject(method = "render", at = @At("HEAD"))
    private void gtna$beginUniversiumItem(ItemStack stack, ItemDisplayContext context, boolean left,
                                          PoseStack pose, MultiBufferSource buffers, int light, int overlay,
                                          BakedModel model, CallbackInfo ci) {
        gtna$universiumRendered = false;
    }

    @Inject(method = "render",
            at = @At(value = "INVOKE",
                     target = "Lnet/minecraft/client/renderer/entity/ItemRenderer;renderModelLists(Lnet/minecraft/client/resources/model/BakedModel;Lnet/minecraft/world/item/ItemStack;IILcom/mojang/blaze3d/vertex/PoseStack;Lcom/mojang/blaze3d/vertex/VertexConsumer;)V",
                     shift = At.Shift.AFTER))
    private void gtna$renderUniversiumForms(ItemStack stack, ItemDisplayContext context, boolean left,
                                            PoseStack pose, MultiBufferSource buffers, int light, int overlay,
                                            BakedModel model, CallbackInfo ci) {
        if (!gtna$universiumRendered) {
            gtna$universiumRendered = true;
            UniversiumRenderer.renderItem(stack, context, model, pose, buffers);
        }
    }
}
