package com.raishxn.gtna.mixin.client;

import com.lowdragmc.lowdraglib.client.scene.ISceneBlockRenderHook;
import com.lowdragmc.lowdraglib.client.scene.ISceneEntityRenderHook;
import com.lowdragmc.lowdraglib.client.scene.WorldSceneRenderer;
import com.lowdragmc.lowdraglib.utils.TrackedDummyWorld;

import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.renderer.ShaderInstance;
import net.minecraft.client.renderer.block.BlockRenderDispatcher;
import net.minecraft.client.renderer.block.ModelBlockRenderer;
import net.minecraft.core.BlockPos;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.entity.BlockEntity;

import com.mojang.blaze3d.systems.RenderSystem;
import com.mojang.blaze3d.vertex.BufferBuilder;
import com.mojang.blaze3d.vertex.DefaultVertexFormat;
import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexBuffer;
import com.mojang.blaze3d.vertex.VertexFormat;
import org.jetbrains.annotations.Nullable;
import org.spongepowered.asm.mixin.Final;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.Unique;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

import java.util.ArrayList;
import java.util.Collection;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.atomic.AtomicReference;

/**
 * Faster multiblock previews (EMI/JEI and the structure GUIs) for very large structures.
 *
 * <p>
 * LDLib compiles a cached scene into one buffer per render layer. For structures with hundreds of thousands of blocks
 * (Eye of Harmony, Forge of Gods, Space Elevator) that single buffer grows past what a {@link BufferBuilder} can hold,
 * and nothing is drawn until the whole structure is built. Here the off-thread compile splits every layer into batches
 * of {@link #BATCH_BLOCKS} blocks, each in its own vertex buffer, uploaded and drawn as soon as it is ready.
 *
 * <p>
 * Technique from GTLCore's {@code WorldSceneRendererMixin} (LGPL-3.0, by Dragons); this code is written for GTNA
 * against LDLib 1.0.52's renderer.
 */
@Mixin(value = WorldSceneRenderer.class, remap = false)
public abstract class WorldSceneRendererBatchMixin {

    @Unique
    private static final int BATCH_BLOCKS = 4096;

    @Shadow
    @Final
    public Map<Collection<BlockPos>, ISceneBlockRenderHook> renderedBlocksMap;
    @Shadow
    @Final
    public Level world;
    @Shadow
    protected boolean useCache;
    @Shadow
    protected Thread thread;
    @Shadow
    protected Set<BlockPos> tileEntities;
    @Shadow
    protected int progress;
    @Shadow
    protected int maxProgress;
    @Shadow
    protected boolean endBatchLast;
    @Shadow
    @SuppressWarnings("rawtypes")
    protected AtomicReference cacheState;
    @Shadow
    private ISceneEntityRenderHook sceneEntityRenderHook;

    /** Compiled batches waiting for the render thread, per layer. */
    @Unique
    private List<ConcurrentLinkedQueue<BufferBuilder.RenderedBuffer>> gtna$pending;
    /** Uploaded batches, per layer; only touched on the render thread. */
    @Unique
    private List<List<VertexBuffer>> gtna$batches;

    @Shadow
    private void renderBlocks(PoseStack poseStack, BlockRenderDispatcher dispatcher, RenderType layer,
                              WorldSceneRenderer.VertexConsumerWrapper wrapperBuffer,
                              Collection<BlockPos> renderedBlocks, @Nullable ISceneBlockRenderHook hook,
                              float partialTicks, RandomSource random) {
        throw new AssertionError();
    }

    @Shadow
    private void renderTESR(Collection<BlockPos> poses, PoseStack poseStack, MultiBufferSource.BufferSource buffers,
                            @Nullable ISceneBlockRenderHook hook, float partialTicks) {
        throw new AssertionError();
    }

    @Shadow
    private void renderEntities(TrackedDummyWorld level, PoseStack poseStack, MultiBufferSource buffer,
                                @Nullable ISceneEntityRenderHook hook, float partialTicks) {
        throw new AssertionError();
    }

    @Shadow
    public static void setDefaultRenderLayerState(RenderType layer) {
        throw new AssertionError();
    }

    @Inject(method = "deleteCacheBuffer", at = @At("HEAD"))
    private void gtna$deleteBatches(CallbackInfoReturnable<WorldSceneRenderer> cir) {
        gtna$freeBatches();
    }

