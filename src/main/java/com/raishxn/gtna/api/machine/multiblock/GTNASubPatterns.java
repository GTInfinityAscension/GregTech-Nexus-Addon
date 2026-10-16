package com.raishxn.gtna.api.machine.multiblock;

import com.gregtechceu.gtceu.api.machine.MultiblockMachineDefinition;
import com.gregtechceu.gtceu.api.pattern.BlockPattern;

import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;

import com.gtinfinityascension.gtialib.module.ModuleRegistry;

import java.util.List;
import java.util.Map;
import java.util.function.Function;

/**
 * Kept for addons and KubeJS scripts that used this name: the module registry now lives in GTIA Lib
 * ({@link ModuleRegistry}) and every method here forwards to it.
 */
public final class GTNASubPatterns {

    private GTNASubPatterns() {}

    public static void register(ResourceLocation machineId,
                                Function<MultiblockMachineDefinition, BlockPattern> factory) {
        ModuleRegistry.register(machineId, factory);
    }

    public static void register(ResourceLocation machineId,
                                Function<MultiblockMachineDefinition, BlockPattern> factory,
                                Component... tooltips) {
        ModuleRegistry.register(machineId, factory, tooltips);
    }

    public static void registerKubeJS(ResourceLocation machineId,
                                      Function<MultiblockMachineDefinition, BlockPattern> factory,
                                      String descriptionKey) {
        ModuleRegistry.registerKubeJS(machineId, factory, descriptionKey);
    }

    public static void registerKubeJS(ResourceLocation machineId,
                                      Function<MultiblockMachineDefinition, BlockPattern> factory,
                                      String descriptionKey, double speedBonus, boolean perfectOverclock) {
        ModuleRegistry.registerKubeJS(machineId, factory, descriptionKey, speedBonus, perfectOverclock);
    }

    public static void clearKubeJS() {
        ModuleRegistry.clearKubeJS();
    }

    public static List<BlockPattern> get(MultiblockMachineDefinition definition) {
        return ModuleRegistry.get(definition);
    }

    public static ModuleRegistry.Performance performance(BlockPattern pattern) {
        return ModuleRegistry.performance(pattern);
    }

    public static List<Component> getTooltips(MultiblockMachineDefinition definition) {
        return ModuleRegistry.getTooltips(definition);
    }

    public static Map<ResourceLocation, List<String>> kubeDescriptions() {
        return ModuleRegistry.kubeDescriptions();
    }

    public static void setClientKubeDescriptions(Map<ResourceLocation, List<String>> descriptions) {
        ModuleRegistry.setClientKubeDescriptions(descriptions);
    }
}
