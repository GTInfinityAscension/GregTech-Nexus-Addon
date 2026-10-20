# 开发环境

## 需求

- JDK 17
- Git
- 支持 Gradle 的 IDE；推荐 IntelliJ IDEA 配合 Minecraft Development 插件。代码使用 Lombok。

## 构建与运行

```bash
git clone https://github.com/GTInfinityAscension/GregTech-Nexus-Addon.git
cd GregTech-Nexus-Addon
./gradlew build          # 编译并打包
./gradlew runClient      # 启动开发客户端
./gradlew runData        # 重新生成语言文件、模型和配方
```

提交 pull request 前，请运行与维护者相同的检查：

```bash
./gradlew spotlessCheck compileJava runUnitTests runGameTestServer runData
```

- `./gradlew spotlessApply` 会修正代码格式。
- 首次运行 GameTest 之前，创建内容为 `eula=true` 的 `run/eula.txt`。
- 即使有配方解析失败，`runGameTestServer` 也可能以 0 退出：请在日志中搜索 `Parsing error loading recipe gtna:`。

## Wiki

```bash
pip install mkdocs-material mkdocs-static-i18n
mkdocs serve
```

图鉴需要数据生成的导出文件：先运行 `./gradlew runData`，再运行 `python3 tools/wiki/generate_machine_pages.py`（加 `--no-render` 可保留现有图片）。其他生成器见[翻译](translating.md)。
