# 翻译

欢迎为模组和本 wiki 提供翻译。GTNA 目前提供英语、葡萄牙语（巴西）和简体中文。新语言可以从少量内容开始，逐页增加：尚未翻译的内容会显示英文。

在开始大量翻译之前，请先提交 [issue](https://github.com/GTInfinityAscension/GregTech-Nexus-Addon/issues) 或在 [Discord](https://discord.gg/TW5vugknk5) 打个招呼，避免两个人翻译同一部分。

## 模组

游戏中的每个名称和提示都来自每种语言一个的 JSON 文件：

```
src/main/resources/assets/gtna/lang/<locale>.json      例如 ru_ru.json、de_de.json、ja_jp.json
```

1. Fork 仓库，并用 Minecraft 的语言代码（`ru_ru`、`es_es`、`fr_fr`……）创建你的语言文件。
2. 从英文源文件复制键并翻译值。完整的英文文件由 `./gradlew runData` 生成到 `src/generated/resources/assets/gtna/lang/en_us.json`；与你的文件同目录下的 `pt_br.json` 和 `zh_cn.json` 可作参考。
3. `§` 颜色代码和 `%s` 占位符必须原样保留。
4. 查看还缺少哪些内容：

    ```bash
    python3 tools/check_lang_parity.py --locale ru_ru
    ```

5. 提交 pull request。不完整的文件也可以；缺少的键会显示英文。

## 本 wiki

本 wiki 使用 [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) 和 [mkdocs-static-i18n](https://ultrabug.github.io/mkdocs-static-i18n/) 构建。每个页面是 `docs/` 下的一个 Markdown 文件；译文是带语言后缀的同名文件：

```
docs/gameplay/systems/bec.md       English（源文件）
docs/gameplay/systems/bec.pt.md    Português
docs/gameplay/systems/bec.zh.md    简体中文
docs/gameplay/systems/bec.ru.md    你的翻译
```

### 小修改

每页顶部都有**编辑**按钮（铅笔图标）。它会在 GitHub 上打开对应文件，无需安装任何东西即可提交修改。

### 新增语言

1. 在 `mkdocs.yml` 的 `plugins → i18n → languages` 中，于 `pt` 和 `zh` 旁边添加语言：

    ```yaml
    - locale: ru
      name: Русский
      build: true
      nav_translations:
        Home: Главная
        Machines: Машины
    ```

2. 在英文文件旁创建 `<页面>.ru.md` 来翻译页面。建议从 `index`、`getting-started/` 和你最常用的页面开始。链接和图片路径保持不变：它们在所有语言中指向同一文件。
3. 部分页面是**自动生成**的，请不要手动编辑：

    | 页面 | 生成器 | 文本来源 |
    |---|---|---|
    | `gameplay/machines/catalog/*` | `tools/wiki/generate_machine_pages.py` | 模组的语言文件，因此请先翻译模组 |
    | `gameplay/materials/index*` | `tools/wiki/material_pages.py` | 模组的语言文件以及脚本中的介绍文字 |
    | `gameplay/systems/forge-of-gods*`、`eye-of-harmony*` | `tools/wiki/system_pages.py` | 脚本中的文本字典 |
    | `roadmap/index*` | `tools/wiki/roadmap_page.py` | 脚本中的文本字典 |

    要为生成器添加语言，请在其语言列表和文本字典中添加条目，然后运行脚本。

4. 本地预览：

    ```bash
    pip install mkdocs-material mkdocs-static-i18n
    mkdocs serve
    ```

    打开 <http://127.0.0.1:8000/ru/>。提交 pull request 前，`mkdocs build --strict` 必须无警告完成。

### 风格

- 像玩家说话一样书写；短句胜过长句。
- 使用游戏在你的语言中显示的物品和机器名称。如果模组还没有某个名称的翻译，保留英文名。
- 数字、公式、配置键和 id 必须与英文页面完全一致。
