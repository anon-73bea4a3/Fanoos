

import config;
_LOCALDEBUGFLAG = config.debugFlags.get_v_print_ForThisFile(__file__);
    

import numpy as np
from utils.contracts import *;

from propagateBoxThroughLearnedSystem.classesToPropogateBoxThroughModels import ModelBoxProgatorManager;
from boxesAndBoxOperations.getBox import isProperBox, getBox, getDimensionOfBox, getJointBox, getContainingBox, getRandomBox;

from boxesAndBoxOperations.CEGARFileWrittingManager import CEGARFileWrittingManager;

def getInitialAbstraction_boxesBySign(universeBox):
    requires(isProperBox(universeBox));
    requires(np.all(universeBox[:, 0] < universeBox[:, 1]));
     
    numberOfBoxes = 2 ** (universeBox.shape[0]);

    listToReturn = [];
    for thisboxIndex in range(0, numberOfBoxes):

        thisBox = universeBox.copy();
        binaryRepresentationOfIndex = np.binary_repr(thisboxIndex, width=getDimensionOfBox(universeBox));
        assert(isinstance(binaryRepresentationOfIndex, str));
        assert(all([(x in {"1", "0"}) for x in binaryRepresentationOfIndex]));
        for thisVariableIndex in range(0, getDimensionOfBox(universeBox)):
            thisBox[thisVariableIndex, int(binaryRepresentationOfIndex[thisVariableIndex])] = np.mean(thisBox[thisVariableIndex, :]);

        listToReturn.append(thisBox);

    return listToReturn;


from boxesAndBoxOperations.splitBox import splitBox;


import inspect;

import time;
timingInfoForLocation_2e048534_BoxTest = [];

from CEGARLikeAnalysis import labelsForBoxes;
from CEGARLikeAnalysis.refinementPathManager import RefPathManager ;

def helper_formDummyBoxes(thisInputBox, functionToDetermineWhenToGiveUpOnBox, CEGARFileWrittingManagerInstance, scalingForSplitting, depth):
    if(functionToDetermineWhenToGiveUpOnBox(thisInputBox)):
        CEGARFileWrittingManagerInstance.writeBox(thisInputBox, \
            [depth, (labelsForBoxes.FALSEEVERYWHERE | labelsForBoxes.LOWESTLEVEL_FALSESOMEWHEREANDEXHAUSTEDLOOKING) ]);
        return;
    dummyBoxesToWrite = splitBox(thisInputBox, "randomNumberOfUniformSplits", scalingFactors=scalingForSplitting);
    for thisNextBox in dummyBoxesToWrite:
        helper_formDummyBoxes(thisNextBox, functionToDetermineWhenToGiveUpOnBox, CEGARFileWrittingManagerInstance, scalingForSplitting, depth + 1)
    return;

