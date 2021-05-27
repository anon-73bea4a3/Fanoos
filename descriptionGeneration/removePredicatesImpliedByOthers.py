

import config;
_LOCALDEBUGFLAG = config.debugFlags.get_v_print_ForThisFile(__file__);
    


from utils.contracts import *;

from boxesAndBoxOperations.getBox import isProperBox, getBox, getDimensionOfBox, getJointBox, getContainingBox, getRandomBox, boxSize, getRandomVectorInBox;

import z3;

from boxesAndBoxOperations.codeForGettingSamplesBetweenBoxes import getSampleVectorsToCheckAgainst, getBoxCenter;

from domainsAndConditions.baseClassConditionsToSpecifyPredictsWith import CharacterizationConditionsBaseClass,\
         Condition_TheBoxItself, MetaCondition_Conjunction;

import config;

def removePredicatesHelper_sytaxBasedFilterForRedundantConjunctions(thisCovering):
    requires(isinstance(thisCovering, list));
    requires(all([isinstance(x, CharacterizationConditionsBaseClass) for x in thisCovering]));
    # Below requires checks that none of the elements of thisCovering are repeats.
    requires(len(set([x.getID() for x in thisCovering])) == len([x.getID() for x in thisCovering]) );

    thisCoveringToReturn=[];

    def convertToFrozenSet(thisIDOrSetOfIDs):
         requires(isinstance(thisIDOrSetOfIDs, frozenset) or isinstance(thisIDOrSetOfIDs, str));
         valueToReturn = thisIDOrSetOfIDs if isinstance(thisIDOrSetOfIDs, frozenset) else frozenset([thisIDOrSetOfIDs]);
         ensures(isinstance(valueToReturn, frozenset));
         ensures( (thisIDOrSetOfIDs in valueToReturn) or (thisIDOrSetOfIDs == valueToReturn) );
         return valueToReturn;      

    idsAsFrozenSets = [convertToFrozenSet(x.getID()) for x in thisCovering];
    inverseIndex = sorted( range(0, len(thisCovering)), reverse=True, key=(lambda x: len(idsAsFrozenSets[x])));
    idsAsFrozenSets.sort(key=(lambda x: len(x)), reverse=True);
    assert(all([  idsAsFrozenSets[x] == \
                  convertToFrozenSet(thisCovering[inverseIndex[x]].getID()) \
                  for x in range(0, len(thisCovering)) ]));
    for indexA in range(0, len(thisCovering)):
        addThisElement = True;
        idConditionA = idsAsFrozenSets[indexA];
        assert(isinstance(idConditionA, frozenset));

        # In the iterator below, we go in descending index order - which means
        # the size of the set idsAsFrozenSets[indexB] is non-decreasing as the
        # iterator proceeds. This has a couple advantages, including the fact
        # that set-comparison operators tend to be faster when the sets 
        # involved are smaller.
        for indexB in range(len(thisCovering) -1 , indexA, -1): 
            idConditionB = idsAsFrozenSets[indexB];
            assert(isinstance(idConditionB, frozenset));

            # See the last requires and this inner-loop's iterator definition
            # for why the below assert should be true.
            assert(idConditionA != idConditionB);
            assert(len(idConditionA) >= len(idConditionB));
            if(len(idConditionA) == len(idConditionB)):
                # In this case we can break since the original list was sorted
                # in descending order by size of the ID sets and since the
                # iterator of this inner-loop is going in order of decreasing 
                # index. Thus, once this condition holds, we know any further
                # iteration of this inner-loop would just result in 
                # len(idConditionB) == len(idConditionA) .
                break;

            assert(len(idConditionA) > len(idConditionB));

            # We ignore the superset since the conjunct it represents is true
            # only a subset of the times the conjunct represented by the subset
            # is true.
            if(idConditionA.issuperset(idConditionB)):
                assert(\
                    convertToFrozenSet(thisCovering[inverseIndex[indexA]].getID()).issuperset( \
                        convertToFrozenSet(thisCovering[inverseIndex[indexB]].getID()) \
                    ) );
                addThisElement =  False;
                break;
        if(addThisElement):
            thisCoveringToReturn.append(thisCovering[inverseIndex[indexA]]);
    ensures({x.getID() for x in thisCovering}.issuperset({x.getID() for x in thisCoveringToReturn}));
    return thisCoveringToReturn;

