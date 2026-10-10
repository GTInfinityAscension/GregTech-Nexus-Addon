import numpy as np
from PIL import Image
from pathlib import Path

# Load cosmic textures
cosmic_dir = Path("/tmp/gtnh_cosmic_textures")
cosmic_textures = []
for i in range(10):
    im = Image.open(cosmic_dir / f"cosmic{i}.png").convert("RGBA")
    cosmic_textures.append(np.array(im, dtype=np.float32) / 255.0)

# Build a single texture atlas (width = 160, height = max height = 112)
atlas_w = 16 * 10
atlas_h = 112
atlas = np.zeros((atlas_h, atlas_w, 4), dtype=np.float32)
cosmicuvs = np.zeros((10, 2), dtype=np.float32)

for i in range(10):
    tex = cosmic_textures[i]
    th, tw = tex.shape[:2]
    # First frame 16x16
    frame0 = tex[:16, :16]
    atlas[:16, i*16:(i+1)*16] = frame0
    # cosmicuvs in shader: vmin, vmax
    # Actually in gtnhlib: cosmicuvs[symbol] has (vmin, vmax)
    cosmicuvs[i, 0] = 0.0
    cosmicuvs[i, 1] = 16.0 / atlas_h

def rotation_matrix(axis, angle):
    axis = axis / np.linalg.norm(axis)
    s = np.sin(angle)
    c = np.cos(angle)
    oc = 1.0 - c
    x, y, z = axis
    return np.array([
        [oc * x * x + c, oc * x * y - z * s, oc * z * x + y * s],
        [oc * x * y + z * s, oc * y * y + c, oc * y * z - x * s],
        [oc * z * x - y * s, oc * y * z + x * s, oc * z * z + c]
    ])

def rand2d(p):
    x, y = p
    dot = x * 12.9898 + y * 78.233
    val = np.sin(dot % 3.141592653589793) * 43758.5453
    return val - np.floor(val)

def smoothstep(edge0, edge1, x):
    t = np.clip((x - edge0) / (edge1 - edge0), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)

def render_universium_frame(t_val, width=16, height=16):
    bg_color = np.array([0.08, 0.12, 0.22]) # [20, 31, 56] / 255
    starColorMultiplier = np.array([0.3, 0.4, 0.3])
    starColorBase = np.array([0.4, 0.6, 0.7])
    
    external_scale = 25.0
    one_over_ext = 1.0 / external_scale
    uvtiles = 16
    cosmiccount = 10
    cosmicoutof = 101
    u_size = 1.0 / cosmiccount
    
    out = np.zeros((height, width, 3), dtype=np.float32)
    
    # Precompute layer params
    layers_data = []
    for i in range(16):
        mult = 16 - i
        j = i + 7
        rand1 = (j * j * 4321 + j * 8) * 2.0
        k = j + 1
        rand2 = (k * k * k * 239 + k * 37) * 3.6
        rand3 = rand1 * 347.4 + rand2 * 63.4
        axis = np.array([np.sin(rand1), np.sin(rand2), np.cos(rand3)])
        axis = axis / np.linalg.norm(axis)
        rot_mat = rotation_matrix(axis, rand3 % (2 * np.pi))
        scale = mult * 0.5 + 2.75
        layers_data.append((mult, rand1, rand2, rand3, rot_mat, scale, i))
    
    for y in range(height):
        for x in range(width):
            # Eye pos in inventory: item quad is around (0,0) to (16,16)
            pos_x = (x - 8.0) * 0.5
            pos_y = (y - 8.0) * 0.5
            pos_z = -100.0
            pos = np.array([pos_x, pos_y, pos_z])
            dir_vec = -pos / np.linalg.norm(pos)
            
            col = bg_color.copy()
            
            for (mult, rand1, rand2, rand3, rot_mat, scale, i) in layers_data:
                ray = np.dot(rot_mat, dir_vec)
                
                rawu = 0.5 + (np.arctan2(ray[2], ray[0]) / (2.0 * np.pi))
                rawv = 0.5 + (np.arcsin(np.clip(ray[1], -1.0, 1.0)) / np.pi)
                
                u = rawu * scale * external_scale
                v = (rawv + t_val * 0.0002 * one_over_ext) * scale * 0.6 * external_scale
                
                tu = int(np.floor(u * uvtiles) % uvtiles)
                tv = int(np.floor(v * uvtiles) % uvtiles)
                
                symbol = int(rand2d((tu, tv + i * 10.0)) * cosmicoutof)
                rotation = int((pow(tu, float(tv)) + tu + 3 + tv * i) % 8)
                flip = False
                if rotation >= 4:
                    rotation -= 4
                    flip = True
                    
                if 0 <= symbol < cosmiccount:
                    ru = np.clip((u % 1.0) * uvtiles - tu, 0.0, 1.0)
                    rv = np.clip((v % 1.0) * uvtiles - tv, 0.0, 1.0)
                    if flip:
                        ru = 1.0 - ru
                    oru, orv = ru, rv
                    if rotation == 1:
                        oru, orv = 1.0 - rv, ru
                    elif rotation == 2:
                        oru, orv = 1.0 - ru, 1.0 - rv
                    elif rotation == 3:
                        oru, orv = rv, 1.0 - ru
                    
                    umin = symbol * u_size
                    vmin, vmax = cosmicuvs[symbol]
                    tile_u = umin + u_size * oru
                    tile_v = vmin * (1.0 - orv) + vmax * orv
                    
                    # Sample atlas
                    px = int(np.clip(tile_u * atlas_w, 0, atlas_w - 1))
                    py = int(np.clip(tile_v * atlas_h, 0, atlas_h - 1))
                    tcol = atlas[py, px]
                    
                    a = tcol[0] * (0.5 + (1.0 / mult)) * (1.0 - smoothstep(0.15, 0.48, abs(rawv - 0.5)))
                    
                    star_color = np.array([
                        (rand1 % 29.0) / 29.0,
                        (rand2 % 35.0) / 35.0,
                        (rand1 % 17.0) / 17.0
                    ]) * starColorMultiplier + starColorBase
                    
                    col += star_color * a
            
            out[y, x] = col
            
    return np.clip(out * 255.0, 0, 255).astype(np.uint8)

frame0 = render_universium_frame(0.0)
im = Image.fromarray(frame0)
im.save("/tmp/test_shader_frame0.png")
im.resize((128, 128), Image.Resampling.NEAREST).save("/tmp/test_shader_frame0_scaled.png")
print("Rendered frame 0 to /tmp/test_shader_frame0_scaled.png")
