"""Hand-designed system pages of the wiki whose tables are computed from the constants in the mod code.

    python3 tools/wiki/system_pages.py

Forge of Gods: formulas from api/machine/feature/godforge/GodforgeMath.java (port of GT5-Unofficial a3e1e112).
Images credited to the GTNH wiki (CC BY-SA 4.0) live in docs/assets/gtnh/.
"""
import math
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
OUT = os.path.join(ROOT, 'docs/gameplay/systems')

# constants copied from GodforgeData.java / GodforgeMath.java
POWER_C, RECIPE_C, FUEL_C = 1e15, 1e7, 1e4
MAX_RESIDUE, MAX_RESIDUE_STEM, MAX_PLASMA, MAX_PLASMA_STEM = 70, 72, 181, 184


def n(x, lang):
    if x >= 1e7: s = f'{x:.3g}'.replace('e+0', 'e').replace('e+', 'e')
    else: s = f'{x:,.0f}' if abs(x - round(x)) < 1e-9 or x >= 100 else f'{x:,.2f}'
    return s.replace(',', 'X').replace('.', ',').replace('X', '.') if lang == 'pt' else s


def table(head, rows):
    return '\n'.join(['| ' + ' | '.join(head) + ' |', '|' + '|'.join('---' for _ in head) + '|'] +
                     ['| ' + ' | '.join(str(c) for c in r) + ' |' for r in rows]) + '\n'


def heat(f, base=1.5): return 12601 + int(math.log(f) / math.log(base) * 1000)
def fuel_residue(f, stem=False): return f * 300 * 1.15 ** f * (0.8 if stem else 1)
def fuel_plasma(f, stem=False): return f * 2 * 1.08 ** f * (0.8 if stem else 1)
def startup(f): return max(f * 25 * 1.2 ** f, 1)
def eff_factor(f): return f if f <= 43 else 43 + math.floor((f - 43) ** 0.4)


