package com.raishxn.gtna.client.debug;

import com.gregtechceu.gtceu.api.data.chemical.ChemicalHelper;

import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraftforge.registries.ForgeRegistries;

import com.raishxn.gtna.GTNACORE;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;

/**
 * Development aid ({@code /gtna_material_sheet [page]}): every GTNA material item drawn at 2x, one material per row,
 * so item effects can be checked for all materials and forms in a few screenshots.
 */
public final class MaterialSheetScreen extends Screen {

    private static final int PER_PAGE = 14, COLUMNS = 26;
    private final int page;
    private final List<Map.Entry<String, List<Item>>> rows;

    public MaterialSheetScreen(int page) {
        super(Component.literal("GTNA material sheet"));
        this.page = page;
        Map<String, List<Item>> byMaterial = new TreeMap<>();
        for (var item : ForgeRegistries.ITEMS) {
            var id = ForgeRegistries.ITEMS.getKey(item);
            if (id == null || !id.getNamespace().equals(GTNACORE.MOD_ID)) continue;
            var entry = ChemicalHelper.getMaterialEntry(item);
            if (entry.isEmpty() || entry.material() == null) continue;
            var set = entry.material().getMaterialIconSet().name;
            if (!set.startsWith("gtna_")) continue;
            byMaterial.computeIfAbsent(entry.material().getName(), k -> new ArrayList<>()).add(item);
        }
        rows = new ArrayList<>(byMaterial.entrySet());
    }

    public static int pages() {
        return (new MaterialSheetScreen(0).rows.size() + PER_PAGE - 1) / PER_PAGE;
    }

    @Override
    public void render(GuiGraphics g, int mouseX, int mouseY, float partialTick) {
        g.fill(0, 0, width, height, 0xFF202028);
        int y = 4;
        int end = Math.min(rows.size(), (page + 1) * PER_PAGE);
        g.drawString(font, "page " + page + " / " + (pages() - 1), width - 70, 2, 0xFFFFFF);
        for (int i = page * PER_PAGE; i < end; i++) {
            var row = rows.get(i);
            g.drawString(font, row.getKey(), 2, y + 10, 0xFFFFFF);
            int x = 90;
            for (int k = 0; k < Math.min(COLUMNS, row.getValue().size()); k++) {
                g.pose().pushPose();
                g.pose().translate(x, y, 0);
                g.pose().scale(1.6f, 1.6f, 1);
                g.renderItem(new ItemStack(row.getValue().get(k)), 0, 0);
                g.pose().popPose();
                x += 28;
            }
            y += 30;
        }
    }

    @Override
    public boolean isPauseScreen() {
        return false;
    }
}
