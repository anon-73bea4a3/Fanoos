

import config;
_LOCALDEBUGFLAG = config.debugFlags.get_v_print_ForThisFile(__file__);
    

from utils.contracts import *;
import numpy as np;

def distributionStatics(thisData):
    # unfortunately, some of the way this is used in the descriptionState (which I have
    #     to retro-fit this into) makes it hard to write requires that won't break.
    #     at the very least, thisData should be a single numerical value or some sort of 
    #     iterable which allows access to numerical items....    

    if(len(thisData) <= 0):
        return {"numberOfDataPoints" : 0};
        """
        ssh-rsa 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 abc@defg
        """
    else:
        return {\
            "numberOfDataPoints" : len(thisData),
            "sumOfValues" : np.sum(thisData, axis=0),
            "median" : np.median(thisData, axis=0), 
            "mean" : np.mean(thisData, axis=0),
            "std"  : np.std(thisData, axis=0),
            "min"  : np.min(thisData, axis=0),
            "max"  : np.max(thisData, axis=0),
            "0.05quantile" : np.quantile(thisData, 0.05, axis=0),
            "0.10quantile" : np.quantile(thisData, 0.10, axis=0),
            "0.25quantile" : np.quantile(thisData, 0.25, axis=0),
            "0.75quantile" : np.quantile(thisData, 0.75, axis=0),
            "0.90quantile" : np.quantile(thisData, 0.90, axis=0),
            "0.95quantile" : np.quantile(thisData, 0.95, axis=0),
        };       
    raise Exception("Control should not reach here");
    return;

