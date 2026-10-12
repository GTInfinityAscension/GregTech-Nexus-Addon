"""Builds tools/multiblock_tooltips/number_claims.json: for every number in a ▸ line, the file and regex that prove it.

Paths are relative to the GTNA repo, or start with "gtceu:" for the GTCEu 7.5.3 checkout.
"""
import json
from pathlib import Path

D = "src/main/java/com/raishxn/gtna/"
M = D + "common/data/GTNAMachines.java"
M2 = D + "common/data/GTNAMachines2.java"
M3 = D + "common/data/GTNAMachines3.java"
MEGA = D + "common/data/GTNAMegaMachines.java"
MOD = D + "common/data/GTNAModules.java"
BAL = D + "config/GTNABalance.java"
REC = D + "data/recipe/GTNAMachineRecipes.java"
ST = D + "common/machine/multiblock/steam/"
EL = D + "common/machine/multiblock/module/steamElevator/"
EN = D + "common/machine/multiblock/energy/"
EC = D + "common/machine/multiblock/electric/"
NE = D + "common/machine/multiblock/noenergy/"
BASE = D + "common/machine/multiblock/multiMachineBase/SteamMultiMachineBase.java"
COIL = EC + "CoilWorkableElectricMultipleRecipesMachine.java"
GTMOD = "gtceu:com/gregtechceu/gtceu/common/data/GTRecipeModifiers.java"
GTOC = "gtceu:com/gregtechceu/gtceu/api/recipe/OverclockingLogic.java"
GTROTOR = "gtceu:com/gregtechceu/gtceu/api/machine/feature/multiblock/IRotorHolderMachine.java"
GTPAR = "gtceu:com/gregtechceu/gtceu/common/machine/multiblock/part/ParallelHatchPartMachine.java"

C = {}


REPO = Path(__file__).resolve().parents[2]


def resolve(path):
    """Fixes a claim path whose package guess is wrong by locating the class file by name."""
    if path.startswith("gtceu:") or (REPO / path).exists():
        return path
    hits = sorted((REPO / "src/main/java").rglob(Path(path).name))
    if len(hits) != 1:
        raise SystemExit(f"cannot resolve claim file {path}: {hits}")
    return str(hits[0].relative_to(REPO))


def c(mid, num, path, pattern, expr):
    # Every claim of a number must hold (e.g. "2x speed" and "high pressure 2x" are two claims for "2").
    claims = C.setdefault(mid, {}).setdefault(str(num), [])
    entry = {"file": resolve(path), "pattern": pattern, "expr": expr}
    if entry not in claims:
        claims.append(entry)


HP = (BASE, r"HIGH_PRESSURE_DURATION_MULTIPLIER", "high pressure halves duration (2x speed, steam per tick unchanged -> 2x rate)")


def steam(mid, cls, default, maxp, dur, speed):
    path = ST + cls + ".java"
    c(mid, speed, path, r"durationMultiplier\s*(?:=\s*|\()%s" % dur.replace(".", r"\."), f"durationMultiplier {dur} -> {speed}x")
    c(mid, default, path, r"targetParallel = %d;" % default, f"default targetParallel {default}")
    c(mid, maxp, path, r"Math\.min\(%d, this\.targetParallel \* 2\)" % maxp, f"max parallel {maxp}")
    c(mid, 2, *HP)


steam("large_steam_crusher", "LargeSteamCrusher", 8, 128, "0.5", 2)
steam("large_steam_furnace", "LargeSteamFurnace", 8, 128, "0.1", 10)
steam("large_steam_alloy_smelter", "LargeSteamAlloySmelter", 64, 64, "0.57", "1.75")
steam("large_steam_hammer", "LargeSteamHammer", 32, 64, "0.5", 2)
steam("large_steam_compressor", "LargeSteamCompressor", 24, 48, "0.4", "2.5")
steam("large_steam_extractor", "LargeSteamExtractor", 24, 48, "0.57", "1.75")
steam("large_steam_ore_washer", "LargeSteamOreWasher", 48, 96, "0.2", 5)
for mid, rt, p, dur in [("large_steam_mixer", "MIXER", 64, "0.5"), ("large_steam_centrifuge", "CENTRIFUGE", 64, "0.5"),
                        ("large_steam_thermal_centrifuge", "THERMAL_CENTRIFUGE", 64, "0.5"),
                        ("large_steam_bath", "CHEMICAL_BATH", 64, "0.5"), ("large_steam_lathe", "LATHE", 16, "0.5"),
                        ("large_steam_cutting", "CUTTER", 16, "0.5"), ("large_steam_bending", "BENDER", 16, "0.5"),
                        ("large_steam_extruder", "EXTRUDER", 16, "0.5"), ("large_steam_wiremill", "WIREMILL", 16, "0.5"),
                        ("large_steam_sifter", "SIFTER", 16, "0.5"), ("large_steam_forming_press", "FORMING_PRESS", 32, "0.4")]:
    c(mid, p, M, r"%s_RECIPES,\s*%d,\s*%d,\s*%s" % (rt, p, p, dur.replace(".", r"\.")), f"AdjustableSteamParallelMachine({rt}, {p}, {p}, {dur})")
    if dur == "0.5":
        c(mid, 2, *HP)  # both "2x speed" (0.5) and high pressure; 0.5 also proven by the pattern above
    else:
        c(mid, "2.5", M, r"FORMING_PRESS_RECIPES,\s*32,\s*32,\s*0\.4", "durationMultiplier 0.4 -> 2.5x")
        c(mid, 2, *HP)
