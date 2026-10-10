package com.raishxn.gtna.common.data;

import com.gregtechceu.gtceu.api.GTValues;
import com.gregtechceu.gtceu.api.data.RotationState;
import com.gregtechceu.gtceu.api.machine.IMachineBlockEntity;
import com.gregtechceu.gtceu.api.machine.MachineDefinition;
import com.gregtechceu.gtceu.api.machine.MetaMachine;
import com.gregtechceu.gtceu.api.machine.multiblock.PartAbility;
import com.gregtechceu.gtceu.api.registry.registrate.MachineBuilder;

import net.minecraft.network.chat.Component;

import com.raishxn.gtna.GTNACORE;
import com.raishxn.gtna.common.machine.multiblock.part.research.ExResearchPartMachine;
import com.raishxn.gtna.common.machine.multiblock.part.research.ThermalConductorHatchPartMachine;

import java.util.function.Function;

import static com.gregtechceu.gtceu.api.machine.property.GTMachineModelProperties.IS_ACTIVE;
import static com.gregtechceu.gtceu.api.machine.property.GTMachineModelProperties.IS_FORMED;
import static com.gregtechceu.gtceu.api.machine.property.GTMachineModelProperties.IS_HPCA_PART_DAMAGED;
import static com.gregtechceu.gtceu.common.data.models.GTMachineModels.createHPCAPartModel;
import static com.raishxn.gtna.api.registry.GTNARegistry.REGISTRATE;

/**
 * GTOCore research parts (G-0249): NICH (tier 3) and GWCA (tier 4) HPCA components for the Supercomputing Center, and
 * the Thermal Conductor Hatch. Overlays are GTOCore's {@code about_computer} textures on GTCEu's advanced computer
 * casing model.
 */
public final class GTNAResearchMachines {

    private GTNAResearchMachines() {}

    public static void init() {}

    private static MachineBuilder<MachineDefinition, ?> part(String name, String lang,
                                                             Function<IMachineBlockEntity, MetaMachine> constructor,
                                                             String overlay, boolean damageable) {
        var normal = GTNACORE.id("block/casings/about_computer/" + overlay);
        var damaged = damageable ? GTNACORE.id("block/casings/about_computer/damaged_" + overlay) : normal;
        return REGISTRATE.machine(name, constructor)
                .langValue(lang)
                .rotationState(RotationState.ALL)
                .abilities(PartAbility.HPCA_COMPONENT)
                .modelProperty(IS_FORMED, false)
                .modelProperty(IS_HPCA_PART_DAMAGED, false)
                .modelProperty(IS_ACTIVE, false)
                .model(createHPCAPartModel(true, normal, damaged));
    }

    public static final MachineDefinition NICH_EMPTY_COMPONENT = part("nich_empty_component", "Empty NICH Component",
            h -> new ExResearchPartMachine.Empty(h, 3), "nich_empty_component", false).register();
    public static final MachineDefinition NICH_COMPUTING_COMPONENTS = part("nich_computing_components",
            "NICH Computing Components", h -> new ExResearchPartMachine.Computation(h, 3),
            "nich_computing_components", true)
            .tooltips(Component.translatable("gtceu.machine.hpca.component_general.upkeep_eut",
                    GTValues.VA[GTValues.LuV]),
                    Component.translatable("gtceu.machine.hpca.component_general.max_eut", GTValues.VA[GTValues.UV]),
                    Component.translatable("gtceu.machine.hpca.component_type.computation_cwut", 64),
                    Component.translatable("gtceu.machine.hpca.component_type.computation_cooling", 16))
            .register();
    public static final MachineDefinition NICH_COOLING_COMPONENTS = part("nich_cooling_components",
            "NICH Cooling Components", h -> new ExResearchPartMachine.Cooler(h, 3), "nich_cooling_components", false)
            .tooltips(Component.translatable("gtceu.machine.hpca.component_general.max_eut", GTValues.VA[GTValues.UV]),
                    Component.translatable("gtceu.machine.hpca.component_type.cooler_active"),
                    Component.translatable("gtceu.machine.hpca.component_type.cooler_cooling", 8))
            .register();
    public static final MachineDefinition NICH_BRIDGE_COMPONENT = part("nich_bridge_component",
            "NICH Bridge Component", h -> new ExResearchPartMachine.Bridge(h, 3), "nich_bridge_component", false)
            .tooltips(Component.translatable("gtceu.machine.hpca.component_type.bridge"))
            .register();
    public static final MachineDefinition GWCA_EMPTY_COMPONENT = part("gwca_empty_component", "Empty GWCA Component",
            h -> new ExResearchPartMachine.Empty(h, 4), "gwca_empty_component", false).register();
    public static final MachineDefinition GWCA_COMPUTING_COMPONENTS = part("gwca_computing_components",
            "GWCA Computing Components", h -> new ExResearchPartMachine.Computation(h, 4),
            "gwca_computing_components", true)
            .tooltips(Component.translatable("gtceu.machine.hpca.component_general.upkeep_eut",
                    GTValues.VA[GTValues.UV]),
                    Component.translatable("gtceu.machine.hpca.component_general.max_eut", GTValues.VA[GTValues.UEV]),
                    Component.translatable("gtceu.machine.hpca.component_type.computation_cwut", 1024),
                    Component.translatable("gtceu.machine.hpca.component_type.computation_cooling", 256))
            .register();
    public static final MachineDefinition GWCA_COOLING_COMPONENTS = part("gwca_cooling_components",
            "GWCA Cooling Components", h -> new ExResearchPartMachine.Cooler(h, 4), "gwca_cooling_components", false)
            .tooltips(Component.translatable("gtceu.machine.hpca.component_general.max_eut",
                    GTValues.VA[GTValues.UHV]),
                    Component.translatable("gtceu.machine.hpca.component_type.cooler_active"),
                    Component.translatable("gtceu.machine.hpca.component_type.cooler_cooling", 64))
            .register();

    public static final MachineDefinition THERMAL_CONDUCTOR_HATCH = REGISTRATE
            .machine("thermal_conductor_hatch", ThermalConductorHatchPartMachine::new)
            .langValue("Thermal Conductor Hatch")
            .rotationState(RotationState.ALL)
            .tier(GTValues.LuV)
            .overlayTieredHullModel("thermal_conductor_hatch")
            .tooltips(Component.translatable("gtna.machine.thermal_conductor_hatch.tooltip"))
            .register();
}
