package com.raishxn.gtna.common.data;

import com.gregtechceu.gtceu.GTCEu;
import com.gregtechceu.gtceu.api.data.RotationState;
import com.gregtechceu.gtceu.api.machine.MultiblockMachineDefinition;
import com.gregtechceu.gtceu.api.machine.multiblock.PartAbility;
import com.gregtechceu.gtceu.api.machine.multiblock.WorkableElectricMultiblockMachine;
import com.gregtechceu.gtceu.api.pattern.FactoryBlockPattern;
import com.gregtechceu.gtceu.api.pattern.TraceabilityPredicate;
import com.gregtechceu.gtceu.api.pattern.util.RelativeDirection;
import com.gregtechceu.gtceu.common.data.GTBlocks;
import com.gregtechceu.gtceu.common.data.GTMaterials;

import net.minecraft.world.level.block.Block;

import com.raishxn.gtna.GTNACORE;
import com.raishxn.gtna.common.data.multiblock.GTNAGTOPatterns;
import com.raishxn.gtna.common.data.multiblock.GTNAMultiBlockFileReader;
import com.raishxn.gtna.common.machine.multiblock.electric.HyperReactorMachine;
import com.tterrag.registrate.util.entry.BlockEntry;

import static com.gregtechceu.gtceu.api.pattern.Predicates.abilities;
import static com.gregtechceu.gtceu.api.pattern.Predicates.any;
import static com.gregtechceu.gtceu.api.pattern.Predicates.blocks;
import static com.gregtechceu.gtceu.api.pattern.Predicates.controller;
import static com.gregtechceu.gtceu.api.pattern.Predicates.frames;
import static com.raishxn.gtna.api.registry.GTNARegistry.REGISTRATE;

/**
 * The naquadah reactor ladder. Step 1, the Large Naquadah Reactor, is GTOCore's ({@code GeneratorMultiblock},
 * commit {@code dc4824d}) with its structure and fuels. Step 2, the Naquadah HyperReactor, is a GTNA original built
 * from the author's design ({@code pattern/naquadah_hyper_reactor.mbs}, made by
 * {@code tools/design/convert_naquadah_hyper_reactor.py}); it burns the same fuels at UEV and takes a booster plasma
 * through {@link HyperReactorMachine}.
 */
public final class GTNANaquadahReactors {

    private GTNANaquadahReactors() {}

    /** GTOCore texture (CC BY-NC-SA 4.0), connected through its _ctm sheet. */
    public static final BlockEntry<Block> EXTREME_STRENGTH_TRITANIUM_CASING = GTNABlocks
            .createCasingBlock("extreme_strength_tritanium_casing");