c("large_steam_circuit_assembler", 4, ST + "LargeSteamCircuitAssembler.java", r"MAX_PARALLELS = 4;.*\n.*\n.*OUTPUT_MULTIPLIER = 2;\n.*DURATION_MULTIPLIER = 4", "MAX_PARALLELS 4, DURATION_MULTIPLIER 4")
c("large_steam_circuit_assembler", 2, ST + "LargeSteamCircuitAssembler.java", r"OUTPUT_MULTIPLIER = 2", "OUTPUT_MULTIPLIER 2 (+ high pressure 2x)")
c("large_steam_circuit_assembler", 16, ST + "LargeSteamCircuitAssembler.java", r"ENGRAVING_NEEDED = 16", "ENGRAVING_NEEDED 16")

R = REC
c("steam_cactus_wonder", 8000, R, r"Items\.COAL\), 8_000", "cactusWonder coal 8,000")
c("steam_cactus_wonder", 90000, R, r"Items\.COAL_BLOCK\), 90_000", "cactusWonder coal block 90,000")
c("steam_cactus_wonder", 1, R, r"outputFluids\(GTMaterials\.Steam\.getFluid\(steam\)\)\s*\.duration\(20\)", "duration 20 ticks = 1 s")
c("steam_cobbler", 16, ST + "SteamCobbler.java", r"targetParallel = 16;[\s\S]*Math\.min\(16,", "parallel 16 / max 16")
c("steam_cracking", 8, ST + "SteamCracking.java", r"isHighPressure\(\) \? 16 : 8", "8 bronze / 16 steel")
c("steam_cracking", 16, ST + "SteamCracking.java", r"isHighPressure\(\) \? 16 : 8", "8 bronze / 16 steel")
for n, pat in [(16384000, r"SLOTS = 256;\s*private static final int SLOT_LIMIT = 64_000"), (256, r"SLOTS = 256"), (64000, r"SLOT_LIMIT = 64_000")]:
    c("steam_item_vault", n, ST + "SteamItemVaultMachine.java", pat, "256 slots x 64,000")
