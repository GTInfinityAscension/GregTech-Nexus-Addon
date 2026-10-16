package com.raishxn.gtna;

import com.raishxn.gtna.api.machine.feature.lance.LanceCore;

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
 * QA contract: the originals' UI and JEI keys exist in en_us, pt_br and zh_cn. Covers the keys the screens build
 * from enums at runtime ({@code gtna.ui.o.slug.<projectile>}, {@code gtna.ui.o.part.<component>}), which no
 * literal scan sees: a missing {@code gtna.ui.o.slug.magnetar} showed as a raw key in the lance screen (G-0272).
 * Dependency-free, {@code main()} + asserts (GTLCore style).
 */
public final class OriginalsLangKeysTest {

    private static final Path EN = Path.of("src/generated/resources/assets/gtna/lang/en_us.json");
    private static final Path PT = Path.of("src/main/resources/assets/gtna/lang/pt_br.json");
    private static final Path ZH = Path.of("src/main/resources/assets/gtna/lang/zh_cn.json");
    private static final Pattern PREFIXED = Pattern
            .compile("\"((?:gtna\\.ui\\.o\\.|gtna\\.originals\\.|gtna\\.machine\\.structure_check)[^\"]*)\"\\s*:");

    private OriginalsLangKeysTest() {}

    public static void main(String[] args) throws IOException {
        String en = Files.readString(EN, StandardCharsets.UTF_8);
        String pt = Files.readString(PT, StandardCharsets.UTF_8);
        String zh = Files.readString(ZH, StandardCharsets.UTF_8);

        Set<String> keys = new LinkedHashSet<>();
        Matcher m = PREFIXED.matcher(en);
        while (m.find()) keys.add(m.group(1));
        for (var p : LanceCore.Projectile.values()) keys.add("gtna.ui.o.slug." + p.name().toLowerCase());
        for (var c : LanceCore.Component.values()) {
            keys.add("gtna.ui.o.part." + c.name().toLowerCase());
            keys.add("gtna.ui.o.part." + c.name().toLowerCase() + ".tip");
        }

        List<String> problems = new ArrayList<>();
        for (String key : keys) {
            String quoted = '"' + key + '"';
            if (!en.contains(quoted)) problems.add(key + ": no en_us");
            if (!pt.contains(quoted)) problems.add(key + ": no pt_br");
            if (!zh.contains(quoted)) problems.add(key + ": no zh_cn");
        }
        if (keys.size() < 300) throw new AssertionError("only " + keys.size() + " originals keys; run runData");
        if (!problems.isEmpty()) {
            throw new AssertionError(problems.size() + " originals lang gap(s):\n  " + String.join("\n  ", problems));
        }
        System.out.println("[OriginalsLangKeysTest] " + keys.size() + " keys in en_us, pt_br and zh_cn");
    }
}