T = {
    'pt': dict(
        title='Forja dos Deuses', intro='A Forja dos Deuses (Godforge) é um multibloco UIV que mantém uma estrela artificial e alimenta até 16 **módulos** de processamento com energia wireless. '
        'Esta página reúne o que o jogo não mostra: todas as fórmulas, as tabelas calculadas a partir do código do GTNA e as diferenças em relação ao GTNH.',
        credit='Imagem: GTNH Wiki, CC BY-SA 4.0.', facts=[('Tier', 'UIV'), ('Tamanho', '186 × 127 × 29 (anel 1)'), ('Energia', 'wireless, sem hatch de energia'),
        ('Overclock', 'imperfeito (4/2), 4/2,3 com GGEBE'), ('Fonte', 'port de GT5-Unofficial a3e1e112')],
        s_struct='Estrutura', struct='Até três anéis. Os módulos ficam em anéis menores ao redor. Para construir um anel novo, desligue a animação (chave de fenda no controlador ou o botão nos cosméticos), construa e religue com o martelo macio. '
        'O projetor holográfico usa o tamanho da pilha para escolher quantos anéis mostrar.',
        s_modules='Módulos', mod_head=['Módulo', 'Libera', 'Paralelo base', 'Função'],
        mods=[('Helioflare Power Forge', 'START', 1024, 'alto-forno ou multi-fornalha (modo fornalha não conta nos marcos)'),
              ('Helioflux Melting Core', 'FDIM', 512, 'alto-forno com saída fundida'), ('Heliothermal Plasma Fabricator', 'GPCI', 512, 'pó/fluido direto para plasma'),
              ('Heliofusion Exoticizer', 'QGPIU (matéria mágica: EE)', 64, 'plasma de quarks e glúons e MagMatter; precisa de automação')],
        slots='Limite de módulos: 8, 12 com o anel 2 (CD), 16 com o anel 3 (EE). Passar do limite desconecta todos.',
        s_fuel='Combustível', fuel_txt='A estrela é acesa com Combustível Estelar no barramento de entrada. Custo de partida: `f · 25 · 1,2^f` itens. '
        'O fator de consumo `f` vai até 5 sem upgrades. O controlador drena a cada 5 s (×2 com a bateria carregando).',
        fuel_head=['f', 'Calor base (K)', 'Partida (itens)', 'DTR/s', 'DTR/s com STEM', 'Plasma estelar/s', 'MCSM/s'],
        fuel_formula='```\nDTR (resíduo)        f · 300 · 1,15^f      (×0,8 com STEM)\nPlasma estelar       f · 2 · 1,08^f        (×0,8 com STEM)\nMCSM                 f / 25\ncalor                12601 + log₁,₅(f) · 1000   (base 1,12 / 1,18 com SEFCP)\n```\n',
        caps='Fatores máximos com TSE: resíduo 70 (72 com STEM), plasma estelar 181 (184 com STEM), MCSM sem limite. Acima de 43 o fator efetivo do SA cresce devagar: `43 + (f − 43)^0,4`.',
        s_heat='Calor e teto de bônus', heat_txt='Os bônus de calor valem até o teto: 15.000 K, ou 30.000 K com CNTI. Com NDPE, acima de 30.000 K o calor conta comprimido: `30000 + (calor − 30000)^e`, com e = 0,85 no Power Forge e 0,8 nos demais.',
        s_par='Paralelo', par_txt='```\nparalelo = base · CTCDD(×2) · SA · EPEC · PoS\nSA    = 1 + f_efetivo / 15          (TCT: ×3 no Melting Core e no Power Forge com DoP, ×2 nos outros)\nEPEC  = 1 + calor / 15000           (Melting Core e Power Forge com DoP) ou 1 + calor / 25000\nPoS   = 1 + upgrades / 5            (Melting Core e Power Forge com DoP) ou 1 + upgrades / 8\nExoticizer: raiz quadrada do total com PA, senão 1\n```\n',
        par_note='A wiki do GTNH mostra só a versão de 15000 e de /5. O código usa divisores maiores fora do Melting Core.',
        s_speed='Velocidade e energia', speed_txt='```\nIGCC   tempo × calor^−0,01\nDoR    tempo ÷ paralelo^0,02 (plasma) ou ^0,012 (outros)\nREC    desconto = (1 − 1,05^(−0,05 · bateria máx)) / 20\nIMKG   desconto pela carga: 1 − (−0,6·(c − 0,5)² + 0,15) no plasma, ×2/3 nos outros\nGISS   voltagem += unidades de combustível/s · 1e8 EU/t\nNGMS   voltagem × 4 por anel ativo (aplicado por último)\n```\n',
        s_ms='Marcos', ms_txt='Cada marco tem 7 níveis e dá fragmentos de gráviton iguais ao nível. Depois que os quatro chegam ao nível 7, a **Inversão** remove o teto e cada nível novo custa o mesmo que o 7.',
        ms_head=['Nível', 'Carga (EU)', 'Conversão (receitas)', 'Catalisador (combustível)', 'Composição'],
        s_up='Upgrades', up_txt='Comprados com fragmentos. Linha azul: basta um pré-requisito; vermelha: todos. Depois do Exoticizer a árvore se divide em três (roxo: calor; laranja: paralelo; verde: plasma). Um ramo no começo, o segundo com o anel 2, os três com o anel 3. Reembolso só sem upgrades dependentes ativos.',
        up_head=['Tag', 'Custo', 'Pré-requisito', 'Efeito'],
        s_cost='Materiais extras dos upgrades (GTNA)', cost_note='Substituições do GTNA em relação ao GTNH: Malha Resistente a UHT → folha de Neutrônio; Fusion Internal Casing 2 → Fusion Casing MK4; Compact Fusion Coil T4 → Compressed Fusion Coil MK2; peças UMV → UXV. Transdimensional Alignment Matrix e nanites de MagMatter não entram.',
        s_diff='Diferenças em relação ao GTNH', diffs=['Plasma Fabricator com paralelo base 512 no código (a wiki do GTNH cita 384).', 'A matéria mágica do Exoticizer é liberada pelo **EE** no código do GTNA (a wiki do GTNH cita END).',
                    'Custos materiais adaptados aos itens que existem no GTNA (seção anterior).', 'Combustíveis e fatores máximos idênticos ao GT5-Unofficial a3e1e112.'],
        s_tree='Árvore de upgrades (GTNH)', s_credits='Créditos',
        credits='Imagens marcadas com "GTNH Wiki" vêm da [wiki do GT New Horizons](https://wiki.gtnewhorizons.com/wiki/Forge_of_the_Gods), licenciadas sob [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). '
        'Esta página é distribuída sob a mesma licença. Mecânica original: GT5-Unofficial (equipe GTNH).'),
    'en': dict(
        title='Forge of the Gods', intro='The Forge of the Gods (Godforge) is a UIV multiblock that keeps an artificial star and powers up to 16 processing **modules** with wireless energy. '
        'This page collects what the game does not show: every formula, tables computed from the GTNA code, and the differences from GTNH.',
        credit='Image: GTNH Wiki, CC BY-SA 4.0.', facts=[('Tier', 'UIV'), ('Size', '186 × 127 × 29 (ring 1)'), ('Energy', 'wireless, no energy hatch'),
        ('Overclock', 'imperfect (4/2), 4/2.3 with GGEBE'), ('Source', 'port of GT5-Unofficial a3e1e112')],
        s_struct='Structure', struct='Up to three rings. Modules sit in smaller rings around them. To build a new ring, turn the animation off (screwdriver on the controller or the cosmetics button), build it, and turn it back on with a soft mallet. '
        'The hologram projector uses the stack size to pick how many rings to show.',
        s_modules='Modules', mod_head=['Module', 'Unlock', 'Base parallel', 'Function'],
        mods=[('Helioflare Power Forge', 'START', 1024, 'blast furnace or multi-smelter (furnace mode does not count for milestones)'),
              ('Helioflux Melting Core', 'FDIM', 512, 'blast furnace with molten output'), ('Heliothermal Plasma Fabricator', 'GPCI', 512, 'dust/fluid straight to plasma'),
              ('Heliofusion Exoticizer', 'QGPIU (magmatter: EE)', 64, 'quark-gluon plasma and MagMatter; needs automation')],
        slots='Module limit: 8, 12 with ring 2 (CD), 16 with ring 3 (EE). Exceeding it disconnects all modules.',
        s_fuel='Fuel', fuel_txt='The star is lit with Stellar Fuel in the input bus. Startup cost: `f · 25 · 1.2^f` items. '
        'The consumption factor `f` goes up to 5 without upgrades. The controller drains every 5 s (×2 while the battery charges).',
        fuel_head=['f', 'Base heat (K)', 'Startup (items)', 'DTR/s', 'DTR/s with STEM', 'Stellar plasma/s', 'MCSM/s'],
        fuel_formula='```\nDTR (residue)        f · 300 · 1.15^f      (×0.8 with STEM)\nStellar plasma       f · 2 · 1.08^f        (×0.8 with STEM)\nMCSM                 f / 25\nheat                 12601 + log₁.₅(f) · 1000   (base 1.12 / 1.18 with SEFCP)\n```\n',
        caps='Max factors with TSE: residue 70 (72 with STEM), stellar plasma 181 (184 with STEM), MCSM uncapped. Above 43 the SA effective factor grows slowly: `43 + (f − 43)^0.4`.',
        s_heat='Heat and bonus cap', heat_txt='Heat bonuses apply up to the cap: 15,000 K, or 30,000 K with CNTI. With NDPE, heat above 30,000 K counts compressed: `30000 + (heat − 30000)^e`, e = 0.85 for the Power Forge and 0.8 for the others.',
        s_par='Parallel', par_txt='```\nparallel = base · CTCDD(×2) · SA · EPEC · PoS\nSA    = 1 + f_effective / 15        (TCT: ×3 on Melting Core and on Power Forge with DoP, ×2 otherwise)\nEPEC  = 1 + heat / 15000            (Melting Core, Power Forge with DoP) or 1 + heat / 25000\nPoS   = 1 + upgrades / 5            (Melting Core, Power Forge with DoP) or 1 + upgrades / 8\nExoticizer: square root of the total with PA, otherwise 1\n```\n',
        par_note='The GTNH wiki only shows the /15000 and /5 versions. The code uses larger divisors outside the Melting Core.',
        s_speed='Speed and energy', speed_txt='```\nIGCC   time × heat^−0.01\nDoR    time ÷ parallel^0.02 (plasma) or ^0.012 (others)\nREC    discount = (1 − 1.05^(−0.05 · max battery)) / 20\nIMKG   charge discount: 1 − (−0.6·(c − 0.5)² + 0.15) on plasma, ×2/3 on the others\nGISS   voltage += fuel units/s · 1e8 EU/t\nNGMS   voltage × 4 per active ring (applied last)\n```\n',
        s_ms='Milestones', ms_txt='Each milestone has 7 tiers and grants graviton shards equal to the tier. Once all four reach tier 7, **Inversion** removes the cap and every new tier costs the same as tier 7.',
        ms_head=['Tier', 'Charge (EU)', 'Conversion (recipes)', 'Catalyst (fuel)', 'Composition'],
        s_up='Upgrades', up_txt='Bought with shards. Blue line: one prerequisite is enough; red: all are needed. After the Exoticizer the tree splits in three (purple: heat; orange: parallel; green: plasma). One branch first, the second with ring 2, all three with ring 3. Refunds only with no dependent upgrade active.',
        up_head=['Tag', 'Cost', 'Requires', 'Effect'],
        s_cost='Extra upgrade materials (GTNA)', cost_note='GTNA substitutions compared with GTNH: UHT Resistant Mesh → Neutronium foil; Fusion Internal Casing 2 → Fusion Casing MK4; Compact Fusion Coil T4 → Compressed Fusion Coil MK2; UMV parts → UXV. Transdimensional Alignment Matrix and MagMatter nanites are left out.',
        s_diff='Differences from GTNH', diffs=['Plasma Fabricator base parallel is 512 in the code (the GTNH wiki says 384).', 'Exoticizer magmatter is unlocked by **EE** in the GTNA code (the GTNH wiki says END).',
                    'Material costs adapted to items that exist in GTNA (previous section).', 'Fuels and max factors identical to GT5-Unofficial a3e1e112.'],
        s_tree='Upgrade tree (GTNH)', s_credits='Credits',
        credits='Images marked "GTNH Wiki" come from the [GT New Horizons wiki](https://wiki.gtnewhorizons.com/wiki/Forge_of_the_Gods), licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). '
        'This page is distributed under the same license. Original mechanics: GT5-Unofficial (GTNH team).'),
}

