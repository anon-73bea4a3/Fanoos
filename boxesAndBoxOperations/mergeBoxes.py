

import config;
_LOCALDEBUGFLAG = config.debugFlags.get_v_print_ForThisFile(__file__);
    

import pickle;
import numpy as np;
from boxesAndBoxOperations.getBox import *;

import config;

def boxesCanMergeWithNoGap(boxA, boxB):
    requires(isProperBox(boxA));
    requires(isProperBox(boxB));
    # if two boxes in n-dimensional space share 2 *(n-1) + 1 = 2n - 1  bounding coordinates (not necessarly serving
    # as the same role - ie, [a, b] and [b,c] are considered to share the "bounding coordinate" c) (out of the 2n they have), 
    # then they share a hyper-face and can merge. To see this, notice that the bounds only differ on one dimension, and
    # since there can only be one bounding-value different between the boxes, the boxes must touch on this dimension.
    # Thus, we can just take the smallest bound that contains the elements along the dimension where the boxes are different
    # then keep the rest of the dimensions the same, and we found a tight box holding them.
    # 
    # For example:
    #     boxA : [[x1, x2],
    #             [y1, y2], 
    #             [z1, z2]]
    #     boxB : [[x1, x2],
    #             [y1, y2'], 
    #             [z1, z2]]
    #     Since it must be that y1< y2 and y1 < y2' we see that one of the boxes actually must be contained in the other.
    # Another example:
    #     boxA : [[x1, x2],
    #             [y1, y2], 
    #             [z1, z2]]
    #     boxB : [[x1, x2],
    #             [y2, y3], 
    #             [z1, z2]]
    #     The union of these two boxes is exactly the box:
    #            [[x1, x2],
    #             [y1, y3], 
    #             [z1, z2]]
    #
   
    # Because of how the code calling this works - only checking corners - 
    # below would only ever trigger if the boxes share a face - in which 
    # case it is actually a less efficient version of the check that comes
    # after it... As such, I am commenting it out for now, but leaving in this
    # deadcode as minimal documentation of this fact and to show the idea
    # was evaluated then hit such a snag.

    indicesWhereDifferent = np.where(~np.isclose(boxA, boxB));
    assert(len(indicesWhereDifferent) == 2); # first coordinate: np.array with 
        # row-values of indices different, second coordinate: np.array with 
        # column-values of indices different
    if(len(indicesWhereDifferent[0]) <= 1):
        return True; # This is a degenerate case and not the main intent of this function...
    variablesDifferent = indicesWhereDifferent[0];
    numberOfVariablesDifferent = len(set(variablesDifferent));
    if(numberOfVariablesDifferent > 1):
        return False;
    variableDifferent = variablesDifferent[0]; # By the previous conditions, we know
        # that the list variablesDifferent must contain all the same element and
        # be non-empty - otherwise the code would have already returned. 
    if(np.isclose(boxB[variableDifferent, 1], boxA[variableDifferent, 0]) or \
       np.isclose(boxA[variableDifferent, 1], boxB[variableDifferent, 0])  ):
         return True; 

    return False;


def getAllRoughCornerPoints(thisBox, precision):
    # this function largely based on the function getInitialAbstraction_boxesBySign
    # from CEGARLikeAnalysis/CEGARLikeAnalysisMain.py
    requires(isProperBox(thisBox));
    numberOfCorners = 2 ** (thisBox.shape[0]);
    listToReturn = [];
    for thisCornerIndex in range(0, numberOfCorners):
        thisCorner = [];
        binaryRepresentationOfIndex = np.binary_repr(thisCornerIndex, width=getDimensionOfBox(thisBox));
        assert(isinstance(binaryRepresentationOfIndex, str));
        assert(all([(x in {"1", "0"}) for x in binaryRepresentationOfIndex]));
        for thisVariableIndex in range(0, getDimensionOfBox(thisBox)):
            valueToRecord = np.round(thisBox[thisVariableIndex, int(binaryRepresentationOfIndex[thisVariableIndex])], precision);
            thisCorner.append(float(valueToRecord)); # if I did not convert it to a float, it would be recorded
                # as a larger numpy-value, taking up more space....
        listToReturn.append(pickle.dumps(thisCorner));
    return listToReturn;


