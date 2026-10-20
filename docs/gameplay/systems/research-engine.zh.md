# 研究引擎

一个由数据驱动、可供其他系统读取的研究树。整合包用 JSON 描述**节点**；队伍通过获得某个物品来**解锁**节点；节点随后可以**限制机器配方**，或开启供其他代码读取的**标记**。GTNA 只提供引擎本身，节点由整合包提供。

## 玩家

- 按 **K**（可改键）打开研究树。节点按等级分组，连线指向其前置节点。绿色为已解锁，黄色为下一个可解锁的节点，灰色为未解锁。鼠标悬停在节点上可查看它需要什么、解锁什么。
- 前置条件满足且你持有节点要求的物品时（合成、拾取或机器产出都算），节点会自动解锁。队伍中任意一人持有即可。
- 受限配方在 EMI 中显示红色的 **研究：<节点>** 行（解锁后变为绿色），无法运行该配方的机器会提示*需要研究：<节点>*。

进度属于玩家所在的 **FTB 队伍**，没有队伍时属于玩家本人，与流体发现记录的规则相同。

没有研究节点的整合包可以在 `config/gtna.yaml` 中设置 `gameplay.researchTree: false` 关闭整个研究树。

## 整合包作者

每个节点一个 JSON 文件，放在 `data/<命名空间>/gtna_research/` 下。节点 id 即文件路径：`data/gtia/gtna_research/lv/aluminium.json` 对应 `gtia:lv/aluminium`。

```json
{
  "tier": 2,
  "icon": "gtceu:aluminium_ingot",
  "prerequisites": ["gtia:lv/blast_furnace"],
  "trigger": { "type": "obtain_item", "item": "gtceu:aluminium_dust" },
  "grants": [
    { "type": "recipe_condition", "recipes": ["gtceu:electric_blast_furnace/blast_aluminium"] },
    { "type": "flag", "id": "gtia:aluminium" }
  ],
  "quest": "可选文本，引擎不使用"
}
```

| 字段 | 含义 |
|---|---|
| `tier` | 在研究树中的列组，至少为 1。默认 1。 |
| `icon` | 在研究树中显示的物品。默认为触发物品。 |
| `prerequisites` | 必须先解锁的节点 id。 |
| `trigger` | `obtain_item`（队伍持有该物品时解锁）或 `manual`（仅限命令和任务）。默认 `manual`。 |
| `requires_mods` | 可选的模组 id 列表。缺少其中任意一个时节点会被静默跳过，便于整合包为可选模组提供节点。不要让其他节点依赖它。 |
| `grants` | `recipe_condition` 在节点解锁前阻止列出的配方 id。`flag` 设置一个可由 `KnowledgeService.hasFlag` 读取的开关。 |

加载器的规则：前置节点未知、前置成环或等级低于 1 的节点会被**丢弃并记录到日志**，依赖它的节点也一并丢弃。字段存在但无效时整个节点失败，而不是静默使用默认值。

触发物品应选择玩家在**不经过**该节点限制的情况下就能获得的物品，否则节点永远无法解锁。好的触发物品是能表明玩家已经准备好的机器或材料。

名称来自语言键：`gtna.research.node.<命名空间>.<用点分隔的路径>`（示例中为 `gtna.research.node.gtia.lv.aluminium`），可选的 `.desc` 键用作提示。没有语言键时显示 id。

受限配方只会为队伍已解锁该节点的所有者运行。工作台配方、AE2 配方和样板不受此限制。

## 命令

| 命令 | 权限 | 作用 |
|---|---|---|
| `/gtna research list [玩家]` | 所有人（查看他人需要 OP） | 已解锁和未解锁的节点。 |
| `/gtna research info <节点>` | 所有人 | 等级和前置节点。 |
| `/gtna research unlock <玩家> <节点> [force]` | OP | 解锁节点；`force` 会解锁其全部前置链。 |
| `/gtna research reset <玩家>` | OP | 清除该玩家队伍的进度。 |

## 开发者

- `KnowledgeService`：`isUnlocked`、`unlock`、`hasFlag`、`recipeAllowed`、`reset`。仅服务端。
- 某个范围首次解锁节点时，会在 Forge 事件总线上发布 `KnowledgeUnlockedEvent`。
- FTB Quests：**研究节点**任务类型（`gtna:research_node`）在节点解锁时完成。仅在安装 FTB Quests 时注册。
- 服务端会在登录时、`/reload` 之后以及进度变化时，把研究图和玩家已解锁的节点发送给客户端。

示例数据包位于 `examples/datapack`。
