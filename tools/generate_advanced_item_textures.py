#!/usr/bin/env python3
import os
import math
import numpy as np
from PIL import Image

OUT_DIR = "/tmp/gtna_items_preview"
os.makedirs(OUT_DIR, exist_ok=True)

NUM_FRAMES = 16

def save_transparent_gif(frames, out_path, duration=80):
    """Saves a list of RGBA PIL Images as a properly formatted transparent animated GIF."""
    p_frames = []
    for f in frames:
        alpha = f.split()[3]
        # Translucent threshold: pixels with alpha < 16 become fully transparent
        mask = Image.eval(alpha, lambda a: 255 if a < 16 else 0)
        rgb = f.convert('RGB')
        # Quantize to 255 colors so 255 is reserved for transparency
        p_frame = rgb.convert('P', palette=Image.ADAPTIVE, colors=254)
        p_frame.paste(255, mask)
        p_frame.info['transparency'] = 255
        p_frames.append(p_frame)
        
    p_frames[0].save(
        out_path,
        save_all=True,
        append_images=p_frames[1:],
        duration=duration,
        loop=0,
        disposal=2,
        transparency=255
    )

# -------------------------------------------------------------------------
# 1. SPECIAL LASER LENS
# -------------------------------------------------------------------------
def create_laser_lens(size=32, num_frames=16):
    frames = []
    scale = size / 32.0
    cx, cy = (size - 1) / 2.0, (size - 1) / 2.0
    
    y_coords, x_coords = np.mgrid[:size, :size].astype(np.float32)
    dx = x_coords - cx
    dy = y_coords - cy
    dist = np.sqrt(dx**2 + dy**2)
    angle = np.arctan2(dy, dx) # -pi to pi
    
    r_outer = 14.5 * scale
    r_rim_mid = 12.8 * scale
    r_bezel = 11.2 * scale
    r_glass = 10.2 * scale
    r_core = 3.2 * scale
    
    for f in range(num_frames):
        phase = (f / num_frames) * 2 * math.pi
        arr = np.zeros((size, size, 4), dtype=np.float32)
        
        # --- A. Outer Mount (Machined Duranium Slate Alloy) ---
        mount_mask = (dist <= r_outer) & (dist >= r_bezel)
        
        # Heavy metallic gradient with top-left keylight (-1, -1)
        light_x = -0.707
        light_y = -0.707
        norm_dist = np.maximum(dist, 1e-4)
        nx = dx / norm_dist
        ny = dy / norm_dist
        dot_light = -(nx * light_x + ny * light_y) # 1 facing light, -1 away
        
        # Duranium base color palette
        # Base: #434c5e / #2e3440 / #5e81ac
        # Highlight: #88c0d0 / #d8dee9
        # Shadow: #1b1f27
        metal_base_r = 65.0 + 35.0 * dot_light
        metal_base_g = 75.0 + 40.0 * dot_light
        metal_base_b = 95.0 + 55.0 * dot_light
        
        arr[mount_mask, 0] = metal_base_r[mount_mask]
        arr[mount_mask, 1] = metal_base_g[mount_mask]
        arr[mount_mask, 2] = metal_base_b[mount_mask]
        arr[mount_mask, 3] = 255.0
        
        # Outer silhouette outline (crisp dark pixel border)
        out_border = (dist <= r_outer) & (dist > r_outer - 1.0 * scale)
        arr[out_border, 0] = 22.0
        arr[out_border, 1] = 26.0
        arr[out_border, 2] = 34.0
        
        # Inner bezel groove (dark recessed ring)
        bezel_groove = (dist >= r_bezel) & (dist < r_bezel + 0.8 * scale)
        arr[bezel_groove, 0] = 30.0
        arr[bezel_groove, 1] = 35.0
        arr[bezel_groove, 2] = 48.0
        
        # Chrome highlight rim
        chrome_rim = (dist >= r_bezel + 0.8 * scale) & (dist < r_bezel + 1.6 * scale)
        arr[chrome_rim, 0] = np.clip(arr[chrome_rim, 0] + 70.0, 0, 255)
        arr[chrome_rim, 1] = np.clip(arr[chrome_rim, 1] + 85.0, 0, 255)
        arr[chrome_rim, 2] = np.clip(arr[chrome_rim, 2] + 110.0, 0, 255)
        
        # 4 Calibration Clamps / Alignment Lugs at cardinal positions
        for c_ang in [0, math.pi/2, math.pi, 3*math.pi/2]:
            lx = cx + (r_outer - 1.2 * scale) * math.cos(c_ang)
            ly = cy + (r_outer - 1.2 * scale) * math.sin(c_ang)
            lug_dist = np.sqrt((x_coords - lx)**2 + (y_coords - ly)**2)
            lug_m = lug_dist < 1.8 * scale
            # Gold contact electrode
            arr[lug_m, 0] = 255.0
            arr[lug_m, 1] = 200.0
            arr[lug_m, 2] = 70.0
            arr[lug_m, 3] = 255.0
            
            # Center gold pin
            pin_m = lug_dist < 0.8 * scale
            arr[pin_m, 0] = 255.0
            arr[pin_m, 1] = 245.0
            arr[pin_m, 2] = 180.0
            
        # 4 Micro Screws at diagonals (45, 135, 225, 315 deg)
        for s_ang in [math.pi/4, 3*math.pi/4, 5*math.pi/4, 7*math.pi/4]:
            sx = cx + r_rim_mid * math.cos(s_ang)
            sy = cy + r_rim_mid * math.sin(s_ang)
            s_dist = np.sqrt((x_coords - sx)**2 + (y_coords - sy)**2)
            screw_m = s_dist < 1.1 * scale
            arr[screw_m, 0] = 160.0
            arr[screw_m, 1] = 180.0
            arr[screw_m, 2] = 205.0
            arr[screw_m, 3] = 255.0
            
        # --- B. Optical Prism Glass Body ---
        glass_mask = dist < r_bezel
        
        # Base glass: Ultra-clear crystalline optic with deep blue/cyan refractive substrate
        g_depth = np.clip(1.0 - dist / r_bezel, 0, 1)
        base_g_r = 18.0 + 25.0 * g_depth
        base_g_g = 45.0 + 55.0 * g_depth
        base_g_b = 85.0 + 85.0 * g_depth
        base_g_a = 200.0 + 55.0 * g_depth
        
        arr[glass_mask, 0] = base_g_r[glass_mask]
        arr[glass_mask, 1] = base_g_g[glass_mask]
        arr[glass_mask, 2] = base_g_b[glass_mask]
        arr[glass_mask, 3] = base_g_a[glass_mask]
        
        # --- C. Dynamic Prismatic Laser Dispersion (Rotating Spectral Caustic) ---
        rot_ang = (angle - phase) % (2 * math.pi)
        
        # Rainbow spectrum generation
        # Map rot_ang to HSV hue
        hue = (rot_ang / (2 * math.pi) + 0.15 * (dist / r_bezel)) % 1.0
        
        # Vectorized Hue -> RGB
        r_c = np.clip(np.abs(hue * 6.0 - 3.0) - 1.0, 0.0, 1.0)
        g_c = np.clip(2.0 - np.abs(hue * 6.0 - 2.0), 0.0, 1.0)
        b_c = np.clip(2.0 - np.abs(hue * 6.0 - 4.0), 0.0, 1.0)
        
        # Optical beam facets (3 rotating laser interference caustic waves)
        facet_wave = (np.cos(3.0 * angle - 3.0 * phase) * 0.5 + 0.5) ** 1.5
        # Radial laser power falloff (brightest in inner glass)
        beam_power = facet_wave * np.clip(1.0 - (dist / r_glass)**1.2, 0, 1) * 1.5
        beam_power = np.clip(beam_power, 0.0, 1.0)
        
        # Blend spectral laser into glass
        arr[glass_mask, 0] = np.clip(arr[glass_mask, 0] * (1.0 - beam_power[glass_mask]) + r_c[glass_mask] * 255.0 * beam_power[glass_mask], 0, 255)
        arr[glass_mask, 1] = np.clip(arr[glass_mask, 1] * (1.0 - beam_power[glass_mask]) + g_c[glass_mask] * 255.0 * beam_power[glass_mask], 0, 255)
        arr[glass_mask, 2] = np.clip(arr[glass_mask, 2] * (1.0 - beam_power[glass_mask]) + b_c[glass_mask] * 255.0 * beam_power[glass_mask], 0, 255)
        
        # --- D. Concentrated Laser Focal Core & Diffraction Star ---
        pulse = 0.85 + 0.3 * math.sin(phase * 2.0)
        core_r_eff = r_core * pulse
        core_int = np.clip(1.0 - dist / core_r_eff, 0, 1) ** 1.8
        core_m = dist < core_r_eff
        
        # Super-intense photonic core (pure blinding white with cyan halo)
        arr[core_m, 0] = np.clip(arr[core_m, 0] + core_int[core_m] * 255.0, 0, 255)
        arr[core_m, 1] = np.clip(arr[core_m, 1] + core_int[core_m] * 255.0, 0, 255)
        arr[core_m, 2] = np.clip(arr[core_m, 2] + core_int[core_m] * 255.0, 0, 255)
        arr[core_m, 3] = 255.0
        
        # Cross laser diffraction spikes
        spike_thick = 0.85 * scale
        spike_len = 7.5 * scale
        sp_h = np.exp(-(dy**2) / (spike_thick**2)) * np.clip(1.0 - np.abs(dx) / spike_len, 0, 1) * pulse * 0.85
        sp_v = np.exp(-(dx**2) / (spike_thick**2)) * np.clip(1.0 - np.abs(dy) / spike_len, 0, 1) * pulse * 0.85
        sp_tot = np.clip(sp_h + sp_v, 0, 1)
        sp_m = (sp_tot > 0.1) & (dist < r_bezel)
        
        arr[sp_m, 0] = np.clip(arr[sp_m, 0] + sp_tot[sp_m] * 230.0, 0, 255)
        arr[sp_m, 1] = np.clip(arr[sp_m, 1] + sp_tot[sp_m] * 245.0, 0, 255)
        arr[sp_m, 2] = np.clip(arr[sp_m, 2] + sp_tot[sp_m] * 255.0, 0, 255)
        
        # --- E. Specular Glass Arc (Upper-Left Reflection) ---
        glint_ang = np.abs(angle - (-3.0 * math.pi / 4.0)) # around -135 deg
        glint_m = (dist >= r_bezel - 2.2 * scale) & (dist <= r_bezel - 0.6 * scale) & (glint_ang < 0.65)
        glint_int = np.clip(1.0 - glint_ang / 0.65, 0, 1)
        arr[glint_m, 0] = np.clip(arr[glint_m, 0] + 190.0 * glint_int[glint_m], 0, 255)
        arr[glint_m, 1] = np.clip(arr[glint_m, 1] + 230.0 * glint_int[glint_m], 0, 255)
        arr[glint_m, 2] = np.clip(arr[glint_m, 2] + 255.0 * glint_int[glint_m], 0, 255)
        arr[glint_m, 3] = 255.0
        
        img_data = np.clip(arr, 0, 255).astype(np.uint8)
        frames.append(Image.fromarray(img_data, mode="RGBA"))
        
    return frames

