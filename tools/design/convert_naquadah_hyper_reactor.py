"""Convert the author's Naquadah HyperReactor build into a GTNA .mbs pattern.

    python3 tools/design/convert_naquadah_hyper_reactor.py <Naquadah HyperReactor.litematic>

Needs nbtlib (pip install nbtlib). The build uses vanilla blocks as markers, mapped as the author approved on
2026-10-19: cracked deepslate tiles -> Hyper Mechanical Casing, acacia wood -> Naquadah Alloy frame, blue wool ->
Naquadah Borosilicate Glass. The controller replaces the casing at the front of the lower central sphere; the casing
around it (radius 3 on the front face) is the hatch ring. Output follows convert_originals.write: pattern/<name>.mbs
plus a JSON sidecar with the letter -> block id table.
"""
import sys
from pathlib import Path

import nbtlib

sys.path.insert(0, str(Path(__file__).resolve().parent))
from convert_originals import to_structurelib, write  # noqa: E402

NAME = 'naquadah_hyper_reactor'
MARKERS = {'minecraft:cracked_deepslate_tiles': 'A', 'minecraft:acacia_wood': 'F', 'minecraft:blue_wool': 'G'}
LETTERS = {'A': 'gtna:hyper_mechanical_casing', 'F': 'gtceu:naquadah_alloy_frame',
           'G': 'gtna:naquadah_borosilicate_glass', 'B': 'hatch'}
CONTROLLER = (48, 5, 0)  # (x, y up, z) in litematic coordinates, front (min z) face


def read_litematic(path):
    """{(x, y, z): block id} of the single region, decoding the packed palette indices."""
    region = next(iter(nbtlib.load(path)['Regions'].values()))
    size = region['Size']
    w, h, l = (abs(int(size[k])) for k in 'xyz')
    palette = [str(entry['Name']) for entry in region['BlockStatePalette']]
    bits = max(2, (len(palette) - 1).bit_length())
    longs = [int(v) & (1 << 64) - 1 for v in region['BlockStates']]
    mask = (1 << bits) - 1
    cells = {}
    for i in range(w * h * l):
        bit = i * bits
        word, offset = bit >> 6, bit & 63
        value = longs[word] >> offset
        if offset + bits > 64: value |= longs[word + 1] << (64 - offset)
        block = palette[value & mask]
        if block in MARKERS:
            y, rest = divmod(i, w * l)
            z, x = divmod(rest, w)
            cells[(x, y, z)] = MARKERS[block]
    return cells


def main(path):
    cells = read_litematic(path)
    cx, cy, cz = CONTROLLER
    if cells.get(CONTROLLER) != 'A': raise SystemExit(f'controller position {CONTROLLER} is not casing')
    for (x, y, z), letter in list(cells.items()):
        if letter == 'A' and z <= cz + 1 and abs(x - cx) <= 3 and abs(y - cy) <= 3:
            cells[(x, y, z)] = 'B'
    write(NAME, to_structurelib(cells, CONTROLLER), LETTERS)


if __name__ == '__main__':
    main(sys.argv[1])
