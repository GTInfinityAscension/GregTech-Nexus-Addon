# 架构

GTNA 是一个 GTCEu 附属模组（`GTNAGTAddon`），模组 id 为 `gtna`，主类为 `com.raishxn.gtna.GTNACORE`。

| 包 | 内容 |
|---|---|
| `api` | 供附属模组使用的公开接口与工具；见 [Java API](api/overview.md) |
| `common.data` | 注册：机器（`GTNAMachines`、`GTNAMachines2`、`GTNAMegaMachines`……）、方块、物品、材料、配方类型、来源（`GTNASources`） |
| `common.machine` | 机器类：`multiblock/steam`、`electric`、`energy`、`noenergy`、`godforge`、`originals`、`part`（仓室、AE2 部件） |
| `data` | 数据生成：语言（`GTNALangProvider`）、配方（`data/recipe`） |
| `config` | `ConfigHolder`（`gtna.yaml`）与 `GTNABalance`（`config/gtna/balance/*.json`） |
| `integration` | AE2、JEI、EMI、Jade、KubeJS、FTB |
| `mixin` | GTCEu 与 AE2 的 mixin（辅助模块、仓室行为、预览） |
| `client`、`network` | 渲染、界面、HUD、网络包 |
| `research` | 研究引擎 |
| `gametest` | GameTest，通过 `runGameTestServer` 运行 |

## 约定

- 移植的机器保留来源的结构、行为和提示；来源在 `GTNASources` 中统一声明，并显示在提示的最后一行。
- 每个可见名称都需要 `en_us`（自动生成）、`pt_br` 和 `zh_cn`。
- 不要在 `integration/jei` 之外引用 JEI 类型，也不要在通用代码中引用 `net.minecraft.client`：仅装 EMI 的客户端和专用服务器都必须能加载模组。测试会检查这两条规则。
- 能量和流体的扣除遵循 模拟 → 扣费 → 执行；余额永远不会为负。
- 组织范围的规则（文件大小、三语关键注释）见[开发约定](https://gtinfinityascension.github.io/GTIA-Dev-Doc/development/conventions/)。
