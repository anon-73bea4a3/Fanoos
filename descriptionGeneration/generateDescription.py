

import config;
_LOCALDEBUGFLAG = config.debugFlags.get_v_print_ForThisFile(__file__);
    

import numpy as np;
import sys;
from utils.contracts import *;

from boxesAndBoxOperations.getBox import isProperBox, getBox, getDimensionOfBox, getJointBox, getContainingBox, getRandomBox, boxSize;

from statesAndOperatorsAndSelection.descriptionState import DescriptionState ;

import z3;

from boxesAndBoxOperations.codeForGettingSamplesBetweenBoxes import getSampleVectorsToCheckAgainst, getBoxCenter; 
from domainsAndConditions.baseClassConditionsToSpecifyPredictsWith import CharacterizationConditionsBaseClass,\
         Condition_TheBoxItself, MetaCondition_Conjunction;

from boxesAndBoxOperations.splitBox import splitBox;


from descriptionGeneration.draftCodeForMulitVariantConditionLearning import getApproximateMultivariateSetCover;

from boxesAndBoxOperations.mergeBoxes import mergeBoxes, \
                                             mergeBoxes_quadraticTime_usefulForOutputSpaceBoxes_mergeBoxesThatContainOneAnother_faster ;

import config;
from descriptionGeneration.removePredicatesImpliedByOthers  import removePredicatesImpliedByOthers ;



def getConsistentConditions(thisBox, listOfConditions, thisState):
    requires(isinstance(listOfConditions, list));
    requires(all([isinstance(x, CharacterizationConditionsBaseClass) for x in listOfConditions]));
    requires(isProperBox(thisBox));
    requires(isinstance(thisState, DescriptionState));

    numberOfSamplesToTry = thisState.readParameter("numberOfSamplesToTry");
    assert(isinstance(numberOfSamplesToTry, int));
    assert(numberOfSamplesToTry >= 0);


    indicesOfCandidateConditions = list(range(0, len(listOfConditions)));
    samplesToTry = getSampleVectorsToCheckAgainst(thisBox, 0.0, 1.0, numberOfSamplesToTry);
    indicesOfCandidateConditionsAfterFeasibilityCheck = [];
    for thisConditionIndex in indicesOfCandidateConditions:
        success = True;
        for thisSample in samplesToTry:
            verdict = listOfConditions[thisConditionIndex].pythonFormatEvaluation(thisSample);
            if(not verdict):
                success = False;
                break;
        if(success):
            indicesOfCandidateConditionsAfterFeasibilityCheck.append(thisConditionIndex);

    listOfConsistentCondtions = [];
    for thisConditionIndex in indicesOfCandidateConditionsAfterFeasibilityCheck:
        if(listOfConditions[thisConditionIndex].allMembersOfBoxSatisfyCondition(thisBox)):
            listOfConsistentCondtions.append(thisConditionIndex);

    return listOfConsistentCondtions;
        

