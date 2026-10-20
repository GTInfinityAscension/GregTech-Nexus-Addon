"""Public roadmap page: progress of the ports and of the original multiblocks.

    python3 tools/wiki/roadmap_page.py   -> docs/roadmap/index.md (English), index.pt.md, index.zh.md

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

ORIGINALS = [  # (en, pt, zh) name, tier, (en, pt, zh) stage, spec page (Portuguese)
    (('Pressurized Water Reactor', 'Reator de Água Pressurizada', '压水反应堆'), 'IV',
     ('design done, implementation starting', 'design fechado, implementação começando', '设计完成，开始实现'), 'design/reator-pwr.md'),
    (('Kinetic Orbital Lance', 'Lança Cinética Orbital', '动能轨道长矛'), 'UEV', None, 'design/lanca-cinetica-orbital.md'),
    (('Dimensional Rift Gate', 'Portão de Fenda Dimensional', '维度裂隙之门'), 'UIV', None, 'design/portao-de-fenda.md'),
    (('Antimatter Collider Ring', 'Anel Colisor de Antimatéria', '反物质对撞环'), 'UIV', None, 'design/anel-colisor.md'),
    (('Stellar Containment Chamber', 'Câmara de Contenção Estelar', '恒星约束舱'), 'MAX', None, 'design/camara-estelar.md'),
]
IN_GAME = ('in game, under test (WIP)', 'no jogo, em teste (WIP)', '已在游戏中，测试中（WIP）')
PHASES = {  # roadmap section number -> phase title (en, pt, zh)
    '3.1': ('Phase A: required, and mechanics of existing endgame', 'Fase A: necessário e mecânicas do endgame existente', 'A 阶段：必需项与现有终局机制'),
    '3.2': ('Phase B: cheap and high value (GTO/GTL, few missing blocks)', 'Fase B: barato e de alto valor (GTO/GTL, poucos blocos faltando)', 'B 阶段：成本低、价值高（GTO/GTL，缺少的方块很少）'),
    '3.3': ('Phase C: medium (GTO, 2–5 missing blocks or own class)', 'Fase C: médio (GTO, 2–5 blocos faltando ou classe própria)', 'C 阶段：中等（GTO，缺 2–5 个方块或需要独立类）'),
    '3.4': ('Phase D: expensive or large systems (GTO)', 'Fase D: caro / sistemas grandes (GTO)', 'D 阶段：昂贵或大型系统（GTO）'),
    '3.5': ('Phase E: GTNH 1.7.10 with no GTO/GTL equivalent', 'Fase E: GTNH 1.7.10 sem equivalente no GTO/GTL', 'E 阶段：GTO/GTL 中没有对应的 GTNH 1.7.10 机器'),
    '3.6': ('Phase F: TST, GTNL and 123Tech with no GTO/GTL version', 'Fase F: TST, GTNL e 123Tech sem versão no GTO/GTL', 'F 阶段：GTO/GTL 中没有版本的 TST、GTNL 与 123Tech 机器'),
    '3.7': ('Phase G: GTLAdditions', 'Fase G: GTLAdditions', 'G 阶段：GTLAdditions'),
}
TXT = {
    'intro': ('GTNA currently registers **{n} multiblocks**. This page shows the progress of the requested ports and of the original multiblocks. It is generated from the project working documents, so it follows the code.',
              'O GTNA tem hoje **{n} multiblocos** registrados. Esta página mostra o andamento dos ports pedidos e dos multiblocos originais. Ela é gerada a partir dos documentos de trabalho do projeto, então acompanha o código.',
              'GTNA 目前注册了 **{n} 个多方块**。本页展示所需移植项目以及原创多方块的进度，由项目工作文档生成，与代码保持同步。'),
    'overall': ('Overall port progress', 'Progresso geral dos ports', '移植总进度'),
    'phase': ('Phase', 'Fase', '阶段'), 'progress': ('Progress', 'Progresso', '进度'), 'done': ('Done', 'Feitos', '完成'),
    'orig': ('Original multiblocks (in development)', 'Multiblocos originais (em desenvolvimento)', '原创多方块（开发中）'),
    'orig_txt': ('Machines made for GTNA, with no equivalent in another mod. Each has a spec sheet (in Portuguese) with formulas, its own progression and an animated render.',
                 'Máquinas criadas para o GTNA, sem equivalente em outro mod. Cada uma tem ficha técnica com fórmulas, progressão própria e render animado.',
                 '为 GTNA 设计、其他模组中没有对应机器的多方块。每台都有一份技术说明（葡萄牙语），包含公式、独立进度和动画渲染。'),
    'machine': ('Machine', 'Máquina', '机器'), 'status': ('Status', 'Estado', '状态'), 'spec': ('Spec', 'Ficha', '说明'), 'open': ('open', 'abrir', '打开'),
    'source': ('Source', 'Fonte', '来源'), 'ported': ('ported', 'portado', '已移植'), 'pending': ('pending', 'pendente', '待移植'),
    'how': ('How it works', 'Como funciona', '规则'),
    'how_txt': ('- Only machines the author asked for are ported, from the named source (GTO, GTL, GTNL, TST, GTNH).\n- Each port brings its original structure, mechanics and textures, with KubeJS support.\n- Default recipes are a baseline; balance belongs to the modpack.',
                '- Só se porta o que o autor pediu, da fonte indicada (GTO, GTL, GTNL, TST, GTNH).\n- Cada port traz estrutura, mecânica e texturas originais, com suporte a KubeJS.\n- As receitas padrão são uma base; o balanceamento fica com o modpack.',
                '- 只移植作者指定的机器，并来自指定的来源（GTO、GTL、GTNL、TST、GTNH）。\n- 每个移植都保留原始结构、机制和材质，并支持 KubeJS。\n- 默认配方只是基准；平衡由整合包决定。'),
}
LANGS = (('en', 0, '.md'), ('pt', 1, '.pt.md'), ('zh', 2, '.zh.md'))


def bar(done, total, width=20):
    k = round(width * done / total) if total else 0
    return '█' * k + '░' * (width - k)


def page(i):
    T = lambda key: TXT[key][i]
    total = sum(len(r) for _, _, r in phases); done = sum(sum(d for *_, d in r) for _, _, r in phases)
    title = lambda code, raw: PHASES[code][i] if code in PHASES else raw
    L = ['# Roadmap\n', T('intro').format(n=n_machines) + '\n']
    L.append(f'## {T("overall")}\n')
    L.append(f'`{bar(done, total, 30)}` **{done}/{total}** ({round(100 * done / total)}%)\n')
    L.append(f'| {T("phase")} | {T("progress")} | {T("done")} |\n|---|---|---|')
    for code, raw, rows in phases:
        d = sum(x for *_, x in rows)
        L.append(f'| {title(code, raw)} | `{bar(d, len(rows))}` | {d}/{len(rows)} |')
    L.append('')
    L.append(f'## {T("orig")}\n')
    L.append(T('orig_txt') + '\n')
    L.append(f'| {T("machine")} | Tier | {T("status")} | {T("spec")} |\n|---|---|---|---|')
    for names, tier, stage, spec in ORIGINALS:
        L.append(f'| {names[i]} | {tier} | :material-progress-wrench: {(stage or IN_GAME)[i]} | [{T("open")}]({spec}) |')
    L.append('')
    for code, raw, rows in phases:
        d = sum(x for *_, x in rows)
        L.append(f'??? {"success" if d == len(rows) else "note"} "{title(code, raw)} — {d}/{len(rows)}"')
        L.append(f'    | {T("machine")} | {T("source")} | {T("status")} |')
        L.append('    |---|---|---|')
        for name, src, ok in rows:
            L.append(f'    | {name} | {src} | {"✅ " + T("ported") if ok else "⏳ " + T("pending")} |')
        L.append('')
    L.append(f'## {T("how")}\n')
    L.append(T('how_txt') + '\n')
    return '\n'.join(L)


for lang, i, suf in LANGS:
    open(os.path.join(ROOT, 'docs/roadmap/index' + suf), 'w', encoding='utf-8').write(page(i))
for old in ('index.en.md', 'index.es.md'):
    path = os.path.join(ROOT, 'docs/roadmap', old)
    if os.path.exists(path): os.remove(path)
print('roadmap', sum(len(r) for _, _, r in phases))
