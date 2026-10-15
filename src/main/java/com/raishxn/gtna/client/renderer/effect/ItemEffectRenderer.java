package com.raishxn.gtna.client.renderer.effect;

import com.gregtechceu.gtceu.api.data.chemical.ChemicalHelper;

import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.renderer.ShaderInstance;
import net.minecraft.client.renderer.block.model.BakedQuad;
import net.minecraft.client.renderer.texture.OverlayTexture;
import net.minecraft.client.renderer.texture.TextureAtlasSprite;
import net.minecraft.client.resources.model.BakedModel;
import net.minecraft.core.Direction;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.Mth;
import net.minecraft.util.RandomSource;
import net.minecraft.world.inventory.InventoryMenu;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemDisplayContext;
import net.minecraft.world.item.ItemStack;
import net.minecraftforge.client.event.RegisterShadersEvent;
import net.minecraftforge.registries.ForgeRegistries;

import com.mojang.blaze3d.vertex.DefaultVertexFormat;
import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import com.mojang.blaze3d.vertex.VertexFormat;
import com.raishxn.gtna.GTNACORE;
import com.raishxn.gtna.api.render.ItemEffect;
import com.raishxn.gtna.api.render.ItemEffectOverrides;
import com.raishxn.gtna.config.ConfigHolder;
import org.jetbrains.annotations.Nullable;
import org.joml.Vector3f;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * Draws {@link ItemEffect}s around item icons. Halo and glow edge sit behind the icon and only show in
 * inventories; cosmic, eternal and unstable are drawn over the icon everywhere with GTNA's own
 * {@code gtna:item_effect} shader.
 */
public final class ItemEffectRenderer extends RenderType {

    public static final int MODE_COSMIC = 0, MODE_ETERNAL = 1, MODE_UNSTABLE = 2;
    private static final int FULL_BRIGHT = 15728880;
    private static final long START = System.currentTimeMillis();

    private static ShaderInstance shader;
    /** Translucent, no depth write; quads are nudged off the surface they cover. */
    public static final RenderType EFFECT = create("gtna_item_effect", DefaultVertexFormat.NEW_ENTITY,
            VertexFormat.Mode.QUADS, 256, false, true, CompositeState.builder()
                    .setShaderState(new ShaderStateShard(() -> shader))
                    .setTextureState(new TextureStateShard(InventoryMenu.BLOCK_ATLAS, false, false))
                    .setTransparencyState(TRANSLUCENT_TRANSPARENCY).setCullState(NO_CULL)
                    .setLightmapState(LIGHTMAP).setOverlayState(OVERLAY)
                    .setWriteMaskState(COLOR_WRITE).createCompositeState(false));

    private static final Map<Item, Optional<List<ItemEffect>>> SCRIPTED = new HashMap<>();
    private static int scriptedVersion = -1;

    private ItemEffectRenderer() {
        super("unused", DefaultVertexFormat.NEW_ENTITY, VertexFormat.Mode.QUADS, 256, false, true, () -> {}, () -> {});
    }

    public static void register(RegisterShadersEvent event) throws IOException {
        event.registerShader(new ShaderInstance(event.getResourceProvider(), GTNACORE.id("item_effect"),
                DefaultVertexFormat.NEW_ENTITY), instance -> shader = instance);
    }

    /** Effects for this stack: script overrides first, then the ones declared by its model. */
    public static List<ItemEffect> effects(ItemStack stack, BakedModel model) {
        List<ItemEffect> own = model instanceof ItemEffectBakedModel wrapped ? wrapped.effects() : List.of();
        if (ItemEffectOverrides.isEmpty()) return own;
        int version = ItemEffectOverrides.version();
        if (version != scriptedVersion) {
            SCRIPTED.clear();
            scriptedVersion = version;
        }
        return SCRIPTED.computeIfAbsent(stack.getItem(), ItemEffectRenderer::scripted).orElse(own);
    }

