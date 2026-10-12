package com.raishxn.gtna.common.machine.multiblock.electric.bec;

import com.gregtechceu.gtceu.api.capability.recipe.EURecipeCapability;
import com.gregtechceu.gtceu.api.capability.recipe.FluidRecipeCapability;
import com.gregtechceu.gtceu.api.capability.recipe.RecipeCapability;
import com.gregtechceu.gtceu.api.gui.fancy.ConfiguratorPanel;
import com.gregtechceu.gtceu.api.gui.widget.IntInputWidget;
import com.gregtechceu.gtceu.api.machine.IMachineBlockEntity;
import com.gregtechceu.gtceu.api.machine.feature.multiblock.IMultiPart;
import com.gregtechceu.gtceu.api.machine.trait.RecipeLogic;
import com.gregtechceu.gtceu.api.recipe.GTRecipe;
import com.gregtechceu.gtceu.api.recipe.RecipeHelper;
import com.gregtechceu.gtceu.api.recipe.content.Content;
import com.gregtechceu.gtceu.api.recipe.content.ContentModifier;
import com.gregtechceu.gtceu.api.recipe.modifier.ParallelLogic;
import com.gregtechceu.gtceu.utils.FormattingUtil;

import com.lowdragmc.lowdraglib.gui.widget.LabelWidget;
import com.lowdragmc.lowdraglib.gui.widget.WidgetGroup;
import com.lowdragmc.lowdraglib.syncdata.annotation.DescSynced;
import com.lowdragmc.lowdraglib.syncdata.annotation.Persisted;
import com.lowdragmc.lowdraglib.syncdata.field.ManagedFieldHolder;

import net.minecraft.ChatFormatting;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.nbt.Tag;
import net.minecraft.network.chat.Component;
import net.minecraft.world.level.material.Fluid;
import net.minecraftforge.fluids.FluidStack;

import com.raishxn.gtna.api.bec.CondensateList;
import com.raishxn.gtna.api.bec.CondensateStack;
import com.raishxn.gtna.api.bec.NaniteTier;
import com.raishxn.gtna.common.data.GTNARecipeType;
import com.raishxn.gtna.common.machine.multiblock.part.bec.IONodeControllerHatchPartMachine;
import com.raishxn.gtna.common.machine.multiblock.part.bec.LineOfSightHatchPartMachine;
import com.raishxn.gtna.common.machine.multiblock.part.bec.NaniteDetectorHatchPartMachine;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.util.*;

/**
 * GTNH {@code MTEBECIONode} (Bose-Einstein Condensate Teleportation Node). It runs Condensate Assembler recipes with
 * its own buses, linked by its Line-of-Sight connector to an Observation Array that supplies the EU, the nanites and
 * the condensate. Each item slot of a recipe has a nanite tier, and the duration is split into one step per slot;
 * to get through a step the array must provide that tier or higher. Every tick the node gains
 * {@code nanites / (parallels x 2^|provided - required| x max(slowdowns + 1, speed divisor))} ticks of progress.
 * Condensate is drawn from the network while crafting; a recipe still missing condensate at the end fails, and
 * more than three unrequested condensates in the network fail it at once. No overclock; parallels are set by the
 * min/max parameters.
 */
public class BECIONodeMachine extends BECMultiblockMachine {

    protected static final ManagedFieldHolder MANAGED_FIELD_HOLDER = new ManagedFieldHolder(
            BECIONodeMachine.class, BECMultiblockMachine.MANAGED_FIELD_HOLDER);

    /** Recipe data: ordinals of the {@link NaniteTier} of each item slot. */
    public static final String NANITE_TIERS = "bec_nanite_tiers";
    private static final String CONDENSATE = "bec_condensate";
    private static final String EUT = "bec_eut";

    /** Recipe data survives JSON as text, not as an int array. */
    public static String encodeTiers(int[] tiers) {
        StringBuilder out = new StringBuilder();
        for (int t : tiers) out.append(out.isEmpty() ? "" : ",").append(t);
        return out.toString();
    }

    public static int[] nanitesOf(CompoundTag data) {
        String text = data.getString(NANITE_TIERS);
        if (text.isEmpty()) return new int[0];
        return java.util.Arrays.stream(text.split(",")).mapToInt(Integer::parseInt).toArray();
    }

