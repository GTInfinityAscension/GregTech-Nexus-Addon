"""Convert the GTNH Nano Forge StructureLib pieces to GTNA .mbs patterns.

Usage: python3 tools/convert_nano_forge_structure.py <GT5-Unofficial checkout>

Source: GT5-Unofficial master (2026-10-07), gregtech/common/tileentities/machines/multi/MTENanoForge.java
(LGPL-3.0). Each piece is written as transpose(String[][]) i.e. raw[y from top][z][x]; buildPiece offsets give the
controller position inside the piece: main (4, 37, 1), tier2 (-7, 14, 4), tier3 (14, 26, 4). Tier pieces become
separate patterns that also contain the controller cell so GTNASubPatterns can anchor them. As for the DTPF,
GTCEu's FactoryBlockPattern.start() reads aisles toward the front and rows bottom-up, so slices and rows are reversed.
Letters: C Radiant Naquadah Alloy Casing, A Assembly Line Casing, F Stellar Alloy frame, B casing or hatch,
~ controller. Tier 4 = the tier-4 base (offset (20, 33, 0)) plus the physical "render" piece (offset (20, 50, 0));
GTNH also accepts an air piece with its render block instead, which GTNA does not port. Tier-4 letters: J Precision
Field Sync, K Field Energy Absorber, P Loadbearing Distribution, Q Nanite Framework, V Magnetic Anchor or hatch,
X Advanced Iridium, R Nanite Shielding Glass; M/N/O MagMatter, Black and White Dwarf Matter frames; Y is C.
"""

from pathlib import Path
import re
import struct
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "src/main/resources/pattern"
CODES = {"C": 0, "B": 1, "A": 2, "J": 3, "F": 5, "K": 8, "O": 12, "N": 13, "M": 14, "P": 15, "Q": 18, " ": 19,
         "R": 20, "V": 21, "X": 22, "~": 61}
PIECES = {"MAIN": (4, 37, 1), "TIER2": (-7, 14, 4), "TIER3": (14, 26, 4)}


def piece(text, name):
    start = text.index(f".addShape(STRUCTURE_PIECE_{name}, transpose(")
    end = text.index("}))", start)
    body = text[start:end]
    layers = re.findall(r"\{([^{}]*)\}", body)
    return [re.findall(r'"([^"]*)"', layer) for layer in layers]


def constant(text, name):
    """A piece written as a {@code String[][] NAME = transpose(new String[][]{...})} field."""
    start = text.index(f"{name} = transpose(")
    end = text.index("});", start)
    layers = re.findall(r"\{([^{}]*)\}", text[start:end])
    return [re.findall(r'"([^"]*)"', layer) for layer in layers]


def cells(raw, offset):
    h, v, d = offset
    out = {}
    for y, layer in enumerate(raw):
        for z, row in enumerate(layer):
            for x, ch in enumerate(row):
                if ch != " ":
                    out[(x - h, y - v, z - d)] = ch
    return out


def write(name, grid):
    grid[(0, 0, 0)] = "~"
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
    src = Path(sys.argv[1]) / "src/main/java/gregtech/common/tileentities/machines/multi/MTENanoForge.java"
    text = src.read_text()
    main_cells = cells(piece(text, "MAIN"), PIECES["MAIN"])
    if main_cells.get((0, 0, 0)) != "~":
        raise ValueError("controller not found at the main piece offset")
    write("nano_forge_main", main_cells)
    for name in ("TIER2", "TIER3"):
        grid = cells(piece(text, name), PIECES[name])
        if (0, 0, 0) in grid:
            raise ValueError(f"{name} overlaps the controller")
        write(f"nano_forge_{name.lower()}", grid)
    tier4 = cells(constant(text, "STRUCTURE_PIECE_TIER4_STRUCT_BASE"), (20, 33, 0))
    tier4.pop((0, 0, 0), None)
    for pos, ch in cells(constant(text, "STRUCTURE_PIECE_TIER4_STRUCT"), (20, 50, 0)).items():
        if pos in tier4 and tier4[pos] != ch:
            raise ValueError(f"tier 4 pieces disagree at {pos}: {tier4[pos]} vs {ch}")
        tier4[pos] = ch
    tier4 = {pos: ("C" if ch == "Y" else ch) for pos, ch in tier4.items()}
    write("nano_forge_tier4", tier4)


if __name__ == "__main__":
    main()
