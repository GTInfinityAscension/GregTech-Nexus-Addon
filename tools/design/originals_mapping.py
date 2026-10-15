"""Role-based vanilla -> GTNH casing mapping per build. Keys are texture ids from gt_tex.pkl."""
import re
DROP = re.compile(r'warpdrive:air_|torch|lever|button|pressure_plate|flower|dandelion|poppy|wheat|carrots|potatoes|grass|_bed$|snow_layer|suspicious_gravel')
COMMON = [
    (r'glass|_pane$', 'gtceu:transparent/fusion_glass'),
    (r'froglight|end_rod|sea_lantern|lamp|glowstone', 'gtna:casings/plasma_heater_casing'),
]
BUILDS = {
  'bfg': [  # railgun: white hull, dark armor panels, green energy cells, black barrel trim
    (r'white_concrete$|white_terracotta|light_gray_terracotta|light_gray_concrete', 'gtceu:solid/machine_casing_clean_stainless_steel'),
    (r'cracked_deepslate_bricks', 'gtna:casings/radiant_naquadah_alloy_casing'),
    (r'deepslate_(copper|coal)_ore|coal_ore|copper', 'gtceu:pipe/machine_casing_pipe_tungstensteel'),
    (r'deepslate|tuff|basalt|cobble|stone|gray_terracotta|mud', 'gtceu:solid/machine_casing_inert_ptfe'),
    (r'black_concrete', 'gtna:casings/neutronium_stable_casing'),
    (r'slime|green|lime|melon|moss|mycelium', 'gtna:casings/dyson_deployment_core'),
    (r'furnace|smoker|crafter|piston', 'gtceu:unique/heat_vent'),
    (r'cyan', 'gtna:casings/molecular_casing'),
    (r'soul|netherite', 'gtna:extreme_density_casing'),
    (r'purpur|pink', 'gtna:casings/magtech_casing'),
  ],
  'portal': [  # dimensional gate: DTPF-blue body, spatial spikes, light injection ring, energy veins
    (r'_wall$', 'gtceu:fusion/fusion_coil'),
    (r'stone_brick_(stairs|slab)', 'gtna:eye_of_harmony/spatial'),
    (r'stone_brick', 'gtna:casings/dimensionally_transcendent_casing'),
    (r'andesite', 'gtna:casings/dimension_injection_casing'),
    (r'sculk', 'gtna:dimensional_stability_casing'),
    (r'copper', 'gtna:advanced_compressed_fusion_coil'),
  ],
  'litematic_27971': [  # orbital ring station with plasma core
    (r'quartz', 'gtna:casings/nano_forge/precision_field_sync_casing'),
    (r'white_concrete', 'gtceu:solid/machine_casing_clean_stainless_steel'),
    (r'(magenta|purple)_stained_glass', 'gtna:casings/hsss_borosilicate_glass'),
    (r'(blue|cyan)_stained_glass', 'gtna:casings/nano_forge/nanite_shielding_glass'),
    (r'tinted_glass', 'gtna:casings/cosmic_neutronium_borosilicate_glass'),
    (r'white_stained_glass', 'gtceu:transparent/fusion_glass'),
    (r'cyan_terracotta|gray_concrete', 'gtna:casings/molecular_casing'),
    (r'pale_oak|diorite_wall|tuff_wall|iron_bars', 'gtna:casings/high_strength_support_spindle'),
    (r'amethyst|pale_moss|calcite', 'gtna:casings/magtech_casing'),
  ],
  'schematic_20061': [  # WarpDrive sphere ship
    (r'hull\.superior\.glass', 'gtna:casings/plasma_field_glass'),
    (r'hull\.superior\.plain#15', 'gtna:casings/neutronium_stable_casing'),
    (r'hull\.superior\.plain', 'gtna:casings/radiant_naquadah_alloy_casing'),
    (r'chisel|blockcraftery|techguns|atum', 'gtceu:solid/machine_casing_robust_tungstensteel'),
    (r'cable|duct|transmitter|computercraft:cable', 'gtceu:pipe/machine_casing_pipe_tungstensteel'),
    (r'fusion|electromagnet', 'gtceu:fusion/fusion_coil'),
    (r'plasma|engine_exhaust', 'gtna:casings/plasma_heater_casing'),
    (r'concrete', 'gtceu:solid/machine_casing_clean_stainless_steel'),
    (r'mekanism|nuclearcraft|appliedenergistics2|thermal|woot|warpdrive|matteroverdrive|elevatorid|ae2stuff|powersuits|metalchests', 'gtna:casings/universal_factory_casing'),
  ],
}
def lum(c): return 0.3 * c[0] + 0.59 * c[1] + 0.11 * c[2]
def gt(build, name, meta, vanilla_rgba):
    key = name + ('#%d' % meta if meta is not None else '')
    if DROP.search(name): return None
    for pat, tex in BUILDS[build] + COMMON:
        if re.search(pat, key): return tex
    l = lum(vanilla_rgba)
    return ('gtceu:solid/machine_casing_clean_stainless_steel' if l > 170 else
            'gtceu:solid/machine_casing_solid_steel' if l > 95 else 'gtceu:solid/machine_casing_inert_ptfe')