def removePredicatesImpliedByOthers(coveringDescriptionsFiltered, \
    dictMappingConditionToBoxesItIsConsistentWith, listOfBoxes, \
    listMappingAxisIndexToVariableInQuestion, dictMappingConditionIDToVolumeCoveredAndUniqueVolumeCovered_initial):

    coveringDescriptionsFiltered = \
        removePredicatesHelper_sytaxBasedFilterForRedundantConjunctions(coveringDescriptionsFiltered)

    z3Solver = coveringDescriptionsFiltered[0].z3Solver;

    boxItselfConditionIDs = frozenset([x.getID() for x in coveringDescriptionsFiltered if \
        isinstance(x, Condition_TheBoxItself)]);
    conjunctionConditionIDs = frozenset([x.getID() for x in coveringDescriptionsFiltered if \
        isinstance(x, MetaCondition_Conjunction)]);
    assert(boxItselfConditionIDs.isdisjoint(conjunctionConditionIDs));
    otherPredicateIDs = frozenset([x.getID() for x in coveringDescriptionsFiltered if \
            not ((x.getID() in boxItselfConditionIDs) or (x.getID() in conjunctionConditionIDs))]); 
    assert(otherPredicateIDs.isdisjoint(boxItselfConditionIDs));
    assert(conjunctionConditionIDs.isdisjoint(otherPredicateIDs));

    orderToConsiderElements = [\
        sorted( list(x), \
            key=(lambda x: dictMappingConditionIDToVolumeCoveredAndUniqueVolumeCovered_initial[x][
                "uniqueVolumeCovered"] ) \
        )
        for x in [\
            boxItselfConditionIDs, conjunctionConditionIDs, otherPredicateIDs \
        ] \
    ];

    newDescription = [x.getID() for x in coveringDescriptionsFiltered];
    perminentSetOfBoxesToCheckOver = set([]);
    for thisListToConsider in orderToConsiderElements:
        for thisPredID in thisListToConsider:
            restOfPreds = [x for x in coveringDescriptionsFiltered if \
                ((x.getID() in newDescription) and (x.getID() != thisPredID))];
            assert(len(restOfPreds) == len(newDescription) -1 );
            boxesCoveredByThisPred = dictMappingConditionToBoxesItIsConsistentWith[thisPredID];
            setOfBoxesToCheckOver = perminentSetOfBoxesToCheckOver.union(boxesCoveredByThisPred);
            removeThisPred = True;
            for thisBoxIndex in setOfBoxesToCheckOver :
                verdict = checkIfPredicateRepetativeForThisBox(listOfBoxes[thisBoxIndex], restOfPreds, z3Solver, \
                    listMappingAxisIndexToVariableInQuestion);
                if( not verdict ): 
                    removeThisPred = False;
                    break;
            if(removeThisPred):
                assert(thisPredID in newDescription);
                newDescription.remove(thisPredID);
                assert(thisPredID not in newDescription);
                perminentSetOfBoxesToCheckOver = setOfBoxesToCheckOver;
                assert(boxesCoveredByThisPred.issubset(perminentSetOfBoxesToCheckOver));
  
    coveringDescriptionsFiltered = [x for x in coveringDescriptionsFiltered if (x.getID() in newDescription)];
    return coveringDescriptionsFiltered;


def _helper_getFunctionToCheckWhetherNoPointsInTheBoxStatisfyCondition_convertBoxToFormulaConstraints(listMappingAxisIndexToVariableInQuestion, thisBox):
    requires(isProperBox(thisBox));
    requires(getDimensionOfBox(thisBox) == len(listMappingAxisIndexToVariableInQuestion));
    F = z3.And([ \
        z3.And( float(thisBox[index, 0]) <= listMappingAxisIndexToVariableInQuestion[index], \
                listMappingAxisIndexToVariableInQuestion[index] <= float(thisBox[index, 1]) \
              ) \
        for index in range(0, len(listMappingAxisIndexToVariableInQuestion))     ]);
    return F;


from utils.quickResetZ3Solver import quickResetZ3Solver;

def checkIfPredicateRepetativeForThisBox(thisBox, restOfConditions, z3Solver, listMappingAxisIndexToVariableInQuestion):

    # TODO: split the two sections below into two functions...

    #V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V
    # for efficiency, some probabilistic checks to see if some quick random sampling
    # shows that the disjunction of the conditions fail to cover the whole box...
    #===========================================================================

    numberOfSamples=\
        config.defaultValues.numberOfStatisticalSamplesToTakeIn_numberOfStatisticalSamplesToTakeIn_getFunctionToCheckWhetherNoPointsInTheBoxStatisfyCondition

    for thisSampleIndex in range(0, numberOfSamples):
        randomVector = getRandomVectorInBox(thisBox).reshape(getDimensionOfBox(thisBox), 1);
        noConditionsHold = True;
        for thisCondition in restOfConditions:
            if(thisCondition.pythonFormatEvaluation(randomVector)):
                noConditionsHold = False;
                break;
        if(noConditionsHold):
            return False;
    #^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^

    #V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V
    # Formal check in the case that probabilistic sampling wasn't able to disprove
    # that the disjunction of the conditions to prove the statement...
    #===========================================================================

    quickResetZ3Solver(z3Solver); 

    # disjunctive normal form - each element in the list is a clause which we or-together....
    formulaToCheck = \
        (\
            z3.ForAll( listMappingAxisIndexToVariableInQuestion , \
                z3.Implies(\
                    _helper_getFunctionToCheckWhetherNoPointsInTheBoxStatisfyCondition_convertBoxToFormulaConstraints(\
                        listMappingAxisIndexToVariableInQuestion, thisBox), \
                    z3.Or([x.z3FormattedCondition for x in restOfConditions]) \
                ) \
            ) \
        );
    z3Solver.add(formulaToCheck);
    verdict = (z3Solver.check() == z3.z3.sat);
    quickResetZ3Solver(z3Solver);
    return verdict;
    #^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^