    /** GTO pattern of the Large Naquadah Reactor, read RIGHT, UP, BACK. */
    private static final String[][] LARGE_NAQUADAH_REACTOR_PATTERN = {
            { "                         ", "                         ", "                         ",
                    "                         ", "                         ", "                         ",
                    "                         ", "                         ", "                         ",
                    "                         ", "                         ", "                         ",
                    "           a~a           ", "                         ", "                         ",
                    "                         ", "                         ", "                         ",
                    "                         ", "                         ", "                         ",
                    "                         ", "                         ", "                         ",
                    "                         " },
            { "                         ", "                         ", "                         ",
                    "                         ", "                         ", "                         ",
                    "                         ", "                         ", "                         ",
                    "                         ", "                         ", "           AAA           ",
                    "          aBBBa          ", "           AAA           ", "                         ",
                    "                         ", "                         ", "                         ",
                    "                         ", "                         ", "                         ",
                    "                         ", "                         ", "                         ",
                    "                         " },
            { "                         ", "          CCCCC          ", "        CC     CC        ",
                    "      CC         CC      ", "    CC             CC    ", "    C               C    ",
                    "   C                 C   ", "   C                 C   ", "  C                   C  ",
                    "  C                   C  ", " C         AAA         C ", " C        A   A        C ",
                    " C       aB   Ba       C ", " C        A   A        C ", " C         AAA         C ",
                    "  C                   C  ", "  C                   C  ", "   C                 C   ",
                    "   C                 C   ", "    C               C    ", "    CC             CC    ",
                    "      CC         CC      ", "        CC     CC        ", "          CCCCC          ",
                    "                         " },
            { "          CCCCC          ", "        CC     CC        ", "      CC  CCCCC  CC      ",
                    "    CC  DD  C  DD  CC    ", "   C  DD    C    DD  C   ", "   C D             D C   ",
                    "  C D               D C  ", "  C D               D C  ", " C D        A        D C ",
                    " C D        A        D C ", "C C       AAAAA       C C", "C C      A E E A      C C",
                    "C CCC   aB E E Ba   CCC C", "C C      A E E A      C C", "C C       AAAAA       C C",
                    " C D        A        D C ", " C D        A        D C ", "  C D               D C  ",
                    "  C D               D C  ", "   C D             D C   ", "   C  DD    C    DD  C   ",
                    "    CC  DD  C  DD  CC    ", "      CC  CCCCC  CC      ", "        CC     CC        ",
                    "          CCCCC          " },
            { "          CCCCC          ", "        CC     CC        ", "      CC  DDFDD CCC      ",
                    "    CC  DDGCFCGDD  CC    ", "   C  DD  GCFCG  DD  C   ", "   C D    G F G    D C   ",
                    "  C D       F       D C  ", "  C D       F       D C  ", " C D       A A       D C ",
                    " C D       A A       D C ", "C DGGG    AA AA    GGGD C", "C DCC    A     A    CCD C",
                    "C DAAAAAAB     BAAAAAAD C", "C DCC    A     A    CCD C", "C DGGG    AA AA    GGGD C",
                    " C D       A A       D C ", " C D       A A       D C ", "  C D       F       D C  ",
                    "  C D       F       D C  ", "   C D    G F G    D C   ", "   CC DD  GCFCG  DD  C   ",
                    "    CC  DDGCFCGDD  CC    ", "      CC  DDFDD  CC      ", "        CC     CC        ",
                    "          CCCCC          " },
            { "          CCCCC          ", "        CC     CC        ", "      CC  CCCCC  CC      ",
                    "    CC  DD  C  DD  CC    ", "   C  DD    C    DD  C   ", "   C D             D C   ",
                    "  C D               D C  ", "  C D               D C  ", " C D        A        D C ",
                    " C D        A        D C ", "C C       AAAAA       C C", "C C      A E E A      C C",
                    "C CCC   aB E E Ba   CCC C", "C C      A E E A      C C", "C C       AAAAA       C C",
                    " C D        A        D C ", " C D        A        D C ", "  C D               D C  ",
                    "  C D               D C  ", "   C D             D C   ", "   CC DD    C    DD  C   ",
                    "    CC  DD  C  DD  CC    ", "      CC  CCCCC  CC      ", "        CC     CC        ",
                    "          CCCCC          " },
            { "                         ", "          CCCCC          ", "        CC     CC        ",
                    "      CC         CC      ", "    CC             CC    ", "    C               C    ",
                    "   C                 C   ", "   C                 C   ", "  C                   C  ",
                    "  C                   C  ", " C         AAA         C ", " C        A   A        C ",
                    " C       aB   Ba       C ", " C        A   A        C ", " C         AAA         C ",
                    "  C                   C  ", "  C                   C  ", "   C                 C   ",
                    "   C                 C   ", "    C               C    ", "    CC             CC    ",
                    "      CC         CC      ", "        CC     CC        ", "          CCCCC          ",
                    "                         " },
            { "                         ", "                         ", "                         ",
                    "                         ", "                         ", "                         ",
                    "                         ", "                         ", "                         ",
                    "                         ", "                         ", "           AAA           ",
                    "          aBBBa          ", "           AAA           ", "                         ",
                    "                         ", "                         ", "                         ",
                    "                         ", "                         ", "                         ",
                    "                         ", "                         ", "                         ",
                    "                         " },
            { "                         ", "                         ", "                         ",
                    "                         ", "                         ", "                         ",
                    "                         ", "                         ", "                         ",
                    "                         ", "                         ", "                         ",
                    "           aaa           ", "                         ", "                         ",
                    "                         ", "                         ", "                         ",
                    "                         ", "                         ", "                         ",
                    "                         ", "                         ", "                         ",
                    "                         " },
    };

