package com.raishxn.gtna.common.machine.multiblock.part;

import com.gregtechceu.gtceu.api.GTValues;
import com.gregtechceu.gtceu.api.capability.recipe.IO;
import com.gregtechceu.gtceu.api.machine.IMachineBlockEntity;
import com.gregtechceu.gtceu.api.machine.MetaMachine;
import com.gregtechceu.gtceu.api.machine.trait.NotifiableEnergyContainer;
import com.gregtechceu.gtceu.common.machine.multiblock.part.EnergyHatchPartMachine;
import com.gregtechceu.gtceu.utils.GTUtil;

import com.lowdragmc.lowdraglib.gui.editor.ColorPattern;
import com.lowdragmc.lowdraglib.gui.texture.GuiTextureGroup;
import com.lowdragmc.lowdraglib.gui.texture.ResourceBorderTexture;
import com.lowdragmc.lowdraglib.gui.texture.TextTexture;
import com.lowdragmc.lowdraglib.gui.widget.ButtonWidget;
import com.lowdragmc.lowdraglib.gui.widget.LabelWidget;
import com.lowdragmc.lowdraglib.gui.widget.SelectorWidget;
import com.lowdragmc.lowdraglib.gui.widget.SwitchWidget;
import com.lowdragmc.lowdraglib.gui.widget.TextFieldWidget;
import com.lowdragmc.lowdraglib.gui.widget.Widget;
import com.lowdragmc.lowdraglib.gui.widget.WidgetGroup;
import com.lowdragmc.lowdraglib.syncdata.annotation.DescSynced;
import com.lowdragmc.lowdraglib.syncdata.annotation.Persisted;
import com.lowdragmc.lowdraglib.syncdata.field.ManagedFieldHolder;

import net.minecraft.MethodsReturnNonnullByDefault;
import net.minecraft.network.chat.Component;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.phys.BlockHitResult;

import org.apache.commons.lang3.ArrayUtils;

import java.util.Arrays;

import javax.annotation.ParametersAreNonnullByDefault;

/**
 * Debug Energy Hatch (and Debug Laser Target Hatch), for testing multiblocks: an energy input that is always full.
 * Its GUI works like the GTCEu Creative Energy Container (the one GTMThings' creative hatches also follow): a tier
 * selector, a free voltage field, the amperage with -/+ buttons and an on/off switch. Any change re-forms the
 * multiblock, so the new voltage is used at once.
 *
 * <p>
 * Written for GTNA on GTCEu's (LGPL) energy hatch and creative energy container GUI.
 */
@ParametersAreNonnullByDefault
@MethodsReturnNonnullByDefault
public class DebugEnergyHatchPartMachine extends EnergyHatchPartMachine {

    protected static final ManagedFieldHolder MANAGED_FIELD_HOLDER = new ManagedFieldHolder(
            DebugEnergyHatchPartMachine.class, EnergyHatchPartMachine.MANAGED_FIELD_HOLDER);

    @Persisted
    @DescSynced
    private long voltage = GTValues.V[GTValues.MAX];
    @Persisted
    @DescSynced
    private int debugAmperage;
    @Persisted
    @DescSynced
    private int setTier = GTValues.MAX;
    @Persisted
    @DescSynced
    private boolean active = true;

    public DebugEnergyHatchPartMachine(IMachineBlockEntity holder, int defaultAmperage, Object... args) {
        super(holder, GTValues.MAX, IO.IN, defaultAmperage, args);
        this.debugAmperage = defaultAmperage;
    }

    @Override
    public ManagedFieldHolder getFieldHolder() {
        return MANAGED_FIELD_HOLDER;
    }

    @Override
    protected NotifiableEnergyContainer createEnergyContainer(Object... args) {
        // Never accepts energy from cables; it is always full anyway.
        var container = new EndlessContainer(this);
        container.setSideInputCondition(side -> false);
        return container;
    }

    @Override
    public void onLoad() {
        super.onLoad();
        applySettings();
    }

    public int getVoltageTier() {
        return setTier;
    }

    public long getVoltage() {
        return voltage;
    }

    public int getDebugAmperage() {
        return debugAmperage;
    }

    public boolean isActive() {
        return active;
    }

    /** Picks a tier and its full voltage, like the tier selector. */
    public void setVoltageTier(int tier) {
        setTier = Math.max(GTValues.ULV, Math.min(GTValues.MAX, tier));
        voltage = GTValues.V[setTier];
        changed();
    }

    public void setVoltage(long value) {
        voltage = Math.max(0, value);
        setTier = Math.min(GTValues.MAX, GTUtil.getTierByVoltage(voltage));
        changed();
    }

