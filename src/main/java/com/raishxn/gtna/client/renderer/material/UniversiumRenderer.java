package com.raishxn.gtna.client.renderer.material;

import com.gregtechceu.gtceu.api.block.MaterialBlock;
import com.gregtechceu.gtceu.api.data.tag.TagPrefix;

import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.renderer.block.model.BakedQuad;
import net.minecraft.client.renderer.texture.TextureAtlasSprite;
import net.minecraft.client.resources.model.BakedModel;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.RandomSource;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.material.Fluid;
import net.minecraftforge.client.event.RenderLevelStageEvent;
import net.minecraftforge.event.TickEvent;
import net.minecraftforge.registries.ForgeRegistries;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import com.raishxn.gtna.GTNACORE;
import com.raishxn.gtna.client.renderer.effect.CosmicShader;
import com.raishxn.gtna.client.renderer.effect.ItemEffectRenderer;
import com.raishxn.gtna.common.data.GTNAMaterials;
import org.joml.Vector3f;

/** Universium's live star field (GTNA item effect shader) on world surfaces and non-material items. */
public final class UniversiumRenderer {

    private static final ResourceLocation SOLID = GTNACORE.id("item/universium/solid_mask");
    private static final ResourceLocation FRAME = GTNACORE.id("item/universium/frame_mask");
    private static final ResourceLocation NANITES = GTNACORE.id("item/universium/nanites_mask");
    /** RenderBlender's cosmic star field (see {@link CosmicShader}), lifted off the surface. */
    private static final RenderType COSMIC = CosmicShader.WORLD;
    private static net.minecraft.client.multiplayer.ClientLevel cachedLevel;

    private UniversiumRenderer() {}

    public static boolean isFluid(Fluid fluid) {
        return GTNAMaterials.Universium != null && fluid.isSame(GTNAMaterials.Universium.getFluid());
    }

    private static boolean isBlock(BlockState state) {
        return state.getBlock() instanceof MaterialBlock block && block.material == GTNAMaterials.Universium &&
                (block.tagPrefix == TagPrefix.block || block.tagPrefix == TagPrefix.frameGt);
    }

    private static boolean ready(boolean inventory) {
        if (!ItemEffectRenderer.shaderEffectsEnabled() || !CosmicShader.ready()) return false;
        CosmicShader.prepare(inventory);
        return true;
    }

    private static TextureAtlasSprite sprite(ResourceLocation id) {
        return ItemEffectRenderer.sprite(id);
    }

    public static void renderItem(ItemStack stack, net.minecraft.world.item.ItemDisplayContext context,
                                  BakedModel model, PoseStack pose, MultiBufferSource buffers) {
        ResourceLocation mask;
        if (stack.getItem() instanceof BlockItem item && isBlock(item.getBlock().defaultBlockState())) {
            var block = (MaterialBlock) item.getBlock();
            mask = block.tagPrefix == TagPrefix.frameGt ? FRAME : SOLID;
        } else if (ForgeRegistries.ITEMS.getKey(stack.getItem()).equals(GTNACORE.id("universium_nanites"))) {
            mask = NANITES;
        } else return;
        if (!ready(context == net.minecraft.world.item.ItemDisplayContext.GUI)) return;
        // Draw the batched block icon first, so the star field lands on it instead of under it.
        if (buffers instanceof MultiBufferSource.BufferSource source) source.endBatch();
        var out = buffers.getBuffer(COSMIC);
        emitModel(model, null, null, pose, out, sprite(mask));
        if (buffers instanceof MultiBufferSource.BufferSource source) source.endBatch(COSMIC);
    }

    private static void emitModel(BakedModel model, BlockState state, BlockPos pos, PoseStack pose,
                                  VertexConsumer out, TextureAtlasSprite mask) {
        var random = RandomSource.create(42);
        for (Direction face : Direction.values()) {
            if (state != null && !Block.shouldRenderFace(state, Minecraft.getInstance().level, pos, face,
                    pos.relative(face)))
                continue;
            random.setSeed(42);
            for (var quad : model.getQuads(state, face, random)) emitQuad(quad, pose, out, mask);
        }
        random.setSeed(42);
        for (var quad : model.getQuads(state, null, random)) emitQuad(quad, pose, out, mask);
    }

    private static void emitQuad(BakedQuad quad, PoseStack pose, VertexConsumer out, TextureAtlasSprite mask) {
        int[] data = quad.getVertices();
        var source = quad.getSprite();
        var normal = quad.getDirection().step();
        for (int i = 0; i < 4; i++) {
            int offset = i * 8;
            float x = Float.intBitsToFloat(data[offset]) + normal.x() * 0.001f;
            float y = Float.intBitsToFloat(data[offset + 1]) + normal.y() * 0.001f;
            float z = Float.intBitsToFloat(data[offset + 2]) + normal.z() * 0.001f;
            float u = (Float.intBitsToFloat(data[offset + 4]) - source.getU0()) / (source.getU1() - source.getU0());
            float v = (Float.intBitsToFloat(data[offset + 5]) - source.getV0()) / (source.getV1() - source.getV0());
            vertex(pose, out, x, y, z, mask.getU(u * 16), mask.getV(v * 16), normal);
        }
    }

