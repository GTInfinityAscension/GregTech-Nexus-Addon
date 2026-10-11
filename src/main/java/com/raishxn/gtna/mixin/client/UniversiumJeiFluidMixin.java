package com.raishxn.gtna.mixin.client;

import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.renderer.texture.TextureAtlasSprite;

import com.raishxn.gtna.client.renderer.material.UniversiumRenderer;
import mezz.jei.api.gui.drawable.TilingDirection;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Pseudo;
import org.spongepowered.asm.mixin.Unique;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/**
 * Draws the animated Universium fluid over JEI fluid tanks. {@code FluidTankRenderer.drawTiledSprite} has a
 * {@link TilingDirection} parameter from JEI 15.32 on and none before, so there is one injection per signature, each
 * with its exact descriptor and optional: whichever JEI 15.x is installed, one matches and the other is skipped.
 */
@Pseudo
@Mixin(targets = "mezz.jei.library.render.FluidTankRenderer", remap = false)
public class UniversiumJeiFluidMixin {

    @Inject(method = "drawTiledSprite(Lnet/minecraft/client/gui/GuiGraphics;IIIJLnet/minecraft/client/renderer/texture/TextureAtlasSprite;Lmezz/jei/api/gui/drawable/TilingDirection;II)V",
            at = @At("TAIL"),
            require = 0,
            expect = 0)
    private static void gtna$universiumJei(GuiGraphics graphics, int width, int height, int color, long amount,
                                           TextureAtlasSprite sprite, TilingDirection direction, int x, int y,
                                           CallbackInfo ci) {
        gtna$overlay(graphics, width, height, amount, sprite, x, y);
    }

    /** JEI 15.31 and older. */
    @Inject(method = "drawTiledSprite(Lnet/minecraft/client/gui/GuiGraphics;IIIJLnet/minecraft/client/renderer/texture/TextureAtlasSprite;II)V",
            at = @At("TAIL"),
            require = 0,
            expect = 0)
    private static void gtna$universiumJeiOld(GuiGraphics graphics, int width, int height, int color, long amount,
                                              TextureAtlasSprite sprite, int x, int y, CallbackInfo ci) {
        gtna$overlay(graphics, width, height, amount, sprite, x, y);
    }

    @Unique
    private static void gtna$overlay(GuiGraphics graphics, int width, int height, long amount,
                                     TextureAtlasSprite sprite, int x, int y) {
        var id = sprite.contents().name();
        if (id.getNamespace().equals("gtna") && id.getPath().equals("block/fluids/fluid.universium")) {
            int filled = (int) Math.min(height, amount);
            UniversiumRenderer.renderFluidGui(graphics, x, y + height - filled, width, filled, 101);
        }
    }
}