# -------------------------------------------------------------------------
# 2. STABLE BOSON CONTAINMENT UNIT
# -------------------------------------------------------------------------
def create_stable_boson_containment_unit(size=32, num_frames=16):
    frames = []
    scale = size / 32.0
    cx, cy = (size - 1) / 2.0, (size - 1) / 2.0
    
    y_coords, x_coords = np.mgrid[:size, :size].astype(np.float32)
    dx = x_coords - cx
    dy = y_coords - cy
    dist_c = np.sqrt(dx**2 + dy**2)
    
    cap_h = 4.8 * scale
    cham_w = 9.2 * scale
    cham_h = 8.5 * scale
    strut_w = 2.2 * scale
    
    for f in range(num_frames):
        phase = (f / num_frames) * 2 * math.pi
        arr = np.zeros((size, size, 4), dtype=np.float32)
        
        # --- A. Outer Frame & End Caps (Heavy Neutronium Bulkheads) ---
        in_cap_x = np.abs(dx) <= cham_w
        top_cap_m = in_cap_x & (dy <= -cham_h) & (dy >= -(cham_h + cap_h))
        bot_cap_m = in_cap_x & (dy >= cham_h) & (dy <= (cham_h + cap_h))
        caps_m = top_cap_m | bot_cap_m
        
        # Heavy metallic cylindrical shading across X
        nx = dx / cham_w
        cap_shade = 1.0 - 0.35 * nx + 0.15 * (1.0 - nx**2)
        
        # Base Neutronium Blue-Slate Metal
        arr[caps_m, 0] = np.clip(55.0 * cap_shade[caps_m], 25, 150)
        arr[caps_m, 1] = np.clip(65.0 * cap_shade[caps_m], 30, 170)
        arr[caps_m, 2] = np.clip(85.0 * cap_shade[caps_m], 45, 210)
        arr[caps_m, 3] = 255.0
        
        # Outline edges on caps
        top_out = in_cap_x & (dy >= -(cham_h + cap_h)) & (dy < -(cham_h + cap_h) + 1.0 * scale)
        bot_out = in_cap_x & (dy <= (cham_h + cap_h)) & (dy > (cham_h + cap_h) - 1.0 * scale)
        side_cap_out = (np.abs(dx) >= cham_w - 1.0 * scale) & (caps_m)
        out_caps = top_out | bot_out | side_cap_out
        
        arr[out_caps, 0] = 20.0
        arr[out_caps, 1] = 24.0
        arr[out_caps, 2] = 32.0
        
        # Top chamfer highlight ridge (reflecting light)
        chamfer_top = in_cap_x & (dy >= -(cham_h + cap_h) + 1.0 * scale) & (dy < -(cham_h + cap_h) + 2.0 * scale)
        arr[chamfer_top, 0] = 160.0
        arr[chamfer_top, 1] = 185.0
        arr[chamfer_top, 2] = 225.0
        
        # Status LED display bar on Top Cap (Pulsing Quantum Lock Indicator)
        led_pulse = 0.75 + 0.25 * math.sin(phase)
        led_m = (np.abs(dx) <= 3.5 * scale) & (dy >= -(cham_h + cap_h * 0.75)) & (dy <= -(cham_h + cap_h * 0.35))
        arr[led_m, 0] = 20.0 * led_pulse
        arr[led_m, 1] = 255.0 * led_pulse
        arr[led_m, 2] = 170.0 * led_pulse
        arr[led_m, 3] = 255.0
        
        # Cooling ribs on Bottom Cap
        rib_m = (np.abs(dx) <= cham_w - 2.0 * scale) & (dy >= cham_h + 1.5 * scale) & (dy <= cham_h + 3.5 * scale) & (np.mod(dx, 2.0 * scale) < 1.0 * scale)
        arr[rib_m, 0] = 30.0
        arr[rib_m, 1] = 35.0
        arr[rib_m, 2] = 48.0
        
        # --- B. Reinforced Structural Confinement Struts (Left & Right) ---
        strut_m = (np.abs(dx) >= cham_w - strut_w) & (np.abs(dx) <= cham_w) & (np.abs(dy) <= cham_h)
        strut_shade = 0.85 + 0.35 * (dx / cham_w)
        arr[strut_m, 0] = np.clip(50.0 * strut_shade[strut_m], 25, 120)
        arr[strut_m, 1] = np.clip(60.0 * strut_shade[strut_m], 30, 140)
        arr[strut_m, 2] = np.clip(80.0 * strut_shade[strut_m], 40, 180)
        arr[strut_m, 3] = 255.0
        
        # Strut outer silhouette border
        strut_out = (np.abs(dx) >= cham_w - 0.9 * scale) & (np.abs(dy) <= cham_h)
        arr[strut_out, 0] = 20.0
        arr[strut_out, 1] = 24.0
        arr[strut_out, 2] = 32.0
        
        # Superconducting coil wrap stripes on struts
        coil_stripes = strut_m & (np.mod(dy + cham_h, 3.5 * scale) < 1.2 * scale)
        arr[coil_stripes, 0] = 240.0 # Gold coil
        arr[coil_stripes, 1] = 180.0
        arr[coil_stripes, 2] = 45.0
        
        # --- C. Transparent Vacuum / Forcefield Glass Chamber ---
        glass_w = cham_w - strut_w
        glass_m = (np.abs(dx) < glass_w) & (np.abs(dy) <= cham_h)
        
        # Curvature cylinder 3D factor
        cyl_t = np.clip(np.abs(dx) / glass_w, 0, 1)
        cyl_curve = np.sqrt(np.maximum(0.0, 1.0 - cyl_t**2))
        
        # Subtle translucent glass body
        arr[glass_m, 0] = 16.0 + 15.0 * cyl_curve[glass_m]
        arr[glass_m, 1] = 35.0 + 30.0 * cyl_curve[glass_m]
        arr[glass_m, 2] = 60.0 + 45.0 * cyl_curve[glass_m]
        arr[glass_m, 3] = 140.0 + 50.0 * (1.0 - cyl_curve[glass_m])
        
        # Glass reflection vertical glint streak (front-left reflection)
        glint_w_m = (dx >= -glass_w * 0.72) & (dx <= -glass_w * 0.48) & (np.abs(dy) <= cham_h * 0.92)
        arr[glint_w_m, 0] = np.clip(arr[glint_w_m, 0] + 130.0, 0, 255)
        arr[glint_w_m, 1] = np.clip(arr[glint_w_m, 1] + 190.0, 0, 255)
        arr[glint_w_m, 2] = np.clip(arr[glint_w_m, 2] + 250.0, 0, 255)
        arr[glint_w_m, 3] = 220.0
        
        # --- D. Top & Bottom Magnetic Emitter Needles (Field Injectors) ---
        needle_m = (np.abs(dx) <= 1.2 * scale) & (
            ((dy >= -cham_h) & (dy <= -cham_h + 3.2 * scale)) | 
            ((dy <= cham_h) & (dy >= cham_h - 3.2 * scale))
        )
        arr[needle_m, 0] = 210.0
        arr[needle_m, 1] = 230.0
        arr[needle_m, 2] = 255.0
        arr[needle_m, 3] = 255.0
        
        # --- E. THE STABLE BOSON (Quantum Singularity Core) ---
        # Breathing pulsation
        boson_r = (3.5 + 0.9 * math.sin(phase)) * scale
        boson_glow_r = 8.0 * scale
        
        b_dist = np.sqrt(dx**2 + dy**2)
        b_core_int = np.clip(1.0 - (b_dist / boson_r), 0, 1)
        b_glow_int = np.clip(1.0 - (b_dist / boson_glow_r), 0, 1) ** 1.6
        
        apply_glow = glass_m & (b_glow_int > 0.05)
        
        # Deep Quantum Indigo / Radiant Cyan-White Glow
        glow_r = 100.0 * b_glow_int + 255.0 * (b_core_int ** 1.8)
        glow_g = 190.0 * b_glow_int + 255.0 * (b_core_int ** 1.8)
        glow_b = 255.0 * b_glow_int + 255.0 * (b_core_int)
        
        arr[apply_glow, 0] = np.clip(arr[apply_glow, 0] + glow_r[apply_glow], 0, 255)
        arr[apply_glow, 1] = np.clip(arr[apply_glow, 1] + glow_g[apply_glow], 0, 255)
        arr[apply_glow, 2] = np.clip(arr[apply_glow, 2] + glow_b[apply_glow], 0, 255)
        arr[apply_glow, 3] = np.clip(arr[apply_glow, 3] + b_glow_int[apply_glow] * 180.0, 0, 255)
        
        # Pure White Hot Boson Center
        hot_core = glass_m & (b_dist < boson_r * 0.5)
        arr[hot_core, 0] = 255.0
        arr[hot_core, 1] = 255.0
        arr[hot_core, 2] = 255.0
        arr[hot_core, 3] = 255.0
        
        # --- F. Quantum Field Containment Rings (Precessing Ellipses) ---
        # Precessing ring 1 (+25 deg)
        ang1 = math.pi / 7.0
        rx1 = dx * math.cos(ang1) - dy * math.sin(ang1)
        ry1 = dx * math.sin(ang1) + dy * math.cos(ang1)
        r1_d = np.abs(np.sqrt((rx1 / 1.5)**2 + (ry1 / 0.7)**2) - 3.4 * scale)
        ring1_m = glass_m & (r1_d < 0.85 * scale)
        
        # Precessing ring 2 (-25 deg)
        ang2 = -math.pi / 7.0
        rx2 = dx * math.cos(ang2) - dy * math.sin(ang2)
        ry2 = dx * math.sin(ang2) + dy * math.cos(ang2)
        r2_d = np.abs(np.sqrt((rx2 / 1.5)**2 + (ry2 / 0.7)**2) - 3.4 * scale)
        ring2_m = glass_m & (r2_d < 0.85 * scale)
        
        for rm in [ring1_m, ring2_m]:
            arr[rm, 0] = np.clip(arr[rm, 0] + 60.0, 0, 255)
            arr[rm, 1] = np.clip(arr[rm, 1] + 200.0, 0, 255)
            arr[rm, 2] = np.clip(arr[rm, 2] + 255.0, 0, 255)
            arr[rm, 3] = 255.0
            
        # Orbiting micro-boson spark 1
        sp1_t = phase
        s1x = 3.4 * 1.5 * scale * math.cos(sp1_t)
        s1y = 3.4 * 0.7 * scale * math.sin(sp1_t)
        sp1_x = s1x * math.cos(-ang1) - s1y * math.sin(-ang1)
        sp1_y = s1x * math.sin(-ang1) + s1y * math.cos(-ang1)
        sp1_dist = np.sqrt((dx - sp1_x)**2 + (dy - sp1_y)**2)
        sp1_m = glass_m & (sp1_dist < 1.25 * scale)
        
        # Orbiting micro-boson spark 2
        sp2_t = -phase + math.pi
        s2x = 3.4 * 1.5 * scale * math.cos(sp2_t)
        s2y = 3.4 * 0.7 * scale * math.sin(sp2_t)
        sp2_x = s2x * math.cos(-ang2) - s2y * math.sin(-ang2)
        sp2_y = s2x * math.sin(-ang2) + s2y * math.cos(-ang2)
        sp2_dist = np.sqrt((dx - sp2_x)**2 + (dy - sp2_y)**2)
        sp2_m = glass_m & (sp2_dist < 1.25 * scale)
        
        for sm in [sp1_m, sp2_m]:
            arr[sm, 0] = 255.0
            arr[sm, 1] = 255.0
            arr[sm, 2] = 255.0
            arr[sm, 3] = 255.0
            
        # Micro electric arc discharges between needle and core
        if f % 4 in [0, 1]:
            arc_y = np.linspace(-cham_h + 3.0*scale, -boson_r, 8)
            arc_x = np.sin(arc_y * 1.8 + phase * 4.0) * 0.75 * scale
            for ax, ay in zip(arc_x, arc_y):
                px = int(round(cx + ax))
                py = int(round(cy + ay))
                if 0 <= px < size and 0 <= py < size:
                    arr[py, px, 0] = 190.0
                    arr[py, px, 1] = 245.0
                    arr[py, px, 2] = 255.0
                    arr[py, px, 3] = 255.0
                    
        img_data = np.clip(arr, 0, 255).astype(np.uint8)
        frames.append(Image.fromarray(img_data, mode="RGBA"))
        
    return frames

