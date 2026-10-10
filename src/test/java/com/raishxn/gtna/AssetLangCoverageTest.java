package com.raishxn.gtna;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * QA contract for ports: every GTNA recipe type has its {@code gtna.<type>} name in the generated en_us and in the
 * manual pt_br; every {@code block.gtna.<id>} / {@code item.gtna.<id>} the datagen names has a pt_br name and an item
 * model, and every block has a blockstate. A gap shows a raw key or a purple/black cube in game, which the dedicated
 * GameTest server never renders. Dependency-free source/resource scan, {@code main()} + asserts (GTLCore style).
 */
public final class AssetLangCoverageTest {

    private static final Path RECIPE_TYPES = Path.of("src/main/java/com/raishxn/gtna/common/data/GTNARecipeType.java");
    private static final Path GENERATED = Path.of("src/generated/resources/assets/gtna");
    private static final Path MAIN = Path.of("src/main/resources/assets/gtna");
    private static final Pattern RECIPE_TYPE = Pattern.compile("\\bregister\\(\\s*\"([a-z0-9_]+)\"");
    /** GTNA material prefixes and tool types: GTCEu names and models those items at runtime. */
    private static final List<Path> RUNTIME_ITEM_SOURCES = List.of(
            Path.of("src/main/java/com/raishxn/gtna/api/data/tag/GTNATagPrefix.java"),
            Path.of("src/main/java/com/raishxn/gtna/mixin/gtceu/GTNAPlateDoubleMixin.java"),
            Path.of("src/main/java/com/raishxn/gtna/api/item/tool/GTNAToolType.java"));
    private static final Pattern RUNTIME_ID = Pattern
            .compile("(?:idPattern|idFormat|GTToolType\\.builder)\\(\\s*\"([a-z0-9_%]+)\"");
    private static final Pattern NAMED = Pattern.compile("\"(block|item)\\.gtna\\.([a-z0-9_]+)\"\\s*:");

    private AssetLangCoverageTest() {}

    public static void main(String[] args) throws IOException {
        String english = read(GENERATED.resolve("lang/en_us.json"));
        String portuguese = read(MAIN.resolve("lang/pt_br.json"));
        List<String> problems = new ArrayList<>();

        Set<String> types = new LinkedHashSet<>();
        Matcher type = RECIPE_TYPE.matcher(read(RECIPE_TYPES));
        while (type.find()) types.add(type.group(1));
        for (String id : types) {
            String key = "\"gtna." + id + "\"";
            if (!english.contains(key)) problems.add("recipe type " + id + ": no en_us name");
            if (!portuguese.contains(key)) problems.add("recipe type " + id + ": no pt_br name");
        }

        List<Pattern> runtimeItems = new ArrayList<>();
        for (Path source : RUNTIME_ITEM_SOURCES) {
            Matcher id = RUNTIME_ID.matcher(read(source));
            while (id.find()) runtimeItems.add(Pattern.compile(id.group(1).replace("%s", "[a-z0-9_]+")));
        }

        int named = 0;
        Matcher entry = NAMED.matcher(english);
        while (entry.find()) {
            String kind = entry.group(1), id = entry.group(2);
            if (kind.equals("item") && runtimeItems.stream().anyMatch(p -> p.matcher(id).matches())) continue;
            named++;
            if (!portuguese.contains("\"" + kind + ".gtna." + id + "\"")) {
                problems.add(kind + " " + id + ": no pt_br name");
            }
            if (!exists("models/item/" + id + ".json")) problems.add(kind + " " + id + ": no item model");
            if (kind.equals("block") && !exists("blockstates/" + id + ".json")) {
                problems.add("block " + id + ": no blockstate");
            }
        }

        if (types.size() < 30 || named < 300) {
            throw new AssertionError("scan found " + types.size() + " recipe types and " + named +
                    " named blocks/items; the source layout changed or runData was not run");
        }
        if (!problems.isEmpty()) {
            throw new AssertionError(problems.size() + " lang/asset gap(s):\n  " + String.join("\n  ", problems));
        }
        System.out.println("[AssetLangCoverageTest] " + types.size() + " recipe types and " + named +
                " blocks/items have en+pt names and models");
    }

    private static boolean exists(String path) {
        return Files.exists(GENERATED.resolve(path)) || Files.exists(MAIN.resolve(path));
    }

    private static String read(Path path) throws IOException {
        return Files.readString(path, StandardCharsets.UTF_8);
    }
}