    private static Optional<List<ItemEffect>> scripted(Item item) {
        var id = ForgeRegistries.ITEMS.getKey(item);
        var effects = id == null ? null : ItemEffectOverrides.forItem(id);
        if (effects == null) {
            var entry = ChemicalHelper.getMaterialEntry(item);
            if (!entry.isEmpty() && entry.material() != null)
                effects = ItemEffectOverrides.forMaterial(entry.material().getResourceLocation());
        }
        return Optional.ofNullable(effects);
    }

    /** Animation clock in seconds, scaled by the client config and wrapped to keep float precision. */
    public static float time(float speed) {
        float configured = ConfigHolder.INSTANCE == null ? 1 : ConfigHolder.INSTANCE.client.itemEffectSpeed / 100f;
        return ((System.currentTimeMillis() - START) % 3_600_000L) / 1000f * configured * speed;
    }

    private static boolean enabled(ItemEffect.Type type) {
        if (ConfigHolder.INSTANCE == null) return true;
        var client = ConfigHolder.INSTANCE.client;
        return switch (type) {
            case HALO -> client.itemHalo;
            case GLOW_EDGE -> client.itemGlowEdge;
            default -> client.itemShaderEffects;
        };
    }

    /** Called with the icon's pose (model space 0..1) just before the icon is drawn. */
    public static void renderBehind(ItemStack stack, ItemDisplayContext context, BakedModel model, PoseStack pose,
                                    MultiBufferSource buffers, int overlay) {
        if (context != ItemDisplayContext.GUI) return;
        for (var effect : effects(stack, model)) {
            if (!enabled(effect.type())) continue;
            if (effect.type() == ItemEffect.Type.HALO) renderHalo(effect, pose, buffers);
            else if (effect.type() == ItemEffect.Type.GLOW_EDGE) renderGlowEdge(effect, stack, model, pose, buffers,
                    overlay);
        }
    }

    /** Called with the icon's pose right after the icon is drawn. */
    public static void renderOver(ItemStack stack, ItemDisplayContext context, BakedModel model, PoseStack pose,
                                  MultiBufferSource buffers) {
        if (shader == null || !(buffers instanceof MultiBufferSource.BufferSource source)) return;
        for (var effect : effects(stack, model)) {
            if (!effect.type().isShader() || !enabled(effect.type())) continue;
            var mask = effect.texture() == null ? null : sprite(effect.texture());
            // The icon itself is still batched; draw it now so the effect lands on top instead of under it.
            if (context == ItemDisplayContext.GUI) source.endBatch();
            prepare(effect, context == ItemDisplayContext.GUI, mask == null);
            var out = source.getBuffer(EFFECT);
            emitSilhouette(model, pose, out, mask);
            source.endBatch(EFFECT);
        }
    }

    private static void renderHalo(ItemEffect effect, PoseStack pose, MultiBufferSource buffers) {
        var sprite = sprite(effect.texture() == null ? ItemEffect.DEFAULT_HALO : effect.texture());
        int color = effect.color() == 0 ? 0xFFFFFFFF : opaque(effect.color());
        float grow = effect.size() / 16f;
        float alpha = (color >>> 24) / 255f;
        if (effect.pulse()) {
            float wave = Mth.sin(time(effect.speed()) * 2.5f);
            grow *= 1 + 0.08f * wave;
            alpha *= 0.8f + 0.2f * wave;
        }
        var out = buffers.getBuffer(RenderType.text(InventoryMenu.BLOCK_ATLAS));
        var matrix = pose.last().pose();
        int r = (color >> 16) & 255, g = (color >> 8) & 255, b = color & 255, a = (int) (alpha * 255);
        // Generated item faces sit at z 7.5..8.5 px; the halo goes just behind the back face.
        float z = 0.44f, min = -grow, max = 1 + grow;
        out.vertex(matrix, min, max, z).color(r, g, b, a).uv(sprite.getU0(), sprite.getV0()).uv2(FULL_BRIGHT)
                .endVertex();
        out.vertex(matrix, min, min, z).color(r, g, b, a).uv(sprite.getU0(), sprite.getV1()).uv2(FULL_BRIGHT)
                .endVertex();
        out.vertex(matrix, max, min, z).color(r, g, b, a).uv(sprite.getU1(), sprite.getV1()).uv2(FULL_BRIGHT)
                .endVertex();
        out.vertex(matrix, max, max, z).color(r, g, b, a).uv(sprite.getU1(), sprite.getV0()).uv2(FULL_BRIGHT)
                .endVertex();
    }