c("steam_lava_maker", 1, D + "data/recipe/GTNALavaMakerRecipes.java", r"\.duration\(20\)", "lava recipe duration 20 ticks = 1 s")
c("steam_lava_maker", 16, ST + "SteamLavaMakerMachine.java", r"targetParallel = 16;[\s\S]*Math\.min\(16,", "parallel 16 / max 16")
c("steam_lava_maker", 2, *HP)
c("steam_manufacturer", 16, ST + "SteamManufacturer.java", r"targetParallel = 16;[\s\S]*Math\.min\(16,", "parallel 16 / max 16")
c("steam_mega_compressor", 256, ST + "MegaSteamCompressor.java", r"getParallelAmount\(machine, recipe, 256\)", "parallel 256")
c("steam_mega_compressor", 2, ST + "MegaSteamCompressor.java", r"durationMultiplier\(0\.5\)", "durationMultiplier 0.5 -> 2x")
c("steam_mega_compressor", 64, REC, r"LARGE_STEAM_COMPRESSOR\.asStack\(\)\.getItem\(\), 64\)", "manufacturer recipe uses 64 Large Steam Compressors")
c("steam_woodcutter", 64, ST + "SteamWoodcutter.java", r"targetParallel = 64;[\s\S]*Math\.min\(64,", "parallel 64 / max 64")
c("stone_superheater", 32, ST + "StoneSuperHeater.java", r"targetParallel = 32;[\s\S]*Math\.min\(32,", "parallel 32 / max 32")
c("large_steam_solar_boiler", 63, ST + "LargeSteamSolarBoilerMachine.java", r"MAX_SIDE = 63", "MAX_SIDE 63")
c("large_steam_solar_boiler", 125, ST + "LargeSteamSolarBoilerMachine.java", r"MAX_BACK = 125", "MAX_BACK 125")
c("large_steam_storage_tank", 120000000, ST + "LargeSteamStorageTank.java", r"CAPACITY = 120_000_000", "CAPACITY")
IC = NE + "InfernalCokeOven.java"
c("infernal_coke_oven", 1, IC, r"continuousWorkingTicks / 100\.0\) \* 0\.01", "+1% per 100 ticks (5 s)")
c("infernal_coke_oven", 5, IC, r"continuousWorkingTicks / 100\.0\) \* 0\.01", "100 ticks = 5 s")
c("infernal_coke_oven", 10, IC, r"Math\.min\(10\.0, bonus\)[\s\S]*|TICKS_PER_STAGE = 10 \* 60 \* 20", "bonus cap 10x; stage every 10 min")
c("infernal_coke_oven", 16, IC, r"PARALLEL_INCREASE = 16", "PARALLEL_INCREASE")
c("infernal_coke_oven", 8, IC, r"BASE_PARALLEL = 8", "BASE_PARALLEL")
c("infernal_coke_oven", 256, IC, r"MAX_PARALLEL_CAP = 256", "MAX_PARALLEL_CAP")
c("infernal_coke_oven", 6400, IC, r"BASE_STEAM_PER_TICK = 320", "320/t x 20 = 6,400 L/s")
c("infernal_coke_oven", 1600, IC, r"STEAM_INCREASE_PER_STAGE = 80", "80/t x 20 = 1,600 L/s")
c("primitive_distillation_tower", 75, ST + "PrimitiveSteamDistillationTowerMachine.java", r"return 0\.75", "steam multiplier 0.75")
c("primitive_stone_furnace", 1, NE + "PrimitiveStoneFurnaceMachine.java", r"RECIPE_DURATION = 1", "RECIPE_DURATION 1 tick")
c("dimensionally_transcendent_dirt_forge", 524288, NE + "DimensionallyTranscendentDirtForgeMachine.java", r"MAX_PARALLEL = 524288", "MAX_PARALLEL")
c("dimensionally_transcendent_dirt_forge", 1, NE + "DimensionallyTranscendentDirtForgeMachine.java", r"1\.0 / Math\.max\(1, recipe\.duration\)", "duration -> 1 tick")
c("dimensionally_transcendent_steam_boiler", 4096000, M, r"LargeBoilerMachine\(\s*holder, 4_096_000", "LargeBoilerMachine(4,096,000)")
OV = ST + "DimensionallyTranscendentSteamOvenMachine.java"
c("dimensionally_transcendent_steam_oven", 100, OV, r"524288, 524288, 0\.01, 2", "0.01 duration -> 100x")
c("dimensionally_transcendent_steam_oven", 2, OV, r"524288, 524288, 0\.01, 2", "2 threads")
c("dimensionally_transcendent_steam_oven", 524288, OV, r"524288, 524288", "parallel 524,288")
LF = ST + "LeapForwardBlastFurnace.java"
c("leap_forward_one_blast_furnace", 32000, LF, r"MAX_PARALLEL_CAP = 32000", "cap 32,000")
c("leap_forward_one_blast_furnace", 20, LF, r"TICKS_PER_LAYER = 400", "400 ticks = 20 s per layer (base 400)")
HPR = ST + "HyperPressureReactor.java"
c("hyper_pressure_reactor", 1, HPR, r"isCompact \? 512 : 1", "parallel 1 (compact 512)")
c("hyper_pressure_reactor", 512, HPR, r"isCompact \? 512 : 1", "compact 512")
c("compact_hyper_pressure_reactor", 512, HPR, r"isCompact \? 512 : 1", "compact 512")
for n, pat, e in [(2, r"denseSteam = new VoidMinerSteamTierBalance\(2, 2\.0, 1\.5\)", "dense 2x/2x/1.5x"),
                  (3, r"superHeatedSteam = new VoidMinerSteamTierBalance\(3, 3\.0, 2\.0\)", "superheated 3x/3x/2x"),
                  (5, r"insanelySupercriticalSteam = new VoidMinerSteamTierBalance\(5, 5\.0, 4\.0\)", "insanely 5x/5x/4x"),
                  ("1.5", r"VoidMinerSteamTierBalance\(2, 2\.0, 1\.5\)", "dense EU 1.5x"),
                  (4, r"VoidMinerSteamTierBalance\(5, 5\.0, 4\.0\)", "insanely EU 4x")]:
    c("void_miner_steam_gate_aged", n, BAL, pat, e)
c("steam_elevator", 12, ST.replace("steam/", "module/steamElevator/") + "SteamElevator.java",
  r"MODULE_OFFSETS = \{\s*\{ 0, -8, -5 \}, \{ 0, -8, -3 \}, \{ 0, -8, -1 \},\s*\{ 0, -2, -11 \}, \{ 0, -2, 5 \},\s*\{ 0, 0, -11 \}, \{ 0, 0, 5 \},\s*\{ 0, 2, -11 \}, \{ 0, 2, 5 \},\s*\{ 0, 8, -5 \}, \{ 0, 8, -3 \}, \{ 0, 8, -1 \},",
  "12 module offsets")