# -------------------------------------------------------------------------
# 3. GRAVITON ANOMALY
# -------------------------------------------------------------------------
def create_graviton_anomaly(size=32, num_frames=16):
    frames = []
    scale = size / 32.0
    cx, cy = (size - 1) / 2.0, (size - 1) / 2.0
    
    y_coords, x_coords = np.mgrid[:size, :size].astype(np.float32)
    dx = x_coords - cx
    dy = y_coords - cy
    dist = np.sqrt(dx**2 + dy**2)
    angle = np.arctan2(dy, dx)
    
    r_singularity = 3.6 * scale
    r_photon_in = 3.8 * scale
    r_photon_out = 6.2 * scale
    r_disk_max = 14.5 * scale
    
    for f in range(num_frames):
        phase = (f / num_frames) * 2 * math.pi
        arr = np.zeros((size, size, 4), dtype=np.float32)
        
        # --- A. Space-Time Warping Waves (Gravitational Ripples) ---
        ripple = np.sin(dist / (1.7 * scale) - phase * 1.8)
        outer_m = (dist <= r_disk_max) & (dist > r_photon_in)
        rip_int = np.clip(ripple * 0.5 + 0.5, 0, 1) * np.clip(1.0 - dist / r_disk_max, 0, 1) ** 1.8
        
        # Deep cosmic void violet
        arr[outer_m, 0] = 55.0 * rip_int[outer_m]
        arr[outer_m, 1] = 15.0 * rip_int[outer_m]
        arr[outer_m, 2] = 105.0 * rip_int[outer_m]
        arr[outer_m, 3] = np.clip(rip_int[outer_m] * 210.0, 0, 255)
        
        # --- B. Swirling Relativistic Accretion Disk (Tilted Perspective) ---
        tilt_y = dy / 0.62
        tilted_r = np.sqrt(dx**2 + tilt_y**2)
        tilted_ang = np.arctan2(tilt_y, dx)
        
        # Logarithmic spiral arms
        # Theta = theta_0 + k * ln(r)
        sp_phase = phase
        arm1 = np.sin(2.0 * tilted_ang - 3.2 * np.log(np.maximum(tilted_r / (3.5 * scale), 0.1)) + sp_phase)
        arm2 = np.sin(2.0 * tilted_ang - 3.2 * np.log(np.maximum(tilted_r / (3.5 * scale), 0.1)) + sp_phase + math.pi)
        spiral_density = np.maximum(arm1, arm2)
        
        disk_m = (tilted_r >= r_photon_in) & (tilted_r <= r_disk_max) & (dist <= r_disk_max)
        rad_falloff = np.clip(1.0 - (tilted_r - r_photon_in) / (r_disk_max - r_photon_in), 0, 1)
        disk_int = np.clip((spiral_density * 0.5 + 0.5) ** 1.2 * rad_falloff, 0, 1)
        
        # Relativistic Doppler Beaming: Left side moves towards us (bright, blueshifted), Right side away (redshifted)
        doppler_boost = 1.0 - 0.42 * (dx / r_disk_max)
        
        # Color temperature:
        # Inner disk: Blinding white-gold & electric cyan
        # Outer disk: Relativistic plasma (amber, orange-red, and violet)
        disk_r = (255.0 * (rad_falloff**0.6) + 170.0 * (1.0 - rad_falloff)) * doppler_boost
        disk_g = (210.0 * (rad_falloff**1.1) + 45.0 * (1.0 - rad_falloff)) * doppler_boost
        disk_b = (130.0 * (rad_falloff**2.2) + 220.0 * (1.0 - rad_falloff)) * doppler_boost
        
        apply_disk = disk_m & (disk_int > 0.08)
        arr[apply_disk, 0] = np.clip(arr[apply_disk, 0] + disk_r[apply_disk] * disk_int[apply_disk], 0, 255)
        arr[apply_disk, 1] = np.clip(arr[apply_disk, 1] + disk_g[apply_disk] * disk_int[apply_disk], 0, 255)
        arr[apply_disk, 2] = np.clip(arr[apply_disk, 2] + disk_b[apply_disk] * disk_int[apply_disk], 0, 255)
        arr[apply_disk, 3] = np.clip(arr[apply_disk, 3] + disk_int[apply_disk] * 255.0, 0, 255)
        
        # --- C. Photon Sphere & Einstein Lensing Ring (Luminous Circular Corona) ---
        photon_m = (dist >= r_photon_in - 0.5 * scale) & (dist <= r_photon_out)
        p_norm = 1.0 - np.abs(dist - (r_photon_in + r_photon_out) / 2.0) / ((r_photon_out - r_photon_in) / 2.0)
        p_int = np.clip(p_norm, 0, 1) ** 1.4
        
        # Fiery relativistic photon halo
        pulse_p = 0.88 + 0.15 * math.sin(phase * 2.0)
        pr = 255.0 * pulse_p
        pg = np.clip(225.0 - 70.0 * (dx / r_photon_out), 120, 255) * pulse_p
        pb = np.clip(160.0 - 140.0 * (dx / r_photon_out), 40, 255) * pulse_p
        
        arr[photon_m, 0] = np.clip(arr[photon_m, 0] + pr * p_int[photon_m], 0, 255)
        arr[photon_m, 1] = np.clip(arr[photon_m, 1] + pg[photon_m] * p_int[photon_m], 0, 255)
        arr[photon_m, 2] = np.clip(arr[photon_m, 2] + pb[photon_m] * p_int[photon_m], 0, 255)
        arr[photon_m, 3] = np.clip(arr[photon_m, 3] + p_int[photon_m] * 255.0, 0, 255)
        
        # --- D. Event Horizon (Pitch Black Vacuum Singularity) ---
        eh_m = dist < r_singularity
        # Pure opaque black
        arr[eh_m, 0] = 3.0
        arr[eh_m, 1] = 1.0
        arr[eh_m, 2] = 6.0
        arr[eh_m, 3] = 255.0
        
        # Gravitational shadow rim
        eh_edge = (dist >= r_singularity - 0.75 * scale) & (dist < r_singularity)
        arr[eh_edge, 0] = 15.0
        arr[eh_edge, 1] = 8.0
        arr[eh_edge, 2] = 28.0
        
        # --- E. Orbiting Graviton Packets / Relativistic Sparks ---
        for i in range(4):
            sp_ang = phase * 1.6 + i * (math.pi / 2.0)
            sp_r = (7.5 + 2.2 * math.sin(phase + i)) * scale
            sp_x = sp_r * math.cos(sp_ang)
            sp_y = sp_r * 0.62 * math.sin(sp_ang) # tilted
            sp_dist = np.sqrt((dx - sp_x)**2 + (dy - sp_y)**2)
            sp_m = (sp_dist < 1.15 * scale) & (dist <= r_disk_max)
            
            arr[sp_m, 0] = 255.0
            arr[sp_m, 1] = 245.0
            arr[sp_m, 2] = 200.0
            arr[sp_m, 3] = 255.0
            
        img_data = np.clip(arr, 0, 255).astype(np.uint8)
        frames.append(Image.fromarray(img_data, mode="RGBA"))
        
    return frames

