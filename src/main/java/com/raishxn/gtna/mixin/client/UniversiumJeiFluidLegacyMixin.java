package com.raishxn.gtna.mixin.client;

import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.renderer.texture.TextureAtlasSprite;

import com.raishxn.gtna.client.renderer.material.UniversiumRenderer;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Pseudo;
import org.spongepowered.asm.mixin.Unique;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/** {@link UniversiumJeiFluidMixin} for JEI 15.31 and older, whose {@code drawTiledSprite} has no tiling direction. */
@Pseudo
@Mixin(targets = "mezz.jei.library.render.FluidTankRenderer", remap = false)
public class UniversiumJeiFluidLegacyMixin {

    @Inject(method = "drawTiledSprite(Lnet/minecraft/client/gui/GuiGraphics;IIIJLnet/minecraft/client/renderer/texture/TextureAtlasSprite;II)V",
            at = @At("TAIL"),
            require = 0,
            expect = 0)
    private static void gtna$universiumJeiOld(GuiGraphics graphics, int width, int height, int color, long amount,
                                              TextureAtlasSprite sprite, int x, int y, CallbackInfo ci) {
        gtna$overlay(width, height, amount, sprite, x, y, graphics);
    }

    @Unique
    private static void gtna$overlay(int width, int height, long amount, TextureAtlasSprite sprite, int x, int y,
                                     GuiGraphics graphics) {
        var id = sprite.contents().name();
        if (id.getNamespace().equals("gtna") && id.getPath().equals("block/fluids/fluid.universium")) {
            int filled = (int) Math.min(height, amount);
            UniversiumRenderer.renderFluidGui(graphics, x, y + height - filled, width, filled, 101);
        }
    }
}