    private static void vertex(PoseStack pose, VertexConsumer out, float x, float y, float z,
                               float u, float v, Vector3f normal) {
        out.vertex(pose.last().pose(), x, y, z).color(255, 255, 255, 255).uv(u, v).uv2(240, 240)
                .normal(pose.last().normal(), normal.x(), normal.y(), normal.z()).endVertex();
    }

    public static void renderFluidGui(GuiGraphics graphics, float x, float y, float width, float height) {
        renderFluidGui(graphics, x, y, width, height, 0.01f);
    }

    public static void renderFluidGui(GuiGraphics graphics, float x, float y, float width, float height, float depth) {
        if (width <= 0 || height <= 0 || !ready(true)) return;
        graphics.flush();
        var out = graphics.bufferSource().getBuffer(COSMIC);
        var s = sprite(SOLID);
        var n = new Vector3f(0, 0, 1);
        var pose = graphics.pose();
        vertex(pose, out, x, y, depth, s.getU0(), s.getV0(), n);
        vertex(pose, out, x, y + height, depth, s.getU0(), s.getV1(), n);
        vertex(pose, out, x + width, y + height, depth, s.getU1(), s.getV1(), n);
        vertex(pose, out, x + width, y, depth, s.getU1(), s.getV0(), n);
        graphics.bufferSource().endBatch(COSMIC);
    }

    // ------------------------------------------------------------------ tracking world surfaces

    /** Universium blocks and fluid in loaded chunks, by chunk. Kept current on load, unload and every change. */
    private static final it.unimi.dsi.fastutil.longs.Long2ObjectOpenHashMap<it.unimi.dsi.fastutil.longs.LongOpenHashSet> TRACKED = new it.unimi.dsi.fastutil.longs.Long2ObjectOpenHashMap<>();
    /** Distance from the camera within which the star field is drawn. */
    private static final double RANGE = 64;

    private static boolean tracked(BlockState state) {
        return isBlock(state) || isFluid(state.getFluidState().getType());
    }

    /**
     * A block changed on the client (from {@code ClientLevel.sendBlockUpdated}): placed Universium gets its star
     * field in the same frame instead of after the next scan.
     */
    public static void blockChanged(BlockPos pos, BlockState newState) {
        long chunk = net.minecraft.world.level.ChunkPos.asLong(pos.getX() >> 4, pos.getZ() >> 4);
        if (tracked(newState)) TRACKED.computeIfAbsent(chunk, k -> new it.unimi.dsi.fastutil.longs.LongOpenHashSet())
                .add(pos.asLong());
        else {
            var set = TRACKED.get(chunk);
            if (set != null && set.remove(pos.asLong()) && set.isEmpty()) TRACKED.remove(chunk);
        }
    }

    public static void chunkLoaded(net.minecraftforge.event.level.ChunkEvent.Load event) {
        if (!event.getLevel().isClientSide() ||
                !(event.getChunk() instanceof net.minecraft.world.level.chunk.LevelChunk chunk))
            return;
        var cp = chunk.getPos();
        var set = new it.unimi.dsi.fastutil.longs.LongOpenHashSet();
        var sections = chunk.getSections();
        for (int si = 0; si < sections.length; si++) {
            var section = sections[si];
            // Palettes answer "maybe has" without touching the 4096 entries.
            if (section.hasOnlyAir() || !section.maybeHas(UniversiumRenderer::tracked)) continue;
            int bottom = chunk.getSectionYFromSectionIndex(si) << 4;
            for (int y = 0; y < 16; y++) for (int z = 0; z < 16; z++) for (int x = 0; x < 16; x++)
                if (tracked(section.getBlockState(x, y, z)))
                    set.add(BlockPos.asLong(cp.getMinBlockX() + x, bottom + y, cp.getMinBlockZ() + z));
        }
        if (set.isEmpty()) TRACKED.remove(cp.toLong());
        else TRACKED.put(cp.toLong(), set);
    }

    public static void chunkUnloaded(net.minecraftforge.event.level.ChunkEvent.Unload event) {
        if (event.getLevel().isClientSide()) TRACKED.remove(event.getChunk().getPos().toLong());
    }

    public static void tick(TickEvent.ClientTickEvent event) {
        if (event.phase != TickEvent.Phase.END) return;
        var mc = Minecraft.getInstance();
        if (mc.level != cachedLevel) {
            TRACKED.clear();
            cachedLevel = mc.level;
        }
    }