def save_texture_package(name, frames_32, frames_64):
    # 1. Transparent Animated GIFs
    save_transparent_gif(frames_32, f"{OUT_DIR}/{name}_32.gif", duration=80)
    save_transparent_gif(frames_64, f"{OUT_DIR}/{name}_64.gif", duration=80)
    
    # 2. Vertical PNG strips (Minecraft format)
    strip_32 = Image.new("RGBA", (32, 32 * len(frames_32)))
    for i, f in enumerate(frames_32):
        strip_32.paste(f, (0, i * 32))
    strip_32.save(f"{OUT_DIR}/{name}_32_strip.png")
    
    strip_64 = Image.new("RGBA", (64, 64 * len(frames_64)))
    for i, f in enumerate(frames_64):
        strip_64.paste(f, (0, i * 64))
    strip_64.save(f"{OUT_DIR}/{name}_64_strip.png")
    
    # 3. .mcmeta files
    mcmeta_content = """{
  "animation": {
    "frametime": 2,
    "interpolate": true
  }
}
"""
    with open(f"{OUT_DIR}/{name}.png.mcmeta", "w") as mf:
        mf.write(mcmeta_content)
        
    print(f"Successfully generated package for {name}!")

if __name__ == "__main__":
    lens_32 = create_laser_lens(32, NUM_FRAMES)
    lens_64 = create_laser_lens(64, NUM_FRAMES)
    save_texture_package("laser_lens_special", lens_32, lens_64)
    
    boson_32 = create_stable_boson_containment_unit(32, NUM_FRAMES)
    boson_64 = create_stable_boson_containment_unit(64, NUM_FRAMES)
    save_texture_package("stable_boson_containment_unit", boson_32, boson_64)
    
    grav_32 = create_graviton_anomaly(32, NUM_FRAMES)
    grav_64 = create_graviton_anomaly(64, NUM_FRAMES)
    save_texture_package("graviton_anomaly", grav_32, grav_64)
