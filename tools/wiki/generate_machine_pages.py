"""Generate the multiblock catalog of the wiki from the datagen dump.

    ./gradlew runData --offline          # writes build/wiki/multiblocks.json
    python3 tools/wiki/generate_machine_pages.py

Writes docs/gameplay/machines/catalog/<id>.md (English), <id>.pt.md and <id>.zh.md, an index per language
grouped by category, and an isometric render per machine in docs/assets/machines/. Names and descriptions come
from the mod's lang files (en_us, pt_br, zh_cn) and the source mod from GTNASources.java. Pages here are
regenerated: write guides under docs/gameplay/ instead and link to the catalog from them.
"""
import glob
import json
import os
import re
import sys
import zipfile
from collections import Counter

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iso  # noqa: E402
import zh_punct  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DUMP = os.path.join(ROOT, 'build/wiki/multiblocks.json')
OUT = os.path.join(ROOT, 'docs/gameplay/machines/catalog')
IMG = os.path.join(ROOT, 'docs/assets/machines')
CACHE = os.path.join(ROOT, 'build/wiki/textures')
GRADLE = os.path.expanduser('~/.gradle/caches')

SKIP = {'minecraft:sponge'}  # GTCEu previews fill 'any block' positions with sponge
TIERS = ['ulv', 'lv', 'mv', 'hv', 'ev', 'iv', 'luv', 'zpm', 'uv', 'uhv', 'uev', 'uiv', 'uxv', 'opv', 'max']


def find_jar(pattern):
    hits = [p for p in glob.glob(os.path.join(GRADLE, '**', pattern), recursive=True) if 'sources' not in p]
    if not hits: raise SystemExit('missing jar ' + pattern)
    return hits[0]


class Assets:
    """Reads models/textures/lang from GTNA's resource folders, the GTCEu jar and the vanilla jar."""

    def __init__(self):
        self.dirs = [os.path.join(ROOT, 'src/main/resources'), os.path.join(ROOT, 'src/generated/resources')]
        self.zips = [zipfile.ZipFile(find_jar('gtceu-1.20.1-7.5.3-slim.jar')),
                     zipfile.ZipFile(find_jar('client-extra.jar'))]

    def read(self, path):
        for d in self.dirs:
            p = os.path.join(d, path)
            if os.path.exists(p): return open(p, 'rb').read()
        for z in self.zips:
            try: return z.read(path)
            except KeyError: pass
        return None

    def json(self, path):
        raw = self.read(path)
        return json.loads(raw.decode('utf-8-sig')) if raw else None

    def lang(self, ns, code):
        merged = {}
        for path in (f'assets/{ns}/lang/{code}.json',):
            for d in self.dirs:
                p = os.path.join(d, path)
                if os.path.exists(p): merged.update(json.loads(open(p, encoding='utf-8-sig').read()))
            for z in self.zips:
                try: merged.update(json.loads(z.read(path).decode('utf-8-sig')))
                except KeyError: pass
        return merged


A = Assets()
LANG = {code: {**A.lang('minecraft', code), **A.lang('gtceu', code), **A.lang('gtna', code)} for code in ('en_us', 'pt_br', 'zh_cn')}
for code in LANG: LANG[code] = {**LANG['en_us'], **LANG[code]}


def text(key, code, fallback=None):
    v = LANG[code].get(key)
    return strip(v) if v else fallback


def strip(s):
    return re.sub(r'§.', '', s)


def block_name(block_id, code):
    ns, path = block_id.split(':')
    name = text(f'block.{ns}.{path}', code)
    if name: return name
    for prefix in ('frame', 'block'):  # material blocks are named at runtime from the material and a tag prefix
        mat = path[:-len(prefix) - 1] if path.endswith('_' + prefix) else None
        fmt = text(f'tagprefix.{prefix}', code)
        mname = mat and (text(f'material.{ns}.{mat}', code) or text(f'material.gtceu.{mat}', code) or text(f'material.gtna.{mat}', code))
        if fmt and mname: return fmt.replace('%s', mname)
    return path.replace('_', ' ').title()