    private static TraceabilityPredicate reactorHatches(TraceabilityPredicate casing) {
        return casing.or(abilities(PartAbility.IMPORT_FLUIDS).setMaxGlobalLimited(3).setPreviewCount(2))
                .or(abilities(PartAbility.MAINTENANCE).setExactLimit(1))
                .or(abilities(PartAbility.OUTPUT_ENERGY).setMaxGlobalLimited(1).setPreviewCount(1))
                .or(abilities(PartAbility.OUTPUT_LASER).setMaxGlobalLimited(1).setPreviewCount(0));
    }

    public static final MultiblockMachineDefinition LARGE_NAQUADAH_REACTOR = REGISTRATE
            .multiblock("large_naquadah_reactor", WorkableElectricMultiblockMachine::new)
            .rotationState(RotationState.ALL)
            .recipeType(GTNANaquadahRecipeTypes.LARGE_NAQUADAH_REACTOR_RECIPES)
            .generator(true)
            .appearanceBlock(GTNABlocks.HYPER_MECHANICAL_CASING)
            .pattern(definition -> GTNAGTOPatterns.aisles(FactoryBlockPattern.start(RelativeDirection.RIGHT,
                    RelativeDirection.UP, RelativeDirection.BACK), LARGE_NAQUADAH_REACTOR_PATTERN)
                    .where('~', controller(blocks(definition.get())))
                    .where('A', blocks(GTNABlocks.HYPER_MECHANICAL_CASING.get()))
                    .where('B', blocks(GTNABlocks.AMPROSIUM_GEARBOX.get()))
                    .where('C', blocks(EXTREME_STRENGTH_TRITANIUM_CASING.get()))
                    .where('D', blocks(GTBlocks.HIGH_POWER_CASING.get()))
                    .where('E', frames(GTMaterials.Naquadria))
                    .where('F', blocks(GTNABlocks.AMPROSIUM_PIPE_CASING.get()))
                    .where('G', frames(GTMaterials.Trinium))
                    .where('a', reactorHatches(blocks(GTNABlocks.HYPER_MECHANICAL_CASING.get())))
                    .where(' ', any())
                    .build())
            .workableCasingModel(GTNACORE.id("block/casings/hyper_mechanical_casing"),
                    GTCEu.id("block/multiblock/fusion_reactor"))
            .register();

    public static final MultiblockMachineDefinition NAQUADAH_HYPER_REACTOR = REGISTRATE
            .multiblock("naquadah_hyper_reactor", HyperReactorMachine::new)
            .rotationState(RotationState.NON_Y_AXIS)
            .recipeType(GTNANaquadahRecipeTypes.NAQUADAH_HYPER_REACTOR_RECIPES)
            .generator(true)
            .recipeModifiers(HyperReactorMachine::recipeModifier)
            .appearanceBlock(GTNABlocks.HYPER_MECHANICAL_CASING)
            .pattern(definition -> GTNAMultiBlockFileReader.start(definition, "naquadah_hyper_reactor")
                    .where('~', controller(blocks(definition.get())))
                    .where('A', blocks(GTNABlocks.HYPER_MECHANICAL_CASING.get()))
                    .where('B', reactorHatches(blocks(GTNABlocks.HYPER_MECHANICAL_CASING.get())))
                    .where('F', frames(GTMaterials.NaquadahAlloy))
                    .where('G', blocks(GTNABlocks.NAQUADAH_BOROSILICATE_GLASS.get()))
                    .where(' ', any())
                    .build())
            .workableCasingModel(GTNACORE.id("block/casings/hyper_mechanical_casing"),
                    GTCEu.id("block/multiblock/fusion_reactor"))
            .register();

    public static void init() {}
}
