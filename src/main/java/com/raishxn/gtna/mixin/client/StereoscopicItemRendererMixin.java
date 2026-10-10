package com.raishxn.gtna.mixin.client;

import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.entity.ItemRenderer;
import net.minecraft.client.resources.model.BakedModel;
import net.minecraft.world.item.ItemDisplayContext;
import net.minecraft.world.item.ItemStack;

import com.mojang.blaze3d.vertex.PoseStack;
import com.raishxn.gtna.client.renderer.item.StereoscopicItemRenderer;
import org.joml.Quaternionf;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/**
 * Applies real-time 3D stereoscopic matrix rotation to Transcendent Metal items in GUI display context,
 * exactly matching GTLCore, GTOCore, and GTNH rendering.
 */
@Mixin(ItemRenderer.class)
public class StereoscopicItemRendererMixin {

    @Inject(
            method = "render",
            at = @At(
                     value = "INVOKE",
                     target = "Lcom/mojang/blaze3d/vertex/PoseStack;translate(FFF)V",
                     shift = At.Shift.AFTER))
    private void gtna$rotateStereoscopicItem(
                                             ItemStack itemStack,
                                             ItemDisplayContext displayContext,
                                             boolean leftHand,
                                             PoseStack poseStack,
                                             MultiBufferSource buffer,
                                             int combinedLight,
                                             int combinedOverlay,
                                             BakedModel model,
                                             CallbackInfo ci) {
        if (displayContext == ItemDisplayContext.GUI && StereoscopicItemRenderer.isStereoscopic(itemStack)) {
            poseStack.mulPose(
                    new Quaternionf().fromAxisAngleDeg(0.3f, 0.5f, 0.2f, (System.currentTimeMillis() / 25) % 360));
        }
    }
}
