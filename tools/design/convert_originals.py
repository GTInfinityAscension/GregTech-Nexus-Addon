"""Convert the author's builds into GTNA .mbs patterns for the original endgame multiblocks.

    python3 tools/design/convert_originals.py <voxels.pkl>

<voxels.pkl> holds the four builds as {name: [(x, y, z, block, props)]} (x right, y up, z), produced from
~/Downloads/{bfg.zip, portal.zip, 27971.litematic, 20061.schematic} by the session tools that also made the
renders. Block names go through tools/design mapping rules (mapping.py next to the voxels) into casing letters.

.mbs convention (same as tools/convert_nano_forge_structure.py): StructureLib coordinates x right, y down, z back,
controller at (0, 0, 0) on the front face; aisles are written back-to-front and rows bottom-up.
Each machine also writes a JSON sidecar with the letter -> block id table used by the Java registration.
"""
import json, math, pickle, struct, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'src/main/resources/pattern'
CODES = {"C": 0, "B": 1, "A": 2, "J": 3, "G": 4, "F": 5, "E": 6, "D": 7, "K": 8, "L": 9, "I": 10, "H": 11, "O": 12,
         "N": 13, "M": 14, "P": 15, "S": 16, "Q": 18, " ": 19, "R": 20, "V": 21, "X": 22, "1": 23, "2": 24, "3": 25,
         "~": 61}


def write(name, grid, letters, center=None):
    grid[(0, 0, 0)] = '~'
    xs, ys, zs = zip(*grid)
    frame = [[''.join(grid.get((x, y, z), ' ') for x in range(min(xs), max(xs) + 1))
              for y in range(min(ys), max(ys) + 1)] for z in range(min(zs), max(zs) + 1)]
    data = [list(reversed(rows)) for rows in reversed(frame)]
    with (OUT / f'{name}.mbs').open('wb') as out:
        out.write(struct.pack('>i', len(data)))
        for rows in data:
            out.write(struct.pack('>i', len(rows)))
            for row in rows:
                out.write(struct.pack('>i', len(row)))
                out.write(bytes(CODES[c] for c in row))
    counts = {k: sum(r.count(k) for rows in data for r in rows) for k in CODES if k != ' '}
    counts = {k: v for k, v in counts.items() if v}
    (OUT / f'{name}.json').write_text(json.dumps({'letters': letters, 'counts': counts, 'center': center,
                                                  'size': [len(data), len(data[0]), len(data[0][0])]}, indent=1))
    print(f'{name}: {len(data)}x{len(data[0])}x{len(data[0][0])} {counts}')


def rel(controller, point):
    """(right, up, back) offset of a point from the controller, in the controller's frame."""
    return [point[0] - controller[0], point[1] - controller[1], point[2] - controller[2]]


def to_structurelib(cells, controller):
    """cells: {(x, y_up, z): letter}; controller (x, y_up, z) on the front (min z) face."""
    cx, cy, cz = controller
    return {(x - cx, cy - y, z - cz): c for (x, y, z), c in cells.items()}


def stellar(voxels):
    """Stellar Containment Chamber: hull shell r >= 40 of the 93^3 WarpDrive sphere, bands, and a degenerate core."""
    c = 46
    cells = {}
    for x, y, z, n, p in voxels:
        r = math.dist((x, y, z), (c, c, c))
        if r < 40 or 'air_' in n: continue
        meta = p.get('meta')
        if 'hull.superior.glass' in n: cells[(x, y, z)] = 'G'
        elif 'hull.superior.plain' in n and meta == 15: cells[(x, y, z)] = 'N'
        else: cells[(x, y, z)] = 'C'
    for x in range(c - 7, c + 8):
        for y in range(c - 7, c + 8):
            for z in range(c - 7, c + 8):
                if math.dist((x, y, z), (c, c, c)) <= 7: cells[(x, y, z)] = 'D'
    front = min(z for (x, y, z) in cells if x == c and y == c)
    ctrl = (c, c, front)
    for (x, y, z) in list(cells):  # hatch ring around the controller on the front face
        if abs(x - c) <= 3 and abs(y - c) <= 3 and z <= front + 1 and cells[(x, y, z)] != 'G': cells[(x, y, z)] = 'B'
    write('stellar_containment_chamber', to_structurelib(cells, ctrl), {
        'C': 'gtna:radiant_naquadah_alloy_casing', 'N': 'gtna:neutronium_stable_casing', 'G': 'gtna:plasma_field_glass',
        'B': 'hatch', 'D': 'gtna:degenerate_matter_core'}, rel(ctrl, (c, c, c)))


