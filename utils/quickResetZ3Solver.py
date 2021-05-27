

import config;
_LOCALDEBUGFLAG = config.debugFlags.get_v_print_ForThisFile(__file__);
    
import z3;
from utils.contracts import *;


def quickResetZ3Solver(z3Solver): 
    requires(isinstance(z3Solver, z3.z3.Solver));  # heavily relies on 
        # invariants upheld elsewhere in code.

    if(len(z3Solver.assertions()) > 1):
        raise Exception("Precondition for using this function violated, "+\
            "almost certainly due to a violation to invariants elsewhere in the code.");

    z3Solver.pop(); # return to previous back-tracking point
    assert(len(z3Solver.assertions()) == 0);
    z3Solver.push(); # create new back-tracking  point, necessary
       # for next time pop is called.
    ensures(len(z3Solver.assertions()) == 0);
    return; 
