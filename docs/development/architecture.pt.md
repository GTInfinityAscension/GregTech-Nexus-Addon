# Arquitetura

O GTNA é um addon do GTCEu (`GTNAGTAddon`) com mod id `gtna` e classe principal `com.raishxn.gtna.GTNACORE`.

| Pacote | Conteúdo |
|---|---|
| `api` | interfaces e utilitários públicos para addons; veja a [API Java](api/overview.md) |
| `common.data` | registros: máquinas (`GTNAMachines`, `GTNAMachines2`, `GTNAMegaMachines`…), blocos, itens, materiais, tipos de receita, origens (`GTNASources`) |
| `common.machine` | classes de máquina: `multiblock/steam`, `electric`, `energy`, `noenergy`, `godforge`, `originals`, `part` (hatches, peças AE2) |
| `data` | datagen: idiomas (`GTNALangProvider`), receitas (`data/recipe`) |
| `config` | `ConfigHolder` (`gtna.yaml`) e `GTNABalance` (`config/gtna/balance/*.json`) |
| `integration` | AE2, JEI, EMI, Jade, KubeJS, FTB |
| `mixin` | mixins do GTCEu e do AE2 (módulos auxiliares, comportamento de hatches, prévias) |
| `client`, `network` | renderização, telas, HUDs, pacotes |
| `research` | o motor de pesquisa |
| `gametest` | GameTests, rodados com `runGameTestServer` |

## Convenções

- Máquinas portadas mantêm estrutura, comportamento e tooltips da fonte; a fonte é declarada uma vez em `GTNASources` e aparece na última linha do tooltip.
- Todo nome visível existe em `en_us` (gerado), `pt_br` e `zh_cn`.
- Nunca use tipos do JEI fora de `integration/jei` nem `net.minecraft.client` em código comum: clientes só com EMI e servidores dedicados precisam carregar o mod. Testes garantem as duas regras.
- Pagamentos de energia e fluido seguem simular → cobrar → executar; saldos nunca ficam negativos.
- As regras da organização (tamanho de arquivo, comentários-chave em três idiomas) estão nas [convenções de desenvolvimento](https://gtinfinityascension.github.io/GTIA-Dev-Doc/development/conventions/).