def getSetupDicts(listOfBoxes, precision=3):
    dictMappingIndexToBox = dict();
    dictMappingCornerToIDsOfBoxesWithThem = dict();
    dictMappingIDsOfBoxesToTheirCorners= dict();
    for thisBox in listOfBoxes:
        indexIDOfThisBox = len(dictMappingIndexToBox);
        sizeOfThisBox = boxSize(thisBox);
        dictMappingIndexToBox[indexIDOfThisBox] = thisBox;
        cornersOfThisBox = getAllRoughCornerPoints(thisBox, precision);
        cornersOfThisBox = list(set(cornersOfThisBox )); # making sure the corners we consider are unique,
            # even if the box is flat....
        dictMappingIDsOfBoxesToTheirCorners[indexIDOfThisBox] = cornersOfThisBox;
        for thisCorner in cornersOfThisBox:
            if(thisCorner not in dictMappingCornerToIDsOfBoxesWithThem):
                dictMappingCornerToIDsOfBoxesWithThem[thisCorner] = [];
            dictMappingCornerToIDsOfBoxesWithThem[thisCorner].append((sizeOfThisBox, indexIDOfThisBox));
    for thisKey in dictMappingCornerToIDsOfBoxesWithThem:
        # this list of boxes that have a certain corner are sorted in reverse order of size
        # so that we can try to aggressively try and greadily merge boxes...
        dictMappingCornerToIDsOfBoxesWithThem[thisKey] = \
            sorted(dictMappingCornerToIDsOfBoxesWithThem[thisKey], reverse=True);
    return {"dictMappingIndexToBox" : dictMappingIndexToBox, \
            "dictMappingCornerToIDsOfBoxesWithThem" : dictMappingCornerToIDsOfBoxesWithThem, \
            "dictMappingIDsOfBoxesToTheirCorners" : dictMappingIDsOfBoxesToTheirCorners};


def addBox(dictMappingIndexToBox, dictMappingCornerToIDsOfBoxesWithThem, \
    dictMappingIDsOfBoxesToTheirCorners, boxToAdd, precision=3):
    indexIDOfThisBox = max(dictMappingIndexToBox) ;
    assert(indexIDOfThisBox + 1 > indexIDOfThisBox); # weak overflow check...
    indexIDOfThisBox = indexIDOfThisBox + 1;
    sizeOfThisBox = boxSize(boxToAdd);
    dictMappingIndexToBox[indexIDOfThisBox] = boxToAdd;
    cornersOfThisBox = getAllRoughCornerPoints(boxToAdd, precision);
    cornersOfThisBox = list(set(cornersOfThisBox )); # making sure the corners we consider are unique,
        # even if the box is flat....
    dictMappingIDsOfBoxesToTheirCorners[indexIDOfThisBox] = cornersOfThisBox;
    for thisCorner in cornersOfThisBox:
        if(thisCorner not in dictMappingCornerToIDsOfBoxesWithThem):
            dictMappingCornerToIDsOfBoxesWithThem[thisCorner] = [];
        dictMappingCornerToIDsOfBoxesWithThem[thisCorner].append((sizeOfThisBox, indexIDOfThisBox));
        # this list of boxes that have a certain corner are sorted in reverse order (i.e., descending order)
        # of size so that we can try to aggressively try and greadily merge boxes...
        dictMappingCornerToIDsOfBoxesWithThem[thisCorner] = \
            sorted(dictMappingCornerToIDsOfBoxesWithThem[thisCorner], reverse=True);
    return indexIDOfThisBox;