for t, r in ((1, 64), (2, 128), (3, 192)):
    mid = "steam_elevator_flight_module_" + "i" * t
    c(mid, r, EL + "SteamFlightModule.java", r"RANGE \* Math\.max\(1, getModuleTier\(\)\)", f"RANGE 64 x tier {t}")
    mid = "steam_elevator_weather_module_" + "i" * t
    c(mid, t, EL + "SteamWeatherModule.java", r"WEATHER_TIME \* Math\.max\(1, getModuleTier\(\)\)", f"72,000 ticks (1 h) x tier {t}")
    c(mid, 1000000, EL + "SteamWeatherModule.java", r"WEATHER_STEAM_COST = 1_000_000L", "1,000,000 mB")
for t, (y, cyc) in ((2, (250, 1200)), (3, (500, 600)), (4, (1000, 400))):
    mid = "steam_elevator_oil_drill_module_" + "i" * (t - 1)
    c(mid, t - 1, EL + "SteamOilDrillModule.java", r"for \(int i = 0; i < getModuleTier\(\) - 1; i\+\+\)", "fluid types = tier - 1")
    c(mid, y, EL + "SteamOilDrillModule.java", r"250 \* \(1 << Math\.max\(0, getModuleTier\(\) - 2\)\)", "250 * 2^(tier-2)")
    c(mid, cyc, EL + "SteamOilDrillModule.java", r"1200 / \(getModuleTier\(\) - 1\)", "1200 / (tier-1)")
for t, cyc in ((1, 400), (2, 200), (3, 100)):
    mid = "steam_elevator_entity_crusher_module_" + "i" * t
    f = EL + "SteamEntityCrusherModule.java"
    c(mid, 2, f, r"BASE_DOUBLING_CHANCE = 2\.0", "2%")
    c(mid, "0.5", f, r"CHANCE_PER_SPAWNER = 0\.5", "0.5% per spawner")
    c(mid, 34, f, r"MAX_DOUBLING_CHANCE = 34\.0", "cap 34%")
    c(mid, cyc, f, r"tier I/II/III = 400/200/100 ticks", "400/200/100 ticks")
G = EL + "SteamGreenhouseModule.java"
c("steam_elevator_greenhouse_module", 16, G, r"RANGE = 16;[\s\S]*\+\+grown >= 16", "range 16, 16 crops")
c("steam_elevator_greenhouse_module", 16000, G, r"WATER_PER_OPERATION = 16_000", "16,000 mB")
c("steam_elevator_greenhouse_module", 60, G, r"CYCLE_TICKS = 1200", "1200 ticks = 60 s")
O = EL + "SteamOreProcessorModule.java"
c("steam_elevator_ore_processor_module", 8, O, r"return 8 << clampMode\(mode\)", "8 x circuit multiplier")
c("steam_elevator_ore_processor_module", 128, O, r"STEAM_UPKEEP = 128", "128 mB/t x multiplier")
for t, r in ((1, 64), (2, 128), (3, 256)):
    mid = "steam_elevator_monster_repellent_module_" + "i" * t
    c(mid, r, EL + "SteamMonsterRepellentModule.java", r"return 1 << \(5 \+ getModuleTier\(\)\)", "1 << (5 + tier)")
    mid = "steam_elevator_beacon_module_" + "i" * t
    c(mid, r, EL + "SteamBeaconModule.java", r"case %d -> %d;" % (t, r), f"range {r}")
    c(mid, 10, EL + "SteamBeaconModule.java", r"GTNL's 12 effects minus the three", "10 effects in ALL_EFFECTS")
A = EL + "SteamApiaryModule.java"
c("steam_elevator_apiary_module", 8, A, r"base 8-bee colony", "base colony 8")
c("steam_elevator_apiary_module", 300, A, r"CYCLE_TICKS = 6000", "6000 ticks = 300 s")
c("steam_elevator_apiary_module", 1000, A, r"WATER_PER_CYCLE = 1000", "1000 mB")
B = EL + "SteamBeeBreedingModule.java"
c("steam_elevator_bee_breeding_module", 128, B, r"FEED_CONSUMED = 128", "128 per operation")
c("steam_elevator_bee_breeding_module", 10, B, r"CYCLE_TICKS = 12000", "12000 ticks = 10 min")