def model_texture(block_id):
    """Texture path (namespace:path) for a block, following blockstate -> model -> parents."""
    ns, path = block_id.split(':')
    model = None
    bs = A.json(f'assets/{ns}/blockstates/{path}.json')
    if bs:
        variants = bs.get('variants') or {}
        first = next(iter(variants.values()), None) if variants else None
        if isinstance(first, list): first = first[0]
        if first: model = first.get('model')
        if not model and bs.get('multipart'):
            apply = bs['multipart'][0]['apply']
            model = (apply[0] if isinstance(apply, list) else apply).get('model')
    model = model or f'{ns}:block/{path}'
    textures = {}
    for _ in range(8):
        mns, mpath = (model.split(':') + [''])[:2] if ':' in model else ('minecraft', model)
        m = A.json(f'assets/{mns}/models/{mpath}.json')
        if not m: break
        for k, v in (m.get('textures') or {}).items(): textures.setdefault(k, v)
        if 'parent' not in m: break
        model = m['parent']
    for key in ('all', 'side', 'texture', 'end', 'top', 'particle', 'layer0', 'bottom', 'overlay'):
        v = textures.get(key)
        for _ in range(6):
            if v and v.startswith('#'): v = textures.get(v[1:])
        if v and not v.startswith('#'): return v if ':' in v else 'minecraft:' + v
    return None


TEX_CACHE = {}


def texture_file(block_id):
    """Local PNG for a block, or a flat colour tile when no texture can be found."""
    if block_id in TEX_CACHE: return TEX_CACHE[block_id]
    os.makedirs(CACHE, exist_ok=True)
    ns, path = block_id.split(':')
    tex = None
    tier = path.split('_')[0]
    if tier in TIERS and any(w in path for w in ('hatch', 'bus', 'muffler')):
        tex = f'gtceu:block/casings/voltage/{tier}/side'
    tex = tex or model_texture(block_id)
    raw = None
    if tex:
        tns, tpath = tex.split(':')
        raw = A.read(f'assets/{tns}/textures/{tpath}.png')
    if not raw:  # GTNA casings without a model file: look the texture up by name
        hits = glob.glob(os.path.join(ROOT, f'src/main/resources/assets/{ns}/textures/block/**/{path}.png'), recursive=True)
        if hits: raw = open(hits[0], 'rb').read()
    out = os.path.join(CACHE, block_id.replace(':', '__') + '.png')
    if raw:
        open(out, 'wb').write(raw)
        im = Image.open(out).convert('RGBA')
        im = im.crop((0, 0, im.width, im.width)).resize((16, 16), Image.NEAREST)
        if 'frame' in path:  # frames are tinted material models: draw them as a hollow box
            im = im.convert('L').convert('RGBA')
        im.save(out)
    else:
        colour = (200, 120, 40, 255) if ns == 'gtna' and 'casing' not in path else (110, 116, 126, 255)
        Image.new('RGBA', (16, 16), colour).save(out)
    TEX_CACHE[block_id] = out
    return out


def render(machine, path):
    shape = machine['shape']; pal = shape['palette']; vox = []
    for x, plane in enumerate(shape['blocks']):
        for y, row in enumerate(plane):
            for z, cell in enumerate(row):
                if cell >= 0 and pal[cell] not in SKIP: vox.append((x, y, z, texture_file(pal[cell])))
    if not vox: return False
    size = max(max(v[i] for v in vox) for i in range(3)) + 1
    s = 8 if size <= 12 else 5 if size <= 25 else 3 if size <= 60 else 2
    tmp = path + '.png'
    iso.render(vox, tmp, s, bg=(20, 22, 28))
    im = Image.open(tmp)
    bb = im.convert('L').point(lambda v: 255 if v > 30 else 0).getbbox()
    if bb: im = im.crop((max(0, bb[0] - 12), max(0, bb[1] - 12), bb[2] + 12, bb[3] + 12))
    if max(im.size) < 450:
        k = 450 // max(im.size) + 1
        im = im.resize((im.width * k, im.height * k), Image.NEAREST)
    im.thumbnail((900, 900))
    im.save(path, quality=82)
    os.remove(tmp)
    return True




