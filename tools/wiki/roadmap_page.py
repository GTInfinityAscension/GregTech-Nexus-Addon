"""Public roadmap page: progress of the ports and of the original multiblocks.

    python3 tools/wiki/roadmap_page.py   -> docs/roadmap/index.md, index.en.md

Sources: docs/roadmap/ROADMAP-multiblocos.md (phases, ✅ = done), docs/roadmap/lista-do-autor.md ("Portados"),
build/wiki/multiblocks.json (registered machines). A roadmap row counts as done when it has ✅ or its machine is in
the author's ported list.
"""
import json, os, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
RM = open(os.path.join(ROOT, 'docs/roadmap/ROADMAP-multiblocos.md'), encoding='utf-8').read()
LA = open(os.path.join(ROOT, 'docs/roadmap/lista-do-autor.md'), encoding='utf-8').read()
DUMP = os.path.join(ROOT, 'build/wiki/multiblocks.json')


def norm(s): return re.sub(r'[^a-z0-9]', '', s.lower())


ported = set()
sec = LA.split('## Portados', 1)[1].split('\n## ', 1)[0]
for line in sec.splitlines():
    if line.startswith('| ') and not line.startswith('| Máquina') and not line.startswith('|---'):
        for name in line.split('|')[1].split('/'):
            ported.add(norm(name.strip()))

registered = set()
if os.path.exists(DUMP):
    lang = json.load(open(os.path.join(ROOT, 'src/generated/resources/assets/gtna/lang/en_us.json')))
    for m in json.load(open(DUMP)):
        registered.add(norm(m['id']))
        registered.add(norm(lang.get('block.gtna.' + m['id'], '')))
registered.discard('')
# Done in the changelog / ledger although named differently in the roadmap rows.
EXTRA_DONE = {norm(x) for x in ('Multiblocos BEC', 'Nano Forge tier 4', 'Space Elevator + módulos', 'Dyson Sphere Launch Silo + Receiving Station')}


def is_registered(name):
    k = norm(name.split('(')[0])
    return k in EXTRA_DONE or k in registered


phases = []
for m in re.finditer(r'^### (3\.\d) (.+?)\n(.*?)(?=^### |^## |\Z)', RM, re.S | re.M):
    rows = []
    for line in m.group(3).splitlines():
        if not line.startswith('| ') or line.startswith('| Máquina') or line.startswith('|---'): continue
        cells = [c.strip() for c in line.strip('|').split('|')]
        name = re.sub(r'\*\*|\(G-\d+\)', '', cells[0]).replace('✅', '').strip()
        done = '✅' in cells[0] or any(norm(p) in ported for p in name.split('/')) or norm(name.split('(')[0]) in ported or is_registered(name)
        rows.append((name, cells[1] if len(cells) > 1 else '', done))
    if rows: phases.append((m.group(1), m.group(2).strip(), rows))

n_machines = len(json.load(open(DUMP))) if os.path.exists(DUMP) else 0

ORIGINALS = [  # name pt, name en, tier, stage pt, stage en, spec page
    ('Reator de Água Pressurizada', 'Pressurized Water Reactor', 'IV', 'design fechado, implementação começando', 'design done, implementation starting', 'design/reator-pwr.md'),
    ('Lança Cinética Orbital', 'Kinetic Orbital Lance', 'UEV', 'em implementação', 'in implementation', 'design/lanca-cinetica-orbital.md'),
    ('Portão de Fenda Dimensional', 'Dimensional Rift Gate', 'UIV', 'em implementação', 'in implementation', 'design/portao-de-fenda.md'),
    ('Anel Colisor de Antimatéria', 'Antimatter Collider Ring', 'UIV', 'em implementação', 'in implementation', 'design/anel-colisor.md'),
    ('Câmara de Contenção Estelar', 'Stellar Containment Chamber', 'MAX', 'em implementação', 'in implementation', 'design/camara-estelar.md'),
]


