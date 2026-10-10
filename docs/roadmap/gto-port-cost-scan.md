# Varredura de custo de port: multiblocos do GTOCore (2026-10-07)

Gerada por `tools/scan_gto_port_cost.py` (rodar dentro da pasta `machines` do GTOCore) a partir de `GTOCore-Main/src/main/java/com/gtocore/common/data/machines/*.java`
(commit `dc4824d`), contra os blocos de `GTNABlocks` e os ids já registrados no GTNA.

Colunas: blocos GTO faltando · id · formato do padrão (`mbs`, `inline`) · classe do GTO | tipos de receita |
blocos faltando. `(+gto machines)` = a estrutura usa máquinas/partes do GTO (hatches especiais, componentes
de pesquisa etc.), o que pede port extra.

Leitura: linhas com `0` e classe padrão (`CoilCrossRecipe…`, `CrossRecipe…`, `ElectricMultiblockMachine`,
`CoilMultiblockMachine`) e tipo de receita do GTCEu são as mais baratas. Classe própria ou tipo do GTO
(`*_RECIPES` sem `gt:`) pede mecânica e/ou um tipo de receita novo.

```
 0 advanced_assembly_line                     inline AdvancedAssemblyLineMachine              | gt:ASSEMBLY_LINE_RECIPES |  
 0 advanced_mana_distributor                  mbs    ManaDistributorMachine.create(64, 128    | gt:DUMMY_RECIPES |  
 0 algae_farm                                 mbs    AlgaeFarmMachine                         | DUMMY_RECIPES |  
 0 analysis_and_research_center               inline AnalysisAndResearchCenterMachine         | DATA_ANALYSIS_RECIPES, DATA_INTEGRATION_RECIPES |  (+gto machines)
 0 ancient_reactor_core                       mbs    VoidTransporterMachine.create(1, 0, Void | DUMMY_RECIPES |  
 0 atomizing_condenser                        mbs    TierCasingParallelMultiblockMachine.crea | ATOMIZATION_CONDENSATION_RECIPES |  
 0 base_mana_distributor                      mbs    ManaDistributorMachine.create(16, 32     | gt:DUMMY_RECIPES |  
 0 boss_summoner                              mbs    BossSummonerMachine                      | DUMMY_RECIPES |  
 0 chemical_energy_devourer                   mbs    ChemicalEnergyDevourerMachine            | COMBUSTION_GENERATOR_FUELS, GAS_TURBINE_FUELS, ROCKET_ENGINE_FUELS |  
 0 chemical_vapor_deposition                  mbs    CoilCustomParallelMultiblockMachine.crea | CHEMICAL_VAPOR_DEPOSITION_RECIPES |  
 0 compound_extreme_cooling_unit              ?      CompoundExtremeCoolingMachine            | VACUUM_RECIPES, ATOMIZATION_CONDENSATION_RECIPES,PLASMA_CONDENSER_RECI |  
 0 crystallization_chamber                    inline CoilMultiblockMachine.createCoilMachine( | CRYSTALLIZATION_RECIPES |  
 0 decay_hastener                             mbs    ElectricMultiblockMachine                | DECAY_HASTENER_RECIPES |  
 0 digestion_tank                             mbs    DigestionTankMachine                     | DIGESTION_TREATMENT_RECIPES |  
 0 digital_miner                              mbs    DigitalMiner                             | DUMMY_RECIPES |  
 0 dimensional_focus_engraving_array          mbs    CoilCrossRecipeMultiblockMachine         | DIMENSIONAL_FOCUS_ENGRAVING_ARRAY_RECIPES |  
 0 disassembly                                mbs    ElectricMultiblockMachine                | DISASSEMBLY_RECIPES |  
 0 drone_control_center                       mbs    DroneControlCenterMachine                | DUMMY_RECIPES |  
 0 electric_cooking                           mbs    ElectricMultiblockMachine                | ELECTRIC_COOKING_RECIPES |  
 0 encapsulator_execution_module              mbs    EncapsulatorExecutionModuleMachine       | gt:DUMMY_RECIPES |  
 0 energy_injector                            mbs    EnergyInjectorMachine                    | gt:DUMMY_RECIPES |  (+gto machines)
 0 fission_reactor                            mbs    FissionReactorMachine                    | FISSION_REACTOR_RECIPES |  (+gto machines)
 0 fluid_vault                                mbs    h -> new MultiblockMEStorageMachine(h, A | DUMMY_RECIPES |  (+gto machines)
 0 gas_compressor                             mbs    ElectricMultiblockMachine                | GAS_COMPRESSOR_RECIPES |  
 0 general_vault                              mbs    h -> new MultiblockMEStorageMachine(h, n | DUMMY_RECIPES |  (+gto machines)
 0 heat_exchanger                             mbs    HeatExchangerMachine                     | HEAT_EXCHANGER_RECIPES |  
 0 high_temperature_reaction_hub              mbs    CoilCrossRecipeMultiblockMachine.createH | LIQUEFACTION_FURNACE_RECIPES,REACTION_FURNACE_RECIPES |  
 0 item_vault                                 mbs    h -> new MultiblockMEStorageMachine(h, A | DUMMY_RECIPES |  (+gto machines)
 0 large_arc_generator                        inline GCYMMultiblockMachine                    | ARC_GENERATOR_RECIPES |  
 0 large_bender                               inline GCYMMultiblockMachine                    | gt:BENDER_RECIPES |  
 0 large_coke_oven                            mbs    LargeCokeOvenMachine                     | gt:COKE_OVEN_RECIPES |  
 0 large_crusher                              inline GCYMMultiblockMachine                    | CRUSHER_RECIPES |  (+gto machines)
 0 large_forming                              inline GCYMMultiblockMachine                    | gt:FORGE_HAMMER_RECIPES,gt:FORMING_PRESS_RECIPES |  
 0 large_gas_collector                        mbs    CustomParallelMultiblockMachine.createPa | LARGE_GAS_COLLECTOR_RECIPES |  
 0 large_incubator                            mbs    IncubatorMachine                         | INCUBATOR_RECIPES |  (+gto machines)
 0 large_laminator                            inline GCYMMultiblockMachine                    | LAMINATOR_RECIPES |  
 0 large_laser_welder                         inline GCYMMultiblockMachine                    | LASER_WELDER_RECIPES |  
 0 large_rock_crusher                         inline GCYMMultiblockMachine                    | gt:ROCK_BREAKER_RECIPES |  
 0 large_rolling                              inline GCYMMultiblockMachine                    | ROLLING_RECIPES,CLUSTER_RECIPES |  
 0 large_steam_forge_hammer                   mbs    LargeSteamMultiblockMachine              | gt:FORGE_HAMMER_RECIPES |  (+gto machines)
 0 large_steam_macerator                      mbs    LargeSteamMultiblockMachine              | gt:MACERATOR_RECIPES |  (+gto machines)
 0 large_void_miner                           mbs    ElectricMultiblockMachine                | LARGE_VOID_MINER_RECIPES,RANDOM_ORE_RECIPES |  
 0 lava_furnace                               mbs    ElectricMultiblockMachine                | LAVA_FURNACE_RECIPES |  
 0 luv_kuangbiao_one_giant_nuclear_fusion_reactor mbs    AdvancedFusionReactorMachine             | gt:FUSION_RECIPES |  
 0 magnetic_fluid_generator                   inline MagneticFluidGeneratorMachine            | gt:PLASMA_GENERATOR_FUELS |  
 0 me_cpu                                     mbs    MECPUMachine                             | DUMMY_RECIPES |  
 0 me_energy_substation                       inline TierCasingMultiblockMachine.createMachin | DUMMY_RECIPES |  
 0 multiblock_crate                           mbs    MultiblockCrateMachine                   | DUMMY_RECIPES |  
 0 nether_reactor_core                        mbs    VoidTransporterMachine.create(2, 1920, V | DUMMY_RECIPES |  
 0 neutron_irradiation_chamber                mbs    NoRecipeLogicMultiblockMachine           | DUMMY_RECIPES |  
 0 neutron_vortex                             ?      NeutronVortexMachine                     | NEUTRON_ACTIVATOR_RECIPES |  
 0 ore_extraction_module                      mbs    h -> new NanitesModuleMachine(h, 1       | NANITES_INTEGRATED_PROCESSING_CENTER_RECIPES |  
 0 pcb_factory                                ?      PCBFactoryMachine                        | PCB_FACTORY_RECIPES |  
 0 physical_vapor_deposition                  mbs    TierCasingParallelMultiblockMachine.crea | PHYSICAL_VAPOR_DEPOSITION_RECIPES |  
 0 polymerization_reactor                     mbs    CoilMultiblockMachine.createCoilMachine( | POLYMERIZATION_REACTOR_RECIPES |  (+gto machines)
 0 precision_assembler                        mbs    PrecisionAssemblerMachine                | PRECISION_ASSEMBLER_RECIPES,gt:ASSEMBLER_RECIPES |  
 0 precision_assembly_center                  mbs    CrossRecipeMultiblockMachine             | PRECISION_ASSEMBLER_RECIPES |  
 0 primordial_scanning_station                inline ScanningStationMachine                   | CRYSTAL_SCAN_RECIPES |  (+gto machines)
 0 processing_plant                           inline ProcessingPlantMachine                   | gt:DUMMY_RECIPES |  (+gto machines)
 0 pulse_machine_maintenance_pedestal         inline PulseMachineMaintenancePedestal          | DUMMY_RECIPES |  (+gto machines)
 0 rare_earth_centrifugal                     mbs    ElectricMultiblockMachine                | RARE_EARTH_CENTRIFUGAL_RECIPES |  
 0 reaction_furnace                           inline CoilMultiblockMachine.createCoilMachine( | REACTION_FURNACE_RECIPES |  (+gto machines)
 0 recycler                                   mbs    CustomParallelMultiblockMachine.createPa | RECYCLER_RECIPES |  
 0 rocket_assembler                           mbs    ElectricMultiblockMachine                | ROCKET_ASSEMBLER_RECIPES |  
 0 satellite_control_center                   mbs    SatelliteControlCenterMachine            | DUMMY_RECIPES |  
 0 sintering_furnace                          mbs    CoilMultiblockMachine.createCoilMachine( | SINTERING_FURNACE_RECIPES |  
 0 slaughterhouse                             mbs    SlaughterhouseMachine                    | gt:DUMMY_RECIPES |  
 0 steam_bath                                 mbs    SteamMultiblockMachine                   | gt:CHEMICAL_BATH_RECIPES |  (+gto machines)
 0 steam_cracker                              mbs    LargeSteamCracker                        | STEAM_CRACKING_RECIPES |  
 0 steam_crusher                              mbs    SteamMultiblockMachine                   | CRUSHER_RECIPES |  (+gto machines)
 0 steam_foundry                              mbs    SteamMultiblockMachine                   | gt:ALLOY_SMELTER_RECIPES |  (+gto machines)
 0 steam_mixer                                mbs    SteamMultiblockMachine                   | gt:MIXER_RECIPES |  (+gto machines)
 0 steam_ore_washer                           mbs    SteamMultiblockMachine                   | gt:ORE_WASHER_RECIPES |  (+gto machines)
 0 steam_piston_hammer                        mbs    SteamMultiblockMachine                   | gt:FORGE_HAMMER_RECIPES |  (+gto machines)
 0 steam_pressor                              mbs    SteamMultiblockMachine                   | gt:COMPRESSOR_RECIPES |  (+gto machines)
 0 steam_separator                            mbs    (holder                                  | gt:CENTRIFUGE_RECIPES |  (+gto machines)
 0 super_molecular_assembler                  mbs    SuperMolecularAssemblerMachine           | DUMMY_RECIPES |  
 0 thermo_press                               mbs    TierCasingMultiblockMachine.createMachin | THERMO_PRESSING_RECIPES |  
 0 three_dimensional_printer                  mbs    ElectricMultiblockMachine                | THREE_DIMENSIONAL_PRINTER_RECIPES |  
 0 void_miner                                 mbs    VoidMinerMachine                         | DUMMY_RECIPES |  
 0 wireless_charger                           mbs    WirelessChargerMachine                   | DUMMY_RECIPES |  
 0 wireless_dimension_repeater                mbs    WirelessDimensionRepeaterMachine         | DUMMY_RECIPES |  
 0 wireless_energy_substation                 inline WirelessEnergySubstationMachine          | DUMMY_RECIPES |  
 1 advanced_mass_fabricator                   mbs    CrossRecipeMultiblockMachine             | MASS_FABRICATOR_RECIPES | TITANSTEEL_COIL_BLOCK 
 1 atomic_energy_excitation_plant             mbs    CoilMultiblockMachine.createCoilMachine( | ATOMIC_ENERGY_EXCITATION_RECIPES | BOROSILICATE_GLASS 
 1 biochemical_extraction                     mbs    BiologicalExtractionMachine              | BIOCHEMICAL_EXTRACTION_RECIPES | BIOLOGICAL_MECHANICAL_CASING 
 1 block_conversion_room                      mbs    holder -> new BlockConversionRoomMachine | BLOCK_CONVERSIONRECIPES | SHINING_OBSIDIAN (+gto machines)
 1 chemical_complex                           mbs    CoilCrossRecipeMultiblockMachine         | LARGE_CHEMICAL_RECIPES, POLYMERIZATION_REACTOR_RECIPES | CHEMICAL_GRADE_GLASS 
 1 circuit_assembly_line                      inline CircuitAssemblyLineMachine               | CIRCUIT_ASSEMBLY_LINE_RECIPES | PIKYONIUM_MACHINE_CASING (+gto machines)
 1 data_center                                inline DataBankMachine                          | gt:DUMMY_RECIPES | IRIDIUM_PIPE_CASING (+gto machines)
 1 drawing_tower                              inline DrawingTowerMachine                      | DRAWING_RECIPES | TUNGSTEN_BOROSILICATE_GLASS (+gto machines)
 1 drilling_control_center                    mbs    DrillingControlCenterMachine             | DUMMY_RECIPES | TUNGSTEN_BOROSILICATE_GLASS 
 1 electroplating_bath                        mbs    ElectricMultiblockMachine                | ELECTROPLATING_RECIPES | CHEMICAL_GRADE_GLASS 
 1 element_copying                            mbs    CrossRecipeMultiblockMachine             | ELEMENT_COPYING_RECIPES | HYPER_CORE 
 1 elf_exchange                               mbs    ElfExchangeMachine                       | ELF_EXCHANGE_RECIPES | MANASTEEL_CASING 
 1 god_forge                                  ?      GodForgeMachine                          | gt:DUMMY_RECIPES | TRANSCENDENTALLY_AMPLIFIED_MAGNETIC_CONFINEMENT_CASING 
 1 gravity_bending_device                     mbs    CrossRecipeMultiblockMachine             | gt:BENDER_RECIPES | HIGH_PRESSURE_RESISTANT_CASING 
 1 hand_of_arachne                            mbs    CrossRecipeMultiblockMachine             | LOOM_RECIPES | PIKYONIUM_MACHINE_CASING 
 1 high_energy_laser_purification_unit        mbs    HighEnergyLaserPurificationUnitMachine   | WATER_PURIFICATION_PLANT_RECIPES | HIGH_ENERGY_ULTRAVIOLET_EMITTER_CASING (+gto machines)
 1 holy_separator                             mbs    CrossRecipeMultiblockMachine             | gt:CENTRIFUGE_RECIPES | MC_NYLON_TENSILE_MECHANICAL_SHELL 
 1 industrial_altar                           mbs    ManaMultiblockMachine                    | INDUSTRIAL_ALTAR_RECIPES | MANASTEEL_CASING 
 1 isostatic_press                            mbs    ElectricMultiblockMachine                | ISOSTATIC_PRESSING_RECIPES | COMPRESSOR_PIPE_CASING 
 1 large_block_conversion_room                mbs    holder -> new BlockConversionRoomMachine | BLOCK_CONVERSIONRECIPES | SHINING_OBSIDIAN (+gto machines)
 1 large_naquadah_reactor                     inline ElectricMultiblockMachine                | LARGE_NAQUADAH_REACTOR_RECIPES | EXTREME_STRENGTH_TRITANIUM_CASING 
 1 lhc                                        mbs    NoRecipeLogicMultiblockMachine           | DUMMY_RECIPES | SHIELDED_ACCELERATOR 
 1 mana_alloy_blast_smelter                   mbs    ManaAlloyBlastSmelterMachine             | ALLOY_BLAST_RECIPES | MANASTEEL_CASING 
 1 mana_beam_assembler                        inline ManaFlowAssembler                        | MANA_FLOW_ASSEMBLER_RECIPES | MANASTEEL_CASING 
 1 mana_condenser                             ?      ManaCondenserMachine                     | MANA_CONDENSER_RECIPES | MANASTEEL_CASING 
 1 mana_garden                                mbs    ElectricManaMultiblockMachine            | MANA_GARDEN_RECIPES, MANA_GARDEN_FUEL | MANASTEEL_CASING 
 1 mana_greenhouse                            mbs    ManaEnergyMultiblockMachine              | GREENHOUSE_RECIPES | MANASTEEL_CASING 
 1 mana_infuser                               mbs    ManaMultiblockMachine                    | MANA_INFUSER_RECIPES | MANASTEEL_CASING 
 1 mass_fabricator                            mbs    ElectricMultiblockMachine                | MASS_FABRICATOR_RECIPES | HYPER_CORE 
 1 molten_core                                inline MoltenCoreMachine                        | FLUID_HEATER_RECIPES, DISTILLERY_RECIPES | PI_HIGH_TEMPERATURE_INSULATION_MECHANICAL_HOUSING 
 1 nanites_integrated_processing_center       mbs    NanitesIntegratedMachine                 | NANITES_INTEGRATED_PROCESSING_CENTER_RECIPES | PPS_CORROSION_RESISTANT_MECHANICAL_HOUSING 
 1 neutron_activator                          inline NeutronActivatorMachine                  | NEUTRON_ACTIVATOR_RECIPES | SPEEDING_PIPE (+gto machines)
 1 neutronium_wire_cutting                    mbs    CrossRecipeMultiblockMachine             | gt:CUTTER_RECIPES | HIGH_PRESSURE_RESISTANT_CASING 
 1 polymer_twisting_module                    mbs    h -> new NanitesModuleMachine(h, 3       | NANITES_INTEGRATED_PROCESSING_CENTER_RECIPES | CHEMICAL_GRADE_GLASS 
 1 rarity_forge                               inline CrossRecipeMultiblockMachine             | RARITY_FORGE_RECIPES | ORIGINAL_BRONZE_CASING 
 1 smart_siftering_hub                        mbs    TierCasingCrossRecipeMultiblockMachine.c | SIFTER_RECIPES | IRIDIUM_GEARBOX 
 1 star_ultimate_material_forge_factory       mbs    CoilCrossRecipeMultiblockMachine.createP | ULTIMATE_MATERIAL_FORGE_RECIPES | ULTIMATE_STELLAR_CONTAINMENT_CASING 
 1 supercomputing_center                      inline SupercomputingCenterMachine              | gt:DUMMY_RECIPES | MC_NYLON_TENSILE_MECHANICAL_SHELL (+gto machines)
 1 superconducting_electromagnetism           mbs    CrossRecipeMultiblockMachine             | gt:POLARIZER_RECIPES,gt:ELECTROMAGNETIC_SEPARATOR_RECIPES | LAFIUM_MECHANICAL_CASING 
 1 superconducting_magnetic_presser           mbs    CrossRecipeMultiblockMachine             | gt:FORMING_PRESS_RECIPES | AMPROSIUM_BOROSILICATE_GLASS 
 1 synthetic_data_assembly_plant              inline SyntheticDataAssemblyPlantMachine        | RECIPES_DATA_GENERATE_RECIPES | HIGH_PRESSURE_RESISTANT_CASING (+gto machines)
 1 tree_growth_simulator                      mbs    TreeGrowthSimulator                      | TREE_GROWTH_SIMULATOR_RECIPES | REINFORCED_WOOD_CASING 
 1 void_transporter                           mbs    VoidTransporterMachine.create(0, 480     | DUMMY_RECIPES | REINFORCED_OBSIDIAN 
 2 bedrock_drilling_rig                       mbs    BedrockDrillingRigMachine                | BEDROCK_DRILLING_RIG_RECIPES | ECHO_CASING MACHINE_CASING_GRINDING_HEAD 
 2 biochemical_reaction                       mbs    BiochemicalReactionRoomMachine           | BIOCHEMICAL_REACTION_RECIPES | BIOLOGICAL_MECHANICAL_CASING CHEMICAL_GRADE_GLASS (+gto machines)
 2 clarifier_purification_unit                mbs    ClarifierPurificationUnitMachine         | WATER_PURIFICATION_PLANT_RECIPES | REINFORCED_STERILE_WATER_PLANT_CASING STERILE_WATER_PLANT_CASING 
 2 compound_distillation_fractionator         mbs    CrossRecipeMultiblockMachine             | gt:DISTILLATION_RECIPES,EVAPORATION_RECIPES | FLOCCULATION_CASING STERILE_WATER_PLANT_CASING 
 2 dragon_egg_copier                          mbs    ElectricMultiblockMachine                | DRAGON_EGG_COPIER_RECIPES | DRAGON_STRENGTH_TRITANIUM_CASING MAGIC_CORE 
 2 entropy_flux_engine                        mbs    TierCasingCrossRecipeMultiblockMachine.c | DECAY_HASTENER_RECIPES | QUARK_PIPE URUIUM_COIL_BLOCK 
 2 extreme_electric_furnace                   mbs    CoilCrossRecipeMultiblockMachine         | gt:ALLOY_SMELTER_RECIPES,gt:FURNACE_RECIPES | ENGINEERING_MECHANICAL_CASING HSSS_BOROSILICATE_GLASS 
 2 fiber_extruder                             mbs    CoilCustomParallelMultiblockMachine.crea | FIBER_EXTRUSION_RECIPES | STAINLESS_STEEL_CORROSION_RESISTANT_CASING TITANIUM_ALLOY_FRAME_INTERNAL 
 2 fuel_cell_generator                        mbs    FullCellGenerator                        | FUEL_CELL_ENERGY_ABSORPTION_RECIPES,FUEL_CELL_ENERGY_TRANSFER_RECIPES, | FLOCCULATION_CASING IRIDIUM_PIPE_CASING (+gto machines)
 2 giant_electrochemical_workstation          mbs    CoilCrossRecipeMultiblockMachine         | ELECTROPLATING_RECIPES, ELECTROLYZER_RECIPES | IRIDIUM_PIPE_CASING SPACE_ELEVATOR_MECHANICAL_CASING 
 2 heavy_rolling                              mbs    CoilCrossRecipeMultiblockMachine         | ROLLING_RECIPES, CLUSTER_RECIPES | AMPROSIUM_CASING HIGH_STRENGTH_SUPPORT_SPINDLE 
 2 high_energy_laser_lathe                    mbs    CrossRecipeMultiblockMachine             | gt:LATHE_RECIPES | HIGH_ENERGY_LASER_EMITTER LASER_COOLING_CASING 
 2 large_crystallization_chamber              mbs    CoilMultiblockMachine.createCoilMachine( | CRYSTALLIZATION_RECIPES | HIGH_PRESSURE_RESISTANT_CASING PPS_CORROSION_RESISTANT_MECHANICAL_HOUSING 
 2 lightning_rod                              mbs    TierCasingCrossRecipeMultiblockMachine.c | ARC_GENERATOR_RECIPES | HYPER_CORE LAFIUM_MECHANICAL_CASING 
 2 magnetic_energy_reaction_furnace           mbs    CoilCrossRecipeMultiblockMachine         | gt:ARC_FURNACE_RECIPES | LAFIUM_MECHANICAL_CASING TRANSCENDENTALLY_AMPLIFIED_MAGNETIC_CONFINEMENT_CASING 
 2 mega_wiremill                              mbs    CoilCrossRecipeMultiblockMachine.createC | gt:WIREMILL_RECIPES, FIBER_EXTRUSION_RECIPES | HIGH_STRENGTH_SUPPORT_SPINDLE PIKYONIUM_MACHINE_CASING 
 2 nanites_circuit_assembly_factory           mbs    CrossRecipeMultiblockMachine             | gt:CIRCUIT_ASSEMBLER_RECIPES | HYPER_CORE PIKYONIUM_MACHINE_CASING 
 2 ph_neutralization_purification_unit        mbs    PHNeutralizationPurificationUnitMachine  | WATER_PURIFICATION_PLANT_RECIPES | CHEMICAL_GRADE_GLASS INERT_NEUTRALIZATION_WATER_PLANT_CASING (+gto machines)
 2 plasma_condenser                           mbs    TierCasingMultiblockMachine.createMachin | PLASMA_CONDENSER_RECIPES | IRIDIUM_PIPE_CASING LASER_COOLING_CASING 
 2 residual_decontaminant_degasser_purification_unit mbs    ResidualDecontaminantDegasserPurificatio | WATER_PURIFICATION_PLANT_RECIPES | OMNI_PURPOSE_INFINITY_FUSED_GLASS PLASMA_HEATER_CASING (+gto machines)
 2 sps_crafting                               mbs    ElectricMultiblockMachine                | TRANSCENDING_CRAFTING_RECIPES | MAGIC_CORE SPS_CASING 
 2 super_particle_collider                    mbs    ElectricMultiblockMachine                | SUPER_PARTICLE_COLLIDER_RECIPES | AGGREGATIONE_CORE LAFIUM_MECHANICAL_CASING 
 2 virtual_coin_miner                         mbs    VirtualCoinMiner                         | DUMMY_RECIPES | INSULATION_TILE_MECHANICAL_BLOCK OPTICAL_DYNAMIC_COATING_INSTRUMENT_PROTECTIVE_SHIELD_GLAS 
 3 absolute_baryonic_perfection_purification_unit mbs    AbsoluteBaryonicPerfectionPurificationUn | WATER_PURIFICATION_PLANT_RECIPES | NON_PHOTONIC_MATTER_EXCLUSION_GLASS QUARK_EXCLUSION_CASING QUARK_PIPE 
 3 assembler_module                           mbs    (holder                                  | ASSEMBLER_MODULE_RECIPES | MODULE_CONNECTOR SPACE_ELEVATOR_MECHANICAL_CASING SPACE_ELEVATOR_MODULE_BASE 
 3 bioengineering_module                      mbs    h -> new NanitesModuleMachine(h, 2       | NANITES_INTEGRATED_PROCESSING_CENTER_RECIPES | BIOACTIVE_MECHANICAL_CASING HIGH_ENERGY_ULTRAVIOLET_EMITTER_CASING STERILE_WATER_PLANT_CAS 
 3 crystal_builder                            mbs    CoilCrossRecipeMultiblockMachine         | gt:AUTOCLAVE_RECIPES,CRYSTALLIZATION_RECIPES | HYPER_CORE PIKYONIUM_MACHINE_CASING QUANTUM_GLASS 
 3 dissolution_core                           mbs    CoilCrossRecipeMultiblockMachine.createC | DISSOLUTION_TREATMENT_RECIPES, DIGESTION_TREATMENT_RECIPES | PI_HIGH_TEMPERATURE_INSULATION_MECHANICAL_HOUSING PLASMA_HEATER_CASING PPS_CORROSION_RESIS 
 3 dissolving_tank                            inline DissolvingTankMachine                    | DISSOLUTION_TREATMENT_RECIPES | IRIDIUM_PIPE_CASING PRESSURE_RESISTANT_HOUSING_MECHANICAL_BLOCK STAINLESS_STEEL_CORROSION_ 
 3 fast_neutron_breeder_reactor               mbs    FastNeutronBreederReactor                | FAST_NEUTRON_BREEDER_REACTOR_RECIPES | FISSION_COOLER_COMPONENT FISSION_FUEL_COMPONENT HIGH_STRENGTH_SUPPORT_SPINDLE (+gto machines)
 3 field_extruder_factory                     mbs    CrossRecipeMultiblockMachine             | gt:EXTRUDER_RECIPES | BOROSILICATE_GLASS HIGH_PRESSURE_RESISTANT_CASING HYPER_CORE 
 3 flocculation_purification_unit             mbs    FlocculationPurificationUnitMachine      | WATER_PURIFICATION_PLANT_RECIPES | CHEMICAL_GRADE_GLASS FLOCCULATION_CASING REINFORCED_STERILE_WATER_PLANT_CASING 
 3 gemini_containment_system                  mbs    CoilCrossRecipeMultiblockMachine         | PACKER_RECIPES, UNPACKER_RECIPES | ENGINEERING_MECHANICAL_CASING INDUSTRIAL_FRAMELESS_GLASS PEEK_WEAR_RESISTANT_MECHANICAL_HO 
 3 giant_sintering_array                      mbs    CoilTieredCasingMultiblockMachine.create | SINTERING_FURNACE_RECIPES | IRIDIUM_GEARBOX IRIDIUM_PIPE_CASING PLASMA_HEATER_CASING 
 3 hyper_reactor                              inline ElectricMultiblockMachine                | HYPER_REACTOR_RECIPES | ENHANCE_HYPER_MECHANICAL_CASING HYPER_CORE PIKYONIUM_MACHINE_CASING 
 3 hyperdimensional_plasma_fusion_core        mbs    DimensionallyTranscendentPlasmaForgeMach | DIMENSIONALLY_TRANSCENDENT_PLASMA_FORGE_RECIPES,STELLAR_FORGE_RECIPES | DIMENSIONAL_BRIDGE_CASING HYPER_CORE SPS_CASING 
 3 integrated_vapor_deposition_system         mbs    TierCasingCrossRecipeMultiblockMachine.c | CHEMICAL_VAPOR_DEPOSITION_RECIPES, PHYSICAL_VAPOR_DEPOSITION_RECIPES | LAFIUM_MECHANICAL_CASING QUANTUM_GLASS SPS_CASING 
 3 large_algae_farm                           mbs    LargeAlgaeFarm                           | DUMMY_RECIPES | BIOLOGICAL_MECHANICAL_CASING IRIDIUM_PIPE_CASING STAINLESS_STEEL_CORROSION_RESISTANT_CASIN 
 3 magnetic_confinement_dimensionality_shock_device mbs    CrossRecipeMultiblockMachine             | DIMENSIONALLY_TRANSCENDENT_SHOCK_RECIPES | AMPROSIUM_CASING DIMENSIONAL_BRIDGE_CASING HIGH_PRESSURE_RESISTANT_CASING 
 3 mega_bath_tank                             mbs    CrossRecipeMultiblockMachine             | gt:CHEMICAL_BATH_RECIPES,gt:ORE_WASHER_RECIPES | CHEMICAL_GRADE_GLASS FLOCCULATION_CASING REINFORCED_STERILE_WATER_PLANT_CASING 
 3 mega_se_assembler                          mbs    (h                                       | ASSEMBLER_MODULE_RECIPES | MODULE_CONNECTOR SPACE_ELEVATOR_MECHANICAL_CASING SPACE_ELEVATOR_MODULE_BASE 
 3 molecular_transformer                      inline CrossRecipeMultiblockMachine             | MOLECULAR_TRANSFORMER_RECIPES | IRIDIUM_PIPE_CASING TITANIUM_ALLOY_FRAME_INTERNAL TUNGSTEN_ALLOY_RADIATION_SHIELDING_MECHA 
 3 ozonation_purification_unit                mbs    OzonationPurificationUnitMachine         | WATER_PURIFICATION_PLANT_RECIPES | CHEMICAL_GRADE_GLASS HIGH_PRESSURE_RESISTANT_CASING OZONE_CASING 
 3 particle_stream_matrix_filling_machine     mbs    CoilCrossRecipeMultiblockMachine         | gt:CANNER_RECIPES | HIGH_PRESSURE_RESISTANT_CASING LAFIUM_MECHANICAL_CASING SPEEDING_PIPE 
 3 resource_collection_module                 mbs    (holder                                  | MINER_MODULE_RECIPES,DRILLING_MODULE_RECIPES | MODULE_CONNECTOR SPACE_ELEVATOR_MECHANICAL_CASING SPACE_ELEVATOR_MODULE_BASE 
 3 space_probe_surface_reception              mbs    SpaceProbeSurfaceReceptionMachine        | SPACE_PROBE_SURFACE_RECEPTION_RECIPES | COSMIC_DETECTION_RECEIVER_MATERIAL_RAY_ABSORBING_ARRAY HIGH_PRESSURE_RESISTANT_CASING HYPE 
 3 water_purification_plant                   mbs    WaterPurificationPlantMachine            | WATER_PURIFICATION_PLANT_RECIPES | CHEMICAL_GRADE_GLASS REINFORCED_STERILE_WATER_PLANT_CASING STERILE_WATER_PLANT_CASING 
 4 advanced_hyper_reactor                     mbs    ElectricMultiblockMachine                | ADVANCED_HYPER_REACTOR_RECIPES | DIMENSIONAL_BRIDGE_CASING ECHO_CASING ENHANCE_HYPER_MECHANICAL_CASING HYPER_CORE 
 4 advanced_infinite_driller                  mbs    AdvancedInfiniteDrillMachine             | gt:DUMMY_RECIPES | DIMENSIONAL_BRIDGE_CASING HYPER_CORE MACHINE_CASING_GRINDING_HEAD NAQUADRIATICTARANIUM_COI 
 4 dyson_sphere_receiving_station             mbs    DysonSphereReceivingStationMcahine       | gt:DUMMY_RECIPES | ENHANCE_HYPER_MECHANICAL_CASING HYPER_CORE SPACE_ELEVATOR_INTERNAL_SUPPORT SPACE_ELEVATOR_ 
 4 extreme_compressor                         mbs    CrossRecipeMultiblockMachine             | COMPRESSOR_RECIPES, GAS_COMPRESSOR_RECIPES, THERMO_PRESSING_RECIPES | HIGH_PRESSURE_RESISTANT_CASING HIGH_STRENGTH_SUPPORT_SPINDLE IRIDIUM_GEARBOX IRIDIUM_PIPE_ 
 4 extreme_temperature_fluctuation_purification_unit mbs    ExtremeTemperatureFluctuationPurificatio | WATER_PURIFICATION_PLANT_RECIPES | CHEMICAL_GRADE_GLASS PLASMA_HEATER_CASING REINFORCED_STERILE_WATER_PLANT_CASING SPEEDING_P (+gto machines)
 4 life_forge                                 mbs    CoilCrossRecipeMultiblockMachine         | BIOCHEMICAL_EXTRACTION_RECIPES, BIOCHEMICAL_REACTION_RECIPES | BIOACTIVE_MECHANICAL_CASING HYPER_CORE SPS_CASING STERILE_WATER_PLANT_CASING 
 4 mantle_crusher                             mbs    CrossRecipeMultiblockMachine             | CRUSHER_RECIPES, gt:ROCK_BREAKER_RECIPES | HIGH_STRENGTH_SUPPORT_SPINDLE IRIDIUM_GEARBOX IRIDIUM_PIPE_CASING MACHINE_CASING_GRINDING_ 
 4 mega_se_assembly_line                      mbs    (h                                       | DUMMY_RECIPES | MODULE_CONNECTOR SPACETIME_ASSEMBLY_LINE_CASING SPACE_ELEVATOR_MECHANICAL_CASING SPACE_ELE 
 4 mega_se_mining                             mbs    (h                                       | MINER_MODULE_RECIPES, DRILLING_MODULE_RECIPES | HIGH_STRENGTH_SUPPORT_SPINDLE MODULE_CONNECTOR SPACE_ELEVATOR_MECHANICAL_CASING SPACE_ELEV 
 4 microorganism_master                       mbs    CrossRecipeMultiblockMachine             | INCUBATOR_RECIPES | BIOACTIVE_MECHANICAL_CASING HIGH_ENERGY_ULTRAVIOLET_EMITTER_CASING HYPER_CORE LAW_FILTER_C 
 4 pigment_mixer                              mbs    PigmentMixer                             | PIGMENT_MIXING_RECIPES | BOROSILICATE_GLASS PRESSURE_RESISTANT_HOUSING_MECHANICAL_BLOCK STABLE_BASE_CASING STAINLES 
 4 swarm_core                                 mbs    CustomParallelMultiblockMachine.createPa | NANO_FORGE_RECIPES | COSMIC_NEUTRONIUM_BOROSILICATE_GLASS DIMENSIONAL_BRIDGE_CASING NAQUADRIATICTARANIUM_COIL_B 
 5 advanced_sps_crafting                      mbs    CrossRecipeMultiblockMachine             | TRANSCENDING_CRAFTING_RECIPES | AMPROSIUM_CASING FUSION_COIL_MK2 HIGH_PRESSURE_RESISTANT_CASING MAGIC_CORE SPS_CASING 
 5 desulfurizer                               inline CoilCrossRecipeMultiblockMachine         | DESULFURIZER_RECIPES | HSSS_BOROSILICATE_GLASS INSULATION_TILE_MECHANICAL_BLOCK IRIDIUM_PIPE_CASING SMELTING_CONT 
 5 electric_implosion_compressor              mbs    CrossRecipeMultiblockMachine             | ELECTRIC_IMPLOSION_COMPRESSOR_RECIPES | AMPROSIUM_BOROSILICATE_GLASS ENERGY_CONTROL_CASING_MK3 TITANIUM_ALLOY_FRAME_INTERNAL TUNGS 
 5 large_perfusion_device                     mbs    ManaMultiblockMachine                    | INFUSER_CORE_RECIPES | INFUSED_GOLD_CASING INFUSED_GOLD_REINFORCED_WOODEN_CASING SOURCE_FIBER_MECHANICAL_CASING S 
 5 matter_fabricator                          inline CrossRecipeMultiblockMachine             | MATTER_FABRICATOR_RECIPES | DIMENSIONAL_BRIDGE_CASING ENERGY_CONTROL_CASING_MK3 HYPER_CORE SPS_CASING TUNGSTEN_ALLOY_R 
 5 rune_engraving_chamber                     mbs    ManaMultiblockMachine                    | RUNE_ENGRAVING_RECIPES | ALFSTEEL_CASING INFUSED_GOLD_CASING ORIGINAL_BRONZE_CASING SOURCE_FIBER_MECHANICAL_CASING  
 5 space_station                              inline SimpleSpaceStationMachine                | DUMMY_RECIPES | ALUMINUM_ALLOY_2090_SKIN_MECHANICAL_BLOCK ALUMINUM_ALLOY_7050_SUPPORT_MECHANICAL_BLOCK ALU 
 5 the_primordial_reconstructor               inline ThePrimordialReconstructor               | gt:DUMMY_RECIPES | HERETICAL_MECHANICAL_CASING SOURCE_FIBER_MECHANICAL_CASING SOURCE_STONE_CASING SPELL_PRISM 
 5 wood_distillation                          mbs    CoilCrossRecipeMultiblockMachine         | WOOD_DISTILLATION_RECIPES | INSULATION_TILE_MECHANICAL_BLOCK LOAD_BEARING_STRUCTURAL_STEEL_MECHANICAL_BLOCK STAINLESS_ 
 6 nano_phagocytosis_plant                    mbs    NanoPhagocytosisPlantMachine             | MACERATOR_RECIPES,ISA_MILL_RECIPES,ULTRA_FINE_GRINDING_RECIPES | ECHO_CASING FUSION_COIL_MK2 HIGH_ENERGY_ULTRAVIOLET_EMITTER_CASING HYPER_CORE IRIDIUM_PIPE 
 6 plasma_extraction                          mbs    ElectricMultiblockMachine                | PLASMA_EXTRACTION_RECIPES | ADVANCED_FUSION_COIL HYPER_CORE LAW_FILTER_CASING QUANTUM_GLASS QUARK_PIPE SHIELDED_ACCELE 
 6 space_elevator                             mbs    SpaceElevatorMachine                     | gt:DUMMY_RECIPES | MODULE_CONNECTOR SPACE_ELEVATOR_INTERNAL_SUPPORT SPACE_ELEVATOR_MECHANICAL_CASING SPACE_EL 
 7 neutron_compressor                         mbs    ElectricMultiblockMachine                | NEUTRON_COMPRESSOR_RECIPES | AMPROSIUM_CASING DIMENSIONAL_BRIDGE_CASING DIMENSIONAL_STABILITY_CASING INFINITY_COIL_BLOC 
 7 planet_core_drilling                       mbs    StarcoreMinerMachine                     | gt:DUMMY_RECIPES | DIMENSIONAL_BRIDGE_CASING ECHO_CASING HIGH_PRESSURE_RESISTANT_CASING HYPER_CORE MACHINE_CA 
 7 resonance_flower                           mbs    ResonanceFlowerMachine                   | ELEMENTAL_RESONANCE | ORIGINAL_BRONZE_CASING SOURCE_STONE_CASING SPELL_PRISM_CASING TERRASTEEL_CASING THE_CHAOS_ 
 7 stellar_forge                              mbs    StellarForgeMachine                      | STELLAR_FORGE_RECIPES | ADVANCED_FUSION_COIL ENHANCE_HYPER_MECHANICAL_CASING HERETICAL_MECHANICAL_CASING MAGIC_COR 
 7 transliminal_oasis                         mbs    TierCasingCrossRecipeMultiblockMachine.c | GREENHOUSE_RECIPES,TREE_GROWTH_SIMULATOR_RECIPES | BIOACTIVE_MECHANICAL_CASING BOROSILICATE_GLASS CHEMICAL_GRADE_GLASS FLOCCULATION_CASING HY 
 8 cosmic_celestial_spire_of_convergence      mbs    CosmicCelestialSpireOfConvergence        | CELESTIAL_CONDENSER_RECIPES | HERETICAL_MECHANICAL_CASING INFUSED_GOLD_REINFORCED_WOODEN_CASING ORICHALCOS_CASING SOURCE 
 8 fuel_refining_complex                      mbs    CoilCrossRecipeMultiblockMachine.createC | FUEL_REFINING_RECIPES | INDUSTRIAL_FRAMELESS_GLASS LOAD_BEARING_STRUCTURAL_STEEL_MECHANICAL_BLOCK LOW_TEMPERATURE_ 
 8 large_alchemical_device                    inline LargeAlchemicalDeviceMachine             | ALCHEMY_CAULDRON_RECIPES | CHEMICAL_GRADE_GLASS ELEMENTIUM_CASING HERETICAL_MECHANICAL_CASING IRIDIUM_PIPE_CASING MAN 
 8 neutron_forging_anvil                      mbs    CrossRecipeMultiblockMachine             | gt:FORGE_HAMMER_RECIPES,ISOSTATIC_PRESSING_RECIPES | AMPROSIUM_BOROSILICATE_GLASS COMPRESSOR_PIPE_CASING ENHANCE_HYPER_MECHANICAL_CASING GRAVIT 
 8 petrochemical_plant                        mbs    CoilCrossRecipeMultiblockMachine         | PETROCHEMICAL_PLANT_RECIPES | CHEMICAL_GRADE_GLASS INDUSTRIAL_FRAMELESS_GLASS IRIDIUM_PIPE_CASING PIKYONIUM_MACHINE_CASI 
 8 processing_encapsulator                    mbs    ProcessingEncapsulatorMachine            | gt:DUMMY_RECIPES | DIMENSIONAL_BRIDGE_CASING ENHANCE_HYPER_MECHANICAL_CASING GRAVITY_STABILIZATION_CASING HER (+gto machines)
 8 quantum_force_transformer                  mbs    ElectricMultiblockMachine                | QUANTUM_FORCE_TRANSFORMER_RECIPES | HYPER_CORE LAW_FILTER_CASING MANIPULATOR QUANTUM_FORCE_TRANSFORMER_COIL QUANTUM_GLASS SPAC 
 9 nyarlathoteps_tentacle                     mbs    CoilCrossRecipeMultiblockMachine         | SUPRACHRONAL_ASSEMBLY_LINE_RECIPES, ASSEMBLY_LINE_RECIPES, CIRCUIT_ASS | ADVANCED_FUSION_COIL DIMENSIONAL_BRIDGE_CASING HYPER_CORE LASER_COOLING_CASING QUANTUM_GLA 
 9 plasma_centrifuge                          mbs    ElectricMultiblockMachine                | PLASMA_CENTRIFUGE_RECIPES | AMPROSIUM_CASING DIMENSIONAL_BRIDGE_CASING GRAVITY_STABILIZATION_CASING HYPER_CORE QUANTUM 
10 dyson_sphere_launch_silo                   mbs    DysonSphereLaunchSiloMachine             | DYSON_SPHERE_RECIPES | DIMENSIONAL_BRIDGE_CASING DYSON_DEPLOYMENT_CASING DYSON_DEPLOYMENT_CORE DYSON_DEPLOYMENT_M 
12 kerr_newman_homogenizer                    mbs    KerrNewmanHomogenizer                    | MIXER_RECIPES | ACCELERATOR_ELECTROMAGNETIC_COIL_CONSTRAINT_CASING_UHV ADVANCED_FUSION_COIL BIOACTIVE_MECH 
14 road_of_heaven                             mbs    SuperSpaceElevatorMachine                | gt:DUMMY_RECIPES | AMPROSIUM_CASING ENHANCE_HYPER_MECHANICAL_CASING HIGH_STRENGTH_SPACE_ELEVATOR_CABLE HIGH_S 
15 large_expandable_space_station_core_module inline Core                                     | DUMMY_RECIPES | ALUMINUM_ALLOY_2090_SKIN_MECHANICAL_BLOCK ALUMINUM_ALLOY_7050_SUPPORT_MECHANICAL_BLOCK ALU 
215
```