LANGS = (('en_us', '.md'), ('pt_br', '.pt.md'), ('zh_cn', '.zh.md'))

# EN: Categories are editorial, not in the mod code; steam machines are found by their steam hatches.
# PT: As categorias são editoriais, não estão no código; as máquinas a vapor são achadas pelos hatches de vapor.
# ZH: 分类是编辑性的,不在模组代码中;蒸汽机器通过其蒸汽仓识别。
PRIMITIVE = {'brick_kiln', 'hyper_pressure_reactor', 'compact_hyper_pressure_reactor', 'leap_forward_one_blast_furnace',
             'infernal_coke_oven', 'primitive_distillation_tower', 'primitive_stone_furnace', 'stone_superheater',
             'dimensionally_transcendent_dirt_forge'}
POWER = {'fuel_cell_generator', 'supercritical_steam_turbine'}
ENDGAME = {'eye_of_harmony', 'forge_of_gods', 'nano_forge', 'space_elevator', 'assembler_module', 'resource_collection_module',
           'dyson_sphere_launch_silo', 'dimensionally_transcendent_plasma_forge', 'hyperdimensional_plasma_fusion_core',
           'transcendent_plasma_mixer', 'star_ultimate_material_forge_factory'}
ORIGINALS = {'kinetic_orbital_lance', 'stellar_containment_chamber', 'antimatter_collider_ring', 'dimensional_rift_gate'}
NETWORK = {'me_storage', 'nexus_me_hypercore', 'nexus_molecular_forge', 'nexus_flux_matrix', 'data_center', 'supercomputing_center'}
DEV = {'duration_tester'}
CATEGORY_ORDER = ('steam', 'processing', 'power', 'network', 'endgame', 'originals', 'dev')


def category(m):
    mid = m['id']
    if mid in DEV: return 'dev'
    if mid in ORIGINALS: return 'originals'
    if mid in ENDGAME or mid.startswith(('godforge_', 'bec_')): return 'endgame'
    if m['generator'] or mid in POWER: return 'power'
    if mid in NETWORK: return 'network'
    if mid in PRIMITIVE or any('steam' in b for b in m['shape']['palette']): return 'steam'
    return 'processing'


def read_sources():
    src = open(os.path.join(ROOT, 'src/main/java/com/raishxn/gtna/common/data/GTNASources.java'), encoding='utf-8').read()
    consts = dict(re.findall(r'public static final String (\w+) = "(\w+)";', src))
    return {mid: consts.get(c, c.lower()) for mid, c in re.findall(r'Map\.entry\("(\w+)",\s*(\w+)\)', src)}


SOURCES = read_sources()
SOURCE_NAMES = {'gto': 'GregTech Odyssey', 'gtl': 'GregTech Leisure', 'gtlcore': 'GTLCore', 'gtlsupb': 'GTLSupb',
                'gtladditions': 'GTL Additions', 'gtnl': 'GT: Not Leisure', 'gtnh': 'GT: New Horizons',
                'tst': 'Twist Space Technology', 'gtoepp': 'GTO Extended Platform Presets',
                'gtneioreplugin': 'GTNEIOrePlugin', 'gtna': 'GTNA'}