def getMostSpecificCondition(thisBox, listOfConditions, thisState):
    """
    Given a list of predicates that are consistent with the box provided, randomly
    samples AROUND (not inside) the box provided to determine which of the predicates
    is most specific. In particular, we sample vectors at increasing distances from the 
    box (based on l_{infinity} norm from the closest box side) and whichever predicates
    become false first (i.e., at a certain "raduis" of sampling, a subset of the predicates
    is no longer consistent with the data sampled) are considered more specifically 
    consistent with the box in question. Bear in mind that this is a randomized approach, 
    so results may vary.
    """
    requires(isinstance(listOfConditions, list));
    requires(all([isinstance(x, CharacterizationConditionsBaseClass) for x in listOfConditions]));
    # Below is a sanity check- we want all the members of listOfConditions to be true over every element in 
    #     thisBox, so they should at least be true for the vector at the center of the box....
    requires(all([ x.pythonFormatEvaluation(getBoxCenter(thisBox)) for x in listOfConditions]));
    requires(isProperBox(thisBox));
    requires(isinstance(thisState, DescriptionState));

    numberOfSamplesToTry = thisState.readParameter("numberOfSamplesToTry");
    assert(isinstance(numberOfSamplesToTry, int));
    assert(numberOfSamplesToTry >= 0);
    exponentialComponent = thisState.readParameter("exponentialComponent");
    assert(isinstance(exponentialComponent, float));
    assert(exponentialComponent >= 0.0);

    numberOfDimensionToCover = getDimensionOfBox(thisBox);

    if(len(listOfConditions) == 0):
        return None;

    dimensionsCovered = set();

    minAndMaxInfinityNormPorportionOfDistanceFromBox = [\
        [1.0, 1.01], \
        [1.01,1.05], \
        [1.05, 1.10], \
        [1.10, 1.20], \
        [1.20, 1.40], \
        [1.40, 1.80], \
        [1.80, 2.60] ];
    for thisRowIndex in range(0, len(minAndMaxInfinityNormPorportionOfDistanceFromBox)):
        for columnIndex in [0, 1]:
            thisValue = minAndMaxInfinityNormPorportionOfDistanceFromBox[thisRowIndex][columnIndex];
            minAndMaxInfinityNormPorportionOfDistanceFromBox[thisRowIndex][columnIndex] = \
                thisValue * np.exp(exponentialComponent * thisValue);
    
    setOfIndicesOfCandidateMostSpecificValues = set();
    success=False;
    for thisMinAndMaxPorpDistance in minAndMaxInfinityNormPorportionOfDistanceFromBox:
        assert(thisMinAndMaxPorpDistance[0] >= 1.0);
        assert(thisMinAndMaxPorpDistance[0] < thisMinAndMaxPorpDistance[1]);
        samples = getSampleVectorsToCheckAgainst(thisBox, \
                      thisMinAndMaxPorpDistance[0], thisMinAndMaxPorpDistance[1], numberOfSamplesToTry);
        temp_newVariablesCovered = set();
        for thisIndex in range(0, len(listOfConditions)):
            if(thisIndex in setOfIndicesOfCandidateMostSpecificValues):
                continue;
            if(set(listOfConditions[thisIndex].relaventVariables()).issubset(dimensionsCovered)):
                continue;
            for thisSample in samples:
                if( (not listOfConditions[thisIndex].pythonFormatEvaluation(thisSample)) ): # and \
                    setOfIndicesOfCandidateMostSpecificValues.add(thisIndex);
                    temp_newVariablesCovered.update(listOfConditions[thisIndex].relaventVariables());
        # notice that we append in the new variables covered only AFTER we are done evaluating for candidate
        # conditions based on thisMinAndMaxPorpDistance. That way, conditions covering the same variables 
        # but in the same partition are both drawn in, as desired.
        dimensionsCovered.update(temp_newVariablesCovered)
        if(len(dimensionsCovered) == numberOfDimensionToCover):
            assert(len(setOfIndicesOfCandidateMostSpecificValues) > 0);
            return setOfIndicesOfCandidateMostSpecificValues;

    assert(len(dimensionsCovered) < numberOfDimensionToCover);
    if(len(setOfIndicesOfCandidateMostSpecificValues) != 0):
        assert(len(dimensionsCovered) > 0);
        return setOfIndicesOfCandidateMostSpecificValues;

    assert(setOfIndicesOfCandidateMostSpecificValues == set());
    return None;

