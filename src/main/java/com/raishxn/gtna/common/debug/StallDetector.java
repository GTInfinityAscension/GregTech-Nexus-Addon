package com.raishxn.gtna.common.debug;

import net.minecraftforge.event.TickEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.loading.FMLEnvironment;

import com.raishxn.gtna.GTNACORE;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Development aid: when the server tick or the client frame stops advancing for more than three seconds, logs the
 * stuck thread's stack every three seconds ({@code [GTNA stall]}), so a freeze in a test world shows where it is
 * spent. Only runs outside production.
 */
@Mod.EventBusSubscriber(modid = GTNACORE.MOD_ID)
public final class StallDetector {

    private static final long LIMIT_MS = 3000;
    private static final Map<String, Beat> BEATS = new ConcurrentHashMap<>();
    private static volatile boolean started;

    private record Beat(Thread thread, long time) {}

    private StallDetector() {}

    /** Records that {@code name}'s thread (the current one) made progress. */
    public static void beat(String name) {
        if (FMLEnvironment.production) return;
        BEATS.put(name, new Beat(Thread.currentThread(), System.currentTimeMillis()));
        if (!started) start();
    }

    private static synchronized void start() {
        if (started) return;
        started = true;
        var watcher = new Thread(() -> {
            Map<String, Long> lastReport = new ConcurrentHashMap<>();
            while (true) {
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    return;
                }
                long now = System.currentTimeMillis();
                for (var e : BEATS.entrySet()) {
                    long stuck = now - e.getValue().time();
                    if (stuck < LIMIT_MS || now - lastReport.getOrDefault(e.getKey(), 0L) < LIMIT_MS) continue;
                    lastReport.put(e.getKey(), now);
                    var sb = new StringBuilder("[GTNA stall] ").append(e.getKey()).append(" stuck for ")
                            .append(stuck / 1000).append(" s:");
                    var frames = e.getValue().thread().getStackTrace();
                    for (int i = 0; i < Math.min(40, frames.length); i++) sb.append("\n    at ").append(frames[i]);
                    GTNACORE.LOGGER.warn(sb.toString());
                }
            }
        }, "GTNA stall detector");
        watcher.setDaemon(true);
        watcher.start();
    }

    @SubscribeEvent
    public static void onServerTick(TickEvent.ServerTickEvent event) {
        beat("server");
    }
}
