# Ambiente de desenvolvimento

## Requisitos

- JDK 17
- Git
- Uma IDE com suporte a Gradle; o IntelliJ IDEA com o plugin Minecraft Development funciona bem. O código usa Lombok.

## Compilar e rodar

```bash
git clone https://github.com/GTInfinityAscension/GregTech-Nexus-Addon.git
cd GregTech-Nexus-Addon
./gradlew build          # compila e empacota
./gradlew runClient      # abre um cliente de desenvolvimento
./gradlew runData        # regenera arquivos de idioma, modelos e receitas
```

Antes de um pull request, rode as mesmas verificações dos mantenedores:

```bash
./gradlew spotlessCheck compileJava runUnitTests runGameTestServer runData
```

- `./gradlew spotlessApply` corrige a formatação.
- Crie `run/eula.txt` com `eula=true` antes da primeira execução dos GameTests.
- O `runGameTestServer` pode sair com 0 mesmo quando uma receita falha ao carregar: procure no log por `Parsing error loading recipe gtna:`.

## Wiki

```bash
pip install mkdocs-material mkdocs-static-i18n
mkdocs serve
```

O catálogo precisa do dump do datagen: rode `./gradlew runData` e depois `python3 tools/wiki/generate_machine_pages.py` (com `--no-render` para manter as imagens existentes). Veja [Traduzir](translating.md) para os outros geradores.
