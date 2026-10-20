# Development setup

## Requirements

- JDK 17
- Git
- An IDE with Gradle support; IntelliJ IDEA with the Minecraft Development plugin works well. The code uses Lombok.

## Build and run

```bash
git clone https://github.com/GTInfinityAscension/GregTech-Nexus-Addon.git
cd GregTech-Nexus-Addon
./gradlew build          # compile and package
./gradlew runClient      # start a development client
./gradlew runData        # regenerate lang files, models and recipes
```

Before a pull request, run the same checks as the maintainers:

```bash
./gradlew spotlessCheck compileJava runUnitTests runGameTestServer runData
```

- `./gradlew spotlessApply` fixes the formatting.
- Create `run/eula.txt` with `eula=true` before the first GameTest run.
- `runGameTestServer` can exit with 0 even when a recipe fails to parse: search the log for `Parsing error loading recipe gtna:`.

## Wiki

```bash
pip install mkdocs-material mkdocs-static-i18n
mkdocs serve
```

The catalog needs the datagen dump: run `./gradlew runData`, then `python3 tools/wiki/generate_machine_pages.py` (add `--no-render` to keep the existing images). See [Translating](translating.md) for the other generators.