    private static void renderGlowEdge(ItemEffect effect, ItemStack stack, BakedModel model, PoseStack pose,
                                       MultiBufferSource buffers, int overlay) {
        int color = effect.color() == 0 ? 0xFFFFFFFF : effect.color();
        float width = effect.size();
        pose.pushPose();
        // Enlarged copy centred on the icon, a hair behind it so only the rim shows.
        pose.translate(-width * 0.025f, -width * 0.025f, -0.001f);
        float scale = 1 + width * 0.05f;
        pose.scale(scale, scale, 1);
        var tinted = new TintedConsumer(buffers.getBuffer(RenderType.entityTranslucent(InventoryMenu.BLOCK_ATLAS)),
                color);
        Minecraft.getInstance().getItemRenderer().renderModelLists(model, stack, FULL_BRIGHT, overlay, pose, tinted);
        pose.popPose();
    }

    /** Sets the shader uniforms for one effect. */
    private static void prepare(ItemEffect effect, boolean gui, boolean alphaMask) {
        int mode = switch (effect.type()) {
            case ETERNAL -> MODE_ETERNAL;
            case UNSTABLE -> MODE_UNSTABLE;
            default -> MODE_COSMIC;
        };
        int a = effect.color(), b = effect.secondary();
        if (a == 0) {
            a = defaultColor(mode, false);
            if (b == 0) b = defaultColor(mode, true);
        } else if (b == 0) b = lighten(a);
        prepare(mode, a, b, time(effect.speed()), gui, alphaMask);
    }

    /**
     * Sets the shader uniforms directly; returns false when the shader is not loaded or effects are disabled.
     * Used by renderers that draw the effect on blocks and fluids.
     */
    public static boolean prepare(int mode, int colorA, int colorB, float time, boolean gui, boolean alphaMask) {
        if (shader == null) return false;
        var mc = Minecraft.getInstance();
        shader.safeGetUniform("EffectTime").set(time);
        shader.safeGetUniform("ViewAngle").set(gui || mc.player == null ? 0 : mc.player.getYRot() * Mth.DEG_TO_RAD,
                gui || mc.player == null ? 0 : -mc.player.getXRot() * Mth.DEG_TO_RAD);
        shader.safeGetUniform("Density").set(gui ? 0.25f : 8f);
        shader.safeGetUniform("Opacity").set(1f);
        shader.safeGetUniform("Mode").set(mode);
        shader.safeGetUniform("AlphaMask").set(alphaMask ? 1 : 0);
        setColor("ColorA", colorA);
        setColor("ColorB", colorB);
        return true;
    }

    public static boolean shaderEffectsEnabled() {
        return shader != null && enabled(ItemEffect.Type.COSMIC);
    }

    public static int defaultColor(int mode, boolean highlight) {
        return switch (mode) {
            case MODE_ETERNAL -> highlight ? 0xFF9EE8FF : 0xFFFFE7A3;
            case MODE_UNSTABLE -> highlight ? 0xFFFF3B6B : 0xFF2A0010;
            default -> highlight ? 0xFF2E2470 : 0xFF06051A;
        };
    }

    private static void setColor(String name, int argb) {
        shader.safeGetUniform(name).set(((argb >> 16) & 255) / 255f, ((argb >> 8) & 255) / 255f,
                (argb & 255) / 255f, 1f);
    }

    private static int opaque(int argb) {
        return (argb >>> 24) == 0 ? argb | 0xFF000000 : argb;
    }

    private static int lighten(int argb) {
        int r = (argb >> 16) & 255, g = (argb >> 8) & 255, b = argb & 255;
        return 0xFF000000 | ((r + 255) / 2 << 16) | ((g + 255) / 2 << 8) | ((b + 255) / 2);
    }

