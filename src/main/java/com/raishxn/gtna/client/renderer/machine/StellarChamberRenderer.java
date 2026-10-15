package com.raishxn.gtna.client.renderer.machine;

import com.gregtechceu.gtceu.client.renderer.machine.DynamicRender;
import com.gregtechceu.gtceu.client.renderer.machine.DynamicRenderManager;
import com.gregtechceu.gtceu.client.renderer.machine.DynamicRenderType;

import net.minecraft.client.renderer.GameRenderer;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.core.BlockPos;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.Vec3;

import com.mojang.blaze3d.systems.RenderSystem;
import com.mojang.blaze3d.vertex.BufferBuilder;
import com.mojang.blaze3d.vertex.DefaultVertexFormat;
import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.Tesselator;
import com.mojang.blaze3d.vertex.VertexBuffer;
import com.mojang.blaze3d.vertex.VertexFormat;
import com.mojang.serialization.Codec;
import com.raishxn.gtna.GTNACORE;
import com.raishxn.gtna.common.machine.multiblock.originals.StellarChamberMachine;
import org.jetbrains.annotations.Nullable;
import org.joml.Matrix4f;

import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Neutron star of the Stellar Containment Chamber: a bright blue-white star (Forge of Gods star shader, blue), two
 * pulsar beams sweeping around the tilted magnetic axis, dipole field lines and an orange accretion disk. In black
 * hole mode the star turns into a black sphere with a photon ring. The hull and bands are real blocks and stay still.
 */
public class StellarChamberRenderer extends DynamicRender<StellarChamberMachine, StellarChamberRenderer> {

    public static final Codec<StellarChamberRenderer> CODEC = Codec.unit(StellarChamberRenderer::new);
    public static final DynamicRenderType<StellarChamberMachine, StellarChamberRenderer> TYPE = DynamicRenderManager
            .register(GTNACORE.id("stellar_chamber/render"), new DynamicRenderType<>(CODEC));

    private static final float STAR_RADIUS = 5f, CORONA_RADIUS = 13f, BEAM_LENGTH = 90f, BEAM_WIDTH = 4f,
            DISK_RADIUS = 28f, LENS_RANGE = 160f;
    private static final float AXIS_TILT = 0.5f;

    @Nullable
    private static VertexBuffer sphere;
    /** Free-standing star for {@code /gtna_star_preview}; null when off. */
    @Nullable
    public static Vec3 debugCenter;
    public static boolean debugHole, debugNoLens;
    private static final Map<BlockPos, StellarChamberMachine> QUEUE = new LinkedHashMap<>();

    @Override
    public DynamicRenderType<StellarChamberMachine, StellarChamberRenderer> getType() {
        return TYPE;
    }

    @Override
    public boolean shouldRender(StellarChamberMachine machine, Vec3 cameraPos) {
        return machine.isStarRunning();
    }

    @Override
    public boolean shouldRenderOffScreen(StellarChamberMachine machine) {
        return true;
    }

    @Override
    public int getViewDistance() {
        return 256;
    }

    @Override
    public AABB getRenderBoundingBox(StellarChamberMachine machine) {
        return new AABB(machine.center()).inflate(BEAM_LENGTH + STAR_RADIUS + 2);
    }

    @Override
    public void render(StellarChamberMachine machine, float partialTicks, PoseStack poseStack, MultiBufferSource buffer,
                       int combinedLight, int combinedOverlay) {
        if (machine.getLevel() != null && machine.isStarRunning()) QUEUE.put(machine.getPos().immutable(), machine);
    }

    public static void onRenderLevelStage(net.minecraftforge.client.event.RenderLevelStageEvent event) {
        if (event.getStage() == net.minecraftforge.client.event.RenderLevelStageEvent.Stage.AFTER_LEVEL) {
            try {
                applyLenses(new Matrix4f(event.getProjectionMatrix()));
            } finally {
                LENSES.clear();
            }
            return;
        }
        if (event.getStage() != net.minecraftforge.client.event.RenderLevelStageEvent.Stage.AFTER_TRANSLUCENT_BLOCKS ||
                (QUEUE.isEmpty() && debugCenter == null))
            return;
        Vec3 camera = event.getCamera().getPosition();
        PoseStack pose = event.getPoseStack();
        Matrix4f projection = new Matrix4f(event.getProjectionMatrix());
        try {
            for (var machine : QUEUE.values()) {
                if (machine.isInValid() || !machine.isStarRunning()) continue;
                BlockPos c = machine.center();
                pose.pushPose();
                pose.translate(c.getX() + 0.5 - camera.x, c.getY() + 0.5 - camera.y, c.getZ() + 0.5 - camera.z);
                draw(machine, pose, projection);
                pose.popPose();
            }
            if (debugCenter != null) {
                pose.pushPose();
                pose.translate(debugCenter.x - camera.x, debugCenter.y - camera.y, debugCenter.z - camera.z);
                drawStar(new Star(0.033f, debugHole, false), new Matrix4f(pose.last().pose()), projection);
                pose.popPose();
            }
        } finally {
            QUEUE.clear();
            RenderSystem.depthMask(true);
            RenderSystem.disableBlend();
            RenderSystem.defaultBlendFunc();
            RenderSystem.enableCull();
            RenderSystem.enableDepthTest();
        }
    }