def removeBox(dictMappingIndexToBox, dictMappingCornerToIDsOfBoxesWithThem, \
    dictMappingIDsOfBoxesToTheirCorners, IDNumberOfBoxToRemove, precision=3):

    cornersToSearchAndRemoveBoxFrom = dictMappingIDsOfBoxesToTheirCorners[IDNumberOfBoxToRemove];

    # removing record of this box
    dictMappingIndexToBox.pop(IDNumberOfBoxToRemove);
    dictMappingIDsOfBoxesToTheirCorners.pop(IDNumberOfBoxToRemove);

    for thisCorner in  cornersToSearchAndRemoveBoxFrom:
        index = 0;
        while(index < len(dictMappingCornerToIDsOfBoxesWithThem[thisCorner])):
            if(dictMappingCornerToIDsOfBoxesWithThem[thisCorner][index][1] == IDNumberOfBoxToRemove):
                dictMappingCornerToIDsOfBoxesWithThem[thisCorner].pop(index);
                if(len(dictMappingCornerToIDsOfBoxesWithThem[thisCorner]) == 0): # no box has this corner
                    dictMappingCornerToIDsOfBoxesWithThem.pop(thisCorner); 
                break; # recall that we inserted boxes into the dict ensuring that the
                    # the coordinates we got for each box are unique, even if the box is flat...
            assert(index < index + 1); # weak overflow check...
            index = index + 1;

        # below assert checks that the sorting order still remains. Note we must use .get for
        # the dict-access in the range since we might have gotten rid of the key thisCorner .
        assert(\
            all([ (dictMappingCornerToIDsOfBoxesWithThem[thisCorner][index][0] >= \
                   dictMappingCornerToIDsOfBoxesWithThem[thisCorner][index+1][0]) \
            for index in range(0, len(dictMappingCornerToIDsOfBoxesWithThem.get(thisCorner, [])) -1)]));

    return;


import sys;
from utils.contracts import *;

def mergeBoxesInTargetSet(dictMappingIndexToBox, dictMappingCornerToIDsOfBoxesWithThem, \
    dictMappingIDsOfBoxesToTheirCorners, cornerToExamine, precision=3):

    listOfIDsOfBoxesToMerge = dictMappingCornerToIDsOfBoxesWithThem.get(cornerToExamine, []); # NOTE: this means that
        # if boxes overlap but DO NOT share a corner, THEN THIS CODE WILL NEVER MERGE IT.

    thisFirstBoxIndex = 0;
    while(thisFirstBoxIndex < len(listOfIDsOfBoxesToMerge)):
        thisSecondBoxIndex = thisFirstBoxIndex + 1;
        while(thisSecondBoxIndex < len(listOfIDsOfBoxesToMerge)):
            thisFirstBoxID = listOfIDsOfBoxesToMerge[thisFirstBoxIndex][1];
            thisSecondBoxID = listOfIDsOfBoxesToMerge[thisSecondBoxIndex][1];
            if(boxesCanMergeWithNoGap(dictMappingIndexToBox[thisFirstBoxID], \
                                      dictMappingIndexToBox[thisSecondBoxID])):
                newBox = getContainingBox([dictMappingIndexToBox[thisFirstBoxID], \
                                           dictMappingIndexToBox[thisSecondBoxID]]);
                # NOTE: We MUST add in a box prior to removing others to prevent
                #     the mechanisms in add-box from (1) repeating an ID (this actually
                #     should not impact correctness, but I suppose it is nice... actually,
                #     that is silly), (2) make sure that we do not work over an 
                #     empty sequence in the list for that corner (... i.e., violate
                #     an invariant... that sounds more like a bug in the code than
                #     an issue with doing operations in a certain order)....
                addBox(dictMappingIndexToBox, dictMappingCornerToIDsOfBoxesWithThem, \
                    dictMappingIDsOfBoxesToTheirCorners, newBox, precision=precision);
                for thisIDToRemove in [thisFirstBoxID, thisSecondBoxID]:
                    removeBox(dictMappingIndexToBox, \
                        dictMappingCornerToIDsOfBoxesWithThem, dictMappingIDsOfBoxesToTheirCorners,\
                        thisIDToRemove, precision=precision);

                if(cornerToExamine not in dictMappingCornerToIDsOfBoxesWithThem):
                    return;
                # There should be a more efficient way of encorporating new boxes
                # instead of doing the below.
                listOfIDsOfBoxesToMerge = dictMappingCornerToIDsOfBoxesWithThem[cornerToExamine];
                thisFirstBoxIndex = 0;
                thisSecondBoxIndex = 1;
                continue;
            assert( thisSecondBoxIndex + 1 > thisSecondBoxIndex);# weak overflow check.
            thisSecondBoxIndex = thisSecondBoxIndex + 1;
        assert(thisFirstBoxIndex + 1 > thisFirstBoxIndex); # weak overflow check.
        thisFirstBoxIndex = thisFirstBoxIndex + 1
    return;


