# 诸神之锻炉

![诸神之锻炉](../../assets/gtnh/forge_of_the_gods.png){ loading=lazy }

<small>图片：GTNH Wiki，CC BY-SA 4.0。</small>

诸神之锻炉（Godforge）是一个 UIV 多方块，维持一颗人造恒星，并以无线能量为最多 16 个加工**模块**供能。本页汇总了游戏内看不到的内容：全部公式、根据 GTNA 代码计算的表格，以及与 GTNH 的差异。

|  |  |
|---|---|
| **等级** | UIV |
| **尺寸** | 186 × 127 × 29（第一环） |
| **能量** | 无线，无需能源仓 |
| **超频** | 非完美（4/2），GGEBE 后为 4/2.3 |
| **来源** | 移植自 GT5-Unofficial a3e1e112 |

## 结构

最多三个环。模块位于周围较小的环上。建造新环时，先关闭动画（对控制器使用螺丝刀，或点击外观按钮），建好后用软锤重新开启。全息投影仪根据物品堆叠数量决定显示几个环。

![结构](../../assets/machines/forge_of_gods.webp){ loading=lazy }

## 模块

| 模块 | 解锁 | 基础并行 | 功能 |
|---|---|---|---|
| 太阳烈焰能量锻炉 | START | 1024 | 高炉或多重熔炉（熔炉模式不计入里程碑） |
| 太阳射流融化核心 | FDIM | 512 | 输出熔融物的高炉 |
| 太阳热能等离子制造机 | GPCI | 512 | 粉或流体直接转为等离子体 |
| 太阳聚变异化器 | QGPIU（磁物质：EE） | 64 | 夸克-胶子等离子体与磁物质；需要自动化 |

模块上限：8 个；第二环（CD）后 12 个；第三环（EE）后 16 个。超过上限会断开所有模块。

## 燃料

在输入总线中放入恒星燃料点燃恒星。启动消耗：$f \cdot 25 \cdot 1.2^{f}$ 个。未升级时燃料消耗系数 $f$ 最高为 5。控制器每 5 秒消耗一次燃料（电池充能时 ×2）。

$$
\begin{aligned}
\text{DTR（残渣）} &= f \cdot 300 \cdot 1.15^{f} && (\text{STEM 后 } \times 0.8) \\
\text{恒星等离子体} &= f \cdot 2 \cdot 1.08^{f} && (\text{STEM 后 } \times 0.8) \\
\text{MCSM} &= f / 25 \\
\text{热量} &= 12601 + 1000 \cdot \log_{1.5} f && (\text{SEFCP 后底数为 } 1.12 / 1.18)
\end{aligned}
$$

| f | 基础热量（K） | 启动（个） | DTR/秒 | STEM 后 DTR/秒 | 恒星等离子体/秒 | MCSM/秒 |
|---|---|---|---|---|---|---|
| 1 | 12,601 | 30 | 345 | 276 | 2.16 | 0.04 |
| 2 | 14,310 | 72 | 793 | 635 | 4.67 | 0.08 |
| 3 | 15,310 | 129 | 1,369 | 1,095 | 7.56 | 0.12 |
| 4 | 16,020 | 207 | 2,099 | 1,679 | 10.88 | 0.16 |
| 5 | 16,570 | 311 | 3,017 | 2,414 | 14.69 | 0.20 |
| 6 | 17,020 | 447 | 4,164 | 3,331 | 19.04 | 0.24 |
| 10 | 18,279 | 1,547 | 12,137 | 9,709 | 43.18 | 0.40 |
| 20 | 19,989 | 19,168 | 98,199 | 78,559 | 186 | 0.80 |
| 43 | 21,877 | 2,730,247 | 5,255,292 | 4,204,234 | 2,354 | 1.72 |
| 70 | 23,079 | 6.11e8 | 3.72e8 | 2.98e8 | 30,605 | 2.80 |

TSE 后的最大系数：残渣 70（STEM 后 72），恒星等离子体 181（STEM 后 184），MCSM 无上限。超过 43 后 SA 的有效系数增长变慢：$43 + (f - 43)^{0.4}$。

## 热量与加成上限

热量加成在上限内生效：15,000 K,CNTI 后为 30,000 K。有 NDPE 时，超过 30,000 K 的热量按压缩计算：$30000 + (\text{热量} - 30000)^{e}$,能量锻炉 e = 0.85,其他模块 e = 0.8。

## 并行

