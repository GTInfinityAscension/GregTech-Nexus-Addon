"""Effect previews for one approved material texture: each effect spec rendered as a GIF (originals_icon_variants).

Usage: python3 tools/design/originals_effect_compare.py <material> <texture option> <specs.json> <out dir>
specs.json: {"<label>": {effect spec as in originals_icon_variants}, ...}
"""

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import originals_icon_variants as v  # noqa: E402

material, opt, specs, out = sys.argv[1], int(sys.argv[2]), json.loads(Path(sys.argv[3]).read_text()), Path(sys.argv[4])
out.mkdir(parents=True, exist_ok=True)
_, _, _, shapes, _ = v.MATERIALS[material]
for label, spec in specs.items():
    for name in [s for s in shapes if s != "block"][:3]:
        frames = v.frames_of(material, opt, name)
        rng = np.random.default_rng(1)
        cells = [v.preview(fr, spec, i, rng).resize((v.CELL * 6, v.CELL * 6), v.Image.NEAREST)
                 for i, fr in enumerate(frames)]
        cells[0].save(out / f"{material}_{label}_{name}.gif", save_all=True, append_images=cells[1:], duration=100,
                      loop=0, disposal=2)
print(out)
