# Architecture

GTNA is a GTCEu addon (`GTNAGTAddon`) with mod id `gtna`, main class `com.raishxn.gtna.GTNACORE`.

| Package | Contents |
|---|---|
| `api` | public interfaces and helpers for addons; see the [Java API](api/overview.md) |
| `common.data` | registration: machines (`GTNAMachines`, `GTNAMachines2`, `GTNAMegaMachines`…), blocks, items, materials, recipe types, sources (`GTNASources`) |
| `common.machine` | machine classes: `multiblock/steam`, `electric`, `energy`, `noenergy`, `godforge`, `originals`, `part` (hatches, AE2 parts) |
| `data` | datagen: lang (`GTNALangProvider`), recipes (`data/recipe`) |
| `config` | `ConfigHolder` (`gtna.yaml`) and `GTNABalance` (`config/gtna/balance/*.json`) |
| `integration` | AE2, JEI, EMI, Jade, KubeJS, FTB |
| `mixin` | GTCEu and AE2 mixins (auxiliary modules, hatch behaviour, previews) |
| `client`, `network` | rendering, screens, HUDs, packets |
| `research` | the research engine |
| `gametest` | GameTests, run with `runGameTestServer` |

## Conventions

- Ported machines keep the source's structure, behaviour and tooltips; the source is declared once in `GTNASources` and shown as the last tooltip line.
- Every visible name exists in `en_us` (generated), `pt_br` and `zh_cn`.
- Never reference JEI types outside `integration/jei` and never reference `net.minecraft.client` from common code: EMI-only clients and dedicated servers must load the mod. Tests enforce both.
- Energy and fluid payments are simulate → charge → execute; balances never go negative.
- Organisation-wide rules (file size, trilingual key comments) are in the [developer conventions](https://gtinfinityascension.github.io/GTIA-Dev-Doc/development/conventions/).
