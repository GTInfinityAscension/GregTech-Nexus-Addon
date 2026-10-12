package com.raishxn.gtna.common.machine.multiblock.part.bec;

/** GTNH {@code ComparisonWithAnalog} (and {@code Comparison} without ANALOG) for the BEC detector hatches. */
public enum BECComparison {

    EQ("="),
    LT("<"),
    GT(">"),
    LTEQ("<="),
    GTEQ(">="),
    ANALOG("~");

    public final String symbol;

    BECComparison(String symbol) {
        this.symbol = symbol;
    }

    public boolean test(long actual, long configured) {
        return switch (this) {
            case EQ -> actual == configured;
            case LT -> actual < configured;
            case GT -> actual > configured;
            case LTEQ -> actual <= configured;
            case GTEQ -> actual >= configured;
            case ANALOG -> throw new UnsupportedOperationException();
        };
    }

    public BECComparison next(boolean allowAnalog) {
        BECComparison next = values()[(ordinal() + 1) % values().length];
        return !allowAnalog && next == ANALOG ? EQ : next;
    }

    public static BECComparison byOrdinal(int ordinal) {
        return ordinal >= 0 && ordinal < values().length ? values()[ordinal] : EQ;
    }
}