def mergeBoxes(listOfInitialBoxes, precision=3, maxNumberOfIterations=None):
    requires(isinstance(maxNumberOfIterations, type(None)) or isinstance(maxNumberOfIterations, int));
    requires(isinstance(maxNumberOfIterations, type(None)) or (maxNumberOfIterations > 0));
    initialDictionary = getSetupDicts(listOfInitialBoxes, precision=precision);
    dictMappingIndexToBox = initialDictionary["dictMappingIndexToBox"];
    dictMappingCornerToIDsOfBoxesWithThem = \
        initialDictionary["dictMappingCornerToIDsOfBoxesWithThem"];
    dictMappingIDsOfBoxesToTheirCorners = \
        initialDictionary["dictMappingIDsOfBoxesToTheirCorners"];

    lengthOfPreviousNumberOfBoxes = None;
    listOfCorners = list(dictMappingCornerToIDsOfBoxesWithThem.keys());
    iterationNumber = 0;
    while(lengthOfPreviousNumberOfBoxes == None or \
        lengthOfPreviousNumberOfBoxes != len(dictMappingIndexToBox)):

        if(maxNumberOfIterations != None and (iterationNumber > maxNumberOfIterations)):
            break;

        sys.stdout.flush();
        assert(iterationNumber < iterationNumber + 1); # weak overflow check
        iterationNumber = iterationNumber + 1;

        lengthOfPreviousNumberOfBoxes = len(dictMappingIndexToBox);

        randomOrderingOfCorners = np.random.permutation(range(0, len(dictMappingCornerToIDsOfBoxesWithThem))); # ssh-rsa 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 abc@defg # Randomly-
            # or trying to randonly- address corners so to avoid  constantly
            # trying to remerge the corners in the same order, which would help form
            # pathological examples.

        for thisIndex in randomOrderingOfCorners:
            thisCorner = listOfCorners[thisIndex];


            mergeBoxesInTargetSet(dictMappingIndexToBox, \
                dictMappingCornerToIDsOfBoxesWithThem, dictMappingIDsOfBoxesToTheirCorners, \
                thisCorner, precision=precision);

    return {"dictMappingIndexToBox" : dictMappingIndexToBox, \
            "dictMappingCornerToIDsOfBoxesWithThem" : dictMappingCornerToIDsOfBoxesWithThem, \
            "dictMappingIDsOfBoxesToTheirCorners" : dictMappingIDsOfBoxesToTheirCorners};


from boxesAndBoxOperations.readAndWriteBoxes import *;

def mergeBoxesOnRealData():
    #V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~VV~V~V~V~V
    # Code copied from analysisOfResults_<redacted>.py
    #==============================================================================

    def getBoxesFromFile():
        fhDict = {\
            "positionAndTheta_notTE" : "CLA_statesWhereNotTE_016410bf-c229-4655-85bf-351c2642d421.bin", \
            "positionAndTheta_TE" : "CLA_statesWhereTrueEverywhere_016410bf-c229-4655-85bf-351c2642d421.bin", \
            "postionAndThetaAndDerivatives_notTE" : "CLA_statesWhereNotTE_29393cea-4a98-4c63-bf00-4035ebe2aee6.bin", \
            "postionAndThetaAndDerivatives_TE" : "CLA_statesWhereTrueEverywhere_29393cea-4a98-4c63-bf00-4035ebe2aee6.bin" \
            };
        fhDict = {\
            "CLA_statesWhereTrueEverywhere_ed43a878-714b-4ff9-be38-2d02dbad9b2c" : \
                "CLA_statesWhereTrueEverywhere_ed43a878-714b-4ff9-be38-2d02dbad9b2c.bin"};
        boxDict = dict();
        for thisKey in fhDict:
            fhDict[thisKey] = open("resultsCEGARLikeAnalysis/" + fhDict[thisKey], "rb");
            boxDict[thisKey] = readBoxes(fhDict[thisKey]);
            fhDict[thisKey].close();
        return boxDict;

    #^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^

    temp = getBoxesFromFile();
    mergeBoxes(temp["CLA_statesWhereTrueEverywhere_ed43a878-714b-4ff9-be38-2d02dbad9b2c"]); #"positionAndTheta_notTE"])
    
    return;