L = {
    'en_us': dict(types='Recipe types', size='Size', blocks='Blocks', block='Block', qty='Qty', about='Description',
                  structure='Structure', kind='Machine type', cat='Category', source='Origin', original='GTNA original',
                  none='None', unknown='—', note='Generated from the mod code; the structure shown is the smallest variant.',
                  index='Multiblock catalog', col=('Machine', 'Type', 'Size', 'Origin'),
                  intro='All {n} GTNA multiblocks, generated from the mod code and its language files. Each page has a render, '
                        'the in-game description and the block list of the smallest valid structure. In game, JEI/EMI shows every '
                        'structure layer by layer and the hologram projector builds it.',
                  cats=dict(steam='Steam and primitive', processing='Electric processing', power='Power generation',
                            network='Energy, AE2 and computation', endgame='Endgame systems', originals='GTNA originals (WIP)',
                            dev='Developer tools')),
    'pt_br': dict(types='Tipos de receita', size='Tamanho', blocks='Blocos', block='Bloco', qty='Qtd.', about='Descrição',
                  structure='Estrutura', kind='Tipo de máquina', cat='Categoria', source='Origem', original='Original do GTNA',
                  none='Nenhum', unknown='—', note='Gerada a partir do código do mod; a estrutura mostrada é a menor variante.',
                  index='Catálogo de multiblocos', col=('Máquina', 'Tipo', 'Tamanho', 'Origem'),
                  intro='Todos os {n} multiblocos do GTNA, gerados a partir do código e dos arquivos de idioma do mod. Cada página '
                        'tem imagem, a descrição do jogo e a lista de blocos da menor estrutura válida. No jogo, o JEI/EMI mostra cada '
                        'estrutura camada por camada e o projetor holográfico a constrói.',
                  cats=dict(steam='Vapor e primitivos', processing='Processamento elétrico', power='Geração de energia',
                            network='Energia, AE2 e computação', endgame='Sistemas de fim de jogo', originals='Originais do GTNA (em teste)',
                            dev='Ferramentas de desenvolvimento')),
    'zh_cn': dict(types='配方类型', size='尺寸', blocks='方块数', block='方块', qty='数量', about='说明',
                  structure='结构', kind='机器类型', cat='分类', source='来源', original='GTNA 原创',
                  none='无', unknown='—', note='根据模组代码生成;所示结构为最小形态。',
                  index='多方块图鉴', col=('机器', '类型', '尺寸', '来源'),
                  intro='GTNA 全部 {n} 个多方块,由模组代码和语言文件生成。每页包含渲染图、游戏内说明以及最小有效结构的方块清单。'
                        '游戏中可在 JEI/EMI 逐层查看结构,并用全息投影仪自动搭建。',
                  cats=dict(steam='蒸汽与原始', processing='电力加工', power='发电', network='能量、AE2 与算力',
                            endgame='终局系统', originals='GTNA 原创(测试中)', dev='开发者工具')),
}


def recipe_type_name(rt, code):
    ns, path = rt.split(':')
    return text(f'{ns}.{path}', code) or text(f'gtceu.{path}', code) or path.replace('_', ' ').title()


def tooltip(mid, code):
    """(machine type, flavour line, prose, bullets) from the tooltip lang keys."""
    lines = []
    for i in range(48):
        line = text(f'gtna.machine.{mid}.tooltip.{i}', code)
        if line is None:
            if i > 2 and not lines: break
            continue
        if line.strip(): lines.append(line.strip())
    kind = flavour = None
    if lines and re.match(r'^[^:：]{2,24}[:：]', lines[0]):
        kind = re.split(r'[:：]', lines.pop(0), maxsplit=1)[1].strip()
    if lines and not lines[0].startswith(('▸', '•', '-', '*')) and lines[0][-1:] in '.!?。！？…' and len(lines[0]) < 120:
        flavour = lines.pop(0)
    lines = [ln for ln in lines if not re.match(r'^(Source|Fonte|来源)\s*[:：]', ln)]
    prose, bullets = [], []
    for line in lines:
        # EN: Tooltip lines wrap mid-sentence: join them into prose; marked or "Label:" lines become bullets.
        # PT: As linhas do tooltip quebram no meio da frase: viram prosa; linhas marcadas ou "Rótulo:" viram itens.
        # ZH: 提示行会在句中换行:合并为段落;带标记或"标签:"的行作为列表项。
        if line[0] in '▸•-*' or re.match(r'^[^.。:：]{1,40}[:：]', line): bullets.append(line.lstrip('▸•-* '))
        else: prose.append(line)
    sep = '' if code == 'zh_cn' else ' '
    return kind, flavour, sep.join(prose), bullets


def num(n, code):
    s = f'{n:,}'
    return s.replace(',', '.') if code == 'pt_br' else s


