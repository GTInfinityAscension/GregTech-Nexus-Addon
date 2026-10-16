package com.raishxn.gtna;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.stream.Stream;

/**
 * GTNA must load in packs without JEI (EMI only). A JEI type named in a class that loads on every client makes the
 * JVM fail the whole mod at construction (GTNA 0.6.0 did this through a debug command). Only the classes below may
 * name {@code mezz.jei}: they load only when JEI is present.
 */
public final class JeiIsolationContractTest {

    private static final List<String> ALLOWED = List.of(
            "com/raishxn/gtna/integration/jei/",
            "com/raishxn/gtna/mixin/",
            "com/raishxn/gtna/client/debug/JeiPreviewOpen.java");

    private JeiIsolationContractTest() {}

    public static void main(String[] args) throws IOException {
        Path root = Path.of("src/main/java");
        if (!Files.isDirectory(root)) throw new AssertionError("run from the project root: " + root.toAbsolutePath());
        try (Stream<Path> files = Files.walk(root)) {
            List<String> offenders = files.filter(p -> p.toString().endsWith(".java"))
                    .filter(p -> {
                        String rel = root.relativize(p).toString().replace('\\', '/');
                        return ALLOWED.stream().noneMatch(rel::startsWith);
                    })
                    .filter(p -> {
                        try {
                            return Files.readString(p).contains("mezz.jei");
                        } catch (IOException e) {
                            throw new RuntimeException(e);
                        }
                    })
                    .map(p -> root.relativize(p).toString())
                    .toList();
            if (!offenders.isEmpty()) {
                throw new AssertionError("JEI types outside JEI-only classes (crash without JEI): " + offenders);
            }
        }
        System.out.println("[JeiIsolationContractTest] no JEI types outside JEI-only classes");
    }
}
