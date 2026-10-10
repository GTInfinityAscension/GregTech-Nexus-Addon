package com.raishxn.gtna.mixin.client;

import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.renderer.texture.TextureAtlasSprite;

import com.raishxn.gtna.client.renderer.material.UniversiumRenderer;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Pseudo;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

@Pseudo
@Mixin(targets = "mezz.jei.library.render.FluidTankRenderer", remap = false)
public class UniversiumJeiFluidMixin {

    @Inject(method = "drawTiledSprite", at = @At("TAIL"))
    private static void gtna$universiumJei(GuiGraphics graphics, int width, int height, int color, long amount,
                                           TextureAtlasSprite sprite, int x, int y, CallbackInfo ci) {
        var id = sprite.contents().name();
        if (id.getNamespace().equals("gtna") && id.getPath().equals("block/fluids/fluid.universium")) {
            int filled = (int) Math.min(height, amount);
            UniversiumRenderer.renderFluidGui(graphics, x, y + height - filled, width, filled, 101);
        }
    }
}
