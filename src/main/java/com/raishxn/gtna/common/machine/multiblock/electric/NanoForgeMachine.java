package com.raishxn.gtna.common.machine.multiblock.electric;

import com.gregtechceu.gtceu.api.machine.IMachineBlockEntity;
import com.gregtechceu.gtceu.api.machine.MetaMachine;
import com.gregtechceu.gtceu.api.machine.feature.multiblock.IMultiPart;
import com.gregtechceu.gtceu.api.machine.multiblock.WorkableElectricMultiblockMachine;
import com.gregtechceu.gtceu.api.recipe.GTRecipe;
import com.gregtechceu.gtceu.api.recipe.modifier.ModifierFunction;
import com.gregtechceu.gtceu.common.data.GTRecipeModifiers;
import com.gregtechceu.gtceu.common.machine.multiblock.part.ItemBusPartMachine;

import net.minecraft.network.chat.Component;
import net.minecraft.world.item.Item;

import com.raishxn.gtna.api.machine.multiblock.IGTNAModuleHost;
import com.raishxn.gtna.common.data.GTNANanoForge;
import org.jetbrains.annotations.NotNull;

import java.util.List;

/**
 * GTNH {@code MTENanoForge}, tiers 1-3. GTNH reads the tier from the nanite in the controller slot and the built
 * pieces; GTCEu controllers have no slot, so the nanite (Carbon, Neutronium or Transcendent Metal) sits in any input
 * bus, is never consumed, and the tier is the lower of the nanite tier and the built pieces (tier 2 and tier 3
 * extensions). Recipes of a lower tier than the machine overclock perfectly, as in GTNH.
 * <p>
 * Tier 4 (MagMatter Nanites and the tier-4 extension): when an input bus holds a nanite equal to the recipe's output
 * (and no nanites the recipe doesn't use), the forge drains all molten MagMatter from its input hatches and spends one
 * of those nanites; parallel {@code MagMatter / (288 / 2^(4 - recipe tier))}, duration {@code x 0.9999^parallel}.
 * Perfect overclock below tier 3 when the forge is above the recipe, and for tier-3 recipes only with that parallel.
 * The modifier only measures; the MagMatter and nanite are taken when the recipe starts ({@link #beforeWorking}).
 */
public class NanoForgeMachine extends WorkableElectricMultiblockMachine {

    public static final String TIER = "nano_forge_tier";

    public NanoForgeMachine(IMachineBlockEntity holder, Object... args) {
        super(holder, args);
    }

    /** 1 + the tier extensions formed in order. */
    public int getStructureTier() {
        long mask = ((IGTNAModuleHost) (Object) this).gtna$formedModuleMask();
        int tier = 1;
        while (tier < 4 && (mask & (1L << (tier - 1))) != 0) tier++;
        return tier;
    }

    public int getNaniteTier() {
        Item[] nanites = GTNANanoForge.tierNanites();
        int best = 0;
        for (IMultiPart part : getParts()) {
            if (!(part instanceof ItemBusPartMachine bus)) continue;
            var storage = bus.getInventory().storage;
            for (int slot = 0; slot < storage.getSlots(); slot++) {
                var stack = storage.getStackInSlot(slot);
                for (int t = nanites.length; t > best; t--) {
                    if (stack.is(nanites[t - 1])) best = t;
                }
            }
        }
        return best;
    }

    public int getNanoTier() {
        return Math.min(getStructureTier(), getNaniteTier());
    }

    public static @NotNull ModifierFunction nanoTier(@NotNull MetaMachine machine, @NotNull GTRecipe recipe) {
        if (!(machine instanceof NanoForgeMachine forge)) return ModifierFunction.NULL;
        int required = Math.max(1, recipe.data.getInt(TIER));
        int tier = forge.getNanoTier();
        if (tier < required) {
            return ModifierFunction.cancel(Component.translatable("gtna.machine.nano_forge.low_tier", required));
        }
        int parallel = tier >= 4 ? forge.magMatterParallel(recipe, required) : 1;
        boolean perfect = (tier < 4 || required < 3) && tier > required || required == 3 && parallel > 1;
        var overclock = (perfect ? GTRecipeModifiers.OC_PERFECT : GTRecipeModifiers.OC_NON_PERFECT)
                .getModifier(machine, recipe);
        if (parallel <= 1 && tier < 4) return overclock;
        var magmatter = ModifierFunction.builder()
                .modifyAllContents(com.gregtechceu.gtceu.api.recipe.content.ContentModifier.multiplier(parallel))
                .eutMultiplier(parallel).parallels(parallel)
                .durationMultiplier(Math.pow(0.9999, parallel)).build();
        return magmatter.andThen(overclock);
    }

