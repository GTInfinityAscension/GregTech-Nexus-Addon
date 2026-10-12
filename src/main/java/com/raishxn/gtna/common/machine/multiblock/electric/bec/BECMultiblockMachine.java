package com.raishxn.gtna.common.machine.multiblock.electric.bec;

import com.gregtechceu.gtceu.api.machine.IMachineBlockEntity;
import com.gregtechceu.gtceu.api.machine.feature.multiblock.IMultiPart;
import com.gregtechceu.gtceu.api.machine.multiblock.WorkableElectricMultiblockMachine;
import com.gregtechceu.gtceu.api.recipe.GTRecipe;
import com.gregtechceu.gtceu.data.recipe.builder.GTRecipeBuilder;
import com.gregtechceu.gtceu.utils.FormattingUtil;

import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.world.level.Level;

import com.raishxn.gtna.api.bec.BECNetwork;
import com.raishxn.gtna.api.bec.CondensateList;
import com.raishxn.gtna.api.bec.CondensateType;
import com.raishxn.gtna.api.bec.IBECHatch;
import com.raishxn.gtna.api.bec.IBECNode;
import com.raishxn.gtna.common.machine.multiblock.part.bec.BECHatchPartMachine;
import org.jetbrains.annotations.Nullable;

import java.util.ArrayList;
import java.util.List;

/** GTNH {@code MTEBECMultiblockBase}: a BEC multiblock on the condensate network. */
public abstract class BECMultiblockMachine extends WorkableElectricMultiblockMachine implements IBECNode {

    protected BECMultiblockMachine(IMachineBlockEntity holder, Object... args) {
        super(holder, args);
    }

    @Override
    public Level getBECLevel() {
        return getLevel();
    }

    @Override
    public boolean isBECFormed() {
        return isFormed() && connectsToNetwork();
    }

    /** The Teleportation Node is not a network element (GTNH {@code connectsToNetwork}). */
    protected boolean connectsToNetwork() {
        return true;
    }

    @Override
    public List<? extends IBECHatch> getBECHatches() {
        List<BECHatchPartMachine> out = new ArrayList<>();
        for (IMultiPart part : getParts()) if (part instanceof BECHatchPartMachine hatch) out.add(hatch);
        return out;
    }

    @Override
    public void onStructureFormed() {
        super.onStructureFormed();
        BECNetwork.invalidate();
    }

    @Override
    public void onStructureInvalid() {
        super.onStructureInvalid();
        BECNetwork.invalidate();
    }

    @Override
    public void onUnload() {
        super.onUnload();
        BECNetwork.invalidate();
    }

    /** Every recipe of a type (GTNH looks recipe maps up directly). */
    protected java.util.Collection<GTRecipe> allRecipes(com.gregtechceu.gtceu.api.recipe.GTRecipeType type) {
        return getLevel() == null ? java.util.List.of() : getLevel().getRecipeManager().getAllRecipesFor(type);
    }

    /** A recipe with no inputs that only keeps the machine running for {@code duration} ticks at {@code eut}. */
    protected static GTRecipe cycle(String id, long voltage, long amperage, int duration) {
        var builder = GTRecipeBuilder.ofRaw().id(com.raishxn.gtna.GTNACORE.id("bec/" + id)).duration(duration);
        if (amperage > 0) builder.EUt(voltage, amperage);
        return builder.buildRawRecipe();
    }

    /** GTNH condensate readout: "Available Condensate:" and one line per condensate. */
    protected static void addCondensateText(List<Component> text, String titleKey, @Nullable CondensateList list) {
        text.add(Component.translatable(titleKey).withStyle(ChatFormatting.GRAY));
        if (list == null || list.isEmpty()) {
            text.add(Component.literal("  ").append(Component.translatable("gtna.bec.gui.none"))
                    .withStyle(ChatFormatting.GRAY));
            return;
        }
        for (var e : list.object2LongEntrySet()) {
            text.add(Component.literal("  ").append(condensateName(e.getKey()).copy().withStyle(ChatFormatting.AQUA))
                    .append(Component.literal(" x ").withStyle(ChatFormatting.GRAY))
                    .append(Component.literal(FormattingUtil.formatNumbers(e.getLongValue()) + " mB")
                            .withStyle(ChatFormatting.GOLD)));
        }
    }

    /** GTNH {@code CondensateType.getCondensateName}: the short name for condensates, the fluid name otherwise. */
    public static Component condensateName(net.minecraft.world.level.material.Fluid fluid) {
        CondensateType type = CondensateType.getCondensateType(fluid);
        if (type != null) return Component.translatable("gtna.bec.condensate." + type.id);
        return new net.minecraftforge.fluids.FluidStack(fluid, 1).getDisplayName();
    }
}
