"""Front overlays of the original multiblocks' special hatches (16x16, drawn over the tiered hull)."""
import os, sys
from PIL import Image, ImageDraw

OUT = os.path.join(os.path.dirname(__file__), '../../src/main/resources/assets/gtna/textures/block/overlay/machine')


def frame(d, rim):
    d.rectangle([2, 2, 13, 13], outline=(30, 30, 36, 255), fill=(18, 18, 24, 255))
    d.rectangle([3, 3, 12, 12], outline=rim)


def beam_dump():
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    frame(d, (90, 140, 255, 255))
    for r, c in ((4, (60, 40, 120, 255)), (3, (110, 80, 220, 255)), (2, (170, 140, 255, 255)), (1, (240, 230, 255, 255))):
        d.ellipse([8 - r, 8 - r, 7 + r, 7 + r], fill=c)
    return im


def seismic_probe():
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    frame(d, (255, 170, 40, 255))
    ys = [8, 8, 7, 9, 5, 11, 6, 9, 8, 8]
    for i in range(len(ys) - 1):
        d.line([(3 + i, ys[i]), (4 + i, ys[i + 1])], fill=(255, 200, 80, 255))
    return im


def liner_hatch():
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    frame(d, (120, 255, 170, 255))
    d.ellipse([4, 4, 11, 11], outline=(150, 160, 170, 255), fill=(70, 75, 85, 255))
    d.ellipse([6, 6, 9, 9], outline=(200, 210, 220, 255), fill=(10, 10, 14, 255))
    return im


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for name, fn in (('beam_dump', beam_dump), ('seismic_probe', seismic_probe), ('liner_hatch', liner_hatch)):
        fn().save(os.path.join(OUT, name + '.png'))
