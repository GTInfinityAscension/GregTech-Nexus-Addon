package com.raishxn.gtna.common.machine.multiblock.electric;

import com.gregtechceu.gtceu.api.GTValues;
import com.gregtechceu.gtceu.api.capability.recipe.IO;
import com.gregtechceu.gtceu.api.machine.IMachineBlockEntity;
import com.gregtechceu.gtceu.api.machine.MetaMachine;
import com.gregtechceu.gtceu.api.machine.multiblock.WorkableElectricMultiblockMachine;
import com.gregtechceu.gtceu.api.machine.trait.RecipeLogic;
import com.gregtechceu.gtceu.api.recipe.GTRecipe;
import com.gregtechceu.gtceu.api.recipe.RecipeHelper;
import com.gregtechceu.gtceu.api.recipe.modifier.ModifierFunction;
import com.gregtechceu.gtceu.common.data.GTMaterials;
import com.gregtechceu.gtceu.data.recipe.builder.GTRecipeBuilder;

import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.level.Level;

import com.raishxn.gtna.common.data.DysonSphereData;
import earth.terrarium.adastra.api.planets.Planet;
import earth.terrarium.adastra.api.planets.PlanetApi;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.util.List;

/**
 * GTOCore Dyson Sphere: the Launch Silo puts swarm modules in orbit of the planet it stands on, and the Receiving
 * Station on the same planet turns them into laser power. GTO's planet distances live in its closed GTOLib, so GTNA
 * uses the Ad Astra tier of the planet plus one (Earth 1, Moon 2, Mars 3, Venus and Mercury 4, Glacio 5); an orbit
 * counts as its planet. The Receiving Station's coolant is liquid helium (GTO: Gelid Cryotheum).
 */
public final class DysonSphereMachines {

    private DysonSphereMachines() {}

    /** The planet a level belongs to (an orbit maps to its planet), or null when Ad Astra knows none. */
    @Nullable
    public static ResourceKey<Level> planetOf(Level level) {
        Planet planet = PlanetApi.API.getPlanet(level);
        if (planet == null) return level.dimension() == Level.OVERWORLD ? Level.OVERWORLD : null;
        return planet.getOrbitPlanet().orElse(planet.dimension());
    }

    /** Distance factor of a planet: its Ad Astra tier plus one; 0 when unknown. */
    public static int distance(ResourceKey<Level> planet) {
        if (planet == null) return 0;
        Planet data = PlanetApi.API.getPlanet(planet);
        if (data == null) return planet == Level.OVERWORLD ? 1 : 0;
        return Math.max(0, data.tier()) + 1;
    }

    /** GTO {@code dyson_sphere_launch_silo}. */
    public static final class LaunchSilo extends WorkableElectricMultiblockMachine {

        public LaunchSilo(IMachineBlockEntity holder, Object... args) {
            super(holder, args);
        }

        /** Only on a planet's surface; the launch takes {@code distance / 4} of the recipe time. */
        public static ModifierFunction launchModifier(MetaMachine machine, @NotNull GTRecipe recipe) {
            Level level = machine.getLevel();
            if (level == null || PlanetApi.API.isSpace(level)) return ModifierFunction.NULL;
            int distance = distance(planetOf(level));
            if (distance <= 0) return ModifierFunction.NULL;
            return ModifierFunction.builder().durationMultiplier(distance / 4.0).build();
        }

        @Override
        public void afterWorking() {
            super.afterWorking();
            if (!(getLevel() instanceof ServerLevel level)) return;
            var planet = planetOf(level);
            if (planet == null) return;
            var data = DysonSphereData.get(level.getServer());
            int modules = data.modules(planet);
            if (modules >= DysonSphereData.MAX_MODULES) return;
            // A launch onto a badly damaged swarm repairs it instead of adding a module (GTO).
            if (data.damage(planet) > 60) data.set(planet, modules, 0);
            else data.set(planet, modules + 1, data.damage(planet));
        }

        @Override
        public void addDisplayText(List<Component> textList) {
            super.addDisplayText(textList);
            if (isFormed() && getLevel() instanceof ServerLevel level && planetOf(level) != null) {
                var data = DysonSphereData.get(level.getServer());
                textList.add(Component.translatable("gtna.machine.dyson_sphere.amount",
                        data.modules(planetOf(level))));
            }
        }
    }

