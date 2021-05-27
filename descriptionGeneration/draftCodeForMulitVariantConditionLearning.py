

import config;
_LOCALDEBUGFLAG = config.debugFlags.get_v_print_ForThisFile(__file__);
    

import pickle;
import numpy as np;
import sys;
from utils.contracts import *;

from boxesAndBoxOperations.getBox import isProperBox, getBox, getDimensionOfBox, getJointBox, getContainingBox, getRandomBox;

import uuid;


import re;

import struct;



from boxesAndBoxOperations.codeForGettingSamplesBetweenBoxes import getSampleVectorsToCheckAgainst, getBoxCenter; 
from domainsAndConditions.baseClassConditionsToSpecifyPredictsWith import CharacterizationConditionsBaseClass,\
         Condition_TheBoxItself, MetaCondition_Conjunction;  

import config;




# A : the list index - boxes...
# B : the elements in the sets - conditions...
def getApproximateMultivariateSetCover(listOfSets, dimensionOfSpace, dictMappingBElementsToConditions):
    requires(isinstance(listOfSets, list));
    requires(all([isinstance(x, set) for x in listOfSets]));
    requires(isinstance(dimensionOfSpace, int));
    requires(dimensionOfSpace > 0);
    requires(isinstance(dictMappingBElementsToConditions, dict));
    requires(all([listOfSets[x].issubset(list(dictMappingBElementsToConditions.keys())) \
        for x in range(0, len(listOfSets))])); # recomputing list(dictMappingBElementsToConditions.keys()) here is expensive,
        # and doing the subset check for each element is expensive....
    requires(all([isinstance(x, CharacterizationConditionsBaseClass) \
        for x in dictMappingBElementsToConditions.values()]));

    # NOTE: at the moment, dimensionOfSpace is not used, but I can see it potentially being useful. So, for now,
    #     assuming it is of minimum effort to provide, we leave it in as a required parameter in case it ultimately 
    #     proves to be useful for efficiency or decision making later.

    # This implements the greedy approximate solution to the 
    # set-cover problem, where the universe to cover is the 
    # indices of the list (i.e., list(range(0, len(listOfSets)))  )
    # https://en.wikipedia.org/wiki/Set_cover_problem 

    # The phrase "UsedToCover" in the below variable name is important: these are not
    # the boxes that the condition happens to cover, but the boxes that were present when it 
    # became the clear best decision to include this box in the results.
    forFinalResult_dictMappingBElementToAElementTheyWereUsedToCover = dict();

    dictMappingAToCoveringB = dict();
    dictMappingBElementsToAElementsTheyCover = dict();
    for thisIndex in range(0, len(listOfSets)):
        assert(thisIndex not in dictMappingAToCoveringB);
        dictMappingAToCoveringB[thisIndex] = listOfSets[thisIndex];
        for thisBElement in listOfSets[thisIndex]:
            if(thisBElement not in dictMappingBElementsToAElementsTheyCover):
                dictMappingBElementsToAElementsTheyCover[thisBElement] = set();
            assert(thisIndex not in dictMappingBElementsToAElementsTheyCover[thisBElement]);
            dictMappingBElementsToAElementsTheyCover[thisBElement].add(thisIndex);
            assert(thisIndex in dictMappingBElementsToAElementsTheyCover[thisBElement]);
        assert(thisIndex in dictMappingAToCoveringB);

    dictMappingAElementToVariablesCoveredForEachSet = {x : set() for x in dictMappingAToCoveringB};

    while(len(dictMappingAToCoveringB) > 0):
        maxCoveringBElement = None;
        AElementsCovered = set();
        for thisBElement in dictMappingBElementsToAElementsTheyCover:
            if(\
                (len(dictMappingBElementsToAElementsTheyCover[thisBElement]) > len(AElementsCovered)) or \
                (len(dictMappingBElementsToAElementsTheyCover[thisBElement]) == len(AElementsCovered) and np.random.rand() > 0.5) \
            ):
                maxCoveringBElement = thisBElement;
                AElementsCovered = dictMappingBElementsToAElementsTheyCover[thisBElement].copy();
        if(maxCoveringBElement not in forFinalResult_dictMappingBElementToAElementTheyWereUsedToCover):
            forFinalResult_dictMappingBElementToAElementTheyWereUsedToCover[maxCoveringBElement] =  set();
        forFinalResult_dictMappingBElementToAElementTheyWereUsedToCover[maxCoveringBElement].update(AElementsCovered);
        assert(maxCoveringBElement in forFinalResult_dictMappingBElementToAElementTheyWereUsedToCover);

        variablesCoveredByTheMaxElement = dictMappingBElementsToConditions[maxCoveringBElement].relaventVariables();
        assert(isinstance(variablesCoveredByTheMaxElement, frozenset));
        assert(len(variablesCoveredByTheMaxElement) > 0);

        for thisAElement in AElementsCovered:
            assert(thisAElement in dictMappingAToCoveringB); # ssh-rsa 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 abc@defg

            dictMappingAElementToVariablesCoveredForEachSet[thisAElement].update(variablesCoveredByTheMaxElement);
            assert(dictMappingAElementToVariablesCoveredForEachSet[thisAElement].issuperset(variablesCoveredByTheMaxElement));

            BElementsCoverThisAElement = dictMappingAToCoveringB[thisAElement].copy();

            assert(len(BElementsCoverThisAElement) > 0);
            assert(isinstance(BElementsCoverThisAElement, set));
            for thisBElement in BElementsCoverThisAElement:
                if(not dictMappingBElementsToConditions[thisBElement].relaventVariables().issubset(dictMappingAElementToVariablesCoveredForEachSet[thisAElement])):
                    continue; # make a dictionary mapping each box to the set of variables for it that have been covered.... 
                assert(thisAElement in dictMappingBElementsToAElementsTheyCover[thisBElement]);
                dictMappingBElementsToAElementsTheyCover[thisBElement].remove(thisAElement);
                assert(thisAElement not in dictMappingBElementsToAElementsTheyCover[thisBElement]);

                assert(thisBElement in dictMappingAToCoveringB[thisAElement]);
                dictMappingAToCoveringB[thisAElement].remove(thisBElement);
                assert(thisBElement not in dictMappingAToCoveringB[thisAElement]);

            if(len(dictMappingAToCoveringB[thisAElement]) == 0):
                BElementsCoverThisAElement = dictMappingAToCoveringB.pop(thisAElement);
                assert(BElementsCoverThisAElement == set());

    # The below note is the same as the one done for forFinalResult_dictMappingBElementToAElementTheyWereUsedToCover, 
    #     done for exactly the same reason...
    # The phrase "UsedToCover" in the below variable name is important: these are not
    # the boxes that the condition happens to cover, but the boxes that were present when it 
    # became the clear best decision to include this box in the results.
    forFinalResult_dictMappingAElementToBElementsThatWereUsedToCoverIt = {x : set() for x in range(0, len(listOfSets))} ;
    for thisBElement in forFinalResult_dictMappingBElementToAElementTheyWereUsedToCover:
        for thisAElement in forFinalResult_dictMappingBElementToAElementTheyWereUsedToCover[thisBElement]:
            forFinalResult_dictMappingAElementToBElementsThatWereUsedToCoverIt[thisAElement].add(thisBElement);
    setOfSetsOfBElementsToCouple = {frozenset(x) for x in forFinalResult_dictMappingAElementToBElementsThatWereUsedToCoverIt.values()};
    assert(all(len(x) > 0 for x in setOfSetsOfBElementsToCouple));
    
    finalListOfElementsToReturn = [];
    for thisSet in setOfSetsOfBElementsToCouple:
        assert(len(thisSet) > 0);
        tempA = set();
        for thisCondID in thisSet:
            if(isinstance(thisCondID, frozenset)):
                tempA.update(thisCondID);
            else:
                assert(isinstance(thisCondID, str));
                tempA.add(thisCondID);
        listOfConditionsWithIDsInThisSet = [ dictMappingBElementsToConditions[x] for x in tempA ];
        if(len(thisSet) == 1):
            finalListOfElementsToReturn.append( \
                listOfConditionsWithIDsInThisSet[0]  );
        else:
            assert(len(thisSet) > 1);                   
            finalListOfElementsToReturn.append( \
                MetaCondition_Conjunction(listOfConditionsWithIDsInThisSet));

    return finalListOfElementsToReturn;


