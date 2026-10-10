package com.raishxn.gtna.mixin.client;

import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.screens.Screen;

import com.raishxn.gtna.integration.jei.EyeOfHarmonyCategory;
import com.raishxn.gtna.integration.jei.EyeOfHarmonyJeiHeight;
import mezz.jei.api.recipe.category.IRecipeCategory;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Pseudo;
import org.spongepowered.asm.mixin.Unique;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/**
 * Optional JEI: the taller recipe window ({@link JeiRecipeGuiHeightMixin}) applies only while the Eye of Harmony
 * category is selected. JEI sizes the window in {@code init()}; when the selected category switches to or from the
 * EOH one, the layout update re-runs {@code init()} through {@code resize} so the frame grows or shrinks back.
 */
@Pseudo
@Mixin(targets = "mezz.jei.gui.recipes.RecipesGui", remap = false)
public abstract class JeiRecipesGuiEohMixin {

    @Inject(method = "updateLayout", at = @At("HEAD"), cancellable = true, require = 0)
    private void gtna$matchEyeOfHarmonyHeight(CallbackInfo ci) {
        boolean eoh = gtna$isEyeOfHarmonySelected();
        if (eoh == EyeOfHarmonyJeiHeight.active) return;
        EyeOfHarmonyJeiHeight.active = eoh;
        ci.cancel();
        Screen screen = (Screen) (Object) this;
        screen.resize(Minecraft.getInstance(), screen.width, screen.height);
    }

    @Unique
    private boolean gtna$isEyeOfHarmonySelected() {
        try {
            var field = this.getClass().getDeclaredField("logic");
            field.setAccessible(true);
            Object logic = field.get(this);
            Object category = logic.getClass().getMethod("getSelectedRecipeCategory").invoke(logic);
            return category instanceof IRecipeCategory<?> recipeCategory &&
                    EyeOfHarmonyCategory.TYPE.equals(recipeCategory.getRecipeType());
        } catch (ReflectiveOperationException | RuntimeException e) {
            return false;
        }
    }
}
