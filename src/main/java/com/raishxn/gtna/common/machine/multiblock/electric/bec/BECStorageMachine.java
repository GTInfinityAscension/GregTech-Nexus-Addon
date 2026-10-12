package com.raishxn.gtna.common.machine.multiblock.electric.bec;

import com.gregtechceu.gtceu.api.gui.fancy.ConfiguratorPanel;
import com.gregtechceu.gtceu.api.gui.widget.LongInputWidget;
import com.gregtechceu.gtceu.api.machine.IMachineBlockEntity;
import com.gregtechceu.gtceu.api.machine.feature.multiblock.IMultiPart;
import com.gregtechceu.gtceu.api.machine.trait.RecipeLogic;
import com.gregtechceu.gtceu.api.recipe.GTRecipe;
import com.gregtechceu.gtceu.utils.FormattingUtil;

import com.lowdragmc.lowdraglib.gui.widget.LabelWidget;
import com.lowdragmc.lowdraglib.gui.widget.WidgetGroup;
import com.lowdragmc.lowdraglib.syncdata.annotation.DescSynced;
import com.lowdragmc.lowdraglib.syncdata.annotation.Persisted;
import com.lowdragmc.lowdraglib.syncdata.field.ManagedFieldHolder;

import net.minecraft.ChatFormatting;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;

import com.raishxn.gtna.api.bec.BECInventory;
import com.raishxn.gtna.api.bec.CondensateList;
import com.raishxn.gtna.api.bec.CondensateStack;
import com.raishxn.gtna.common.machine.multiblock.part.bec.CondensateDetectorHatchPartMachine;
import org.jetbrains.annotations.NotNull;

import java.util.Collections;
import java.util.Iterator;
import java.util.List;

/**
 * GTNH {@code MTEBECStorage} (Bose-Einstein Condensate Containment Field). Capacity is the field strength, set in the
 * parameters: 1 field strength holds 1 mB and costs 1 EU/t. Every second, if it holds more than its field strength,
 * each stored condensate keeps 9/10 of its amount. If the field loses power or is switched off, its contents are
 * voided.
 */
public class BECStorageMachine extends BECMultiblockMachine implements BECInventory {

    protected static final ManagedFieldHolder MANAGED_FIELD_HOLDER = new ManagedFieldHolder(
            BECStorageMachine.class, BECMultiblockMachine.MANAGED_FIELD_HOLDER);

    @Persisted
    @DescSynced
    private long fieldStrength = 1;
    private final CondensateList stored = new CondensateList();
    private boolean contentsChanged;

    public BECStorageMachine(IMachineBlockEntity holder, Object... args) {
        super(holder, args);
    }

    @Override
    public ManagedFieldHolder getFieldHolder() {
        return MANAGED_FIELD_HOLDER;
    }

    @Override
    protected RecipeLogic createRecipeLogic(Object... args) {
        return new RecipeLogic(this) {

            @Override
            public @NotNull Iterator<GTRecipe> searchRecipe() {
                if (!isFormed()) return Collections.emptyIterator();
                long voltage = Math.max(1, getMaxVoltage());
                long amps = Math.max(1, (fieldStrength + voltage - 1) / voltage);
                return List.of(cycle("containment_field", Math.min(voltage, fieldStrength), amps, 20)).iterator();
            }

            @Override
            public void setStatus(Status status) {
                super.setStatus(status);
                if (status == Status.WAITING || status == Status.SUSPEND) voidContents();
            }
        };
    }

    @Override
    public boolean alwaysTryModifyRecipe() {
        return false;
    }

    /** GTNH {@code checkProcessing_EM}: the decay runs when each one-second cycle starts. */
    @Override
    public boolean beforeWorking(GTRecipe recipe) {
        if (!super.beforeWorking(recipe)) return false;
        if (getAmountStored() > fieldStrength) {
            stored.replaceAll((fluid, amount) -> amount * 9 / 10);
            stored.object2LongEntrySet().removeIf(e -> e.getLongValue() <= 0);
            contentsChanged = true;
        }
        refreshDetectors();
        return true;
    }

    private boolean running() {
        return isFormed() && !getRecipeLogic().isWaiting() && !getRecipeLogic().isSuspend();
    }

    private void voidContents() {
        if (!stored.isEmpty()) {
            stored.clear();
            contentsChanged = true;
            refreshDetectors();
        }
    }

    @Override
    public void onStructureInvalid() {
        super.onStructureInvalid();
        stored.clear();
    }

    public double getAmountStored() {
        double sum = 0;
        for (long l : stored.values()) sum += l;
        return sum;
    }

    public long getFieldStrength() {
        return fieldStrength;
    }

    public void setFieldStrength(long strength) {
        fieldStrength = Math.max(1, strength);
        getRecipeLogic().markLastRecipeDirty();
    }

    @Override
    public CondensateList getContents() {
        return stored;
    }

    @Override
    public double getCondensateCapacity() {
        return fieldStrength;
    }

    @Override
    public void addCondensate(CondensateStack request) {
        if (!running()) {
            voidContents();
            return;
        }
        stored.addTo(request.fluid, request.amount);
        request.amount = 0;
        contentsChanged = true;
        refreshDetectors();
    }

    @Override
    public boolean removeCondensate(CondensateStack request) {
        if (!running()) {
            voidContents();
            return false;
        }
        long have = stored.getLong(request.fluid);
        if (have <= 0) return false;
        long taken = Math.min(have, request.amount);
        request.amount -= taken;
        have -= taken;
        if (have == 0) stored.removeLong(request.fluid);
        else stored.put(request.fluid, have);
        contentsChanged = true;
        refreshDetectors();
        return request.amount == 0;
    }

    private void refreshDetectors() {
        if (!contentsChanged) return;
        contentsChanged = false;
        for (IMultiPart part : getParts())
            if (part instanceof CondensateDetectorHatchPartMachine detector) detector.updateAmount(this);
    }

    @Override
    public void onStructureFormed() {
        super.onStructureFormed();
        for (IMultiPart part : getParts())
            if (part instanceof CondensateDetectorHatchPartMachine detector) detector.bindStorage(this);
    }

    @Override
    public void saveCustomPersistedData(@NotNull CompoundTag tag, boolean forDrop) {
        super.saveCustomPersistedData(tag, forDrop);
        tag.put("condensate", stored.save());
    }

    @Override
    public void loadCustomPersistedData(@NotNull CompoundTag tag) {
        super.loadCustomPersistedData(tag);
        stored.load(tag.getCompound("condensate"));
    }

    @Override
    public void addDisplayText(List<Component> textList) {
        super.addDisplayText(textList);
        if (!isFormed()) return;
        textList.add(Component.translatable("gtna.bec.gui.field_strength",
                FormattingUtil.formatNumbers(fieldStrength)).withStyle(ChatFormatting.GRAY));
        textList.add(Component.translatable("gtna.bec.gui.stored",
                FormattingUtil.formatNumbers((long) getAmountStored())).withStyle(ChatFormatting.GRAY));
        addCondensateText(textList, "gtna.bec.gui.stored_condensate", stored);
    }

    @Override
    public void attachConfigurators(ConfiguratorPanel panel) {
        super.attachConfigurators(panel);
        panel.attachConfigurators(new BECConfigurator("gtna.bec.gui.parameters", () -> {
            var group = new WidgetGroup(0, 0, 160, 40);
            group.addWidget(new LabelWidget(4, 4, "gtna.bec.gui.field_strength_param"));
            group.addWidget(new LongInputWidget(4, 18, 152, 14, this::getFieldStrength, this::setFieldStrength)
                    .setMin(1L));
            return group;
        }));
    }
}