def handleNewInstancesOf_MetaCondition_Conjunction(coveringDescriptions, dictMappingConditionToBoxesItIsConsistentWith):
    """
    updates dictMappingConditionToBoxesItIsConsistentWith to list the boxes that newly-introduced conjuncts are consistent with.
    """
    for thisConditionIndex in range(0, len(coveringDescriptions)):
        if(coveringDescriptions[thisConditionIndex].getID() in dictMappingConditionToBoxesItIsConsistentWith):
            continue; # Not 100% this is correct to do....
        if(isinstance(coveringDescriptions[thisConditionIndex], MetaCondition_Conjunction)):
            idsOfConjunctsInCondition = coveringDescriptions[thisConditionIndex].getID();
            assert(isinstance(idsOfConjunctsInCondition, frozenset));
            assert(len(idsOfConjunctsInCondition) > 0);
            assert( idsOfConjunctsInCondition not in dictMappingConditionToBoxesItIsConsistentWith);
            setOfBoxesThatConditionIsConsistentWith = None;
            for thisID in idsOfConjunctsInCondition:
                boxesConsistentWithThisID = dictMappingConditionToBoxesItIsConsistentWith[thisID].copy(); # CRITICAL TO USE .copy() HERE TO AVOID ACCIDENTALLY MODIFYING THE INFORMATION FOR THE ORIGINAL CONDTIONS USING THE intersection_update BELOW - NOTE THAT THE ORIGINAL CONIDITIONS CAN BE AND LIKLEY ARE IN USE ELSEWHERE....
                assert(isinstance(boxesConsistentWithThisID, set));
                assert(len(boxesConsistentWithThisID) > 0); # otherwise this condition would not be in the minimal covering.....
                if(setOfBoxesThatConditionIsConsistentWith == None):
                    setOfBoxesThatConditionIsConsistentWith = boxesConsistentWithThisID;
                else:
                    setOfBoxesThatConditionIsConsistentWith.intersection_update(boxesConsistentWithThisID);
                assert(isinstance(setOfBoxesThatConditionIsConsistentWith, set));
                assert(len(setOfBoxesThatConditionIsConsistentWith) > 0);
            assert(isinstance(setOfBoxesThatConditionIsConsistentWith, set));
            assert(len(setOfBoxesThatConditionIsConsistentWith) > 0);
            assert(idsOfConjunctsInCondition not in dictMappingConditionToBoxesItIsConsistentWith);
            dictMappingConditionToBoxesItIsConsistentWith[idsOfConjunctsInCondition] = setOfBoxesThatConditionIsConsistentWith;    
            assert(idsOfConjunctsInCondition in dictMappingConditionToBoxesItIsConsistentWith);
    return;


def handleNewInstancesOf_BoxItself(coveringDescriptionsFiltered, listOfConditions_after, listMappingAxisIndexToVariableInQuestion, dictMappingConditionToBoxesItIsConsistentWith):
    """
    Takes the description provided (coveringDescriptionsFiltered), and extracts occurances of 
    Condition_TheBoxItself. This function then produces a new description by removing the
    boxes from the original description and inserting new instances of Condition_TheBoxItself that
    result from merging the boxes extracted from the original description.
    """
    requires(isinstance(coveringDescriptionsFiltered, list));
    requires(all([isinstance(x, CharacterizationConditionsBaseClass) for x in coveringDescriptionsFiltered]));
    requires({x.getID() for x in coveringDescriptionsFiltered if not isinstance(x, MetaCondition_Conjunction)}.issubset({x.getID() for x in listOfConditions_after}));

    localMappingFromBoxIDToIndex = dict();
    localMappingFromBoxIDToBox = dict();
    for thisCondition in coveringDescriptionsFiltered:
        if( isinstance(thisCondition, Condition_TheBoxItself) ):
            # Notice that we do the copy below so that, when pop is done after, it does not
            # effect the original set in dictMappingConditionToBoxesItIsConsistentWith...
            indexes = dictMappingConditionToBoxesItIsConsistentWith[thisCondition.getID()].copy();
            assert(len(indexes) == 1);
            assert(isinstance(indexes, set));
            localMappingFromBoxIDToIndex[thisCondition.getID()] = indexes.pop();
            localMappingFromBoxIDToBox[thisCondition.getID()] = thisCondition.personalBox;
            assert(len(indexes) == 0);

    listOfCandidateBoxes = [thisCondition.personalBox for thisCondition in coveringDescriptionsFiltered \
                            if isinstance(thisCondition, Condition_TheBoxItself)];
    listOfConditions_after = [thisCondition for thisCondition in listOfConditions_after if not isinstance(thisCondition, Condition_TheBoxItself)];
    coveringDescriptionsFiltered = [thisCondition for thisCondition in coveringDescriptionsFiltered \
                            if not isinstance(thisCondition, Condition_TheBoxItself)];
    temp = mergeBoxes(listOfCandidateBoxes, precision=5, maxNumberOfIterations=None); 
    newMergedBoxes = list(temp["dictMappingIndexToBox"].values());
    newMergedBoxes =  mergeBoxes_quadraticTime_usefulForOutputSpaceBoxes_mergeBoxesThatContainOneAnother_faster(newMergedBoxes);

    temp = mergeBoxes(listOfCandidateBoxes, precision=5, maxNumberOfIterations=None); 

    newConditionsToAddIn = [\
        Condition_TheBoxItself(listOfConditions_after[0].z3Solver, thisBox, listMappingAxisIndexToVariableInQuestion) \
        for thisBox in newMergedBoxes]; # note that we have NOT set .listMappingPositionToVariableName for these new variables...
    for thisCondition in newConditionsToAddIn:
        listOfConditions_after.append(thisCondition);
        coveringDescriptionsFiltered.append(thisCondition);
        # Below is a bit of a hacky and slow way to do things - 
        # ideally we would keep track of this information when we did the original
        # merges - but it is a reasonable start subsequent to any extensive rewritting...
        dictMappingConditionToBoxesItIsConsistentWith[thisCondition.getID()] = \
            set([localMappingFromBoxIDToIndex[x] for x in localMappingFromBoxIDToIndex.keys() if 
                  thisCondition.allMembersOfBoxSatisfyCondition(localMappingFromBoxIDToBox[x]) ]); 

    assert({x.getID() for x in coveringDescriptionsFiltered if not isinstance(x, MetaCondition_Conjunction)}.issubset({x.getID() for x in listOfConditions_after}));
    return (coveringDescriptionsFiltered, listOfConditions_after, dictMappingConditionToBoxesItIsConsistentWith);



