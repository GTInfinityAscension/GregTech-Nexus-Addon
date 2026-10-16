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

import javax.imageio.ImageIO;

/**
 * QA contract for GTNA's custom material sets ({@code gtna_*}): the asset mistakes that only showed in a client.
 * <ul>
 * <li>a block model with {@code children} but no {@code forge:composite} loader renders invisible (the SpaceTime
 * block and frame, G-0272);</li>
 * <li>every {@code gtna_*} or {@code gtna:} texture a model names exists;</li>
 * <li>a texture strip taller than wide has its {@code .mcmeta}, or the game shows the whole strip squashed.</li>
 * </ul>
 * Dependency-free resource scan, {@code main()} + asserts (GTLCore style).
 */
public final class MaterialSetAssetContractTest {

    private static final Path RES = Path.of("src/main/resources/assets");
    private static final Pattern TEXTURE = Pattern.compile("\"((?:gtceu|gtna):(?:item|block)/[a-z0-9_/]+)\"");

    private MaterialSetAssetContractTest() {}

    public static void main(String[] args) throws IOException {
        List<String> problems = new ArrayList<>();
        int models = 0, textures = 0;
        for (String kind : List.of("block", "item")) {
            Path root = RES.resolve("gtceu/models/" + kind + "/material_sets");
            List<Path> files;
            try (Stream<Path> walk = Files.walk(root)) {
                files = walk.filter(p -> p.toString().endsWith(".json") &&
                        p.getParent().getFileName().toString().startsWith("gtna_")).toList();
            }
            for (Path file : files) {
                models++;
                String json = Files.readString(file, StandardCharsets.UTF_8);
                String name = RES.relativize(file).toString();
                if (json.contains("\"children\"") && !json.contains("\"forge:composite\"")) {
                    problems.add(name + ": children without the forge:composite loader (renders invisible)");
                }
                Matcher m = TEXTURE.matcher(json);
                while (m.find()) {
                    String ref = m.group(1);
                    if (!ref.contains("material_sets/gtna_") && !ref.startsWith("gtna:")) continue;
                    String[] parts = ref.split(":", 2);
                    Path png = RES.resolve(parts[0] + "/textures/" + parts[1] + ".png");
                    textures++;
                    if (!Files.exists(png)) {
                        problems.add(name + ": missing texture " + ref);
                        continue;
                    }
                    var image = ImageIO.read(png.toFile());
                    if (image != null && image.getHeight() > image.getWidth() &&
                            !Files.exists(Path.of(png + ".mcmeta"))) {
                        problems.add(
                                ref + ": " + image.getWidth() + "x" + image.getHeight() + " strip without .mcmeta");
                    }
                }
            }
        }
        if (models < 200) throw new AssertionError("only " + models + " gtna_* material set models found");
        if (!problems.isEmpty()) {
            throw new AssertionError(problems.size() + " material set asset problem(s):\n  " +
                    String.join("\n  ", problems));
        }
        System.out.println("[MaterialSetAssetContractTest] " + models + " models, " + textures +
                " texture references OK");
    }
}