def page(m, code, has_img):
    t = L[code]; mid = m['id']
    name = text(f'block.gtna.{mid}', code, mid.replace('_', ' ').title())
    kind, flavour, prose, bullets = tooltip(mid, code)
    shape = m['shape']; pal = shape['palette']
    counts = Counter(pal[c] for plane in shape['blocks'] for row in plane for c in row if c >= 0 and pal[c] not in SKIP)
    dims = (len(shape['blocks']), len(shape['blocks'][0]), len(shape['blocks'][0][0]))
    types = ', '.join(recipe_type_name(r, code) for r in m['recipeTypes'] if r != 'gtceu:dummy') or t['none']
    src = SOURCES.get(mid)
    origin = t['original'] if src == 'gtna' else SOURCE_NAMES.get(src, t['unknown']) if src else t['unknown']
    cat = t['cats'][category(m)]
    out = [f'---\ntags:\n  - {cat}\n---\n\n', f'# {name}\n\n', f'<!-- {t["note"]} -->\n\n']
    if flavour: out.append(f'*{flavour}*\n\n')
    if has_img: out.append(f'![{name}](../../../assets/machines/{mid}.webp){{ loading=lazy }}\n\n')
    rows = [(t['kind'], kind)] if kind else []
    rows += [(t['cat'], cat), (t['types'], types), (t['size'], f'{dims[0]} × {dims[1]} × {dims[2]}'),
             (t['blocks'], num(sum(counts.values()), code)), (t['source'], origin)]
    out.append('| | |\n|---|---|\n' + ''.join(f'| **{k}** | {v} |\n' for k, v in rows))
    if prose or bullets:
        out.append(f'\n## {t["about"]}\n\n')
        if prose: out.append(prose + '\n\n')
        out.extend(f'- {line}\n' for line in bullets)
    out.append(f'\n## {t["structure"]}\n\n| {t["block"]} | {t["qty"]} |\n|---|---:|\n')
    out.extend(f'| {block_name(b, code)} | {num(n, code)} |\n' for b, n in counts.most_common())
    out.append(f'\n<small>{t["note"]}</small>\n')
    return dict(name=name, kind=kind or '', dims=dims, origin=origin, cat=category(m), md=''.join(out))


def main():
    machines = sorted(json.load(open(DUMP)), key=lambda m: m['id'])
    os.makedirs(OUT, exist_ok=True); os.makedirs(IMG, exist_ok=True)
    rows = {c: {k: [] for k in CATEGORY_ORDER} for c, _ in LANGS}
    for m in machines:
        if 'shape' not in m: continue
        img = os.path.join(IMG, m['id'] + '.webp')
        has_img = os.path.exists(img) if '--no-render' in sys.argv else render(m, img)
        for code, suffix in LANGS:
            p = page(m, code, has_img)
            open(os.path.join(OUT, m['id'] + suffix), 'w', encoding='utf-8').write(zh_punct.fix(p['md']) if code == 'zh_cn' else p['md'])
            d = p['dims']
            rows[code][p['cat']].append((p['name'], f'| [{p["name"]}]({m["id"]}.md) | {p["kind"]} | {d[0]}×{d[1]}×{d[2]} | {p["origin"]} |\n'))
        print(m['id'])
    for code, suffix in LANGS:
        t = L[code]; c = t['col']; total = sum(len(v) for v in rows[code].values())
        md = [f'# {t["index"]}\n\n{t["intro"].format(n=total)}\n\n']
        for k in CATEGORY_ORDER:
            if not rows[code][k]: continue
            md.append(f'## {t["cats"][k]} ({len(rows[code][k])}) {{#{k}}}\n\n| {c[0]} | {c[1]} | {c[2]} | {c[3]} |\n|---|---|---|---|\n')
            md.extend(r for _, r in sorted(rows[code][k], key=lambda x: x[0].lower()))
            md.append('\n')
        md = ''.join(md)
        open(os.path.join(OUT, 'index' + suffix), 'w', encoding='utf-8').write(zh_punct.fix(md) if code == 'zh_cn' else md)


if __name__ == '__main__':
    main()
