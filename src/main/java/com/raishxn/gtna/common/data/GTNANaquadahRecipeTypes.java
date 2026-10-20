package com.raishxn.gtna.common.data;

import com.gregtechceu.gtceu.api.capability.recipe.IO;
import com.gregtechceu.gtceu.api.gui.GuiTextures;
import com.gregtechceu.gtceu.api.recipe.GTRecipeType;
import com.gregtechceu.gtceu.common.data.GTRecipeTypes;
import com.gregtechceu.gtceu.common.data.GTSoundEntries;

import static com.lowdragmc.lowdraglib.gui.texture.ProgressTexture.FillDirection.LEFT_TO_RIGHT;

/** Recipe types of the naquadah reactor ladder ({@link GTNANaquadahReactors}): fuel in, EU out. */
public final class GTNANaquadahRecipeTypes {

    private GTNANaquadahRecipeTypes() {}

    public static final GTRecipeType LARGE_NAQUADAH_REACTOR_RECIPES = GTNARecipeType.register(
            "large_naquadah_reactor", GTRecipeTypes.MULTIBLOCK)
            .setMaxIOSize(0, 0, 2, 0).setEUIO(IO.OUT)
            .setProgressBar(GuiTextures.PROGRESS_BAR_ARROW, LEFT_TO_RIGHT).setSound(GTSoundEntries.ARC);

    public static final GTRecipeType NAQUADAH_HYPER_REACTOR_RECIPES = GTNARecipeType.register(
            "naquadah_hyper_reactor", GTRecipeTypes.MULTIBLOCK)
            .setMaxIOSize(0, 0, 2, 0).setEUIO(IO.OUT)
            .setProgressBar(GuiTextures.PROGRESS_BAR_ARROW, LEFT_TO_RIGHT).setSound(GTSoundEntries.ARC);

    public static void init() {}
}