    public enum NodeState {
        Idle,
        Unpowered,
        AssemblerOffline,
        NaniteTierTooLow,
        PausedStep,
        PausedImmediate,
        Crafting,
        InternalError
    }

    public record RecipeStep(NaniteTier nanite, int start, int end, int index) {}

    @Persisted
    @DescSynced
    private int minParallel = 1;
    @Persisted
    @DescSynced
    private int maxParallel = Integer.MAX_VALUE;
    @Persisted
    @DescSynced
    private int speedDivisor = 1;
    @DescSynced
    private int state = NodeState.Idle.ordinal();
    @DescSynced
    private int slowdowns;
    @DescSynced
    private int requiredTierOrdinal = -1;
    private int subtickCounter;
    private int parallelRecipesInProgress;
    private long assemblerEUt;
    private boolean powered;
    @Nullable
    private CondensateList requiredCondensate, consumedCondensate;
    @Nullable
    private List<RecipeStep> recipeSteps;
    @Nullable
    private int[] requiredNanites;

    public BECIONodeMachine(IMachineBlockEntity holder, Object... args) {
        super(holder, args);
    }

    @Override
    public ManagedFieldHolder getFieldHolder() {
        return MANAGED_FIELD_HOLDER;
    }

    @Override
    protected boolean connectsToNetwork() {
        return false;
    }

    // ---- recipe search

    @Override
    protected RecipeLogic createRecipeLogic(Object... args) {
        return new NodeLogic();
    }

    @Override
    public boolean alwaysTryModifyRecipe() {
        return false;
    }

    /**
     * The recipe the node runs: no condensate fluid inputs (they come from the network, kept in the data) and no EU
     * (billed to the array, kept in the data), multiplied by the parallels the inputs allow up to the max parameter.
     */
    @Nullable
    GTRecipe prepare(GTRecipe recipe) {
        Map<RecipeCapability<?>, List<Content>> inputs = new HashMap<>(recipe.inputs);
        inputs.remove(FluidRecipeCapability.CAP);
        Map<RecipeCapability<?>, List<Content>> tickInputs = new HashMap<>(recipe.tickInputs);
        tickInputs.remove(EURecipeCapability.CAP);
        CompoundTag data = recipe.data.copy();
        CompoundTag condensate = new CompoundTag();
        for (Content content : recipe.getInputContents(FluidRecipeCapability.CAP)) {
            FluidStack[] stacks = FluidRecipeCapability.CAP.of(content.content).getStacks();
            if (stacks.length == 0) continue;
            var id = net.minecraftforge.registries.ForgeRegistries.FLUIDS.getKey(stacks[0].getFluid());
            if (id != null) condensate.putLong(id.toString(), stacks[0].getAmount());
        }
        data.put(CONDENSATE, condensate);
        data.putLong(EUT, recipe.getInputEUt().getTotalEU());
        GTRecipe trimmed = new GTRecipe(recipe.recipeType, recipe.id, inputs, recipe.outputs, tickInputs,
                recipe.tickOutputs, recipe.inputChanceLogics, recipe.outputChanceLogics,
                recipe.tickInputChanceLogics, recipe.tickOutputChanceLogics, recipe.conditions,
                recipe.ingredientActions, data, recipe.duration, recipe.recipeCategory, recipe.groupColor);
        if (!RecipeHelper.matchContents(this, trimmed).isSuccess()) return null;
        int parallel = ParallelLogic.getParallelAmountWithoutEU(this, trimmed, Math.max(1, maxParallel));
        if (parallel < minParallel) {
            RecipeLogic.putFailureReason(this, recipe, Component.translatable("gtna.bec.recipe.not_enough_parallels"));
            return null;
        }
        GTRecipe result = trimmed.copy(ContentModifier.multiplier(parallel), false);
        result.parallels = parallel;
        return result;
    }

    private class NodeLogic extends RecipeLogic {

        NodeLogic() {
            super(BECIONodeMachine.this);
        }

