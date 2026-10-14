"""Generate the multiblock catalog of the wiki from the datagen dump.

    ./gradlew runData --offline          # writes build/wiki/multiblocks.json
    python3 tools/wiki/generate_machine_pages.py

Writes docs/gameplay/machines/catalog/<id>.md (pt) and <id>.en.md, an index for each language and an
isometric render per machine in docs/assets/machines/. Pages here are regenerated: edit the hand-written
pages under docs/gameplay/machines/ instead, and they get linked from the catalog.
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
LANG = {code: {**A.lang('minecraft', code), **A.lang('gtceu', code), **A.lang('gtna', code)} for code in ('en_us', 'pt_br')}
for code in LANG: LANG[code] = {**LANG['en_us'], **LANG[code]}


def text(key, code, fallback=None):
    v = LANG[code].get(key)
    return strip(v) if v else fallback


def strip(s):
    return re.sub(r'§.', '', s)


def block_name(block_id, code):
    ns, path = block_id.split(':')
    return text(f'block.{ns}.{path}', code) or path.replace('_', ' ').title()


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


HAND = {}  # machine id -> hand-written page path, relative to docs/gameplay/machines
for p in glob.glob(os.path.join(ROOT, 'docs/gameplay/machines/*/*.md')):
    if re.search(r'\.(en|es)\.md$', p) or '/catalog/' in p: continue
    HAND[os.path.basename(p)[:-3].replace('-', '_')] = os.path.relpath(p, os.path.join(ROOT, 'docs/gameplay/machines'))

L = {
    'pt_br': {'types': 'Tipos de receita', 'size': 'Tamanho', 'blocks': 'Blocos', 'block': 'Bloco', 'qty': 'Qtd.',
              'about': 'Descrição', 'structure': 'Estrutura', 'generator': 'Gerador', 'guide': 'Guia completo',
              'none': 'Nenhum', 'note': 'Página gerada a partir do código do mod; a estrutura é a menor variante.',
              'index': 'Catálogo de multiblocos', 'intro': 'Todos os {n} multiblocos do GTNA, gerados a partir do código. '
              'Os que têm guia escrito à mão estão marcados.', 'col': ('Máquina', 'Tipos de receita', 'Tamanho')},
    'en_us': {'types': 'Recipe types', 'size': 'Size', 'blocks': 'Blocks', 'block': 'Block', 'qty': 'Qty',
              'about': 'Description', 'structure': 'Structure', 'generator': 'Generator', 'guide': 'Full guide',
              'none': 'None', 'note': 'Generated from the mod code; the structure shown is the smallest variant.',
              'index': 'Multiblock catalog', 'intro': 'All {n} GTNA multiblocks, generated from the code. '
              'Machines with a hand-written guide are marked.', 'col': ('Machine', 'Recipe types', 'Size')},
}


def recipe_type_name(rt, code):
    ns, path = rt.split(':')
    return text(f'{ns}.{path}', code) or text(f'gtceu.{path}', code) or path.replace('_', ' ').title()


def page(machine, code, has_img):
    t = L[code]; mid = machine['id']
    name = text(f'block.gtna.{mid}', code, mid.replace('_', ' ').title())
    tips = []
    for i in range(40):
        line = text(f'gtna.machine.{mid}.tooltip.{i}', code)
        if line is None:
            if i > 0 and not tips: break
            continue
        if line.strip(): tips.append(line.strip())
    shape = machine['shape']; pal = shape['palette']
    counts = Counter(pal[c] for plane in shape['blocks'] for row in plane for c in row if c >= 0 and pal[c] not in SKIP)
    dims = (len(shape['blocks']), len(shape['blocks'][0]), len(shape['blocks'][0][0]))
    types = ', '.join(recipe_type_name(r, code) for r in machine['recipeTypes'] if r != 'gtceu:dummy') or t['none']
    num = (lambda n: f'{n:,}'.replace(',', '.')) if code == 'pt_br' else (lambda n: f'{n:,}')
    out = [f'---\ntags:\n  - {t["index"]}\n---\n\n', f'# {name}\n\n', f'<!-- {t["note"]} -->\n\n']
    if has_img: out.append(f'![{name}](../../../assets/machines/{mid}.webp){{ loading=lazy }}\n\n')
    out.append(f'| | |\n|---|---|\n| **{t["types"]}** | {types} |\n| **{t["size"]}** | {dims[0]} × {dims[1]} × {dims[2]} |\n'
               f'| **{t["blocks"]}** | {num(sum(counts.values()))} |\n' + (f'| **{t["generator"]}** | ✓ |\n' if machine['generator'] else ''))
    if mid in HAND: out.append(f'\n[{t["guide"]} →](../{HAND[mid][:-3]}.md)\n')
    if tips:
        out.append(f'\n## {t["about"]}\n\n')
        # Tooltip lines wrap mid-sentence: join them into prose, keep marked lines as bullets.
        prose, bullets = [], []
        for line in tips:
            if line[0] in '▸•-*' or ':' in line[:40]: bullets.append(line.lstrip('▸•-* '))
            else: prose.append(line)
        if prose: out.append(' '.join(prose) + '\n\n')
        out.extend(f'- {line}\n' for line in bullets)
    out.append(f'\n## {t["structure"]}\n\n| {t["block"]} | {t["qty"]} |\n|---|---:|\n')
    out.extend(f'| {block_name(b, code)} | {num(n)} |\n' for b, n in counts.most_common())
    out.append(f'\n<small>{t["note"]}</small>\n')
    return name, types, dims, ''.join(out)


def main():
    machines = sorted(json.load(open(DUMP)), key=lambda m: m['id'])
    os.makedirs(OUT, exist_ok=True); os.makedirs(IMG, exist_ok=True)
    rows = {c: [] for c in L}
    for m in machines:
        if 'shape' not in m: continue
        img = os.path.join(IMG, m['id'] + '.webp')
        has_img = render(m, img)
        for code, suffix in (('pt_br', '.md'), ('en_us', '.en.md')):
            name, types, dims, md = page(m, code, has_img)
            open(os.path.join(OUT, m['id'] + suffix), 'w', encoding='utf-8').write(md)
            mark = ' ★' if m['id'] in HAND else ''
            rows[code].append(f'| [{name}]({m["id"]}.md){mark} | {types} | {dims[0]}×{dims[1]}×{dims[2]} |\n')
        print(m['id'])
    for code, suffix in (('pt_br', '.md'), ('en_us', '.en.md')):
        t = L[code]; c = t['col']
        md = (f'# {t["index"]}\n\n{t["intro"].format(n=len(rows[code]))}\n\n| {c[0]} | {c[1]} | {c[2]} |\n|---|---|---|\n'
              + ''.join(rows[code]))
        open(os.path.join(OUT, 'index' + suffix), 'w', encoding='utf-8').write(md)


if __name__ == '__main__':
    main()