def getVolumesCoveredInformation(listOfBoxes, coveringDescriptionsFiltered, dictMappingConditionToBoxesItIsConsistentWith):
    requires( {x.getID() for x in coveringDescriptionsFiltered}.issubset(set(dictMappingConditionToBoxesItIsConsistentWith.keys())));
    #V~V~V~V~V~V~VV~V~VV~V~V~VV~V~V~VV~V~V~V~V~V~V~V~VV~V~VV~~V~V~V~V
    # Volumes covered information
    #----------------------------------------------------------------
    # Each member of coveringDescriptionsFiltered should uniquely cover at 
    # least on axis of at least one box, or else it would not have been selected 
    # in the approximal set covering...
    #================================================================
    listMappingFromBoxIndexToSetOfChosenConditionsCoveringIt = [set() for x in range(0, len(listOfBoxes))];
    for thisConditionIndex in range(0, len(coveringDescriptionsFiltered)):
        thisConditionID = coveringDescriptionsFiltered[thisConditionIndex].getID(); # this works as intended even when dealing with
            # instances of MetaCondition_Conjunction


        indicesOfBoxesCoveredByCondition = dictMappingConditionToBoxesItIsConsistentWith.get(thisConditionID, set());
        assert(thisConditionID in dictMappingConditionToBoxesItIsConsistentWith);
        assert( len(indicesOfBoxesCoveredByCondition) > 0);

        for thisBoxIndex in indicesOfBoxesCoveredByCondition:
            listMappingFromBoxIndexToSetOfChosenConditionsCoveringIt[thisBoxIndex].update([thisConditionID]);
            assert(thisConditionID in listMappingFromBoxIndexToSetOfChosenConditionsCoveringIt[thisBoxIndex]);

    dictMappingConditionIDToVolumeCoveredAndUniqueVolumeCovered = \
        {x.getID() : {"volumeCovered" : 0.0, "uniqueVolumeCovered" : 0.0} for x in coveringDescriptionsFiltered};
    totalVolumeOfBoxesInList = 0.0;
    for thisBoxIndex in range(0, len(listOfBoxes)):
        volumeOfThisBox = boxSize(listOfBoxes[thisBoxIndex]);
        assert((totalVolumeOfBoxesInList + volumeOfThisBox > totalVolumeOfBoxesInList) or np.isclose(volumeOfThisBox, 0.0));
        totalVolumeOfBoxesInList = totalVolumeOfBoxesInList + volumeOfThisBox; # Notice that since we do not ensure the boxes in the
            # list are disjoint, this sum is NOT necessarly the volume of the union of the boxes. However, since we do some merging of
            # the boxes prior to trying to describe them, it should be reasonable close or have a reasonable correspondance. It is not
            # overly important, it just provides a reasonable scaling - see the section below titled "normalizing results".
        conditionsCoveringBox = listMappingFromBoxIndexToSetOfChosenConditionsCoveringIt[thisBoxIndex]; 
        # NOTE: conditionsCoveringBox may be an empty set if the box was covered by an instance of Condition_TheBoxItself
        for thisCoveringBoxID in conditionsCoveringBox:
            assert("," not in thisCoveringBoxID);
            dictMappingConditionIDToVolumeCoveredAndUniqueVolumeCovered[thisCoveringBoxID]["volumeCovered"] = \
                dictMappingConditionIDToVolumeCoveredAndUniqueVolumeCovered[thisCoveringBoxID]["volumeCovered"] + volumeOfThisBox;
            if(len(conditionsCoveringBox) == 1): # TODO: improve this for the multi-dimensional cases (i.e., multi boxes, but each covering non-subset collections of variables)
                dictMappingConditionIDToVolumeCoveredAndUniqueVolumeCovered[thisCoveringBoxID]["uniqueVolumeCovered"] = \
                    dictMappingConditionIDToVolumeCoveredAndUniqueVolumeCovered[thisCoveringBoxID]["uniqueVolumeCovered"] + volumeOfThisBox;

    #V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V
    # Normalizing results
    #-----------------------------------------------------------------
    #=================================================================
    assert(totalVolumeOfBoxesInList >= 0.0);
    if(totalVolumeOfBoxesInList == 0.0):
        totalVolumeOfBoxesInList = 1.0;
    for thisKey in dictMappingConditionIDToVolumeCoveredAndUniqueVolumeCovered:
        for thisSubKey in ["volumeCovered", "uniqueVolumeCovered"]:
            dictMappingConditionIDToVolumeCoveredAndUniqueVolumeCovered[thisKey][thisSubKey] =  \
                dictMappingConditionIDToVolumeCoveredAndUniqueVolumeCovered[thisKey][thisSubKey] / totalVolumeOfBoxesInList;

    dictMappingConditionIDToVolumeCoveredAndUniqueVolumeCovered["totalVolumeOfBoxesInList"] = totalVolumeOfBoxesInList;
    #^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^

    #^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^
    return dictMappingConditionIDToVolumeCoveredAndUniqueVolumeCovered;




