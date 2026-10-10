package com.raishxn.gtna.mixin.client;

import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.resources.model.BakedModel;
import net.minecraft.world.inventory.InventoryMenu;
import net.minecraft.world.item.ItemDisplayContext;
import net.minecraft.world.item.ItemStack;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import org.spongepowered.asm.mixin.Final;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Pseudo;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/** Apply configured glow color using the vanilla atlas pipeline, without shader global state. */
@Pseudo
@Mixin(targets = "committee.nova.mods.renderblender.client.model.GlowEdgeBakedModel", remap = false)
public class RenderBlenderGlowMixin {

    @Shadow
    @Final
    private BakedModel parentModel;
    @Shadow
    @Final
    private int glowColor;
    @Shadow
    @Final
    private float glowWidth;
    @Shadow
    @Final
    private float glowOffset;

    @Inject(method = "renderGlowEdge", at = @At("HEAD"), cancellable = true)
    private void gtna$renderColoredGlow(ItemStack stack, ItemDisplayContext context, PoseStack pose,
                                        MultiBufferSource buffers, int light, int overlay, CallbackInfo ci) {
        var id = net.minecraft.core.registries.BuiltInRegistries.ITEM.getKey(stack.getItem());
        if (!id.getNamespace().equals("gtna")) return;
        pose.pushPose();
        pose.translate(-glowWidth * 0.025f, -glowWidth * 0.025f + glowOffset, -0.001f);
        float scale = 1 + glowWidth * 0.05f;
        pose.scale(scale, scale, 1);
        VertexConsumer delegate = buffers.getBuffer(RenderType.entityTranslucent(InventoryMenu.BLOCK_ATLAS));
        VertexConsumer colored = new VertexConsumer() {

            public VertexConsumer vertex(double x, double y, double z) {
                delegate.vertex(x, y, z);
                return this;
            }

            public VertexConsumer color(int r, int g, int b, int a) {
                delegate.color((glowColor >> 16) & 255, (glowColor >> 8) & 255, glowColor & 255, a);
                return this;
            }

            public VertexConsumer uv(float u, float v) {
                delegate.uv(u, v);
                return this;
            }

            public VertexConsumer overlayCoords(int u, int v) {
                delegate.overlayCoords(u, v);
                return this;
            }

            public VertexConsumer uv2(int u, int v) {
                delegate.uv2(240, 240);
                return this;
            }

            public VertexConsumer normal(float x, float y, float z) {
                delegate.normal(x, y, z);
                return this;
            }

            public void endVertex() {
                delegate.endVertex();
            }

            public void defaultColor(int r, int g, int b, int a) {
                delegate.defaultColor((glowColor >> 16) & 255, (glowColor >> 8) & 255, glowColor & 255, a);
            }

            public void unsetDefaultColor() {
                delegate.unsetDefaultColor();
            }
        };
        Minecraft.getInstance().getItemRenderer().renderModelLists(parentModel, stack, 15728880, overlay, pose,
                colored);
        pose.popPose();
        ci.cancel();
    }
}
