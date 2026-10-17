package com.raishxn.gtna.data;

import com.gregtechceu.gtceu.api.GTCEuAPI;
import com.gregtechceu.gtceu.api.GTValues;
import com.gregtechceu.gtceu.api.data.chemical.material.Material;
import com.gregtechceu.gtceu.api.data.tag.TagPrefix;

import net.minecraft.ChatFormatting;
import net.minecraft.data.PackOutput;
import net.minecraftforge.common.data.LanguageProvider;

import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import com.raishxn.gtna.GTNACORE;
import com.raishxn.gtna.api.data.tag.GTNATagPrefix;
import com.raishxn.gtna.common.data.GTNAEyeOfHarmonyContent;
import com.raishxn.gtna.common.data.GTNAMachines2;
import com.raishxn.gtna.utils.TextUtil;
import org.apache.commons.lang3.text.WordUtils;

import java.io.IOException;
import java.io.Reader;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashSet;
import java.util.Locale;
import java.util.Set;

public class GTNALangProvider extends LanguageProvider {

    private final Set<String> addedKeys = new HashSet<>();
    private final PackOutput output;

    private static final TagPrefix[] GTNA_PREFIXES = {
            GTNATagPrefix.doubleIngot,
            GTNATagPrefix.membraneElectrode,
            GTNATagPrefix.tripleIngot,
            GTNATagPrefix.quadrupleIngot,
            GTNATagPrefix.quintupleIngot,
            GTNATagPrefix.triplePlate,
            GTNATagPrefix.quadruplePlate,
            GTNATagPrefix.quintuplePlate,
            GTNATagPrefix.superdensePlate,
            GTNATagPrefix.singularity,
            GTNATagPrefix.brick,
            GTNATagPrefix.roughBlank,
            GTNATagPrefix.flake,
            GTNATagPrefix.MILLED
    };

    /**
     * Registrate's lang provider and this one both target {@code assets/gtna/lang/en_us.json}; two writers erase each
     * other. Feed these translations into Registrate's provider instead (GTNA values win over Registrate defaults).
     */
    public static void feed(com.tterrag.registrate.providers.RegistrateLangProvider registrate, PackOutput output) {
        java.util.Map<String, String> data;
        try {
            var field = net.minecraftforge.common.data.LanguageProvider.class.getDeclaredField("data");
            field.setAccessible(true);
            @SuppressWarnings("unchecked")
            var map = (java.util.Map<String, String>) field.get(registrate);
            data = map;
        } catch (ReflectiveOperationException e) {
            throw new IllegalStateException("cannot merge GTNA translations into Registrate", e);
        }
        new GTNALangProvider(output) {

            @Override
            public void add(String key, String value) {
                data.put(key, value);
            }
        }.addTranslations();
    }

    public GTNALangProvider(PackOutput output) {
        super(output, GTNACORE.MOD_ID, "en_us");
        this.output = output;
    }

    @Override
    public void add(String key, String value) {
        if (addedKeys.contains(key)) {
            return;
        }
        addedKeys.add(key);
        super.add(key, value);
    }

    /** Registers a Steam Elevator module's block name for its tier I/II/III items ({@code baseId_i/_ii/_iii}). */
    private void elevatorModuleTiers(String baseId, String name) {
        String[] suffixes = { "_i", "_ii", "_iii" };
        String[] romans = { " I", " II", " III" };
        for (int tier = 0; tier < suffixes.length; tier++) {
            add("block.gtna." + baseId + suffixes[tier], name + romans[tier]);
        }
    }

    @Override
    protected void addTranslations() {
        // Standard multiblock tooltips (tools/apply_multiblock_tooltips.py)
        com.raishxn.gtna.common.data.GTNAMultiblockTooltipText.ENGLISH.forEach((id, lines) -> {
            for (int i = 0; i < lines.length; i++) {
                add("gtna.machine." + id + ".tooltip." + i, lines[i]);
            }
        });
        // Forge of Gods (GTNH)
        com.raishxn.gtna.data.lang.GodforgeLang.add(this);
        add("gtna.godforge.gui.threads", "Threads: %s");
        add("gtna.godforge.gui.threads.locked", "Thread Hatch locked: needs %s (unlocked up to %s)");
        add("gtna.godforge.machine_type.stellar_forge", "Stellar Forge");
        add("gtna.godforge.machine_type.blast_furnace", "Blast Furnace, Furnace");
        add("gtna.godforge.machine_type.blast_smelter", "Blast Smelter");
        add("gtna.godforge.machine_type.plasma_fabricator", "Plasma Fabricator");
        add("gtna.godforge.machine_type.exotic_matter_producer", "Exotic Matter Producer");
        add("block.gtna.singularity_reinforced_stellar_shielding_casing",
                "Singularity Reinforced Stellar Shielding Casing");
        add("block.gtna.singularity_reinforced_stellar_shielding_casing.tooltip.0",
                "Shielded by the event horizon of a singularity");
        add("block.gtna.singularity_reinforced_stellar_shielding_casing.tooltip.1", "Don't get too close...");
        add("block.gtna.celestial_matter_guidance_casing", "Celestial Matter Guidance Casing");
        add("block.gtna.celestial_matter_guidance_casing.tooltip.0",
                "Designed to route stellar matter using spacetime distortion");
        add("block.gtna.celestial_matter_guidance_casing.tooltip.1", "Reality Distortion");
        add("block.gtna.boundless_gravitationally_severed_structure_casing",
                "Boundless Gravitationally Severed Structure Casing");
        add("block.gtna.boundless_gravitationally_severed_structure_casing.tooltip.0",
                "Unaffected by gravitational forces");
        add("block.gtna.boundless_gravitationally_severed_structure_casing.tooltip.1",
                "Not even a black hole could tear it apart.");
        add("block.gtna.transcendentally_amplified_magnetic_confinement_casing",
                "Transcendentally Amplified Magnetic Confinement Casing");
        add("block.gtna.transcendentally_amplified_magnetic_confinement_casing.tooltip.0",
                "Creates enormous magnetic fields capable of constraining entire stars");
        add("block.gtna.transcendentally_amplified_magnetic_confinement_casing.tooltip.1", "It's super effective!");
        add("block.gtna.stellar_energy_siphon_casing", "Stellar Energy Siphon Casing");
        add("block.gtna.stellar_energy_siphon_casing.tooltip.0",
                "Taps into streams of stellar matter to harness their heat energy");
        add("block.gtna.stellar_energy_siphon_casing.tooltip.1", "Turn up the heat!");
        add("block.gtna.remote_graviton_flow_modulator", "Remote Graviton Flow Modulator");
        add("block.gtna.remote_graviton_flow_modulator.tooltip.0",
                "Controls the flow of gravitons to manipulate gravity");
        add("block.gtna.remote_graviton_flow_modulator.tooltip.1", "Exponential scaling past 800 Galaxies");
        add("block.gtna.medial_graviton_flow_modulator", "Medial Graviton Flow Modulator");
        add("block.gtna.medial_graviton_flow_modulator.tooltip.0",
                "Controls the flow of gravitons to manipulate gravity");
        add("block.gtna.medial_graviton_flow_modulator.tooltip.1", "Getting closer...");
        add("block.gtna.central_graviton_flow_modulator", "Central Graviton Flow Modulator");
        add("block.gtna.central_graviton_flow_modulator.tooltip.0",
                "Controls the flow of gravitons to manipulate gravity");
        add("block.gtna.central_graviton_flow_modulator.tooltip.1", "Gravity Central");
        add("block.gtna.harmonic_phonon_transmission_conduit", "Harmonic Phonon Transmission Conduit");
        add("block.gtna.harmonic_phonon_transmission_conduit.tooltip.0",
                "Transfers and stores extreme amounts of heat without any loss");
        add("block.gtna.harmonic_phonon_transmission_conduit.tooltip.1", "<<<Thermal<<< >>>Wave>>>");
        add("block.gtna.spatially_transcendent_gravitational_lens", "Spatially Transcendent Gravitational Lens");
        add("block.gtna.spatially_transcendent_gravitational_lens.tooltip.0", "Gravitational lensing taken literal");
        add("block.gtna.spatially_transcendent_gravitational_lens.tooltip.1", "GraviLens 9000!");
        add("block.gtna.hypogen_coil", "Hypogen Coil Block");
        add("gtna.godforge.casing_mark", "§9Tec§1Tech§9: Project Godforge");
        add("block.gtna.forge_of_gods", "Forge of the Gods");
        add("block.gtna.godforge_smelting_module", "Helioflare Power Forge");
        add("block.gtna.godforge_molten_module", "Helioflux Melting Core");
        add("block.gtna.godforge_plasma_module", "Heliothermal Plasma Fabricator");
        add("block.gtna.godforge_exotic_module", "Heliofusion Exoticizer");
        add("gtna.godforge.animations.enabled", "Animations are now enabled.");
        add("gtna.godforge.animations.disabled", "Animations are now disabled.");
        add("gtna.godforge.info.rings", "Number of Rings: %s");
        add("gtna.subtitle.godforge.loop", "Forge of the Gods hums");
        add("gtna.godforge.info.upgrades", "Total Upgrades Unlocked: %s");
        add("gtna.godforge.info.connected", "Connected Modules: %s/%s");
        add("gtna.godforge.gui.no_extra_cost", "No upgrade needs extra materials");
        add("gtna.godforge.gui.battery_locked", "Requires Relativistic Electron Capacitor (upgrade)");
        add("gtna.godforge.gui.voltage_config", "Voltage Config");
        add("gtna.godforge.gui.max_parallel", "Max");
        add("gtna.godforge.gui.max_parallel.tooltip", "Always use the maximum parallel");
        add("gtna.godforge_plasma", "Godforge Plasma");
        add("gtna.godforge_molten", "Helioflux Melting Core");
        add("gtna.godforge.exotic.mode.qgp", "Mode: Quark Gluon Plasma");
        add("gtna.godforge.exotic.mode.magmatter", "Mode: Magmatter");
        add("gtna.godforge.exotic.requires", "Requires %s: %s mB");
        add("gtna.godforge.exotic.mode.locked", "Magmatter mode needs the forge's Effortless Existence (EE) upgrade.");
        addManualTranslations();
        addEyeOfHarmonyContentNames();
        for (Material material : java.util.List.of(
                com.raishxn.gtna.common.data.GTNAMaterials.SpaceTime,
                com.raishxn.gtna.common.data.GTNAMaterials.RawStarMatter,
                com.raishxn.gtna.common.data.GTNAMaterials.WhiteDwarfMatter,
                com.raishxn.gtna.common.data.GTNAMaterials.BlackDwarfMatter,
                com.raishxn.gtna.common.data.GTNAMaterials.Universium,
                com.raishxn.gtna.common.data.GTNAMaterials.Time,
                com.raishxn.gtna.common.data.GTNAMaterials.Space)) {
            add(material.getUnlocalizedName(), material.getDefaultTranslation());
        }
        for (int tier = GTValues.LV; tier <= GTValues.IV; tier++) {
            add("block.gtna." + GTValues.VN[tier].toLowerCase(Locale.ROOT) + "_world_data_scanner",
                    GTValues.VN[tier] + " World Data Scanner");
        }
        add("gtna.jade.void_random_pool", "Random mining: %s possible ores");
        add("gtna.jade.void_random_chance", "Chance per ore/run: %s%%. Not all ores drop each cycle.");
        add("item.gtna.deposit_recorder", "Deposit Recorder");
        add("item.gtna.deposit_data", "Deposit Data");
        add("item.gtna.fluid_separation_filter", "Fluid Separation Filter");
        add("item.gtna.essence", "Essence");
        add("item.gtna.essence_seed", "Essence Seed");
        for (String stage : java.util.List.of("terrestrial", "t1", "t2", "t3", "t4", "t5")) {
            add("item.gtna.fluid_remote_upgrade_" + stage,
                    "Remote Fluid Upgrade " + stage.toUpperCase(Locale.ROOT));
        }
        for (String id : com.raishxn.gtna.common.data.GTNAItems.VEIN_ESSENCES.keySet()) {
            add("item.gtna." + id, com.gregtechceu.gtceu.utils.FormattingUtil.toEnglishName(id));
        }
        for (String world : java.util.List.of("overworld", "nether", "end")) {
            add("item.gtna." + world + "_data",
                    com.gregtechceu.gtceu.utils.FormattingUtil.toEnglishName(world) + " Data Chip");
        }
        for (String planet : com.raishxn.gtna.common.data.GTNAItems.PLANET_DATA_CHIP_PLANETS) {
            add("item.gtna.planet_data_chip_" + planet,
                    com.gregtechceu.gtceu.utils.FormattingUtil.toEnglishName(planet) + " Planet Data Chip");
        }
        add("gtna.void_fluid_drilling", "Void Fluid Drilling");
        add("key.gtna.research_tree", "Open Research Tree");
        add("key.categories.gtna", "GregTech Nexus Addon");
        add("gtna.research.screen.title", "Research");
        add("gtna.research.screen.empty", "No research is available in this world.");
        add("gtna.research.screen.progress", "%1$s of %2$s unlocked");
        add("gtna.research.tier", "Tier %s");
        add("gtna.research.state.unlocked", "Unlocked");
        add("gtna.research.state.available", "Available");
        add("gtna.research.state.locked", "Locked");
        add("gtna.research.kind.trunk", "Trunk");
        add("gtna.research.kind.branch", "Branch");
        add("gtna.research.kind.leaf", "Leaf");
        add("gtna.research.screen.select",
                "Click a node to see what it costs and what it needs. Drag or scroll to move around.");
        add("gtna.research.screen.click", "Click for details");
        add("gtna.research.screen.cost", "Cost (you have):");
        add("gtna.research.screen.free", "Free");
        add("gtna.research.screen.requirement", "Hold once: %s");
        add("gtna.research.screen.eureka.found", "Eureka found: %s%% off");
        add("gtna.research.screen.eureka.hint", "Eureka: analyse %s for %s%% off");
        add("gtna.research.screen.research", "Research");
        add("gtna.research.tooltip.obtain", "Obtain: %s");
        add("gtna.research.tooltip.requires", "Requires: %s");
        add("gtna.research.tooltip.recipes", "Unlocks %s machine recipes");
        add("gtna.research.task", "Research: %s");
        add("gtna.research.task.type", "Research node");
        add("gtna.research.unlocked", "Research unlocked: %s");
        add("gtna.research.viewer", "Research: %s");
        add("gtna.research.requires", "Requires research: %s");
        add("gtna.research.command.list", "%1$s: %2$s of %3$s research nodes unlocked");
        add("gtna.research.command.entry.unlocked", "[x] %1$s (tier %2$s)");
        add("gtna.research.command.entry.locked", "[ ] %1$s (tier %2$s)");
        add("gtna.research.command.info", "%1$s: tier %2$s, requires %3$s");
        add("gtna.research.command.none", "nothing");
        add("gtna.research.command.unknown", "Unknown research node %s");
        add("gtna.research.command.unlock.done", "Unlocked %1$s for %2$s");
        add("gtna.research.command.unlock.already", "%1$s is already unlocked for %2$s");
        add("gtna.research.command.unlock.missing", "%1$s needs: %2$s (add 'force' to unlock the whole chain)");
        add("gtna.research.command.reset", "Removed %1$s research entries from %2$s");
        add("gtna.research.points.gained", "+%s %s research");
        add("gtna.research.eureka", "Eureka! Analysing it taught you something: %s now costs less.");
        add("gtna.research.requirement_met", "Research requirement met: %s. You can now buy it with research points.");
        add("gtna.research.command.buy.done", "Researched %s.");
        add("gtna.research.command.buy.requirement", "%s needs %s to have been held once by your team first.");
        add("gtna.research.command.buy.points", "Not enough research points for %s: it costs %s.");
        add("gtna.research.command.points", "Research points of %s: %s");
        add("gtna.research.command.points.add", "%s is now %s for %s.");
        add("gtna.fluid.recorder.tooltip",
                "Use on a Fluid Drilling Rig after extraction. Use in air with Deposit Data in the other hand to copy. Requires a Data Stick.");
        add("gtna.fluid.data.tooltip",
                "Reusable discovery program for one fluid and origin. Shared with the discovering machine owner/team.");
        add("gtna.fluid.data.origin", "Origin: %s");
        add("gtna.fluid.recipe.origin", "Discovery origin: %s");
        add("gtna.fluid.recipe.remote", "Remote production: upgrade %s + matching power tier");
        add("gtna.fluid.data.fluid", "Fluid: %s");
        add("gtna.fluid.recorder.owner", "This discovery belongs to another player/team.");
        add("gtna.fluid.recorder.extract_first", "Complete an extraction cycle with available output space first.");
        add("gtna.fluid.recorder.unsupported", "No production program is configured for this fluid and origin.");
        add("gtna.fluid.recorder.stick", "A Data Stick is required in your inventory.");
        add("gtna.fluid.recorder.recorded", "Deposit recorded. The data is reusable.");
        add("gtna.fluid.recorder.copied", "Deposit Data copied.");
        add("gtna.fluid.rig.tooltip",
                "EV entry. Requires a recorded extraction, reusable Deposit Data and Drilling Fluid. Remote production needs the origin upgrade.");
        add("gtna.fluid.rig.reagent", "%s: %s mB/cycle");
        add("gtna.fluid.rig.rate", "Output rate: %s mB/s");
        add("gtna.fluid.rig.parallel", "Parallel cap: %s");
        add("gtna.fluid.rig.no_program", "Insert your recorded Deposit Data in the input bus.");
        add("gtna.fluid.rig.program", "Program: %s");
        add("gtna.fluid.rig.cost", "%s EU/t \u00b7 %s s/cycle \u00b7 %s parallel");
        add("gtna.fluid.rig.gated", "Waiting for valid discovery data, origin or remote upgrade.");
        addStaticTranslations();
        addTagPrefixCategories();
        for (Material material : GTCEuAPI.materialManager.getRegisteredMaterials()) {
            if (material.getModid().equals(GTNACORE.MOD_ID)) {
                String langKey = material.getUnlocalizedName();
                String matName = formatMaterialName(material.getName());

                add(langKey, matName);

                for (TagPrefix prefix : GTNA_PREFIXES) {
                    if (prefix.doGenerateItem(material)) {
                        String idNoMod = String.format(prefix.idPattern(), material.getName());
                        String itemKey = "item." + GTNACORE.MOD_ID + "." + idNoMod;
                        String itemValue = String.format(prefix.langValue(), matName);

                        add(itemKey, itemValue);
                    }
                }
            }
        }
    }

    private void addEyeOfHarmonyContentNames() {
        var families = java.util.List.of(GTNAEyeOfHarmonyContent.COMPRESSION_FIELDS,
                GTNAEyeOfHarmonyContent.ACCELERATION_FIELDS, GTNAEyeOfHarmonyContent.STABILISATION_FIELDS);
        for (var family : families) {
            for (var entry : family) {
                var block = entry.get();
                add(block, GTNAEyeOfHarmonyContent.TIER_NAMES[block.getFieldTier()] + " " +
                        block.getFamily().englishName + " Field Generator");
            }
        }
        add(GTNAEyeOfHarmonyContent.BOUNDARY_CASING.get(), "Infinite Spacetime Energy Boundary Casing");
        add(GTNAEyeOfHarmonyContent.SPATIAL_CASING.get(), "Reinforced Spatial Structure Casing");
        add(GTNAEyeOfHarmonyContent.TEMPORAL_CASING.get(), "Reinforced Temporal Structure Casing");
        add(GTNAEyeOfHarmonyContent.OVERWORLD_PLANET.get(), "Overworld Planet Block");
        add(GTNAEyeOfHarmonyContent.NETHER_PLANET.get(), "Nether Planet Block");
        add(GTNAEyeOfHarmonyContent.END_PLANET.get(), "End Planet Block");
        add(GTNAEyeOfHarmonyContent.ASTRAL_ARRAY_FABRICATOR.get(), "Astral Array Fabricator");
    }

    private void addManualTranslations() {
        Path manualLangPath = output.getOutputFolder()
                .getParent()
                .getParent()
                .resolve("main")
                .resolve("resources")
                .resolve("assets")
                .resolve(GTNACORE.MOD_ID)
                .resolve("lang")
                .resolve("en_us.json");
        if (!Files.exists(manualLangPath)) {
            return;
        }

        try (Reader reader = Files.newBufferedReader(manualLangPath, StandardCharsets.UTF_8)) {
            JsonObject json = JsonParser.parseReader(reader).getAsJsonObject();
            for (var entry : json.entrySet()) {
                JsonElement value = entry.getValue();
                if (value != null && value.isJsonPrimitive()) {
                    add(entry.getKey(), value.getAsString());
                }
            }
        } catch (IOException exception) {
            throw new RuntimeException("Failed to load manual GTNA en_us translations", exception);
        }
    }

    private String formatMaterialName(String name) {
        return WordUtils.capitalize(name.replace('_', ' '));
    }

    private void addTagPrefixCategories() {
        add(GTNATagPrefix.doubleIngot.getUnlocalizedName(), "Double Ingot");
        add(GTNATagPrefix.tripleIngot.getUnlocalizedName(), "Triple Ingot");
        add(GTNATagPrefix.quadrupleIngot.getUnlocalizedName(), "Quadruple Ingot");
        add(GTNATagPrefix.quintupleIngot.getUnlocalizedName(), "Quintuple Ingot");
        add(GTNATagPrefix.triplePlate.getUnlocalizedName(), "Triple Plate");
        add(GTNATagPrefix.quadruplePlate.getUnlocalizedName(), "Quadruple Plate");
        add(GTNATagPrefix.quintuplePlate.getUnlocalizedName(), "Quintuple Plate");
        add(GTNATagPrefix.superdensePlate.getUnlocalizedName(), "Superdense Plate");
        add(GTNATagPrefix.singularity.getUnlocalizedName(), "Singularity");
        add(GTNATagPrefix.brick.getUnlocalizedName(), "Brick");
        add(GTNATagPrefix.roughBlank.getUnlocalizedName(), "Rough Blank");
        add(GTNATagPrefix.flake.getUnlocalizedName(), "Flake");
        // Milled items are the first GTNA prefix applied to GTCEu materials, so the prefix string
        // must keep the material argument (as GTO's "Milled %s").
        add(GTNATagPrefix.MILLED.getUnlocalizedName(), "Milled %s");
    }