    /** Star parameters for one frame: from a machine, or the debug preview. */
    private record Star(float period, boolean hole, boolean magnetar) {}

    private static void draw(StellarChamberMachine machine, PoseStack pose, Matrix4f projection) {
        drawStar(new Star((float) machine.renderPeriod(), machine.isBlackHole(), machine.isMagnetar()),
                new Matrix4f(pose.last().pose()), projection);
    }

    /**
     * The effects of the 3D preview (docs/roadmap/design): procedural neutron-star surface with hot polar caps,
     * fresnel corona, two pulsing beam cones on the tilted magnetic axis, dipole field lines, a spiral accretion disk.
     */
    private static void drawStar(Star star, Matrix4f center, Matrix4f projection) {
        var shader = StellarShaders.fx();
        var glow = StellarShaders.fxAdditive();
        if (shader == null || glow == null) return;
        float time = (float) ((net.minecraft.Util.getMillis() % 3_600_000L) / 1000.0);
        // Visible spin: a real pulsar is far too fast to see; shorter periods still turn faster.
        float spin = time * (float) Math.min(4.0, 2.2 * Math.sqrt(0.033 / Math.max(1e-3, star.period())));
        float r = 0.55f, g = 0.75f, b = 1f;
        if (star.magnetar()) {
            r = 0.85f;
            g = 0.55f;
        }
        for (var sh : new net.minecraft.client.renderer.ShaderInstance[] { shader, glow }) {
            sh.safeGetUniform("Time").set(time);
            sh.safeGetUniform("Tint").set(r, g, b, 1f);
        }
        RenderSystem.enableDepthTest();

        // Star (opaque) or event horizon.
        RenderSystem.disableBlend();
        RenderSystem.depthMask(true);
        RenderSystem.disableCull();
        shader.safeGetUniform("Mode").set(star.hole() ? 4f : 0f);
        drawMesh(sphere(), new Matrix4f(center).rotateY(spin).scale(STAR_RADIUS), projection, shader);

        // Additive glow passes (the glow shader carries the additive blend mode).
        shader = glow;
        RenderSystem.enableBlend();
        RenderSystem.blendFunc(com.mojang.blaze3d.platform.GlStateManager.SourceFactor.SRC_ALPHA,
                com.mojang.blaze3d.platform.GlStateManager.DestFactor.ONE);
        RenderSystem.depthMask(false);
        if (!star.hole()) {
            // Corona: a fresnel shell that is bright at its rim and clear in front of the star.
            RenderSystem.disableCull();
            shader.safeGetUniform("Mode").set(1f);
            drawMesh(sphere(), new Matrix4f(center).scale(CORONA_RADIUS), projection, shader);
            Matrix4f axis = new Matrix4f(center).rotateZ(AXIS_TILT).rotateY(spin);
            shader.safeGetUniform("Mode").set(2f);
            drawMesh(cone(), axis, projection, shader);
            drawMesh(cone(), new Matrix4f(axis).rotateX((float) Math.PI), projection, shader);
            var lines = StellarShaders.additiveColor();
            RenderSystem.setShader(lines != null ? () -> lines : GameRenderer::getPositionColorShader);
            fieldLines(axis, 0.56f, 0.73f, 1f);
        }
        RenderSystem.disableCull();
        shader.safeGetUniform("Mode").set(3f);
        shader.safeGetUniform("Tint").set(r, g, b, star.hole() ? 1.6f : 1f);
        drawMesh(disk(), new Matrix4f(center).rotateX(0.25f), projection, shader);
        RenderSystem.enableCull();
        LENSES.add(new float[] { center.m30(), center.m31(), center.m32(), star.hole() ? 1.4f : 1f });
    }

    private static void drawMesh(VertexBuffer mesh, Matrix4f model, Matrix4f projection,
                                 net.minecraft.client.renderer.ShaderInstance shader) {
        mesh.bind();
        mesh.drawWithShader(model, projection, shader);
        VertexBuffer.unbind();
    }

