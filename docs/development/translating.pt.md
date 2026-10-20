# Traduzir

Traduções são bem-vindas, para o mod e para esta wiki. Hoje o GTNA tem inglês, português (Brasil) e chinês simplificado. Um idioma novo pode começar pequeno e crescer página por página: o que ainda não foi traduzido aparece em inglês.

Antes de uma tradução grande, abra uma [issue](https://github.com/GTInfinityAscension/GregTech-Nexus-Addon/issues) ou avise no [Discord](https://discord.gg/TW5vugknk5), para duas pessoas não traduzirem a mesma coisa.

## O mod

Todo nome e tooltip do jogo vem de um arquivo JSON por idioma:

```
src/main/resources/assets/gtna/lang/<locale>.json      ex.: ru_ru.json, de_de.json, ja_jp.json
```

1. Faça um fork do repositório e crie o arquivo do seu idioma, com o código de locale do Minecraft (`ru_ru`, `es_es`, `fr_fr`…).
2. Copie as chaves da fonte em inglês e traduza os valores. O arquivo inglês completo é gerado por `./gradlew runData` em `src/generated/resources/assets/gtna/lang/en_us.json`; o `pt_br.json` e o `zh_cn.json`, na mesma pasta do seu, servem de referência.
3. Mantenha os códigos de cor `§` e os marcadores `%s` exatamente como estão.
4. Veja o que ainda falta:

    ```bash
    python3 tools/check_lang_parity.py --locale ru_ru
    ```

5. Abra um pull request. Arquivos parciais servem; as chaves que faltarem aparecem em inglês.

## Esta wiki

A wiki é feita com [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) e [mkdocs-static-i18n](https://ultrabug.github.io/mkdocs-static-i18n/). Cada página é um arquivo Markdown em `docs/`; a tradução é o mesmo arquivo com um sufixo de idioma:

```
docs/gameplay/systems/bec.md       English (a fonte)
docs/gameplay/systems/bec.pt.md    Português
docs/gameplay/systems/bec.zh.md    简体中文
docs/gameplay/systems/bec.ru.md    a sua tradução
```

### Correções pequenas

Toda página tem um botão de **editar** (o lápis no topo). Ele abre o arquivo no GitHub, onde dá para propor a mudança sem instalar nada.

### Um idioma novo

1. Acrescente o idioma no `mkdocs.yml`, em `plugins → i18n → languages`, junto de `pt` e `zh`:

    ```yaml
    - locale: ru
      name: Русский
      build: true
      nav_translations:
        Home: Главная
        Machines: Машины
    ```

2. Traduza as páginas criando `<página>.ru.md` ao lado do arquivo em inglês. Comece por `index`, `getting-started/` e as páginas que você mais usa. Deixe links e caminhos de imagem como estão: eles apontam para os mesmos arquivos em todos os idiomas.
3. Algumas páginas são **geradas**, então não edite à mão:

    | Páginas | Gerador | De onde vem o texto |
    |---|---|---|
    | `gameplay/machines/catalog/*` | `tools/wiki/generate_machine_pages.py` | dos arquivos de idioma do mod, então traduza o mod primeiro |
    | `gameplay/materials/index*` | `tools/wiki/material_pages.py` | dos arquivos de idioma do mod e da introdução dentro do script |
    | `gameplay/systems/forge-of-gods*`, `eye-of-harmony*` | `tools/wiki/system_pages.py` | dos dicionários de texto dentro do script |
    | `roadmap/index*` | `tools/wiki/roadmap_page.py` | dos dicionários de texto dentro do script |

    Para pôr um idioma num gerador, acrescente uma entrada na lista de idiomas e no dicionário de textos dele e rode o script.

4. Veja o resultado localmente:

    ```bash
    pip install mkdocs-material mkdocs-static-i18n
    mkdocs serve
    ```

    Abra <http://127.0.0.1:8000/ru/>. O `mkdocs build --strict` precisa terminar sem avisos antes do pull request.

### Estilo

- Escreva como um jogador fala; frases curtas são melhores que longas.
- Use os nomes de itens e máquinas que o jogo mostra no seu idioma. Se o mod ainda não tem tradução para um nome, mantenha o nome em inglês.
- Números, fórmulas, chaves de config e ids ficam exatamente como na página em inglês.
