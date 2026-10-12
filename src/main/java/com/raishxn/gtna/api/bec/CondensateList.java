package com.raishxn.gtna.api.bec;

import net.minecraft.nbt.CompoundTag;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.material.Fluid;
import net.minecraftforge.registries.ForgeRegistries;

import it.unimi.dsi.fastutil.objects.Object2LongMap;
import it.unimi.dsi.fastutil.objects.Object2LongOpenHashMap;

/** GTNH {@code CondensateList}: condensate amounts as longs (a storage easily holds more than 2.1B). */
public class CondensateList extends Object2LongOpenHashMap<Fluid> {

    public CompoundTag save() {
        CompoundTag tag = new CompoundTag();
        for (Object2LongMap.Entry<Fluid> e : object2LongEntrySet()) {
            ResourceLocation id = ForgeRegistries.FLUIDS.getKey(e.getKey());
            if (id != null) tag.putLong(id.toString(), e.getLongValue());
        }
        return tag;
    }

    public void load(CompoundTag tag) {
        clear();
        for (String key : tag.getAllKeys()) {
            Fluid fluid = ForgeRegistries.FLUIDS.getValue(new ResourceLocation(key));
            if (fluid != null) put(fluid, tag.getLong(key));
        }
    }

    public long total() {
        long sum = 0;
        for (long l : values()) sum += l;
        return sum;
    }

    @Override
    public CondensateList clone() {
        CondensateList copy = new CondensateList();
        copy.putAll(this);
        return copy;
    }
}