def analysis_divingIntoBox(thisInputBox, thisInstanceOfModelBoxProgatorManager, functionToStatisfy, functionToDetermineWhenToGiveUpOnBox, \
        CEGARFileWrittingManagerInstance, scalingForSplitting, depth, path, functionToCheckWhetherNoPointsInTheBoxStatisfyCondition=None):
    thisOutputBox = thisInstanceOfModelBoxProgatorManager.pushBoxThrough(thisInputBox);

    sideInformationForRefinementProcess = None;
    lazyEval_checkWhetherNoPoints = None;


    RefPathManager.old.goToNextDepthDecreaseIfTooDeep(depth);
    startTime = time.process_time();  #location2e048534-c79b-4177-a79d-cc0ef71384d4_boxTest
    if(RefPathManager.old.headIsApplicable(depth)):
        tempPath = RefPathManager.old.getCopyOfCurrentPath();
        assert(tempPath == path); # a good check to ensure things remained aligned.
        (dTemp, rf1, rf2, sideRefinementInfoTemp) = RefPathManager.old.head();
        RefPathManager.old.advance();
        assert(dTemp == depth);
        sideInformationForRefinementProcess = (sideRefinementInfoTemp if (sideRefinementInfoTemp > 0) else None);
        boxTest = rf1;
        lazyEval_checkWhetherNoPoints = (lambda *ignoreVal : rf2);
        assert( (sideInformationForRefinementProcess is None) or (not boxTest)); # basically, 
            # we wouldn't be refining (i.e., sideInformationForRefinementProcess would NOT
            # be None if we were refining) if boxTest was True. See the conditional
            # branches below.
    else:
        boxTest = functionToStatisfy(thisInputBox, thisOutputBox);
        lazyEval_checkWhetherNoPoints = (lambda *ignoreVal : 
             (functionToCheckWhetherNoPointsInTheBoxStatisfyCondition is not None) and \
              (functionToCheckWhetherNoPointsInTheBoxStatisfyCondition(thisInputBox, thisOutputBox)) \
            );
    endTime   = time.process_time();
    timingInfoForLocation_2e048534_BoxTest.append(endTime - startTime);

    if(boxTest):
        result_checkWhetherNoPoints = None
        RefPathManager.new.append(depth, boxTest, result_checkWhetherNoPoints, 0 );

        CEGARFileWrittingManagerInstance.writeBox(thisInputBox, [depth, labelsForBoxes.TRUEEVERYWHERE]);
        return True; # True for success...
    elif(functionToDetermineWhenToGiveUpOnBox(thisInputBox)):
        result_checkWhetherNoPoints = None
        RefPathManager.new.append(depth, boxTest, result_checkWhetherNoPoints, 0 );


        CEGARFileWrittingManagerInstance.writeBox(thisInputBox, \
                    [depth, labelsForBoxes.LOWESTLEVEL_FALSESOMEWHEREANDEXHAUSTEDLOOKING]);
        return False; #False for failure.
    elif( lazyEval_checkWhetherNoPoints() ):
        result_checkWhetherNoPoints = True;
        RefPathManager.new.append(depth, boxTest, result_checkWhetherNoPoints, 0 );


        CEGARFileWrittingManagerInstance.writeBox(thisInputBox, \
            [depth, labelsForBoxes.FALSEEVERYWHERE]);
        helper_formDummyBoxes(thisInputBox, functionToDetermineWhenToGiveUpOnBox, \
            CEGARFileWrittingManagerInstance, scalingForSplitting, depth); # yes, we pass the depth here, not depth+1, 
                # because the further splitting occurs in helper_formDummyBoxes.
        return False; #False for failure. # goes up a layer to accumulate a larger box where all members of the box failed
    else:
        result_checkWhetherNoPoints = (None if (functionToCheckWhetherNoPointsInTheBoxStatisfyCondition is None) else False);

        # recurse
        refimentElements = splitBox(thisInputBox, "randomNumberOfUniformSplits", scalingFactors=scalingForSplitting, \
            sideInformation=sideInformationForRefinementProcess);
        assert( (sideInformationForRefinementProcess is None) or \
            (len(refimentElements) == sideInformationForRefinementProcess));
        RefPathManager.new.append(depth, boxTest, result_checkWhetherNoPoints, \
            len(refimentElements) \
        );
        resultOfFurtherRefining = [\
            analysis_divingIntoBox(x, thisInstanceOfModelBoxProgatorManager, functionToStatisfy, functionToDetermineWhenToGiveUpOnBox, \
                CEGARFileWrittingManagerInstance, scalingForSplitting, depth+1, path + [index],functionToCheckWhetherNoPointsInTheBoxStatisfyCondition)\
            for index, x in enumerate(refimentElements)];
        if(not any(resultOfFurtherRefining)):
            return False; # goes up a layer to accumulate a larger box where all members of the box failed
        else:
            for thisIndex in range(0, len(resultOfFurtherRefining)):
                if(resultOfFurtherRefining[thisIndex]): # box succeeded and thus was written out by lower level...
                    continue;

                CEGARFileWrittingManagerInstance.writeBox(refimentElements[thisIndex], \
                    [depth+1, labelsForBoxes.HIGHESTLEVELBOXUNIONBOX_FALSESOMEWHEREANDEXHAUSTEDLOOKING]);
            return True; # i.e., not all members of the box failed, so thisInputBox should not be accumulated into 
                 # a box where we label all members of the box as failures...
    raise Exception("Control should never reach here");
    return;


"""
ssh-rsa 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 abc@defg
"""
from databaseInterface.databaseValueTracker import ObjDatabaseValueTracker;

import config;

import pickle;