    /** GTNH tier-4 parallel the MagMatter in the input hatches would give this recipe, or 1. */
    int magMatterParallel(GTRecipe recipe, int recipeTier) {
        if (findOutputNanite(recipe) == null) return 1;
        long magmatter = magMatterAmount(false);
        long perParallel = 288L >> (4 - Math.min(4, recipeTier));
        return (int) Math.max(1, Math.min(Integer.MAX_VALUE, magmatter / Math.max(1, perParallel)));
    }

    /** The bus slot holding a nanite equal to the recipe's output, when no foreign nanite is present. */
    @org.jetbrains.annotations.Nullable
    private int[] findOutputNanite(GTRecipe recipe) {
        var outputs = recipe.getOutputContents(com.gregtechceu.gtceu.api.capability.recipe.ItemRecipeCapability.CAP);
        if (outputs.isEmpty()) return null;
        var output = com.gregtechceu.gtceu.api.capability.recipe.ItemRecipeCapability.CAP.of(outputs.get(0).content)
                .getItems();
        if (output.length == 0 || !GTNANanoForge.isNanite(output[0].getItem())) return null;
        java.util.Set<Item> inputNanites = new java.util.HashSet<>();
        for (var content : recipe.getInputContents(
                com.gregtechceu.gtceu.api.capability.recipe.ItemRecipeCapability.CAP)) {
            for (var stack : com.gregtechceu.gtceu.api.capability.recipe.ItemRecipeCapability.CAP.of(content.content)
                    .getItems()) {
                if (GTNANanoForge.isNanite(stack.getItem())) inputNanites.add(stack.getItem());
            }
        }
        int[] found = null;
        int index = 0;
        for (IMultiPart part : getParts()) {
            if (part instanceof ItemBusPartMachine bus) {
                var storage = bus.getInventory().storage;
                for (int slot = 0; slot < storage.getSlots(); slot++) {
                    var stack = storage.getStackInSlot(slot);
                    if (stack.isEmpty() || !GTNANanoForge.isNanite(stack.getItem())) continue;
                    if (stack.is(output[0].getItem())) found = new int[] { index, slot };
                    else if (!inputNanites.contains(stack.getItem()) && !isTierNanite(stack.getItem())) return null;
                }
            }
            index++;
        }
        return found;
    }

    private static boolean isTierNanite(Item item) {
        for (Item nanite : GTNANanoForge.tierNanites()) if (nanite == item) return true;
        return false;
    }

    /** Molten MagMatter in the input hatches; drains it all when {@code drain}. */
    private long magMatterAmount(boolean drain) {
        var magmatter = com.raishxn.gtna.common.data.GTNAMaterials.MagMatter.getFluid(1).getFluid();
        long total = 0;
        for (IMultiPart part : getParts()) {
            for (var handlerList : part.getRecipeHandlers()) {
                if (!handlerList.isValid(com.gregtechceu.gtceu.api.capability.recipe.IO.IN)) continue;
                for (var handler : handlerList.getCapability(
                        com.gregtechceu.gtceu.api.capability.recipe.FluidRecipeCapability.CAP)) {
                    if (!(handler instanceof com.gregtechceu.gtceu.api.machine.trait.NotifiableFluidTank tank))
                        continue;
                    for (int t = 0; t < tank.getTanks(); t++) {
                        var fluid = tank.getFluidInTank(t);
                        if (fluid.getFluid() != magmatter) continue;
                        total += fluid.getAmount();
                        if (drain) tank.drainInternal(fluid.copy(),
                                net.minecraftforge.fluids.capability.IFluidHandler.FluidAction.EXECUTE);
                    }
                }
            }
        }
        return total;
    }

    @Override
    public boolean beforeWorking(@org.jetbrains.annotations.Nullable GTRecipe recipe) {
        if (recipe != null && getNanoTier() >= 4) {
            int[] nanite = findOutputNanite(recipe);
            if (nanite != null && magMatterAmount(false) > 0) {
                magMatterAmount(true);
                if (getParts().get(nanite[0]) instanceof ItemBusPartMachine bus) {
                    bus.getInventory().storage.extractItem(nanite[1], 1, false);
                }
            }
        }
        return super.beforeWorking(recipe);
    }

    @Override
    public void addDisplayText(List<Component> textList) {
        super.addDisplayText(textList);
        if (!isFormed()) return;
        textList.add(Component.translatable("gtna.machine.nano_forge.tier", getNanoTier(), getStructureTier(),
                getNaniteTier()));
    }
}
