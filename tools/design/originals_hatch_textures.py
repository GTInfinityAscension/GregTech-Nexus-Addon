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


def mass_injector():
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    frame(d, (90, 200, 255, 255))
    d.polygon([(5, 5), (10, 5), (8, 10), (7, 10)], fill=(160, 220, 255, 255))
    d.ellipse([6, 10, 9, 12], fill=(255, 255, 255, 255))
    return im


def detector_hatch():
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    frame(d, (255, 90, 160, 255))
    for i, c in enumerate(((255, 120, 200, 255), (120, 200, 255, 255), (255, 230, 120, 255))):
        d.line([(8, 8), (4 + i * 4, 4)], fill=c)
        d.line([(8, 8), (12 - i * 4, 12)], fill=c)
    d.point((8, 8), fill=(255, 255, 255, 255))
    return im


def target_cartridge_hatch():
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    frame(d, (120, 255, 170, 255))
    d.ellipse([4, 4, 11, 11], outline=(255, 90, 90, 255))
    d.line([(8, 3), (8, 12)], fill=(255, 90, 90, 255)); d.line([(3, 8), (12, 8)], fill=(255, 90, 90, 255))
    return im


def tuning_hatch():
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    frame(d, (170, 90, 255, 255))
    import math
    pts = [(3 + i, 8 - round(3 * math.sin(i * 0.9))) for i in range(10)]
    d.line(pts, fill=(220, 160, 255, 255))
    d.point((8, 12), fill=(255, 40, 40, 255))
    return im


BODY_COLOURS = {'moon': (200, 200, 205), 'phobos': (140, 110, 90), 'vesta': (170, 160, 140), 'ceres': (120, 130, 140),
                'psyche': (190, 170, 120), 'europa': (220, 200, 170), 'arrokoth': (200, 110, 90), 'nexus_1': (160, 80, 255)}


def cartridge(colour):
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([3, 2, 12, 14], fill=(60, 64, 72, 255), outline=(20, 22, 26, 255))
    d.rectangle([4, 3, 11, 5], fill=(120, 255, 170, 255))
    d.ellipse([5, 7, 10, 12], fill=colour + (255,), outline=(20, 20, 20, 255))
    return im


if __name__ == '__main__':
    items = os.path.join(OUT, '../../../item/originals')
    os.makedirs(items, exist_ok=True)
    for body, colour in BODY_COLOURS.items():
        cartridge(colour).save(os.path.join(items, 'target_cartridge_' + body + '.png'))
    for name, fn in (('mass_injector', mass_injector), ('detector_hatch', detector_hatch),
                     ('target_cartridge_hatch', target_cartridge_hatch), ('tuning_hatch', tuning_hatch)):
        fn().save(os.path.join(OUT, name + '.png'))
    os.makedirs(OUT, exist_ok=True)
    for name, fn in (('beam_dump', beam_dump), ('seismic_probe', seismic_probe), ('liner_hatch', liner_hatch)):
        fn().save(os.path.join(OUT, name + '.png'))
