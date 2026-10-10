# Multiblock tooltip verification (G-0240/G-0242)

Every ▸ number was checked against the code listed below. Every row was traced to the code cited. The "Unconfirmed numbers" column comes from the mechanical per-number trace in `multiblock-tooltips-trace.md` (`tools/trace_multiblock_tooltip_numbers.py`): 0 unconfirmed numbers.

| Machine | id | Flavor | Evidence in code | Unconfirmed numbers |
|---|---|---|---|---|
| Advanced Fusion Reactor MK-I | `advanced_fusion_reactor` | It simulates the eternal light. | AdvancedFusionReactorMachine.bufferCapacity(LuV,16)=160M, module rules | none |
| Advanced Integrated Ore Processor | `advanced_integrated_ore_processor` | Why process one ore when you can process all of them? | AdvancedIntegratedOreProcessorMachine Integer.MAX_VALUE; pattern INPUT_LASER only | none |
| Artificial Star | `annihilate_generator` | Let there be light. Lots of it. | ArtificialStarMachine 4x/÷4 OC loop; pattern OUTPUT_ENERGY max 16, OUTPUT_LASER | none |
| Blaze Blast Furnace | `blaze_blast_furnace` | An intern kept a blaze spawner in here. It worked. | BlazeBlastFurnaceMachine parallel 64, durationMultiplier 0.5 | none |
| Brick Kiln | `brick_kiln` | Bricks: the original building block. | pattern: item/fluid buses only, no energy hatch; GTNAMachineRecipes brick recipes: coal + 8 compressed clay | none |
| Cactus Wonder | `steam_cactus_wonder` | Who needs a boiler when you have a desert? | GTNAMachineRecipes.cactusWonder: 8,000 / 90,000 mB, duration 20 | none |
| Chemical Plant | `chemical_plant` | The chairman poses with a microscope. Nobody is fooled. | ChemicalPlantMachine 1 - coilTier*0.05, perfect OC | none |
| Cold Ice Freezer | `cold_ice_freezer` | Born from a liquid ice leak. The intern is still missing. | ColdIceFreezerMachine parallel 64, durationMultiplier 0.5 | none |
| Compact Hyper Pressure Reactor | `compact_hyper_pressure_reactor` | All the pressure, a fraction of the footprint. | HyperPressureReactor maxParallel isCompact ? 512 : 1 | none |
| Component Assembler | `component_assembler` | Your first salary won't cover one of its parts. | ComponentAssemblerMachine: baseCap IV, UV with extension, min(cap, casing tier); GTNAModules extension: Laser/Parallel/Accelerate | none |
| Component Assembly Line | `component_assembly_line` | Industry's closest approximation to divine creation. | ComponentAssemblyLineMachine: casingTier = min(UV, matched tier), beforeWorking recipe tier <= casingTier; registration hatchParallel | none |
| Cracker Hub | `cracker_hub` | Make sure the safety valves work. Then check again. | CoilWorkableElectricMultipleRecipesMachine 2^(coilTemp/900) vs hatch; thread hatch base | none |
| Crystal Builder | `crystal_builder` | The Braggs' dream factory, one perfect lattice at a time. | CoilWorkableElectricMultipleRecipesMachine 2^(coilTemp/900) vs hatch; thread hatch base | none |
| Dimensionally Transcendent Dirt Forge | `dimensionally_transcendent_dirt_forge` | Someone looked at the DTPF and thought: what if dirt? | DimensionallyTranscendentDirtForgeMachine MAX_PARALLEL 524288, duration -> 1 tick | none |
| Dimensionally Transcendent Plasma Forge | `dimensionally_transcendent_plasma_forge` | Transcending dimensional boundaries since 2015. | PlasmaForgeMachine MAXIMUM_DISCOUNT 0.5, 8 h, DECAY 100; GTNAPlasmaForge min 1250 casings, 2 energy / 1 laser | none |
| Dimensionally Transcendent Steam Boiler | `dimensionally_transcendent_steam_boiler` | Bends spacetime to boil water. Priorities. | LargeBoilerMachine(holder, 4_096_000, 32) | none |
| Dimensionally Transcendent Steam Oven | `dimensionally_transcendent_steam_oven` | Preheat to 350 degrees. Then add infinity. | DimensionallyTranscendentSteamOvenMachine(524288, 524288, 0.01, 2 threads) | none |
| Duration Tester | `duration_tester` | If you are reading this, you found the dev room. | registration: WorkableElectricMultipleRecipesMachine, assembler + circuit assembler, Thread/Overclock hatch abilities | none |
| Electric Void Miner | `electric_void_miner` | Mining nothing and getting everything. Physics is optional. | ElectricVoidMinerMachine parallelCap (IV gate from GTNABalance), circuitMeta 1/2 programs | none |
| Engraving Laser Plant | `engraving_laser_plant` | Precise enough to engrave QR codes on viruses. Why? Unknown. | registration: precision = IDENTITY (parallel 1), OC_PERFECT | none |
| Evaporation Plant | `evaporation_plant` | Patience, salt and a very tall tower. | pattern setRepeatable(5); GTCEu ParallelHatch 4^(tier-EV) (IV=4); GTNAModules performance hatches | none |
| Eye of Harmony | `eye_of_harmony` | The universe is big. You built a bigger one. | EyeOfHarmonyMath: circuit 0-24, time *2^-circuit, startup <<2*circuit, gas 10^9*(tier+1); machine in noenergy; gas reset on start | none |
| Eye of Wood | `eye_of_wood` | The Eye of Harmony's rustic cousin from the countryside. | EyeOfWoodMachine STANDARD 256,000, DURATION 1200, SUCCESS_BASE 7500 | none |
| Fishing Ground | `fishing_ground` | Like eating fish? The whole office does now. | FishingGroundMachine circuit 1-4 loot tables | none |
| Forge of the Gods | `forge_of_gods` | Also known as Godforge or Gorge for short. | GodforgeMath.maxModuleCount 8 +4 +4 | none |
| Generator Array | `generator_array` | Four generators walk into a bar. Only one bill. | GeneratorArrayMachine MAX_GENERATORS 4, OUTPUT_MULTIPLIER 1.3, WIRELESS_LOSS 5% | none |
| Giant Flotation Tank | `giant_flotation_tank` | Billions of bubbles, each one a tiny elevator for ore. | WorkableElectricMultipleRecipesMachine: Parallel Hatch, Thread Hatch, laser hatches | none |
| Greenhouse | `greenhouse` | Photosynthesis as a service. | GreenhouseMachine skylight gate | none |
| Helioflare Power Forge | `godforge_smelting_module` | Smelting, but the furnace is a neutron star. | GodforgeModuleMachine / GTNH module text (no numbers) | none |
| Helioflux Melting Core | `godforge_molten_module` | Skip the ingot. Go straight to soup. | GodforgeModuleMachine / GTNH module text (no numbers) | none |
| Heliofusion Exoticizer | `godforge_exotic_module` | Breaking the building blocks of reality, responsibly. | GodforgeModuleMachine / GTNH module text (no numbers) | none |
| Heliothermal Plasma Fabricator | `godforge_plasma_module` | Ionize first, ask questions never. | GodforgeModuleMachine / GTNH module text (no numbers) | none |
| Holy Separator | `holy_separator` | Centrifugation as a sacred purification ritual. Amen. | WorkableElectricMultipleRecipesMachine: Parallel Hatch, Thread Hatch, laser hatches | none |
| Hyper Pressure Reactor | `hyper_pressure_reactor` | Pressure makes diamonds. It also makes this. | HyperPressureReactor maxParallel isCompact ? 512 : 1 | none |
| ISA Mill | `isa_mill` | Despite its green paint, it is not eco-friendly at all. | IsaMillParallel parallel 2; registration OC_PERFECT | none |
| Incubator | `incubator` | Growing ore veins in a petri dish. Science! | VoidMinerEssenceRecipes: 10000 mB Biomass + Milk, 64 essences | none |
| Industrial Flotation Cell | `industrial_flotation_cell` | Smells like essential balm. Fewer mosquitoes, too. | IndustrialFlotationCellMachine perfect OC | none |
| Industrial Slaughterhouse | `industrial_slaughterhouse` | No mobs were harmed in this tooltip. Many were in the machine. | IndustrialSlaughterhouse base tiers/multipliers; recipes EUt 1000/2560/32000/120000 | none |
| Infernal Coke Oven | `infernal_coke_oven` | Hell's kitchen, but for coal. | InfernalCokeOven BASE_PARALLEL 8, PARALLEL_INCREASE 16, MAX 256, TICKS_PER_STAGE 12000, steam 320/t +80/t, bonus cap 10x | none |
| Infinity Fluid Drilling Rig | `infinity_fluid_drilling_rig` | Better than Minecraft's infinite water. Barely legal. | InfinityFluidDrillMachine(ZPM, 256), +50% above rig tier | none |
| Integrated Assembler | `integrated_assembler` | Make complexity simple, make impossible routine. | WorkableElectricMultipleRecipesMachine: Parallel Hatch, Thread Hatch, laser hatches | none |
| Integrated Ore Processor | `integrated_ore_processor` | The entire ore processing line, in one box. | IntegratedOreRecipes circuitMeta 1-7 | none |
| Large Cracker | `large_cracker` | Cracking hydrocarbons like it's a Sunday crossword. | GTRecipeModifiers.crackerOverclock 1 - coilTier*0.1 | none |
| Large Greenhouse | `large_greenhouse` | Who needs the sun? We have lamps and ambition. | registration: Greenhouse + Tree Growth recipe types, hatchParallel, WorkableElectricMultiblockMachine (no skylight gate) | none |
| Large Pyrolyse Oven | `large_pyrolyse_oven` | Wood goes in, chemistry comes out, smoke goes everywhere. | GTRecipeModifiers.pyrolyseOvenOverclock | none |
| Large Steam Alloy Smelter | `large_steam_alloy_smelter` | Bronze Age metallurgy, now with industrial ambition. | LargeSteamAlloySmelter parallel 64/64, durationMultiplier 0.57 | none |
| Large Steam Bath | `large_steam_bath` | A spa day for ores. No cucumbers provided. | AdjustableSteamParallelMachine args (parallel, durationMultiplier) in GTNAMachines; SteamMultiMachineBase.applyHighPressure | none |
| Large Steam Bending Machine | `large_steam_bending` | Bend it like Bessemer. | AdjustableSteamParallelMachine args (parallel, durationMultiplier) in GTNAMachines; SteamMultiMachineBase.applyHighPressure | none |
| Large Steam Centrifuge | `large_steam_centrifuge` | Round and round it goes, where it stops, everyone knows. | AdjustableSteamParallelMachine args (parallel, durationMultiplier) in GTNAMachines; SteamMultiMachineBase.applyHighPressure | none |
| Large Steam Circuit Assembler | `large_steam_circuit_assembler` | Hand-soldered circuits, minus the hands. | LargeSteamCircuitAssembler MAX_PARALLELS 4, OUTPUT_MULTIPLIER 2, DURATION_MULTIPLIER 4, ENGRAVING_NEEDED 16 | none |
| Large Steam Compressor | `large_steam_compressor` | Under pressure, everything becomes a plate eventually. | LargeSteamCompressor parallel 24/48, durationMultiplier 0.4 | none |
| Large Steam Crusher | `large_steam_crusher` | Rocks go in, gravel comes out. Nobody asks about the noise. | LargeSteamCrusher targetParallel 8 / max 128, durationMultiplier 0.5 | none |
| Large Steam Cutting Machine | `large_steam_cutting` | Measure twice, cut sixteen times. | AdjustableSteamParallelMachine args (parallel, durationMultiplier) in GTNAMachines; SteamMultiMachineBase.applyHighPressure | none |
| Large Steam Extractor | `large_steam_extractor` | Squeezes the juice out of things that never had juice. | LargeSteamExtractor parallel 24/48, durationMultiplier 0.57 | none |
| Large Steam Extruder | `large_steam_extruder` | Like a pasta maker, but for metal and regret. | AdjustableSteamParallelMachine args (parallel, durationMultiplier) in GTNAMachines; SteamMultiMachineBase.applyHighPressure | none |
| Large Steam Forming Press | `large_steam_forming_press` | Pressing matters, one stamp at a time. | AdjustableSteamParallelMachine args (parallel, durationMultiplier) in GTNAMachines; SteamMultiMachineBase.applyHighPressure | none |
| Large Steam Furnace | `large_steam_furnace` | Do not attempt to bake cookies inside. They will vaporize. | LargeSteamFurnace targetParallel 8 / max 128, durationMultiplier 0.1 | none |
| Large Steam Hammer | `large_steam_hammer` | Stop. Hammer time. | LargeSteamHammer parallel 32/64, durationMultiplier 0.5 | none |
| Large Steam Lathe | `large_steam_lathe` | Turning rods since before electricity was cool. | AdjustableSteamParallelMachine args (parallel, durationMultiplier) in GTNAMachines; SteamMultiMachineBase.applyHighPressure | none |
| Large Steam Mixer | `large_steam_mixer` | Shaken, not stirred. Actually, both. | AdjustableSteamParallelMachine args (parallel, durationMultiplier) in GTNAMachines; SteamMultiMachineBase.applyHighPressure | none |
| Large Steam Ore Washer | `large_steam_ore_washer` | The cleanest ores in the Bronze Age. Mom would be proud. | LargeSteamOreWasher parallel 48/96, durationMultiplier 0.2 | none |
| Large Steam Sifter | `large_steam_sifter` | Panning for gems, minus the river and the tetanus. | AdjustableSteamParallelMachine args (parallel, durationMultiplier) in GTNAMachines; SteamMultiMachineBase.applyHighPressure | none |
| Large Steam Solar Boiler | `large_steam_solar_boiler` | Free steam, courtesy of a very large star. | LargeSteamSolarBoilerMachine MAX_SIDE 63, MAX_BACK 125 | none |
| Large Steam Storage Tank | `large_steam_storage_tank` | Hot air, stored responsibly. | LargeSteamStorageTank CAPACITY 120,000,000 | none |
| Large Steam Thermal Centrifuge | `large_steam_thermal_centrifuge` | Spinning and roasting: the ore's worst day. | AdjustableSteamParallelMachine args (parallel, durationMultiplier) in GTNAMachines; SteamMultiMachineBase.applyHighPressure | none |
| Large Steam Wiremill | `large_steam_wiremill` | Thin is in. Very, very thin. | AdjustableSteamParallelMachine args (parallel, durationMultiplier) in GTNAMachines; SteamMultiMachineBase.applyHighPressure | none |
| Leap Forward One Blast Furnace | `leap_forward_one_blast_furnace` | A great leap forward in primitive technology. | LeapForwardBlastFurnace MAX_PARALLEL_CAP 32000, 400 ticks + 400/layer | none |
| Liquefaction Furnace | `liquefaction_furnace` | Everything is a liquid if you heat it enough. | GTNAModules liquefaction extension: Parallel + Accelerate | none |
| ME Storage | `me_storage` | More bytes than you will ever need. Probably. | ME storage pattern setRepeatable(1, 128) | none |
| Magnetic Energy Reaction Furnace | `magnetic_energy_reaction_furnace` | Smells like ozone. Fresh, but dangerous. | CoilWorkableElectricMultipleRecipesMachine 2^(coilTemp/900) vs hatch; thread hatch base | none |
| Mega Alloy Blast Smelter | `mega_alloy_blast_smelter` | The Alloy Blast Smelter, but it went to the gym. | MegaAlloyBlastSmelterMachine eut 0.8, duration 0.6 | none |
| Mega Brewer | `mega_brewer` | Thousand-ton brewing. The whole workshop smells great. | CoilWorkableElectricMultipleRecipesMachine 2^(coilTemp/900) vs hatch; thread hatch base | none |
| Mega Distillery | `mega_distillery` | Every fraction of the barrel, accounted for. | WorkableElectricMultipleRecipesMachine: Parallel Hatch, Thread Hatch, laser hatches | none |
| Mega Vacuum Drying Furnace | `mega_vacuum_drying_furnace` | Zero oxidation, zero contamination, zero patience needed. | CoilWorkableElectricMultipleRecipesMachine 2^(coilTemp/900) vs hatch; thread hatch base | none |
| Mega Wiremill | `mega_wiremill` | From bulky ingots to hair-thin perfect wires. | CoilWorkableElectricMultipleRecipesMachine 2^(coilTemp/900) vs hatch; thread hatch base | none |
| Nanites Circuit Assembly Factory | `nanites_circuit_assembly_factory` | No furnace roar, no robot arms. Just nanites. | WorkableElectricMultipleRecipesMachine: Parallel Hatch, Thread Hatch, laser hatches | none |
| Nano Forge | `nano_forge` | Nanobots, son. Billions of them. | NanoForgeMachine tier nanites (carbon/neutronium/transcendent), OC_PERFECT when tier > required | none |
| Neutronium Wire Cutting | `neutronium_wire_cutting` | Neutron star matter cuts like butter. Earth stuff? Air. | WorkableElectricMultipleRecipesMachine: Parallel Hatch, Thread Hatch, laser hatches | none |
| Nexus Assembly Forge | `nexus_molecular_forge` | Ingredients? Where we're going, we don't need ingredients. | NexusMolecularForgeMachine eut = totalItems (1 EU/item) | none |
| Nexus Flux Matrix | `nexus_flux_matrix` | Infinite power, if you can afford the batteries. | NexusFluxMatrixMachine unlimited = 750 capacitors at MAX | none |
| Nexus ME Hypercore | `nexus_me_hypercore` | Can it run Crysis? It can craft it. | NexusMEHyperCoreMachine TOTAL_MODULE_SLOTS 320, threads 4/16/128/1024, transcendent = 320 x IV | none |
| Particle Stream Matrix Filling Machine | `particle_stream_matrix_filling_machine` | Even photons and sound waves fit in a can now. | CoilWorkableElectricMultipleRecipesMachine 2^(coilTemp/900) vs hatch; thread hatch base | none |
| Phase Change Cube | `phase_change_cube` | Six faces, six phase changes. A Rubik's Cube for matter. | CoilWorkableElectricMultipleRecipesMachine 2^(coilTemp/900) vs hatch; thread hatch base | none |
| Primitive Distillation Tower | `primitive_distillation_tower` | Moonshine technology, scaled up for oil. | PrimitiveSteamDistillationTowerMachine 0.75 steam, MV cap; pattern 5 repeated tower layers | none |
| Primitive Stone Furnace | `primitive_stone_furnace` | Carved by hand, powered by nothing, judged by no one. | PrimitiveStoneFurnaceMachine RECIPE_DURATION 1, getMaxParallel Integer.MAX_VALUE, threads MAX-1, IZeroEnergyMachine | none |
| Rocket Large Turbine | `rocket_large_turbine` | Not rocket science. Okay, it is rocket science. | GTNALargeTurbineMachine HIGH_SPEED 3x, rotor damage 10; module 2x/+20%; V[EV]*2.5 = 5120 | none |
| Steam Bee Breeding Module | `steam_elevator_bee_breeding_module` | Let the bees feel the scorching love. | SteamBeeBreedingModule CYCLE 12000, FEED_CONSUMED 128 | none |
| Steam Cobbler | `steam_cobbler` | Infinite cobblestone: the oldest trick in the book, now industrial. | SteamCobbler targetParallel 16 / max 16 | none |
| Steam Cracker | `steam_cracking` | Petrochemistry, Victorian edition. | SteamCracking maxParallel 8 / 16 (high pressure) | none |
| Steam Elevator | `steam_elevator` | Going up? Please hold on to your top hat. | SteamElevator MODULE_OFFSETS (12 slots), SteamElevatorTeleport.setOut | none |
| Steam Elevator Beacon Module I | `steam_elevator_beacon_module_i` | A beacon, but it runs on tea-kettle energy. | SteamBeaconModule range 64/128/256, amplifier tier-1, 10 effects | none |
| Steam Elevator Beacon Module II | `steam_elevator_beacon_module_ii` | Buffs for the whole neighborhood. | SteamBeaconModule range 64/128/256, amplifier tier-1, 10 effects | none |
| Steam Elevator Beacon Module III | `steam_elevator_beacon_module_iii` | Elite beacon. The Wither wishes it were this cool. | SteamBeaconModule range 64/128/256, amplifier tier-1, 10 effects | none |
| Steam Entity Crusher Module I | `steam_elevator_entity_crusher_module_i` | Smelting mobs with high-temperature steam. Grim. | SteamEntityCrusherModule 400/200/100 ticks, 2% + 0.5%/spawner, cap 34% | none |
| Steam Entity Crusher Module II | `steam_elevator_entity_crusher_module_ii` | Faster crushing. The mobs did not vote for this. | SteamEntityCrusherModule 400/200/100 ticks, 2% + 0.5%/spawner, cap 34% | none |
| Steam Entity Crusher Module III | `steam_elevator_entity_crusher_module_iii` | Industrial-grade mob disposal. Very efficient. Very sad. | SteamEntityCrusherModule 400/200/100 ticks, 2% + 0.5%/spawner, cap 34% | none |
| Steam Flight Module I | `steam_elevator_flight_module_i` | I believe I can fly. With enough steam. | SteamFlightModule RANGE 64 x module tier | none |
| Steam Flight Module II | `steam_elevator_flight_module_ii` | Twice the range, twice the bragging rights. | SteamFlightModule RANGE 64 x module tier | none |
| Steam Flight Module III | `steam_elevator_flight_module_iii` | Icarus would have loved this. Briefly. | SteamFlightModule RANGE 64 x module tier | none |
| Steam Greenhouse Planting Module | `steam_elevator_greenhouse_module` | The farmer's secret to fortune. | SteamGreenhouseModule WATER_PER_OPERATION 16,000, RANGE 16, CYCLE 1200, 16 crops | none |
| Steam Item Vault | `steam_item_vault` | A Victorian warehouse. Dragons not included. | SteamItemVaultMachine SLOTS 256, SLOT_LIMIT 64,000 | none |
| Steam Lava Maker | `steam_lava_maker` | Turning the floor into lava, professionally. | SteamLavaMakerMachine parallel 16; GTNALavaMakerRecipes duration 20 | none |
| Steam Manufacturer | `steam_manufacturer` | The assembly line, but every worker is a piston. | SteamManufacturer targetParallel 16 / max 16 | none |
| Steam Monster Repellator Module I | `steam_elevator_monster_repellent_module_i` | It drives away monsters with loud noise. | SteamMonsterRepellentModule range 1<<(5+tier) | none |
| Steam Monster Repellator Module II | `steam_elevator_monster_repellent_module_ii` | You can't hear it, but the monsters hear it loud and clear. | SteamMonsterRepellentModule range 1<<(5+tier) | none |
| Steam Monster Repellator Module III | `steam_elevator_monster_repellent_module_iii` | Monsters get the hint and leave on their own. | SteamMonsterRepellentModule range 1<<(5+tier) | none |
| Steam Oil Drill Module I | `steam_elevator_oil_drill_module_i` | Black gold, Texas tea, steam-pumped. | SteamOilDrillModule cycle 1200/(tier-1), yield 250*2^(tier-2), fluids tier-1 | none |
| Steam Oil Drill Module II | `steam_elevator_oil_drill_module_ii` | There will be oil. Twice as much. | SteamOilDrillModule cycle 1200/(tier-1), yield 250*2^(tier-2), fluids tier-1 | none |
| Steam Oil Drill Module III | `steam_elevator_oil_drill_module_iii` | I drink your milkshake. All of it. | SteamOilDrillModule cycle 1200/(tier-1), yield 250*2^(tier-2), fluids tier-1 | none |
| Steam Ore Processing Module | `steam_elevator_ore_processor_module` | The whole ore line in one box. Steam-powered, of course. | SteamOreProcessorModule maxParallelFor 8<<mode, upkeepFor 128<<mode | none |
| Steam Supercompressor | `steam_mega_compressor` | Diamonds are made under pressure. So is this machine. | MegaSteamCompressor parallel 256, durationMultiplier 0.5 | none |
| Steam Weather Module I | `steam_elevator_weather_module_i` | Rain dance, but with pipes. | SteamWeatherModule WEATHER_TIME 72000 x tier, WEATHER_STEAM_COST 1,000,000 | none |
| Steam Weather Module II | `steam_elevator_weather_module_ii` | The forecast is whatever you want it to be. | SteamWeatherModule WEATHER_TIME 72000 x tier, WEATHER_STEAM_COST 1,000,000 | none |
| Steam Weather Module III | `steam_elevator_weather_module_iii` | Thor called. He wants his job back. | SteamWeatherModule WEATHER_TIME 72000 x tier, WEATHER_STEAM_COST 1,000,000 | none |
| Steam Woodcutter | `steam_woodcutter` | I'm a lumberjack and I'm okay. | SteamWoodcutter targetParallel 64 / max 64 | none |
| Steam-Powered Apiary Module | `steam_elevator_apiary_module` | High pressure makes the bees work harder. Union pending. | SteamApiaryModule CYCLE 6000, WATER 1000, base colony 8 | none |
| Stone SuperHeater | `stone_superheater` | Rocks, but hotter. Much hotter. | StoneSuperHeater targetParallel 32 / max 32 | none |
| Super Blast Smelter | `super_blast_smelter` | Smelting all things at artificial-sun temperatures. | CoilWorkableElectricMultipleRecipesMachine coilTemp + 100*(tier-MV) | none |
| Superconducting Electromagnetism | `superconducting_electromagnetism` | Maxwell's equations, now in industrial size. | WorkableElectricMultipleRecipesMachine: Parallel Hatch, Thread Hatch, laser hatches | none |
| Superconducting Magnetic Presser | `superconducting_magnetic_presser` | Can easily accelerate coins to Mach 3! | WorkableElectricMultipleRecipesMachine: Parallel Hatch, Thread Hatch, laser hatches | none |
| Supercritical Steam Turbine | `supercritical_steam_turbine` | Steam, but it has seen things. | SupercriticalSteamTurbineMachine V[IV]*2 = 16384; module 2x/+20%/2x wear | none |
| Thermal Power Pump | `thermal_power_pump` | Turns steam back into water. Circle of life. | ThermalPowerPumpMachine biome modifier, x3/2 in rain, Nether 0 | none |
| Transcendent Plasma Mixer | `transcendent_plasma_mixer` | Assisting in all your DTPF needs! | TranscendentPlasmaMixerMachine EU_MULTIPLIER default 10 | none |
| Universal Factory | `universal_factory` | One factory to rule them all. | registry: 32 recipe types | none |
| Vacuum Drying Furnace | `vacuum_drying_furnace` | Turns foam back into dust. Magic, but with vacuum. | VacuumDryingFurnaceMachine: Dehydrator 2^floor(coil/900), Vacuum Drying serial | none |
| Void Fluid Drilling Rig | `void_fluid_drilling_rig` | The well ran dry. The void did not. | VoidFluidDrillConfig minimumTier EV, remote upgrade | none |
| Void Miner SteamGate Aged | `void_miner_steam_gate_aged` | Mining a dimension made entirely of steam. Don't ask. | GTNABalance.VoidMinerSteamGateBalance 2/2.0/1.5, 3/3.0/2.0, 5/5.0/4.0 | none |
