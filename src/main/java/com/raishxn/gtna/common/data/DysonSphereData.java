package com.raishxn.gtna.common.data;

import net.minecraft.nbt.CompoundTag;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.MinecraftServer;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.saveddata.SavedData;

import java.util.HashMap;
import java.util.Map;

/**
 * GTOCore {@code DysonSphereSavaedData}: per planet, how many Dyson swarm modules are in orbit and how damaged the
 * swarm is (0-100), plus whether a receiving station is drawing from it right now. Kept in the overworld's data.
 */
public final class DysonSphereData extends SavedData {

    private static final String NAME = "gtna_dyson_sphere";
    /** GTO's cap on launched modules. */
    public static final int MAX_MODULES = 100_000;

    private final Map<ResourceLocation, int[]> swarms = new HashMap<>();

    public static DysonSphereData get(MinecraftServer server) {
        return server.overworld().getDataStorage().computeIfAbsent(DysonSphereData::load, DysonSphereData::new, NAME);
    }

    private static DysonSphereData load(CompoundTag tag) {
        var data = new DysonSphereData();
        for (String key : tag.getAllKeys()) {
            int[] values = tag.getIntArray(key);
            if (values.length >= 2) data.swarms.put(new ResourceLocation(key), new int[] { values[0], values[1], 0 });
        }
        return data;
    }

    @Override
    public CompoundTag save(CompoundTag tag) {
        swarms.forEach((dim, values) -> tag.putIntArray(dim.toString(), new int[] { values[0], values[1] }));
        return tag;
    }

    private int[] of(ResourceKey<Level> planet) {
        return swarms.computeIfAbsent(planet.location(), k -> new int[3]);
    }

    public int modules(ResourceKey<Level> planet) {
        return of(planet)[0];
    }

    public int damage(ResourceKey<Level> planet) {
        return of(planet)[1];
    }

    public boolean inUse(ResourceKey<Level> planet) {
        return of(planet)[2] != 0;
    }

    public void set(ResourceKey<Level> planet, int modules, int damage) {
        int[] values = of(planet);
        values[0] = modules;
        values[1] = damage;
        setDirty();
    }

    public void setInUse(ResourceKey<Level> planet, boolean inUse) {
        of(planet)[2] = inUse ? 1 : 0;
    }
}
