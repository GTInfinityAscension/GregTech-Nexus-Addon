# Era do vapor

O GTNA transforma a era do vapor num tier de fábrica completo: multiblocos a vapor grandes com paralelo, vapor sem canos, máquinas que não precisam de energia nenhuma e um elevador a vapor que chega a outros planetas. Toda máquina daqui tem uma [página no catálogo](catalog/index.md) com a estrutura.

## Fornecimento de vapor

| Máquina | O que dá |
|---|---|
| [Large Steam Solar Boiler](catalog/large_steam_solar_boiler.md) | campo expansível de células solares de fervura, até 63 blocos para os lados e 125 para trás; a produção cresce com as células ao sol. É a única estrutura que aceita o [hatch de saída de vapor sem fio](../systems/wireless-steam-network.md) |
| [Maravilha dos Cactos](catalog/steam_cactus_wonder.md) | queima carvão mineral e vegetal (8.000 mB de vapor cada) ou blocos de carvão (90.000 mB), um item por segundo; precisa de cactos crescidos no chão de areia |
| [Large Steam Storage Tank](catalog/large_steam_storage_tank.md) | guarda 120.000.000 mB de vapor para suavizar a produção das caldeiras |
| [Dimensionally Transcendent Steam Boiler](catalog/dimensionally_transcendent_steam_boiler.md) | uma caldeira enorme e tardia, vinda do GregTech Leisure |

Depois leve o vapor pela [rede de vapor sem fio](../systems/wireless-steam-network.md) em vez de canos.

## Máquinas a vapor grandes

Versões a vapor das máquinas básicas do GregTech, trazidas do GT: Not Leisure: fornalha, macerador, fundição de ligas, compressor, extrator, martelo de forja, torno, cortadora, dobradeira, extrusora, trefiladora, prensa de conformação, peneira, misturador, centrífuga, centrífuga térmica, lavador de minério, banho químico e montadora de circuitos.

- Elas processam muitos itens de uma vez. O limite de paralelo depende da máquina e pode ser diminuído no controlador:

    | Paralelo | Máquinas |
    |---:|---|
    | 128 | Fornalha, Macerador |
    | 96 | Lavador de Minério |
    | 64 | Fundição de Ligas, Martelo de Forja, Misturador, Centrífuga, Centrífuga Térmica, Banho |
    | 48 | Compressor, Extrator |
    | 32 | Prensa de Conformação |
    | 16 | Torno, Máquina de Corte, Máquina de Dobra, Extrusora, Trefiladora, Peneiradora |
    | 4 | Montadora de Circuitos |

- Cada uma é mais rápida que a versão de um bloco: 10× a Fornalha, 5× o Lavador de Minério, 2,5× o Compressor e a Prensa de Conformação, cerca de 1,75× a Fundição de Ligas e o Extrator, 2× as demais.
- **Alta pressão:** construa a estrutura com os casings de aço em vez dos de bronze (todos precisam ser de aço) e a máquina roda 2× mais rápido gastando 2× vapor.
- Use os [Barramentos Grandes a Vapor](../parts/huge-steam-bus.md) (54 slots) para alimentá-las.

As receitas delas usam os [componentes hidráulicos](../systems/hydraulic-system.md) do GTNA, feitos à mão ou no **Fabricante a Vapor**.

## Máquinas primitivas

Nenhuma delas usa EU. Só o Forno de Coque Infernal usa vapor.

| Máquina | Destaques |
|---|---|
| [Forno de Coque Infernal](catalog/infernal_coke_oven.md) | acelera 1% a cada 5 s até 10× e ganha 16 de paralelo a cada 10 minutos (de 8 até 256). Usa vapor: 6.400 L/s mais 1.600 L/s por estágio. O bônus de velocidade cai quando para |
| [Reator de Hiperpressão](catalog/hyper_pressure_reactor.md) | reações de fluido sem energia e sem vapor, 1 de paralelo; a versão Compacta tem 512 |
| [Alto-Forno Um Salto Adiante](catalog/leap_forward_one_blast_furnace.md) | alto-forno primitivo que cresce: cada camada extra dobra o paralelo (até 32.000) e soma 20 s ao ciclo de 20 s |
| [Fornalha de Pedra Primitiva](catalog/primitive_stone_furnace.md) | faz todas as receitas de fornalha ao mesmo tempo, cada uma em 1 tick |
| [Forno de Tijolos](catalog/brick_kiln.md) | queima tijolos e cerâmicas a partir de argila compactada e carvão |

## Especialistas

| Máquina | O que faz |
|---|---|
| [Superaquecedor de Pedra](catalog/stone_superheater.md) | receitas de superaquecimento da era do vapor, 32 de paralelo |
| [Cortador de Madeira a Vapor](catalog/steam_woodcutter.md) | entra muda, sai tora, 64 de paralelo |
| [Gerador de Pedregulho a Vapor](catalog/steam_cobbler.md) | gerador de pedra; o circuito escolhe a pedra, 16 de paralelo |
| [Fabricante a Vapor](catalog/steam_manufacturer.md) | Manufatura Hidráulica, 16 de paralelo; fabrica as maiores máquinas a vapor |
| [Supercompressor a Vapor](catalog/steam_mega_compressor.md) | 256 de paralelo; feito com 64 Grandes Compressores a Vapor |
| [Portão a Vapor Envelhecido do Minerador do Vazio](catalog/void_miner_steam_gate_aged.md) | minera minério bruto do nada; veja [mineração do vazio](../systems/void-mining.md) |

A maioria deixa diminuir o paralelo no controlador.

## Elevador a Vapor

O [Elevador a Vapor](catalog/steam_elevator.md) é uma estrutura modular com até 12 vagas de módulo. Com o Ad Astra instalado, *Set out* abre a seleção de planetas. Os módulos só funcionam enquanto estão encaixados:

| Módulo | Tiers |
|---|---|
| Voo, Farol, Climático, Repelente de Monstros, Triturador de Entidades, Broca de Óleo | I, II, III |
| Estufa, Apiário, Reprodução de Abelhas, Processador de Minério | um de cada |

O módulo de Reprodução de Abelhas só existe com o Productive Bees instalado.

## Balanceamento para modpacks

Um modpack pode escalar o paralelo e a duração de **todos** os multiblocos a vapor do GTNA de um só lugar, em Java (`GTNASteamBalance`), por exemplo por dificuldade.