# GTO / electric
c("isa_mill", 4, M3, r'multiblock\("isa_mill"[\s\S]{0,200}OC_PERFECT', "perfect overclock: duration / 4")
c("isa_mill", 2, D + "common/machine/multiblock/electric/IsaMillParallel.java", r"getParallelAmount\(machine, recipe, 2\)", "parallel 2")
c("isa_mill", 1, D + "data/recipe/GTNAIsaMillRecipes.java", r"circuitMeta\(ballTier == 2 \? 10 : 1\)", "circuit 1 / 10")
c("isa_mill", 10, D + "data/recipe/GTNAIsaMillRecipes.java", r"circuitMeta\(ballTier == 2 \? 10 : 1\)", "circuit 1 / 10")
c("chemical_plant", 4, EC + "ChemicalPlantMachine.java", r"perfect overclock", "perfect overclock / 4")
c("chemical_plant", 5, EC + "ChemicalPlantMachine.java", r"1 - plant\.getCoilTier\(\) \* 0\.05", "-5% per coil tier")
GA = EN + "GeneratorArrayMachine.java"
c("generator_array", "1.3", GA, r"OUTPUT_MULTIPLIER = 1\.3", "1.3x")
c("generator_array", 4, GA, r"MAX_GENERATORS = 4", "4 generators")
c("generator_array", 5, GA, r"WIRELESS_LOSS_PERCENT = 5", "5% loss")
for mid, cls in (("cold_ice_freezer", "ColdIceFreezerMachine"), ("blaze_blast_furnace", "BlazeBlastFurnaceMachine")):
    f = EC + cls + ".java"
    c(mid, "0.5", f, r"\.durationMultiplier\(0\.5\)", "0.5 duration")
    c(mid, 64, f, r"getParallelAmount\(machine, recipe, 64\)", "parallel 64")
    c(mid, 2, f, r"\(1 << Math\.max\(0, Math\.min\(20, getTier\(\) - 2\)\)\) \* 10", "2^(tier-2) x 10")
    c(mid, 10, f, r"\(1 << Math\.max\(0, Math\.min\(20, getTier\(\) - 2\)\)\) \* 10", "2^(tier-2) x 10")
c("mega_alloy_blast_smelter", "0.8", EC + "MegaAlloyBlastSmelterMachine.java", r"\.eutMultiplier\(0\.8\)", "0.8 EU")
c("mega_alloy_blast_smelter", "0.6", EC + "MegaAlloyBlastSmelterMachine.java", r"\.durationMultiplier\(0\.6\)", "0.6 duration")
FG = EC + "FishingGroundMachine.java"
for n in (1, 2, 3, 4):
    c("fishing_ground", n, FG, r"if \(circuit < 1 \|\| circuit > 4\) return null;", "circuits 1-4")
c("evaporation_plant", 5, M3, r'"X#X", "XXX"\)\.setRepeatable\(5\)', "5 tower stages")
c("evaporation_plant", 4, GTPAR, r"Math\.pow\(4, tier - GTValues\.EV\)", "IV parallel hatch = 4^(IV-EV) = 4")
c("component_assembler", 2, MOD, r"registerComponentAssemblerExtensionWide|buildComponentAssemblerExtensionWide", "second extension pattern")
RT = EC + "GTNALargeTurbineMachine.java"
for mid in ("rocket_large_turbine", "supercritical_steam_turbine"):
    c(mid, 10, GTROTOR, r"return 100 \+ 10 \* tierDifference;", "+10% efficiency per rotor tier")
    c(mid, 2, GTROTOR, r"Math\.pow\(2, getTierDifference\(\)\)", "2x power per rotor tier (module 2x per GTNAModules)")
    c(mid, 20, MOD, r"2× output, \+20% efficiency", "module +20% efficiency")
c("rocket_large_turbine", 5120, M3, r"RocketLargeTurbineMachine\(holder, GTValues\.EV", "V[EV] * 2.5 = 5,120")
c("rocket_large_turbine", 3, RT, r"HIGH_SPEED_OUTPUT_MULTIPLIER = 3\.0F", "high speed 3x")
c("rocket_large_turbine", 10, RT, r"HIGH_SPEED_ROTOR_DAMAGE = 10", "10x rotor damage")
c("supercritical_steam_turbine", 16384, EC + "SupercriticalSteamTurbineMachine.java", r"V\[IV\] \* 2 = 16384", "V[IV] * 2")
c("industrial_flotation_cell", 4, EC + "IndustrialFlotationCellMachine.java", r"divides the duration by 4", "perfect overclock / 4")
VD = EC + "VacuumDryingFurnaceMachine.java"
c("vacuum_drying_furnace", 2, VD, r"parallel \{@code 2\^floor\(coilTemp / 900\)\}", "2^floor(coil/900)")
c("vacuum_drying_furnace", 900, VD, r"parallel \{@code 2\^floor\(coilTemp / 900\)\}", "every 900K")
c("advanced_fusion_reactor", 160, EC + "AdvancedFusionReactorMachine.java", r"energyInputs \* \(1L << \(tier - GTValues\.LuV\)\) \* 10_000_000L", "16 inputs x 10M at LuV = 160M")
c("advanced_fusion_reactor", 4, EC + "AdvancedFusionReactorMachine.java", r"TIER_EXTENSIONS = 4", "4 extensions")
c("large_cracker", 10, GTMOD, r"1\.0 - coilMachine\.getCoilTier\(\) \* 0\.1", "-10% EU per coil tier; EternalCoil tier 9 -> 10%")
for mid in ("cracker_hub", "mega_brewer", "mega_vacuum_drying_furnace", "phase_change_cube", "magnetic_energy_reaction_furnace",
            "particle_stream_matrix_filling_machine", "mega_wiremill", "crystal_builder"):
    c(mid, 2, COIL, r"coilType\.getCoilTemperature\(\) / 900\);\s*int coilParallel = exponent >= 30 \? Integer\.MAX_VALUE : 1 << exponent", "2^(coil/900)")
    c(mid, 900, COIL, r"getCoilTemperature\(\) / 900", "every 900K")
