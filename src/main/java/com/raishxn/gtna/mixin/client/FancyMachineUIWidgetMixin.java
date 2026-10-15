package com.raishxn.gtna.mixin.client;

import com.gregtechceu.gtceu.api.gui.fancy.FancyMachineUIWidget;
import com.gregtechceu.gtceu.api.gui.fancy.IFancyUIProvider;
import com.gregtechceu.gtceu.api.machine.MetaMachine;
import com.gregtechceu.gtceu.api.machine.multiblock.MultiblockControllerMachine;

import com.lowdragmc.lowdraglib.gui.widget.Widget;
import com.lowdragmc.lowdraglib.gui.widget.WidgetGroup;

import com.raishxn.gtna.GTNACORE;
import com.raishxn.gtna.client.renderer.GTNATextures;
import com.raishxn.gtna.common.machine.multiblock.originals.OriginalsInfoPanel;
import org.spongepowered.asm.mixin.Final;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.Unique;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/**
 * Draws the GTNA logo in the bottom-right corner of every GTNA multiblock's fancy UI.
 *
 * <p>
 * The logo was only added to the custom steam {@code ModularUI}s (G-0049). Electric, no-energy and
 * the fancy steam machines build their screen through GTCEu's {@link FancyMachineUIWidget} instead,
 * so they never got it. Hooking the shared setup covers every GTNA multiblock at once (including
 * future ones) without touching each controller.
 *
 * <p>
 * Client-only: {@code FancyMachineUIWidget} and the logo widget are client classes.
 */
@Mixin(FancyMachineUIWidget.class)
public abstract class FancyMachineUIWidgetMixin {

    @Shadow(remap = false)
    @Final
    protected IFancyUIProvider mainPage;

    @Shadow(remap = false)
    protected WidgetGroup pageContainer;

    @Inject(method = "setupFancyUI(Lcom/gregtechceu/gtceu/api/gui/fancy/IFancyUIProvider;Z)V",
            at = @At("RETURN"),
            remap = false)
    private void gtna$addLogo(IFancyUIProvider fancyUI, boolean showInventory, CallbackInfo ci) {
        // setupFancyUI() is called on every page navigation, but it clears the page container and
        // creates a fresh page widget first, so this always leaves exactly one logo.
        if (!(mainPage instanceof MetaMachine machine) || !(machine instanceof MultiblockControllerMachine)) {
            return;
        }
        if (!GTNACORE.MOD_ID.equals(machine.getDefinition().getId().getNamespace())) {
            return;
        }
        // Put the logo in the page (content) widget, flush with its bottom-right corner, so it sits
        // inside the machine's display area instead of on the padding above the player inventory.
        WidgetGroup target = pageContainer;
        if (!pageContainer.widgets.isEmpty()) {
            Widget page = pageContainer.widgets.get(pageContainer.widgets.size() - 1);
            if (page instanceof WidgetGroup pageGroup) {
                target = pageGroup;
            }
        }
        int x = Math.max(0, target.getSize().width - GTNATextures.LOGO_SIZE - 2);
        int y = Math.max(0, target.getSize().height - GTNATextures.LOGO_SIZE - 2);
        String id = machine.getDefinition().getId().getPath();
        if (!OriginalsInfoPanel.has(id)) {
            target.addWidget(GTNATextures.logo(x, y));
            return;
        }
        // Originals: the logo opens the how-it-works panel, laid over the whole screen.
        var self = (WidgetGroup) (Object) this;
        if (gtna$infoPanel != null) self.removeWidget(gtna$infoPanel);
        gtna$infoPanel = new OriginalsInfoPanel(id, self.getSize().width, self.getSize().height);
        self.addWidget(gtna$infoPanel);
        target.addWidget(OriginalsInfoPanel.logoButton(x, y, gtna$infoPanel));
    }

    @Unique
    private OriginalsInfoPanel gtna$infoPanel;
}
