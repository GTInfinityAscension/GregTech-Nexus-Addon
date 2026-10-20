# Pressurized Water Reactor (planned)

!!! info "Not in the game yet"
    The design is approved; the code has not started. Numbers below are the design targets and may change in balancing.

A fission reactor for the **IV** age, with the physics of a real PWR on a game time and power scale. It makes **high-pressure steam**; separate turbines turn it into EU. Hard to design, easy to run: everything that needs constant attention has an automatic mode set once (power setpoint, boron program, refuelling campaign).

| | |
|---|---|
| **Tier** | IV (all blocks and parts from the IV age: tungstensteel, Inconel 625, Hastelloy-N, boron carbide, PBI) |
| **Rated power** | 131,072 EU/t thermal (16 A IV), 262,144 L/t of steam |
| **Structure** | containment about 47 × 48 × 47, plus a 66-block cooling tower |
| **Core** | 37 fuel channels, 5 control rod banks, 4 steam generators, 4 primary pumps, pressurizer |

## Fuel

Each channel takes a **fuel assembly** with enrichment $e$ (%) and burnup $B$ (GWd/t):

$$
\begin{aligned}
k_\infty(e, B) &= k_0(e) - 0.006\,B, \qquad k_0(e) = 0.92 + 0.075\,e \\
k_{\text{core}} &= 0.97 \cdot \overline{k_\infty} \quad \text{(neutron leakage)}
\end{aligned}
$$

| Assembly | $e$ (%) | $k_0$ | Max burnup (GWd/t) |
|---|---|---|---|
| LEU-3 | 3 | 1.15 | 19 |
| LEU-4 | 4 | 1.22 | 31.5 |
| LEU-4.5 | 4.5 | 1.26 | 37.8 |
| LEU-5 | 5 | 1.29 | 44 |

Gadolinia assemblies (burnable absorber) and, at LuV, MOX from PUREX-recycled plutonium.

## Reactivity

$$
\begin{aligned}
\rho &= \frac{k - 1}{k} \quad (1\ \text{pcm} = 10^{-5}) \\
\rho_{\text{total}} &= \rho_{\text{fuel}} + \rho_{\text{rods}} + \rho_{\text{boron}} + \rho_{\text{Doppler}} + \rho_{\text{mod}} + \rho_{\text{Xe}} + \rho_{\text{Sm}} \\
\rho_{\text{rods}} &= -8000\ \text{pcm} \cdot \left(x - \frac{\sin 2\pi x}{2\pi}\right) \\
\rho_{\text{boron}} &= -10\ \text{pcm/ppm} \cdot C_B \\
\rho_{\text{Doppler}} &= -2.5\ \text{pcm/K} \cdot (T_{\text{fuel}} - 565\ \text{K}), \qquad \rho_{\text{mod}} = -40\ \text{pcm/K} \cdot (T_{\text{mod}} - 565\ \text{K})
\end{aligned}
$$

Both temperature coefficients are negative, so the reactor regulates itself. Rods are worth little at the ends and a lot in the middle (the real S curve).

## Kinetics

Point kinetics with one delayed-neutron group: $\beta = 650$ pcm, $\Lambda = 2 \times 10^{-5}$ s, $\lambda = 0.08\ \text{s}^{-1}$.

$$
\frac{dn}{dt} = \frac{\rho - \beta}{\Lambda}\,n + \lambda C, \qquad \frac{dC}{dt} = \frac{\beta}{\Lambda}\,n - \lambda C, \qquad \tau \approx \frac{\beta - \rho}{\lambda\,\rho}
$$

Above $\beta$ the reactor is prompt critical; an automatic SCRAM on short period (< 10 s) keeps normal operation far from it.

## Xenon

Real I-135 → Xe-135 chain with time compressed (1 real hour = 1 game minute). After a shutdown xenon rises for about 10 minutes before falling (the xenon pit); the automatic mode shows how long until a restart is possible.

$$
\frac{dI}{dt} = \gamma_I \Sigma_f \varphi - \lambda_I I, \qquad \frac{dX}{dt} = \gamma_X \Sigma_f \varphi + \lambda_I I - \lambda_X X - \sigma_X \varphi X, \qquad \rho_{\text{Xe}} = -2800\ \text{pcm} \cdot \frac{X}{X_{\text{eq}}}
$$

## Fuel cycle

Enrichment uses the real separative work formula:

$$
V(x) = (2x - 1)\ln\frac{x}{1 - x}, \qquad \text{SWU/kg} = V(x_p) + T\,V(x_t) - F\,V(x_f), \quad x_f = 0.711\,\%,\ x_t = 0.25\,\%
$$

| Product | Natural UF₆ feed (kg/kg) | SWU per kg |
|---|---|---|
| LEU-3 | 5.97 | 3.81 |
| LEU-4 | 8.13 | 5.83 |
| LEU-4.5 | 9.22 | 6.87 |
| LEU-5 | 10.3 | 7.92 |

Spent fuel (45 GWd/t) goes to a pool and later to PUREX reprocessing.
