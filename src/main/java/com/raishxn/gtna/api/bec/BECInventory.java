package com.raishxn.gtna.api.bec;

/** GTNH {@code BECInventory}: something that stores condensate in a BEC network. */
public interface BECInventory {

    CondensateList getContents();

    /** Max condensate this storage can hold; weights the split when condensate is injected. */
    double getCondensateCapacity();

    /** Adds the request's condensate and lowers {@code request.amount} by what was taken. */
    void addCondensate(CondensateStack request);

    /** Removes up to {@code request.amount} and lowers it by what was removed. */
    boolean removeCondensate(CondensateStack request);
}
