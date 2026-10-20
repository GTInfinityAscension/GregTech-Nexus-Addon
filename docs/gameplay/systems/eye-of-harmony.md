# Eye of Harmony

![Eye of Harmony](../../assets/machines/eye_of_harmony.webp){ loading=lazy }

The Eye of Harmony simulates a miniature universe and extracts the ores of a whole planet. Each run is expensive, slow and may fail; this page shows every calculation the controller makes.

|  |  |
|---|---|
| **Tier** | UXV |
| **Energy** | wireless (Nexus network) |
| **Origin** | port of GT5-Unofficial a3e1e112 |

## Planetary programs

The planet item in the controller slot picks the program. Products come from the GTCEu ore veins registered in that dimension. Packs add planets through KubeJS (`GTNAStartupEvents.eyeOfHarmony`). Planets beyond the Minecraft dimensions need Ad Astra.

```
base duration = 18000 s · 1.4^tier
each gas (H and He) = 1e9 · (tier + 1) mB
base chance = 1 − 0.05 · tier
return = cost · (0.6 + tier/10)
cost = plasmas + ticks · (2^19 + 1e11) EU
```

| Planet | Tier | Base duration | H and He (mB) | Base chance | Cost without plasmas (EU) |
|---|---|---|---|---|---|
| Overworld, Nether, End | 0 | 5 h | 1e9 | 100% | 3.6e16 |
| Moon | 1 | 7 h | 2e9 | 95% | 5.04e16 |
| Mars | 2 | 9.80 h | 3e9 | 90% | 7.06e16 |
| Venus, Mercury | 4 | 19.21 h | 5e9 | 80% | 1.38e17 |
| Glacio | 5 | 26.89 h | 6e9 | 75% | 1.94e17 |

## Fields and circuit

Three fields of tier 0 to 8 (compression `c`, acceleration `a`, stabilisation `s`) and a circuit `k` from 0 to 24:

```
duration = max(T · 2^−a · 0.97^(c − r) · 2^−k, 1)          r = program minimum compression
startup cost = cost · 4^k
return = base return · (1 − (8 − s) · 0.05)                does not scale with the circuit
chance = base chance − 0.0925·a + 0.05·s − gas penalties
yield = 1 − 0.05·s − gas penalties
gas penalty = 1 − exp(−(30 · (stored/required − 1))²)
```

| a / s | Chance (Overworld) | Yield | Time |
|---|---|---|---|
| 0 / 0 | 100% | 100% | ÷1 |
| 2 / 2 | 91.50% | 90% | ÷4 |
| 4 / 4 | 83% | 80% | ÷16 |
| 6 / 6 | 74.50% | 70% | ÷64 |
| 8 / 8 | 66% | 60% | ÷256 |
| 8 / 0 | 26% | 100% | ÷256 |
| 0 / 8 | 100% | 60% | ÷1 |

Excess gas also reduces chance and yield: storing 10% more already costs 99.99% per gas. Deliver the exact amount.

## Failure and pity

- A failure still returns the EU and produces SpaceTime: `chance · 14400 · 2^(tier + 1)` mB.
- Consecutive failures **under the same conditions** build pity: `(1 − chance) · chance` per failure. Changing fields or circuit resets it.
- The result is rolled at startup and saved: breaking the controller or reloading the world does not change it.

## Tips

- The controller consumes **all** stored hydrogen and helium at startup, excess included.
- The return arrives through the Nexus network in parts; network loss is shown separately in the GUI.
- A full output never loses anything: the cycle waits.