UPGRADES = [  # tag, cost, requires, effect pt, effect en
    ('START', 0, '—', '8 módulos, anel 1, Power Forge, 2 bi EU/t, teto 15.000 K', '8 modules, ring 1, Power Forge, 2 bn EU/t, 15,000 K cap'),
    ('IGCC', 1, 'START', 'tempo × calor^−0,01', 'time × heat^−0.01'), ('STEM', 1, 'IGCC', 'combustível × 0,8', 'fuel × 0.8'),
    ('CFCE', 1, 'IGCC', 'fator máximo × 1,2', 'max factor × 1.2'), ('GISS', 1, 'STEM', 'voltagem += combustível/s · 1e8', 'voltage += fuel/s · 1e8'),
    ('FDIM', 1, 'STEM, CFCE', 'libera Melting Core', 'unlocks Melting Core'), ('SA', 1, 'CFCE', 'paralelo × (1 + f/15)', 'parallel × (1 + f/15)'),
    ('GPCI', 2, 'FDIM', 'libera Plasma Fabricator (T3, um passo)', 'unlocks Plasma Fabricator (T3, single step)'),
    ('REC', 2, 'GISS + GPCI', 'bateria configurável e desconto', 'configurable battery and discount'),
    ('GEM', 2, 'GPCI', 'fator máximo += upgrades ativos', 'max factor += active upgrades'),
    ('CTCDD', 2, 'GPCI + SA', 'paralelo × 2', 'parallel × 2'), ('QGPIU', 2, 'REC, CTCDD', 'libera Exoticizer', 'unlocks Exoticizer'),
    ('SEFCP', 3, 'QGPIU', 'calor com base 1,12 / 1,18', 'heat with base 1.12 / 1.18'), ('TCT', 3, 'QGPIU', 'SA × 2 ou × 3', 'SA × 2 or × 3'),
    ('GGEBE', 3, 'QGPIU', 'overclock 4/2,3', 'overclock 4/2.3'), ('TPTP', 4, 'GGEBE', 'plasmas de vários passos', 'multi-step plasmas'),
    ('CNTI', 3, 'SEFCP', 'teto 30.000 K', '30,000 K cap'), ('DOP', 4, 'CNTI', 'Power Forge ganha bônus do Melting Core', 'Power Forge gets Melting Core bonuses'),
    ('EPEC', 3, 'TCT', 'paralelo × (1 + calor/15000 ou /25000)', 'parallel × (1 + heat/15000 or /25000)'),
    ('IMKG', 3, 'GGEBE', 'desconto pela carga da bateria', 'battery-charge discount'), ('NDPE', 3, 'CNTI', 'calor comprimido acima de 30.000 K', 'compressed heat above 30,000 K'),
    ('POS', 3, 'EPEC', 'paralelo × (1 + upgrades/5 ou /8)', 'parallel × (1 + upgrades/5 or /8)'), ('DOR', 3, 'IMKG', 'tempo ÷ paralelo^0,02', 'time ÷ parallel^0.02'),
    ('NGMS', 4, 'NDPE, POS, DOR', 'voltagem × 4 por anel', 'voltage × 4 per ring'), ('SEDS', 5, 'NGMS', 'plasmas até T5', 'plasmas up to T5'),
    ('PA', 6, 'SEDS', 'Exoticizer recebe os bônus (raiz quadrada)', 'Exoticizer gets the bonuses (square root)'),
    ('CD', 7, 'PA', 'anel 2, +4 módulos', 'ring 2, +4 modules'), ('TSE', 8, 'CD', 'tira o teto do combustível', 'removes the fuel cap'),
    ('TBF', 9, 'TSE', 'voltagem livre por módulo', 'free voltage per module'), ('EE', 10, 'TBF', 'anel 3, +4 módulos, matéria mágica', 'ring 3, +4 modules, magmatter'),
    ('END', 12, 'EE', 'plasmas exóticos, ejeção de fragmentos', 'exotic plasmas, shard ejection'),
]
COSTS = [
    ('START', '64 frame Superconductor UIV Base, 32 Superconductor Composite, 16 Metastable Oganesson gear, 8 Eternal Singularity, 64 Robot Arm UIV, 64 Field Generator UEV'),
    ('FDIM', '16 Mega Alloy Blast Smelter, 64 Hypogen Coil, 32 Harmonic Phonon Conduit, 16 Eternal Singularity, 48 Field Restriction Coil T3, 64 Robot Arm UIV, 64 Field Generator UEV'),
    ('GPCI', '8 Stellar Energy Siphon, 8 Advanced Fusion, 64 Fusion Casing MK4, 64 Neutronium foil, 48 dense Quantum plate, 32 Rhugnor gear, 16 Eternal Singularity, 64 Robot Arm UIV, 64 Field Generator UEV'),
    ('QGPIU', '16 Stellar Energy Siphon, 2 Advanced Fusion, 64 Compressed Fusion Coil MK2, 16 Harmonic Phonon Conduit, 4 Transcendent Plasma Mixer, 64 Rhugnor gear, 64 Ichorium gear, 32 Eternal Singularity, 64 Robot Arm UIV, 64 Field Generator UEV'),
    ('CD', '64 frame SpaceTime, 64 frame Superconductor UMV Base, 64 frame Hypogen, 64 frame Dragon Metal, 64 Spatial Casing, 8 Boundary Casing, 2 Mega Battery, 32 Field Generator UXV'),
    ('EE', '64 frame White Dwarf Matter, 64 frame Black Dwarf Matter, 16 frame Eternity, 2 frame Universium, 64 Boundary Casing, 48 Stabilisation Field T5, 16 Mega Battery, 32 Exoticizer, 64 Siphon, 64 Field Generator UXV, 64 Robot Arm UXV'),
    ('END', '64 frame MHDCSM, 64 frame Eternity, 64 frame MagMatter, 64 Stabilisation Field T7, 64 Exoticizer, 4 Astral Array Fabricator, 32 Mega Battery, 64 Field Generator UXV, 64 Robot Arm UXV'),
]


