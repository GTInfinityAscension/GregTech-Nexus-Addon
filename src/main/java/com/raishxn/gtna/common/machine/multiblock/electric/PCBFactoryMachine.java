package com.raishxn.gtna.common.machine.multiblock.electric;

import com.gregtechceu.gtceu.api.machine.IMachineBlockEntity;
import com.gregtechceu.gtceu.api.pattern.BlockPattern;
import com.gregtechceu.gtceu.api.recipe.modifier.ModifierFunction;
import com.gregtechceu.gtceu.api.recipe.modifier.RecipeModifier;

import com.lowdragmc.lowdraglib.syncdata.annotation.DescSynced;
import com.lowdragmc.lowdraglib.syncdata.annotation.Persisted;
import com.lowdragmc.lowdraglib.syncdata.field.ManagedFieldHolder;

import net.minecraft.core.Direction;
import net.minecraft.network.chat.Component;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.phys.BlockHitResult;

import com.raishxn.gtna.api.machine.multiblock.GTNAStructureRefresh;
import com.raishxn.gtna.common.data.GTNAMegaMachines;

import java.util.List;

/**
 * GTO {@code PCBFactoryMachine}: three structures (tier 1 to 3), each one larger. The tier caps the recipe EU/t as in
 * GTO: tier 1 up to {@link #TIER_1_MAX_EUT}, tier 2 up to {@link #TIER_2_MAX_EUT}, tier 3 unlimited. GTO picks the
 * tier from Gold / Orichalcum / Enderium nanites in a controller slot; GTNA has no Orichalcum or Enderium nanites, so
 * the tier is chosen with a screwdriver on the controller (the structure of that tier must then be built).
 */
public class PCBFactoryMachine extends WorkableElectricMultipleRecipesMachine {

    protected static final ManagedFieldHolder MANAGED_FIELD_HOLDER = new ManagedFieldHolder(
            PCBFactoryMachine.class, WorkableElectricMultipleRecipesMachine.MANAGED_FIELD_HOLDER);

    public static final long TIER_1_MAX_EUT = 30719;
    public static final long TIER_2_MAX_EUT = 491519;

    @Persisted
    @DescSynced
    private int machineTier = 1;

    public PCBFactoryMachine(IMachineBlockEntity holder) {
        super(holder);
    }

    @Override
    public ManagedFieldHolder getFieldHolder() {
        return MANAGED_FIELD_HOLDER;
    }

    public int getMachineTier() {
        return machineTier;
    }

    public void setMachineTier(int tier) {
        machineTier = Math.max(1, Math.min(3, tier));
    }

    @Override
    public BlockPattern getPattern() {
        return GTNAMegaMachines.pcbFactoryPattern(machineTier, getDefinition());
    }

    @Override
    protected InteractionResult onScrewdriverClick(Player playerIn, InteractionHand hand, Direction gridSide,
                                                   BlockHitResult hitResult) {
        if (isRemote()) return InteractionResult.SUCCESS;
        setMachineTier(machineTier % 3 + 1);
        playerIn.sendSystemMessage(Component.translatable("gtna.machine.pcb_factory.tier", machineTier));
        GTNAStructureRefresh.refresh(this, true);
        return InteractionResult.CONSUME;
    }

    /** The highest recipe EU/t the current tier runs ({@link Long#MAX_VALUE} for tier 3). */
    public static long maxEUt(int tier) {
        return tier < 2 ? TIER_1_MAX_EUT : tier < 3 ? TIER_2_MAX_EUT : Long.MAX_VALUE;
    }

    /** GTO {@code getRealRecipe}: a recipe above the tier's EU/t cap is not run (checked before overclocking). */
    @Override
    public RecipeModifier getRecipeModifier() {
        RecipeModifier base = super.getRecipeModifier();
        return (machine, recipe) -> recipe.getInputEUt().getTotalEU() > maxEUt(machineTier) ?
                ModifierFunction.cancel(Component.translatable("gtna.machine.pcb_factory.tier_too_low")) :
                base.getModifier(machine, recipe);
    }

    @Override
    public void addDisplayText(List<Component> textList) {
        super.addDisplayText(textList);
        textList.add(Component.translatable("gtna.machine.pcb_factory.tier", machineTier));
    }
}
