package com.raishxn.gtna.gametest;

import com.gregtechceu.gtceu.api.capability.recipe.ItemRecipeCapability;
import com.gregtechceu.gtceu.api.recipe.GTRecipe;

import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.world.item.Items;
import net.minecraftforge.gametest.GameTestHolder;
import net.minecraftforge.gametest.PrefixGameTestTemplate;

import java.io.IOException;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.List;

/**
 * Fails when a GTNA recipe has an item input that resolves to nothing (missing item or empty tag): EMI shows it as
 * an empty slot and the recipe can never run. The full list goes to {@code gtna-empty-ingredients.txt}.
 */
@PrefixGameTestTemplate(false)
@GameTestHolder("gtna")
public final class GTNAEmptyIngredientGameTests {

    private GTNAEmptyIngredientGameTests() {}

    @GameTest(template = "empty_12", timeoutTicks = 200)
    public static void noEmptyItemInputs(GameTestHelper helper) {
        List<String> broken = new ArrayList<>();
        for (var recipe : helper.getLevel().getServer().getRecipeManager().getRecipes()) {
            if (!(recipe instanceof GTRecipe gt) || !"gtna".equals(gt.getId().getNamespace())) continue;
            var inputs = gt.getInputContents(ItemRecipeCapability.CAP);
            for (int i = 0; i < inputs.size(); i++) {
                var stacks = ItemRecipeCapability.CAP.of(inputs.get(i).content).getItems();
                boolean empty = true;
                // EN: Forge shows an empty tag as a barrier named "Empty Tag", so a barrier counts as missing.
                // PT: O Forge mostra tag vazia como uma barreira "Empty Tag"; barreira conta como faltando.
                // ZH: Forge 将空标签显示为名为 "Empty Tag" 的屏障，因此屏障视为缺失。
                for (var stack : stacks) if (!stack.isEmpty() && !stack.is(Items.BARRIER)) empty = false;
                if (empty) broken.add(
                        gt.getId() + " slot " + i + " " + ItemRecipeCapability.CAP.of(inputs.get(i).content).toJson());
            }
        }
        try {
            Files.write(helper.getLevel().getServer().getServerDirectory().toPath()
                    .resolve("gtna-empty-ingredients.txt"), broken);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        helper.assertTrue(broken.isEmpty(), broken.size() + " empty item inputs, first: " +
                (broken.isEmpty() ? "" : broken.get(0)));
        helper.succeed();
    }
}