def forge_of_gods(lang):
    t = T[lang]; L = []
    a = L.append
    a(f'# {t["title"]}\n')
    a(f'![{t["title"]}](../../assets/gtnh/forge_of_the_gods.png){{ loading=lazy }}\n')
    a(f'<small>{t["credit"]}</small>\n')
    a(t['intro'] + '\n')
    a(table(['', ''], [(f'**{k}**', v) for k, v in t['facts']]))
    a(f'## {t["s_struct"]}\n\n{t["struct"]}\n')
    a(f'![structure](../../assets/machines/forge_of_gods.webp){{ loading=lazy }}\n')
    a(f'## {t["s_modules"]}\n')
    a(table(t['mod_head'], t['mods'])); a(t['slots'] + '\n')
    a(f'## {t["s_fuel"]}\n\n{t["fuel_txt"]}\n')
    a(t['fuel_formula'])
    a(table(t['fuel_head'], [(f, n(heat(f), lang), n(math.floor(startup(f)), lang), n(fuel_residue(f), lang), n(fuel_residue(f, True), lang),
                              n(fuel_plasma(f), lang), n(f / 25, lang)) for f in (1, 2, 3, 4, 5, 6, 10, 20, 43, 70)]))
    a(t['caps'] + '\n')
    a(f'## {t["s_heat"]}\n\n{t["heat_txt"]}\n')
    a(f'## {t["s_par"]}\n\n{t["par_txt"]}')
    a(table(['f', 'f_ef.', 'SA', 'SA+TCT (Melting)'], [(f, eff_factor(f), n(1 + eff_factor(f) / 15, lang), n((1 + eff_factor(f) / 15) * 3, lang)) for f in (5, 15, 43, 70, 181, 1000)]))
    a(t['par_note'] + '\n')
    a(f'## {t["s_speed"]}\n\n{t["speed_txt"]}')
    a(f'## {t["s_ms"]}\n\n{t["ms_txt"]}\n')
    a(table(t['ms_head'], [(k, n(POWER_C * 9 ** (k - 1), lang), n(RECIPE_C * 4 ** (k - 1), lang), n(FUEL_C * 3 ** (k - 1), lang), k) for k in range(1, 8)]))
    a(f'## {t["s_up"]}\n\n{t["up_txt"]}\n')
    a(table(t['up_head'], [(u[0], u[1], u[2], u[3] if lang == 'pt' else u[4]) for u in UPGRADES]))
    a(f'### {t["s_tree"]}\n\n![tree](../../assets/gtnh/godforge_upgrade_tree.png){{ loading=lazy width=360 }}\n\n<small>{t["credit"]}</small>\n')
    a(f'## {t["s_cost"]}\n')
    a(table(['Tag', 'Materiais' if lang == 'pt' else 'Materials'], COSTS)); a(t['cost_note'] + '\n')
    a(f'## {t["s_diff"]}\n'); a('\n'.join('- ' + d for d in t['diffs']) + '\n')
    a(f'## {t["s_credits"]}\n\n{t["credits"]}\n')
    return '\n'.join(L)