$$
\begin{aligned}
\text{并行} &= \text{基础} \cdot \text{CTCDD}(\times 2) \cdot \text{SA} \cdot \text{EPEC} \cdot \text{PoS} \\
\text{SA} &= 1 + f_{\text{有效}} / 15 && (\text{TCT：融化核心及有 DoP 的能量锻炉 } \times 3\text{，其他 } \times 2) \\
\text{EPEC} &= 1 + \text{热量} / 15000 && (\text{融化核心、有 DoP 的能量锻炉；否则 } 1 + \text{热量}/25000) \\
\text{PoS} &= 1 + \text{升级数} / 5 && (\text{融化核心、有 DoP 的能量锻炉；否则 } 1 + \text{升级数}/8)
\end{aligned}
$$

异化器：有 PA 时取总值的平方根，否则为 1。


| f | f 有效 | SA | SA + TCT（融化核心） |
|---|---|---|---|
| 5 | 5 | 1.33 | 4 |
| 15 | 15 | 2 | 6 |
| 43 | 43 | 3.87 | 11.60 |
| 70 | 46 | 4.07 | 12.20 |
| 181 | 50 | 4.33 | 13 |
| 1000 | 58 | 4.87 | 14.60 |

GTNH Wiki 只列出了 /15000 和 /5 的版本。代码在融化核心以外使用更大的除数。

## 速度与能量

$$
\begin{aligned}
\text{IGCC：}\quad & t \times \text{热量}^{-0.01} \\
\text{DoR：}\quad & t \div \text{并行}^{0.02}\text{（等离子）或 } \text{并行}^{0.012}\text{（其他）} \\
\text{REC：}\quad & \text{折扣} = \frac{1 - 1.05^{-0.05 \cdot \text{最大电池}}}{20} \\
\text{IMKG：}\quad & \text{按充能折扣} = 1 - \left(-0.6\,(c - 0.5)^2 + 0.15\right)\text{（等离子），其他 } \times \tfrac{2}{3} \\
\text{GISS：}\quad & V \mathrel{+}= \text{燃料单位/秒} \cdot 10^{8}\ \text{EU/t} \\
\text{NGMS：}\quad & \text{每个激活的环 } V \times 4\text{（最后计算）}
\end{aligned}
$$

## 里程碑

每个里程碑有 7 级，每级给予与等级相同数量的引力子碎片。四个里程碑都到 7 级后，**反转**解除上限，之后每一级的花费与第 7 级相同。

| 等级 | 充能（EU） | 转化（配方） | 催化（燃料） | 组成 |
|---|---|---|---|---|
| 1 | 1e15 | 1e7 | 10,000 | 1 |
| 2 | 9e15 | 4e7 | 30,000 | 2 |
| 3 | 8.1e16 | 1.6e8 | 90,000 | 3 |
| 4 | 7.29e17 | 6.4e8 | 270,000 | 4 |
| 5 | 6.56e18 | 2.56e9 | 810,000 | 5 |
| 6 | 5.9e19 | 1.02e10 | 2,430,000 | 6 |
| 7 | 5.31e20 | 4.1e10 | 7,290,000 | 7 |

## 升级

用引力子碎片购买。蓝线：满足任一前置即可；红线：需要全部前置。异化器之后升级树分为三支（紫：热量；橙：并行；绿：等离子）。起初只能走一支，第二环后两支，第三环后三支。只有在没有依赖它的升级激活时才能退还。

| 标签 | 花费 | 前置 | 效果 |
|---|---|---|---|
| START | 0 | — | 8 个模块、第一环、能量锻炉、20 亿 EU/t、上限 15,000 K |
| IGCC | 1 | START | $t \times \text{热量}^{-0.01}$ |
| STEM | 1 | IGCC | 燃料 × 0.8 |
| CFCE | 1 | IGCC | 最大系数 × 1.2 |
| GISS | 1 | STEM | $V \mathrel{+}= \text{燃料/秒} \cdot 10^{8}$ |
| FDIM | 1 | STEM, CFCE | 解锁融化核心 |
| SA | 1 | CFCE | 并行 $\times (1 + f/15)$ |
| GPCI | 2 | FDIM | 解锁等离子制造机（T3,单步） |
| REC | 2 | GISS + GPCI | 可配置电池与折扣 |
| GEM | 2 | GPCI | 最大系数 += 已激活升级数 |
| CTCDD | 2 | GPCI + SA | 并行 × 2 |
| QGPIU | 2 | REC, CTCDD | 解锁异化器 |
| SEFCP | 3 | QGPIU | 热量底数改为 1.12 / 1.18 |
| TCT | 3 | QGPIU | SA × 2 或 × 3 |
| GGEBE | 3 | QGPIU | 超频 4/2.3 |
| TPTP | 4 | GGEBE | 多步等离子体 |
| CNTI | 3 | SEFCP | 上限 30,000 K |
| DOP | 4 | CNTI | 能量锻炉获得融化核心的加成 |
| EPEC | 3 | TCT | 并行 $\times (1 + \text{热量}/15000)$ 或 $/25000$ |
| IMKG | 3 | GGEBE | 按电池充能折扣 |
| NDPE | 3 | CNTI | 30,000 K 以上热量压缩计算 |
| POS | 3 | EPEC | 并行 $\times (1 + \text{升级数}/5)$ 或 $/8$ |
| DOR | 3 | IMKG | $t \div \text{并行}^{0.02}$ |
| NGMS | 4 | NDPE, POS, DOR | 每环电压 × 4 |
| SEDS | 5 | NGMS | 等离子体最高 T5 |
| PA | 6 | SEDS | 异化器获得加成（平方根） |
| CD | 7 | PA | 第二环，+4 模块 |
| TSE | 8 | CD | 解除燃料上限 |
| TBF | 9 | TSE | 每个模块电压自由设定 |
| EE | 10 | TBF | 第三环，+4 模块，磁物质 |
| END | 12 | EE | 奇异等离子体，碎片弹出 |