    @Inject(method = "needCompileCache", at = @At("HEAD"))
    private void gtna$recompileBatches(CallbackInfoReturnable<WorldSceneRenderer> cir) {
        gtna$freeBatches();
    }

    @Unique
    private void gtna$freeBatches() {
        if (gtna$batches != null) {
            List<List<VertexBuffer>> old = gtna$batches;
            gtna$batches = null;
            Runnable close = () -> old.forEach(list -> list.forEach(VertexBuffer::close));
            if (RenderSystem.isOnRenderThread()) close.run();
            else RenderSystem.recordRenderCall(close::run);
        }
        if (gtna$pending != null) {
            gtna$pending.forEach(queue -> {
                BufferBuilder.RenderedBuffer data;
                while ((data = queue.poll()) != null) data.release();
            });
            gtna$pending = null;
        }
    }

    @Inject(method = "renderCacheBuffer", at = @At("HEAD"), cancellable = true)
    private void gtna$renderBatched(Minecraft mc, MultiBufferSource.BufferSource buffers, float partialTicks,
                                    CallbackInfo ci) {
        ci.cancel();
        List<RenderType> layers = RenderType.chunkBufferLayers();
        if (gtna$isState("NEED")) {
            gtna$freeBatches();
            gtna$pending = new ArrayList<>(layers.size());
            gtna$batches = new ArrayList<>(layers.size());
            for (int i = 0; i < layers.size(); i++) {
                gtna$pending.add(new ConcurrentLinkedQueue<>());
                gtna$batches.add(new ArrayList<>());
            }
            gtna$startCompile(mc, layers, gtna$pending);
            return;
        }
        if (gtna$batches == null || gtna$pending == null) return;
        // Upload what the compile thread finished so far; partial structures show while the rest builds.
        for (int i = 0; i < layers.size(); i++) {
            BufferBuilder.RenderedBuffer data;
            while ((data = gtna$pending.get(i).poll()) != null) {
                VertexBuffer vbo = new VertexBuffer(VertexBuffer.Usage.STATIC);
                vbo.bind();
                vbo.upload(data);
                VertexBuffer.unbind();
                gtna$batches.get(i).add(vbo);
            }
        }
        PoseStack poseStack = new PoseStack();
        for (int i = 0; i < layers.size(); i++) {
            RenderType layer = layers.get(i);
            if (layer == RenderType.translucent() && tileEntities != null) {
                if (world instanceof TrackedDummyWorld level) {
                    renderEntities(level, poseStack, buffers, sceneEntityRenderHook, partialTicks);
                }
                renderTESR(tileEntities, poseStack, mc.renderBuffers().bufferSource(), null, partialTicks);
                if (!endBatchLast) buffers.endBatch();
            }
            List<VertexBuffer> batches = gtna$batches.get(i);
            if (batches.isEmpty()) continue;
            layer.setupRenderState();
            ShaderInstance shader = RenderSystem.getShader();
            if (shader != null) {
                for (int j = 0; j < 12; j++) shader.setSampler("Sampler" + j, RenderSystem.getShaderTexture(j));
                if (shader.MODEL_VIEW_MATRIX != null) shader.MODEL_VIEW_MATRIX.set(RenderSystem.getModelViewMatrix());
                if (shader.PROJECTION_MATRIX != null)
                    shader.PROJECTION_MATRIX.set(RenderSystem.getProjectionMatrix());
                if (shader.COLOR_MODULATOR != null) shader.COLOR_MODULATOR.set(RenderSystem.getShaderColor());
                if (shader.FOG_START != null) shader.FOG_START.set(RenderSystem.getShaderFogStart());
                if (shader.FOG_END != null) shader.FOG_END.set(RenderSystem.getShaderFogEnd());
                if (shader.FOG_COLOR != null) shader.FOG_COLOR.set(RenderSystem.getShaderFogColor());
                if (shader.FOG_SHAPE != null) shader.FOG_SHAPE.set(RenderSystem.getShaderFogShape().getIndex());
                if (shader.TEXTURE_MATRIX != null) shader.TEXTURE_MATRIX.set(RenderSystem.getTextureMatrix());
                if (shader.GAME_TIME != null) shader.GAME_TIME.set(RenderSystem.getShaderGameTime());
                RenderSystem.setupShaderLights(shader);
                shader.apply();
            }
            setDefaultRenderLayerState(layer);
            RenderSystem.setShaderColor(1.0F, 1.0F, 1.0F, 1.0F);
            for (VertexBuffer vbo : batches) {
                if (vbo.isInvalid() || vbo.getFormat() == null) continue;
                vbo.bind();
                vbo.draw();
            }
            VertexBuffer.unbind();
            if (shader != null) shader.clear();
            layer.clearRenderState();
        }
    }

