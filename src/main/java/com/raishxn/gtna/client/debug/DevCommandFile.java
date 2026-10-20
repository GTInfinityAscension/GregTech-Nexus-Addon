package com.raishxn.gtna.client.debug;

import net.minecraft.client.Minecraft;
import net.minecraft.client.Screenshot;
import net.minecraftforge.event.TickEvent;
import net.minecraftforge.fml.loading.FMLEnvironment;

import com.raishxn.gtna.GTNACORE;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayDeque;
import java.util.Deque;

/**
 * Development aid for driving a test client without the keyboard: every line of {@code gtna_dev_commands.txt} in the
 * game directory runs as a chat command, one per second; {@code close} closes the open screen, {@code inv} opens the
 * inventory, {@code lang <code>} switches the language, {@code mouse <x> <y>} moves the cursor, {@code shot <name>}
 * saves a screenshot, {@code wait <s>} pauses. Only outside production.
 */
public final class DevCommandFile {

    private static final Deque<String> QUEUE = new ArrayDeque<>();
    private static int cooldown;

    private DevCommandFile() {}

    public static void onClientTick(TickEvent.ClientTickEvent event) {
        if (FMLEnvironment.production || event.phase != TickEvent.Phase.END) return;
        var mc = Minecraft.getInstance();
        if (mc.player == null) return;
        if (cooldown > 0) {
            cooldown--;
            return;
        }
        if (QUEUE.isEmpty()) {
            Path file = mc.gameDirectory.toPath().resolve("gtna_dev_commands.txt");
            if (!Files.exists(file)) {
                cooldown = 10;
                return;
            }
            try {
                QUEUE.addAll(Files.readAllLines(file));
                Files.delete(file);
            } catch (Exception e) {
                GTNACORE.LOGGER.warn("[GTNA dev] could not read {}", file, e);
                cooldown = 20;
                return;
            }
        }
        String line = QUEUE.poll();
        if (line == null || line.isBlank()) return;
        line = line.trim();
        GTNACORE.LOGGER.info("[GTNA dev] {}", line);
        cooldown = 20;
        if (line.equals("close")) mc.setScreen(null);
        else if (line.equals("inv"))
            mc.setScreen(new net.minecraft.client.gui.screens.inventory.InventoryScreen(mc.player));
        else if (line.startsWith("wait ")) cooldown = 20 * Integer.parseInt(line.substring(5).trim());
        else if (line.startsWith("lang ")) {
            // Wiki screenshots in every language without restarting the client.
            mc.options.languageCode = line.substring(5).trim();
            mc.getLanguageManager().setSelected(mc.options.languageCode);
            mc.reloadResourcePacks();
            cooldown = 200;
        } else if (line.startsWith("mouse ")) {
            String[] xy = line.substring(6).trim().split(" ");
            org.lwjgl.glfw.GLFW.glfwSetCursorPos(mc.getWindow().getWindow(), Double.parseDouble(xy[0]),
                    Double.parseDouble(xy[1]));
        } else if (line.startsWith("shot ")) Screenshot.grab(mc.gameDirectory, line.substring(5).trim() + ".png",
                mc.getMainRenderTarget(), msg -> {});
        else mc.player.connection.sendCommand(line.startsWith("/") ? line.substring(1) : line);
    }
}