    public static TextureAtlasSprite sprite(ResourceLocation id) {
        return Minecraft.getInstance().getTextureAtlas(InventoryMenu.BLOCK_ATLAS).apply(id);
    }

    /** Emits the first layer's quads; with a mask the UVs are remapped onto it, otherwise kept. */
    private static void emitSilhouette(BakedModel model, PoseStack pose, VertexConsumer out,
                                       @Nullable TextureAtlasSprite mask) {
        var random = RandomSource.create(42);
        List<BakedQuad> quads = new ArrayList<>();
        for (Direction face : Direction.values()) {
            random.setSeed(42);
            quads.addAll(model.getQuads(null, face, random));
        }
        random.setSeed(42);
        quads.addAll(model.getQuads(null, null, random));
        boolean layered = quads.stream().anyMatch(q -> q.getTintIndex() == 0);
        for (var quad : quads) {
            if (!layered || quad.getTintIndex() == 0) emitQuad(quad, pose, out, mask);
        }
    }

    public static void emitQuad(BakedQuad quad, PoseStack pose, VertexConsumer out,
                                @Nullable TextureAtlasSprite mask) {
        int[] data = quad.getVertices();
        var source = quad.getSprite();
        var normal = quad.getDirection().step();
        int stride = DefaultVertexFormat.BLOCK.getIntegerSize();
        for (int i = 0; i < 4; i++) {
            int offset = i * stride;
            float x = Float.intBitsToFloat(data[offset]) + normal.x() * 0.001f;
            float y = Float.intBitsToFloat(data[offset + 1]) + normal.y() * 0.001f;
            float z = Float.intBitsToFloat(data[offset + 2]) + normal.z() * 0.001f;
            float u = Float.intBitsToFloat(data[offset + 4]);
            float v = Float.intBitsToFloat(data[offset + 5]);
            if (mask != null) {
                u = mask.getU((u - source.getU0()) / (source.getU1() - source.getU0()) * 16);
                v = mask.getV((v - source.getV0()) / (source.getV1() - source.getV0()) * 16);
            }
            vertex(pose, out, x, y, z, u, v, normal);
        }
    }

    public static void vertex(PoseStack pose, VertexConsumer out, float x, float y, float z, float u, float v,
                              Vector3f normal) {
        out.vertex(pose.last().pose(), x, y, z).color(255, 255, 255, 255).uv(u, v)
                .overlayCoords(OverlayTexture.NO_OVERLAY).uv2(FULL_BRIGHT)
                .normal(pose.last().normal(), normal.x(), normal.y(), normal.z()).endVertex();
    }

    /** Replaces vertex colour (keeping alpha) and forces full brightness. */
    private record TintedConsumer(VertexConsumer delegate, int color) implements VertexConsumer {

        @Override
        public VertexConsumer vertex(double x, double y, double z) {
            delegate.vertex(x, y, z);
            return this;
        }

        @Override
        public VertexConsumer color(int r, int g, int b, int a) {
            delegate.color((color >> 16) & 255, (color >> 8) & 255, color & 255, a);
            return this;
        }

        @Override
        public VertexConsumer uv(float u, float v) {
            delegate.uv(u, v);
            return this;
        }

        @Override
        public VertexConsumer overlayCoords(int u, int v) {
            delegate.overlayCoords(u, v);
            return this;
        }

        @Override
        public VertexConsumer uv2(int u, int v) {
            delegate.uv2(240, 240);
            return this;
        }

        @Override
        public VertexConsumer normal(float x, float y, float z) {
            delegate.normal(x, y, z);
            return this;
        }

        @Override
        public void endVertex() {
            delegate.endVertex();
        }

        @Override
        public void defaultColor(int r, int g, int b, int a) {
            delegate.defaultColor((color >> 16) & 255, (color >> 8) & 255, color & 255, a);
        }

        @Override
        public void unsetDefaultColor() {
            delegate.unsetDefaultColor();
        }
    }
}