c("super_blast_smelter", 100, COIL, r"\+ 100 \* Math\.max\(0, getTier\(\) - 2\)", "+100K per tier above MV")
c("engraving_laser_plant", 4, MEGA, r"GTRecipeModifiers\.OC_PERFECT", "perfect overclock / 4")
c("engraving_laser_plant", 1, MEGA, r"PRECISION_LASER_ENGRAVER_RECIPES \?\s*com\.gregtechceu\.gtceu\.api\.recipe\.modifier\.ModifierFunction\.IDENTITY", "precision runs unmodified (parallel 1)")
c("infinity_fluid_drilling_rig", 256, MEGA, r"InfinityFluidDrillMachine\(holder, GTValues\.ZPM, 256\)", "basis 256")
c("infinity_fluid_drilling_rig", 384, MEGA, r"InfinityFluidDrillMachine\(holder, GTValues\.ZPM, 256\)", "256 x 1.5 above rig tier (class doc)")
c("infinity_fluid_drilling_rig", 0, EC + "InfinityFluidDrillMachine.java", r"without depletion", "no depletion")
c("thermal_power_pump", 50, EN + "ThermalPowerPumpMachine.java", r"\* 3 / 2\} in rain", "x3/2 in rain")
c("annihilate_generator", 4, EN + "ArtificialStarMachine.java", r"resultVoltage \* 4;[\s\S]{0,200}resultDuration / 4", "x4 voltage, /4 duration")
c("annihilate_generator", 16, M, r"abilities\(OUTPUT_ENERGY\)\.setMaxGlobalLimited\(16\)", "16 dynamo hatches")

# endgame / misc
c("forge_of_gods", 8, D + "api/machine/feature/godforge/GodforgeMath.java", r"int max = 8;", "8 base")
c("forge_of_gods", 16, D + "api/machine/feature/godforge/GodforgeMath.java", r"max \+= 4;\s*if \(data\.isUpgradeActive\(END\)\) max \+= 4;", "8 + 4 + 4")
EM = D + "api/machine/feature/eyeofharmony/EyeOfHarmonyMath.java"
c("eye_of_harmony", 0, EM, r"Math\.min\(24, circuitSetting\)", "circuit 0-24")
c("eye_of_harmony", 24, EM, r"Math\.min\(24, circuitSetting\)", "circuit 0-24")
c("eye_of_harmony", 4, EM, r"shiftLeft\(2 \* circuit\)", "x4 per circuit level")
c("eye_of_harmony", 1000000, EM, r"1_000_000_000L, blockRocketTier \+ 1L", "10^9 mB x (tier+1); Overworld = 1,000,000 buckets")
PF = EC + "PlasmaForgeMachine.java"
c("dimensionally_transcendent_plasma_forge", 50, PF, r"MAXIMUM_DISCOUNT = 0\.5d", "up to 50%")
c("dimensionally_transcendent_plasma_forge", 8, PF, r"after 8", "8 hours")
c("dimensionally_transcendent_plasma_forge", 100, PF, r"DECAY_PER_TICK = 100", "decay 100x")
c("dimensionally_transcendent_plasma_forge", 1250, D + "common/data/GTNAPlasmaForge.java", r"setMinGlobalLimited\(1250\)", "1250 casings")
c("dimensionally_transcendent_plasma_forge", 2, D + "common/data/GTNAPlasmaForge.java", r"INPUT_ENERGY\)\.setMaxGlobalLimited\(2\)", "2 energy hatches")
c("dimensionally_transcendent_plasma_forge", 1, D + "common/data/GTNAPlasmaForge.java", r"INPUT_LASER\)\.setMaxGlobalLimited\(1\)", "1 laser")
c("transcendent_plasma_mixer", 10, EC + "TranscendentPlasmaMixerMachine.java", r"getLong\(EU_MULTIPLIER\) : 10", "default multiplier 10")
for n in (1, 2, 3):
    c("nano_forge", n, D + "common/data/GTNANanoForge.java", r"CARBON_NANITES\.get\(\), NEUTRONIUM_NANITES\.get\(\), TRANSCENDENT_METAL_NANITES\.get\(\)", "nanite tiers 1-3")
HC = EN + "NexusMEHyperCoreMachine.java"
c("nexus_me_hypercore", 320, HC, r"TOTAL_MODULE_SLOTS = 320", "320 slots")
for n, pat in ((4, r"MODULE_I_THREADS = 4L"), (16, r"MODULE_II_THREADS = 16L"), (128, r"MODULE_III_THREADS = 128L"), (1024, r"MODULE_IV_THREADS = 1024L")):
    c("nexus_me_hypercore", n, HC, pat, "threads per module tier")