def main():
    os.makedirs(OUT, exist_ok=True)
    for lang, suffix in (('pt', '.md'), ('en', '.en.md')):
        open(os.path.join(OUT, 'forge-of-gods' + suffix), 'w', encoding='utf-8').write(forge_of_gods(lang))
    print('forge-of-gods')




# ---------------------------------------------------------------------------------------------------------
# Eye of Harmony (api/machine/feature/eyeofharmony/EyeOfHarmonyMath.java, GT5U a3e1e112)
# ---------------------------------------------------------------------------------------------------------
PLANETS = [('Overworld / Nether / End', 0), ('Lua / Moon', 1), ('Marte / Mars', 2), ('Vênus, Mercúrio / Venus, Mercury', 4), ('Glacio', 5)]


def eoh_seconds(t):
    r, b, e = 1.0, 1.4, t
    while e > 0:
        if e & 1: r *= b
        b *= b; e >>= 1
    return int(18000 * r)


def eye_of_harmony(lang):
    pt = lang == 'pt'; L = []; a = L.append
    a('# Olho da Harmonia\n' if pt else '# Eye of Harmony\n')
    a('![](../../assets/machines/eye_of_harmony.webp){ loading=lazy }\n')
    a(('O Olho da Harmonia simula um universo em miniatura e extrai os minérios de um planeta inteiro. Cada operação é cara, '
       'demorada e pode falhar; esta página mostra todas as contas que o controlador faz.\n') if pt else
      ('The Eye of Harmony simulates a miniature universe and extracts the ores of a whole planet. Each run is expensive, '
       'slow and may fail; this page shows every calculation the controller makes.\n'))
    a(table(['', ''], [('**Tier**', 'UXV'), ('**' + ('Energia' if pt else 'Energy') + '**', 'wireless (Nexus)'),
                       ('**' + ('Fonte' if pt else 'Source') + '**', 'GT5-Unofficial a3e1e112')]))
    a('## ' + ('Programas planetários' if pt else 'Planetary programs') + '\n')
    a(('O item de planeta no slot do controlador escolhe o programa. Os produtos vêm dos veios de minério do GTCEu registrados naquela dimensão. '
       'Packs adicionam planetas pelo KubeJS (`GTNAStartupEvents.eyeOfHarmony`).\n') if pt else
      ('The planet item in the controller slot picks the program. Products come from the GTCEu ore veins registered in that dimension. '
       'Packs add planets through KubeJS (`GTNAStartupEvents.eyeOfHarmony`).\n'))
    a('```\n' + ('duração base = 18000 s · 1,4^tier\ngás de cada (H e He) = 1e9 · (tier + 1) mB\nchance base = 1 − 0,05 · tier\nretorno = custo · (0,6 + tier/10)\ncusto = plasmas + ticks · (2^19 + 1e11) EU' if pt else
                 'base duration = 18000 s · 1.4^tier\neach gas (H and He) = 1e9 · (tier + 1) mB\nbase chance = 1 − 0.05 · tier\nreturn = cost · (0.6 + tier/10)\ncost = plasmas + ticks · (2^19 + 1e11) EU') + '\n```\n')
    a(table(['Planeta' if pt else 'Planet', 'Tier', 'Duração base' if pt else 'Base duration', 'H e He (mB)' if pt else 'H and He (mB)', 'Chance base' if pt else 'Base chance', 'Custo sem plasmas (EU)' if pt else 'Cost without plasmas (EU)'],
            [(p, t, f'{n(eoh_seconds(t) / 3600, lang)} h', n(1e9 * (t + 1), lang), f'{n(100 - 5 * t, lang)}%', n(eoh_seconds(t) * 20 * (2 ** 19 + 1e11), lang)) for p, t in PLANETS]))
    a('## ' + ('Campos e circuito' if pt else 'Fields and circuit') + '\n')
    a(('Três campos de tier 0 a 8 (compressão `c`, aceleração `a`, estabilização `s`) e um circuito `k` de 0 a 24:\n') if pt else
      ('Three fields of tier 0 to 8 (compression `c`, acceleration `a`, stabilisation `s`) and a circuit `k` from 0 to 24:\n'))
    a('```\n' + ('duração = max(T · 2^−a · 0,97^(c − r) · 2^−k, 1)          r = compressão mínima do programa\ncusto de partida = custo · 4^k\nretorno = retorno_base · (1 − (8 − s) · 0,05)            não sobe com o circuito\nchance = chance_base − 0,0925·a + 0,05·s − penalidades de gás\nrendimento = 1 − 0,05·s − penalidades de gás\npenalidade de gás = 1 − exp(−(30 · (guardado/necessário − 1))²)' if pt else
                 'duration = max(T · 2^−a · 0.97^(c − r) · 2^−k, 1)          r = program minimum compression\nstartup cost = cost · 4^k\nreturn = base return · (1 − (8 − s) · 0.05)                does not scale with the circuit\nchance = base chance − 0.0925·a + 0.05·s − gas penalties\nyield = 1 − 0.05·s − gas penalties\ngas penalty = 1 − exp(−(30 · (stored/required − 1))²)') + '\n```\n')
    a(table(['a / s', 'Chance (Overworld)', 'Rendimento' if pt else 'Yield', 'Tempo' if pt else 'Time'],
            [(f'{x} / {y}', f'{n(max(0, min(1, 1 - 0.0925 * x + 0.05 * y)) * 100, lang)}%', f'{n((1 - 0.05 * y) * 100, lang)}%', f'÷{2 ** x}') for x, y in ((0, 0), (2, 2), (4, 4), (6, 6), (8, 8), (8, 0), (0, 8))]))
    a(('O gás em excesso também reduz chance e rendimento: guardar 10% a mais já custa ' + n((1 - math.exp(-(30 * 0.1) ** 2)) * 100, lang) + '% em cada gás. Entregue a quantidade exata.\n') if pt else
      ('Excess gas also reduces chance and yield: storing 10% more already costs ' + n((1 - math.exp(-(30 * 0.1) ** 2)) * 100, lang) + '% per gas. Deliver the exact amount.\n'))
    a('## ' + ('Falha e pity' if pt else 'Failure and pity') + '\n')
    a(('- A falha também devolve o retorno de EU e gera SpaceTime: `chance · 14400 · 2^(tier + 1)` mB.\n'
       '- Falhas seguidas **nas mesmas condições** acumulam pity: soma `(1 − chance) · chance` a cada falha. Mudar campos ou circuito zera.\n'
       '- O resultado é sorteado na partida e salvo: quebrar ou recarregar o mundo não muda o resultado.\n') if pt else
      ('- A failure still returns the EU and produces SpaceTime: `chance · 14400 · 2^(tier + 1)` mB.\n'
       '- Consecutive failures **under the same conditions** build pity: `(1 − chance) · chance` per failure. Changing fields or circuit resets it.\n'
       '- The result is rolled at startup and saved: breaking the controller or reloading does not change it.\n'))
    a('## ' + ('Dicas' if pt else 'Tips') + '\n')
    a(('- O controlador consome **todo** o hidrogênio e hélio guardados na partida, inclusive o excesso.\n- O retorno chega pela rede Nexus em parcelas; a perda da rede aparece separada na GUI.\n- Saída cheia não perde nada: o ciclo espera.\n') if pt else
      ('- The controller consumes **all** stored hydrogen and helium at startup, excess included.\n- The return arrives through the Nexus network in parts; network loss is shown separately.\n- A full output never loses anything: the cycle waits.\n'))
    return '\n'.join(L)


