package com.raishxn.gtna;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Stream;

/**
 * Every ldlib CTM {@code connection} in a GTNA texture {@code .mcmeta} must point to a {@code gtna:} texture that
 * exists. Textures ported from GTOCore kept {@code gtocore:} connections without the {@code _ctm} sheet, so the casings
 * rendered with broken connected textures (G-0214); see {@code tools/fix_gto_ctm.py}.
 */
public final class CtmConnectionContractTest {

    private static final Path TEXTURES = Path.of("src/main/resources/assets/gtna/textures");
    private static final Pattern CONNECTION = Pattern.compile("\"connection\"\\s*:\\s*\"([^\"]+)\"");

    private CtmConnectionContractTest() {}

    public static void main(String[] args) throws IOException {
        List<String> broken = new ArrayList<>();
        int checked = 0;
        try (Stream<Path> files = Files.walk(TEXTURES)) {
            for (Path file : files.filter(p -> p.toString().endsWith(".mcmeta")).toList()) {
                String json = Files.readString(file, StandardCharsets.UTF_8);
                int ldlib = json.indexOf("\"ldlib\"");
                if (ldlib < 0) continue; // e.g. GTNH "myctmlib" metadata, which ldlib ignores
                Matcher matcher = CONNECTION.matcher(json.substring(ldlib));
                if (!matcher.find()) continue;
                checked++;
                String[] parts = matcher.group(1).split(":", 2);
                Path target = Path.of("src/main/resources/assets", parts[0], "textures", parts[1] + ".png");
                if (!"gtna".equals(parts[0]) || !Files.exists(target)) {
                    broken.add(TEXTURES.relativize(file) + " -> " + matcher.group(1));
                }
            }
        }
        if (!broken.isEmpty()) {
            throw new AssertionError(broken.size() + " broken CTM connection(s): " + broken);
        }
        if (checked < 50) throw new AssertionError("expected at least 50 CTM textures, found " + checked);
        System.out.println("[CtmConnectionContractTest] " + checked + " CTM connections resolve to gtna textures");
    }
}