        @Override
        public @NotNull Iterator<GTRecipe> searchRecipe() {
            if (getAssembler() == null) {
                setWaiting(Component.translatable("gtna.bec.recipe.no_bec_assembler"));
                return Collections.emptyIterator();
            }
            List<GTRecipe> found = new ArrayList<>();
            for (GTRecipe recipe : allRecipes(GTNARecipeType.CONDENSATE_ASSEMBLER_RECIPES)) {
                GTRecipe prepared = prepare(recipe);
                if (prepared != null) {
                    found.add(prepared);
                    break;
                }
            }
            return found.iterator();
        }

        @Override
        public void handleRecipeWorking() {
            if (lastRecipe == null) return;
            incrementProgress(this);
            if (state == NodeState.Crafting.ordinal()) {
                setStatus(Status.WORKING);
                totalContinuousRunningTime++;
            } else if (isWorking()) {
                setWaiting(Component.translatable("gtna.bec.node_state." + NodeState.values()[state].name()));
            }
        }

        @Override
        public void onRecipeFinish() {
            if (lastRecipe != null && requiredCondensate != null && consumedCondensate != null) {
                for (var required : requiredCondensate.object2LongEntrySet()) {
                    long remaining = required.getLongValue() - consumedCondensate.getLong(required.getKey());
                    if (remaining > 0) {
                        failRecipe(Component.translatable("gtna.bec.recipe.missing_condensate",
                                condensateName(required.getKey()), FormattingUtil.formatNumbers(remaining)));
                        return;
                    }
                }
            }
            clearCurrentRecipe();
            super.onRecipeFinish();
        }

        int getProgressValue() {
            return progress;
        }

        void fail(Component reason) {
            interruptRecipe();
            lastRecipe = null;
            setWaiting(reason);
            setStatus(Status.IDLE);
        }
    }

    // ---- recipe state

    @Override
    public boolean beforeWorking(@Nullable GTRecipe recipe) {
        if (!super.beforeWorking(recipe) || recipe == null) return false;
        if (getAssembler() == null) return false;
        parallelRecipesInProgress = Math.max(1, recipe.parallels);
        requiredCondensate = new CondensateList();
        consumedCondensate = new CondensateList();
        CompoundTag condensate = recipe.data.getCompound(CONDENSATE);
        for (String key : condensate.getAllKeys()) {
            Fluid fluid = net.minecraftforge.registries.ForgeRegistries.FLUIDS.getValue(
                    new net.minecraft.resources.ResourceLocation(key));
            if (fluid != null) requiredCondensate.addTo(fluid, condensate.getLong(key) * parallelRecipesInProgress);
        }
        assemblerEUt = recipe.data.getLong(EUT) * parallelRecipesInProgress;
        requiredNanites = nanitesOf(recipe.data);
        loadRequiredNanites(recipe.duration, requiredNanites);
        subtickCounter = 0;
        state = NodeState.Crafting.ordinal();
        LineOfSightHatchPartMachine los = getLosHatch();
        if (los != null) los.setBeamActive(true);
        return true;
    }

    private void clearCurrentRecipe() {
        requiredCondensate = null;
        consumedCondensate = null;
        requiredNanites = null;
        recipeSteps = null;
        parallelRecipesInProgress = 0;
        assemblerEUt = 0;
        state = NodeState.Idle.ordinal();
        setRequiredTier(null);
        LineOfSightHatchPartMachine los = getLosHatch();
        if (los != null) los.setBeamActive(false);
    }

    private void failRecipe(Component reason) {
        clearCurrentRecipe();
        ((NodeLogic) getRecipeLogic()).fail(reason);
    }

    /** Assembler power failure (GTNH stops powered nodes on a critical shutdown). */
    void powerFail() {
        if (getRecipeLogic().getLastRecipe() == null) return;
        failRecipe(Component.translatable("gtna.bec.recipe.power_failure"));
    }

    @Override
    public void onStructureInvalid() {
        super.onStructureInvalid();
        clearCurrentRecipe();
    }

    /** Splits the duration into roughly equal steps, one per nanite (GTNH {@code IntDivisionIterator}). */
    public static List<RecipeStep> steps(int duration, int[] tiers) {
        List<RecipeStep> steps = new ArrayList<>();
        if (tiers.length == 0) tiers = new int[] { NaniteTier.Carbon.ordinal() };
        int remaining = duration, current = 0;
        for (int i = 0; i < tiers.length && remaining > 0; i++) {
            int bucketsLeft = tiers.length - i;
            int value = bucketsLeft == 1 ? remaining : Math.round(remaining / (float) bucketsLeft);
            remaining -= value;
            NaniteTier tier = NaniteTier.byOrdinal(tiers[i]);
            steps.add(new RecipeStep(tier == null ? NaniteTier.Carbon : tier, current, current + value, i));
            current += value;
        }
        return steps;
    }