SIMPLE = {
    'bec': ('Condensado de Bose-Einstein', 'Bose-Einstein Condensate', 'bec_generator', [
        ('Rede de condensado', 'Condensate network',
         'Cinco multiblocos ligados por **conduítes de BEC** (pinte para separar redes). O condensado é um recurso de rede, como energia: não fica em hatches.',
         'Five multiblocks linked by **BEC conduits** (dye them to split networks). Condensate is a network resource, like energy: it does not sit in hatches.'),
        ('Máquinas', 'Machines', None, None),
        ('Fabricação passo a passo', 'Step-by-step crafting',
         'O **Nó de Teleporte** fabrica receitas de Montagem com Condensado com os próprios barramentos. Cada slot de item pede um tier de nanite por vez; nanites extras aceleram linearmente; '
         'nanites de tier maior atrasam em `2^(fornecido − exigido)`. O condensado pode chegar a qualquer momento antes do fim; faltando no fim, a receita falha.',
         'The **Teleportation Node** crafts Condensate Assembly recipes with its own buses. Each item slot asks for one nanite tier at a time; extra nanites speed it up linearly; '
         'higher-tier nanites slow it by `2^(supplied − required)`. Condensate may arrive any time before the end; if it is missing at the end, the recipe fails.'),
        ('Armazenamento', 'Storage',
         'No **Campo de Contenção**, 1 de força guarda 1 mB e custa 1 EU/t. Acima da capacidade, mantém 9/10 de cada condensado por segundo. **Sem energia ou desligado, destrói tudo.**',
         'In the **Containment Field**, 1 strength stores 1 mB and costs 1 EU/t. Above capacity it keeps 9/10 of each condensate per second. **Without power or when off, it destroys everything.**'),
    ], [('Aparato de Emaranhamento', 'Entanglement Apparatus', 'gera condensado a partir de metais fundidos; paralelos até o EU/t disponível', 'makes condensate from molten metals; parallels up to the available EU/t'),
        ('Campo de Contenção', 'Containment Field', 'guarda condensado (seção abaixo)', 'stores condensate (section below)'),
        ('Portão de Maxwell', 'Maxwell Gate', 'deixa o condensado passar em um sentido, com filtros; 1A UIV ativo', 'lets condensate flow one way, with filters; 1A UIV while active'),
        ('Matriz de Observação', 'Observation Array', 'alimenta os nós por linha de visão com nanites, EU e condensado; até 30.720 nanites', 'feeds the nodes by line of sight with nanites, EU and condensate; up to 30,720 nanites'),
        ('Nó de Teleporte', 'Teleportation Node', 'fabrica as receitas (seção abaixo)', 'crafts the recipes (section below)')]),
    'space-elevator': ('Elevador Espacial', 'Space Elevator', 'space_elevator', [
        ('Funcionamento', 'How it works',
         'O elevador só alimenta módulos acima de ZPM, com computação (`128 · (tier − ZPM)` CWU/t) e **256 Nanotube Spools** colocados pelo barramento de entrada. Até 12 módulos.',
         'The elevator only powers modules above ZPM, with computation (`128 · (tier − ZPM)` CWU/t) and **256 Nanotube Spools** fed through its input bus. Up to 12 modules.'),
        ('Power Modules', 'Power Modules',
         'O MK (I–V) dos Power Modules define o paralelo de todos os módulos: `4^(MK − 1)`, e quais receitas do Módulo de Montagem podem rodar. Todos precisam ser do mesmo MK.',
         'The MK (I–V) of the Power Modules sets every module\'s parallel: `4^(MK − 1)`, and which Assembler Module recipes may run. All must share the same MK.'),
        ('Módulos', 'Modules',
         '**Montagem:** monta peças em órbita. **Coleta de Recursos:** drones minerando 20 misturas de asteroide e coletando 11 gases, com drones MK I–VI e combustível de foguete.',
         '**Assembler:** builds parts in orbit. **Resource Collection:** drones mining 20 asteroid ore mixes and collecting 11 gases, with MK I–VI drones and rocket fuel.'),
    ], None),
    'nano-forge': ('Nano Forge', 'Nano Forge', 'nano_forge', [
        ('Tiers', 'Tiers',
         'A nanita num barramento de entrada define o tier e **nunca é consumida**: Carbono T1, Neutrônio T2, Transcendente T3, MagMatter T4. Cada tier muda a estrutura. Overclock perfeito em receitas de tier menor.',
         'The nanite in an input bus sets the tier and **is never consumed**: Carbon T1, Neutronium T2, Transcendent T3, MagMatter T4. Each tier changes the structure. Perfect overclock on lower-tier recipes.'),
        ('Tier 4: MagMatter', 'Tier 4: MagMatter',
         'Com uma nanita igual à saída da receita no barramento, a forja drena **todo** o MagMatter fundido dos hatches. Paralelo = `MagMatter / (288 / 2^(4 − tier da receita))`; duração × `0,9999^paralelo`.',
         'With a nanite equal to the recipe output in the bus, the forge drains **all** molten MagMatter in the hatches. Parallel = `MagMatter / (288 / 2^(4 − recipe tier))`; duration × `0.9999^parallel`.'),
    ], None),
    'dyson-sphere': ('Esfera de Dyson', 'Dyson Sphere', 'dyson_sphere_launch_silo', [
        ('Ciclo', 'Cycle',
         'O **Silo de Lançamento** põe módulos do enxame na órbita do planeta onde está (só na superfície). A **Estação Receptora** converte o enxame em laser, com computação e hélio líquido.',
         'The **Launch Silo** puts swarm modules in orbit of its planet (surface only). The **Receiving Station** turns the swarm into laser power, with computation and liquid helium.'),
        ('Fórmulas', 'Formulas',
         '`EU/t = V[MAX] · módulos · (50 − max(0, dano − 60)) / 50`. Cada ciclo da estação soma 1 de dano; acima de 99 o enxame perde um módulo. Um lançamento com dano acima de 60 **repara** o enxame em vez de somar módulo. Máximo de 100.000 módulos por planeta.',
         '`EU/t = V[MAX] · modules · (50 − max(0, damage − 60)) / 50`. Each station cycle adds 1 damage; above 99 the swarm loses a module. A launch with damage above 60 **repairs** the swarm instead of adding a module. Up to 100,000 modules per planet.'),
    ], None),
    'item-effects': ('Efeitos de item', 'Item effects', None, [
        ('O que são', 'What they are',
         'Halo, borda brilhante e os shaders cosmic, eternal e unstable nos ícones dos materiais do GTNA. São do próprio GTNA desde a 0.5.6; o RenderBlender não é mais necessário.',
         'Halo, glow edge and the cosmic, eternal and unstable shaders on GTNA material icons. They are GTNA\'s own since 0.5.6; RenderBlender is no longer needed.'),
        ('Configuração', 'Configuration',
         'Em `config/gtna.json`, seção client: `itemHalo`, `itemGlowEdge`, `itemShaderEffects` e `itemEffectSpeed` (0–400%).',
         'In `config/gtna.json`, client section: `itemHalo`, `itemGlowEdge`, `itemShaderEffects` and `itemEffectSpeed` (0–400%).'),
        ('KubeJS', 'KubeJS',
         'Em `kubejs/client_scripts`: `GTNAClientEvents.itemEffects(event => { event.material(\'gtna:advanced_nitinol\').halo(0xFF66CCFF, 8).pulse(true) })`. Veja a página da API KubeJS.',
         'In `kubejs/client_scripts`: `GTNAClientEvents.itemEffects(event => { event.material(\'gtna:advanced_nitinol\').halo(0xFF66CCFF, 8).pulse(true) })`. See the KubeJS API page.'),
    ], None),
}


def simple_page(key, lang):
    pt = lang == 'pt'; tpt, ten, mid, secs, machines = SIMPLE[key]; L = [f'# {tpt if pt else ten}\n']
    if mid: L.append(f'![](../../assets/machines/{mid}.webp){{ loading=lazy }}\n')
    for h_pt, h_en, b_pt, b_en in secs:
        L.append(f'## {h_pt if pt else h_en}\n')
        if b_pt is None:
            L.append(table(['Máquina' if pt else 'Machine', 'Função' if pt else 'Role'], [(m[0] if pt else m[1], m[2] if pt else m[3]) for m in machines]))
        else: L.append((b_pt if pt else b_en) + '\n')
    return '\n'.join(L)


def main_all():
    main()
    for lang, suffix in (('pt', '.md'), ('en', '.en.md')):
        open(os.path.join(OUT, 'eye-of-harmony' + suffix), 'w', encoding='utf-8').write(eye_of_harmony(lang))
        for key in SIMPLE: open(os.path.join(OUT, key + suffix), 'w', encoding='utf-8').write(simple_page(key, lang))
    print('eye-of-harmony', *SIMPLE)


if __name__ == '__main__':
    main_all()
