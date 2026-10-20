# Naquadah reactors

Two generators burn naquadah fuel for EU. The **Large Naquadah Reactor** (UHV, port from GregTech Odyssey) comes first; the **Naquadah Hyper Reactor** (UEV, GTNA original) burns the same fuels at four times the EU per mB and can be boosted with plasma.

| | Large Naquadah Reactor | Naquadah Hyper Reactor |
|---|---|---|
| **Tier** | UHV | UEV |
| **Size** | 25 × 25 × 9 | 96 × 38 × 24 |
| **Output** | Dynamo or Laser Source Hatch (one) | Dynamo or Laser Source Hatch (one) |
| **Hatches** | up to 3 Input Hatches, 1 Maintenance | up to 3 Input Hatches, 1 Maintenance |
| **Controller** | Assembly Line, research on the UV Field Generator | Assembly Line (4 Large Naquadah Reactors), research on the Large Naquadah Reactor |
| **Blocks** | [catalog page](catalog/large_naquadah_reactor.md) | [catalog page](catalog/naquadah_hyper_reactor.md) |

<div class="grid" markdown>

![Large Naquadah Reactor](../../assets/machines/large_naquadah_reactor.webp){ loading=lazy }

![Naquadah Hyper Reactor](../../assets/machines/naquadah_hyper_reactor.webp){ loading=lazy }

</div>

## Fuels

Both fuels are made in the Large Chemical Reactor at UV (4000 ticks, 20,000 mB each):

- **Naquadah Fuel**: 16 Naquadah dust, 30,000 mB hydrogen, 15,000 mB nitrogen, 8,000 mB fluorine, 8,000 mB nitric acid.
- **Enriched Naquadah Fuel**: 16 Enriched Naquadah dust, 4 antimony dust, 48,000 mB hydrogen, 30,000 mB nitrogen, 12,000 mB fluorine, 8,000 mB xenon, 6,000 mB radon.

A modpack can replace these recipes by id.

## Energy per mB

$$
\frac{\text{EU}}{\text{mB}} = \frac{t \cdot V}{\text{fuel (mB)}}
$$

| Machine | Recipe | Fuel per run | Time | EU/t | EU per mB of fuel |
|---|---|---|---|---|---|
| Large | Naquadah Fuel + 80 mB hydrogen | 16 mB | 875 ticks | $2^{21}$ (UHV) | 114,688,000 |
| Large | Enriched Naquadah Fuel + 80 mB hydrogen | 16 mB | 1,250 ticks | $2^{21}$ (UHV) | 163,840,000 |
| Large | Naquadah Fuel + 40 mB oxygen plasma | 160 mB | 28,000 ticks | $2^{19}$ (UV) | 91,750,400 |
| Large | Enriched Naquadah Fuel + 40 mB nitrogen plasma | 160 mB | 40,000 ticks | $2^{19}$ (UV) | 131,072,000 |
| Hyper | Naquadah Fuel + 80 mB hydrogen | 16 mB | 875 ticks | $2^{23}$ (UEV) | 458,752,000 |
| Hyper | Enriched Naquadah Fuel + 80 mB hydrogen | 16 mB | 1,250 ticks | $2^{23}$ (UEV) | 655,360,000 |

On the Large reactor the plasma recipes trade some EU per mB for a run 32 times longer at UV.

## Hyper Reactor boost

When a booster plasma is in an input hatch at the start of a run, the run is multiplied by the booster's parallel: fuel, hydrogen and EU/t all grow together, and the booster is consumed once per run. The best booster present wins.

$$
\text{EU/t} = 2^{23} \cdot p \qquad \text{fuel per run} = 16\,p\ \text{mB} \qquad p \le \text{booster parallel}
$$

| Booster (per run) | Parallel $p$ | EU/t with naquadah fuel |
|---|---|---|
| none | 1 | $2^{23}$ = 8,388,608 |
| 40 mB oxygen plasma | 8 | $2^{26}$ = 67,108,864 |
| 40 mB nitrogen plasma | 16 | $2^{27}$ = 134,217,728 |

The parallel is limited by the fuel in the hatches, never by energy. The EU per mB of fuel stays the same, so boosting raises power, not efficiency.