    private void loadRequiredNanites(int duration, int[] tiers) {
        recipeSteps = steps(duration, tiers);
        setRequiredTier(recipeSteps.isEmpty() ? null : recipeSteps.get(0).nanite);
    }

    private @Nullable RecipeStep getCurrentStep(int progress) {
        if (recipeSteps == null) return null;
        for (RecipeStep step : recipeSteps) if (step.start <= progress && progress < step.end) return step;
        return null;
    }

    private @Nullable RecipeStep getNextProgressGate(int progress, @Nullable NaniteTier provided) {
        RecipeStep step = getCurrentStep(progress);
        if (step == null || provided == null) return null;
        int index = step.index;
        while (recipeSteps.get(index).nanite.tier <= provided.tier) {
            index++;
            if (index >= recipeSteps.size()) return null;
        }
        return recipeSteps.get(index);
    }

    private @Nullable RecipeStep getNextNaniteSwitch(int progress) {
        RecipeStep step = getCurrentStep(progress);
        if (step == null) return null;
        for (int i = step.index + 1; i < recipeSteps.size(); i++) {
            if (recipeSteps.get(i).nanite != step.nanite) return recipeSteps.get(i);
        }
        return null;
    }

    private void setRequiredTier(@Nullable NaniteTier tier) {
        requiredTierOrdinal = tier == null ? -1 : tier.ordinal();
        for (IMultiPart part : getParts())
            if (part instanceof NaniteDetectorHatchPartMachine detector) detector.setRequiredTier(tier);
    }

    /** GTNH {@code incrementProgressTime}. */
    private void incrementProgress(NodeLogic logic) {
        int progress = logic.getProgressValue();
        RecipeStep step = getCurrentStep(progress);
        if (step == null || requiredCondensate == null || consumedCondensate == null) {
            state = NodeState.InternalError.ordinal();
            return;
        }
        NaniteTier required = step.nanite;
        setRequiredTier(required);
        BECAssemblerMachine assembler = getAssembler();
        if (assembler == null || !assembler.isRunning()) {
            state = NodeState.AssemblerOffline.ordinal();
            return;
        }
        if (!powered) {
            state = NodeState.Unpowered.ordinal();
            return;
        }
        NaniteTier provided = assembler.getCurrentNaniteTier();
        int availableNanites = assembler.getAvailableNanites();
        if (provided == null || provided.tier < required.tier) {
            state = NodeState.NaniteTierTooLow.ordinal();
            return;
        }
        for (IONodeControllerHatchPartMachine controller : getControllerHatches()) {
            if (controller.getMode() == IONodeControllerHatchPartMachine.Mode.PAUSE_INSTANT &&
                    controller.receivingSignal()) {
                state = NodeState.PausedImmediate.ordinal();
                return;
            }
        }
        slowdowns = assembler.getSlowdowns(requiredCondensate.keySet());
        int aboveTierDivisor = 1 << Math.abs(required.tier - provided.tier);
        int slowdownDivisor = Math.max(slowdowns + 1, speedDivisor);
        int divisor = mulSafe(mulSafe(Math.max(1, parallelRecipesInProgress), aboveTierDivisor), slowdownDivisor);
        subtickCounter += availableNanites;
        int fullTicks = subtickCounter / divisor;
        subtickCounter -= fullTicks * divisor;
        int nextProgress = progress + fullTicks;
        RecipeStep gate = getNextProgressGate(progress, provided);
        if (gate != null) {
            if (nextProgress == gate.start) state = NodeState.NaniteTierTooLow.ordinal();
            nextProgress = Math.min(nextProgress, gate.start);
        }
        boolean pauseStep = false;
        for (IONodeControllerHatchPartMachine controller : getControllerHatches()) {
            if (controller.getMode() == IONodeControllerHatchPartMachine.Mode.PAUSE_STEP &&
                    controller.receivingSignal()) {
                pauseStep = true;
                break;
            }
        }
        if (pauseStep) {
            if (progress == step.start) {
                state = NodeState.PausedStep.ordinal();
                return;
            }
            if (step.index + 1 < recipeSteps.size()) {
                nextProgress = Math.min(nextProgress, recipeSteps.get(step.index + 1).start);
            }
        }
        if (slowdowns > 3) {
            failRecipe(Component.translatable("gtna.bec.recipe.bec_clogged"));
            return;
        }
        for (var e : requiredCondensate.object2LongEntrySet()) {
            long remaining = e.getLongValue() - consumedCondensate.getLong(e.getKey());
            if (remaining == 0) continue;
            CondensateStack request = new CondensateStack(e.getKey(), remaining);
            assembler.drainCondensate(request);
            consumedCondensate.addTo(e.getKey(), remaining - request.amount);
        }
        logic.setProgress(nextProgress);
        state = NodeState.Crafting.ordinal();
    }