### 升级树（GTNH）

![升级树（GTNH）](../../assets/gtnh/godforge_upgrade_tree.png){ loading=lazy width=360 }

<small>图片：GTNH Wiki，CC BY-SA 4.0。</small>

## 升级的额外材料（GTNA）

| Tag | 材料 |
|---|---|
| START | 64 frame Superconductor UIV Base, 32 Superconductor Composite, 16 Metastable Oganesson gear, 8 Eternal Singularity, 64 Robot Arm UIV, 64 Field Generator UEV |
| FDIM | 16 Mega Alloy Blast Smelter, 64 Hypogen Coil, 32 Harmonic Phonon Conduit, 16 Eternal Singularity, 48 Field Restriction Coil T3, 64 Robot Arm UIV, 64 Field Generator UEV |
| GPCI | 8 Stellar Energy Siphon, 8 Advanced Fusion, 64 Fusion Casing MK4, 64 Neutronium foil, 48 dense Quantum plate, 32 Rhugnor gear, 16 Eternal Singularity, 64 Robot Arm UIV, 64 Field Generator UEV |
| QGPIU | 16 Stellar Energy Siphon, 2 Advanced Fusion, 64 Compressed Fusion Coil MK2, 16 Harmonic Phonon Conduit, 4 Transcendent Plasma Mixer, 64 Rhugnor gear, 64 Ichorium gear, 32 Eternal Singularity, 64 Robot Arm UIV, 64 Field Generator UEV |
| CD | 64 frame SpaceTime, 64 frame Superconductor UMV Base, 64 frame Hypogen, 64 frame Dragon Metal, 64 Spatial Casing, 8 Boundary Casing, 2 Mega Battery, 32 Field Generator UXV |
| EE | 64 frame White Dwarf Matter, 64 frame Black Dwarf Matter, 16 frame Eternity, 2 frame Universium, 64 Boundary Casing, 48 Stabilisation Field T5, 16 Mega Battery, 32 Exoticizer, 64 Siphon, 64 Field Generator UXV, 64 Robot Arm UXV |
| END | 64 frame MHDCSM, 64 frame Eternity, 64 frame MagMatter, 64 Stabilisation Field T7, 64 Exoticizer, 4 Astral Array Fabricator, 32 Mega Battery, 64 Field Generator UXV, 64 Robot Arm UXV |

GTNA 相对 GTNH 的替换：抗超高温网 → 中子素箔；聚变内部外壳 2 → 聚变外壳 MK4;紧凑聚变线圈 T4 → 压缩聚变线圈 MK2;UMV 部件 → UXV。未加入跨维对准矩阵与磁物质纳米蜂群。

## 与 GTNH 的差异

- 代码中等离子制造机的基础并行为 512（GTNH Wiki 写的是 384）。
- GTNA 代码中异化器的磁物质由 **EE** 解锁（GTNH Wiki 写的是 END）。
- 材料花费已改为 GTNA 中存在的物品（见上一节）。
- 燃料与最大系数与 GT5-Unofficial a3e1e112 相同。

## 致谢

标注 "GTNH Wiki" 的图片来自 [GT New Horizons Wiki](https://wiki.gtnewhorizons.com/wiki/Forge_of_the_Gods),采用 [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) 许可。本页以相同许可发布。原始机制：GT5-Unofficial（GTNH 团队）。