def bar(done, total, width=20):
    k = round(width * done / total) if total else 0
    return '█' * k + '░' * (width - k)


def page(lang):
    pt = lang == 'pt'; T = lambda a, b: a if pt else b
    total = sum(len(r) for _, _, r in phases); done = sum(sum(d for *_, d in r) for _, _, r in phases)
    L = [f'# Roadmap\n', T(f'O GTNA tem hoje **{n_machines} multiblocos** registrados. Esta página mostra o andamento dos ports pedidos e dos multiblocos originais. '
                           'Ela é gerada a partir dos documentos de trabalho do projeto, então acompanha o que está no código.\n',
                           f'GTNA currently registers **{n_machines} multiblocks**. This page shows the progress of the requested ports and of the original multiblocks. '
                           'It is generated from the project working documents, so it follows the code.\n')]
    L.append(f'## {T("Progresso geral dos ports", "Overall port progress")}\n')
    L.append(f'`{bar(done, total, 30)}` **{done}/{total}** ({round(100 * done / total)}%)\n')
    L.append('| ' + T('Fase', 'Phase') + ' | ' + T('Progresso', 'Progress') + ' | ' + T('Feitos', 'Done') + ' |\n|---|---|---|')
    for code, title, rows in phases:
        d = sum(x for *_, x in rows)
        L.append(f'| {code} {title} | `{bar(d, len(rows))}` | {d}/{len(rows)} |')
    L.append('')
    L.append(f'## {T("Multiblocos originais (em desenvolvimento)", "Original multiblocks (in development)")}\n')
    L.append(T('Máquinas criadas para o GTNA, sem equivalente em outro mod. Cada uma tem ficha técnica com fórmulas, progressão própria e render animado.\n',
               'Machines made for GTNA, with no equivalent in another mod. Each has a spec sheet with formulas, its own progression and an animated render.\n'))
    L.append('| ' + T('Máquina', 'Machine') + ' | Tier | ' + T('Estado', 'Status') + ' | ' + T('Ficha', 'Spec') + ' |\n|---|---|---|---|')
    for npt, nen, tier, spt, sen, spec in ORIGINALS:
        L.append(f'| {npt if pt else nen} | {tier} | :material-progress-wrench: {spt if pt else sen} | [{T("abrir", "open")}]({spec}) |')
    L.append('')
    for code, title, rows in phases:
        d = sum(x for *_, x in rows)
        L.append(f'??? {"success" if d == len(rows) else "note"} "{code} {title} — {d}/{len(rows)}"')
        L.append('    | ' + T('Máquina', 'Machine') + ' | ' + T('Fonte', 'Source') + ' | ' + T('Estado', 'Status') + ' |')
        L.append('    |---|---|---|')
        for name, src, ok in rows:
            L.append(f'    | {name} | {src} | {"✅ " + T("portado", "ported") if ok else "⏳ " + T("pendente", "pending")} |')
        L.append('')
    L.append(f'## {T("Como funciona", "How it works")}\n')
    L.append(T('- Só se porta o que o autor pediu, da fonte indicada (GTO, GTL, GTNL, TST, GTNH).\n- Cada port traz estrutura, mecânica e texturas originais, com suporte a KubeJS.\n- As receitas padrão são uma base; o balanço fica com o modpack.\n',
               '- Only machines the author asked for are ported, from the named source (GTO, GTL, GTNL, TST, GTNH).\n- Each port brings its original structure, mechanics and textures, with KubeJS support.\n- Default recipes are a baseline; balance belongs to the modpack.\n'))
    return '\n'.join(L)


for lang, suf in (('pt', '.md'), ('en', '.en.md')):
    open(os.path.join(ROOT, 'docs/roadmap/index' + suf), 'w', encoding='utf-8').write(page(lang))
es = os.path.join(ROOT, 'docs/roadmap/index.es.md')
if os.path.exists(es): os.remove(es)
print('roadmap', sum(len(r) for _, _, r in phases))
