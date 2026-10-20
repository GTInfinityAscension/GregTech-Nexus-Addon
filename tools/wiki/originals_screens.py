"""Crops the dev-client screenshots of the original multiblocks for the wiki.

    python3 tools/wiki/originals_screens.py [left top right bottom]
        run/screenshots/wiki_<machine>_<panel>_<en|pt|zh>.png -> docs/assets/originals/<machine>_<panel>_<lang>.webp

The box (pixels of the screenshot) keeps the machine window and its side panels; the default fits a 1600 x 1000
client at GUI scale 2. Needs Pillow.
"""
import glob
import os
import re
import sys

from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SRC = os.path.join(ROOT, 'run/screenshots')
OUT = os.path.join(ROOT, 'docs/assets/originals')
BOX = (400, 200, 1200, 800)


def main():
    box = tuple(int(v) for v in sys.argv[1:5]) if len(sys.argv) >= 5 else BOX
    os.makedirs(OUT, exist_ok=True)
    n = 0
    for path in sorted(glob.glob(os.path.join(SRC, 'wiki_*_*_*.png'))):
        m = re.match(r'wiki_(.+)_([a-z]+)_(en|pt|zh)\.png$', os.path.basename(path))
        if not m or m.group(2) == 'manual': continue
        img = Image.open(path).convert('RGB').crop(box)
        img.save(os.path.join(OUT, f'{m.group(1)}_{m.group(2)}_{m.group(3)}.webp'), 'WEBP', quality=88, method=6)
        n += 1
    print(n, 'screens')


if __name__ == '__main__':
    main()