    private static int mulSafe(int a, int b) {
        long r = (long) a * b;
        return r > Integer.MAX_VALUE ? Integer.MAX_VALUE : (int) r;
    }

    // ---- links

    @Nullable
    LineOfSightHatchPartMachine getLosHatch() {
        for (IMultiPart part : getParts()) if (part instanceof LineOfSightHatchPartMachine los) return los;
        return null;
    }

    public @Nullable BECAssemblerMachine getAssembler() {
        if (isRemote()) return null;
        LineOfSightHatchPartMachine los = getLosHatch();
        if (los == null) return null;
        var other = los.getConnectedHatch();
        return other != null && other.getOwnerMachine() instanceof BECAssemblerMachine assembler &&
                assembler.isFormed() ?
                        assembler : null;
    }

    private List<IONodeControllerHatchPartMachine> getControllerHatches() {
        List<IONodeControllerHatchPartMachine> out = new ArrayList<>();
        for (IMultiPart part : getParts()) if (part instanceof IONodeControllerHatchPartMachine c) out.add(c);
        return out;
    }

    public long getAssemblerEUt() {
        return assemblerEUt;
    }

    public void setPowered(boolean powered) {
        this.powered = powered;
    }

    public boolean isPowered() {
        return powered;
    }

    public NodeState getState() {
        return NodeState.values()[state];
    }

    public int getParallelRecipesInProgress() {
        return parallelRecipesInProgress;
    }

    public @Nullable CondensateList getRequiredCondensate() {
        return requiredCondensate;
    }

    public @Nullable CondensateList getConsumedCondensate() {
        return consumedCondensate;
    }

    public int getMinParallel() {
        return minParallel;
    }

    public void setMinParallel(int value) {
        minParallel = Math.max(1, value);
    }

    public int getMaxParallel() {
        return maxParallel;
    }

    public void setMaxParallel(int value) {
        maxParallel = Math.max(1, value);
    }

    public int getSpeedDivisor() {
        return speedDivisor;
    }

    /** Resets the subtick counter to avoid accumulating ticks (GTNH {@code SpeedDivisorParameter}). */
    public void setSpeedDivisor(int value) {
        speedDivisor = Math.max(1, value);
        subtickCounter = 0;
    }

    static Component describe(NaniteTier tier) {
        return Component.translatable("gtna.bec.gui.nanite_desc", tier.getStack().getHoverName(), tier.tier);
    }

    // ---- persistence

    @Override
    public void saveCustomPersistedData(@NotNull CompoundTag tag, boolean forDrop) {
        super.saveCustomPersistedData(tag, forDrop);
        if (requiredNanites != null) tag.putIntArray("nanites", requiredNanites);
        if (requiredCondensate != null) tag.put("required", requiredCondensate.save());
        if (consumedCondensate != null) tag.put("consumed", consumedCondensate.save());
        tag.putInt("parallels", parallelRecipesInProgress);
        tag.putLong("assemblerEUt", assemblerEUt);
        tag.putInt("subtick", subtickCounter);
    }