    @Unique
    private void gtna$startCompile(Minecraft mc, List<RenderType> layers,
                                   List<ConcurrentLinkedQueue<BufferBuilder.RenderedBuffer>> pending) {
        if (thread != null) thread.interrupt();
        progress = 0;
        maxProgress = renderedBlocksMap.keySet().stream().map(Collection::size).reduce(0, Integer::sum) *
                (layers.size() + 1);
        gtna$setState("COMPILING");
        long started = System.nanoTime();
        int blocks = maxProgress / (layers.size() + 1);
        thread = new Thread(() -> {
            BlockRenderDispatcher dispatcher = mc.getBlockRenderer();
            RandomSource random = RandomSource.createNewThreadLocalInstance();
            ModelBlockRenderer.enableCaching();
            try {
                PoseStack poseStack = new PoseStack();
                for (int i = 0; i < layers.size(); i++) {
                    RenderType layer = layers.get(i);
                    for (var entry : renderedBlocksMap.entrySet()) {
                        List<BlockPos> chunk = new ArrayList<>(BATCH_BLOCKS);
                        for (BlockPos pos : entry.getKey()) {
                            chunk.add(pos);
                            if (chunk.size() == BATCH_BLOCKS) {
                                if (!gtna$compileBatch(poseStack, dispatcher, layer, chunk, entry.getValue(), random,
                                        pending.get(i)))
                                    return;
                                chunk = new ArrayList<>(BATCH_BLOCKS);
                            }
                        }
                        if (!chunk.isEmpty() && !gtna$compileBatch(poseStack, dispatcher, layer, chunk,
                                entry.getValue(), random, pending.get(i)))
                            return;
                    }
                }
            } finally {
                ModelBlockRenderer.clearCache();
            }
            Set<BlockPos> withRenderer = new HashSet<>();
            for (var renderedBlocks : renderedBlocksMap.keySet()) {
                for (BlockPos pos : renderedBlocks) {
                    if (Thread.interrupted()) return;
                    progress++;
                    BlockEntity tile = world.getBlockEntity(pos);
                    if (tile != null && mc.getBlockEntityRenderDispatcher().getRenderer(tile) != null) {
                        withRenderer.add(pos);
                    }
                }
            }
            tileEntities = withRenderer;
            gtna$setState("COMPILED");
            long ms = (System.nanoTime() - started) / 1_000_000;
            if (ms > 500)
                com.raishxn.gtna.GTNACORE.LOGGER.info("[GTNA perf] preview scene of {} blocks compiled in {} ms",
                        blocks, ms);
            thread = null;
            maxProgress = -1;
        }, "GTNA scene compile");
        thread.setDaemon(true);
        thread.start();
    }

    // LDLib's CacheState enum is package-private: read and write it by constant name.
    @Unique
    private boolean gtna$isState(String name) {
        return cacheState.get() instanceof Enum<?> state && state.name().equals(name);
    }

    @Unique
    @SuppressWarnings({ "unchecked", "rawtypes" })
    private void gtna$setState(String name) {
        if (cacheState.get() instanceof Enum<?> state) {
            cacheState.set(Enum.valueOf((Class) state.getDeclaringClass(), name));
        }
    }

    /** Compiles one batch; returns false when the thread was interrupted. */
    @Unique
    private boolean gtna$compileBatch(PoseStack poseStack, BlockRenderDispatcher dispatcher, RenderType layer,
                                      List<BlockPos> blocks, @Nullable ISceneBlockRenderHook hook,
                                      RandomSource random,
                                      ConcurrentLinkedQueue<BufferBuilder.RenderedBuffer> out) {
        if (Thread.currentThread().isInterrupted()) return false;
        BufferBuilder buffer = new BufferBuilder(layer.bufferSize());
        buffer.begin(VertexFormat.Mode.QUADS, DefaultVertexFormat.BLOCK);
        renderBlocks(poseStack, dispatcher, layer, new WorldSceneRenderer.VertexConsumerWrapper(buffer), blocks, hook,
                0.0F, random);
        progress += blocks.size();
        BufferBuilder.RenderedBuffer data = buffer.endOrDiscardIfEmpty();
        if (data != null) out.add(data);
        return true;
    }
}
