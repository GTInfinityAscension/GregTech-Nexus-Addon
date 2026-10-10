package com.raishxn.gtna;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * GTCEu keeps material icon sets in one global map by name, and a second registration of the same name crashes the
 * game ("MaterialIconSet infinity already registered!", reported with GTNN). Every GTNA icon set must be prefixed
 * {@code gtna_} (G-0215).
 */
public final class IconSetNamespaceTest {

    private static final Path SOURCE = Path.of(
            "src/main/java/com/raishxn/gtna/common/data/material/GodforgeIconSets.java");
    private static final Pattern ICON_SET = Pattern.compile("new MaterialIconSet\\(\\s*\"([^\"]+)\"");

    private IconSetNamespaceTest() {}

    public static void main(String[] args) throws IOException {
        Matcher matcher = ICON_SET.matcher(Files.readString(SOURCE, StandardCharsets.UTF_8));
        List<String> bad = new ArrayList<>();
        int checked = 0;
        while (matcher.find()) {
            checked++;
            String name = matcher.group(1);
            if (!name.startsWith("gtna_")) bad.add(name);
            Path textures = Path.of("src/main/resources/assets/gtceu/textures/item/material_sets", name);
            if (!Files.isDirectory(textures)) bad.add(name + " (no textures at " + textures + ")");
        }
        if (!bad.isEmpty()) throw new AssertionError("icon sets must be gtna_-prefixed with textures: " + bad);
        if (checked < 20) throw new AssertionError("expected the GTNA icon sets, found " + checked);
        System.out.println("[IconSetNamespaceTest] " + checked + " icon sets are gtna_-prefixed");
    }
}
