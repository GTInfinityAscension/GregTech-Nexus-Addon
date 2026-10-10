package com.raishxn.gtna;

import com.raishxn.gtna.common.data.GTNAMultiblockTooltipText;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeSet;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Stream;

/**
 * Contract of the standard multiblock tooltip ({@code tools/apply_multiblock_tooltips.py}): every multiblock id
 * registered in the sources has an entry; each entry starts with Machine Type and a flavor line, has a description
 * between two separators and at least one bullet line; pt_br has the same lines with contiguous
 * {@code gtna.machine.<id>.tooltip.N} keys (no gaps, no leftovers) and no old auto-inserted
 * {@code gtna.machine.<id>.tooltip} description. GTLCore style: {@code main()} + asserts.
 */
public final class MultiblockTooltipStandardTest {

    private static final Path SOURCES = Path.of("src/main/java");
    private static final Path PT_BR = Path.of("src/main/resources/assets/gtna/lang/pt_br.json");
    private static final Pattern MULTIBLOCK = Pattern
            .compile("(?:\\.multiblock|registerElevatorModule)\\(\\s*\"([a-z0-9_]+)\"");
    private static final Pattern PT_KEY = Pattern
            .compile("\"gtna\\.machine\\.([a-z0-9_]+)\\.tooltip(?:\\.(\\d+))?\"\\s*:\\s*\"((?:[^\"\\\\]|\\\\.)*)\"");
    /** Visible characters per line (color codes excluded); separators are exempt. */
    private static final int MAX_LINE = 72;

    private MultiblockTooltipStandardTest() {}

    private static String visible(String line) {
        return line.replaceAll("§.", "");
    }

    public static void main(String[] args) throws IOException {
        Map<String, String[]> english = GTNAMultiblockTooltipText.ENGLISH;
        List<String> errors = new ArrayList<>();

        Set<String> registered = new TreeSet<>();
        try (Stream<Path> files = Files.walk(SOURCES)) {
            for (Path file : files.filter(f -> f.toString().endsWith(".java")).toList()) {
                Matcher matcher = MULTIBLOCK.matcher(Files.readString(file, StandardCharsets.UTF_8));
                while (matcher.find()) registered.add(matcher.group(1));
            }
        }
        for (String id : registered) {
            if (!english.containsKey(id)) errors.add(id + ": registered multiblock without a standard tooltip");
        }

        for (var entry : english.entrySet()) {
            String id = entry.getKey();
            String[] lines = entry.getValue();
            if (lines.length < 6 || !lines[0].startsWith("Machine Type: §e")) errors.add(id + ": no Machine Type");
            if (lines.length < 2 || !lines[1].startsWith("§7§o")) errors.add(id + ": no flavor line");
            long separators = Stream.of(lines).filter(line -> line.startsWith("§b§m")).count();
            if (separators != 2) errors.add(id + ": expected 2 separators, found " + separators);
            if (lines.length > 3 && lines[3].startsWith("§b§m")) errors.add(id + ": empty description");
            if (Stream.of(lines).noneMatch(line -> line.contains("▸ "))) errors.add(id + ": no bullet line");
            for (String line : lines) {
                if (!line.startsWith("§b§m") && visible(line).length() > MAX_LINE) {
                    errors.add(id + ": en line longer than " + MAX_LINE + ": " + visible(line));
                }
            }
        }

        String portuguese = Files.readString(PT_BR, StandardCharsets.UTF_8);
        Map<String, Set<Integer>> ptIndexes = new java.util.HashMap<>();
        Matcher matcher = PT_KEY.matcher(portuguese);
        while (matcher.find()) {
            String id = matcher.group(1);
            if (!english.containsKey(id)) continue;
            if (matcher.group(2) == null) {
                errors.add(id + ": pt_br still has the old auto-inserted description key");
                continue;
            }
            ptIndexes.computeIfAbsent(id, k -> new TreeSet<>()).add(Integer.parseInt(matcher.group(2)));
            String value = matcher.group(3);
            if (!value.startsWith("§b§m") && visible(value).length() > MAX_LINE) {
                errors.add(id + ": pt_br line longer than " + MAX_LINE + ": " + visible(value));
            }
        }
        for (var entry : english.entrySet()) {
            Set<Integer> indexes = ptIndexes.getOrDefault(entry.getKey(), Set.of());
            Set<Integer> expected = new TreeSet<>();
            for (int i = 0; i < entry.getValue().length; i++) expected.add(i);
            if (!indexes.equals(expected)) {
                errors.add(entry.getKey() + ": pt_br tooltip keys " + indexes + " != " + expected);
            }
        }

        if (registered.size() < 100) errors.add("found only " + registered.size() + " registered multiblocks");
        if (!errors.isEmpty()) {
            throw new AssertionError(errors.size() + " multiblock tooltip problem(s):\n" + String.join("\n", errors));
        }
        System.out.println("[MultiblockTooltipStandardTest] " + english.size() + " standard multiblock tooltips OK");
    }
}
