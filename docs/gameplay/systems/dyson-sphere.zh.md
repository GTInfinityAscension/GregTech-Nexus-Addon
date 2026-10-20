# 戴森球

![戴森球发射井](../../assets/machines/dyson_sphere_launch_silo.webp){ loading=lazy }

两个多方块在行星的恒星周围建立集能器群，并把它转化为激光能量。

| 机器 | 作用 |
|---|---|
| [戴森球发射井](../machines/catalog/dyson_sphere_launch_silo.md) | 把戴森球模块发射到所在行星的轨道上。只能建在行星表面，不能建在轨道上。发射时间随行星距离增加 |
| [戴森球接收站](../machines/catalog/dyson_sphere_receiving_station.md) | 把集能器群转化为能量并以激光输出。需要算力和液氦 |

## 公式

$$\text{EU/t} = V_{\text{MAX}} \cdot \text{模块数} \cdot \frac{50 - \max(0,\ \text{损伤} - 60)}{50}$$

- 接收站每运行一个循环，集能器群增加 1 点损伤。损伤超过 99 时会失去一个模块。
- 损伤高于 60 时发射会**修复**集能器群，而不是增加模块。
- 每颗行星最多 100,000 个模块。

持续发射，把损伤保持在 60 以下，输出就能保持满功率。