def generateBoxDivisionsForTesting(numberOfDivisionsAlongAxis, dimensionOfBoxes):
    requires(isinstance(numberOfDivisionsAlongAxis, int));
    requires(numberOfDivisionsAlongAxis > 0);

    axisIntervals = [[x, x + 1] for x in range(0, numberOfDivisionsAlongAxis)];

    boxesInPreviousInteration = [[]];

    dimensionIndex = 0;
    while(dimensionIndex < dimensionOfBoxes):
        boxesInThisIteration = [];

        for thisPreviousBox in boxesInPreviousInteration:
            for thisAddedAxis in axisIntervals:
                boxesInThisIteration.append(thisPreviousBox + [thisAddedAxis]);

        boxesInPreviousInteration = boxesInThisIteration;

        assert(dimensionIndex < dimensionIndex + 1); # weak overflow check...
        dimensionIndex = dimensionIndex + 1;

    for thisIndex in range(0, len(boxesInThisIteration)):
        boxesInThisIteration[thisIndex] = np.array(boxesInThisIteration[thisIndex]);

    ensures(len(boxesInThisIteration) == numberOfDivisionsAlongAxis ** dimensionOfBoxes);
    ensures(all([isProperBox(x) for x in boxesInThisIteration]));
    return boxesInThisIteration;

def generateMutlidimensionalBlockStairsForTesting(numberOfGroups, dimension):
    requires(isinstance(numberOfGroups, int));
    requires(numberOfGroups > 0);
    requires(isinstance(dimension, int));
    requires(dimension >= 2);
    startBox =  getRandomBox(dimension); 
    # Note that in-and-of themselves, the four boxes - boxA, boxB, boxC, boxD -
    # should all be able to merge into a single box, [0,2]x[0,2]
    # TODO: pick the two dimensions that form the basis of the four boxes merged randomly...
    boxA = startBox.copy();
    boxA[0, :] = np.array([0,1]);
    boxA[1, :] = np.array([0,1]);
    boxB = startBox.copy();
    boxB[0, :] = np.array([1,2]);
    boxB[1, :] = np.array([0,1]);
    boxC = startBox.copy();
    boxC[0, :] = np.array([0,1]);
    boxC[1, :] = np.array([1,2]);
    boxD = startBox.copy();
    boxD[0, :] = np.array([1,2]);
    boxD[1, :] = np.array([1,2]);
    boxAAndBAndCAndDMergedTogether = startBox.copy();
    boxAAndBAndCAndDMergedTogether[1, :] = np.array([0,2]);
    boxAAndBAndCAndDMergedTogether[0, :] = np.array([0,2]);


    listToMerge = [];
    whatMergedResultShouldBe = [];

    def copyAndMoveOnDiagonalFourBasicBoxes(displacementOfDiagonal):
        requires(isinstance(displacementOfDiagonal, float) or isinstance(displacementOfDiagonal, int));
        thisCopy = [boxA.copy(), boxB.copy(), boxC.copy(), boxD.copy()];
        for thisIndex in range(0, len(thisCopy)):
            thisCopy[thisIndex][:2,:] = thisCopy[thisIndex][:2,:] + displacementOfDiagonal;
        return thisCopy;
    
    for thisIndex in range(0, numberOfGroups):
        displacement = 2 * thisIndex; # why times 2? Becuase the side-lengths of
            # boxAAndBAndCAndDMergedTogether are that long.
        listToMerge= listToMerge + copyAndMoveOnDiagonalFourBasicBoxes(displacement);
        whatMergedResultShouldBe.append(boxAAndBAndCAndDMergedTogether.copy());
        whatMergedResultShouldBe[-1][:2, :] = whatMergedResultShouldBe[-1][:2, :] + displacement;

    return {"listToMerge" : listToMerge, "whatMergedResultShouldBe" : whatMergedResultShouldBe};

