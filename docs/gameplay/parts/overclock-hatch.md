# Overclock Hatch

Improves the overclock curve itself. Normally each overclock step (4× EU/t) halves the duration; with this hatch each step divides it by the hatch's divisor. Ported from GregTech Odyssey.

| Hatch | Divisor per step | Duration per step |
|---|---:|---:|
| UV | 2 | 50% |
| UHV | 3 | 33.3% |
| UEV | 4 | 25% |
| UIV | 5 | 20% |
| UXV | 6 | 16.7% |
| OpV | 7 | 14.3% |
| MAX | 8 | 12.5% |

The UV hatch equals the standard overclock, so the gain starts at UHV. You can lower the divisor in the hatch UI. Values are in `config/gtna/balance/hatches.json` (`overclockHatch`).

## Example

A 200-tick recipe overclocked twice, with an EV Accelerate Hatch (44%) and a UHV Overclock Hatch:

```
200 ÷ 3 ÷ 3 = 22.2 ticks      (two overclock steps with divisor 3)
22.2 × 0.44 = 9.8 ticks       (Accelerate Hatch)
```

Without the Overclock Hatch the same recipe takes `200 ÷ 2 ÷ 2 × 0.44 = 22` ticks.
