"""Convert the GTNH BEC structures to GTNA .mbs patterns.

Usage: python3 tools/convert_bec_structures.py <GT5-Unofficial checkout>

Source: GT5-Unofficial 9b4c2a7, tectech/thing/metaTileEntity/multi/structures/BECStructureDefinitions.java
(LGPL-3.0). The definitions are not transposed: def[z][y][x], z toward the back, y top-down, '~' the controller
(StructureWrapper). As for the other converters, GTCEu's FactoryBlockPattern reads aisles toward the front and
rows bottom-up, so slices and rows are reversed. Letters keep GTNH's meaning per machine; 1/2/3 are the hatch
slots (codes 23/24/25).
"""

from pathlib import Path
import re
import struct
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "src/main/resources/pattern"
CODES = {"C": 0, "B": 1, "A": 2, "G": 4, "F": 5, "E": 6, "D": 7, "H": 11, " ": 19, "1": 23, "2": 24, "3": 25,
         "~": 61}
PIECES = {"BEC_GENERATOR": "bec_generator", "BEC_CONTAINMENT_FIELD": "bec_storage",
          "BEC_ASSEMBLER": "bec_assembler", "BEC_IO_NODE": "bec_io_node", "BEC_DIODE": "bec_diode"}


def definition(text, name):
    start = text.index(f"{name} = {{{{")
    end = text.index("}};", start)
    body = text[start + len(name) + 3:end + 2]
    layers = re.findall(r"\{([^{}]*)\}", body)
    return [re.findall(r'"([^"]*)"', layer) for layer in layers]


def write(name, raw):
    cells = {}
    ctrl = None
    for z, layer in enumerate(raw):
        for y, row in enumerate(layer):
            for x, ch in enumerate(row):
                if ch in " -+":
                    continue
                if ch == "~":
                    ctrl = (x, y, z)
                cells[(x, y, z)] = ch
    if ctrl is None:
        raise ValueError(f"{name}: no controller")
    grid = {(x - ctrl[0], y - ctrl[1], z - ctrl[2]): ch for (x, y, z), ch in cells.items()}
    xs, ys, zs = zip(*grid)
    frame = [[["".join(grid.get((x, y, z), " ") for x in range(min(xs), max(xs) + 1))]
              for y in range(min(ys), max(ys) + 1)] for z in range(min(zs), max(zs) + 1)]
    data = [list(reversed([row[0] for row in rows])) for rows in reversed(frame)]
    path = OUT / f"{name}.mbs"
    with path.open("wb") as out:
        out.write(struct.pack(">i", len(data)))
        for rows in data:
            out.write(struct.pack(">i", len(rows)))
            for row in rows:
                out.write(struct.pack(">i", len(row)))
                out.write(bytes(CODES[ch] for ch in row))
    counts = {k: sum(row.count(k) for rows in data for row in rows) for k in CODES if k != " "}
    print(f"wrote {path.relative_to(ROOT)}: {len(data)}x{len(data[0])}x{len(data[0][0])} {counts}")


def main():
    src = (Path(sys.argv[1]) / "src/main/java/tectech/thing/metaTileEntity/multi/structures"
           / "BECStructureDefinitions.java")
    text = src.read_text()
    for const, name in PIECES.items():
        write(name, definition(text, const))


if __name__ == "__main__":
    main()