    /** Dipole field lines r = R sin^2(theta), co-rotating with the beams. */
    private static void fieldLines(Matrix4f axis, float r, float g, float b) {
        BufferBuilder buf = Tesselator.getInstance().getBuilder();
        RenderSystem.lineWidth(2f);
        buf.begin(VertexFormat.Mode.DEBUG_LINES, DefaultVertexFormat.POSITION_COLOR);
        for (int k = 0; k < 10; k++) {
            double ph = k * Math.PI / 5;
            float big = 9 + (k % 3) * 5;
            float[] prev = null;
            for (int i = 0; i <= 80; i++) {
                double th = 0.15 + i / 80.0 * (Math.PI - 0.3);
                double rr = big * Math.sin(th) * Math.sin(th);
                float[] p = { (float) (rr * Math.sin(th) * Math.cos(ph)), (float) (rr * Math.cos(th)),
                        (float) (rr * Math.sin(th) * Math.sin(ph)) };
                if (prev != null) {
                    buf.vertex(axis, prev[0], prev[1], prev[2]).color(r, g, b, 0.55f).endVertex();
                    buf.vertex(axis, p[0], p[1], p[2]).color(r, g, b, 0.55f).endVertex();
                }
                prev = p;
            }
        }
        Tesselator.getInstance().end();
    }

    @Nullable
    private static VertexBuffer cone, disk;

    /** Open cone along +Y: apex at the star's surface (v = 1), wide end BEAM_LENGTH away (v = 0). */
    private static VertexBuffer cone() {
        if (cone != null) return cone;
        BufferBuilder builder = new BufferBuilder(32 * 6 * 20);
        builder.begin(VertexFormat.Mode.TRIANGLES, DefaultVertexFormat.POSITION_TEX);
        int seg = 32;
        float y0 = STAR_RADIUS * 0.6f, y1 = y0 + BEAM_LENGTH;
        for (int i = 0; i < seg; i++) {
            double a0 = 2 * Math.PI * i / seg, a1 = 2 * Math.PI * (i + 1) / seg;
            float u0 = (float) i / seg, u1 = (float) (i + 1) / seg;
            builder.vertex(0, y0, 0).uv(u0, 1).endVertex();
            builder.vertex((float) Math.cos(a0) * BEAM_WIDTH, y1, (float) Math.sin(a0) * BEAM_WIDTH).uv(u0, 0)
                    .endVertex();
            builder.vertex((float) Math.cos(a1) * BEAM_WIDTH, y1, (float) Math.sin(a1) * BEAM_WIDTH).uv(u1, 0)
                    .endVertex();
        }
        cone = upload(builder);
        return cone;
    }

    /** Flat square in the XZ plane, UV 0..1; the shader cuts the ring. */
    private static VertexBuffer disk() {
        if (disk != null) return disk;
        BufferBuilder builder = new BufferBuilder(6 * 20);
        builder.begin(VertexFormat.Mode.TRIANGLES, DefaultVertexFormat.POSITION_TEX);
        float h = DISK_RADIUS;
        float[][] q = { { -h, -h, 0, 0 }, { h, -h, 1, 0 }, { h, h, 1, 1 }, { -h, h, 0, 1 } };
        for (int k : new int[] { 0, 1, 2, 0, 2, 3 })
            builder.vertex(q[k][0], 0, q[k][1]).uv(q[k][2], q[k][3]).endVertex();
        disk = upload(builder);
        return disk;
    }

    private static VertexBuffer upload(BufferBuilder builder) {
        var vbo = new VertexBuffer(VertexBuffer.Usage.STATIC);
        vbo.bind();
        vbo.upload(builder.end());
        VertexBuffer.unbind();
        return vbo;
    }

    // ------------------------------------------------------------------ gravitational lens

    /** View-space centres of the stars drawn this frame, {x, y, z, strength}. */
    private static final java.util.List<float[]> LENSES = new java.util.ArrayList<>();
    @Nullable
    private static com.mojang.blaze3d.pipeline.TextureTarget sceneCopy;