    private void addStaticTranslations() {
        // --- Ported-content attribution (appended to machine tooltips by GTNASources) ---
        add("gtna.tooltip.source", "Source: %s");
        add("gtna.tooltip.block_properties", "Hardness: %s Blast Resistance: %s");
        add("gtna.jade.need_grind_ball", "Need to grind ball");
        add("gtna.ui.voiding_mode", "Voiding Mode: %s");
        add("gtna.ui.parallel_max", "Performing up to %s Recipes in Parallel");
        add("gtna.ui.heat_capacity", "Heat Capacity: %s");
        add("gtna.ui.no_recipe_found", "No Recipe found");
        add("gtna.jade.energy_multiplier", "Total Energy Cost Multiplier: %s");
        add("gtna.jade.time_multiplier", "Total Time Cost Multiplier: %s");
        add("gtna.jade.chunk_not_forced", "The chunk the machine is in is not forced loaded");
        add("gtna.tooltip.gto_story", "GTO Story:");
        add("gtna.gto.blaze.header", "§9GTO Core | Machine");
        add("gtna.jade.hardness", "Hardness: %s");
        add("gtna.jade.blast_resistance", "Blast Resistance: %s");
        add("gtna.tooltip.recipe_types", "Recipe Types: ");
        add("gtna.story.fishing_ground.0", "Like eating fish?");
        add("gtna.story.fishing_ground.1", "The AFFL-200 fishing farm is a regular in GregTech cuisine.");
        add("gtna.story.fishing_ground.2", "Its intelligent breeding system delivers remarkable output.");
        add("gtna.story.fishing_ground.3", "It feeds an entire branch office with aquatic food.");
        add("gtna.story.component_assembler.0",
                "GTO's gift to new employees makes assembly feel like building blocks.");
        add("gtna.story.component_assembler.1", "The base handles recipes through IV; its extension reaches UV.");
        add("gtna.story.component_assembler.2",
                "Treat it well: your first salary may cost less than one of its parts.");
        add("gtna.story.blaze_blast_furnace.0",
                "A new Tinkers' Construct employee kept a blaze spawner among the furnaces.");
        add("gtna.story.blaze_blast_furnace.1",
                "The furnaces gained a coat of blaze residue and suddenly ran twice as fast.");
        add("gtna.story.blaze_blast_furnace.2", "They could also process 64 items in a batch.");
        add("gtna.story.blaze_blast_furnace.3", "The spawner was removed, but blaze acceleration stayed.");
        add("gtna.story.cold_ice_freezer.0", "A liquid ice leak led to the discovery of this cryogenic machine.");
        add("gtna.story.cold_ice_freezer.1",
                "The ice reacted with the aluminium frame to create a stable superconducting space.");
        add("gtna.story.cold_ice_freezer.2",
                "Tungsten steel pipes circulate the cold in a vortex and freeze 64 samples at once.");
        add("gtna.story.cold_ice_freezer.3",
                "The employee behind the accident vanished, but the chairman treasures the machine.");
        add("gtna.story.isa_mill.0", "The Isa 1672N mill is green on the outside, but hardly eco-friendly.");
        add("gtna.story.isa_mill.1", "Its exhaust smells strange, and few workers want to touch the messy output.");
        add("gtna.story.isa_mill.2", "Wet ball milling crushes ores with remarkable efficiency.");
        add("gtna.story.isa_mill.3", "The scientists reluctantly admit that brute force sometimes works.");
        add("gtna.story.industrial_flotation_cell.0", "The Isa U-276 ore separator is a mature purification machine.");
        add("gtna.story.industrial_flotation_cell.1",
                "Pine oil flotation leaves the workshop smelling of essential balm.");
        add("gtna.story.industrial_flotation_cell.2", "At least mosquitoes rarely bite anyone working here.");
        add("gtna.story.industrial_flotation_cell.3", "Safety first; stay alert around the machinery!");
        add("gtna.tooltip.machine_type", "Machine Type: %s");
        add("gtna.source.gto", "GregTech Odyssey (GTO)");
        add("gtna.source.gtna", "GregTech Nexus Addon (GTNA)");
        add("gtna.source.gtnl", "GT: Not Leisure (GTNL)");
        add("gtna.source.gtnh", "GT: New Horizons (GTNH)");
        add("gtna.source.gtneioreplugin", "GTNH NEI Ore Plugin");
        add("gtna.eoh.structure.uniform_compression", "All compression fields must use the same tier.");
        add("gtna.eoh.structure.uniform_acceleration", "All acceleration fields must use the same tier.");
        add("gtna.eoh.structure.uniform_stabilisation", "All stabilisation fields must use the same tier.");
        add("gtna.eoh.structure.fields",
                "138 compression, 168 acceleration and 48 stabilisation fields; uniform tier per family.");
        add("gtna.eoh.structure.ports",
                "Exactly 1 ME item input bus, 2 ME fluid input hatches, 1 ME item output bus and 1 ME fluid output hatch. No stocking, crafting buffers, dual or energy hatches.");
        add("gtna.eoh.structure.tiers", "Field tiers: Compression %1$s/9 · Acceleration %2$s/9 · Stabilisation %3$s/9");
        add("gtna.eoh.structure.component", "Eye of Harmony structure component.");
        add("gtna.eoh.field_tier", "Field Tier: %s / 9");
        add("gtna.eoh.field.compression", "Sets the supported planet tier; higher fields reduce processing time.");
        add("gtna.eoh.field.acceleration", "Accelerates time at the cost of recipe success chance.");
        add("gtna.eoh.field.stabilisation", "Improves success chance at the cost of material yield.");
        add("gtna.eoh.planet_dimension", "Planet Dimension: %s");
        add("gtna.eoh.component_stage",
                "Planet selector: only Overworld operates currently. Component crafting is not available yet.");
        add("gtna.eoh.jei.title", "Eye of Harmony");
        add("gtna.eoh.jei.page", "Products · Page %s/%s");
        add("gtna.eoh.jei.amount_item", "Base output: %s items");
        add("gtna.eoh.jei.amount_fluid", "Base amount: %s mB");
        add("gtna.eoh.jei.time", "Base time: %s ticks");
        add("gtna.eoh.jei.hydrogen", "Hydrogen: %s B");
        add("gtna.eoh.jei.helium", "Helium: %s B");
        add("gtna.eoh.jei.tier", "Spacetime Tier: %s");
        add("gtna.eoh.jei.input", "EU Input: %s EU");
        add("gtna.eoh.jei.output", "EU Output: %s EU");
        add("gtna.eoh.jei.chance", "Base Recipe Chance: %s%%");
        add("gtna.eoh.jei.efficiency", "Recipe Energy Efficiency: %s%%");
        add("gtna.eoh.jei.amount_buckets", "Base amount: %s buckets (%s mB)");
        add("gtna.eoh.jei.warning_base", "Warning: base outputs; fields and gas excess change quantities.");
        add("gtna.eoh.jei.warning", "Warning: Not all outputs displayed here (%s/%s)");
        add("emi.category.gtna.eye_of_harmony", "Eye of Harmony");
        add("gtna.eoh.jei.base", "Before fields, circuit, gas excess and Nexus loss");
        add("gtna.eoh.manual.hint", "Press Z for the next page");
        add("gtna.eoh.manual.page", "Eye of Harmony — page %s/%s");
        add("gtna.eoh.manual.page1", "Eye of Harmony — fields (1/2)");
        add("gtna.eoh.manual.page2", "Eye of Harmony — operation (2/2)");
        add("gtna.eoh.manual.fields",
                "Each field family has 9 tiers. Use a uniform tier within each family; the three families can differ.");
        add("gtna.eoh.manual.compression",
                "Compression: unlocks programs by minimum tier. Each tier above the minimum multiplies duration by 0.97 (3% faster).");
        add("gtna.eoh.manual.acceleration",
                "Time acceleration: each tier above the first halves duration and subtracts 9.25 percentage points from success chance.");
        add("gtna.eoh.manual.stabilisation",
                "Stabilisation: each tier above the first adds 5 percentage points to success chance and subtracts 5 points from output yield.");
        add("gtna.eoh.manual.energy",
                "The first stabilisation tier reduces base EU return by 40%. Each higher tier removes 5 points of this penalty.");
        add("gtna.eoh.manual.circuit",
                "Circuit 0–24: configuration k multiplies EU input by 4^k and duration by 2^-k. EU return and product yield are unchanged by the circuit.");
        add("gtna.eoh.manual.gas",
                "While idle and enabled, absorbs hydrogen and helium once per second. Starting a cycle consumes ALL stored gas, including excess.");
        add("gtna.eoh.manual.ratio", "For each gas: overflow ratio = stored / required - 1.");
        add("gtna.eoh.manual.penalty",
                "Penalty = 1 - exp(-(30 × overflow ratio)^2). Both gas penalties are subtracted from success chance and product yield, clamped to 0–100%.");
        add("gtna.eoh.manual.failure",
                "A failed Overworld cycle produces chance × 28,800 mB of molten SpaceTime instead of regular products. Failure still returns the same gross EU.");
        add("gtna.eoh.manual.pity",
                "Repeated failures at the same chance accumulate progress toward a guaranteed success. Gas excess still applies to the next cycle.");
        add("gtna.eoh.manual.ports",
                "Exactly one item input, two fluid inputs, one item output and one fluid output. Only finite-buffer ME inputs and ME outputs are supported; ordinary, stocking, crafting and dual ports are rejected.");
        add("gtna.eoh.manual.delivery",
                "Wireless energy uses the bound Nexus owner. EU input is charged once; outputs wait when ports or the network are full. Nexus transfer losses apply to the EU return.");
        add("gtna.eoh.manual.scope",
                "Programs: Overworld, Nether, End, Moon, Mars, Venus, Mercury and Glacio (planets need Ad Astra). Put the Planet Block in the controller slot; higher tier planets need more gas, more time and better compression fields. Astral Arrays and parallel operation are not implemented yet.");
        add("gtna.eoh.operation.gas_excess", "Gas excess: Hydrogen %s%% / Helium %s%%");
        add("gtna.eoh.operation.planet", "Planet: %s");
        add("gtna.eoh.operation.no_planet", "None");
        add("gtna.eoh.operation.circuit", "Circuit: %s (0–24)");
        add("gtna.eoh.operation.gas_required", "Required per gas: %s mB");
        add("gtna.eoh.operation.preview", "Preview after minimum gas fill: %s ticks");
        add("gtna.eoh.operation.chance_yield", "Chance: %s%% / Yield: %s%%");
        add("gtna.eoh.operation.return", "Gross return before Nexus loss: %s EU");
        add("gtna.eoh.operation.net", "Net before Nexus loss: %s EU");
        add("gtna.eoh.operation.pending_eu", "Gross EU still pending: %s");
        add("gtna.eoh.operation.planet_slot", "Planet catalyst");
        add("gtna.eoh.operation.summary_progress", "Progress: %s%% · Remaining: %s");
        add("gtna.eoh.operation.state.structure", "Incomplete structure.");
        add("gtna.eoh.operation.state.paused", "Operation paused.");
        add("gtna.eoh.operation.consumed_gases", "Consumed this cycle: Hydrogen %s B / Helium %s B");
        add("gtna.eoh.operation.consumed_unknown", "Consumed gas: unavailable for this older cycle.");
        add("gtna.nexus.direct_debit", "Last direct withdrawal: %s — %s EU");
        add("gtna.nexus.direct_debit_details", "One-time debit: %s EU\nPosition: %s\nDimension: %s\nServer tick: %s");
        add("gtna.eoh.operation.progress", "Progress: %s / %s ticks");
        add("gtna.eoh.operation.rebind_busy", "Finish the pending operation before changing the network owner.");
        add("gtna.eoh.operation.state.planet", "Insert a Planet Block with a planetary program.");
        add("gtna.eoh.operation.state.owner", "Bind a network owner with a Data Stick.");
        add("gtna.eoh.operation.state.gas", "Insufficient hydrogen or helium for this planet.");
        add("gtna.eoh.operation.state.compression",
                "This planet needs a higher Spacetime Compression Field tier.");
        add("gtna.eoh.operation.state.catalog", "No supported planetary resource catalog.");
        add("gtna.eoh.operation.state.energy", "Insufficient accessible Nexus energy.");
        add("gtna.eoh.operation.state.running", "Planetary operation running.");
        add("gtna.eoh.operation.state.outputs", "Waiting for product space or Nexus capacity.");
        add("gtna.eoh.operation.state.ready", "Ready for another operation.");
        add("gtna.eoh.astral_array",
                "Astral Array Fabricator: a physical upgrade for the future planetary parallel system.");
        add("gtna.source.tst", "Twist Space Technology (TST)");
        add("gtna.source.gtl", "GregTech Leisure (GTL)");
        add("gtna.source.gtlcore", "GTLCore");
        add("gtna.source.gtlsupb", "GTLsupb");
        add("gtna.source.gtoepp", "GTO Extended Platform Presets");
        add("gtna.source.gtladditions", "GTLAdditions");
        add("block.gtna.wireless_energy_network_input_terminal", "Nexus Wireless Network Input Terminal");
        add("block.gtna.wireless_energy_network_output_terminal", "Nexus Wireless Network Output Terminal");
        add("gtna.nexus.capacity", "§7Max Capacity: §e%s EU");
        add("gtna.nexus.transfer", "§7Transfer Limit: §6%s EU/t");
        add("gtna.nexus.energy", "§7Energy: §f%s / %s EU");
        add("gtna.nexus.unlimited", "§dUnlimited storage and network transfer: 750 MAX capacitors");
        add("gtna.network_terminal.input", "Supplies recipe energy directly from the bound Nexus network.");
        add("gtna.network_terminal.output", "Sends generated recipe energy directly to the bound Nexus network.");
        add("gtna.network_terminal.limit",
                "Up to Long.MAX_VALUE EU per operation; respects matrix capacity, dimension and loss. No cable IO.");
        add("gtna.network_terminal.binding",
                "Binds to placer. Data Stick: right-click to bind, left-click to unbind. Supports Nexus Linker.");
        add("gtna.network_terminal.bound", "Nexus network bound to %s");
        add("gtna.network_terminal.unbound", "Nexus network unbound");

        // --- Multiple-recipes machine UI (previously hardcoded literals) ---
        add("gtna.machine.modules_amount", "Formed modules: %s / %s");
        add("gtna.machine.structure_check", "Update structure check");
        add("gtna.machine.structure_check.up_to_date", "Structure formed");
        add("gtna.machine.structure_check.shift", "Shift+click to force a full structure rebuild");
        add("gtna.machine.structure_check.formed", "Structure formed. Auxiliary modules: %s / %s.");
        add("gtna.machine.structure_check.missing", "Structure incomplete at %s: found %s; expected %s.");
        add("gtna.machine.structure_check.module_missing",
                "Structure formed; the machine works. Optional module incomplete at %s: found %s; expected %s.");
        add("gtna.machine.structure_check.generic", "Structure incomplete: %s");
        add("gtna.machine.structure_check.rejected", "Auxiliary module rejected: duplicate performance hatch.");
        add("gtna.machine.structure_check.expected", "a valid structure block");
        add("gtna.machine.auxiliary_module", "- Auxiliary Module: ✔");
        add("gtna.machine.auxiliary_module.description",
                "  Allows the expansion of structures to improve machine efficiency.");
        add("gtna.machine.auxiliary_module.hatches",
                "  Expansion structures can install additional hatches to bring additional bonuses.");
        add("gtna.machine.auxiliary_module.unlocked",
                "Hatch types unlocked by installing auxiliary modules : %s");
        add("gtna.machine.auxiliary_module.recipe_types",
                "Recipe types unlocked by installing auxiliary modules : %s");
        add("gtna.machine.auxiliary_module.hatch.accelerate", "Accelerate Hatch");
        add("gtna.machine.auxiliary_module.hatch.extra_energy", "Extra Energy Hatch");
        add("gtna.machine.auxiliary_module.hatch.parallel", "Parallel Hatch");
        add("gtna.machine.auxiliary_module.hatch.laser", "Laser Hatch");
        add("gtna.machine.auxiliary_module.kubejs.generic",
                "Expands the structure with abilities defined by the server script.");
        add("gtna.machine.auxiliary_module.kubejs.item_import", "Unlocks an additional Item Import Bus.");
        add("gtna.multiblock.max_eut", "Max EU/t: %s (%s)");
        add("gtna.multiblock.parallels", "Parallels: %s");
        add("gtna.multiblock.pattern.error.glass", "All glass must be the same tier");
        add("gtna.multiblock.large_incubator.glass_tier", "Glass tier: %s");
        add("gtna.multiblock.large_incubator.filter_tier", "Filter tier: %s");
        add("gtna.multiblock.overclock_hatch", "Overclock Hatch: %s");
        add("gtna.multiblock.overclock_hatch.value", "%.2fx duration per 4x EU");
        add("gtna.multiblock.accelerate_hatch", "Accelerate Hatch: %s");
        add("gtna.multiblock.accelerate_hatch.value", "%.2fx Duration");
        add("gtna.multiblock.output_boost_hatch", "Output Boost Hatch: %s");
        add("gtna.multiblock.output_boost_hatch.value", "%dx Outputs");
        add("gtna.multiblock.active_threads", "Active Threads: %s");
        add("gtna.multiblock.idle", "Idle - Waiting for inputs...");
        add("gtna.multiblock.thread_line", "Thread %s: %s%s");
        add("gtna.multiblock.output_line", " -> %s x%s%s");
        add("gtna.multiblock.unknown", "Unknown");
        add("gtna.multiblock.steam.high_pressure",
                "High pressure mode active: 2x processing speed, 2x steam consumption");
        add("gtna.tooltip.steam.high_pressure",
                "High pressure mode doubles processing speed and steam consumption");

        add("material.gtna.aluminium_bronze", "Aluminium Bronze");
        add("material.gtna.eglin_steel", "Eglin Steel");
        add("material.gtna.end_steel", "EndSteel");
        add("material.gtna.indalloy_140", "Indalloy 140");
        add("material.gtna.trinaquadalloy", "Trinaquadalloy");
        add("material.gtna.mar_m_200_steel", "Mar-M200 Steel");
        add("material.gtna.fall_king", "FallKing");
        add("material.gtna.cobalt_oxide", "Cobalt Oxide");
        add("material.gtna.lithium_oxide", "Lithium Oxide");
        add("material.gtna.zirconium_oxide", "Zirconium Oxide");
        add("material.gtna.zirconia_ceramic", "Zirconia Ceramic");
        add("material.gtna.boron_carbide", "Boron Carbide");
        add("material.gtna.boron_carbide_ceramics", "Boron Carbide Ceramics");
        add("material.gtna.draconium", "Draconium");
        add("material.gtna.awakened_draconium", "Awakened Draconium");
        add("material.gtna.cosmic_neutronium", "Cosmic Neutronium");
        add("material.gtna.exo_halkonite", "Exo-Halkonite");
        add("material.gtna.chaos_matter", "Chaos Matter");
        add("material.gtna.axonium", "Axonium");
        // --- Hatches Translations (UPDATED) ---

        // Accelerate Hatch
        add("gtna.machine.accelerate_hatch.main_function",
                "§6Main Function:§r §7Reduces recipe duration on top of the normal overclock.");
        add("gtna.machine.accelerate_hatch.range",
                "§7Default duration: §b%s§7 of the original. §eAdjust it in the hatch UI§7, up to 100%% (no effect).");
        add("gtna.machine.accelerate_hatch.weakness",
                "§cPenalty:§r §7+20%% duration per tier the recipe is above this hatch. A low-tier recipe in a high-tier machine is not penalized.");
        add("gtna.machine.accelerate_hatch.compat",
                "§7Works in any electric multiblock that accepts the hatch (GTCEu and GTNA).");

        // Thread Hatch
        add("gtna.machine.thread_hatch.tooltip",
                "§6Main Function:§r §7Provides §b+%s§7 threads so the machine can process different recipes at the same time.");
        add("gtna.machine.thread_hatch.range", "§7Adjustable in the hatch UI: §b0..%s§7.");
        add("gtna.machine.thread_hatch.requires",
                "§7Requires a machine on the multiple-recipes base (currently the Duration Tester and KubeJS machines).");

        // Overclock Hatch
        add("gtna.machine.overclock_hatch.main_function",
                "§6Main Function:§r §7Improves the machine's overclock curve.");
        add("gtna.machine.overclock_hatch.not_installed",
                "§7Without this hatch, every 4x EU/t overclock uses the standard §b50%%§7 duration factor.");
        add("gtna.machine.overclock_hatch.installed",
                "§7With this hatch, every 4x EU/t overclock reduces duration to §b%s%%§7 (duration divisor §b%s§7). Adjust the divisor in the hatch UI; §b2§7 = standard overclock.");
        add("gtna.machine.overclock_hatch.desc",
                "§7Changes the overclock scaling itself; it is not a final duration multiplier like the Accelerate Hatch.");
        add("gtna.machine.overclock_hatch.note",
                "§8Note: at UV the divisor equals the standard overclock, so a UV hatch gives no gain - the gain starts at UHV.");
        add("gtna.machine.overclock_hatch.divisor", "Divisor of duration");
        add("gtna.machine.output_boost_hatch.main_function",
                "§6Main Function:§r §7Multiplies only recipe outputs for compatible multiblocks.");
        add("gtna.machine.output_boost_hatch.multiplier", "§7Output Multiplier: §a%sx§7 items and fluids.");
        add("gtna.machine.infinite_input_bus.tooltip",
                "§6Main Function:§r §7Compatible multiblocks can read item inputs from this bus without consuming them.");
        add("gtna.machine.infinite_input_hatch.tooltip",
                "§6Main Function:§r §7Compatible multiblocks can read fluid inputs from this hatch without consuming them.");
        add("gtna.machine.output_boost_bus.tooltip",
                "§6Main Function:§r §7Compatible multiblocks multiply item outputs by §a%sx§7 while this bus is installed.");
        add("gtna.machine.infinite_steam_input_bus.tooltip",
                "§6Main Function:§r §7Steam multiblocks can read item inputs from this bus without consuming them.");
        add("gtna.machine.output_boost_steam_output_bus.boost",
                "§6Main Function:§r §7Steam multiblocks multiply item outputs by §a%sx§7 while this bus is installed.");
        // Universal Factory (GTLsupb port)
        add("block.gtna.universal_factory_casing", "Universal Factory Casing");
        add("block.gtna.universal_factory", "Universal Factory");
        // Large steam casings (GTNL port; textures from Modernity-GTNH)
        add("block.gtna.industrial_steam_casing", "Industrial Steam Casing");
        add("block.gtna.advanced_industrial_steam_casing", "Advanced Industrial Steam Casing");
        add("gtna.machine.universal_factory.budget",
                "Operation budget: %s | Threads: %s | Parallel/thread: %s | Total: %s");
        add("gtna.machine.universal_factory.thermal_status", "Thermal status: %s / %s (warmup %sx)");
        add("gtna.machine.universal_factory.overload_active", "OVERLOAD ACTIVE - maximum warmup");
        add("gtna.machine.universal_factory.dynamic_threads", "Dynamic threads: %s");
        add("gtna.machine.batch_multiplier", "Batch multiplier: %s");

        // Integrated Ore Processors (GTLCore port, LGPLv3)
        add("block.gtna.integrated_ore_processor", "Integrated Ore Processor");
        add("block.gtna.advanced_integrated_ore_processor", "Advanced Integrated Ore Processor");
        add("gtna.ore_processing", "Integrated Ore Processing");

        // Primitive Stone Furnace (GTLsupb port)
        add("block.gtna.primitive_stone_furnace", "Primitive Stone Furnace");

        // Brick Kiln (GTOCore port, G-0060)
        add("block.gtna.brick_kiln", "Brick Kiln");
        add("gtna.brick_furnace", "Brick Firing");

        // Thermal Power Pump (GTOCore port, G-0062)
        add("block.gtna.thermal_power_pump", "Thermal Power Pump");
        add("gtna.machine.thermal_power_pump.production", "Water production: %s mB/t");
        add("gtna.machine.thermal_power_pump.rain", "Raining: +50% output");

        // Liquefaction Furnace (GTOCore port, G-0063)
        add("block.gtna.liquefaction_furnace", "Liquefaction Furnace");
        add("gtna.liquefaction_furnace", "Liquefaction");

        add("block.gtna.generator_array", "Generator Array");
        add("gtna.machine.generator_array.generators", "Installed generators: %s / 4");
        add("gtna.machine.generator_array.generator_slot", "Generators (up to 4)");
        add("gtna.machine.generator_array.wireless", "Wireless output: ");
        add("gtna.machine.generator_array.on", "[On]");
        add("gtna.machine.generator_array.off", "[Off]");
        add("block.gtna.aluminium_bronze_casing", "Aluminium Bronze Casing");
        add("block.gtna.fishing_ground", "Fishing Ground");
        add("gtna.fishing_ground", "Fishing Ground");
        add("block.gtna.stainless_evaporation_casing", "Stainless Evaporation Casing");
        add("block.gtna.evaporation_plant", "Evaporation Plant");
        add("gtna.evaporation", "Evaporation");
        add("block.gtna.greenhouse", "Greenhouse");
        add("gtna.greenhouse", "Greenhouse");
        add("gtna.machine.greenhouse.skylight", "Current illumination: %s");
        add("block.gtna.multi_functional_casing", "Multi Functional Casing");
        add("block.gtna.component_assembly_casing_lv", "LV Component Assembly Casing");
        add("block.gtna.component_assembly_casing_mv", "MV Component Assembly Casing");
        add("block.gtna.component_assembly_casing_hv", "HV Component Assembly Casing");
        add("block.gtna.component_assembly_casing_ev", "EV Component Assembly Casing");
        add("block.gtna.component_assembly_casing_iv", "IV Component Assembly Casing");
        add("block.gtna.component_assembly_casing_luv", "LuV Component Assembly Casing");
        add("block.gtna.component_assembly_casing_zpm", "ZPM Component Assembly Casing");
        add("block.gtna.component_assembly_casing_uv", "UV Component Assembly Casing");
        add("block.gtna.component_assembler", "Component Assembler");
        add("gtna.component_assembly", "Component Assembly");
        add("gtna.recipe.component_assembly.tier", "Casing Tier: %s");
        add("gtna.recipe.eu_usage", "Usage: %s EU/t");
        add("block.gtna.molecular_casing", "Molecular Casing");
        add("block.gtna.boron_carbide_ceramic_radiation_resistant_mechanical_cube",
                "Boron Carbide Radiation Resistant Casing");
        add("block.gtna.precision_processing_mechanical_casing", "Precision Processing Mechanical Casing");
        add("block.gtna.advanced_assembly_line_unit", "Advanced Assembly Line Unit");
        add("block.gtna.chemical_corrosion_resistant_pipe_casing", "Chemical Corrosion Resistant Pipe Casing");
        add("block.gtna.machine_casing_circuit_assembly_line", "Circuit Assembly Line Machine Casing");
        add("block.gtna.spacetime_assembly_line_unit", "Spacetime Assembly Line Unit");
        add("block.gtna.pressure_containment_casing", "Pressure Containment Casing");
        add("gtna.multiblock.pattern.error.component_casing_tier", "Component assembly casings must have one tier");
        add("gtna.machine.component_assembler.casing_tier", "Casing tier: %s");
        add("block.gtna.large_greenhouse", "Large Greenhouse");
        add("gtna.tree_growth_simulator", "Tree Growth Simulator");
        // GTNA recipe-type display names (GTCEu uses <namespace>.<path> as the category title).
        add("gtna.annihilate_generator", "Annihilation Generator");
        add("gtna.dehydrator", "Dehydrator");
        add("block.gtna.lv_dehydrator", "Basic Dehydrator");
        add("block.gtna.mv_dehydrator", "Advanced Dehydrator");
        add("block.gtna.hv_dehydrator", "Advanced Dehydrator II");
        add("block.gtna.ev_dehydrator", "Advanced Dehydrator III");
        add("block.gtna.iv_dehydrator", "Elite Dehydrator");
        add("block.gtna.luv_dehydrator", "Elite Dehydrator II");
        add("block.gtna.zpm_dehydrator", "Elite Dehydrator III");
        add("block.gtna.uv_dehydrator", "Ultimate Dehydrator");
        add("block.gtna.uhv_dehydrator", "Epic Dehydrator");
        add("block.gtna.uev_dehydrator", "Epic Dehydrator II");
        add("block.gtna.uiv_dehydrator", "Epic Dehydrator III");
        add("block.gtna.uxv_dehydrator", "Epic Dehydrator IV");
        add("block.gtna.opv_dehydrator", "Legendary Dehydrator");
        add("gtna.flotating_beneficiation", "Flotating Beneficiation");
        add("gtna.isa_mill", "ISA Mill");
        add("gtna.rocket_engine", "Rocket Engine");
        add("gtna.machine.auxiliary_module.kubejs.performance", "2x speed and perfect overclock when formed");
        add("block.gtna.ev_rocket_engine", "Advanced Rocket Engine III");
        add("block.gtna.iv_rocket_engine", "Elite Rocket Engine");
        add("block.gtna.luv_rocket_engine", "Elite Rocket Engine II");
        add("gtna.supercritical_steam_turbine", "Supercritical Steam Turbine");
        add("gtna.vacuum_drying", "Vacuum Drying");
        add("gtna.precision_laser_engraver", "Precision Laser Engraving");
        add("block.gtna.blaze_casing", "Blaze Casing");
        add("block.gtna.blaze_blast_furnace", "Blaze Blast Furnace");
        add("block.gtna.cold_ice_casing", "Cold Ice Casing");
        add("block.gtna.cold_ice_freezer", "Cold Ice Freezer");
        add("block.gtna.chemical_plant", "Chemical Plant");
        add("gtna.machine.chemical_plant.eut_multiplier", "§7EU multiplier: §b%s");
        add("gtna.machine.chemical_plant.duration_multiplier", "§7Duration multiplier: §b%s");
        add("block.gtna.mega_alloy_blast_smelter", "Mega Alloy Blast Smelter");
        add("gtna.recipe.grindball", "§7Grinding Ball Material: §b%s");
        add("block.gtna.inconel_625_casing", "Inconel-625 Casing");
        add("block.gtna.inconel_625_gearbox", "Inconel-625 Gearbox");
        add("block.gtna.inconel_625_pipe", "Inconel-625 Pipe");
        add("block.gtna.iridium_casing", "Iridium Casing");
        add("block.gtna.isa_mill", "ISA Mill");
        add("block.gtna.grind_ball_hatch", "Grinding Ball Hatch");
        add("gtna.machine.grind_ball_hatch.tooltip",
                "§6Main Function:§r §7Holds one grinding ball for the ISA Mill.");
        add("gtna.machine.grind_ball_hatch.tooltip.0",
                "§7Accepts Soapstone (tier 1) and Aluminium (tier 2) grinding balls.");
        add("gtna.machine.grind_ball_hatch.tooltip.1",
                "§7Touching the hatch while the mill is running hurts.");
        add("item.gtna.grindball_soapstone", "Soapstone Grinding Ball");
        add("item.gtna.grindball_aluminium", "Aluminium Grinding Ball");
        add("block.gtna.rocket_large_turbine", "Rocket Large Turbine");
        add("gtna.machine.rocket_large_turbine.estimated_output", "§7Estimated Max Output: §b%s EU/t");
        add("gtna.machine.rocket_large_turbine.high_speed_mode", "High-Speed Mode");
        add("gtna.machine.rocket_large_turbine.high_speed_enabled", " [§aEnabled§r]");
        add("gtna.machine.rocket_large_turbine.high_speed_disabled", " [§cDisabled§r]");
        add("gtna.machine.rocket_large_turbine.module_bonus",
                "§7Rocket engine module: §f2x output§7, §f+20% efficiency§7, §f2x rotor damage multiplier§7 and up to three extra Energy Output Hatches.");
        add("block.gtna.supercritical_turbine_casing", "Supercritical Turbine Casing");
        add("block.gtna.supercritical_steam_turbine", "Supercritical Steam Turbine");
        add("gtna.machine.supercritical_steam_turbine.estimated_output", "§7Estimated Max Output: §b%s EU/t");
        add("gtna.machine.supercritical_steam_turbine.high_speed_mode", "High-Speed Mode");
        add("gtna.machine.supercritical_steam_turbine.high_speed_enabled", " [§aEnabled§r]");
        add("gtna.machine.supercritical_steam_turbine.high_speed_disabled", " [§cDisabled§r]");
        add("gtna.machine.supercritical_steam_turbine.module_bonus",
                "§7Supercritical module: §f2x output§7, §f+20% efficiency§7, §f2x rotor damage multiplier§7 and up to three extra Energy Output Hatches.");
        add("block.gtna.hastelloy_n_75_casing", "Hastelloy N 75 Casing");
        add("block.gtna.hastelloy_n_75_gearbox", "Hastelloy N 75 Gearbox");
        add("block.gtna.hastelloy_n_75_pipe", "Hastelloy N 75 Pipe");
        add("block.gtna.flotation_cell", "Flotation Cell");
        add("block.gtna.industrial_flotation_cell", "Industrial Flotation Cell");
        add("block.gtna.red_steel_casing", "Red Steel Casing");
        add("block.gtna.three_proof_computer_casing", "Three-Proof Computer Casing");
        add("block.gtna.machining_control_casing_mk2", "Machining Control Casing MK II");
        add("block.gtna.energy_control_casing_mk2", "Energy Control Casing MK II");
        add("block.gtna.electric_power_transmission_casing", "Electric Power Transmission Casing");
        add("block.gtna.titanium_nitride_ceramic_impact_resistant_mechanical_block",
                "Titanium Nitride Ceramic Impact-Resistant Mechanical Block");
        add("block.gtna.component_assembly_line_casing_lv", "LV Component Assembly Line Casing");
        add("block.gtna.component_assembly_line_casing_mv", "MV Component Assembly Line Casing");
        add("block.gtna.component_assembly_line_casing_hv", "HV Component Assembly Line Casing");
        add("block.gtna.component_assembly_line_casing_ev", "EV Component Assembly Line Casing");
        add("block.gtna.component_assembly_line_casing_iv", "IV Component Assembly Line Casing");
        add("block.gtna.component_assembly_line_casing_luv", "LuV Component Assembly Line Casing");
        add("block.gtna.component_assembly_line_casing_zpm", "ZPM Component Assembly Line Casing");
        add("block.gtna.component_assembly_line_casing_uv", "UV Component Assembly Line Casing");
        add("block.gtna.component_assembly_line", "Component Assembly Line");
        add("gtna.machine.component_assembly_line.casing_tier", "Casing tier: %s");
        add("block.gtna.vacuum_drying_furnace", "Vacuum Drying Furnace");
        add("gtna.multiblock.pattern.rotor_clearance", "§6Requires an exclusive 5x5 space§r");
        add("material.gtna.raw_brine", "Raw Brine");
        add("material.gtna.hot_brine", "Hot Brine");
        add("material.gtna.hot_chlorinated_brominated_brine", "Hot Chlorinated Brominated Brine");
        add("material.gtna.hot_debrominated_brine", "Hot Debrominated Brine");
        add("material.gtna.hot_alkaline_debrominated_brine", "Hot Alkaline Debrominated Brine");
        add("material.gtna.debrominated_brine", "Debrominated Brine");
        add("material.gtna.brominated_chlorine_vapor", "Brominated Chlorine Vapor");
        add("material.gtna.acidic_bromine_solution", "Acidic Bromine Solution");
        add("material.gtna.concentrated_bromine_solution", "Concentrated Bromine Solution");
        add("material.gtna.acidic_bromine_exhaust", "Acidic Bromine Exhaust");
        add("material.gtna.hydrogen_iodide", "Hydrogen Iodide");

        add("block.gtna.industrial_platform_deployment_tools", "Industrial Platform Deployment Tools");
        add("gtna.machine.industrial_platform_deployment_tools.tooltip.0",
                "§6Main Function:§r §7Deploys prefabricated platform and factory presets directly into the world.");
        add("gtna.machine.industrial_platform_deployment_tools.tooltip.1",
                "§7Consumes hydraulic deployment materials from its internal inventory.");

        // Parallel Hatch
        add("block.gtna.parallel_hatch_uhv", "UHV Parallel Control Hatch");
        add("block.gtna.parallel_hatch_uev", "UEV Parallel Control Hatch");
        add("block.gtna.parallel_hatch_uiv", "UIV Parallel Control Hatch");
        add("block.gtna.parallel_hatch_uxv", "UXV Parallel Control Hatch");
        add("block.gtna.parallel_hatch_opv", "OpV Parallel Control Hatch");
        add("gtna.machine.parallel_hatch.tooltip", "Enables huge parallel processing for multiblocks");
        add("gtna.machine.parallel_hatch.tier", "Max Parallel: %s");
        add("block.gtna.me_mini_pattern_buffer", "ME Mini Pattern Buffer");
        add("block.gtna.me_pattern_buffer", "ME Pattern Buffer");
        add("block.gtna.me_advanced_pattern_buffer", "ME Advanced Pattern Buffer");
        add("block.gtna.me_ultimate_pattern_buffer", "ME Ultimate Pattern Buffer");
        add("block.gtna.me_pattern_buffer_proxy", "ME Pattern Buffer Proxy");
        add("block.gtna.me_craft_pattern_hatch", "Nexus Craft Pattern Hatch");
        add("block.gtna.crafting_cpu_interface", "Crafting CPU Interface");
        add("block.gtna.nexus_me_hypercore", "Nexus ME Hypercore");
        add("item.gtna.infinite_cell_component", "Infinite Cell Component");
        add("item.gtna.cell_component_1m", "1M Cell Component");
        add("item.gtna.cell_component_4m", "4M Cell Component");
        add("item.gtna.cell_component_16m", "16M Cell Component");
        add("item.gtna.cell_component_64m", "64M Cell Component");
        add("item.gtna.cell_component_256m", "256M Cell Component");
        add("item.gtna.pattern_buffer_copy_card", "Pattern Buffer Copy Card");
        add("item.gtna.pattern_buffer_cut_card", "Pattern Buffer Cut Card");
        add("item.gtna.standard_industrial_components_small", "Standard Industrial Components (Small)");
        add("item.gtna.standard_industrial_components_medium", "Standard Industrial Components (Medium)");
        add("item.gtna.standard_industrial_components_large", "Standard Industrial Components (Large)");
        add("item.gtna.extended_industrial_components_small", "Extended Industrial Components (Small)");
        add("item.gtna.extended_industrial_components_medium", "Extended Industrial Components (Medium)");
        add("item.gtna.extended_industrial_components_large", "Extended Industrial Components (Large)");
        add("item.gtna.special_industrial_components_small", "Special Industrial Components (Small)");
        add("item.gtna.special_industrial_components_medium", "Special Industrial Components (Medium)");
        add("item.gtna.special_industrial_components_large", "Special Industrial Components (Large)");
        add("gtna.block.me_storage_core.capacity", "Capacity: %s");
        add("gtna.ae2.cpu.nexus_hypercore", "N-ME CPU");
        add("gui.gtna.craft_confirm.nexus_planner", "Nexus Planner · %s");
        add("gtna.machine.nexus_me_hypercore.ui.title", "Nexus ME Hypercore");
        add("gtna.machine.nexus_me_hypercore.ui.tier", "Tier: ");
        add("gtna.machine.nexus_me_hypercore.ui.modules", "Installed Modules: ");
        add("gtna.machine.nexus_me_hypercore.ui.storage", "Storage: ");
        add("gtna.machine.nexus_me_hypercore.ui.coprocessors", "Co-Processors: ");
        add("gtna.machine.nexus_me_hypercore.ui.threads", "Threads: ");
        add("gtna.machine.nexus_me_hypercore.ui.cpus", "Shared CPU: %s (%s active jobs)");
        add("gtna.machine.nexus_me_hypercore.ui.transcendent", "Transcendent Mode: ");
        add("gtna.machine.nexus_me_hypercore.ui.on", "Active");
        add("gtna.machine.nexus_me_hypercore.ui.off", "Inactive");
        add("gtna.machine.pattern_buffer.tooltip", "AE2 pattern buffer with per-slot GTNA specialization");
        add("gtna.machine.pattern_buffer.slots", "Pattern Slots: %s");
        add("gtna.machine.pattern_buffer.break_persist", "Stored patterns and slot data are preserved on block drop");
        add("gtna.machine.pattern_buffer.specialization_pending",
                "Middle-click a pattern slot to edit item, fluid, circuit, and mode specialization");
        add("gtna.machine.pattern_buffer.middle_click_hint", "Middle-click to configure this pattern slot");
        add("gtna.machine.pattern_buffer.selected_slot", "Editing Slot %s");
        add("gtna.machine.pattern_buffer.no_slot_selected", "No slot selected");
        add("gtna.machine.pattern_buffer.cached_recipe_short", "Recipe: %s");
        add("gtna.machine.pattern_buffer.derived_mode_short", "Mode: %s");
        add("gtna.machine.pattern_buffer.select_slot_hint", "Select a pattern slot");
        add("gtna.machine.pattern_buffer.item_field", "Ghost Items");
        add("gtna.machine.pattern_buffer.item_count_field", "Special Item Count");
        add("gtna.machine.pattern_buffer.fluid_field", "Ghost Fluids");
        add("gtna.machine.pattern_buffer.fluid_amount_field", "Special Fluid Amount (mB)");
        add("gtna.machine.pattern_buffer.fluid_amount_hint", "Drag a fluid here. Right-click clears the slot.");
        add("gtna.machine.pattern_buffer.circuit_field", "Circuit");
        add("gtna.machine.pattern_buffer.mode_field", "Preferred Mode");
        add("gtna.machine.pattern_buffer.mode.auto", "Auto");
        add("gtna.machine.pattern_buffer.mode.none", "No Mode");
        add("gtna.machine.pattern_buffer.mode.legacy", "Custom: %s");
        add("gtna.machine.pattern_buffer.mode.all", "All Modes");
        add("gtna.machine.pattern_buffer.buffer_mode.tooltip",
                "Limits this buffer to a single recipe type");
        add("gtna.machine.pattern_buffer.mode_button.tooltip",
                "Click to cycle the preferred multiblock mode for this slot");
        add("gtna.machine.pattern_buffer.mode_button.current", "Selected Mode: %s");
        add("gtna.machine.pattern_buffer.mode_button.derived", "Detected Mode: %s");
        add("gtna.machine.pattern_buffer.no_circuit", "No configured circuit");
        add("gtna.machine.pattern_buffer.previous_page", "Previous pattern page");
        add("gtna.machine.pattern_buffer.next_page", "Next pattern page");
        add("gtna.machine.pattern_buffer.back", "Back to patterns");
        add("gtna.machine.pattern_buffer.clear_machine_recipe_cache", "Clear Machine Recipe Cache");
        add("gtna.machine.pattern_buffer.clear_machine_recipe_cache.tooltip",
                "Clear all recipe lookup caches in this buffer without changing encoded patterns");
        add("gtna.machine.pattern_buffer.clear_pattern_recipe_cache", "Clear Recipe in Pattern");
        add("gtna.machine.pattern_buffer.clear_pattern_recipe_cache.tooltip",
                "Clear the recipe recorded in this pattern without changing its inputs or outputs");
        add("gtna.machine.pattern_buffer.embedded_circuit", "Embedded Circuit (all patterns)");
        add("gtna.machine.pattern_buffer.embed_circuit", "Embed Circuit");
        add("gtna.machine.pattern_buffer.remove_circuits", "Remove Circuits");
        add("gtna.machine.pattern_buffer.skip_existing.on", "Skip Existing: ON");
        add("gtna.machine.pattern_buffer.skip_existing.off", "Skip Existing: OFF");
        add("gtna.machine.pattern_buffer.skip_existing.tooltip",
                "ON keeps patterns that already carry a circuit untouched when embedding");
        add("gtna.machine.pattern_buffer.cache_section", "Recipe Cache");
        add("gtna.machine.pattern_buffer.tools", "Buffer Tools");
        add("gtna.machine.pattern_buffer.tools.tooltip",
                "Recipe cache maintenance and encoded-pattern circuit tooling for the whole buffer");
        add("item.gtna.pattern_buffer_copy.tooltip.snapshot",
                "Sneak-right-click a Pattern Buffer to snapshot its configuration");
        add("item.gtna.pattern_buffer_copy.tooltip.apply",
                "Right-click another Pattern Buffer to paste the configuration");
        add("item.gtna.pattern_buffer_cut.tooltip.snapshot",
                "Sneak-right-click a Pattern Buffer to cut its configuration out");
        add("item.gtna.pattern_buffer_cut.tooltip.apply",
                "Right-click another Pattern Buffer to paste the configuration");
        add("gtna.machine.pattern_buffer.copy.copied", "Pattern buffer configuration copied");
        add("gtna.machine.pattern_buffer.copy.cut", "Pattern buffer configuration cut");
        add("gtna.machine.pattern_buffer.copy.empty", "No buffer configuration stored on this card");
        add("gtna.machine.pattern_buffer.copy.pasted", "Pasted %s of %s pattern(s) into the buffer");
        add("gtna.jade.pattern_buffer.proxies", "Bound Proxies: %s");
        add("gtna.machine.pattern_buffer.recipe_cached", "Recipe cached for this slot");
        add("gtna.machine.pattern_buffer.cache_toggle.on", "Recipe Cache: ON (click to disable)");
        add("gtna.machine.pattern_buffer.cache_toggle.off", "Recipe Cache: OFF (click to enable)");
        add("gtna.machine.pattern_buffer.cache_toggle.tooltip",
                "Caching remembers the resolved recipe per slot; disable to always resolve fresh");
        add("gtna.machine.pattern_buffer.keep_byproduct", "Keep Byproducts: ");
        add("gtna.machine.pattern_buffer.toggle_yes", "ON");
        add("gtna.machine.pattern_buffer.toggle_no", "OFF");
        add("gtna.machine.pattern_buffer.proxy", "ME Pattern Buffer Proxy");
        add("gtna.machine.pattern_buffer.proxy.tooltip",
                "Lets another multiblock use the patterns stored in a distant ME Pattern Buffer");
        add("gtna.machine.pattern_buffer.proxy.binding",
                "Bind: Shift-right-click the buffer with a Data Stick, then right-click this part");
        add("gtna.machine.pattern_buffer.proxy.range_note",
                "Same dimension only; the buffer chunk must be loaded");
        add("gtna.machine.pattern_buffer.proxy_bound", "Pattern Buffer bound to this proxy");
        add("gtna.machine.pattern_buffer.catalyst_item_field", "Catalyst Items (not consumed)");
        add("gtna.machine.pattern_buffer.catalyst_fluid_field", "Catalyst Fluids (not consumed)");
        add("gtna.machine.pattern_buffer.terminal_visibility", "Terminal: ");
        add("gtna.machine.pattern_buffer.terminal_hidden", "Hidden from Pattern Access Terminal");
        add("gtna.machine.pattern_buffer.terminal_visible", "Visible in Pattern Access Terminal");
        add("gtna.machine.pattern_buffer.clear_specialization", "Clear Spec");
        add("gtna.machine.pattern_buffer.clear_cache", "Clear Cache");
        add("gtna.machine.pattern_buffer.refund_slot", "Refund");
        add("gtna.machine.craft_pattern_hatch.tooltip", "Dedicated AE2 crafting hatch for the Nexus Assembly Forge");
        add("gtna.machine.craft_pattern_hatch.slots", "Pattern Slots: %s");
        add("gtna.machine.craft_pattern_hatch.patterns",
                "Accepts encoded crafting patterns only and registers them to the AE2 network");
        add("gtna.machine.craft_pattern_hatch.cheat",
                "Queues crafted outputs directly for the controller to materialize");
        add("gtna.machine.crafting_cpu_interface.tooltip",
                "Connects the Nexus ME Hypercore to the AE2 crafting CPU network");
        add("gtna.machine.crafting_cpu_interface.network",
                "The Nexus ME Hypercore structure requires exactly one interface");
        add("gtna.machine.crafting_cpu_interface.connection_only", "AE2 network connection only");
        add("item.gtna.pattern_buffer_upgrade_21", "Pattern Buffer Expansion Card");
        add("item.gtna.pattern_buffer_upgrade_32", "Pattern Buffer Precision Card");
        add("item.gtna.pattern_buffer_upgrade_72", "Pattern Buffer Ascension Card");
        add("item.gtna.infinite_steam_singleblock_cover", "Infinite Steam Singleblock Cover");
        add("item.gtna.infinite_electric_singleblock_cover", "Infinite Electric Singleblock Cover");
        add("item.gtna.pattern_buffer_upgrader.tooltip.use",
                "Right-click a lower tier GTNA Pattern Buffer to upgrade it");
        add("item.gtna.pattern_buffer_upgrader.tooltip.keep_data",
                "Preserves encoded patterns, internal slot data, and slot specialization");
        add("item.gtna.primitive_mans_spacetime_distortion_device",
                "Primitive Man's SpaceTime Distortion Device");
        add("item.gtna.primitive_mans_spacetime_distortion_device.tooltip", "Anyway...");

        // --- Wireless Energy/Dynamo Hatches ---
        add("gtna.machine.wireless_energy_hatch.tooltip", "§7Pulls energy wirelessly from the Nexus Network.");
        add("gtna.machine.wireless_energy_hatch.tier_info", "§7Tier: §e%s§7 | Amperage: §e%sA");
        add("gtna.machine.wireless_energy_hatch.bound", "§a[GTNA] §fWireless Energy Hatch bound to your network.");

        add("gtna.machine.wireless_dynamo_hatch.tooltip", "§7Pushes energy wirelessly to the Nexus Network.");
        add("gtna.machine.wireless_dynamo_hatch.tier_info", "§7Tier: §e%s§7 | Amperage: §e%sA");
        add("gtna.machine.wireless_dynamo_hatch.bound", "§a[GTNA] §fWireless Dynamo Hatch bound to your network.");

        add("gtna.machine.wireless_hatch.not_bound", "§cNot bound to any network! Place to auto-bind.");
        add("gtna.machine.wireless_hatch.capacity", "Buffer Capacity: %s EU");
        add("gtna.machine.wireless_hatch.auto_bind", "§8Place in world to auto-bind to your network");

        // Generate names for all Wireless Hatches (LV to MAX, 1A to MAX A) — colored tier names
        for (int tier = GTValues.LV; tier <= GTValues.MAX; tier++) {
            String tierName = GTValues.VN[tier].toLowerCase(Locale.ROOT);
            ChatFormatting color = (tier < TextUtil.GTI_CORE$VC.length) ? TextUtil.GTI_CORE$VC[tier] :
                    ChatFormatting.WHITE;
            String colorCode = getColorCode(color);
            String coloredTierName = colorCode + GTValues.VN[tier] + "§r";
            for (int ampExp = 0; ampExp <= 10; ampExp++) {
                int amps = (int) Math.pow(4, ampExp);
                String outName = "block.gtna.wireless_energy_hatch_" + amps + "a_" + tierName;
                String inName = "block.gtna.wireless_dynamo_hatch_" + amps + "a_" + tierName;
                add(outName, coloredTierName + " " + amps + "A Wireless Energy Hatch");
                add(inName, coloredTierName + " " + amps + "A Wireless Dynamo Hatch");
            }
        }

        // Linker
        add("gtna.message.linker.copied", "Network ID copied to linker!");
        add("gtna.message.linker.linked", "%s linked to network!");
        add("item.gtna.nexus_linker", "Nexus Linker");

        // Terminal
        add("item.gtna.quantum_network_terminal", "Quantum Network Terminal");
        add("gtna.terminal.locate.message", "§a[GTNA Terminal] §fLocated at §eX: %s Y: %s Z: %s §7(%s)");

        // Nexus Structure Terminal
        add("item.gtna.nexus_structure_terminal", "Nexus Structure Terminal");
        add("gtna.terminal.nexus.clear_all", "Clear all choices");
        add("gtna.terminal.nexus.clear_choice", "Clear this choice");
        add("gtna.terminal.nexus.select_hint",
                "Click to select; click again to clear. Applies only to compatible structure cells.");
        add("gtna.terminal.config.abs_casing", "ABS Casings");
        add("gtna.terminal.config.battery", "Capacitors");
        add("gtna.terminal.config.cleanroom", "Cleanroom Filters");
        add("gtna.terminal.config.component_assembly", "Component Assembly Casings");
        add("gtna.terminal.config.computer_casing", "Computer Casings");
        add("gtna.terminal.config.computer_heat", "Computer Heat Vents");
        add("gtna.terminal.config.glass", "Glass");
        add("gtna.terminal.config.graviton", "Graviton Casings");
        add("gtna.terminal.config.hermetic", "Hermetic Casings");
        add("gtna.terminal.config.integral_frame", "Integral Frameworks");
        add("gtna.terminal.config.light", "Lights");
        add("gtna.terminal.config.space_elevator", "Space Elevator Casings");
        add("gtna.terminal.config.stellar_containment", "Stellar Containment");
        add("gtna.terminal.config.eoh_compression", "EOH Compression Fields");
        add("gtna.terminal.config.eoh_acceleration", "EOH Time Fields");
        add("gtna.terminal.config.eoh_stabilisation", "EOH Stabilisation Fields");
        add("gtna.terminal.nexus.tiered_block", "Tiered Block");
        add("gtna.terminal.nexus.select", "Select");
        add("gtna.terminal.nexus.title", "§l§5Nexus Terminal");

        // Toggle settings
        add("gtna.terminal.nexus.no_hatch", "No Hatch Mode");
        add("gtna.terminal.nexus.no_hatch.tooltip",
                "When enabled, skips placing hatches\n(buses, energy I/O, etc.) during auto-build.");
        add("gtna.terminal.nexus.no_hatch.hint", "§7Bypass hatch placement");

        add("gtna.terminal.nexus.replace_mode", "Replace Mode");
        add("gtna.terminal.nexus.replace_mode.tooltip",
                "When enabled, replaces existing tier blocks\n(e.g. coils) with the configured selection.");
        add("gtna.terminal.nexus.replace_mode.hint", "§7Swap existing blocks with configured tier");

        add("gtna.terminal.nexus.demolition_mode", "Demolition Mode");
        add("gtna.terminal.nexus.demolition_mode.tooltip",
                "When enabled, clears blocks in cells that\nrequire air; ignored cells are preserved.");
        add("gtna.terminal.nexus.demolition_mode.hint", "§7Clear blocks in required air cells");

        add("gtna.terminal.nexus.use_ae", "Use AE Items");
        add("gtna.terminal.nexus.use_ae.tooltip",
                "When enabled, extracts required blocks from\nyour AE2 network via Wireless Terminal.");
        add("gtna.terminal.nexus.use_ae.hint", "§7Pull materials from ME network");

        add("gtna.terminal.nexus.mirror_build", "Mirror Build");
        add("gtna.terminal.nexus.mirror_build.tooltip",
                "When enabled, builds the structure in\nmirrored orientation.");
        add("gtna.terminal.nexus.mirror_build.hint", "§7Build mirrored structure");

        // Numeric settings
        add("gtna.terminal.nexus.repetitions", "Repetitions");
        add("gtna.terminal.nexus.repetitions.tooltip",
                "Number of structure layer repetitions (0-1000).\nUsed for expandable multiblocks like Distillation Tower.");
        add("gtna.terminal.nexus.repetitions.hint", "§7Scroll wheel or type (0-1000)");

        add("gtna.terminal.nexus.module_build", "Module Build");
        add("gtna.terminal.nexus.module_build.tooltip",
                "Module build count (0-100).\nSets how many module layers to construct.");
        add("gtna.terminal.nexus.module_build.hint", "§7Scroll wheel or type (0-100)");

        // Nexus Structure Terminal Tooltips
        add("item.gtna.nexus_structure_terminal.tooltip.use", "§dRight Click§7: Open Settings");
        add("item.gtna.nexus_structure_terminal.tooltip.shift_use",
                "§dShift + Right Click§7 on Controller: Build Structure");
        add("item.gtna.nexus_structure_terminal.tooltip.replace_mode_active", "§5⚠ Replace Mode Active");
        add("item.gtna.nexus_structure_terminal.tooltip.config", "Open block selection configuration");

        // Block Config tab — category labels with purple accent
        add("gtna.terminal.config.title", "Block Configuration");
        add("gtna.terminal.config.coils", "§dCoils");
        add("gtna.terminal.config.machine_casing", "§dMachine Casings");
        add("gtna.terminal.config.muffler", "§dMuffler Hatches");
        add("gtna.terminal.config.rotor_holder", "§dRotor Holders");
        add("gtna.terminal.config.wireless_capacitor", "§dWireless Capacitors");
        add("gtna.terminal.config.matrix_storage_module", "§dMatrix Storage Modules");
        add("gtna.terminal.config.matrix_crafting_module", "§dMatrix Crafting Modules");
        add("gtna.terminal.config.me_storage_access", "§dME Storage Access");

        // AE2 Network linking
        add("gtna.terminal.nexus.ae2.linked", "§a[GTNA] §fLinked to ME Wireless Access Point!");
        add("gtna.terminal.nexus.ae2.tooltip.linked", "§a⚡ ME Network linked at [%s, %s, %s]");
        add("gtna.terminal.nexus.ae2.tooltip.not_linked", "§c✖ ME Network: Not connected");
        add("gtna.terminal.nexus.ae2.tooltip.how_to_link", "§8Right-click a Wireless Access Point to link");
        add("gtna.terminal.nexus.ae2.tooltip.in_range", "§a✔ Wireless: In Range");
        add("gtna.terminal.nexus.ae2.tooltip.out_of_range", "§c✖ Wireless: Out of Range");

        // Nexus Flux Matrix
        add("block.gtna.nexus_flux_matrix", "Nexus Flux Matrix");

        // Capacitor blocks — colored tier names
        String[] capacitorTierNames = { "lv", "mv", "hv", "ev", "iv", "luv", "zpm", "uv", "uhv", "uev", "uiv", "uxv",
                "opv", "max" };
        for (int ci = 0; ci < capacitorTierNames.length; ci++) {
            int capTier = ci + GTValues.LV; // LV=1, MV=2, ...
            ChatFormatting capColor = (capTier < TextUtil.GTI_CORE$VC.length) ? TextUtil.GTI_CORE$VC[capTier] :
                    ChatFormatting.WHITE;
            String capColorCode = getColorCode(capColor);
            String coloredCapTierName = capColorCode + GTValues.VN[capTier] + "§r";
            add("block.gtna.nexus_capacitor_" + capacitorTierNames[ci], coloredCapTierName + " Nexus Capacitor");
        }

        // --- Other Machines & Items ---
        add("block.gtna.wireless_steam_input_hatch", "Wireless Steam Input Hatch");
        add("block.gtna.wireless_steam_input_hatch_steel", "Wireless Steam Input Hatch Steel");
        add("block.gtna.wireless_steam_output_hatch", "Wireless Steam Output Hatch");
        add("block.gtna.wireless_steam_output_hatch_steel", "Wireless Steam Output Hatch Steel");
        add("item.gtna.structure_detect", "Structure Writer");
        add("item.gtna.debug_structure_writer", "Debug Structure Writer");
        add("item.gtna.vajra", "Vajra");
        add("item.gtna.hydraulic_motor", "Hydraulic Motor");
        add("item.gtna.hydraulic_piston", "Hydraulic Piston");
        add("item.gtna.hydraulic_pump", "Hydraulic Pump");
        add("item.gtna.hydraulic_arm", "Hydraulic Arm");
        add("item.gtna.hydraulic_conveyor", "Hydraulic Conveyor");
        add("item.gtna.hydraulic_regulator", "Hydraulic Regulator");
        add("item.gtna.hydraulic_vapor_generator", "Hydraulic Vapor Generator");
        add("item.gtna.hydraulic_steam_jet_spewer", "Hydraulic Steam Jet Spewer");
        add("item.gtna.hydraulic_steam_receiver", "Hydraulic Steam Receiver");
        add("item.gtna.annihilation_constrainer", "Annihilation Constrainer");
        add("item.gtna.neutronium_antimatter_fuel_rod", "Neutronium Antimatter Fuel Rod");
        add("item.gtna.draconium_antimatter_fuel_rod", "Draconium Antimatter Fuel Rod");
        add("item.gtna.cosmic_neutronium_antimatter_fuel_rod", "Cosmic Neutronium Antimatter Fuel Rod");
        add("item.gtna.infinity_antimatter_fuel_rod", "Infinity Antimatter Fuel Rod");
        add("item.gtna.structure_detect.tooltip.0", "§aRight click§7 block to select Multiblock Controller.");
        add("item.gtna.structure_detect.tooltip.1", "§aShift Right click§7 to change mode.");
        add("item.gtna.structure_detect.tooltip.2", "§aMode: §f%s");
        add("item.gtna.structure_detect.error.0", "Required at %s:\n");
        add("item.gtna.structure_detect.error.1", "Required at %s:");
        add("item.gtna.structure_detect.error.2", "At %s %s");
        add("item.gtna.structure_detect.error.3", "(Mirrored Mode)");
        add("item.gtna.structure_detect.error.4", "(Normal Mode)");
        add("structure_detect.tooltip.0", "Right-click multiblock main block");
        add("structure_detect.tooltip.1", "Shift right-click to switch detection mode");
        add("itemGroup.gtna.creative_tab", "GregTech: Nexus Addon");
        add("itemGroup.gtna.creative_tab.machines", "GregTech: Nexus Addon Machines");
        add("itemGroup.gtna.creative_tab.items", "GregTech: Nexus Addon Items");
        add("itemGroup.gtna.creative_tab.material_blocks", "GregTech: Nexus Addon Material Blocks");
        add("itemGroup.gtna.creative_tab.material_fluids", "GregTech: Nexus Addon Material Fluids");
        add("itemGroup.gtna.creative_tab.material_items", "GregTech: Nexus Addon Material Items");
        add("itemGroup.gtna.creative_tab.material_pipes", "GregTech: Nexus Addon Material Pipes & Wires");
        add("itemGroup.gtna.creative_tab.blocks", "GregTech: Nexus Addon Blocks");
        add("itemGroup.gtna.creative_tab.wireless", "GregTech: Nexus Addon Wireless");
        add("structure_writer.export_order", "Export Order: C:%s  S:%s  A:%s");
        add("structure_writer.structural_scale", "Structure Scale: X:%s  Y:%s  Z:%s");
        add("message.gtna.detection_mode_mirrored", "Current detection mode: (Mirrored mode)");
        add("message.gtna.detection_mode_normal", "Current detection mode: (Normal mode)");
        add("message.gtnacore.structure_formed", "Structure formed");
        add("block.gtna.large_steam_crusher", "Large Steam Crusher");
        add("item.gtna.precision_steam_component", "Precision Steam Component");
        add("gtna.tooltip.large_steam_crusher.steam",
                "§7Steam Consumption: 80% of original");
        add("gtna.multiblock.parallel_amount", "Parallels: %s");
        add("block.gtna.huge_steam_input_bus", "Huge Steam Input Bus");
        add("block.gtna.huge_steam_output_bus", "Huge Steam Output Bus");
        add("block.gtna.infinite_steam_input_bus", "Infinite Steam Input Bus");
        add("block.gtna.output_boost_steam_output_bus", "Output Boost Steam Output Bus");
        add("gtna.tooltip.huge_steam_input_bus", "Huge Steam Input Bus: stores 54 slots.");
        add("gtna.tooltip.huge_steam_output_bus", "Huge Steam Output Bus: stores 54 slots.");
        add("gtna.machine.wireless_steam_hatch.tooltip", "Steam Production: %s L/t");
        add("block.gtna.breel_pipe_casing", "Breel Pipe Casing");
        add("block.gtna.hyper_pressure_breel_casing", "Hyper Pressure Breel Casing");
        add("block.gtna.steam_compact_pipe_casing", "Steam Compact Pipe Casing");
        add("block.gtna.vibration_safe_casing", "Vibration Safe Casing");
        add("block.gtna.graviton_field_constraint_casing", "Graviton Field Constraint Casing");
        add("block.gtna.annihilate_core", "Annihilate Core");
        add("block.gtna.hyper_mechanical_casing", "Hyper Mechanical Casing");
        add("block.gtna.hollow_casing", "Hollow Casing");
        add("block.gtna.naquadah_alloy_casing", "Naquadah Alloy Casing");
        add("block.gtna.dyson_control_toroid", "Dyson Control Toroid");
        add("block.gtna.dyson_control_casing", "Dyson Control Casing");
        add("block.gtna.degenerate_rhenium_constrained_casing", "Degenerate Rhenium Constrained Casing");
        add("block.gtna.dyson_receiver_casing", "Dyson Receiver Casing");
        add("block.gtna.rhenium_reinforced_energy_glass", "Rhenium Reinforced Energy Glass");
        add("block.gtna.antimatter_containment_casing", "Antimatter Containment Casing");
        add("block.gtna.dimensionally_transcendent_casing", "Dimensionally Transcendent Casing");
        add("block.gtna.dimension_injection_casing", "Dimension Injection Casing");
        add("block.gtna.bronze_reinforced_wood", "Bronze Reinforced Wood");
        add("block.gtna.steel_reinforced_wood", "Steel Reinforced Wood");
        add("block.gtna.iron_reinforced_wood", "Iron Reinforced Wood");
        add("block.gtna.solar_boiling_cell", "Solar Boiling Cell");
        add("block.gtna.oxidation_resistant_hastelloy_n_mechanical_casing",
                "Oxidation Resistant Hastelloy N Mechanical Casing");
        add("block.gtna.zirconia_ceramic_high_strength_bending_resistance_mechanical_block",
                "Zirconia Ceramic High Strength Bending Resistance Mechanical Block");
        add("block.gtna.high_strength_concrete", "High Strength Concrete");
        add("block.gtna.cobalt_oxide_ceramic_strong_thermally_conductive_mechanical_block",
                "Cobalt Oxide Ceramic Strong Thermally Conductive Mechanical Block");
        add("block.gtna.lithium_oxide_ceramic_heat_resistant_shock_resistant_mechanical_cube",
                "Lithium Oxide Ceramic Heat Resistant Shock Resistant Mechanical Cube");
        add("block.gtna.abs_black_casing", "Black ABS Plastic Mechanical Casing");
        add("block.gtna.abs_blue_casing", "Blue ABS Plastic Mechanical Casing");
        add("block.gtna.abs_brown_casing", "Brown ABS Plastic Mechanical Casing");
        add("block.gtna.abs_green_casing", "Green ABS Plastic Mechanical Casing");
        add("block.gtna.abs_grey_casing", "Gray ABS Plastic Mechanical Casing");
        add("block.gtna.abs_lime_casing", "Lime ABS Plastic Mechanical Casing");
        add("block.gtna.abs_orange_casing", "Orange ABS Plastic Mechanical Casing");
        add("block.gtna.abs_red_casing", "Red ABS Plastic Mechanical Casing");
        add("block.gtna.abs_white_casing", "White ABS Plastic Mechanical Casing");
        add("block.gtna.abs_yellow_casing", "Yellow ABS Plastic Mechanical Casing");
        add("block.gtna.abs_cyan_casing", "Cyan ABS Plastic Mechanical Casing");
        add("block.gtna.abs_magenta_casing", "Magenta ABS Plastic Mechanical Casing");
        add("block.gtna.abs_pink_casing", "Pink ABS Plastic Mechanical Casing");
        add("block.gtna.abs_purple_casing", "Purple ABS Plastic Mechanical Casing");
        add("block.gtna.abs_light_bull_casing", "Light Blue ABS Plastic Mechanical Casing");
        add("block.gtna.abs_light_grey_casing", "Light Gray ABS Plastic Mechanical Casing");
        add("block.gtna.t1_me_storage_core", "T1 Matrix Storage Module");
        add("block.gtna.t2_me_storage_core", "T2 Matrix Storage Module");
        add("block.gtna.t3_me_storage_core", "T3 Matrix Storage Module");
        add("block.gtna.t4_me_storage_core", "T4 Matrix Storage Module");
        add("block.gtna.t5_me_storage_core", "T5 Matrix Storage Module");
        add("block.gtna.t1_crafting_storage_core", "T1 Matrix Crafting Module");
        add("block.gtna.t2_crafting_storage_core", "T2 Matrix Crafting Module");
        add("block.gtna.t3_crafting_storage_core", "T3 Matrix Crafting Module");
        add("block.gtna.t4_crafting_storage_core", "T4 Matrix Crafting Module");
        add("block.gtna.t5_crafting_storage_core", "T5 Matrix Crafting Module");
        add("gtna.machine.me_storage_access_hatch.tooltip", "Connects ME Storage to an AE2 network.");
        for (var planet : com.raishxn.gtna.common.data.worldgen.GTNAPlanetOres.Planet.values()) {
            add("tagprefix." + planet.id + "_stone", planet.englishName + " %s Ore");
        }
        add("gtna.machine.restricted_part.tier_lock", "§eOnly acts on %s recipes (recipe tier before overclock).");
        add("block.gtna.coolant_pip_casing", "Coolant Pipe Casing");
        add("block.gtna.uev_hermetic_casing", "UEV Hermetic Casing");
        add("gtna.machine.advanced_fusion_reactor.module", "Extension %s: raises the tier to %s");
        add("gtna.machine.advanced_fusion_reactor.cross_recipe",
                "Cross-recipe extension: holds 1 Thread Hatch and 1 Overclock Hatch");
        add("gtna.machine.advanced_fusion_reactor.tier", "Tier: %s (%s tier extensions)");
        add("block.gtna.plasma_forge_bridge_casing", "Dimensional Bridge Casing");
        add("block.gtna.eternal_coil", "Eternal Coil Block");
        add("gtna.machine.plasma_forge.discount", "Catalyst discount: %s%% (%s h of run time)");
        add("gtna.machine.transcendent_plasma_mixer.no_energy", "Not enough wireless EU: needs %s EU");
        add("gtna.recipe.wireless_cost", "Wireless cost: %s EU");
        add("gtna.machine.nano_forge.module",
                "Extension: tier %s");
        add("gtna.machine.nano_forge.tier",
                "Nano Forge tier %s (structure %s, nanite %s)");
        add("gtna.machine.nano_forge.low_tier",
                "Needs Nano Forge tier %s");
        add("gtna.recipe.nano_forge_tier",
                "Nano Forge tier: %s");
        add("gtna.machine.me_export_buffer.tooltip",
                "Output bus and output hatch in one block: sends items and fluids straight to the ME network.");
        add("gtna.machine.debug_energy_hatch.tooltip",
                "§6Test part:§r §7always full; set its tier, voltage, amperage and on/off in the GUI, like a creative energy hatch.");
        add("gtna.machine.debug_energy_hatch.rate", "Supplying up to %s EU/t");
        add("gtna.machine.debug_input_bus.tooltip",
                "§6Test part:§r §7mark items in its 3x3 ghost slots; recipes get endless amounts and nothing is consumed.");
        add("gtna.machine.debug_input_hatch.tooltip",
                "§6Test part:§r §7mark fluids in its 3x3 ghost tanks; recipes get endless amounts and nothing is consumed.");
        add("gtna.machine.debug_laser_hatch.tooltip",
                "§6Test part:§r §7always-full laser input (4096 A by default); set its tier, voltage, amperage and on/off in the GUI.");
        add("item.gtna.debug_energy_cover.tooltip",
                "§6Test cover:§r §7keeps the energy buffer of any GregTech machine full. §cCreative only.");
        add("gtna.machine.debug_part.creative_only", "§cCreative only, for testing multiblocks. Has no recipe.");
        add("gtna.machine.me_export_buffer.capacity",
                "Internal buffer with no practical limit (up to 9.2 quintillion per item or fluid); recipes never stall on full output.");
        add("gtna.machine.me_big_storage_access_hatch.tooltip",
                "Connects ME Storage to an AE2 network with BigInteger storage mode.");
        add("gtna.machine.me_io_port_hatch.tooltip", "Connects ME Storage to an AE2 network through IO Port mode.");
        add("gtna.machine.me_storage_access_hatch.network",
                "The ME Storage multiblock accepts exactly one of these access hatches.");
        add("gtna.machine.me_storage_access_hatch.mode", "Storage Access");
        add("gtna.machine.me_big_storage_access_hatch.mode", "Big Storage Access");
        add("gtna.machine.me_io_port_hatch.mode", "IO Port");
        add("gtna.machine.me_storage.unformed", "Form the Matrix Storage structure to mount AE2 storage.");
        add("gtna.machine.me_storage.title", "ME Storage");
        add("gtna.machine.me_storage.no_access",
                "Missing ME Storage Access Hatch, ME Big Storage Access Hatch, or ME IO Port Hatch.");
        add("gtna.machine.me_storage.access", "%s: %s");
        add("gtna.machine.me_storage.capacity", "Capacity: %s");
        add("gtna.machine.me_storage.used", "Used: %s / Types: %s");
        add("gtna.machine.me_storage.infinite_status", "Infinite Cell Components: %s/64 - %s");
        add("gtna.machine.me_storage.infinite_cell_slot", "Infinite Cell Component Slot");
        add("block.gtna.naquadah_borosilicate_glass", "Naquadah Borosilicate Glass");
        add("block.gtna.magtech_casing", "Magtech Casing");
        add("block.gtna.process_machine_casing", "Process Machine Casing");
        add("block.gtna.compressor_controller_casing", "Compressor Controller Casing");
        add("block.gtna.extreme_density_casing", "Extreme Density Casing");
        add("block.gtna.steam_assembly_block", "Steam Assembly Block");
        add("block.gtna.brass_reinforced_wooden_casing", "Brass Reinforced Wooden Casing");
        add("block.gtna.solar_heat_collector_pipe_casing", "Solar Heat Collector Pipe Casing");
        add("block.gtna.annihilate_generator", "Artificial Star");
        add("block.gtna.eye_of_harmony", "Eye of Harmony");
        add("block.gtna.eye_of_wood", "Eye of Wood");
        add("block.gtna.nexus_molecular_forge", "Nexus Assembly Forge");
        add("block.gtna.me_storage", "ME Storage");
        add("gtceu.annihilate_generator", "Annihilation Generator");
        add("gtna.cosmos_simulation", "Cosmos Simulation");
        add("gtna.machine.artificial_star.output",
                "§7Supports §bLaser§7 or up to §b16 Wireless Dynamos§7. Infinity supports one Nexus Network Output Terminal or 16 MAX 1,048,576A dynamos at base speed.");
        add("gtna.machine.eye_of_harmony.owner", "Network Owner: %s");
        add("gtna.machine.eye_of_harmony.network_eu", "Stored Network EU: %s");
        add("gtna.machine.eye_of_harmony.startup_eu", "Startup Energy: %s EU");
        add("gtna.machine.eye_of_harmony.hydrogen", "Hydrogen for next cycle: %s B");
        add("gtna.machine.eye_of_harmony.helium", "Helium for next cycle: %s B");
        add("gtna.machine.eye_of_harmony.rebound", "[GTNA] Eye of Harmony rebound to your network.");
        add("gtna.machine.eye_of_wood.water", "Stored Water: %s / %s mB");
        add("gtna.machine.eye_of_wood.lava", "Stored Lava: %s / %s mB");
        add("gtna.machine.eye_of_wood.chance", "Success Chance: %s / 10000");
        add("gtna.machine.eye_of_wood.last_result", "Last Roll: %s");
        add("gtna.machine.eye_of_wood.result.success", "Success");
        add("gtna.machine.eye_of_wood.result.fail", "Steam Vent");
        add("gtna.machine.wireless_steam_output.tooltip_desc", "Sends Steam wirelessly to your Global Network.");
        add("gtna.machine.wireless_steam_output.tooltip_usage", "Usage: Place on Boilers to export Steam.");
        add("gtna.machine.wireless_steam_input.tooltip_desc", "Receives Steam wirelessly from your Global Network.");
        add("gtna.machine.wireless_steam.transfer_rate", "Transfer Rate: %s mB/t");
        add("gtna.machine.wireless_steam.transfer_rate.unlimited",
                "Transfer Rate: Unlimited (moves the whole buffer every tick)");
        add("block.gtna.large_steam_furnace", "Large Steam Furnace");
        add("block.gtna.large_steam_alloy_smelter", "Large Steam Alloy Smelter");
        add("block.gtna.large_steam_hammer", "Large Steam Hammer");
        add("block.gtna.large_steam_compressor", "Large Steam Compressor");
        add("block.gtna.large_steam_extractor", "Large Steam Extractor");
        add("block.gtna.large_steam_ore_washer", "Large Steam Ore Washer");
        add("block.gtna.large_steam_circuit_assembler", "Large Steam Circuit Assembler");
        add("gtna.machine.large_steam_circuit_assembler.engrave_circuit", "Engrave Circuit");
        add("gtna.machine.large_steam_circuit_assembler.circuit", "Engraved Circuit: %s");
        add("gtna.machine.large_steam_circuit_assembler.remaining", "Circuits Needed: %s");
        add("gtna.machine.large_steam_circuit_assembler.multiply_mode", "Multiply Mode: %s");
        add("gtna.machine.on", "On");
        add("gtna.machine.off", "Off");
        add("block.gtna.large_steam_mixer", "Large Steam Mixer");
        add("block.gtna.large_steam_centrifuge", "Large Steam Centrifuge");
        add("block.gtna.large_steam_thermal_centrifuge", "Large Steam Thermal Centrifuge");
        add("block.gtna.large_steam_bath", "Large Steam Bath");
        add("block.gtna.primitive_distillation_tower", "Primitive Distillation Tower");
        add("block.gtna.large_steam_lathe", "Large Steam Lathe");
        add("block.gtna.large_steam_cutting", "Large Steam Cutting Machine");
        add("block.gtna.large_steam_bending", "Large Steam Bending Machine");
        add("block.gtna.large_steam_extruder", "Large Steam Extruder");
        add("block.gtna.large_steam_wiremill", "Large Steam Wiremill");
        add("block.gtna.large_steam_sifter", "Large Steam Sifter");
        add("block.gtna.steam_lava_maker", "Steam Lava Maker");
        add("block.gtna.steam_item_vault", "Steam Item Vault");
        add("gtna.multiblock.vault.types", "Stored types: %s / %s");
        add("gtna.multiblock.vault.items", "Stored items: %s");
        add("block.gtna.large_steam_forming_press", "Large Steam Forming Press");
        add("block.gtna.steam_cactus_wonder", "Cactus Wonder");
        add("block.gtna.steam_cracking", "Steam Cracker");
        add("block.gtna.steam_mega_compressor", "Steam Supercompressor");
        add("block.gtna.large_steam_storage_tank", "Large Steam Storage Tank");
        add("block.gtna.large_steam_solar_boiler", "Large Steam Solar Boiler");
        add("gtna.machine.large_steam_solar_boiler.size", "Structure Size: %s x %s");
        add("gtna.machine.large_steam_solar_boiler.sunlit", "Sunlit Cells: %s");
        add("gtna.machine.large_steam_solar_boiler.production", "Steam Production: %s mB/s");
        add("gtna.machine.large_steam_solar_boiler.idle",
                "Not producing: night, rain, or no sunlit solar boiling cells.");
        add("block.gtna.dimensionally_transcendent_dirt_forge", "Dimensionally Transcendent Dirt Forge");
        add("block.gtna.dimensionally_transcendent_steam_boiler", "Dimensionally Transcendent Steam Boiler");
        add("block.gtna.dimensionally_transcendent_steam_oven", "Dimensionally Transcendent Steam Oven");
        add("block.gtna.steam_cobbler", "Steam Cobbler");
        add("block.gtna.stone_superheater", "Stone SuperHeater");
        add("block.gtna.steam_manufacturer", "Steam Manufacturer");
        add("block.gtna.stronze_wrapped_casing", "Stronze-Wrapped Casing");
        add("block.gtna.hydraulic_assembler_casing", "Hydraulic Assembler Casing");
        add("block.gtna.borosilicate_glass", "Borosilicate Glass");
        add("block.gtna.breel_plated_casing", "Breel-Plated Casing");
        add("gtna.super_heater", "Super Heating");
        add("gtna.hydraulic_manufacturing", "Hydraulic Manufacturing");
        add("gtna.lava_maker", "Lava Maker");
        add("gtna.cactus_wonder", "Cactus Wonder");
        add("item.gtceu.tool.vajra", "Vajra Omnitool");
        add("block.gtna.steam_woodcutter", "Steam Woodcutter");
        add("gtna.woodcutter", "Woodcutter");
        add("gtna.nano_forge", "Nano Forge");
        add("gtna.plasma_forge", "Plasma Forge");
        add("gtna.desulfurizer", "Desulfurizer");
        add("gtna.dimensional_focus_engraving_array", "Dimensional Focus Engraving Array");
        add("gtna.ultimate_material_forge", "Ultimate Material Forge");
        add("gtna.loom", "Loom");
        add("gtna.sintering_furnace", "Sintering Furnace");
        add("gtna.dyson_sphere", "Dyson Sphere");
        add("gtna.assembler_module", "Space Assembly");
        add("gtna.miner_module", "Space Miner");
        add("gtna.drilling_module", "Space Drilling");
        add("gtna.recipe.power_module_tier", "Power Module: MK %s");
        add("gtna.multiblock.pattern.error.power_module", "All Power Modules must be the same MK");
        add("gtna.machine.space_elevator.spools", "Nanotube Spools: %s / %s");
        add("gtna.machine.space_elevator.power_module", "Power Module: MK %s");
        add("gtna.machine.space_elevator.modules", "Modules connected: %s");
        add("gtna.machine.space_elevator_module.connected", "Connected to a running Space Elevator");
        add("gtna.machine.space_elevator_module.not_connected", "Not connected to a running Space Elevator");
        add("gtna.machine.dyson_sphere.amount", "Swarm modules in orbit: %s");
        add("gtna.machine.dyson_sphere.damage", "Swarm damage: %s%%");
        // GTNH Bose-Einstein Condensate
        add("gtna.bec.condensate.neutronium", "Neutronium");
        add("gtna.bec.condensate.cosmicneutronium", "Cosmic Neutronium");
        add("gtna.bec.condensate.bedrockium", "Bedrockium");
        add("gtna.bec.condensate.chromaticglass", "Chromatic Glass");
        add("gtna.bec.condensate.celestialtungsten", "Celestial Tungsten");
        add("gtna.bec.condensate.infinity", "Infinity");
        add("gtna.bec.condensate.hypogen", "Hypogen");
        add("gtna.bec.condensate.transcendentmetal", "Transcendent Metal");
        add("gtna.bec.condensate.dimshiftedsuperfluid", "Dim. Shifted Superfluid");
        add("gtna.bec.condensate.phononmedium", "Lossless Phonon Transfer Medium");
        add("gtna.bec.condensate.quarkgluonplasma", "Degenerate Quark Gluon Plasma");
        add("gtna.bec.condensate.spacetime", "SpaceTime");
        add("gtna.bec.condensate.time", "Tachyon Rich");
        add("gtna.bec.condensate.space", "Spatially Enlarged");
        add("gtna.bec.condensate.cosmicsolder", "Cosmic Solder");
        add("gtna.bec.condensate.mhdcsm", "MHDCSM");
        add("gtna.bec.condensate.magmatter", "MagMatter");
        add("gtna.bec.condensate.universium", "Universium");
        add("gtna.bec.condensate.eternity", "Eternity");
        add("gtna.condensate_generator", "Condensate Entanglement");
        add("gtna.condensate_assembler", "Condensate Assembly");
        add("gtna.recipe.bec_nanite_tiers", "Nanite tiers: %s");
        add("gtna.bec.gui.none", "None");
        add("gtna.bec.gui.operation", "Operation");
        add("gtna.bec.gui.analog", "Analog");
        add("gtna.bec.gui.threshold", "Threshold");
        add("gtna.bec.gui.current", "Current: %s");
        add("gtna.bec.gui.nanite_tier", "Tier %s");
        add("gtna.bec.gui.filter", "Condensate filter");
        add("gtna.bec.gui.mode", "Mode");
        add("gtna.bec.gui.pause_next_step", "Pause Next Step");
        add("gtna.bec.gui.pause_immediately", "Pause Immediately");
        add("gtna.bec.gui.nanite_count", "%s x %s");
        add("gtna.bec.gui.producing", "Condensate this cycle:");
        add("gtna.bec.gui.field_strength", "Field strength: %s");
        add("gtna.bec.gui.stored", "Stored: %s mB");
        add("gtna.bec.gui.stored_condensate", "Stored Condensate:");
        add("gtna.bec.gui.parameters", "Parameters");
        add("gtna.bec.gui.field_strength_param", "Field strength (mB, EU/t)");
        add("gtna.bec.gui.filters", "Condensate filters");
        add("gtna.bec.gui.available_condensate", "Available Condensate:");
        add("gtna.bec.gui.providing_nanites", "Providing Nanites:");
        add("gtna.bec.gui.ionode_status", "Status: %s");
        add("gtna.bec.gui.provided_nanite", "Provided Nanite: %s");
        add("gtna.bec.gui.required_nanite", "Required Nanite: %s");
        add("gtna.bec.gui.next_nanite_none", "Next Nanite: None");
        add("gtna.bec.gui.next_nanite", "Next Nanite: %s at progress %s");
        add("gtna.bec.gui.slowdowns", "Unrequested condensates: %s");
        add("gtna.bec.gui.required_condensate", "Required Condensate:");
        add("gtna.bec.gui.remaining_condensate", "  %s %s / %s");
        add("gtna.bec.gui.min_parallel", "Min parallels");
        add("gtna.bec.gui.max_parallel", "Max parallels");
        add("gtna.bec.gui.speed_divisor", "Speed divisor");
        add("gtna.bec.gui.nanite_desc", "%s (Tier %s)");
        add("gtna.bec.node_state.Idle", "Idle");
        add("gtna.bec.node_state.Unpowered", "§cUnpowered");
        add("gtna.bec.node_state.AssemblerOffline", "§cObservation Array Offline");
        add("gtna.bec.node_state.NaniteTierTooLow", "§eInsufficient Nanite Tier");
        add("gtna.bec.node_state.PausedStep", "Paused (Step)");
        add("gtna.bec.node_state.PausedImmediate", "Paused (Immediate)");
        add("gtna.bec.node_state.Crafting", "Crafting");
        add("gtna.bec.node_state.InternalError", "§cInternal Error: break and replace the node");
        add("gtna.bec.recipe.not_enough_parallels", "Insufficient Parallels (Min Parallels Too High)");
        add("gtna.bec.recipe.no_bec_assembler", "Condensate Observation Array Offline");
        add("gtna.bec.recipe.missing_condensate", "Missing condensate: %s x %s mB");
        add("gtna.bec.recipe.power_failure", "The Observation Array lost power");
        add("gtna.bec.recipe.bec_clogged", "More than 3 unrequested condensates in the network");
        add("gtna.machine.bec_hatch.tooltip.0",
                "Connects a BEC multiblock to Bose-Einstein Condensate Conduits through its front face");
        add("gtna.machine.bec_hatch.tooltip.1", "Conduits only join conduits of the same colour (dye them)");
        add("gtna.machine.nanite_containment_bus.tooltip.0",
                "Holds nanites for use in multiblocks; they are never consumed");
        add("gtna.machine.nanite_containment_bus.tooltip.1", "Keeps its contents when broken");
        add("gtna.machine.line_of_sight_connector_hatch.tooltip.0",
                "Connects to another Line-Of-Sight Connector Hatch");
        add("gtna.machine.line_of_sight_connector_hatch.tooltip.1", "Connectors must face each other");
        add("gtna.machine.line_of_sight_connector_hatch.tooltip.2", "Opaque blocks prevent connections");
        add("gtna.machine.line_of_sight_connector_hatch.tooltip.3",
                "The maximum distance between two connectors is %s blocks");
        add("gtna.machine.nanite_detector_hatch.tooltip.0", "Checks the nanite tier requested by a Teleportation Node");
        add("gtna.machine.nanite_detector_hatch.tooltip.1",
                "Emits a redstone signal when the condition in its UI is true");
        add("gtna.machine.nanite_detector_hatch.tooltip.2", "Analog mode ignores the threshold and emits the tier");
        add("gtna.machine.condensate_detector_hatch.tooltip.0", "Checks the condensate stored in a Containment Field");
        add("gtna.machine.condensate_detector_hatch.tooltip.1",
                "Emits a redstone signal when the condition in its UI is true");
        add("gtna.machine.condensate_detector_hatch.tooltip.2", "An empty filter sums all stored condensate");
        add("gtna.machine.io_node_controller_hatch.tooltip.0", "A redstone signal pauses its Teleportation Node");
        add("gtna.machine.io_node_controller_hatch.tooltip.1", "Pause immediately, or when the next step begins");
        add("gtna.machine.io_node_controller_hatch.tooltip.2",
                "Paused nodes use no condensate and do not fail from contaminants");
        add("gtna.reaction_furnace", "Reaction Furnace");
        add("gtna.machine.reaction_furnace.module",
                "§6Extension:§r §7unlocks the Parallel and Accelerate Hatches");
        add("gtna.chemical_vapor_deposition", "Chemical Vapor Deposition");
        add("gtna.physical_vapor_deposition", "Physical Vapor Deposition");
        add("gtna.rare_earth_centrifugal", "Rare Earth Centrifugal");
        add("gtna.arc_generator", "Arc Generator");
        add("gtna.pcb_factory", "PCB Factory");
        add("gtna.space_probe_surface_reception", "Space Probe Surface Reception");
        add("gtna.atomization_condensation", "Atomization Condensation");
        add("gtna.plasma_condenser", "Plasma Condenser");
        add("gtna.hyper_reactor", "Hyper Reactor");
        add("gtna.fuel_cell_energy_absorption", "Fuel Cell Energy Absorption");
        add("gtna.data_analysis", "Data Analysis");
        add("gtna.data_integration", "Data Integration");
        add("gtna.machine.supercomputing_center.tier", "Supercomputing Center Tier: %s");
        add("gtna.machine.supercomputing_center.incompatible",
                "Components do not match the tier (tier 1: HPCA, 2: NICH, 3: GWCA)");
        add("gtna.machine.supercomputing_center.modification", "CWU/t Multiplier: %s");
        add("gtna.machine.thermal_conductor_hatch.tooltip", "§7Holds MFPC coolant for the Supercomputing Center");
        add("gtna.fuel_cell_energy_transfer", "Fuel Cell Energy Transfer");
        add("gtna.fuel_cell_energy_release", "Fuel Cell Energy Release");
        add("gtna.recipe.fuel_cell.converted_energy", "Stored Energy: %s EU");
        add("gtna.recipe.fuel_cell.converted_efficiency", "Conversion Efficiency: %s%%");
        add("gtna.machine.fuel_cell.no_membrane", "No membrane electrode in the input buses");
        add("gtna.machine.fuel_cell.no_electrolyte", "No released electrolyte (anode and cathode) in the hatches");
        add("gtna.machine.fuel_cell.efficiency", "Fuel Efficiency Multiplier: %s");
        add("gtna.machine.fuel_cell.decay", "Continuous Operation Efficiency Decay: %s");
        add("gtna.fluid.energy_storage_anode", "%s Energy Storage Anode");
        add("gtna.fluid.energy_storage_cathode", "%s Energy Storage Cathode");
        add("gtna.fluid.energy_release_anode", "%s Energy Release Anode");
        add("gtna.fluid.energy_release_cathode", "%s Energy Release Cathode");
        add("gtna.advanced_hyper_reactor", "Advanced Hyper Reactor");
        add("gtna.machine.pcb_factory.tier", "PCB Factory Tier: %s");
        add("gtna.machine.pcb_factory.tier_too_low", "Structure tier too low for this recipe");
        add("gtna.machine.desulfurizer.module",
                "§6Extension:§r §7unlocks Thread, Overclock, Accelerate, Parallel and Laser Hatches");
        add("gtna.transcendent_plasma_mixer", "Transcendent Plasma Mixer");
        add("gtna.recipe.hydraulic_manufacturing", "Hydraulic Manufacturing");
        add("block.gtna.leap_forward_one_blast_furnace", "Leap Forward One Blast Furnace");
        add("gtna.multiblock.leap_pbf.parallel_hud", "Current Parallel: %s");
        add("gtna.multiblock.leap_pbf.duration_hud", "Cycle Time: %ss");
        add("block.gtna.infernal_coke_oven", "Infernal Coke Oven");
        add("gtna.multiblock.infernal_coke.speed", "Current Speed: %s");
        add("gtna.multiblock.infernal_coke.uptime", "Uptime: %ss");
        add("gtna.recipe.infernal_coke", "Infernal Coke Processing");
        add("gtna.infernal_coke", "Infernal Coke Processing");
        add("block.gtna.hyper_pressure_reactor", "Hyper Pressure Reactor");
        add("gtna.high_pressure_reactor", "Hyper Pressure Reactor");
        add("block.gtna.compact_hyper_pressure_reactor", "Compact Hyper Pressure Reactor");
        add("gtna.recipe.high_pressure_reactor", "High Pressure Reaction");
        add("gtna.recipe.condition.compact_only", "Requires: CHPR\nCompact HyperPressure Reactor");
        add("block.gtna.void_miner_steam_gate_aged", "Void Miner SteamGate Aged");
        add("gtna.machine.void_miner.steam_tier", "Steam Injection Tier");
        add("block.gtna.electric_void_miner", "Electric Void Miner");
        add("gtna.machine.electric_void_miner.parallel_cap", "Parallel cap: §b%s");
        add("gtna.machine.electric_void_miner.no_program", "§7No active recipe");
        add("gtna.machine.electric_void_miner.active_program", "Recipe: §b%s");
        add("gtna.machine.electric_void_miner.active_cost",
                "Cost: §b%s mB Drilling Fluid§7, §b%s EU/t§7; Parallel: §b%s");
        add("item.gtna.planet_data_chip_moon", "Moon Planet Data Chip");
        add("item.gtna.planet_data_chip_mars", "Mars Planet Data Chip");
        add("item.gtna.planet_data_chip_venus", "Venus Planet Data Chip");
        add("item.gtna.planet_data_chip_mercury", "Mercury Planet Data Chip");
        add("item.gtna.planet_data_chip_glacio", "Glacio Planet Data Chip");
        add("gtna.electric_void_mining", "Precise Void Mining");
        add("gtna.random_void_mining", "Random Void Mining");
        add("gtna.world_data_scanner", "World Data Scanner");
        add("gtna.incubator", "Incubator");
        add("block.gtna.incubator", "Incubator");
        add("gtna.machine.electric_void_miner.mode", "Mode: §b%s");
        add("block.gtna.industrial_slaughterhouse", "Industrial Slaughterhouse");
        add("gtna.machine.slaughterhouse.tier", "Current Tier: %s");
        add("gtna.machine.slaughterhouse.mode.passive", "Passive Farming");
        add("gtna.machine.slaughterhouse.mode.hostile", "Hostile Farming");
        add("gtna.machine.slaughterhouse.mode.boss", "Boss Farming");
        add("gtna.machine.slaughterhouse.mode.dragon", "Dragon Slayer");
        add("gtna.machine.slaughterhouse.mode.unknown", "Unknown/Idle");
        add("gtna.recipe.slaughterhouse", "Industrial Slaughter");
        add("gtna.slaughterhouse", "Industrial Slaughter");
        add("gtna.multiblock.leap_pbf.layers_hud", "Extra Layers: %s");
        add("gtna.multiblock.max_threads", "Max Threads: %s");
        add("gtna.recipe.condition.restricted_items_disabled", "Disabled by Journey mode or Self Restraint");

        // --- Configurações (GUI) ---
        // Drift
        add("config.gtna.option.gameplay", "Gameplay");
        add("config.gtna.option.client", "Client");
        add("config.gtna.option.machines", "Machines");
        add("config.gtna.option.nexusFluxMatrix", "Nexus Flux Matrix");
        add("config.gtna.option.modDifficulty", "Mod Difficulty");
        add("config.gtna.option.selfRestraint", "Self Restraint");
        add("config.gtna.option.disableFlyInertia", "Disable Fly Inertia");
        add("config.gtna.option.wirelessSteamHud", "Wireless Steam HUD");
        add("config.gtna.option.wirelessEnergyHud", "Wireless Energy HUD");
        add("config.gtna.option.wirelessEnergyHudX", "Wireless Energy HUD X Position");
        add("config.gtna.option.wirelessEnergyHudY", "Wireless Energy HUD Y Position");
        add("config.gtna.option.wirelessSteamHudX", "Wireless Steam HUD X Position");
        add("config.gtna.option.wirelessSteamHudY", "Wireless Steam HUD Y Position");
        add("config.gtna.option.wirelessSteamHudHistorySeconds", "Wireless Steam HUD History Seconds");
        add("config.gtna.option.itemHalo", "Item Halos");
        add("gtna.machine.antimatter_collider_ring.mode_physics", "§b[Run: physics]");
        add("gtna.machine.antimatter_collider_ring.mode_production", "§a[Run: production]");
        add("gtna.machine.antimatter_collider_ring.magnet", "Magnets: §e%s §7(%s T)");
        add("gtna.machine.antimatter_collider_ring.energy", "Beam energy: §e%s TeV");
        add("gtna.machine.antimatter_collider_ring.lumi", "Luminosity: §e%s cm⁻²s⁻¹");
        add("gtna.machine.antimatter_collider_ring.helium", "Helium: §e%s%%");
        add("gtna.machine.antimatter_collider_ring.quench", "§cQuench: recovering for %s s");
        add("gtna.machine.antimatter_collider_ring.traps", "Penning traps: §e%s / %s");
        add("gtna.machine.antimatter_collider_ring.proposal", "Committee proposal: §e%s");
        add("gtna.machine.dimensional_rift_gate.open", "§a[Open a new rift]");
        add("gtna.machine.dimensional_rift_gate.close", "§c[Close the rift]");
        add("gtna.machine.dimensional_rift_gate.seed", "Seed: §e%s");
        add("gtna.machine.dimensional_rift_gate.biome", "Biome: §e%s");
        add("gtna.machine.dimensional_rift_gate.frequency", "Frequency: §e%s THz");
        add("gtna.machine.dimensional_rift_gate.phase", "Phase: §e%s°");
        add("gtna.machine.dimensional_rift_gate.amplitude", "Amplitude: §e%s%%");
        add("gtna.machine.dimensional_rift_gate.resonance", "Resonance R: §e%s");
        add("gtna.machine.dimensional_rift_gate.stability", "Stability: §e%s");
        add("gtna.machine.dimensional_rift_gate.depth", "Depth: §e%s / %s");
        add("gtna.machine.dimensional_rift_gate.upkeep", "SpaceTime upkeep: §e%s L/s");
        add("gtna.machine.dimensional_rift_gate.score", "Score:");
        add("gtna.machine.dimensional_rift_gate.atlas", "Atlas: §e%s seeds");
        add("gtna.machine.kinetic_orbital_lance.target", "Target:");
        add("gtna.machine.kinetic_orbital_lance.survey", "Survey: §e%s%%");
        add("gtna.machine.kinetic_orbital_lance.bank", "Bank: §e%s / %s EU");
        add("gtna.machine.kinetic_orbital_lance.barrel", "Barrel: §e%s K§7, liner wear §e%s%%");
        add("gtna.machine.kinetic_orbital_lance.efficiency", "Rail efficiency η §e%s§7, accuracy §e%s");
        add("gtna.originals.gui.committee", "Beam-Time Committee");
        add("gtna.originals.gui.atlas", "Constellation Atlas");
        add("gtna.originals.gui.bench", "Workbench");
        add("gtna.machine.beam_dump.tooltip.0",
                "§7Absorbs the beam of the §bAntimatter Collider Ring§7 when its magnets quench.");
        add("gtna.machine.beam_dump.tooltip.1", "§cWithout one, a quench hits the ring: recovery takes twice as long.");
        add("gtna.machine.seismic_probe.tooltip.0", "§7Records the starquakes of the §bStellar Containment Chamber§7.");
        add("gtna.machine.seismic_probe.tooltip.1",
                "§7Only recorded quakes are decoded and unlock new regions; also feeds the seismogram tab.");
        add("gtna.machine.liner_hatch.tooltip.0",
                "§7Holds spare barrel liners for the §bKinetic Orbital Lance§7: naquadah alloy or neutronium plates (dense or plain).");
        add("gtna.machine.liner_hatch.tooltip.1",
                "§7A worn or cracked liner is swapped automatically, without taking the gun apart.");
        add("gtna.originals.gui.quakes", "Seismogram");
        add("gtna.originals.gui.no_probe", "Install a Seismic Probe to record quakes");
        add("gtna.machine.mass_injector.tooltip.0",
                "§7Feeds solid star matter (dust or ingots) to the §bStellar Containment Chamber§7.");
        add("gtna.machine.mass_injector.tooltip.1",
                "§7Each item counts as 144 mB of the matching fluid; up to 64 per slot per second.");
        add("gtna.machine.detector_hatch.tooltip.0",
                "§7Records the collisions of the §bAntimatter Collider Ring§7 for the beam-time committee.");
        add("gtna.machine.detector_hatch.tooltip.1",
                "§cWithout one, physics runs record nothing: no significance and no proposal progress.");
        add("gtna.machine.target_cartridge_hatch.tooltip.0",
                "§7The first Target Cartridge picks the §bKinetic Orbital Lance§7 target.");
        add("gtna.machine.target_cartridge_hatch.tooltip.1",
                "§7After each shot the cartridges take turns: load several to rotate targets.");
        add("gtna.machine.tuning_hatch.tooltip.0", "§7Lets redstone tune the §bDimensional Rift Gate§7.");
        add("gtna.machine.tuning_hatch.tooltip.1",
                "§7Signal strength 1–15 sets the amplitude (about 6.7 % per level); 0 leaves the GUI value.");
        add("gtna.originals.gui.mass_period", "Mass–Period Diagram");
        add("gtna.originals.gui.standard_model", "Standard Model Board");
        add("gtna.originals.gui.seismograph", "Rift Seismograph");
        add("gtna.originals.gui.orbital_map", "Orbital Map");
        add("gtna.machine.kinetic_orbital_lance.computation", "Aim computation: §b%s CWU/t");
        add("gtna.originals.info.title", "Information");
        add("gtna.originals.info.toc", "Contents");
        add("gtna.originals.info.close", "§c[Close]");
        add("gtna.originals.info.hint", "Click for how this machine works");
        add("gtna.originals.info.stellar_containment_chamber.overview", "Overview");
        add("gtna.originals.info.stellar_containment_chamber.overview.1",
                "Holds a neutron star in containment bands and turns its spin into EU for the owner's Nexus wireless network. There are no recipes: the star has a mass, a spin period and a crust, and everything you do changes them.");
        add("gtna.originals.info.stellar_containment_chamber.build", "Structure and hatches");
        add("gtna.originals.info.stellar_containment_chamber.build.1",
                "93×93×93 sphere. Hatches replace the Radiant Naquadah casings in the 5×5 ring around the controller: up to 8 Input Hatches, 4 Output Buses, 4 Mass Injectors and 1 Seismic Probe.");
        add("gtna.originals.info.stellar_containment_chamber.build.2",
                "The Degenerate Matter Core (radius 7) at the centre must be complete. When the bands get power the core is taken into the star; it comes back as blocks when the chamber stops or the structure breaks.");
        add("gtna.originals.info.stellar_containment_chamber.power", "Power and extraction");
        add("gtna.originals.info.stellar_containment_chamber.power.1",
                "The bands draw their upkeep from the owner's Nexus network every second. Without it the star stays dark, and a lit star takes containment damage.");
        add("gtna.originals.info.stellar_containment_chamber.power.2", "Band upkeep = 2^(40 + 2·tier) EU/t");
        add("gtna.originals.info.stellar_containment_chamber.power.3",
                "Set the extraction with [-] and [+] as 2^n EU/t (n from 40 to 62). The energy goes to the Nexus network.");
        add("gtna.originals.info.stellar_containment_chamber.power.4",
                "Cap = 2^(55 + tier) EU/t (half until the star reaches the millisecond region); 2^62 as a black hole");
        add("gtna.originals.info.stellar_containment_chamber.feeding", "Feeding and outputs");
        add("gtna.originals.info.stellar_containment_chamber.feeding.1",
                "Feed star matter through Input Hatches (liquid, molten, gas or plasma) or as dusts and ingots through a Mass Injector (144 mB each). Feeding adds mass and spins the star up, like a recycled pulsar; 15% of the mass leaves as binding energy, paid at once as EU.");
        add("gtna.originals.info.stellar_containment_chamber.feeding.2",
                "Solar masses per mB: constrained star matter 1e-7, white dwarf matter 1e-8, raw star matter 1e-9, neutronium 1e-10");
        add("gtna.originals.info.stellar_containment_chamber.feeding.3",
                "Outputs in the Output Buses: neutronium dust from crust mining (grows with extraction) and white dwarf matter dust from starquakes.");
        add("gtna.originals.info.stellar_containment_chamber.quakes", "Starquakes and bands");
        add("gtna.originals.info.stellar_containment_chamber.quakes.1",
                "Changing the spin builds stress; at 1 a starquake happens. Only a Seismic Probe decodes quakes (Seismogram tab). Decoded quakes raise the band tier: micro → tier 2, Vela (fast feeding) → tier 3, Vela plus a record spin (< 1.4 ms) → tier 4.");
        add("gtna.originals.info.stellar_containment_chamber.quakes.2",
                "The Magnetar button inverts the band field. After 10 minutes the star becomes a magnetar and can give antiquakes.");
        add("gtna.originals.info.stellar_containment_chamber.quakes.3",
                "A quake bigger than the band capacity, or any quake with unpowered bands, damages containment by 10%. At 100% the star loses 10% of its mass.");
        add("gtna.originals.info.stellar_containment_chamber.limits", "Limits");
        add("gtna.originals.info.stellar_containment_chamber.limits.1",
                "Above the TOV limit (2.2 M☉) the star collapses into a black hole, for good. Energy then comes from the ergosphere: the faster it spun when it collapsed, the more there is.");
        add("gtna.originals.info.stellar_containment_chamber.limits.2",
                "Kepler period = 2π·sqrt(R³ / (G·M)); spinning faster tears the star apart");
        add("gtna.originals.info.stellar_containment_chamber.limits.3",
                "Side tabs: Mass–Period diagram (the star's track with the TOV and Kepler limits) and Seismogram.");
        add("gtna.originals.info.antimatter_collider_ring.overview", "Overview");
        add("gtna.originals.info.antimatter_collider_ring.overview.1",
                "Accelerates two counter-rotating beams around a 3 km ring and collides them. Production runs make exotic particles and antiprotons; physics runs gather luminosity to discover particles and complete committee proposals.");
        add("gtna.originals.info.antimatter_collider_ring.build", "Structure and hatches");
        add("gtna.originals.info.antimatter_collider_ring.build.1",
                "Hatches replace casings in the 5×5 ring around the controller: Input Hatches for liquid helium, Output Buses for particles and antiproton cells, a Collision Detector Hatch (needed for physics runs) and a Beam Dump (halves the quench recovery).");
        add("gtna.originals.info.antimatter_collider_ring.build.2",
                "While running, the ring and gyro blocks are taken into the controller and drawn moving; they come back when the machine stops.");
        add("gtna.originals.info.antimatter_collider_ring.power", "Power and cooling");
        add("gtna.originals.info.antimatter_collider_ring.power.1",
                "Magnets = 2^(33 + magnet tier) EU/t; Penning traps = 2^(20 + trap tier) EU/t, both from the Nexus network");
        add("gtna.originals.info.antimatter_collider_ring.power.2",
                "Liquid helium per second = 0.5·2^tier L (×0.6 after cryogenic Penning traps)");
        add("gtna.originals.info.antimatter_collider_ring.power.3",
                "Less helium than the demand quenches the magnets: the beam stops for 60·(tier + 1) seconds.");
        add("gtna.originals.info.antimatter_collider_ring.modes", "Modes");
        add("gtna.originals.info.antimatter_collider_ring.modes.1",
                "Click the mode line to switch. Production: particles with 10% yield before evidence, 40% at 3σ and 100% after the 5σ discovery; antiprotons fill the traps and leave as Antiproton Penning Cells (1e11 each).");
        add("gtna.originals.info.antimatter_collider_ring.modes.2",
                "Physics: the integrated luminosity raises each particle's significance and advances the active proposal.");
        add("gtna.originals.info.antimatter_collider_ring.modes.3",
                "Beam energy p = 0.3·B·ρ (B magnet field, ρ = 3 km); a particle needs E_cm above its threshold");
        add("gtna.originals.info.antimatter_collider_ring.proposals", "Committee proposals");
        add("gtna.originals.info.antimatter_collider_ring.proposals.1",
                "In order: Nb3Sn magnet, vertex detector, stochastic cooling, cryogenic Penning traps, REBCO magnet, lepton collider, heavy ions, neutronium magnet, beyond the Standard Model. Each one unlocks stronger magnets, traps or modes.");
        add("gtna.originals.info.antimatter_collider_ring.proposals.2",
                "If the trap upkeep is not paid the stored antiprotons annihilate and damage the ring. Side tabs: Standard Model board and Committee.");
        add("gtna.originals.info.dimensional_rift_gate.overview", "Overview");
        add("gtna.originals.info.dimensional_rift_gate.overview.1",
                "Opens a rift to a seeded dimension and pulls resources from it. Tune frequency, phase and amplitude towards the seed's hidden optimum to raise the resonance.");
        add("gtna.originals.info.dimensional_rift_gate.build", "Structure and hatches");
        add("gtna.originals.info.dimensional_rift_gate.build.1",
                "Hatches in the 5×5 ring around the controller: an Input Hatch for SpaceTime, an Input Bus for Rift Probes and Depth Anchors, an Output Bus, and a Rift Tuning Hatch (a redstone signal 0–15 sets the amplitude to 0–100%).");
        add("gtna.originals.info.dimensional_rift_gate.power", "Power and stability");
        add("gtna.originals.info.dimensional_rift_gate.power.1",
                "Field = 2^36 EU/t from the Nexus network while open; without it the rift collapses");
        add("gtna.originals.info.dimensional_rift_gate.power.2",
                "SpaceTime fluid keeps it stable: each litre adds 2 stability. Losses grow with low resonance and with depth.");
        add("gtna.originals.info.dimensional_rift_gate.power.3",
                "Upkeep (L/s) = (λ·(1 − R)·(1 + D/10) + 0.4·(8 − pylons)) / 2");
        add("gtna.originals.info.dimensional_rift_gate.tuning", "Tuning");
        add("gtna.originals.info.dimensional_rift_gate.tuning.1",
                "Click Open for a rift with a random seed. Tune with [--] [-] [+] [++] (±10 / ±1). Each Rift Probe consumed narrows the tolerances by 20%.");
        add("gtna.originals.info.dimensional_rift_gate.tuning.2", "Resonance R = exp(−(Δf/σf)² − (Δφ/σφ)² − (ΔA/σA)²)");
        add("gtna.originals.info.dimensional_rift_gate.tuning.3",
                "Output per second ∝ R²·D^1.5·S/100, as dusts of the biome's materials");
        add("gtna.originals.info.dimensional_rift_gate.tuning.4",
                "A Depth Anchor deepens the rift by one, up to the maximum depth. Relic and Void biomes only yield from depth 20 and 40.");
        add("gtna.originals.info.dimensional_rift_gate.harmonics", "Harmonics");
        add("gtna.originals.info.dimensional_rift_gate.harmonics.1",
                "Holding R ≥ 0.9 for 30 s records the seed's harmonic. Click recorded harmonics to load up to 5 in the chord: consonant chords (octave, fifth) are stable; dissonant chords (tritone, minor second) dig deeper but cost more SpaceTime.");
        add("gtna.originals.info.dimensional_rift_gate.harmonics.2",
                "Holding R ≥ 0.98 for a minute can give a Rift Singularity. Stability at 0 collapses the rift; R under 0.2 for 10 s inverts it (−10 stability). Side tabs: Seismograph and Atlas.");
        add("gtna.originals.info.kinetic_orbital_lance.endgame",
                "Endgame");
        add("gtna.originals.info.kinetic_orbital_lance.endgame.1",
                "Exclusive: capsules from Arrokoth bring Primordial Tholin (Forge of Gods structure casing); capsules from Nexus-1 bring Nexium (Collider dipoles, Magnetarium).");
        add("gtna.originals.info.kinetic_orbital_lance.endgame.2",
                "Needs: Nexus-1's crust only breaks under Magnetarium ingots (Magnetar Slug, 2000 t). Mixer: 2 Nexium + 1 Magnetar Crystal + 4 White Dwarf Matter dust, then the blast furnace at 12000 K.");
        add("gtna.originals.info.kinetic_orbital_lance.endgame.3",
                "The Magnetar Crystal comes from the Stellar Containment Chamber; the Collider needs your Nexium for its last magnets.");
        add("gtna.originals.info.stellar_containment_chamber.endgame",
                "Endgame");
        add("gtna.originals.info.stellar_containment_chamber.endgame.1",
                "Exclusive: a magnetar starquake (field inverted for 600 s) leaves 4 Magnetar Crystals; a collapse leaves 64 Degenerate Core Matter (Eye of Harmony fields from Advanced tier).");
        add("gtna.originals.info.stellar_containment_chamber.endgame.2",
                "Needs: the inverted field tears the crust. Each 60 s of magnetar field takes one Forgecore plate from the Mass Injector; without one the field drops and the crust takes 10% damage.");
        add("gtna.originals.info.stellar_containment_chamber.endgame.3",
                "Forgecore comes from the Forge World biome of the Dimensional Rift Gate; the Lance needs your crystals for the Magnetar Slug.");
        add("gtna.originals.info.antimatter_collider_ring.endgame",
                "Endgame");
        add("gtna.originals.info.antimatter_collider_ring.endgame.1",
                "Exclusive: antiproton cells go into the Cosmic Neutronium and Infinity fuel rods and the Forge of Gods siphon. Higgs and top: Gravitational Lens. X-Nexus: Forge of Gods controller and deep anchors.");
        add("gtna.originals.info.antimatter_collider_ring.endgame.2",
                "Needs: the Neutronium Magnet proposal only closes with 1024 fine Nexium wire in the input buses; the wire is wound into the tier-4 dipoles when it closes.");
        add("gtna.originals.info.antimatter_collider_ring.endgame.3",
                "Nexium comes from the Kinetic Orbital Lance (Nexus-1); the Rift Gate needs your X-Nexus to go past depth 40.");
        add("gtna.originals.info.dimensional_rift_gate.endgame",
                "Endgame");
        add("gtna.originals.info.dimensional_rift_gate.endgame.1",
                "Exclusive: one material per biome (Prismatium, Chronomercury, Forgecore, Vivispore, Abyssal Antimatter, Precursor Residue, Void Ash). The Singularity goes into the Forge of Gods controller and Advanced+ Eye of Harmony fields.");
        add("gtna.originals.info.dimensional_rift_gate.endgame.2",
                "Needs: from depth 40 on, each Depth Anchor also takes one Contained X-Nexus; without one it stays in the bus.");
        add("gtna.originals.info.dimensional_rift_gate.endgame.3",
                "X-Nexus comes from the Antimatter Collider Ring; the Stellar Chamber needs your Forgecore to hold a magnetar.");
        add("gtna.originals.info.kinetic_orbital_lance.lore",
                "Records I");
        add("gtna.originals.info.kinetic_orbital_lance.lore.1",
                "Nexus-1 was never on any chart. The first survey of Arrokoth's red tholin fields found its shadow: a body heavier than its size allows, its crust pressed into a lattice no slug could dent. The Lance was built to answer one question: what is it made of?");
        add("gtna.originals.info.kinetic_orbital_lance.lore_2",
                "Records II");
        add("gtna.originals.info.kinetic_orbital_lance.lore_2.1",
                "The answer came back in the capsules as Nexium, a metal that carries current without heat and keeps the shape of every field it has crossed. Each landing raises the same doubt among the engineers: who left it out there, and are they still waiting for it to be collected?");
        add("gtna.originals.info.stellar_containment_chamber.lore",
                "Records I");
        add("gtna.originals.info.stellar_containment_chamber.lore.1",
                "A contained neutron star is not a power plant; it is a negotiation. Every starquake is the crust giving way, and every quake the Seismic Probe decodes teaches the bands how to hold the next one.");
        add("gtna.originals.info.stellar_containment_chamber.lore_2",
                "Records II");
        add("gtna.originals.info.stellar_containment_chamber.lore_2.1",
                "Invert the field and the star becomes a magnetar. For ten minutes the crust screams, held together by Forgecore plates from a world that should not exist. When it finally breaks, it breaks into crystals that still carry the inverted field. What else does the star remember?");
        add("gtna.originals.info.antimatter_collider_ring.lore",
                "Records I");
        add("gtna.originals.info.antimatter_collider_ring.lore.1",
                "The committee grants beam time one proposal at a time, and every proposal is a bet on what lies past the last threshold. Kaons, bottom quarks, the W and the Z were expected. The Higgs was a confirmation.");
        add("gtna.originals.info.antimatter_collider_ring.lore_2",
                "Records II");
        add("gtna.originals.info.antimatter_collider_ring.lore_2.1",
                "X-Nexus was not. At 4.8 TeV the detectors recorded a particle that decays into nothing the Standard Model allows, and only dipoles wound from Nexium bend the beam hard enough to make it. The heavy-ion runs keep producing it. The committee no longer asks what it is, only how many.");
        add("gtna.originals.info.dimensional_rift_gate.lore",
                "Records I");
        add("gtna.originals.info.dimensional_rift_gate.lore.1",
                "The Gate does not open a door; it tunes a chord until space agrees to part. Each seed resolves into a different place: crystal plains, a sea of mercury that runs backwards in time, a world that is one endless forge.");
        add("gtna.originals.info.dimensional_rift_gate.lore_2",
                "Records II");
        add("gtna.originals.info.dimensional_rift_gate.lore_2.1",
                "Below depth 40 the anchors slip unless an X-Nexus is set into their lattice, as if the deep biomes recognise it. There, among ash and precursor ruins, the rift sometimes folds in on itself and leaves a singularity behind. Someone built those ruins. Did they also build the Gate?");
        add("gtna.originals.jei.nexium",
                "Only from the Kinetic Orbital Lance: return capsules from Nexus-1, which can only be hit with Magnetar Slugs. Blast furnace (10800 K) for the ingot, wiremill for fine wire: the Antimatter Collider Ring needs 1024 for its tier-4 dipoles.");
        add("gtna.originals.jei.primordial_tholin",
                "Only from the Kinetic Orbital Lance: return capsules from Arrokoth. Used in the Forge of Gods structure casing.");
        add("gtna.originals.jei.magnetar_crystal",
                "Only from the Stellar Containment Chamber: 4 per magnetar starquake (magnetar field held 600 s, one Forgecore plate per 60 s in the Mass Injector). Mixed into Magnetarium for the Magnetar Slug.");
        add("gtna.originals.jei.degenerate_core_matter",
                "Only from the Stellar Containment Chamber: 64 when the star collapses. Used in Eye of Harmony field generators from the Advanced tier.");
        add("gtna.originals.jei.prismatium",
                "Only from the Dimensional Rift Gate, Crystal Plains biome. Used in the Forge of Gods Gravitational Lens.");
        add("gtna.originals.jei.chronomercury",
                "Only from the Dimensional Rift Gate, Mercury Ocean biome. Used in Eye of Harmony field generators from the Advanced tier.");
        add("gtna.originals.jei.forgecore",
                "Only from the Dimensional Rift Gate, Forge World biome. Blast furnace (9000 K) and bender: its plates hold the Stellar Containment Chamber's magnetar field.");
        add("gtna.originals.jei.vivispore",
                "Only from the Dimensional Rift Gate, Spore Forest biome. Used in the Forge of Gods Harmonic Phonon Transmission Conduit.");
        add("gtna.originals.jei.abyssal_antimatter",
                "Only from the Dimensional Rift Gate, Antimatter Abyss biome. Used in the Infinity Antimatter Fuel Rod.");
        add("gtna.originals.jei.precursor_residue",
                "Only from the Dimensional Rift Gate, Civilisation Relic biome. Used in the Forge of Gods Remote Graviton Flow Modulator.");
        add("gtna.originals.jei.void_ash",
                "Only from the Dimensional Rift Gate, Void biome (depth 40 and deeper). Used in Eye of Harmony field generators from the Advanced tier.");
        add("gtna.originals.jei.antiproton_cell",
                "Only from the Antimatter Collider Ring in production runs: one cell per 1e11 antiprotons in the Penning traps. Used in the Cosmic Neutronium and Infinity antimatter fuel rods and the Forge of Gods siphon casing.");
        add("gtna.originals.jei.particles",
                "Only from the Antimatter Collider Ring in production runs, once the beam passes each particle's threshold. Higgs and top go into the Gravitational Lens; X-Nexus into the Forge of Gods controller and Depth Anchors past depth 40.");
        add("gtna.originals.jei.rift_singularity",
                "Only from the Dimensional Rift Gate, when a deep rift folds in on itself. Used in the Forge of Gods controller and Eye of Harmony field generators from the Advanced tier.");
        add("gtna.originals.info.kinetic_orbital_lance.overview", "Overview");
        add("gtna.originals.info.kinetic_orbital_lance.overview.1",
                "Fires projectiles from a capacitor bank at moons and asteroids and recovers the fragments in return capsules, which land as dusts of the body's materials.");
        add("gtna.originals.info.kinetic_orbital_lance.build", "Structure and hatches");
        add("gtna.originals.info.kinetic_orbital_lance.build.1",
                "Hatches in the 5×5 ring around the controller: Input Bus (projectile ingots), Output Bus (dusts), Computation Data Reception Hatch (aim), Barrel Liner Hatch (spare liners) and Target Cartridge Hatch.");
        add("gtna.originals.info.kinetic_orbital_lance.build.2",
                "While formed, the gun (everything above the turret ring) is taken into the controller and drawn slewing to the target.");
        add("gtna.originals.info.kinetic_orbital_lance.power", "Bank and firing");
        add("gtna.originals.info.kinetic_orbital_lance.power.1",
                "The bank charges from the Nexus network at up to 2^36 EU/t. With auto-fire on, a shot fires the whole bank as soon as it is full.");
        add("gtna.originals.info.kinetic_orbital_lance.power.2", "Bank = 4e12·2^(rings − 1) EU");
        add("gtna.originals.info.kinetic_orbital_lance.power.3",
                "Projectiles: ingots of naquadah alloy, trinium, neutronium, cosmic neutronium or white dwarf matter. Heavier projectiles are slower but carry more.");
        add("gtna.originals.info.kinetic_orbital_lance.power.4",
                "v = sqrt(2·η·E / m); recovered mass ∝ 0.2·η·E / hardness × capsule × accuracy");
        add("gtna.originals.info.kinetic_orbital_lance.targets", "Targets and aim");
        add("gtna.originals.info.kinetic_orbital_lance.targets.1",
                "Start with the Moon. A body becomes targetable once its parents are surveyed to 100% (recover their characteristic mass). Cartridges in the Target Cartridge Hatch pick the target and take turns shot by shot.");
        add("gtna.originals.info.kinetic_orbital_lance.targets.2",
                "The reception hatch must be linked by optical cable to a transmission hatch of a working computation network (e.g. Network Switch fed by a Supercomputer). More CWU/t tightens the aim; it matters for far bodies.");
        add("gtna.originals.info.kinetic_orbital_lance.bench", "Barrel bench and wear");
        add("gtna.originals.info.kinetic_orbital_lance.bench.1",
                "Click components on the bench line: rails raise efficiency (up to 8, shift-click removes), cooling raises heat capacity, sensors improve aim, capsules improve recovery, the salvo splitter fires several projectiles. Mass and heat must stay within the budget; surveying bodies unlocks components.");
        add("gtna.originals.info.kinetic_orbital_lance.bench.2",
                "Each shot wears the liner and heats the barrel. A worn liner (100%) or a barrel over 2500 K misfires. Spare liners (naquadah alloy or neutronium plates) in the Barrel Liner Hatch are swapped in automatically. Side tabs: Orbital map and Bench.");
        add("gtna.subtitle.originals.collider_loop", "Collider ring hums");
        add("gtna.subtitle.originals.lance_charge_loop", "Lance capacitors charge");
        add("gtna.subtitle.originals.rift_loop", "Rift resonates");
        add("gtna.subtitle.originals.stellar_black_hole_loop", "Black hole roars");
        add("gtna.subtitle.originals.stellar_pulsar_loop", "Pulsar spins");
        add("gtna.subtitle.originals.lance_fire", "Orbital lance fires");
        add("gtna.subtitle.originals.collider_quench", "Collider magnets quench");
        add("gtna.subtitle.originals.stellar_quake", "Starquake");
        add("gtna.subtitle.originals.rift_open", "Rift opens");
        add("gtna.ui.o.nexus.tip", "Scan the structure: highlights the first wrong block");
        add("gtna.ui.o.prev_target", "Prev");
        add("gtna.ui.o.prev_target.tip", "Previous targetable body");
        add("gtna.ui.o.next_target", "Next");
        add("gtna.ui.o.next_target.tip", "Next targetable body");
        add("gtna.ui.o.auto", "Auto");
        add("gtna.ui.o.auto.tip", "Auto-fire: shoot whenever the bank is full");
        add("gtna.ui.o.orbit", "Orbit");
        add("gtna.ui.o.orbit.tip", "Orbital map");
        add("gtna.ui.o.bench", "Bench");
        add("gtna.ui.o.bench.tip", "Barrel bench");
        add("gtna.ui.o.pods", "Pods");
        add("gtna.ui.o.pods.tip", "Lit while capsules are returning");
        add("gtna.ui.o.info", "Info");
        add("gtna.ui.o.info.tip", "Field manual: how this machine works");
        add("gtna.ui.o.power", "Power");
        add("gtna.ui.o.power.tip", "Turn the machine on or off");
        add("gtna.ui.o.less", "Less");
        add("gtna.ui.o.less.tip", "Lower the extraction (2^n EU/t)");
        add("gtna.ui.o.more", "More");
        add("gtna.ui.o.more.tip", "Raise the extraction (2^n EU/t)");
        add("gtna.ui.o.magnetar", "Field");
        add("gtna.ui.o.magnetar.tip", "Invert the band field (magnetar after 10 min)");
        add("gtna.ui.o.mass_period", "M-P");
        add("gtna.ui.o.mass_period.tip", "Mass-period diagram");
        add("gtna.ui.o.seismo", "Quake");
        add("gtna.ui.o.seismo.tip", "Seismogram");
        add("gtna.ui.o.star", "Star");
        add("gtna.ui.o.star.tip", "Lit while the star burns");
        add("gtna.ui.o.mode", "Mode");
        add("gtna.ui.o.mode.tip", "Switch production / physics run");
        add("gtna.ui.o.model", "Model");
        add("gtna.ui.o.model.tip", "Standard Model board");
        add("gtna.ui.o.committee", "Board");
        add("gtna.ui.o.committee.tip", "Beam-time committee");
        add("gtna.ui.o.traps", "Traps");
        add("gtna.ui.o.traps.tip", "Penning traps");
        add("gtna.ui.o.cryo", "Cryo");
        add("gtna.ui.o.cryo.tip", "Lit while the helium supply is full");
        add("gtna.ui.o.ring", "Ring");
        add("gtna.ui.o.ring.tip", "Lit while the ring spins");
        add("gtna.ui.o.open_rift", "Open");
        add("gtna.ui.o.open_rift.tip", "Open a rift to a new seed");
        add("gtna.ui.o.close_rift", "Close");
        add("gtna.ui.o.close_rift.tip", "Close the rift");
        add("gtna.ui.o.chord", "Chord");
        add("gtna.ui.o.chord.tip", "Harmonic chord");
        add("gtna.ui.o.atlas", "Atlas");
        add("gtna.ui.o.atlas.tip", "Seed atlas");
        add("gtna.ui.o.depth", "Depth");
        add("gtna.ui.o.depth.tip", "Lit when depth anchors have deepened the rift");
        add("gtna.ui.o.resonant", "Lock");
        add("gtna.ui.o.resonant.tip", "Lit at resonance 0.9 or more (harmonics record)");
        add("gtna.ui.o.step_down", "-1");
        add("gtna.ui.o.step_down.tip", "Lower by 1");
        add("gtna.ui.o.step_up", "+1");
        add("gtna.ui.o.step_up.tip", "Raise by 1");
        add("gtna.ui.o.step_big", "+10");
        add("gtna.ui.o.step_big.tip", "Raise by 10");
        add("gtna.ui.o.orbit_map_title", "Orbital Map");
        add("gtna.ui.o.bench_title", "Barrel Bench");
        add("gtna.ui.o.mass_period_title", "Mass-Period Diagram");
        add("gtna.ui.o.seismo_title", "Seismogram");
        add("gtna.ui.o.standard_model_title", "Standard Model");
        add("gtna.ui.o.committee_title", "Beam-Time Committee");
        add("gtna.ui.o.chord_title", "Harmonic Chord");
        add("gtna.ui.o.atlas_title", "Seed Atlas");
        add("gtna.ui.o.manual", "Field manual");
        add("gtna.ui.o.prev", "prev");
        add("gtna.ui.o.next", "next");
        add("gtna.ui.o.set_target", "Set target");
        add("gtna.ui.o.accuracy", "accuracy");
        add("gtna.ui.o.active", "active");
        add("gtna.ui.o.aim", "Aim");
        add("gtna.ui.o.all_done", "All proposals done");
        add("gtna.ui.o.ampl", "Ampl");
        add("gtna.ui.o.atlas_empty", "No seeds yet");
        add("gtna.ui.o.band_tier", "Band tier");
        add("gtna.ui.o.bank", "Bank");
        add("gtna.ui.o.barrel", "Barrel");
        add("gtna.ui.o.beam", "BEAM");
        add("gtna.ui.o.bench_bad", "Over budget");
        add("gtna.ui.o.bench_ok", "Bench valid");
        add("gtna.ui.o.best_r", "Best R");
        add("gtna.ui.o.biome", "Biome");
        add("gtna.ui.o.black_hole", "Black hole");
        add("gtna.ui.o.capsules", "capsules");
        add("gtna.ui.o.chord_hint1", "Click a recorded");
        add("gtna.ui.o.chord_hint2", "harmonic (max 5)");
        add("gtna.ui.o.closed", "CLOSED");
        add("gtna.ui.o.consonance", "Consonance");
        add("gtna.ui.o.crust_stress", "Crust stress");
        add("gtna.ui.o.damage", "Damage");
        add("gtna.ui.o.dark", "dark");
        add("gtna.ui.o.decoded", "decoded");
        add("gtna.ui.o.distance", "Distance");
        add("gtna.ui.o.done", "done");
        add("gtna.ui.o.dump", "DUMP");
        add("gtna.ui.o.efficiency", "efficiency");
        add("gtna.ui.o.extraction", "Extraction");
        add("gtna.ui.o.formed", "FORMED");
        add("gtna.ui.o.freq", "Freq");
        add("gtna.ui.o.hardness", "Hardness");
        add("gtna.ui.o.heat", "Heat");
        add("gtna.ui.o.helium", "Helium");
        add("gtna.ui.o.liner", "Liner");
        add("gtna.ui.o.lit", "lit");
        add("gtna.ui.o.loaded", "Loaded");
        add("gtna.ui.o.locked", "LOCKED");
        add("gtna.ui.o.mass", "Mass");
        add("gtna.ui.o.max_depth", "Max depth");
        add("gtna.ui.o.ms_pulsar", "Millisecond pulsar");
        add("gtna.ui.o.no_probe", "No Seismic Probe: quakes are not decoded");
        add("gtna.ui.o.no_slug", "No slug in the input bus");
        add("gtna.ui.o.note", "Harmonic");
        add("gtna.ui.o.open", "OPEN");
        add("gtna.ui.o.output", "Output");
        add("gtna.ui.o.phase", "Phase");
        add("gtna.ui.o.physics_run", "Physics run");
        add("gtna.ui.o.probe", "PROBE");
        add("gtna.ui.o.production_run", "Production run");
        add("gtna.ui.o.proposal", "Proposal");
        add("gtna.ui.o.pulsar", "Pulsar");
        add("gtna.ui.o.quench", "Quench");
        add("gtna.ui.o.rails", "rails");
        add("gtna.ui.o.ramp", "Ramp");
        add("gtna.ui.o.recorded", "Recorded");
        add("gtna.ui.o.resonance", "Resonance");
        add("gtna.ui.o.return", "Return");
        add("gtna.ui.o.rift_closed", "Rift closed");
        add("gtna.ui.o.rift_open", "Rift open");
        add("gtna.ui.o.seeds", "seeds");
        add("gtna.ui.o.spin_period", "spin period (ms, log)");
        add("gtna.ui.o.stability", "Stability");
        add("gtna.ui.o.survey", "survey");
        add("gtna.ui.o.target", "Target");
        add("gtna.ui.o.tuning", "TUNING");
        add("gtna.ui.o.yields", "Yields");
        add("gtna.ui.o.quake.micro", "Micro");
        add("gtna.ui.o.quake.micro.how", "steady extraction");
        add("gtna.ui.o.quake.crab", "Crab");
        add("gtna.ui.o.quake.crab.how", "vary the extraction");
        add("gtna.ui.o.quake.vela", "Vela");
        add("gtna.ui.o.quake.vela.how", "fast feeding");
        add("gtna.ui.o.quake.anti", "Anti");
        add("gtna.ui.o.quake.anti.how", "magnetar only");
        add("gtna.ui.o.quake.collapse", "Collapse");
        add("gtna.ui.o.quake.collapse.how", "cross the TOV edge");
        add("gtna.ui.o.ask.nb3sn_magnet", "5 fb, 7 TeV");
        add("gtna.ui.o.ask.vertex_detector", "charm 5σ");
        add("gtna.ui.o.ask.stochastic_cooling", "20 fb");
        add("gtna.ui.o.ask.cryo_penning", "1e13 p̄ / 40 fb");
        add("gtna.ui.o.ask.rebco_magnet", "W, Z 5σ");
        add("gtna.ui.o.ask.lepton_collider", "bottom 5σ");
        add("gtna.ui.o.ask.heavy_ions", "top 5σ");
        add("gtna.ui.o.ask.neutronium_magnet", "Higgs 5σ + Nx wire");
        add("gtna.ui.o.ask.beyond_standard_model", "X-Nexus 3σ");
        add("gtna.ui.o.slot.rail", "Rail");
        add("gtna.ui.o.slot.cooling", "Cooling");
        add("gtna.ui.o.slot.sensor", "Sensor");
        add("gtna.ui.o.slot.capsule", "Capsule");
        add("gtna.ui.o.slot.salvo", "Salvo");
        add("gtna.ui.o.part.rail_cu_nb", "CuNb");
        add("gtna.ui.o.part.rail_cu_nb.tip", "Copper-niobium rail: +2% efficiency, 40 t (up to 8)");
        add("gtna.ui.o.part.rail_superconductor", "SC rail");
        add("gtna.ui.o.part.rail_superconductor.tip", "Superconducting rail: +4%, 60 t; unlocked by Phobos");
        add("gtna.ui.o.part.rail_graphene", "Graphene");
        add("gtna.ui.o.part.rail_graphene.tip", "Graphene rail: +7%, 140 t; unlocked by Psyche");
        add("gtna.ui.o.part.cooling_helium", "Helium");
        add("gtna.ui.o.part.cooling_helium.tip", "Helium cooling: 2x heat capacity; unlocked by Ceres");
        add("gtna.ui.o.part.cooling_superconductor", "SC cool");
        add("gtna.ui.o.part.cooling_superconductor.tip", "Superconducting cooling: 4x; unlocked by Europa");
        add("gtna.ui.o.part.cooling_plasma_ice", "Plasma ice");
        add("gtna.ui.o.part.cooling_plasma_ice.tip", "Plasma ice cooling: 8x; unlocked by Arrokoth");
        add("gtna.ui.o.part.sensor_telescope", "Telescope");
        add("gtna.ui.o.part.sensor_telescope.tip", "Aim error x0.7; unlocked by the Moon");
        add("gtna.ui.o.part.sensor_interferometer", "Interfer.");
        add("gtna.ui.o.part.sensor_interferometer.tip", "Aim error x0.35; unlocked by Europa");
        add("gtna.ui.o.part.sensor_lens", "Lens");
        add("gtna.ui.o.part.sensor_lens.tip", "Aim error x0.175; unlocked by Arrokoth");
        add("gtna.ui.o.part.capsule_ablative", "Ablative");
        add("gtna.ui.o.part.capsule_ablative.tip", "Recovers 75%; unlocked by Ceres");
        add("gtna.ui.o.part.capsule_magnetic", "Magnetic");
        add("gtna.ui.o.part.capsule_magnetic.tip", "Recovers 85%; unlocked by Psyche");
        add("gtna.ui.o.part.capsule_fold", "Fold");
        add("gtna.ui.o.part.capsule_fold.tip", "Recovers 95%; unlocked by Nexus-1");
        add("gtna.ui.o.part.salvo_splitter", "Splitter");
        add("gtna.ui.o.part.salvo_splitter.tip", "Fires two slugs per shot; unlocked by Vesta");
        add("gtna.ui.o.slug.naquadah_alloy", "Naquadah alloy slug");
        add("gtna.ui.o.slug.trinium", "Trinium slug");
        add("gtna.ui.o.slug.neutronium", "Neutronium slug");
        add("gtna.ui.o.slug.cosmic_neutronium", "Cosmic neutronium slug");
        add("gtna.ui.o.slug.degenerate", "White dwarf matter slug");
        add("gtna.ui.o.slug.magnetar", "Magnetar Slug (Magnetarium)");
        add("gtna.machine.original.nexus_power", "Powered by the owner's Nexus wireless network");
        add("gtna.machine.kinetic_orbital_lance.computation_none", "§cNo optical computation hatch: the aim is blind");
        add("gtna.machine.kinetic_orbital_lance.computation_starved",
                "§eComputation hatch receives 0 CWU/t: link it to a transmitter of a running Network Switch/Supercomputer");
        add("gtna.machine.kinetic_orbital_lance.capsules", "Capsules in flight: §e%s");
        add("gtna.machine.kinetic_orbital_lance.bench", "Bench:");
        add("gtna.machine.kinetic_orbital_lance.bench_ok", "§aBench within budget");
        add("gtna.machine.kinetic_orbital_lance.bench_invalid", "§cBench over budget or locked part");
        add("gtna.machine.kinetic_orbital_lance.auto_on", "§a[Auto fire: on]");
        add("gtna.machine.kinetic_orbital_lance.auto_off", "§7[Auto fire: off]");
        add("gtna.machine.antimatter_collider_ring.particle.antiproton", "Antiprotons");
        add("gtna.machine.antimatter_collider_ring.particle.kaon", "Kaons");
        add("gtna.machine.antimatter_collider_ring.particle.lambda", "Lambda");
        add("gtna.machine.antimatter_collider_ring.particle.charm", "Charm");
        add("gtna.machine.antimatter_collider_ring.particle.bottom", "Bottom");
        add("gtna.machine.antimatter_collider_ring.particle.w_boson", "W boson");
        add("gtna.machine.antimatter_collider_ring.particle.z_boson", "Z boson");
        add("gtna.machine.antimatter_collider_ring.particle.higgs", "Higgs");
        add("gtna.machine.antimatter_collider_ring.particle.top", "Top");
        add("gtna.machine.antimatter_collider_ring.particle.x_nexus", "X(Nexus)");
        add("gtna.machine.antimatter_collider_ring.proposal.nb3sn_magnet", "Nb3Sn magnet test");
        add("gtna.machine.antimatter_collider_ring.proposal.vertex_detector", "Vertex detector");
        add("gtna.machine.antimatter_collider_ring.proposal.stochastic_cooling", "Stochastic cooling");
        add("gtna.machine.antimatter_collider_ring.proposal.cryo_penning", "Cryogenic Penning");
        add("gtna.machine.antimatter_collider_ring.proposal.rebco_magnet", "REBCO magnet");
        add("gtna.machine.antimatter_collider_ring.proposal.lepton_collider", "e+e- collisions");
        add("gtna.machine.antimatter_collider_ring.proposal.heavy_ions", "Heavy ions");
        add("gtna.machine.antimatter_collider_ring.proposal.neutronium_magnet", "Neutronium magnet");
        add("gtna.machine.antimatter_collider_ring.proposal.beyond_standard_model", "Beyond the Standard Model");
        add("gtna.machine.dimensional_rift_gate.biome.crystal_plains", "Crystal plains");
        add("gtna.machine.dimensional_rift_gate.biome.mercury_ocean", "Mercury ocean");
        add("gtna.machine.dimensional_rift_gate.biome.forge_world", "Forge world");
        add("gtna.machine.dimensional_rift_gate.biome.spore_forest", "Spore forest");
        add("gtna.machine.dimensional_rift_gate.biome.antimatter_abyss", "Antimatter abyss");
        add("gtna.machine.dimensional_rift_gate.biome.civilisation_relic", "Civilisation relic");
        add("gtna.machine.dimensional_rift_gate.biome.void", "Void");
        add("gtna.machine.kinetic_orbital_lance.body.moon", "Moon");
        add("gtna.machine.kinetic_orbital_lance.body.phobos", "Phobos");
        add("gtna.machine.kinetic_orbital_lance.body.vesta", "Vesta");
        add("gtna.machine.kinetic_orbital_lance.body.ceres", "Ceres");
        add("gtna.machine.kinetic_orbital_lance.body.psyche", "Psyche");
        add("gtna.machine.kinetic_orbital_lance.body.europa", "Europa");
        add("gtna.machine.kinetic_orbital_lance.body.arrokoth", "Arrokoth");
        add("gtna.machine.kinetic_orbital_lance.body.nexus_1", "Nexus-1");
        add("block.gtna.degenerate_matter_core", "Degenerate Matter Core");
        add("gtna.machine.stellar_containment_chamber.lit", "§bStar lit");
        add("gtna.machine.stellar_containment_chamber.dark", "§7Star dark: the degenerate core must be complete");
        add("gtna.machine.stellar_containment_chamber.mass", "Mass: §e%s M☉");
        add("gtna.machine.stellar_containment_chamber.period", "Spin period: §e%s ms");
        add("gtna.machine.stellar_containment_chamber.kepler", "Break-up period: §c%s ms");
        add("gtna.machine.stellar_containment_chamber.bands", "Band tier: §e%s");
        add("gtna.machine.stellar_containment_chamber.damage", "Containment damage: §c%s%%");
        add("gtna.machine.stellar_containment_chamber.output", "Output: §a%s EU/t");
        add("gtna.machine.stellar_containment_chamber.setpoint", "Extraction: 2^%s EU/t");
        add("gtna.machine.stellar_containment_chamber.magnetar_on", "§d[Magnetar field: on]");
        add("gtna.machine.stellar_containment_chamber.magnetar_off", "§7[Magnetar field: off]");
        add("gtna.machine.stellar_containment_chamber.black_hole", "§5Black hole: extracting from the ergosphere");
        add("config.gtna.option.itemGlowEdge", "Item Glow Edges");
        add("config.gtna.option.itemShaderEffects", "Item Shader Effects");
        add("config.gtna.option.itemEffectSpeed", "Item Effect Speed (%)");

        // Accelerate Hatch
        add("config.gtna.option.accelerateHatchMultiplier", "Accelerate Hatch Speed");
        add("config.gtna.option.accelerateHatchEnergyCost", "Accelerate Hatch Energy Cost");

        // Pattern Buffer mode auto-switch on GTCEu multiblocks
        add("config.gtna.option.bufferDrivenMachineMode", "Buffer Driven Machine Mode");

        // Wireless Steam
        add("config.gtna.option.wirelessSteamTransferRate", "Wireless Steam Transfer Rate");
        add("config.gtna.option.solarBoilerSteamPerCell", "Solar Boiler Steam Per Cell");
        add("config.gtna.option.bronzeInputBuffer", "Bronze Input Hatch Buffer");
        add("config.gtna.option.steelInputBuffer", "Steel Input Hatch Buffer");
        add("config.gtna.option.bronzeOutputBuffer", "Bronze Output Hatch Buffer");
        add("config.gtna.option.steelOutputBuffer", "Steel Output Hatch Buffer");

        // GTNL steam machine toggles
        add("config.gtna.option.steamCactusWonder", "Cactus Wonder");
        add("config.gtna.option.steamCracking", "Steam Cracker");
        add("config.gtna.option.megaSteamCompressor", "Steam Supercompressor");
        add("config.gtna.option.steamElevator", "Steam Elevator");
        add("config.gtna.option.steamElevatorModules", "Steam Elevator Modules");
        add("config.gtna.option.steamApiaryModule", "Steam Apiary Module");
        add("config.gtna.option.steamBeeBreedingModule", "Steam Bee Breeding Module");
        add("config.gtna.option.integratedOreProcessor", "Integrated Ore Processor");
        add("config.gtna.option.advancedIntegratedOreProcessor", "Advanced Integrated Ore Processor");
        add("config.gtna.option.brickKiln", "Brick Kiln");
        add("config.gtna.option.thermalPowerPump", "Thermal Power Pump");
        add("config.gtna.option.liquefactionFurnace", "Liquefaction Furnace");

        // Steam Elevator + its modules (GTNL port)
        add("block.gtna.steam_elevator", "Steam Elevator");
        add("gtna.machine.steam_elevator.steam", "Steam: %s mB");
        add("gtna.machine.steam_elevator.modules", "Modules: %s");
        add("gtna.machine.steam_elevator.steam_hatches", "Steam hatches: %s");
        add("gtna.machine.steam_elevator.no_modules", "No modules installed");
        add("gtna.machine.steam_elevator.set_out", "Set out");
        add("gtna.machine.steam_elevator.set_out.not_running", "The elevator must be running to set out.");

        add("gtna.machine.steam_elevator_module.tier", "Module tier: %s");
        add("gtna.machine.steam_elevator_module.upkeep", "Upkeep: %s mB/t | Own steam: %s mB");
        add("gtna.machine.steam_elevator_module.connected", "Connected to the elevator");
        add("gtna.machine.steam_elevator_module.working", "Working");
        add("gtna.machine.steam_elevator_module.not_working", "Not Working");
        add("gtna.machine.steam_elevator_module.disconnected", "Not connected");

        // Shared stat line shown on the module's own screen (not the item tooltip): the item
        // tooltips are the exact GTNL module lines, added per module below.
        add("gtna.machine.steam_elevator_module.upkeep", "Upkeep: %s mB/t | Own steam: %s mB");

        // Wireless steam network inspection command (/gtna steam)
        add("gtna.command.steam.balance", "§b[GTNA] §fWireless steam network §7(%s)§f: §b%s§f mB");
        add("gtna.command.steam.flow",
                "§b[GTNA] §7Flow since server start: §a+%s§7 mB in, §c-%s§7 mB out; §e%s§7 input hatch(es) with space");
        add("gtna.command.steam.hatches", "§b[GTNA] §fConnected wireless steam hatches: §e%s");
        add("gtna.command.steam.hatch_entry",
                "  §7- §f%s §7%s §f@ §7%s %s §7| §7tank §f%s§7/§f%s §7mB | §e%s §7mB/t | %s");
        add("gtna.command.steam.rate.unlimited", "unlimited");
        add("gtna.command.steam.no_hatches", "§b[GTNA] §7No connected wireless steam hatches.");
        add("gtna.command.steam.type.input", "Input");
        add("gtna.command.steam.type.output", "Output");
        add("gtna.command.steam.tier.bronze", "bronze");
        add("gtna.command.steam.tier.steel", "steel");
        add("gtna.command.steam.last.none", "§7no transfer yet");
        add("gtna.command.steam.last.push", "§apushed %s§7 mB (%s§7 t ago)");
        add("gtna.command.steam.last.pull", "§bpulled %s§7 mB (%s§7 t ago)");
        add("gtna.command.steam.not_player", "§c[GTNA] This command must be run by a player.");
        add("gtna.command.steam.added", "§b[GTNA] §fAdded §b%s§f mB; balance is now §b%s§f mB.");
        add("gtna.command.steam.set", "§b[GTNA] §fSet the balance to §b%s§f mB.");
        add("gtna.command.steam.add_failed", "§c[GTNA] Could not add that amount to the network.");

        // Wireless steam network HUD (client overlay, off by default; see ConfigHolder.Client)
        add("gtna.hud.wireless_steam.name", "Wireless Steam HUD");
        add("gtna.hud.wireless_energy.name", "Wireless Energy HUD");
        add("gtna.hud.wireless_energy.balance", "§bWireless Energy§7: §f%s§7 / §f%s §7EU");
        add("gtna.hud.wireless_energy.flow", "§7Flow: §a+%s§7 / §c-%s§7 EU/t");
        add("gtna.hud.wireless_energy.connections", "§7Connections: §f%s");
        add("gtna.machine.wireless_energy.hud.toggle", "Toggle the wireless energy HUD");
        add("gtna.machine.wireless_energy.hud.editor", "Right click to move the HUD");
        add("gtna.hud.wireless_steam.balance", "§bWireless Steam§7: §f%s §7mB");
        add("gtna.hud.wireless_steam.flow", "§7Flow: §a+%s§7 / §c-%s§7 mB/s");
        add("gtna.hud.wireless_steam.hatches", "§7Hatches: §f%s §7drain / §f%s §7feed");
        add("gtna.hud.editor.title", "HUD Editor");
        add("gtna.hud.editor.hint", "Drag the HUD to move it; the position is saved automatically. ESC closes.");
        add("gtna.hud.editor.toggle", "Wireless Steam HUD: %s");
        add("gtna.hud.editor.on", "ON");
        add("gtna.hud.editor.off", "OFF");
        add("gtna.machine.wireless_steam.hud.toggle", "Toggle the wireless steam HUD");
        add("gtna.machine.wireless_steam.hud.editor", "Right click to move the HUD");

        elevatorModuleTiers("steam_elevator_flight_module", "Steam Flight Module");

        elevatorModuleTiers("steam_elevator_weather_module", "Steam Weather Module");

        add("block.gtna.steam_elevator_greenhouse_module", "Steam Greenhouse Planting Module");

        add("block.gtna.steam_elevator_oil_drill_module_i", "Steam Oil Drill Module I");
        add("block.gtna.steam_elevator_oil_drill_module_ii", "Steam Oil Drill Module II");
        add("block.gtna.steam_elevator_oil_drill_module_iii", "Steam Oil Drill Module III");

        elevatorModuleTiers("steam_elevator_entity_crusher_module", "Steam Entity Crusher Module");

        add("block.gtna.steam_elevator_ore_processor_module", "Steam Ore Processing Module");

        add("block.gtna.steam_elevator_monster_repellent_module_i", "Steam Monster Repellator Module I");
        add("block.gtna.steam_elevator_monster_repellent_module_ii", "Steam Monster Repellator Module II");
        add("block.gtna.steam_elevator_monster_repellent_module_iii", "Steam Monster Repellator Module III");

        add("block.gtna.steam_elevator_beacon_module_i", "Steam Elevator Beacon Module I");
        add("block.gtna.steam_elevator_beacon_module_ii", "Steam Elevator Beacon Module II");
        add("block.gtna.steam_elevator_beacon_module_iii", "Steam Elevator Beacon Module III");

        add("block.gtna.steam_elevator_apiary_module", "Steam-Powered Apiary Module");

        add("block.gtna.steam_elevator_bee_breeding_module", "Steam Bee Breeding Module");

        add("config.gtna.option.eyeOfWood", "Eye of Wood");

        // Void Miner - Tier 1 (Dense)
        add("config.gtna.option.voidMinerDenseOutputMult", "Void Miner (Dense) Output");
        add("config.gtna.option.voidMinerDenseSpeedMult", "Void Miner (Dense) Speed");
        add("config.gtna.option.voidMinerDenseEnergyMult", "Void Miner (Dense) Energy");

        // Void Miner - Tier 2 (SuperHeated)
        add("config.gtna.option.voidMinerSuperHeatedOutputMult", "Void Miner (SuperHeated) Output");
        add("config.gtna.option.voidMinerSuperHeatedSpeedMult", "Void Miner (SuperHeated) Speed");
        add("config.gtna.option.voidMinerSuperHeatedEnergyMult", "Void Miner (SuperHeated) Energy");

        // Void Miner - Tier 3 (Insanely)
        add("config.gtna.option.voidMinerInsanelyOutputMult", "Void Miner (Insanely) Output");
        add("config.gtna.option.voidMinerInsanelySpeedMult", "Void Miner (Insanely) Speed");
        add("config.gtna.option.voidMinerInsanelyEnergyMult", "Void Miner (Insanely) Energy");
        add("config.gtna.option.baseLossPercent", "Base Loss Percent");
        add("config.gtna.option.maxTransferTierMAX", "MAX Tier Transfer Limit");
        add("config.gtna.option.alertCooldownTicks", "Alert Cooldown");
        add("config.gtna.option.useHighestTierForEfficiency", "Use Highest Tier For Efficiency");
        // Jade builds one config entry per registered data provider and asserts the translation
        // exists (config.jade.plugin_<namespace>.<provider uid path>); a missing one crashes the dev
        // client with 'Missing config translation'. Keep these in sync with GTNAJadePlugin.
        add("config.jade.plugin_gtna.multiple_recipes_provider", "Multiple Recipes Machine Info");
        add("config.jade.plugin_gtna.isa_mill_status", "ISA Mill Status");
        add("config.jade.plugin_gtna.void_miner_random", "Void Miner Random Chances");
        add("config.jade.plugin_gtna.block_stats", "Block Hardness and Blast Resistance");
        add("config.jade.plugin_gtna.gto_status", "GTO Machine Status");
        add("config.jade.plugin_gtna.me_pattern_buffer", "ME Pattern Buffer Info");
        add("config.jade.plugin_gtna.solar_boiler_provider", "Large Steam Solar Boiler Info");
        add("config.jade.plugin_gtna.wireless_steam_network", "Wireless Steam Network Info");
        add("gtna.jade.wireless_steam.balance", "Network: %s mB");
        add("gtna.jade.wireless_steam.tank", "Hatch Tank: %s / %s mB");
        add("gtna.jade.wireless_steam.last_push", "Last push: %s mB");
        add("gtna.jade.wireless_steam.last_pull", "Last pull: %s mB");
        add("gtna.jade.wireless_steam.idle", "No transfer yet");

        for (int i = 0; i < GTValues.V.length; i++) {
            String tierName = GTValues.VN[i];
            String tierLower = tierName.toLowerCase(Locale.ROOT);
            ChatFormatting color = (i < TextUtil.GTI_CORE$VC.length) ? TextUtil.GTI_CORE$VC[i] : ChatFormatting.WHITE;
            String colorCode = getColorCode(color);
            String coloredTierName = colorCode + tierName + "§r";
            if (i < GTNAMachines2.THREAD_HATCHES.length && GTNAMachines2.THREAD_HATCHES[i] != null) {
                add("block.gtna.thread_hatch_" + tierLower, coloredTierName + " Thread Hatch");
            }
            if (i < GTNAMachines2.ACCELERATE_HATCHES.length && GTNAMachines2.ACCELERATE_HATCHES[i] != null) {
                add("block.gtna.accelerate_hatch_" + tierLower, coloredTierName + " Accelerate Hatch");
            }
            if (i < GTNAMachines2.OVERCLOCK_HATCHES.length && GTNAMachines2.OVERCLOCK_HATCHES[i] != null) {
                add("block.gtna.overclock_hatch_" + tierLower, coloredTierName + " Overclock Hatch");
            }
            if (i < GTNAMachines2.OUTPUT_BOOST_HATCHES.length && GTNAMachines2.OUTPUT_BOOST_HATCHES[i] != null) {
                add("block.gtna.output_boost_hatch_" + tierLower, coloredTierName + " Output Boost Hatch");
            }
            if (i < GTNAMachines2.INFINITE_INPUT_BUSES.length && GTNAMachines2.INFINITE_INPUT_BUSES[i] != null) {
                add("block.gtna.infinite_input_bus_" + tierLower, coloredTierName + " Infinite Input Bus");
            }
            if (i < GTNAMachines2.INFINITE_INPUT_HATCHES.length && GTNAMachines2.INFINITE_INPUT_HATCHES[i] != null) {
                add("block.gtna.infinite_input_hatch_" + tierLower, coloredTierName + " Infinite Input Hatch");
            }
            if (i < GTNAMachines2.OUTPUT_BOOST_ITEM_BUSES.length && GTNAMachines2.OUTPUT_BOOST_ITEM_BUSES[i] != null) {
                add("block.gtna.output_boost_item_bus_" + tierLower, coloredTierName + " Output Boost Item Bus");
            }
            if (i < GTNAMachines2.OUTPUT_BOOST_FLUID_HATCHES.length &&
                    GTNAMachines2.OUTPUT_BOOST_FLUID_HATCHES[i] != null) {
                add("block.gtna.output_boost_fluid_hatch_" + tierLower, coloredTierName + " Output Boost Fluid Hatch");
            }
        }
    }

    private String getColorCode(ChatFormatting formatting) {
        if (formatting == null) return "§f";
        return switch (formatting) {
            case BLACK -> "§0";
            case DARK_BLUE -> "§1";
            case DARK_GREEN -> "§2";
            case DARK_AQUA -> "§3";
            case DARK_RED -> "§4";
            case DARK_PURPLE -> "§5";
            case GOLD -> "§6";
            case GRAY -> "§7";
            case DARK_GRAY -> "§8";
            case BLUE -> "§9";
            case GREEN -> "§a";
            case AQUA -> "§b";
            case RED -> "§c";
            case LIGHT_PURPLE -> "§d";
            case YELLOW -> "§e";
            case WHITE -> "§f";
            case OBFUSCATED -> "§k";
            case BOLD -> "§l";
            case STRIKETHROUGH -> "§m";
            case UNDERLINE -> "§n";
            case ITALIC -> "§o";
            case RESET -> "§r";
        };
    }
}