    public void setDebugAmperage(int amperage) {
        debugAmperage = Math.max(0, amperage);
        changed();
    }

    public void setActive(boolean value) {
        active = value;
        changed();
    }

    private void changed() {
        applySettings();
        reformControllers();
    }

    private void applySettings() {
        long amps = active ? debugAmperage : 0;
        long volts = active ? voltage : 0;
        energyContainer.resetBasicInfo(capacity(volts, amps), volts, amps, 0, 0);
        energyContainer.setEnergyStored(energyContainer.getEnergyCapacity());
    }

    /** 64 ticks of input, saturating; kept well under Long.MAX_VALUE so a multi summing hatches cannot overflow. */
    private static long capacity(long volts, long amps) {
        long limit = Long.MAX_VALUE >> 8;
        if (volts == 0 || amps == 0) return 0;
        if (volts > limit / 64 / amps) return limit;
        return volts * 64L * amps;
    }

    /** The controllers cache the hatch voltage when they form; make them check the structure again. */
    private void reformControllers() {
        if (isRemote()) return;
        for (var controller : getControllers()) {
            controller.onPartUnload();
        }
    }

    // No weather or terrain explosions for a test part.
    @Override
    protected void checkExplosion() {}

    @Override
    public boolean shouldOpenUI(Player player, InteractionHand hand, BlockHitResult hit) {
        return true;
    }

    @Override
    public Widget createUIWidget() {
        var group = new WidgetGroup(0, 0, 176, 150);
        group.addWidget(new LabelWidget(7, 32, "gtceu.creative.energy.voltage"));
        group.addWidget(new TextFieldWidget(9, 47, 152, 16, () -> String.valueOf(voltage),
                value -> setVoltage(Long.parseLong(value))).setNumbersOnly(0L, Long.MAX_VALUE));
        group.addWidget(new LabelWidget(7, 74, "gtceu.creative.energy.amperage"));
        group.addWidget(new ButtonWidget(7, 87, 20, 20,
                new GuiTextureGroup(ResourceBorderTexture.BUTTON_COMMON, new TextTexture("-")),
                cd -> setDebugAmperage(debugAmperage - 1)));
        group.addWidget(new TextFieldWidget(31, 89, 114, 16, () -> String.valueOf(debugAmperage),
                value -> setDebugAmperage(Integer.parseInt(value))).setNumbersOnly(0, Integer.MAX_VALUE));
        group.addWidget(new ButtonWidget(149, 87, 20, 20,
                new GuiTextureGroup(ResourceBorderTexture.BUTTON_COMMON, new TextTexture("+")),
                cd -> {
                    if (debugAmperage < Integer.MAX_VALUE) setDebugAmperage(debugAmperage + 1);
                }));
        group.addWidget(new LabelWidget(7, 112, () -> Component.translatable("gtna.machine.debug_energy_hatch.rate",
                com.gregtechceu.gtceu.utils.FormattingUtil.formatNumbers(active ? voltage * (long) debugAmperage : 0))
                .getString()));
        group.addWidget(new SwitchWidget(7, 126, 77, 20, (clickData, value) -> setActive(value))
                .setTexture(
                        new GuiTextureGroup(ResourceBorderTexture.BUTTON_COMMON,
                                new TextTexture("gtceu.creative.activity.off")),
                        new GuiTextureGroup(ResourceBorderTexture.BUTTON_COMMON,
                                new TextTexture("gtceu.creative.activity.on")))
                .setPressed(active));
        group.addWidget(new SelectorWidget(7, 7, 50, 20, Arrays.stream(GTValues.VNF).toList(), -1)
                .setOnChanged(tier -> setVoltageTier(ArrayUtils.indexOf(GTValues.VNF, tier)))
                .setSupplier(() -> GTValues.VNF[setTier])
                .setButtonBackground(ResourceBorderTexture.BUTTON_COMMON)
                .setBackground(ColorPattern.BLACK.rectTexture())
                .setValue(GTValues.VNF[setTier]));
        return group;
    }

    /** Reports the chosen voltage and amperage and stays full whatever is drawn from it. */
    private static class EndlessContainer extends NotifiableEnergyContainer {

        EndlessContainer(MetaMachine machine) {
            super(machine, 0, 0, 0, 0, 0);
        }

        @Override
        public long changeEnergy(long energyToAdd) {
            setEnergyStored(getEnergyCapacity());
            return energyToAdd;
        }

        @Override
        public long getEnergyStored() {
            return getEnergyCapacity();
        }
    }
}
