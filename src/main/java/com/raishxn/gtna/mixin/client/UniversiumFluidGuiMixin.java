package com.raishxn.gtna.mixin.client;

import com.lowdragmc.lowdraglib.gui.util.DrawerHelper;
import com.lowdragmc.lowdraglib.side.fluid.FluidStack;

import net.minecraft.client.gui.GuiGraphics;

import com.raishxn.gtna.client.renderer.material.UniversiumRenderer;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

@Mixin(value = DrawerHelper.class, remap = false)
public class UniversiumFluidGuiMixin {

    @Inject(method = "drawFluidForGui(Lnet/minecraft/client/gui/GuiGraphics;Lcom/lowdragmc/lowdraglib/side/fluid/FluidStack;FFFF)V",
            at = @At("TAIL"))
    private static void gtna$renderUniversiumFluid(GuiGraphics graphics, FluidStack fluid, float x, float y,
                                                   float width, float height, CallbackInfo ci) {
        if (!fluid.isEmpty() && UniversiumRenderer.isFluid(fluid.getFluid())) {
            UniversiumRenderer.renderFluidGui(graphics, x, y, width, height);
        }
    }
}