KEY2ID = {
    'gtceu:solid/machine_casing_clean_stainless_steel': 'gtceu:clean_machine_casing',
    'gtna:casings/radiant_naquadah_alloy_casing': 'gtna:radiant_naquadah_alloy_casing',
    'gtceu:pipe/machine_casing_pipe_tungstensteel': 'gtceu:tungstensteel_pipe_casing',
    'gtceu:solid/machine_casing_inert_ptfe': 'gtceu:inert_machine_casing',
    'gtna:casings/neutronium_stable_casing': 'gtna:neutronium_stable_casing',
    'gtna:casings/dyson_deployment_core': 'gtna:dyson_deployment_core',
    'gtceu:unique/heat_vent': 'gtceu:heat_vent',
    'gtna:casings/molecular_casing': 'gtna:molecular_casing',
    'gtna:extreme_density_casing': 'gtna:extreme_density_casing',
    'gtna:casings/magtech_casing': 'gtna:magtech_casing',
    'gtceu:transparent/fusion_glass': 'gtceu:fusion_glass',
    'gtna:casings/plasma_heater_casing': 'gtna:plasma_heater_casing',
    'gtceu:solid/machine_casing_solid_steel': 'gtceu:solid_machine_casing',
    'gtceu:solid/machine_casing_robust_tungstensteel': 'gtceu:robust_machine_casing',
    'gtna:casings/dimensionally_transcendent_casing': 'gtna:dimensionally_transcendent_casing',
    'gtna:eye_of_harmony/spatial': 'gtna:reinforced_spatial_structure_casing',
    'gtceu:fusion/fusion_coil': 'gtceu:fusion_coil',
    'gtna:casings/dimension_injection_casing': 'gtna:dimension_injection_casing',
    'gtna:dimensional_stability_casing': 'gtna:stabilisation_field_generator_tier_0',
    'gtna:advanced_compressed_fusion_coil': 'gtna:advanced_compressed_fusion_coil',
    'gtna:casings/nano_forge/precision_field_sync_casing': 'gtna:precision_field_sync_casing',
    'gtna:casings/hsss_borosilicate_glass': 'gtna:hsss_borosilicate_glass',
    'gtna:casings/nano_forge/nanite_shielding_glass': 'gtna:nanite_shielding_glass',
    'gtna:casings/cosmic_neutronium_borosilicate_glass': 'gtna:cosmic_neutronium_borosilicate_glass',
    'gtna:casings/high_strength_support_spindle': 'gtna:high_strength_support_spindle',
    'gtna:casings/universal_factory_casing': 'gtna:universal_factory_casing',
}
LETTERS = 'CAJGFEKLIHONMPSQRVX123'
MOVING = {'ring': ('gtna:precision_field_sync_casing', 'gtna:hsss_borosilicate_glass'),
          'gyro': ('gtna:high_strength_support_spindle', 'gtna:nanite_shielding_glass')}


def mapped(build, voxels):
    sys.path.insert(0, str(Path(__file__).parent))
    import originals_mapping as m
    out = []
    for x, y, z, n, p in voxels:
        meta = p.get('meta') if 'meta' in p else None
        key = m.gt(build, n, meta, (128, 128, 128, 255))
        if key: out.append((x, y, z, KEY2ID[key]))
    return out


