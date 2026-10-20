# 压水反应堆（计划中）

!!! info "尚未加入游戏"
    设计已批准，代码尚未开始。以下数值为设计目标，平衡时可能调整。

一座 **IV** 时代的裂变反应堆，采用真实压水堆的物理模型，并按游戏的时间与功率尺度缩放。它产出**高压蒸汽**，由独立的涡轮转换为 EU。设计复杂、运行简单：所有需要持续关注的部分都有一次设定即可的自动模式（功率设定点、硼程序、换料计划）。

| | |
|---|---|
| **等级** | IV（所有方块与部件均来自 IV 时代：钨钢、因科镍 625、哈氏合金-N、碳化硼、PBI） |
| **额定功率** | 131,072 EU/t 热功率（16 A IV），262,144 L/t 蒸汽 |
| **结构** | 安全壳约 47 × 48 × 47，另有 66 格高的冷却塔 |
| **堆芯** | 37 个燃料通道、5 组控制棒、4 台蒸汽发生器、4 台一回路泵、稳压器 |

## 燃料

每个通道放入一个**燃料组件**，富集度 $e$（%），燃耗 $B$（GWd/t）：

$$
\begin{aligned}
k_\infty(e, B) &= k_0(e) - 0.006\,B, \qquad k_0(e) = 0.92 + 0.075\,e \\
k_{\text{堆芯}} &= 0.97 \cdot \overline{k_\infty} \quad \text{（中子泄漏）}
\end{aligned}
$$

| 组件 | $e$ (%) | $k_0$ | 最大燃耗 (GWd/t) |
|---|---|---|---|
| LEU-3 | 3 | 1.15 | 19 |
| LEU-4 | 4 | 1.22 | 31.5 |
| LEU-4.5 | 4.5 | 1.26 | 37.8 |
| LEU-5 | 5 | 1.29 | 44 |

另有含钆组件（可燃毒物）；LuV 时可用 PUREX 回收钚制成的 MOX 燃料。

## 反应性

$$
\begin{aligned}
\rho &= \frac{k - 1}{k} \quad (1\ \text{pcm} = 10^{-5}) \\
\rho_{\text{总}} &= \rho_{\text{燃料}} + \rho_{\text{棒}} + \rho_{\text{硼}} + \rho_{\text{多普勒}} + \rho_{\text{慢化剂}} + \rho_{\text{Xe}} + \rho_{\text{Sm}} \\
\rho_{\text{棒}} &= -8000\ \text{pcm} \cdot \left(x - \frac{\sin 2\pi x}{2\pi}\right) \\
\rho_{\text{硼}} &= -10\ \text{pcm/ppm} \cdot C_B \\
\rho_{\text{多普勒}} &= -2.5\ \text{pcm/K} \cdot (T_{\text{燃料}} - 565\ \text{K}), \qquad \rho_{\text{慢化剂}} = -40\ \text{pcm/K} \cdot (T_{\text{慢化剂}} - 565\ \text{K})
\end{aligned}
$$

两个温度系数均为负，因此反应堆可以自我调节。控制棒在两端价值低、在中段价值高（真实的 S 曲线）。

## 动力学

单组缓发中子的点堆动力学：$\beta = 650$ pcm，$\Lambda = 2 \times 10^{-5}$ s，$\lambda = 0.08\ \text{s}^{-1}$。

$$
\frac{dn}{dt} = \frac{\rho - \beta}{\Lambda}\,n + \lambda C, \qquad \frac{dC}{dt} = \frac{\beta}{\Lambda}\,n - \lambda C, \qquad \tau \approx \frac{\beta - \rho}{\lambda\,\rho}
$$

超过 $\beta$ 时反应堆进入瞬发临界；短周期（< 10 秒）自动紧急停堆让正常运行远离这一区域。

## 氙

真实的 I-135 → Xe-135 衰变链，时间经过压缩（现实 1 小时 = 游戏 1 分钟）。停堆后氙会先上升约 10 分钟再下降（碘坑）；自动模式会显示还需多久才能重新启动。

$$
\frac{dI}{dt} = \gamma_I \Sigma_f \varphi - \lambda_I I, \qquad \frac{dX}{dt} = \gamma_X \Sigma_f \varphi + \lambda_I I - \lambda_X X - \sigma_X \varphi X, \qquad \rho_{\text{Xe}} = -2800\ \text{pcm} \cdot \frac{X}{X_{\text{eq}}}
$$

## 燃料循环

浓缩使用真实的分离功公式：

$$
V(x) = (2x - 1)\ln\frac{x}{1 - x}, \qquad \text{SWU/kg} = V(x_p) + T\,V(x_t) - F\,V(x_f), \quad x_f = 0.711\,\%,\ x_t = 0.25\,\%
$$

| 产品 | 天然 UF₆ 进料 (kg/kg) | 每 kg SWU |
|---|---|---|
| LEU-3 | 5.97 | 3.81 |
| LEU-4 | 8.13 | 5.83 |
| LEU-4.5 | 9.22 | 6.87 |
| LEU-5 | 10.3 | 7.92 |

乏燃料（45 GWd/t）先送入乏燃料池，之后进行 PUREX 后处理。
