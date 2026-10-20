# 常见问题

??? question "游戏提示缺少前置模组并停止加载"
    GTNA 0.6.1 需要 **GTCEu 7.5.3 或更高**以及 **GTIA Lib 0.5.0 或更高**。旧版 GTCEu 会导致 `NoSuchFieldError: CLUSTER_MAX_HARVESTABLES` 等崩溃（issue #1）。请同时更新这两个模组。见[安装](installation.md)。

??? question "GTNA 材料图标显示为缺失纹理"
    GTNA 0.5.4 和 0.5.5 的这些模型依赖 RenderBlender。请更新到 0.5.6 或更高版本，新版本会自行绘制特效。

??? question "可以关闭物品特效（光环、着色器）吗？"
    可以，在 `config/gtna.yaml` 的 `client` 部分：`itemHalo`、`itemGlowEdge`、`itemShaderEffects` 和 `itemEffectSpeed`。见[物品特效](../gameplay/systems/item-effects.md)。

??? question "结构无法成型"
    在 JEI/EMI 中打开结构逐层对照；把鼠标悬停在每个位置上查看可放置的方块。检查机器要求同等级的地方外壳等级是否一致（高压模式的蒸汽机器需要**全部**外壳为钢制）。[Nexus结构终端](../gameplay/systems/modules.md#nexus-structure-terminal)可以替你建造。

??? question "无线蒸汽输出仓装在锅炉上没有反应"
    它只能装在大型蒸汽太阳能锅炉上，并且不接受管道输入的蒸汽。见[无线蒸汽网络](../gameplay/systems/wireless-steam-network.md)。

??? question "样板总成中的某个样板一直不运行"
    用鼠标中键点击该槽位：最常见的原因是缺少编程电路或首选模式错误。见 [ME 样板总成](../gameplay/systems/pattern-buffers.md)。

??? question "配方和 GTNH 或 GTO 不一样"
    GTNA 自带可用的默认配方。平衡由整合包决定，整合包可以通过 KubeJS、数据包以及 `config/gtna/balance/` 中的平衡文件修改一切。

??? question "需要 Ad Astra 吗？"
    不需要。没有它时蒸汽电梯无法出行，鸿蒙之眼只有 Minecraft 原版维度，星球虚空采矿程序也不会出现。

??? question "在哪里报告 bug？"
    在 [issue 追踪](https://github.com/GTInfinityAscension/GregTech-Nexus-Addon/issues)中提交，附上 `latest.log`（如果崩溃，还有 `crash-reports/`）以及 GTNA、GTCEu 和 GTIA Lib 的版本。

??? question "我可以翻译 wiki 或模组吗？"
    可以，见[翻译](../development/translating.md)。