def lettered(vox, groups):
    """groups: list of (predicate(x,y,z), tag); one letter per (tag, block id)."""
    table, cells = {}, {}
    for x, y, z, bid in vox:
        tag = next((t for f, t in groups if f(x, y, z)), 'static')
        if tag in MOVING:  # moving parts keep one solid and one glass block each
            bid = MOVING[tag][1] if 'glass' in bid else MOVING[tag][0]
        k = (tag, bid)
        if k not in table: table[k] = LETTERS[len(table)]
        cells[(x, y, z)] = table[k]
    return cells, {v: k[1] + ('' if k[0] == 'static' else '#' + k[0]) for k, v in table.items()}


def hatch_ring(cells, letters, ctrl, axis_drop, radius=2):
    cx, cy, cz = ctrl
    for (x, y, z), c in list(cells.items()):
        if abs(x - cx) <= radius and abs(y - cy) <= radius and abs(z - cz) <= 1 and (x, y, z) != ctrl \
                and 'glass' not in letters[c]:
            cells[(x, y, z)] = 'B'
    letters['B'] = 'hatch'


def station(voxels):
    vox = mapped('litematic_27971', voxels)
    cx, cy, cz = 68, 63, 64.5
    ring = lambda x, y, z: math.hypot(x - cx, y - cy) >= 50 and abs(z - cz) < 14
    gyro = lambda x, y, z: 12 <= math.hypot(x - cx, y - cy) < 26 and 6 < abs(z - cz) < 40
    cells, letters = lettered(vox, [(ring, 'ring'), (gyro, 'gyro')])
    # controller at the front end of the injector shaft
    front = min(z for (x, y, z) in cells if abs(x - cx) <= 3 and abs(y - cy) <= 3)
    ctrl = min(((x, y, z) for (x, y, z) in cells if z == front and abs(x - cx) <= 3 and abs(y - cy) <= 3),
               key=lambda p: math.hypot(p[0] - cx, p[1] - cy))
    hatch_ring(cells, letters, ctrl, None)
    write('antimatter_collider_ring', to_structurelib(cells, ctrl), letters, rel(ctrl, (cx, cy, cz)))


def portal(voxels):
    vox = mapped('portal', voxels)
    cells, letters = lettered(vox, [])
    bottom = min(y for (x, y, z) in cells if abs(x - 62) <= 2)
    col = [(x, y, z) for (x, y, z) in cells if abs(x - 62) <= 2 and y <= bottom + 2]
    front = min(z for (x, y, z) in col)
    ctrl = min((p for p in col if p[2] == front), key=lambda p: (abs(p[0] - 62), p[1]))
    hatch_ring(cells, letters, ctrl, None)
    write('dimensional_rift_gate', to_structurelib(cells, ctrl), letters, rel(ctrl, (62.5, 62.5, 26.5)))


def lance(voxels):
    vox = mapped('bfg', voxels)
    cells, letters = lettered(vox, [(lambda x, y, z: y >= 67, 'gun')])
    base = [(x, y, z) for (x, y, z) in cells if y <= 8 and abs(x - 82) <= 3]
    front = min(z for (x, y, z) in base)
    ctrl = min((p for p in base if p[2] == front), key=lambda p: (abs(p[0] - 82), p[1]))
    hatch_ring(cells, letters, ctrl, None)
    muzzle = max(z for (x, y, z) in cells if y >= 67)
    write('kinetic_orbital_lance', to_structurelib(cells, ctrl), letters, rel(ctrl, (81, 100, muzzle)))


def main():
    builds = pickle.load(open(sys.argv[1], 'rb'))
    stellar(builds['schematic_20061'])
    station(builds['litematic_27971'])
    portal(builds['portal'])
    lance(builds['bfg'])


if __name__ == '__main__':
    main()