c("nexus_me_hypercore", 2, HC, r"transcendentMode = matrixIV == TOTAL_MODULE_SLOTS", "44x22x44 is the structure size; 'tier IV' from matrixIV")
c("nexus_flux_matrix", 750, EN + "NexusFluxMatrixMachine.java", r"totalCapacitors == 750 && sumTiers == 750 \* GTValues\.MAX", "750 MAX capacitors")
c("nexus_molecular_forge", 1, EN + "NexusMolecularForgeMachine.java", r"Math\.max\(1L, Math\.min\(maxEUt, totalItems\)\)", "1 EU per item")
c("me_storage", 128, M, r'"CBC", "cHc", "cHc", "cHc", "CBC"\)\.setRepeatable\(1, 128\)', "up to 128 sections")
c("universal_factory", 32, M,
  r'multiblock\("universal_factory", UniversalFactoryMachine::new\)\s*\.\w+\([^)]*\)\s*(?:\.recipeType\(GTRecipeTypes\.\w+\)\s*){32}(?!\.recipeType)',
  "exactly 32 consecutive .recipeType(...) calls in the registration")
EV = EC + "ElectricVoidMinerMachine.java"
c("electric_void_miner", 1, D + "data/recipe/VoidMinerEssenceRecipes.java", r"circuitMeta\(1\)", "circuit 1 programs")
c("electric_void_miner", 2, D + "data/recipe/VoidMinerEssenceRecipes.java", r"circuitMeta\(2\)", "circuit 2 programs")
c("incubator", 10000, D + "data/recipe/VoidMinerEssenceRecipes.java", r"Biomass\.getFluid\(10000\)\)\s*\.inputFluids\(GTMaterials\.Milk\.getFluid\(10000\)\)", "10,000 mB each")
c("incubator", 64, D + "data/recipe/VoidMinerEssenceRecipes.java", r"outputItems\(essence, 64\)", "64 essences")
SH = EN + "IndustrialSlaughterhouse.java"
c("industrial_slaughterhouse", 3, SH, r"multiplierBase = 3", "boss x3")
c("industrial_slaughterhouse", 5, SH, r"multiplierBase = 5", "dragon x5")
for n in (1, 2, 3, 4):
    c("industrial_slaughterhouse", n, SH, r"case 2 ->[\s\S]*case 3 ->[\s\S]*case 4 ->", "circuits 1-4 (default = 1)")
for n, pat in ((1000, r'slaughterhouse_passive"\)[\s\S]{0,300}\.EUt\(1000\)'), (2560, r'slaughterhouse_hostile"\)[\s\S]{0,300}\.EUt\(2560\)'),
               (32, r'slaughterhouse_boss"\)[\s\S]{0,300}\.EUt\(32000\)'), (120, r'slaughterhouse_ender_dragon"\)[\s\S]{0,300}\.EUt\(120000\)')):
    c("industrial_slaughterhouse", n, REC, pat, "slaughterhouse recipe EU/t")
c("integrated_ore_processor", 1, D + "data/recipe/IntegratedOreRecipes.java", r"circuitMeta\(1\)", "circuit 1")
c("integrated_ore_processor", 7, D + "data/recipe/IntegratedOreRecipes.java", r"circuitMeta\(7\)", "circuit 7")
c("advanced_integrated_ore_processor", 2147483647, EC + "AdvancedIntegratedOreProcessorMachine.java", r"return Integer\.MAX_VALUE;", "Integer.MAX_VALUE")
EW = D + "common/machine/multiblock/electric/EyeOfWoodMachine.java"
c("eye_of_wood", 75, EW, r"SUCCESS_BASE = 7500", "7500 / 10,000")
c("eye_of_wood", 256000, EW, r"STANDARD_WATER = 256_000;\s*private static final int STANDARD_LAVA = 256_000", "256,000 each")
c("eye_of_wood", 60, EW, r"DURATION = 1200", "1200 ticks = 60 s")
c("eye_of_wood", 270000000, EW, r"return 36_000 \* Math\.max\(1, successChance\)", "36,000 x 7,500")
PCB = EC + "PCBFactoryMachine.java"
c("pcb_factory", 1, PCB, r"return tier < 2 \? TIER_1_MAX_EUT", "tier 1 uses TIER_1_MAX_EUT")
c("pcb_factory", 30719, PCB, r"TIER_1_MAX_EUT = 30719", "tier 1 cap")
c("pcb_factory", 2, PCB, r"tier < 3 \? TIER_2_MAX_EUT", "tier 2 uses TIER_2_MAX_EUT")
c("pcb_factory", 491519, PCB, r"TIER_2_MAX_EUT = 491519", "tier 2 cap")
HR = EC + "HyperReactorMachine.java"
c("hyper_reactor", 16, HR, r"DEFAULT_BOOST = 16", "default booster parallel")
c("advanced_hyper_reactor", 16, HR, r"DEFAULT_BOOST = 16", "default booster parallel")
FC = EC + "FuelCellGeneratorMachine.java"
c("fuel_cell_generator", 50, FC, r"MAX_RELEASE_PARALLEL = 50", "release parallel cap")
c("fuel_cell_generator", 600, FC, r"RECOVERY_WATER = 600", "distilled water per idle tick")
c("fuel_cell_generator", 0.35, FC, r"MEMBRANE_DAMAGE_CHANCE = 0\.0035d", "0.0035 = 0.35%")
SC = EC + "SupercomputingCenterMachine.java"
c("supercomputing_center", 1, SC, r"if \(machineTier == 1\) upkeepEUt /= 4", "tier 1")
c("supercomputing_center", 2, SC, r"tier == 2 \? GTNACircuits\.OPTICAL_MAINFRAME", "tier 2 mainframe")
c("supercomputing_center", 3, SC, r"tier == 3 \? GTNACircuits\.EXOTIC_MAINFRAME", "tier 3 mainframe")
c("data_center", 16, MEGA, r"OPTICAL_DATA_TRANSMISSION\)\.setMaxGlobalLimited\(16, 1\)", "transmission hatches")
c("data_center", 4, MEGA, r"OPTICAL_DATA_RECEPTION\)\.setMaxGlobalLimited\(4, 1\)", "reception hatches")