from boxesAndBoxOperations.getBox import *;

def mergeBoxes_quadraticTime_usefulForOutputSpaceBoxes_mergeBoxesThatContainOneAnother(thisListOfBoxes):
    indicesToKeep = [];
    indicesToContinueCheckingAgainst = set(range(0, len(thisListOfBoxes)));
    for thisStartIndex in range(0, len(thisListOfBoxes)):
        keep = True;
        for thisEndIndex in indicesToContinueCheckingAgainst:
            if(thisEndIndex == thisStartIndex):
                continue;
            if(boxAContainsBoxB(thisListOfBoxes[thisEndIndex], thisListOfBoxes[thisStartIndex])):
                keep = False;
                break;
        if(keep):
            indicesToKeep.append(thisStartIndex);
        else:
            indicesToContinueCheckingAgainst.remove(thisStartIndex);
    assert(set(indicesToKeep) == indicesToContinueCheckingAgainst); # this should apply
        # by the end of the process....
    return [thisListOfBoxes[thisIndex] for thisIndex in indicesToKeep];







def mergeBoxes_quadraticTime_usefulForOutputSpaceBoxes_mergeBoxesThatContainOneAnother_faster(thisListOfBoxes):
    """
    If box A contains box B, then the volume and sum-of-side-lengths of A must be greater than the
    respective values of B. Note that it is possible for two boxes to have equal volume, but different
    sum-of-side-lengths; in three dimensions, for instance, if box A is 2-by-2-by-2 and box B is
    8-by-1-by-1, boxes A and B have equal volume but the sum of B's side lengths is greater than 
    that of B. If we consider a box C with side-lengths 2.5-by-2.5-by-2.5, even then its volume is
    greater than B's volume, but the sum of side-lengths of B is greater than C's. 

    In the code of this function, we sort in descending order of volume. After that, given 
    two boxes, A and B, we check that the sum A's sides is no less than the sum of B's sides
    prior to the slightly more expensive check of whether A actually contains B. 
    
    A further check examines the lower-bounds of the first coordinates, ensuring
    that they following the feasible order (i.e., if A[0,0] > B[0,0], then A 
    cannot contain B) and that they are in the proper range (i.e., if 
    (B[0,0] - A[0,0]) > sumOfA'sSideLengths then A cannot contain B). While one 
    may be tempted to expand the axis-feasibility checks to more dimensions, 
    this route of optimization (1) has diminishing returns, and thus does not
    likely justify the complication to the code (2) if carried out further, must
    be done while staying conscious of the hardware used, since (2a) the 
    potential use of SIMD in numpy array calculations (as present in the code 
    for boxAContainsBoxB) may actually make it more efficient that an overly 
    engineered serial implementation in Python, (2b) considering more extreme 
    cases, effects on cache locality may be worth bearing in mind as tempRefList
    grows in memory consumption; concerns about case (2b), however, are are 
    probably impractical to consider for our intentions.
    """
    tempRefList = [ (boxSize(x), getSumOfSideLengths(x), -x[0,0]) for x in thisListOfBoxes];
    orderToCheckBoxes = sorted( list(range(0, len(thisListOfBoxes))) , \
                            reverse=True, key=(lambda x: tempRefList[x]) );
    rawIndex_A = 0;
    while(rawIndex_A < len(thisListOfBoxes)):
        convertedIndex_A = orderToCheckBoxes[rawIndex_A];
        rawIndex_A = rawIndex_A + 1;
        if(convertedIndex_A < 0):
            continue;
        dataElem_A=tempRefList[convertedIndex_A];
        sumSideLength_A = dataElem_A[1];
        negativeLowerBoundFirstCoordinate_A = dataElem_A[2];
        thisBox_A = thisListOfBoxes[convertedIndex_A];
        rawIndex_B = rawIndex_A; # recall that we already incremented
            # rawIndex_A by 1.
        while(rawIndex_B < len(thisListOfBoxes)):
            convertedIndex_B = orderToCheckBoxes[rawIndex_B];
            rawIndex_B = rawIndex_B + 1;
            if(convertedIndex_B < 0):
                continue;
            dataElem_B = tempRefList[convertedIndex_B];
            if(dataElem_B[1] > sumSideLength_A):
                continue;
            if(dataElem_B[2] > negativeLowerBoundFirstCoordinate_A):
                continue;
            if(negativeLowerBoundFirstCoordinate_A - dataElem_B[2] >
                sumSideLength_A):
                continue;
            if(boxAContainsBoxB(thisBox_A, thisListOfBoxes[convertedIndex_B])):
                orderToCheckBoxes[rawIndex_B-1] = -1;
    return [thisListOfBoxes[x] for x in orderToCheckBoxes if (x >= 0)];


