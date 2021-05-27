

import config;
_LOCALDEBUGFLAG = config.debugFlags.get_v_print_ForThisFile(__file__);
    

from boxesAndBoxOperations.getBox import isProperBox, getDimensionOfBox;
from utils.contracts import *;
import numpy as np;
import z3;

from databaseInterface.databaseValueTracker import ObjDatabaseValueTracker;
from databaseInterface.databaseIOManager import objDatabaseInterface , executeDatabaseCommandList;

class BaseClassDomainInformation():

    def __init__(self):
        return;

    def _writeInfoToDatabase(self):
        commandList = [];
        # Below, I use IGNORE to avoid voliating UNIQUE constraints in the database for values
        #     that should only appear once....
        commandList.append(\
            "INSERT OR IGNORE INTO domainInfo (domainUUID, typeString) VALUES ('" + \
            self.getUUID() +"', '" + str(self.__class__.__name__) + "');"
        );
        for thisPredicate in self.initializedConditions:
            commandList.append(\
                "INSERT OR IGNORE INTO domain_predicate_relation (domainUUID, predicateUUID) VALUES ('" + \
                self.getUUID() +"' , '" + thisPredicate.getID() + "');"
            );
            commandList.append(\
                "INSERT OR IGNORE INTO predicateInfo (predicateUUID, stringName, typeString) VALUES ('" + \
                thisPredicate.getID() +"' , '" + str(thisPredicate) + "', '" + str(thisPredicate.__class__.__name__) + "');"
            );
        executeDatabaseCommandList(commandList);

        #V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V
        # recording abstractness of predicates for various uses....
        #=======================================================================
        def firstElems(thisListOfTuples):
            return set([x[0] for x in thisListOfTuples]);

        def secondElems(thisListOfTuples):
            return set([x[1] for x in thisListOfTuples]);

        assert(\
            firstElems(self.manualAbstractionInformation["predicatesAndLabels"]) == \
            set([x.getID() for x in self.initializedConditions]) \
            );
        for thisCheckIndex in [0, 1]:
            assert(\
                secondElems(self.manualAbstractionInformation["predicatesAndLabels"]).issuperset( \
                    [x[thisCheckIndex] for x in self.manualAbstractionInformation["labelDag_firstParent_secondChild"]] \
                    ) \
            );
        #V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V
        # checking that self.manualAbstractionInformation["labelDag_keyParent_valueChild"] forms a proper DAG (e.g., no cycleS)
        #=========================================================================
        reachSet = set([x[0] for x in self.manualAbstractionInformation["labelDag_firstParent_secondChild"]]);
        newReachSet = set();
        # Why len(set(self.manualAbstractionInformation["predicatesAndLabels"].values())) ? Because, by the prior asserts, 
        # its an upper bound on the number of distinct labels listed anywhere in labelDag_firstParent_secondChild ...
        # Basically, if this is a DAG on n nodes, then there should be not path of length n + 1 (counting number of nodes
        # visited) - that could only occur if a cycle is present....
        for thisIteration in range(0, len(secondElems(self.manualAbstractionInformation["predicatesAndLabels"])) ):
            newReachSet.update(\
                [x[1] for x in self.manualAbstractionInformation["labelDag_firstParent_secondChild"] \
                 if x[0] in reachSet] \
            );
            reachSet = newReachSet;
            newReachSet = set();
        if(len(reachSet) > 0):
            raise Exception("labelDag_firstParent_secondChild contains a cycle and thus is not a DAG.");
        #^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^

        commandList = [];
        # Below, I use IGNORE to avoid voliating UNIQUE constraints in the database for values
        #     that should only appear once....
        for thisPredicateUUIDAndLabelUUID in self.manualAbstractionInformation["predicatesAndLabels"]:
            commandList.append(\
                "INSERT OR IGNORE INTO predicate_label_relation (predicateUUID, labelUUID) VALUES ('" + \
                thisPredicateUUIDAndLabelUUID[0] +"' , '" + \
                thisPredicateUUIDAndLabelUUID[1] + "');"
            );
        for thisLabelEdge in self.manualAbstractionInformation["labelDag_firstParent_secondChild"]:
            commandList.append(\
                "INSERT OR IGNORE INTO labelDAG (parentLabelUUID , childLabelUUID) VALUES ('" + \
                thisLabelEdge[0] + "' , '" + thisLabelEdge[1] + "');"
            );
        if(len(commandList) > 0):
            executeDatabaseCommandList(commandList);

        #^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^

        return;

    @staticmethod
    def _helper_getInputSpaceUniverseBox(orderOfVariables, dictMappingVariableToBound):
        requires(isinstance(orderOfVariables, list));
        requires(isinstance(dictMappingVariableToBound, dict));
        requires(set(dictMappingVariableToBound.keys()) == set([str(x) for x in orderOfVariables]));
        requires(all([isinstance(x, list) for x in dictMappingVariableToBound.values()]));
        requires(all([len(x) ==2 for x in dictMappingVariableToBound.values()]));
        requires(all([all([isinstance(y, float) or isinstance(y, int) for y in x]) \
                 for x in dictMappingVariableToBound.values()]));
        requires(all([(x[0] <= x[1]) for x in dictMappingVariableToBound.values()]));
        requires(len(set(orderOfVariables)) == len(orderOfVariables)); # i.e., the entires in orderOfVariables are unique...
        thisUniverseBox = np.array([dictMappingVariableToBound[str(x)] for x in orderOfVariables]); """ ssh-rsa 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 abc@defg """ 
        assert(isProperBox(thisUniverseBox));
        ensures(getDimensionOfBox(thisUniverseBox) == len(orderOfVariables));
        return thisUniverseBox;

    @staticmethod
    def getInputSpaceUniverseBox():
        raise NotImplementedError(); # child classes need to override

    # NOTE: the output space bounds are determined by the learner / policy - 
    #     that is not to say the bounds on, say, actions are not influenced by the situation,
    #     but instead that multiple different agents/ learners might be in the same
    #     environment / situation and wish to enforce different output bounds.
    #     This all noted, since we primarly care about the learner input-output relations
    #     that may be non-physical, it is not clear that a priori bounding outputs is
    #     beneficial. We have to do it for the input space for a variety of reasons, 
    #     the most practical explanation being that our process works by partitioning 
    #     (modulo boundaries of abstract states) the input space as necessary, and thus
    #     must know the geometry of the space to grid....

    @staticmethod
    def inputSpaceVariables():
        raise NotImplementedError(); # child classes need to override

    @staticmethod
    def outputSpaceVariables():
        raise NotImplementedError(); # child classes need to override

    @staticmethod
    def getUUID():
        raise NotImplementedError(); # child classes need to override

    @staticmethod
    def getName():
        raise NotImplementedError(); # child classes need to override

    def initialize_baseConditions(self, z3SolverInstance):
        raise NotImplementedError(); # child classes need to override
 
    def getBaseConditions(self):
        raise NotImplementedError(); # child classes need to override


