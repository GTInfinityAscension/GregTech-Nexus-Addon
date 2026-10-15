package com.raishxn.gtna.mixin;

import org.objectweb.asm.tree.ClassNode;
import org.spongepowered.asm.mixin.extensibility.IMixinConfigPlugin;
import org.spongepowered.asm.mixin.extensibility.IMixinInfo;

import java.util.List;
import java.util.Set;

/** Picks the JEI fluid-tank mixin that matches the installed JEI, checked by resource so nothing is loaded early. */
public class GTNAMixinPlugin implements IMixinConfigPlugin {

    private static final boolean TILING_DIRECTION = GTNAMixinPlugin.class.getClassLoader()
            .getResource("mezz/jei/api/gui/drawable/TilingDirection.class") != null;

    @Override
    public boolean shouldApplyMixin(String targetClassName, String mixinClassName) {
        if (mixinClassName.endsWith(".UniversiumJeiFluidMixin")) return TILING_DIRECTION;
        if (mixinClassName.endsWith(".UniversiumJeiFluidLegacyMixin")) return !TILING_DIRECTION;
        return true;
    }

    @Override
    public void onLoad(String mixinPackage) {}

    @Override
    public String getRefMapperConfig() {
        return null;
    }

    @Override
    public void acceptTargets(Set<String> myTargets, Set<String> otherTargets) {}

    @Override
    public List<String> getMixins() {
        return null;
    }

    @Override
    public void preApply(String targetClassName, ClassNode targetClass, String mixinClassName, IMixinInfo mixinInfo) {}

    @Override
    public void postApply(String targetClassName, ClassNode targetClass, String mixinClassName, IMixinInfo mixinInfo) {}
}
