# 超频仓

改进超频曲线本身。通常每一级超频（4 倍 EU/t）让时长减半；安装此仓后，每一级超频把时长除以仓室的除数。移植自 GregTech Odyssey。

| 仓室 | 每级除数 | 每级剩余时长 |
|---|---:|---:|
| UV | 2 | 50% |
| UHV | 3 | 33.3% |
| UEV | 4 | 25% |
| UIV | 5 | 20% |
| UXV | 6 | 16.7% |
| OpV | 7 | 14.3% |
| MAX | 8 | 12.5% |

UV 仓与标准超频相同，因此收益从 UHV 开始。可以在仓室界面中调低除数。数值位于 `config/gtna/balance/hatches.json`（`overclockHatch`）。

## 示例

一个 200 刻的配方，超频两级，安装 EV 加速仓（44%）和 UHV 超频仓：

$$
\begin{aligned}
200 \div 3 \div 3 &= 22.2\ \text{刻} && \text{（两级超频，除数 3）} \\
22.2 \times 0.44 &= 9.8\ \text{刻} && \text{（加速仓）}
\end{aligned}
$$

没有超频仓时，同一配方需要 $200 \div 2 \div 2 \times 0.44 = 22$ 刻。