def analysis(universeBox, thisInstanceOfModelBoxProgatorManager, functionToStatisfy, functionToDetermineWhenToGiveUpOnBox, \
        limitSplittingToAxisWithIndicesInThisList=None, functionToCheckWhetherNoPointsInTheBoxStatisfyCondition=None,\
        completelyRedoRefinement=config.defaultValues.completelyRedoRefinementEachCallToCEGAR):
    timingInfoForLocation_2e048534_BoxTest = [];
    requires(isinstance(limitSplittingToAxisWithIndicesInThisList, list));
    requires( \
        np.all([(x >= 0 and x < getDimensionOfBox(universeBox)) for x in limitSplittingToAxisWithIndicesInThisList]));
    requires( \
        (len(set(limitSplittingToAxisWithIndicesInThisList)) == len(limitSplittingToAxisWithIndicesInThisList))  );

    # One probably can't effectively put the function being checked in the parameters being
    #     sorted (at least not by using pickle) since the functions were locally scoped.
    #     Within the responces for a single question, however, that should not be a issue anytime
    #     in the near futures. Also, within the responces for a single question, the universeBox 
    #     is unlikely to be something to be changed anytime in the near future. Thus, for now
    #     those are not essential items to store.
    pickleOfParametersPassedInHereThatMayChangeWithTheSameQuestion = \
        pickle.dumps({"limitSplittingToAxisWithIndicesInThisList" : limitSplittingToAxisWithIndicesInThisList});


    if(completelyRedoRefinement or \
            (RefPathManager.old.highlevelParametersForSplitting != \
             pickleOfParametersPassedInHereThatMayChangeWithTheSameQuestion ) \
        ):
        RefPathManager.reset();
        RefPathManager.old.highlevelParametersForSplitting = \
            pickleOfParametersPassedInHereThatMayChangeWithTheSameQuestion;

    RefPathManager.new.highlevelParametersForSplitting = \
        pickleOfParametersPassedInHereThatMayChangeWithTheSameQuestion;

    CEGARFileWrittingManagerInstance = CEGARFileWrittingManager(universeBox);
    CEGARFileWrittingManagerInstance.writeMetadata(\
        "fileNameOfLoadedModel", thisInstanceOfModelBoxProgatorManager.fileNameOfLoadedModel);
    CEGARFileWrittingManagerInstance.writeMetadata(\
        "functionToStatisfy", inspect.getsource(functionToStatisfy));
    CEGARFileWrittingManagerInstance.writeMetadata(\
        "functionToDetermineWhenToGiveUpOnBox", inspect.getsource(functionToDetermineWhenToGiveUpOnBox));
    CEGARFileWrittingManagerInstance.writeMetadata(\
        "QAStateUUID_mostRecentBeingComputed", ObjDatabaseValueTracker.get_QAStateUUID_mostRecentBeingComputed());
    theseInputAbstractions = getInitialAbstraction_boxesBySign(universeBox);
    assert(isinstance(theseInputAbstractions, list));
    assert(len(theseInputAbstractions) > 0);

    scalingForSplitting = universeBox[:, 1] - universeBox[:, 0]; 
    tempBox = scalingForSplitting.copy(); # TODO: remove this unnecessary copy in the near future.
    # As implemented in the splitBox file, when the scaling factor has a nan in a posotion, 
    # the axis corresponding to that index is ignored.
    tempBox[:] = np.nan;
    tempBox[limitSplittingToAxisWithIndicesInThisList] = scalingForSplitting[limitSplittingToAxisWithIndicesInThisList];
    scalingForSplitting = tempBox;

    for index, thisBox in enumerate(theseInputAbstractions):
        anySuccess = analysis_divingIntoBox(thisBox, thisInstanceOfModelBoxProgatorManager, \
            functionToStatisfy, functionToDetermineWhenToGiveUpOnBox, CEGARFileWrittingManagerInstance, scalingForSplitting,\
            0, [index], \
            functionToCheckWhetherNoPointsInTheBoxStatisfyCondition=functionToCheckWhetherNoPointsInTheBoxStatisfyCondition);
        if(not anySuccess):
            CEGARFileWrittingManagerInstance.writeBox(thisBox, [0, labelsForBoxes.HIGHESTLEVELBOXUNIONBOX_FALSESOMEWHEREANDEXHAUSTEDLOOKING]);

    CEGARFileWrittingManagerInstance.closeFilesToSaveResultsIn();
    RefPathManager.replaceOld();
    RefPathManager.new.highlevelParametersForSplitting = \
        pickleOfParametersPassedInHereThatMayChangeWithTheSameQuestion;
    return CEGARFileWrittingManagerInstance;