    @Override
    public void loadCustomPersistedData(@NotNull CompoundTag tag) {
        super.loadCustomPersistedData(tag);
        parallelRecipesInProgress = tag.getInt("parallels");
        assemblerEUt = tag.getLong("assemblerEUt");
        subtickCounter = tag.getInt("subtick");
        if (tag.contains("required")) {
            requiredCondensate = new CondensateList();
            requiredCondensate.load(tag.getCompound("required"));
        }
        if (tag.contains("consumed")) {
            consumedCondensate = new CondensateList();
            consumedCondensate.load(tag.getCompound("consumed"));
        }
        if (tag.contains("nanites", Tag.TAG_INT_ARRAY)) {
            requiredNanites = tag.getIntArray("nanites");
            var last = getRecipeLogic().getLastRecipe();
            loadRequiredNanites(last == null ? 1 : last.duration, requiredNanites);
            state = NodeState.Crafting.ordinal();
        }
    }

    // ---- GUI (GTNH MTEBECIONodeGui)

    @Override
    public void addDisplayText(List<Component> textList) {
        super.addDisplayText(textList);
        if (!isFormed()) return;
        textList.add(Component.translatable("gtna.bec.gui.ionode_status",
                Component.translatable("gtna.bec.node_state." + NodeState.values()[state].name())));
        BECAssemblerMachine assembler = getAssembler();
        NaniteTier provided = assembler == null ? null : assembler.getCurrentNaniteTier();
        textList.add(Component.translatable("gtna.bec.gui.provided_nanite", provided == null ?
                Component.translatable("gtna.bec.gui.none") :
                Component.translatable("gtna.bec.gui.nanite_count", describe(provided),
                        FormattingUtil.formatNumbers(assembler.getAvailableNanites()))));
        NaniteTier required = NaniteTier.byOrdinal(requiredTierOrdinal);
        textList.add(Component.translatable("gtna.bec.gui.required_nanite", required == null ?
                Component.translatable("gtna.bec.gui.none") : describe(required).copy()
                        .withStyle(ChatFormatting.GOLD)));
        if (getRecipeLogic().getLastRecipe() != null) {
            int progress = (int) Math.round(getRecipeLogic().getProgressPercent() *
                    getRecipeLogic().getMaxProgress());
            RecipeStep next = getNextNaniteSwitch(progress);
            textList.add(next == null ? Component.translatable("gtna.bec.gui.next_nanite_none") :
                    Component.translatable("gtna.bec.gui.next_nanite", describe(next.nanite).copy()
                            .withStyle(ChatFormatting.GOLD), next.start));
        }
        textList.add(Component.translatable("gtna.bec.gui.slowdowns", slowdowns).withStyle(ChatFormatting.GRAY));
        textList.add(Component.translatable("gtna.bec.gui.required_condensate"));
        if (requiredCondensate == null || consumedCondensate == null || requiredCondensate.isEmpty()) {
            textList.add(Component.literal("  ").append(Component.translatable("gtna.bec.gui.none")));
        } else {
            for (var e : requiredCondensate.object2LongEntrySet()) {
                textList.add(Component.translatable("gtna.bec.gui.remaining_condensate", condensateName(e.getKey()),
                        FormattingUtil.formatNumbers(consumedCondensate.getLong(e.getKey())),
                        FormattingUtil.formatNumbers(e.getLongValue())));
            }
        }
    }

    @Override
    public void attachConfigurators(ConfiguratorPanel panel) {
        super.attachConfigurators(panel);
        panel.attachConfigurators(new BECConfigurator("gtna.bec.gui.parameters", () -> {
            var group = new WidgetGroup(0, 0, 160, 96);
            group.addWidget(new LabelWidget(4, 4, "gtna.bec.gui.min_parallel"));
            group.addWidget(new IntInputWidget(4, 16, 152, 14, this::getMinParallel, this::setMinParallel).setMin(1));
            group.addWidget(new LabelWidget(4, 34, "gtna.bec.gui.max_parallel"));
            group.addWidget(new IntInputWidget(4, 46, 152, 14, this::getMaxParallel, this::setMaxParallel).setMin(1));
            group.addWidget(new LabelWidget(4, 64, "gtna.bec.gui.speed_divisor"));
            group.addWidget(new IntInputWidget(4, 76, 152, 14, this::getSpeedDivisor, this::setSpeedDivisor)
                    .setMin(1));
            return group;
        }));
    }
}