    /** GTO {@code dyson_sphere_receiving_station}: a generator whose output grows with the swarm. */
    public static final class ReceivingStation extends WorkableElectricMultiblockMachine {

        public ReceivingStation(IMachineBlockEntity holder, Object... args) {
            super(holder, args);
        }

        @Override
        protected RecipeLogic createRecipeLogic(Object... args) {
            return new Logic(this);
        }

        @Nullable
        GTRecipe swarmRecipe() {
            if (!(getLevel() instanceof ServerLevel level)) return null;
            var planet = planetOf(level);
            int distance = distance(planet);
            if (planet == null || distance == 0) return null;
            var data = DysonSphereData.get(level.getServer());
            if (data.inUse(planet)) return null;
            int modules = data.modules(planet);
            if (modules < 1) return null;
            long eu = GTValues.V[GTValues.MAX] * modules * (50 - Math.max(0, data.damage(planet) - 60)) / 50;
            GTRecipe recipe = GTRecipeBuilder.ofRaw().duration(20)
                    .CWUt(Math.max(1, modules * distance / 10))
                    .EUt(-Math.max(1, eu))
                    .inputFluids(GTMaterials.Helium.getFluid(
                            com.gregtechceu.gtceu.api.fluids.store.FluidStorageKeys.LIQUID,
                            Math.max(1, (int) Math.sqrt(modules))))
                    .buildRawRecipe();
            return RecipeHelper.matchContents(this, recipe).isSuccess() ? recipe : null;
        }

        @Override
        public boolean beforeWorking(@Nullable GTRecipe recipe) {
            if (getLevel() instanceof ServerLevel level && planetOf(level) != null) {
                DysonSphereData.get(level.getServer()).setInUse(planetOf(level), true);
            }
            return super.beforeWorking(recipe);
        }

        @Override
        public void afterWorking() {
            super.afterWorking();
            if (!(getLevel() instanceof ServerLevel level)) return;
            var planet = planetOf(level);
            if (planet == null) return;
            var data = DysonSphereData.get(level.getServer());
            data.setInUse(planet, false);
            int modules = data.modules(planet);
            // GTO: each run may damage the swarm; a fully damaged swarm loses a module.
            if (GTValues.RNG.nextFloat() >= 0.01F * (1 + (double) modules / 128)) return;
            int damage = data.damage(planet);
            if (damage > 99) data.set(planet, Math.max(0, modules - 1), 0);
            else data.set(planet, modules, damage + 1);
        }

        @Override
        public void onStructureInvalid() {
            super.onStructureInvalid();
            if (getLevel() instanceof ServerLevel level && planetOf(level) != null) {
                DysonSphereData.get(level.getServer()).setInUse(planetOf(level), false);
            }
        }

        @Override
        public void addDisplayText(List<Component> textList) {
            super.addDisplayText(textList);
            if (isFormed() && getLevel() instanceof ServerLevel level && planetOf(level) != null) {
                var data = DysonSphereData.get(level.getServer());
                var planet = planetOf(level);
                textList.add(Component.translatable("gtna.machine.dyson_sphere.amount", data.modules(planet)));
                textList.add(Component.translatable("gtna.machine.dyson_sphere.damage", data.damage(planet)));
            }
        }

        /** Builds the swarm recipe every cycle instead of looking one up. */
        static final class Logic extends RecipeLogic {

            Logic(ReceivingStation machine) {
                super(machine);
            }

            private ReceivingStation station() {
                return (ReceivingStation) machine;
            }

            @Override
            public void findAndHandleRecipe() {
                lastRecipe = null;
                GTRecipe recipe = station().swarmRecipe();
                if (recipe != null) setupRecipe(recipe);
            }

            @Override
            public void onRecipeFinish() {
                machine.afterWorking();
                if (lastRecipe != null) RecipeHelper.handleRecipeIO(machine, lastRecipe, IO.OUT, chanceCaches);
                GTRecipe next = station().swarmRecipe();
                if (next != null) {
                    setupRecipe(next);
                    return;
                }
                setStatus(Status.IDLE);
                progress = 0;
                duration = 0;
            }
        }
    }
}