    public static void renderWorld(RenderLevelStageEvent event) {
        if (event.getStage() != RenderLevelStageEvent.Stage.AFTER_TRANSLUCENT_BLOCKS || TRACKED.isEmpty() ||
                !ready(false))
            return;
        var mc = Minecraft.getInstance();
        if (mc.level == null) return;
        var pose = event.getPoseStack();
        var camera = event.getCamera().getPosition();
        var buffers = mc.renderBuffers().bufferSource();
        var out = buffers.getBuffer(COSMIC);
        var pos = new BlockPos.MutableBlockPos();
        for (var chunk : TRACKED.long2ObjectEntrySet()) {
            int cx = net.minecraft.world.level.ChunkPos.getX(chunk.getLongKey()) * 16 + 8;
            int cz = net.minecraft.world.level.ChunkPos.getZ(chunk.getLongKey()) * 16 + 8;
            double dx = cx - camera.x, dz = cz - camera.z;
            if (dx * dx + dz * dz > (RANGE + 12) * (RANGE + 12)) continue;
            for (long packed : chunk.getValue()) {
                pos.set(packed);
                if (pos.distToCenterSqr(camera) > RANGE * RANGE ||
                        !event.getFrustum().isVisible(new net.minecraft.world.phys.AABB(pos)))
                    continue;
                renderSurface(mc, pos, pose, camera, out);
            }
        }
        buffers.endBatch(COSMIC);
    }

    private static void renderSurface(Minecraft mc, BlockPos pos, PoseStack pose,
                                      net.minecraft.world.phys.Vec3 camera, VertexConsumer out) {
        {
            var state = mc.level.getBlockState(pos);
            pose.pushPose();
            pose.translate(pos.getX() - camera.x, pos.getY() - camera.y, pos.getZ() - camera.z);
            if (isBlock(state)) {
                var block = (MaterialBlock) state.getBlock();
                emitModel(mc.getBlockRenderer().getBlockModel(state), state, pos, pose, out,
                        sprite(block.tagPrefix == TagPrefix.frameGt ? FRAME : SOLID));
            } else if (isFluid(state.getFluidState().getType())) {
                renderFluidSurface(mc.level, pos, pose, out);
            }
            pose.popPose();
        }
    }

    private static float fluidCorner(net.minecraft.client.multiplayer.ClientLevel level, BlockPos pos, int dx, int dz) {
        float total = 0, weight = 0;
        for (int x : new int[] { 0, dx }) for (int z : new int[] { 0, dz }) {
            var sample = pos.offset(x, 0, z);
            var state = level.getFluidState(sample);
            if (isFluid(state.getType())) {
                if (isFluid(level.getFluidState(sample.above()).getType())) return 1;
                float h = state.getOwnHeight();
                float w = h >= 0.8f ? 10 : 1;
                total += h * w;
                weight += w;
            } else if (!level.getBlockState(sample).isSolid()) weight++;
        }
        return weight == 0 ? 0 : total / weight;
    }

    private static void surface(PoseStack pose, VertexConsumer out, TextureAtlasSprite s, Vector3f n, float... points) {
        for (int i = 0; i < 4; i++) {
            vertex(pose, out, points[i * 3] + n.x() * 0.002f, points[i * 3 + 1] + n.y() * 0.002f,
                    points[i * 3 + 2] + n.z() * 0.002f,
                    i >= 2 ? s.getU1() : s.getU0(), (i == 1 || i == 2) ? s.getV1() : s.getV0(), n);
        }
    }

    private static void renderFluidSurface(net.minecraft.client.multiplayer.ClientLevel level, BlockPos pos,
                                           PoseStack pose, VertexConsumer out) {
        float nw = fluidCorner(level, pos, -1, -1), ne = fluidCorner(level, pos, 1, -1);
        float sw = fluidCorner(level, pos, -1, 1), se = fluidCorner(level, pos, 1, 1);
        var s = sprite(SOLID);
        if (!isFluid(level.getFluidState(pos.above()).getType()))
            surface(pose, out, s, new Vector3f(0, 1, 0), 0, nw, 0, 0, sw, 1, 1, se, 1, 1, ne, 0);
        for (var face : Direction.Plane.HORIZONTAL) {
            var neighbor = pos.relative(face);
            if (isFluid(level.getFluidState(neighbor).getType()) ||
                    level.getBlockState(neighbor).isSolidRender(level, neighbor))
                continue;
            var n = face.step();
            switch (face) {
                case NORTH -> surface(pose, out, s, n, 0, 0, 0, 0, nw, 0, 1, ne, 0, 1, 0, 0);
                case SOUTH -> surface(pose, out, s, n, 1, 0, 1, 1, se, 1, 0, sw, 1, 0, 0, 1);
                case WEST -> surface(pose, out, s, n, 0, 0, 1, 0, sw, 1, 0, nw, 0, 0, 0, 0);
                case EAST -> surface(pose, out, s, n, 1, 0, 0, 1, ne, 0, 1, se, 1, 1, 0, 1);
                default -> {}
            }
        }
        var below = pos.below();
        if (!isFluid(level.getFluidState(below).getType()) && !level.getBlockState(below).isSolidRender(level, below))
            surface(pose, out, s, new Vector3f(0, -1, 0), 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1);
    }
}
