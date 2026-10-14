"""Textured isometric render: faces are affine-warped 16x16 casing textures."""
from PIL import Image, ImageEnhance
_spr = {}
def sprites(path, s):
    k = (path, s)
    if k in _spr: return _spr[k]
    t = Image.open(path).convert('RGBA'); t = t.crop((0, 0, t.width, t.width)).resize((16, 16), Image.NEAREST)
    W, H = 4 * s, 4 * s
    def warp(img, coeffs, shade):
        im = img.transform((W, H), Image.AFFINE, coeffs, Image.NEAREST, fillcolor=(0, 0, 0, 0))
        if shade != 1: im = Image.merge('RGBA', [*ImageEnhance.Brightness(im.convert('RGB')).enhance(shade).split(), im.split()[3]])
        return im
    # Output pixel (X,Y) -> texture (u,v). Origin of sprite = top-left of the voxel's 2s*... box.
    # top rhombus: corners (2s,0)->u0v0, (4s,s)->u16, (0,s)->v16
    q, r = 4 / s, 8 / s
    top = warp(t, (q, r, -8, -q, r, 8), 1.0)
    left = warp(t, (r, 0, 0, -q, r, -8), 0.72)
    right = warp(t, (-r, 0, 32, q, r, -24), 0.86)
    _spr[k] = (top, left, right); return _spr[k]
def render(vox, path, s=4, bg=(24, 26, 32), title=None):
    """vox: (x,y,z,texpath)."""
    occ = {(x, y, z) for x, y, z, _ in vox}
    X = max(v[0] for v in vox) + 1; Y = max(v[1] for v in vox) + 1; Z = max(v[2] for v in vox) + 1
    w = (X + Z) * s * 2 + 40; h = (X + Z) * s + Y * s * 2 + 60
    im = Image.new('RGBA', (w, h), bg + (255,))
    ox = Z * s * 2 + 20; oy = Y * s * 2 + 40
    vis = [v for v in vox if (v[0], v[1] + 1, v[2]) not in occ or (v[0], v[1], v[2] + 1) not in occ or (v[0] + 1, v[1], v[2]) not in occ]
    vis.sort(key=lambda v: (v[0] + v[2], v[1]))
    for x, y, z, tp in vis:
        top, left, right = sprites(tp, s)
        # screen pos of point (x, y+1, z): top vertex of the top rhombus
        px = ox + (x - z) * s * 2 - 2 * s; py = oy + (x + z) * s - (y + 1) * s * 2
        if (x, y + 1, z) not in occ: im.alpha_composite(top, (px, py))
        if (x, y, z + 1) not in occ: im.alpha_composite(left, (px, py))
        if (x + 1, y, z) not in occ: im.alpha_composite(right, (px, py))
    im = im.convert('RGB')
    if title:
        from PIL import ImageDraw; ImageDraw.Draw(im).text((10, 10), title, fill=(230, 230, 230))
    im.save(path)