EOH_MATH = D + "api/machine/feature/eyeofharmony/EyeOfHarmonyMath.java"
DATA_BANK = "gtceu:com/gregtechceu/gtceu/common/machine/multiblock/electric/research/DataBankMachine.java"
for eut, voltage in ((1920, "EV"), (30720, "LuV")):
    c("data_center", eut, DATA_BANK, rf"GTValues\.VA\[GTValues\.{voltage}\]", f"Data Bank hatch upkeep VA[{voltage}]")
    c("data_center", eut, "gtceu:com/gregtechceu/gtceu/api/GTValues.java",
      r"int\[\] VA = \{ 7, 30, 120, 480, 1920, 7680, 30720,", "VA table: EV=1920, LuV=30720")
c("eye_of_harmony", 3, EOH_MATH, r"double base = 0\.97;", "compression time multiplier 0.97 per excess tier")
c("eye_of_harmony", 50, EOH_MATH, r"Math\.pow\(2, -fields\.acceleration\)", "time halved per acceleration tier")
c("eye_of_harmony", 5, EOH_MATH,
  r"fields\.stabilisation \* 0\.05", "stabilisation adds 5 percentage points of chance and removes 5% yield per tier")
c("eye_of_harmony", "9.25", EOH_MATH, r"fields\.acceleration \* 0\.0925", "acceleration removes 9.25 percentage points of chance per tier")
c("fuel_cell_generator", 15, FC, r"DECAY_RECOVERY = 0\.15d", "idle water recovers 15% of lost efficiency per tick")
for route in range(1, 8):
    c("integrated_ore_processor", route, D + "data/recipe/IntegratedOreRecipes.java",
      rf"\.circuitMeta\({route}\)", f"processing route {route}")
for suffix in ("i", "ii", "iii"):
    for setting, mode in ((1, "CLEAR"), (2, "RAIN"), (3, "THUNDER")):
        c("steam_elevator_weather_module_" + suffix, setting, EL + "SteamWeatherModule.java",
          rf"case {setting} -> MODE_{mode};", f"circuit {setting} selects {mode.lower()}")

# Coil parallel uses the base temperature (not the voltage-adjusted heating temperature).
for mid in ("cracker_hub", "mega_brewer", "mega_vacuum_drying_furnace", "phase_change_cube",
            "magnetic_energy_reaction_furnace", "particle_stream_matrix_filling_machine", "mega_wiremill",
            "crystal_builder", "gemini_containment_system", "giant_electrochemical_workstation", "desulfurizer",
            "dimensional_focus_engraving_array", "heavy_rolling"):
    c(mid, 2, COIL, r"int coilParallel = exponent >= 30 \? Integer.MAX_VALUE : 1 << exponent;",
      "coil parallel = 2^exponent, saturated at Integer.MAX_VALUE")
    c(mid, 900, COIL, r"int exponent = Math.max\(0, coilType.getCoilTemperature\(\) / 900\);",
      "exponent = floor(base coil temperature / 900)")

c("giant_sintering_array", 4, EC + "GiantSinteringArrayMachine.java", r"1 << \(2 \* glassTier\)",
  "glass parallel = 2^(2*tier) = 4^glass tier")

c("integrated_vapor_deposition_system", 4, EC + "GiantSinteringArrayMachine.java", r"1 << \(2 \* glassTier\)",
  "glass parallel = 4^glass tier (shared with GlassParallelMultipleRecipesMachine)")

Path(__file__).with_name("number_claims.json").write_text(json.dumps(C, indent=1) + "\n")
print(sum(len(v) for v in C.values()), "claims")