def getInitialListOfConditionsConsistentWithBoxes(\
        listOfBoxes, listOfConditions, listMappingAxisIndexToVariableInQuestion, thisState):  
    requires(isinstance(thisState, DescriptionState));
    requires(isinstance(listOfConditions, list));
    requires(all([isinstance(x, CharacterizationConditionsBaseClass) for x in listOfConditions]));
    requires(isinstance(listOfBoxes, list));
    requires(len(listOfBoxes) > 0);
    requires(all([isProperBox(thisBox) for thisBox in listOfBoxes]));
    requires(isinstance(listMappingAxisIndexToVariableInQuestion, list));
    requires(all([isinstance(x, z3.z3.ArithRef) for x in listMappingAxisIndexToVariableInQuestion]));
    requires(len(listMappingAxisIndexToVariableInQuestion) == getDimensionOfBox(listOfBoxes[0]));

    listOfConditions_after = listOfConditions.copy(); # see the condition where "if(len(consistentConditions) == 0):"
        # below for why this was necessary...

    dictMappingConditionToBoxesItIsConsistentWith = dict();
    listOfSetsCoveringBox = [];
    boxIndex = 0;
    for thisBox in listOfBoxes:
        consistentConditions = [listOfConditions[x] for x in \
            getConsistentConditions(thisBox, listOfConditions, thisState)  ];

        # below chunk is important for removing redundant (in respect to logical implication) predicates
        # at the end.
        for thisCondition in consistentConditions:
            thisConditionID = thisCondition.getID();
            if(thisConditionID not in dictMappingConditionToBoxesItIsConsistentWith):
                dictMappingConditionToBoxesItIsConsistentWith[thisConditionID] = set();
            dictMappingConditionToBoxesItIsConsistentWith[thisConditionID].add(boxIndex);
        assert(boxIndex + 1 > boxIndex); # weak overflow check....
        boxIndex = boxIndex + 1;

        subIndicesOfMostSpecificConsistentConditions = getMostSpecificCondition(\
                    thisBox, \
                    consistentConditions, \
                    thisState);

        if( (len(consistentConditions) == 0)  or ( subIndicesOfMostSpecificConsistentConditions == None  ) ):

            setOfConditionsCoveringThisBox = set();
            produceGreaterAbstraction = thisState.readParameter("produceGreaterAbstraction");
            assert(isinstance(produceGreaterAbstraction, bool));
            if(   (not produceGreaterAbstraction)  or (len(consistentConditions) == 0) ):
                thisConditionForBox = Condition_TheBoxItself(\
                    listOfConditions[0].z3Solver,thisBox, listMappingAxisIndexToVariableInQuestion); 
                listOfConditions_after.append(thisConditionForBox);

                # In the line below, we have boxIndex -1 because boxIndex was INCREMENTED prior to reaching
                #     here - the boxIndex corresponding to thisBox is thus (boxIndex -1)
                dictMappingConditionToBoxesItIsConsistentWith[thisConditionForBox.getID()] = set([boxIndex -1]);
                assert(boxIndex -1 >= 0);
                assert(boxIndex -1 < boxIndex); # though technically not possible in python integers, checking 
                    # integer arithmetic behavior.... though, given the assert prior, underflow should be impossible...

                setOfConditionsCoveringThisBox.update([thisConditionForBox.getID()]);
            else:
                setOfConditionsCoveringThisBox.update({x.getID() for x in consistentConditions});
            listOfSetsCoveringBox.append(setOfConditionsCoveringThisBox);
        else:
            mostSpecificConsistentConditions = [consistentConditions[x] for x in \
                                                subIndicesOfMostSpecificConsistentConditions];

            listOfSetsCoveringBox.append({x.getID() for x in mostSpecificConsistentConditions});

    return (listOfConditions_after, dictMappingConditionToBoxesItIsConsistentWith, listOfSetsCoveringBox);


