# 太空电梯

![太空电梯](../../assets/machines/space_elevator.webp){ loading=lazy }

一条通往轨道的缆索，为底座周围最多 **12 个模块**供能。移植自 GT: New Horizons。

## 运行太空电梯

- 只能在 UHV（高于 ZPM）及以上运行，并需要算力：$128 \cdot (\text{等级} - \text{ZPM})$ CWU/t。
- 通过输入总线放入 **256 个纳米管线轴**。
- 结构中的**太空电梯动力模块**决定所有模块的并行：$4^{\,\text{MK} - 1}$。所有动力模块必须是同一 MK（I 至 V）。MK 还决定组装模块可以运行哪些配方。

| 动力模块 | 模块并行 |
|---|---:|
| MK I | 1 |
| MK II | 4 |
| MK III | 16 |
| MK IV | 64 |
| MK V | 256 |

## 模块

| 模块 | 作用 |
|---|---|
| [太空电梯组装模块](../machines/catalog/assembler_module.md) | 在轨道上组装零件 |
| [太空电梯资源采集模块](../machines/catalog/resource_collection_module.md) | 派出无人机开采 20 种小行星矿物组合并收集 11 种气体，使用 MK I 至 VI 无人机和火箭燃料 |

模块只有在其太空电梯运行时才能工作。
