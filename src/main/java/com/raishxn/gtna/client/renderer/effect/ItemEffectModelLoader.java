package com.raishxn.gtna.client.renderer.effect;

import net.minecraft.client.renderer.block.model.ItemOverrides;
import net.minecraft.client.renderer.texture.TextureAtlasSprite;
import net.minecraft.client.resources.model.BakedModel;
import net.minecraft.client.resources.model.Material;
import net.minecraft.client.resources.model.ModelBaker;
import net.minecraft.client.resources.model.ModelState;
import net.minecraft.client.resources.model.UnbakedModel;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.GsonHelper;
import net.minecraftforge.client.event.ModelEvent;
import net.minecraftforge.client.model.ItemLayerModel;
import net.minecraftforge.client.model.geometry.IGeometryBakingContext;
import net.minecraftforge.client.model.geometry.IGeometryLoader;
import net.minecraftforge.client.model.geometry.IUnbakedGeometry;

import com.google.gson.JsonDeserializationContext;
import com.google.gson.JsonObject;
import com.google.gson.JsonParseException;
import com.raishxn.gtna.api.render.ItemEffect;

import java.util.List;
import java.util.function.Function;

/**
 * {@code gtna:halo}, {@code gtna:glow_edge}, {@code gtna:cosmic}, {@code gtna:eternal} and {@code gtna:unstable}
 * item model loaders. The icon is baked like a plain {@code item/generated} model, so it always renders; the
 * effect section (an object named after the loader) only adds the effect on top.
 *
 * <pre>{@code
 * "loader": "gtna:halo",      "halo":      { "texture": "#halo", "color": -2331879, "size": 5, "pulse": true }
 * "loader": "gtna:glow_edge", "glow_edge": { "color": 12513904, "width": 1.5 }
 * "loader": "gtna:cosmic",    "cosmic":    { "mask": "gtna:mask/cosmic", "color": 0, "secondary": 0, "speed": 1 }
 * }</pre>
 */
public final class ItemEffectModelLoader implements IGeometryLoader<ItemEffectModelLoader.Geometry> {

    private final ItemEffect.Type type;

    private ItemEffectModelLoader(ItemEffect.Type type) {
        this.type = type;
    }

    public static void register(ModelEvent.RegisterGeometryLoaders event) {
        for (var type : ItemEffect.Type.values()) event.register(type.id(), new ItemEffectModelLoader(type));
    }

    @Override
    public Geometry read(JsonObject json, JsonDeserializationContext context) throws JsonParseException {
        var section = GsonHelper.getAsJsonObject(json, type.id(), new JsonObject());
        var effect = ItemEffect.of(type)
                .withColor(GsonHelper.getAsInt(section, "color", 0))
                .withSecondary(GsonHelper.getAsInt(section, "secondary", 0))
                .withSize(GsonHelper.getAsFloat(section, "size",
                        GsonHelper.getAsFloat(section, "width", type.defaultSize)))
                .withPulse(GsonHelper.getAsBoolean(section, "pulse", false))
                .withSpeed(GsonHelper.getAsFloat(section, "speed", 1));
        String texture = GsonHelper.getAsString(section, type == ItemEffect.Type.HALO ? "texture" : "mask", null);
        // "#halo" points into this model's own textures. Resolve it here: GTCEu's material items bake through a
        // generated child model whose texture map only has the layers, so the reference would be lost at bake time.
        if (texture != null && texture.startsWith("#")) {
            var textures = GsonHelper.getAsJsonObject(json, "textures", new JsonObject());
            String key = texture.substring(1);
            for (int i = 0; i < 4 && textures.has(key); i++) {
                String value = GsonHelper.getAsString(textures, key);
                if (!value.startsWith("#")) {
                    texture = value;
                    break;
                }
                key = value.substring(1);
            }
        }
        // Shader effects use the icon's own silhouette when no mask is given.
        if (texture != null || type.isShader()) effect = effect.withTexture(null);
        return new Geometry(ItemLayerModel.Loader.INSTANCE.read(json, context), effect, texture);
    }

    public record Geometry(ItemLayerModel layers, ItemEffect effect, String texture)
            implements IUnbakedGeometry<Geometry> {

        @Override
        public BakedModel bake(IGeometryBakingContext context, ModelBaker baker,
                               Function<Material, TextureAtlasSprite> sprites, ModelState state,
                               ItemOverrides overrides, ResourceLocation location) {
            var base = layers.bake(context, baker, sprites, state, overrides, location);
            var resolved = effect;
            if (texture != null) {
                // "#halo" style references resolve through the model's texture map.
                var material = texture.startsWith("#") ? context.getMaterial(texture.substring(1)) : null;
                resolved = effect.withTexture(material != null ? material.texture() : new ResourceLocation(texture));
            }
            return ItemEffectBakedModel.wrap(base, List.of(resolved));
        }

        @Override
        public void resolveParents(Function<ResourceLocation, UnbakedModel> models, IGeometryBakingContext context) {
            layers.resolveParents(models, context);
        }
    }
}
