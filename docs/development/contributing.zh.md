# 贡献代码

组织通用指南见 GTInfinityAscension 的 [CONTRIBUTING](https://github.com/GTInfinityAscension/.github/blob/main/CONTRIBUTING.md)。GTNA 的简要版本：

1. 除修复 bug 以外的改动，请先提交 issue。平衡和进度方面的修改需要作者批准。
2. Fork 仓库，从 `main` 创建分支，每个 pull request 只做一件事。
3. 每个新机器、物品或配方都需要 **en_us、pt_br 和 zh_cn** 的名称。
4. 添加或更新 GameTest。新的多方块需要一个成型测试和一个反向测试（在不应成型或运行时确实不会）。
5. 运行 `./gradlew spotlessCheck compileJava runUnitTests runGameTestServer runData`，并在 pull request 中说明你在游戏中如何测试。
6. 提交信息和更新日志使用英文。
7. 移植内容保留来源署名：把机器加入 `GTNASources`，并遵循 `THIRD_PARTY_NOTICES.md` 中的许可说明。