import time;


def generateDescription(listOfBoxes, listOfConditions, listMappingAxisIndexToVariableInQuestion, thisState):
    requires(isinstance(listOfConditions, list));
    requires(all([isinstance(x, CharacterizationConditionsBaseClass) for x in listOfConditions]));
    requires(isinstance(listOfBoxes, list));
    requires(all([isProperBox(thisBox) for thisBox in listOfBoxes]));
    requires(isinstance(listMappingAxisIndexToVariableInQuestion, list));
    requires(all([isinstance(x, z3.z3.ArithRef) for x in listMappingAxisIndexToVariableInQuestion]));
    requires( len(listOfBoxes) == 0 or \
        len(listMappingAxisIndexToVariableInQuestion) == getDimensionOfBox(listOfBoxes[0]));
    requires(isinstance(thisState, DescriptionState));


    if(len(listOfBoxes) == 0):
        raise NotImplementedError("There is No Situation where the State of Affairs Asked-About Occurs "+ \
                                  "(in terms of mechanics, this means no boxes where found containing any elements "+\
                                  "that are applicable to your question).");
    assert(len(listOfBoxes)  > 0);

    (listOfConditions_after, dictMappingConditionToBoxesItIsConsistentWith, listOfSetsCoveringBox) = \
        getInitialListOfConditionsConsistentWithBoxes(\
            listOfBoxes, listOfConditions, listMappingAxisIndexToVariableInQuestion, thisState); 

    # Below two variables are for use in the set coverings.
    dimensionOfSpace = getDimensionOfBox(listOfBoxes[0]);
    dictMappingBElementsToConditions = {x.getID() : x for x in listOfConditions_after};
    for thisElem in dictMappingBElementsToConditions:
        if(isinstance(thisElem, frozenset)): # occurs in the case of an instance of MetaCondition_Conjunction
            for thisSubElem in thisElem:
                dictMappingBElementsToConditions[thisSubElem] = [x for x in listOfConditions_after if x.getID() == thisSubElem][0]; 

    coveringDescriptionsInitial = getApproximateMultivariateSetCover(listOfSetsCoveringBox, dimensionOfSpace, dictMappingBElementsToConditions);
    assert(isinstance(coveringDescriptionsInitial, list));
    
    coveringDescriptionsFiltered = set(); # coveringDescriptionsInitial.copy();
    coveringDescriptionsInitial = list(coveringDescriptionsInitial);
    listOfConditions_after = listOfConditions_after + list(coveringDescriptionsInitial);

    handleNewInstancesOf_MetaCondition_Conjunction(coveringDescriptionsInitial, dictMappingConditionToBoxesItIsConsistentWith)

    listMappingFromBoxIndexToSetOfChosenConditionsCoveringIt = [set() for x in range(0, len(listOfBoxes))];
    dictMappingBElementsToConditions = dict();
    forCheckPurposes_setOfBoxesCovered = set();
    for thisConditionIndex in range(0, len(coveringDescriptionsInitial)):
        thisConditionID = coveringDescriptionsInitial[thisConditionIndex].getID();
        dictMappingBElementsToConditions[thisConditionID] = coveringDescriptionsInitial[thisConditionIndex];
        indicesOfBoxesCoveredByCondition = dictMappingConditionToBoxesItIsConsistentWith[thisConditionID];
        assert(len(indicesOfBoxesCoveredByCondition) > 0); # otherwise it should not be in the minimal set covering 
            # description...
        assert(isinstance(indicesOfBoxesCoveredByCondition, set));
        forCheckPurposes_setOfBoxesCovered.update(indicesOfBoxesCoveredByCondition);
        assert(forCheckPurposes_setOfBoxesCovered.issuperset(indicesOfBoxesCoveredByCondition));
        for thisBoxIndex in indicesOfBoxesCoveredByCondition:
            listMappingFromBoxIndexToSetOfChosenConditionsCoveringIt[thisBoxIndex].update([thisConditionID]);
            assert(thisConditionID in listMappingFromBoxIndexToSetOfChosenConditionsCoveringIt[thisBoxIndex]);
    assert(forCheckPurposes_setOfBoxesCovered == {x for x in range(0, len(listOfBoxes))}); # ssh-rsa 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 abc@defg


    for thisElem in listOfConditions:
        dictMappingBElementsToConditions[thisElem.getID()] = thisElem;
    coveringDescriptionsFiltered = list(getApproximateMultivariateSetCover(\
            listMappingFromBoxIndexToSetOfChosenConditionsCoveringIt, dimensionOfSpace, dictMappingBElementsToConditions));
    listOfConditions_after = listOfConditions_after + list(coveringDescriptionsFiltered);
    handleNewInstancesOf_MetaCondition_Conjunction(coveringDescriptionsFiltered, dictMappingConditionToBoxesItIsConsistentWith)


    dictMappingConditionIDToVolumeCoveredAndUniqueVolumeCovered_initial = \
        getVolumesCoveredInformation(listOfBoxes, coveringDescriptionsFiltered, \
        dictMappingConditionToBoxesItIsConsistentWith);

    coveringDescriptionsFiltered = removePredicatesImpliedByOthers(\
        coveringDescriptionsFiltered, dictMappingConditionToBoxesItIsConsistentWith, \
        listOfBoxes, listMappingAxisIndexToVariableInQuestion, 
        dictMappingConditionIDToVolumeCoveredAndUniqueVolumeCovered_initial); 


    (coveringDescriptionsFiltered, listOfConditions_after, dictMappingConditionToBoxesItIsConsistentWith) = \
        handleNewInstancesOf_BoxItself( \
            coveringDescriptionsFiltered, listOfConditions_after, listMappingAxisIndexToVariableInQuestion,
            dictMappingConditionToBoxesItIsConsistentWith);


    dictMappingConditionIDToVolumeCoveredAndUniqueVolumeCovered = \
        getVolumesCoveredInformation(listOfBoxes, coveringDescriptionsFiltered, dictMappingConditionToBoxesItIsConsistentWith);


    assert(set(listOfConditions_after).issuperset(listOfConditions));

    ensures({x.getID() for x in coveringDescriptionsFiltered if not isinstance(x, MetaCondition_Conjunction)}.issubset({x.getID() for x in listOfConditions_after}));
    ensures({x.getID() for x in coveringDescriptionsFiltered}.union(set(["totalVolumeOfBoxesInList"])) == \
            set(dictMappingConditionIDToVolumeCoveredAndUniqueVolumeCovered.keys()));
    return {"description" : coveringDescriptionsFiltered, \
            "listOfConditions_after" : listOfConditions_after ,\
            "dictMappingConditionIDToVolumeCoveredAndUniqueVolumeCovered" : dictMappingConditionIDToVolumeCoveredAndUniqueVolumeCovered} ;