if(_LOCALDEBUGFLAG > 0):
    import pickle;
    import time;

def test_mergeBoxes_quadraticTime_usefulForOutputSpaceBoxes_mergeBoxesThatContainOneAnother_faster():    
    def convertToEasilyComparedValues(thisListOfBoxes):
        tempList = [pickle.dumps(x) for x in thisListOfBoxes];
        return sorted(tempList);
    def orderForDisplay(thisListOfBoxes):
        return sorted(thisListOfBoxes, key=(lambda x: pickle.dumps(x)));
    def checkResults(thisBoxList):
        Astart=time.clock();
        resultToCheck = mergeBoxes_quadraticTime_usefulForOutputSpaceBoxes_mergeBoxesThatContainOneAnother_faster(thisBoxList);
        Aend=time.clock();
        print("          time for improved version:" + str(Aend- Astart), flush=True);
        Bstart=time.clock(); # avoids capturing the time to print to terminal, as
            # reusing Aend would, though obviously that time should be neglegable in most
            # cases..
        expectedResult = mergeBoxes_quadraticTime_usefulForOutputSpaceBoxes_mergeBoxesThatContainOneAnother(thisBoxList);   
        Bend=time.clock();
        print("             time for non-optimized:" + str(Bend-Bstart), flush=True);
        if(convertToEasilyComparedValues(expectedResult) != convertToEasilyComparedValues(resultToCheck)):
            raise Exception("\n\n\n" + \
                "test_mergeBoxes_quadraticTime_usefulForOutputSpaceBoxes_mergeBoxesThatContainOneAnother_faster:\n"+ \
                "Test failed: \n" + \
                "Input = " + str(thisBoxList) + "\n" + \
                "expectedResult = "+ str(orderForDisplay(expectedResult)) + "\n" +\
                "resultToCheck  = " + str(orderForDisplay(resultToCheck)) );
        endOfCheck=time.clock();
        print("        time for checking results:" + str(endOfCheck - Bend), flush=True);
        return;
    
    print("test_mergeBoxes_quadraticTime_usefulForOutputSpaceBoxes_mergeBoxesThatContainOneAnother_faster:", flush=True);
    for thisNumberOfBoxesToCheck in [5, 25, 1000, 5000]:
        for thisDimension in [1, 2, 5, 10, 30]:
            print("    testing: dimension:" + str(thisDimension) + \
                  ", thisNumberOfBoxesToCheck:" + str(thisNumberOfBoxesToCheck), flush=True);
            for thisTrialNumber in range(1,6):
                print("    trial:" + str(thisTrialNumber), flush=True);
                thisBoxList = [getRandomBox(thisDimension) for x in range(0, thisNumberOfBoxesToCheck)];
                checkResults(thisBoxList);
    return;

if(_LOCALDEBUGFLAG > 0):
    test_mergeBoxes_quadraticTime_usefulForOutputSpaceBoxes_mergeBoxesThatContainOneAnother_faster();


