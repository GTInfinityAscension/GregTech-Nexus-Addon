# 安装

## 需求

| 模组 | 版本 | |
|---|---|---|
| Minecraft | 1.20.1 | 必需 |
| Forge | 47.4.1 或更高 | 必需 |
| [GregTech CEu Modern](https://www.curseforge.com/minecraft/mc-mods/gregtechceu-modern) | 7.5.3 或更高 | 必需；版本过旧时 Forge 会停止加载并提示 |
| [GTIA Lib](https://github.com/GTInfinityAscension/GTIA-Lib) | 0.5.0 或更高 | 自 GTNA 0.6.1 起必需 |
| [Applied Energistics 2](https://www.curseforge.com/minecraft/mc-mods/applied-energistics-2) | 1.20.1 版本（已用 15.4.10 测试） | 必需：ME 部件始终会注册 |
| JEI 或 EMI | 任意较新版本 | 可选，强烈推荐：查看配方和结构预览 |
| KubeJS | 2001.6.5 | 可选：[脚本 API](../development/api/kubejs.md) |
| Ad Astra | 1.15.20 或更高 | 可选：蒸汽电梯、鸿蒙之眼和星球虚空采矿程序所需的星球 |
| FTB Teams / FTB Quests | — | 可选：研究和流体发现的队伍进度、研究任务类型 |
| Productive Bees | — | 可选：蒸汽电梯育蜂模块 |
| Jade | — | 可选：显示无线蒸汽仓详情 |

GTCEu 有自己的前置模组（例如 LDLib）；请安装其下载页面要求的版本。自 GTNA 0.5.6 起**不再需要** RenderBlender。

## 步骤

1. 为 Minecraft 1.20.1 安装 Forge 47.4.1 或更高版本。
2. 把 GTCEu、GTIA Lib、Applied Energistics 2 和 GTNA 放入 `mods` 文件夹。
3. 添加需要的可选模组。
4. 启动一次游戏。GTNA 会生成 `config/gtna.yaml` 以及 `config/gtna/balance/` 中的平衡文件（见[配置](configuration.md)）。

下载：[GitHub Releases](https://github.com/GTInfinityAscension/GregTech-Nexus-Addon/releases)。开发者也可以从[组织的 Maven 仓库](https://gtinfinityascension.github.io/maven/)获取正式版本的 jar。

## 服务器

GTNA 可在专用服务器上运行。服务器和每个客户端需要安装相同的模组；仅客户端选项（HUD、物品特效）保存在各玩家自己的 `config/gtna.yaml` 中。
