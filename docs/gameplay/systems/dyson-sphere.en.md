# Dyson Sphere

![](../../assets/machines/dyson_sphere_launch_silo.webp){ loading=lazy }

## Cycle

The **Launch Silo** puts swarm modules in orbit of its planet (surface only). The **Receiving Station** turns the swarm into laser power, with computation and liquid helium.

## Formulas

`EU/t = V[MAX] · modules · (50 − max(0, damage − 60)) / 50`. Each station cycle adds 1 damage; above 99 the swarm loses a module. A launch with damage above 60 **repairs** the swarm instead of adding a module. Up to 100,000 modules per planet.
