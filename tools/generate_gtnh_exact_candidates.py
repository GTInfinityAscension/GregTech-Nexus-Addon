import numpy as np
from PIL import Image
from pathlib import Path

cosmic_dir = Path("/tmp/gtnh_cosmic_textures")
MOD_DIR = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures")
OUT_DIR = Path("/tmp/universium_gtnh_candidates")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Load cosmic textures
cosmic_textures = []
for i in range(10):
    im = Image.open(cosmic_dir / f"cosmic{i}.png").convert("RGBA")
    cosmic_textures.append(np.array(im, dtype=np.float32) / 255.0)

atlas_w = 16 * 10
atlas_h = 112
atlas = np.zeros((atlas_h, atlas_w, 4), dtype=np.float32)
cosmicuvs = np.zeros((10, 2), dtype=np.float32)

for i in range(10):
    tex = cosmic_textures[i]
    atlas[:16, i*16:(i+1)*16] = tex[:16, :16]
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

def get_base_and_overlay(shape):
    if shape == "ingot":
        base = Image.open(MOD_DIR / "items/materialicons/CUSTOM/universium/ingot.png").convert("RGBA")
        ov = Image.open(MOD_DIR / "items/materialicons/CUSTOM/universium/ingot_OVERLAY.png").convert("RGBA")
    elif shape == "plate":
        base = Image.open(MOD_DIR / "items/materialicons/CUSTOM/universium/plate.png").convert("RGBA")
        ov = Image.open(MOD_DIR / "items/materialicons/CUSTOM/universium/plate_OVERLAY.png").convert("RGBA")
    elif shape == "gear":
        base = Image.open(MOD_DIR / "items/materialicons/CUSTOM/universium/gearGt.png").convert("RGBA")
        ov = Image.open(MOD_DIR / "items/materialicons/CUSTOM/universium/gearGt_OVERLAY.png").convert("RGBA")
    elif shape == "block":
        base = Image.open(MOD_DIR / "blocks/iconsets/BLOCK_UNIVERSIUM.png").convert("RGBA")
        arr = np.array(base)
        ov_arr = np.zeros_like(arr)
        h, w = arr.shape[:2]
        for y in range(h):
            for x in range(w):
                if (y == 0 or x == 0) and (y < h - 1 and x < w - 1):
                    ov_arr[y, x] = [255, 255, 255, 200]
        ov = Image.fromarray(ov_arr)
    return base, ov

# Precompute layer data
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

def render_gtnh_exact(shape, option=1, n_frames=30):
    base_im, ov_im = get_base_and_overlay(shape)
    base_arr = np.array(base_im, dtype=np.float32)
    ov_arr = np.array(ov_im, dtype=np.float32)
    h, w = base_arr.shape[:2]
    alpha = base_arr[:, :, 3] > 0
    ov_mask = ov_arr[:, :, 3] > 40
    
    bg_color = np.array([0.08, 0.12, 0.22])
    starColorMultiplier = np.array([0.3, 0.4, 0.3])
    starColorBase = np.array([0.4, 0.6, 0.7])
    
    # Scale options
    # Opt 1: exact GTNH scale (externalScale = 25.0)
    # Opt 2: slightly higher star density (externalScale = 18.0) + twinkling pulse
    # Opt 3: maximum starfield density (externalScale = 12.0) like the zoomed Item Zoom view
    if option == 1:
        external_scale = 22.0
        drift_speed = 350.0
    elif option == 2:
        external_scale = 16.0
        drift_speed = 400.0
    else: # option == 3
        external_scale = 11.0
        drift_speed = 450.0

    one_over_ext = 1.0 / external_scale
    uvtiles = 16
    cosmiccount = 10
    cosmicoutof = 101 if option != 3 else 70  # denser stars
    u_size = 1.0 / cosmiccount

    frames = []
    for f in range(n_frames):
        t_val = (f / n_frames) * drift_speed
        frame_rgb = np.zeros((h, w, 3), dtype=np.float32)
        
        for y in range(h):
            for x in range(w):
                if not alpha[y, x]:
                    continue
                
                pos_x = (x - 7.5) * 0.4
                pos_y = (y - 7.5) * 0.4
                pos_z = -100.0
                pos = np.array([pos_x, pos_y, pos_z])
                dir_vec = -pos / np.linalg.norm(pos)
                
                col = bg_color.copy()
                
                for (mult, rand1, rand2, rand3, rot_mat, scale, i) in layers_data:
                    ray = np.dot(rot_mat, dir_vec)
                    rawu = 0.5 + (np.arctan2(ray[2], ray[0]) / (2.0 * np.pi))
                    rawv = 0.5 + (np.arcsin(np.clip(ray[1], -1.0, 1.0)) / np.pi)
                    
                    u = rawu * scale * external_scale
                    # Slow linear celestial drift (the exact formula from universium.frag)
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
                        
                        px = int(np.clip(tile_u * atlas_w, 0, atlas_w - 1))
                        py = int(np.clip(tile_v * atlas_h, 0, atlas_h - 1))
                        tcol = atlas[py, px]
                        
                        a = tcol[0] * (0.5 + (1.0 / mult)) * (1.0 - smoothstep(0.15, 0.48, abs(rawv - 0.5)))
                        
                        # Star color
                        star_color = np.array([
                            (rand1 % 29.0) / 29.0,
                            (rand2 % 35.0) / 35.0,
                            (rand1 % 17.0) / 17.0
                        ]) * starColorMultiplier + starColorBase
                        
                        # Option 2 twinkle
                        if option == 2:
                            twinkle = 0.8 + 0.3 * np.cos((f / n_frames + (rand1 % 10.0)/10.0) * 2 * np.pi)
                            star_color = star_color * twinkle
                            
                        col += star_color * a
                
                frame_rgb[y, x] = col
                
        # Superimpose pure white ridge overlay
        out_rgba = np.zeros((h, w, 4), dtype=np.uint8)
        rgb_bytes = np.clip(frame_rgb * 255.0, 0, 255).astype(np.uint8)
        
        for y in range(h):
            for x in range(w):
                if alpha[y, x]:
                    if ov_mask[y, x]:
                        # White ridge of Modernity
                        out_rgba[y, x] = [255, 255, 255, 255]
                    else:
                        out_rgba[y, x] = [rgb_bytes[y, x, 0], rgb_bytes[y, x, 1], rgb_bytes[y, x, 2], 255]
                        
        frames.append(Image.fromarray(out_rgba))

    # Save animated GIF
    gif_path = OUT_DIR / f"universium_gtnh_opt{option}_{shape}.gif"
    frames[0].save(
        gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=66,
        loop=0,
        disposal=2
    )
    print(f"Saved {gif_path.name}")

if __name__ == "__main__":
    for opt in [1, 2, 3]:
        for sh in ["ingot", "plate", "gear", "block"]:
            render_gtnh_exact(sh, option=opt)
