"""Repairs GTNA textures whose .png.mcmeta still point their ldlib CTM connection at gtocore:, copying the original
GTOCore *_ctm.png (and its .mcmeta) next to the GTNA texture and rewriting the connection to gtna: (G-0214)."""
import json, os, shutil, sys
gtna = 'src/main/resources/assets/gtna/textures'
gto = sys.argv[1]  # .../GTOCore-Main/src/main/resources/assets/gtocore/textures
fixed = []
for d, _, fs in os.walk(gtna):
    for f in fs:
        if not f.endswith('.png.mcmeta'):
            continue
        p = os.path.join(d, f)
        j = json.load(open(p))
        c = j.get('ldlib', {}).get('connection')
        if not c:
            continue
        ns, path = c.split(':', 1)
        if ns == 'gtna' and os.path.exists(f'src/main/resources/assets/gtna/textures/{path}.png'):
            continue
        src = os.path.join(gto, path + '.png')
        if not os.path.exists(src):
            print('MISSING SOURCE', p, c); continue
        base = f[:-len('.png.mcmeta')]
        dst = os.path.join(d, base + '_ctm.png')
        shutil.copyfile(src, dst)
        if os.path.exists(src + '.mcmeta'):
            m = json.load(open(src + '.mcmeta'))
            m.get('ldlib', {}).pop('connection', None)
            json.dump(m, open(dst + '.mcmeta', 'w'), indent=2)
        rel = os.path.relpath(dst, gtna)[:-4]
        j['ldlib']['connection'] = 'gtna:' + rel
        json.dump(j, open(p, 'w'), indent=2)
        fixed.append(rel)
print(len(fixed), 'fixed')