    /** Screen-space lens after everything else in the level is drawn (the preview's post pass). */
    private static void applyLenses(Matrix4f projection) {
        var shader = StellarShaders.lens();
        if (shader == null || LENSES.isEmpty() || debugNoLens) return;
        var mc = net.minecraft.client.Minecraft.getInstance();
        var main = mc.getMainRenderTarget();
        if (sceneCopy == null || sceneCopy.width != main.width || sceneCopy.height != main.height) {
            if (sceneCopy != null) sceneCopy.destroyBuffers();
            sceneCopy = new com.mojang.blaze3d.pipeline.TextureTarget(main.width, main.height, false,
                    net.minecraft.client.Minecraft.ON_OSX);
        }
        float aspect = (float) main.width / main.height;
        for (float[] lens : LENSES) {
            var view = new org.joml.Vector4f(lens[0], lens[1], lens[2], 1);
            float dist = view.length();
            float k = Math.max(0, Math.min(1, (LENS_RANGE - dist) / (LENS_RANGE * 0.65f))) * 0.75f * lens[3];
            if (k <= 0) continue;
            var clip = new org.joml.Vector4f(view).mul(projection);
            if (clip.w <= 0) continue;
            float cx = clip.x / clip.w * 0.5f + 0.5f, cy = clip.y / clip.w * 0.5f + 0.5f;
            var edge = new org.joml.Vector4f(lens[0], lens[1] + STAR_RADIUS * 2.2f, lens[2], 1).mul(projection);
            float radius = Math.abs(edge.y / edge.w * 0.5f + 0.5f - cy);
            var rim = new org.joml.Vector4f(lens[0], lens[1] + STAR_RADIUS, lens[2], 1).mul(projection);
            float starRadius = Math.abs(rim.y / rim.w * 0.5f + 0.5f - cy);
            if (radius > 1.5f) continue;
            // Copy the frame, then draw it back through the lens.
            com.mojang.blaze3d.platform.GlStateManager._glBindFramebuffer(org.lwjgl.opengl.GL30.GL_READ_FRAMEBUFFER,
                    main.frameBufferId);
            com.mojang.blaze3d.platform.GlStateManager._glBindFramebuffer(org.lwjgl.opengl.GL30.GL_DRAW_FRAMEBUFFER,
                    sceneCopy.frameBufferId);
            com.mojang.blaze3d.platform.GlStateManager._glBlitFrameBuffer(0, 0, main.width, main.height, 0, 0,
                    main.width, main.height, org.lwjgl.opengl.GL11.GL_COLOR_BUFFER_BIT,
                    org.lwjgl.opengl.GL11.GL_NEAREST);
            main.bindWrite(false);
            shader.setSampler("Scene", sceneCopy.getColorTextureId());
            shader.safeGetUniform("Center").set(cx, cy);
            shader.safeGetUniform("Radius").set(radius);
            shader.safeGetUniform("StarRadius").set(starRadius);
            shader.safeGetUniform("Strength").set(k);
            shader.safeGetUniform("Aspect").set(aspect);
            RenderSystem.disableDepthTest();
            RenderSystem.disableBlend();
            RenderSystem.depthMask(false);
            RenderSystem.setShader(() -> shader);
            BufferBuilder buf = Tesselator.getInstance().getBuilder();
            buf.begin(VertexFormat.Mode.QUADS, DefaultVertexFormat.POSITION_TEX);
            buf.vertex(-1, -1, 0).uv(0, 0).endVertex();
            buf.vertex(1, -1, 0).uv(1, 0).endVertex();
            buf.vertex(1, 1, 0).uv(1, 1).endVertex();
            buf.vertex(-1, 1, 0).uv(0, 1).endVertex();
            com.mojang.blaze3d.vertex.BufferUploader.drawWithShader(buf.end());
            RenderSystem.enableDepthTest();
        }
    }

    private static VertexBuffer sphere() {
        if (sphere != null) return sphere;
        BufferBuilder builder = new BufferBuilder(64 * 64 * 6 * 20);
        builder.begin(VertexFormat.Mode.TRIANGLES, DefaultVertexFormat.POSITION_TEX);
        int n = 64;
        for (int i = 0; i < n; i++) {
            float v0 = (float) i / n, v1 = (float) (i + 1) / n;
            double p0 = Math.PI / 2 - i * Math.PI / n, p1 = Math.PI / 2 - (i + 1) * Math.PI / n;
            for (int j = 0; j < n; j++) {
                float u0 = 1f - (float) j / n, u1 = 1f - (float) (j + 1) / n;
                double t0 = j * 2 * Math.PI / n, t1 = (j + 1) * 2 * Math.PI / n;
                float[][] q = {
                        { (float) (Math.cos(p0) * Math.cos(t0)), (float) Math.sin(p0),
                                (float) (Math.cos(p0) * Math.sin(t0)), u0, v0 },
                        { (float) (Math.cos(p1) * Math.cos(t0)), (float) Math.sin(p1),
                                (float) (Math.cos(p1) * Math.sin(t0)), u0, v1 },
                        { (float) (Math.cos(p1) * Math.cos(t1)), (float) Math.sin(p1),
                                (float) (Math.cos(p1) * Math.sin(t1)), u1, v1 },
                        { (float) (Math.cos(p0) * Math.cos(t1)), (float) Math.sin(p0),
                                (float) (Math.cos(p0) * Math.sin(t1)), u1, v0 } };
                for (int k : new int[] { 0, 1, 2, 0, 2, 3 })
                    builder.vertex(q[k][0], q[k][1], q[k][2]).uv(q[k][3], q[k][4]).endVertex();
            }
        }
        sphere = new VertexBuffer(VertexBuffer.Usage.STATIC);
        sphere.bind();
        sphere.upload(builder.end());
        VertexBuffer.unbind();
        return sphere;
    }
}
