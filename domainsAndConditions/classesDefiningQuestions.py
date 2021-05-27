

import config;
_LOCALDEBUGFLAG = config.debugFlags.get_v_print_ForThisFile(__file__);
    
from utils.quickResetZ3Solver import quickResetZ3Solver;

import pickle;
import numpy as np;
import sys;
from utils.contracts import *;

from propagateBoxThroughLearnedSystem.classesToPropogateBoxThroughModels import ModelBoxProgatorManager;
from boxesAndBoxOperations.getBox import isProperBox, getBox, getDimensionOfBox, getJointBox, getContainingBox, getRandomBox, getRandomVectorInBox, getRandomVectorInBox, boxSize;

import uuid;

from utils.getGitCommitHash import gitCommitHashWhenThisCodeStartedRunning;
from utils.getStringTimeNow import *;

import re;

import struct;

from boxesAndBoxOperations.readAndWriteBoxes import readBoxes;
from boxesAndBoxOperations.splitBox import splitBox;
from CEGARLikeAnalysis.CEGARLikeAnalysisMain import analysis ;

from boxesAndBoxOperations.mergeBoxes import mergeBoxes, mergeBoxes_quadraticTime_usefulForOutputSpaceBoxes_mergeBoxesThatContainOneAnother_faster;

import inspect;

from CEGARLikeAnalysis import labelsForBoxes;

from boxesAndBoxOperations.codeForGettingSamplesBetweenBoxes import getSampleVectorsToCheckAgainst, getBoxCenter;
from domainsAndConditions.baseClassConditionsToSpecifyPredictsWith import CharacterizationConditionsBaseClass,\
         Condition_TheBoxItself, MetaCondition_Conjunction;
from domainsAndConditions.baseClassDomainInformation import BaseClassDomainInformation; 

import z3;

import config;

from databaseInterface.databaseValueTracker import ObjDatabaseValueTracker;
from databaseInterface.databaseIOManager import objDatabaseInterface, executeDatabaseCommandList;
from utils.distributionStatics import distributionStatics;

from statesAndOperatorsAndSelection.descriptionState import DescriptionState ;

class QuestionBaseClass():

    def setID(self):
        self.uuid = str(uuid.uuid4());
        return

    def getID(self):
        return self.uuid;# .copy();

    def __init__(self, conditionsToBeConsistentWith):
        requires(isinstance(conditionsToBeConsistentWith, list));
        requires(len(conditionsToBeConsistentWith) > 0);
        requires(all([isinstance(x, CharacterizationConditionsBaseClass) for x in conditionsToBeConsistentWith]));
        self.conditionsToBeConsistentWith = conditionsToBeConsistentWith;
        self.setID();
        
        return;

    def getCopyOfConditionsToBeConsistentWith(self):
        return self.conditionsToBeConsistentWith.copy();

    def formConditionToSatisfy(self, numberOfSamples):
        raise NotImplementedError(); # child classes must override.



###############################################################################

###############################################################################

###############################################################################


import traceback;
import os;
import time as timePackageToUseForSleep;


class Question_DomainOfVariablesInResponce(QuestionBaseClass):

    @staticmethod
    def setVariablesInformation(domainInfo):
        raise NotImplementedError();
    
    @staticmethod
    def getUseableConditions(domainInfo, classType, conditionNameStartsWith=""):
        requires(issubclass(classType, Question_DomainOfVariablesInResponce));
        requires(isinstance(conditionNameStartsWith, str));
        requires(isinstance(domainInfo, BaseClassDomainInformation));
        (variablesConditionMayInclude, variablesBoxesProducedMayBeOver) = \
            classType.setVariablesInformation(domainInfo);
            
        def convertConditionName(thisCondition):
            return str(thisCondition).replace(" ", "_").lower();
        temp= [convertConditionName(thisCondition) for thisCondition in domainInfo.getBaseConditions() if \
               (   thisCondition.relaventVariables().issubset(variablesConditionMayInclude) and \
                   convertConditionName(thisCondition).startswith(conditionNameStartsWith)   
               )  ];
        return temp;


    def helper_getRelaventInputBoxes_get_functionToStatisfy(self):
        functionToStatisfy_initial = self.formConditionToSatisfy();
        return self.setupProperFeedToFunctionforThisQuestionType(functionToStatisfy_initial);

    def setupProperFeedToFunctionforThisQuestionType(self, thisFunct):
        raise NotImplementedError(); 

    def getFunctionToCheckWhetherNoPointsInTheBoxStatisfyCondition(self):
        raise NotImplementedError(); 

    def helper_getBoxesToDescribe_get_boxesToDescribePriorToMerging(self, thisInstanceOfModelBoxProgatorManager, \
        inputDomainBoxes):
        raise NotImplementedError(); 

    def __init__(self, conditionsToBeConsistentWith, domainInformation):
        requires(isinstance(domainInformation, BaseClassDomainInformation));
        QuestionBaseClass.__init__(self, conditionsToBeConsistentWith);

        self.domainInfo = domainInformation;
        self.variablesConditionMayInclude = None;
        self.variablesBoxesProducedMayBeOver = None;
        (self.variablesConditionMayInclude, self.variablesBoxesProducedMayBeOver) = \
            self.setVariablesInformation(self.domainInfo);
        assert(isinstance(self.variablesConditionMayInclude, list));
        assert(isinstance(self.variablesBoxesProducedMayBeOver, list));
        assert(len(self.variablesConditionMayInclude) > 0);
        assert(len(self.variablesBoxesProducedMayBeOver) > 0);

        if(not all([thisCondition.relaventVariables().issubset(self.variablesConditionMayInclude) \
                for thisCondition in self.conditionsToBeConsistentWith])):
            raise Exception("Conditions provided involve variables that are not restricted to the domain of interest.");

        ensures(isinstance(self.variablesConditionMayInclude, list));
        ensures(isinstance(self.variablesBoxesProducedMayBeOver, list));
        ensures(len(self.variablesConditionMayInclude) > 0);
        ensures(len(self.variablesBoxesProducedMayBeOver) > 0);
        ensures(all([isinstance(x, z3.z3.ArithRef) for x in self.variablesConditionMayInclude]));
        ensures(all([isinstance(x, z3.z3.ArithRef) for x in self.variablesBoxesProducedMayBeOver]));
        ensures(set(self.variablesConditionMayInclude + self.variablesBoxesProducedMayBeOver).issubset(\
            self.domainInfo.inputSpaceVariables() + self.domainInfo.outputSpaceVariables() ) );
        return
 

    def getRelaventInputBoxes(self, thisInstanceOfModelBoxProgatorManager, thisState):
        requires(isinstance(thisState, DescriptionState)); 

        functionToStatisfy = self.helper_getRelaventInputBoxes_get_functionToStatisfy();

        functionToCheckWhetherNoPointsInTheBoxStatisfyCondition = self.getFunctionToCheckWhetherNoPointsInTheBoxStatisfyCondition();

        completelyRedoRefinement = thisState.readParameter("completelyRedoRefinement");
        epsilonForBoxSize = thisState.readParameter("floatValueForBoxDivisionCutoff");
        splitOnlyOnRelaventVariables = thisState.readParameter("splitOnlyOnRelaventVariables");
        assert(isinstance(completelyRedoRefinement, bool));
        assert(isinstance(epsilonForBoxSize, float));
        assert(epsilonForBoxSize > 0);
        assert(isinstance(splitOnlyOnRelaventVariables, bool));
        

        axisToSplitOn= list( range(0, getDimensionOfBox(self.domainInfo.getInputSpaceUniverseBox())) );
        if(splitOnlyOnRelaventVariables):
            setOfRelaventVariables = set();
            for thisCondition in self.conditionsToBeConsistentWith:
                setOfRelaventVariables.update(thisCondition.relaventVariables());
            tempAxisToSplitOn=[\
                thisIndex for thisIndex in axisToSplitOn \
                if (self.domainInfo.inputSpaceVariables()[thisIndex] in setOfRelaventVariables)];
            if(len(tempAxisToSplitOn) > 0): #This would fail to happen, for instanc, when 
                # self.conditionsToBeConsistentWith specify conditions over the output space
                # as oppossed to the input space.
                axisToSplitOn=tempAxisToSplitOn;
        assert(len(axisToSplitOn) > 0);
        # The below assert is most easily understood from converting (p or q) to (if (not p) then q).
        # That is, if axisToSplitOn does not include the whole input space, it is because 
        # splitOnlyOnRelaventVariables has been enabled. Note that this does NOT say the converse,
        # since even if splitOnlyOnRelaventVariables is True, axisToSplitOn might not reduce in
        # size for a number of reasons.
        assert( (len(axisToSplitOn) == len(self.domainInfo.inputSpaceVariables())) or \
                splitOnlyOnRelaventVariables);
        assert( len(axisToSplitOn) <= len(self.domainInfo.inputSpaceVariables()) );
        assert( set(axisToSplitOn).issubset(range(0, len(self.domainInfo.inputSpaceVariables())) ));
        # Below checks that the elements of axisToSplitOn are unique
        assert( len(set(axisToSplitOn)) == len(axisToSplitOn) );
    
        axisScaling = self.domainInfo.getInputSpaceUniverseBox()[:, 1] - self.domainInfo.getInputSpaceUniverseBox()[:, 0];
        assert(all(axisScaling >= 0.0));
        indicesWhereAxisNotFlat = np.where(axisScaling[axisToSplitOn] > 0)[-1];
        assert(np.all(axisScaling[axisToSplitOn][indicesWhereAxisNotFlat] > 0));
        def functionToDetermineWhenToGiveUpOnBox_axisSmallAfterScalingByUniverseSize(thisBox):
            return np.max( (thisBox[axisToSplitOn,:][indicesWhereAxisNotFlat,1] - thisBox[axisToSplitOn,:][indicesWhereAxisNotFlat,0]) /\
                axisScaling[axisToSplitOn][indicesWhereAxisNotFlat]) <= epsilonForBoxSize;

        thisCEGARFileWrittingManagerInstance = analysis(self.domainInfo.getInputSpaceUniverseBox(), thisInstanceOfModelBoxProgatorManager, \
            functionToStatisfy, functionToDetermineWhenToGiveUpOnBox_axisSmallAfterScalingByUniverseSize, \
            limitSplittingToAxisWithIndicesInThisList=axisToSplitOn, \
            functionToCheckWhetherNoPointsInTheBoxStatisfyCondition=functionToCheckWhetherNoPointsInTheBoxStatisfyCondition,\
            completelyRedoRefinement=completelyRedoRefinement);
    
        fileNameHoldingDesiredBoxes = \
            thisCEGARFileWrittingManagerInstance.dictMappingFileTypeToFileHandleToUse["boxes"].name;
    
        def continuationToGetBoxesToReturn():
            tempFH = open(fileNameHoldingDesiredBoxes, "rb");
            boxesToReturn = [x[0] for x in readBoxes(tempFH) if ((x[1][1] &  labelsForBoxes.LOWESTLEVEL_FALSESOMEWHEREANDEXHAUSTEDLOOKING) > 0)];  #<---------------- NOTICE THE NOT (i.e., the check for falsity)....
            tempFH.close();
            ensures(isinstance(boxesToReturn, list));
            ensures(all([isProperBox(x) for x in boxesToReturn]));
            return boxesToReturn;

        # Note that the second disjunct in the below depends on the specifics
        # of the splitting strategy and stop-criteria we use, and as such may
        # need to be adjusted if we employ different functions later.
        ensures(splitOnlyOnRelaventVariables or \
            all([ np.all((x[:,1] - x[:,0]) <= (epsilonForBoxSize * axisScaling)) \
                    for x in continuationToGetBoxesToReturn() ]) \
            );

        return continuationToGetBoxesToReturn;



    @staticmethod
    def recordBoxStats(listOfBoxes, phaseLabel):
        requires(isinstance(phaseLabel, str));
        requires(len(phaseLabel) > 0);
        requires(isinstance(listOfBoxes, list));
        requires(all([isProperBox(x) for x in listOfBoxes]));

        labelForThisPhaseInQuestionAnswering = "Question_DomainOfVariablesInResponce:" + phaseLabel;

        #V~~VV~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V
        # Below is largely copied from descriptionState.py
        # TODO: add this sort of code as a funtion in the utils to call upon....
        #=========================================================================
        generalSummaryFunctionsAndLabelsForThem = [\
            ( (lambda A : np.prod(np.diff(A, axis=1)) ), "bvolume"), \
            ( (lambda A : np.min(np.diff(A, axis=1)) ), "bminSideLength"), \
            ( (lambda A : np.max(np.diff(A, axis=1)) ), "bmaxSideLength"), \
            ( (lambda A : np.sum(np.diff(A, axis=1)) ), "bsumSideLengths"), \
        ];
        for thisFunctAndLabel in generalSummaryFunctionsAndLabelsForThem:
            theseValues = [ thisFunctAndLabel[0](x) for x in listOfBoxes];
            resultValue = distributionStatics(theseValues);
            specificLabel = labelForThisPhaseInQuestionAnswering + ":" + thisFunctAndLabel[1];
            for thisKey in resultValue:
                commandToExecute = \
                    "INSERT INTO QAStateValues ( QAStateUUID , fieldName, fieldValue) VALUES ('" + \
                    ObjDatabaseValueTracker.get_QAStateUUID_mostRecentBeingComputed() + "', '" + (specificLabel + ":" + thisKey)  + "', ? );";
                objDatabaseInterface.interfaceBleed_insertValuesForBlob(\
                    commandToExecute, [resultValue[thisKey]]  );                
            objDatabaseInterface.commit();
        #^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^
        return;



    def getBoxesToDescribe(self, thisInstanceOfModelBoxProgatorManager, thisState ):
        requires(isinstance(thisState, DescriptionState));
   
        continuationFor_inputDomainBoxes = self.getRelaventInputBoxes(\
                thisInstanceOfModelBoxProgatorManager, thisState );
        assert("function" in str(type(continuationFor_inputDomainBoxes)) );
        inputDomainBoxes = continuationFor_inputDomainBoxes();
        assert(isinstance(inputDomainBoxes, list));
    
        listMappingBoxIndexToVariable = self.variablesBoxesProducedMayBeOver;
        if(len(inputDomainBoxes) == 0):
            return ([], listMappingBoxIndexToVariable, continuationFor_inputDomainBoxes);
        assert(len(inputDomainBoxes) > 0);
    
        boxesToDescribePriorToMerging = self.helper_getBoxesToDescribe_get_boxesToDescribePriorToMerging(\
                                            thisInstanceOfModelBoxProgatorManager, inputDomainBoxes);
    
        assert(all([ (getDimensionOfBox(thisBox) == \
                len(self.variablesBoxesProducedMayBeOver) ) \
                for thisBox in boxesToDescribePriorToMerging]));
    
        boxesToReturn = None;
        limitOnNumberOfTimesToMerge = thisState.readParameter("limitOnNumberOfTimesToMerge");
        assert(isinstance(limitOnNumberOfTimesToMerge, int) or (type(limitOnNumberOfTimesToMerge) == type(None)));
        assert((limitOnNumberOfTimesToMerge == None) or (limitOnNumberOfTimesToMerge >= 0));
        if((limitOnNumberOfTimesToMerge == None) or (limitOnNumberOfTimesToMerge > 0)):
            middleLabelForBoxStatsRecording = "getBoxesToDescribe:"
            
            self.recordBoxStats(boxesToDescribePriorToMerging, \
                middleLabelForBoxStatsRecording + "boxesOfInterestPriorToMerging");

            precisionForMerging = thisState.readParameter("precisionForMerging");
            temp = mergeBoxes(boxesToDescribePriorToMerging, precision=precisionForMerging, \
                            maxNumberOfIterations=limitOnNumberOfTimesToMerge);
            boxesToReturn = list(temp["dictMappingIndexToBox"].values());
            boxesToReturn = mergeBoxes_quadraticTime_usefulForOutputSpaceBoxes_mergeBoxesThatContainOneAnother_faster(boxesToReturn);

            self.recordBoxStats(boxesToReturn, \
                middleLabelForBoxStatsRecording + "boxesOfInterestAfterMerging");

        else:
            temp = boxesToDescribePriorToMerging;
            boxesToReturn = temp;
        assert(boxesToReturn is not None);
    
        # It is important to have this function return listMappingBoxIndexToVariable, not
        # only to possibly save labels and provide some centeralization, but also to ensure
        # that the variable list in question is always returned in the same order...
        ensures(isinstance(listMappingBoxIndexToVariable, list));
        ensures(all([isinstance(x, z3.z3.ArithRef) for x in listMappingBoxIndexToVariable]));
        ensures(all([ (getDimensionOfBox(thisBox) == \
                len(listMappingBoxIndexToVariable) ) \
                for thisBox in boxesToReturn]));
        return (boxesToReturn, listMappingBoxIndexToVariable, continuationFor_inputDomainBoxes);




class Question_InputDomain(Question_DomainOfVariablesInResponce):

    @staticmethod
    def setVariablesInformation(domainInfo):
        variablesConditionMayInclude = domainInfo.outputSpaceVariables();
        variablesBoxesProducedMayBeOver = domainInfo.inputSpaceVariables();
        return (variablesConditionMayInclude, variablesBoxesProducedMayBeOver);

    def setupProperFeedToFunctionforThisQuestionType(self, thisFunctIntial): 
        # The CEGAR-like analysis uses functions of form that take (inputBox, outputBox) as 
        #     input ...
        thisFunctFinal = (lambda inputBox, outputBox : thisFunctIntial(outputBox));
        return thisFunctFinal;
    
    def helper_getBoxesToDescribe_get_boxesToDescribePriorToMerging(self, thisInstanceOfModelBoxProgatorManager, \
        inputDomainBoxes):
        boxesToDescribePriorToMerging = inputDomainBoxes;
        return boxesToDescribePriorToMerging;
    


class Question_OutputDomain(Question_DomainOfVariablesInResponce):

    @staticmethod
    def setVariablesInformation(domainInfo):
        variablesConditionMayInclude = domainInfo.inputSpaceVariables();
        variablesBoxesProducedMayBeOver = domainInfo.outputSpaceVariables();
        return (variablesConditionMayInclude, variablesBoxesProducedMayBeOver);

    def setupProperFeedToFunctionforThisQuestionType(self, thisFunctIntial):
        # The CEGAR-like analysis uses functions of form that take (inputBox, outputBox) as 
        #     input ...
        thisFunctFinal = (lambda inputBox, outputBox : thisFunctIntial(inputBox));
        return thisFunctFinal;
    
    
    def helper_getBoxesToDescribe_get_boxesToDescribePriorToMerging(self, thisInstanceOfModelBoxProgatorManager, \
        inputDomainBoxes):

        boxesToDescribePriorToMerging = [\
            thisInstanceOfModelBoxProgatorManager.pushBoxThrough(thisInputBox) \
            for thisInputBox in inputDomainBoxes ];

        return boxesToDescribePriorToMerging;
    


class Question_JointInputAndOutputDomain(Question_DomainOfVariablesInResponce):

    @staticmethod
    def setVariablesInformation(domainInfo):
        variablesConditionMayInclude =  domainInfo.inputSpaceVariables() + domainInfo.outputSpaceVariables();
        variablesBoxesProducedMayBeOver =  domainInfo.inputSpaceVariables() + domainInfo.outputSpaceVariables();
        return (variablesConditionMayInclude, variablesBoxesProducedMayBeOver);

    def setupProperFeedToFunctionforThisQuestionType(self, thisFunctIntial):
        thisFunctFinal = (lambda inputBox, outputBox : thisFunctIntial(getJointBox([inputBox, outputBox])));
        return thisFunctFinal;
    
    def helper_getBoxesToDescribe_get_boxesToDescribePriorToMerging(self, thisInstanceOfModelBoxProgatorManager, \
        inputDomainBoxes):

        correspondingOutputBoxes = [\
            thisInstanceOfModelBoxProgatorManager.pushBoxThrough(thisInputBox) \
            for thisInputBox in inputDomainBoxes ];
        assert(len(correspondingOutputBoxes) == len(inputDomainBoxes));
        assert(all([ (getDimensionOfBox(thisBox) == len(self.domainInfo.outputSpaceVariables())) \
            for thisBox in correspondingOutputBoxes]));
        boxesToDescribePriorToMerging = [\
            getJointBox(list(x)) for x in zip(inputDomainBoxes, correspondingOutputBoxes)];
    
        return boxesToDescribePriorToMerging;
    

###############################################################################

############################################################################### ssh-rsa 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 abc@defg

###############################################################################



class Question_WayConditionIsChecked(QuestionBaseClass):
    pass;


class Question_FormalUniversalQuant(Question_WayConditionIsChecked):

    def _helper_getFunctionToCheckWhetherNoPointsInTheBoxStatisfyCondition_convertBoxToFormulaConstraints(self, thisBox):
        requires(isProperBox(thisBox));
        requires(getDimensionOfBox(thisBox) == len(self.variablesConditionMayInclude));
        F = z3.And([ \
            z3.And( float(thisBox[index, 0]) <= self.variablesConditionMayInclude[index], \
                    self.variablesConditionMayInclude[index] <= float(thisBox[index, 1]) \
                  ) \
            for index in range(0, len(self.variablesConditionMayInclude))     ]);
        return F;

    def getFunctionToCheckWhetherNoPointsInTheBoxStatisfyCondition(self):
       
        def functToCheck(thisBox):
            #V~V~V~V~V~VV~V~V~V~V~VV~V~V~V~V~V~V~V~V~V~V~V~V~VV~V~V~V~V~VV~V
            # Statistical sampling to help speed of the forall-checking. If we 
            # find one counter-example to the forall-claim, then there is no
            # reason to do the expensive z3 check... 
            #===============================================================
            for thisSample in range(0, config.defaultValues.numberOfStatisticalSamplesToTakeIn_getFunctionToCheckWhetherNoPointsInTheBoxStatisfyCondition):
                randomVector = getRandomVectorInBox(thisBox).reshape(getDimensionOfBox(thisBox), 1);
                if(not any([thisCondition.pythonFormatEvaluation(randomVector) for thisCondition in self.conditionsToBeConsistentWith]) ):
                    return False;                
            #^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^

            z3Solver = self.conditionsToBeConsistentWith[0].z3Solver;
            quickResetZ3Solver(z3Solver);

            # disjunctive normal form - each element in the list is a clause which we or-together....
            formulaToCheck = \
                (\
                    z3.ForAll( self.variablesConditionMayInclude , \
                        z3.Implies(\
                            self._helper_getFunctionToCheckWhetherNoPointsInTheBoxStatisfyCondition_convertBoxToFormulaConstraints(thisBox), \
                            z3.Or([x.z3FormattedCondition for x in self.conditionsToBeConsistentWith]) \
                        ) \
                    ) \
                );
            z3Solver.add(formulaToCheck);
            verdict = (z3Solver.check() == z3.z3.sat);
            quickResetZ3Solver(z3Solver);

            return verdict;

        # NOTE: <<<<<<<<<<<<<<<<<<<<<<<<< notice I AM NOT NEGATING functToCheck <<<<<<<<<<<<
        return self.setupProperFeedToFunctionforThisQuestionType(functToCheck);



    def formConditionToSatisfy_hackyCopyFrom_Question_Probabilistic(self):
        # This function returns FALSE when it found a random sample that statisfies the DNF in question,
        # and returns TRUE when it DOES NOT
        numberOfSamples=\
            config.defaultValues.numberOfStatisticalSamplesToTakeIn_numberOfStatisticalSamplesToTakeIn_getFunctionToCheckWhetherNoPointsInTheBoxStatisfyCondition
    
        def statisticalCheckForallConditionFails(thisBox, thisCondition):
            # Statistically checking that thisCondition FAILS EVERYWHERE in   #<<<<<<<<<<<<<<<<<<<<<<<<<<< NOTICE IT TRIES TO CHECK FOR FAILURE
            # the box.
            for thisSampleIndex in range(0, numberOfSamples):
                randomVector = getRandomVectorInBox(thisBox).reshape(getDimensionOfBox(thisBox), 1);
                if(thisCondition.pythonFormatEvaluation(randomVector)):
                    return False;
            return True;
        
        return (lambda thisBox : all([\
                statisticalCheckForallConditionFails(thisBox, thisCondition) \
                for thisCondition in self.conditionsToBeConsistentWith]));

    # Below, numberOfSamples is not used
    def formConditionToSatisfy(self, numberOfSamples=config.defaultValues.formConditionToSatisfy_statistical_numberOfSamples):
        # disjunctive normal form - each element in the list is a clause which we or-together....
        mainCondition = \
            (lambda thisBox : any([x.existsMemberOfBoxSatifyingCondition(thisBox) for x in self.conditionsToBeConsistentWith]));
    
        def functToGive(thisBox):
            # In the case where random sampling could not find a satisfying assigment, we still need
            # to do a formal check that no such assignment exists. If, however, random sampling
            # found it is possible to satisfy, no formal checking is needed. As we do elsewhere, the 
            # goal of this function is TO RETURN FALSE WHEN AN ASSIGNEMNT IS TRUE, AND TRUE WHEN IT
            # DOES NOT.
            if(self.formConditionToSatisfy_hackyCopyFrom_Question_Probabilistic()(thisBox)):
                return (not mainCondition(thisBox)); #<<<<<<<<<<<<<<<<<<<<<<<<< NOTICE THE NOT
            else:
                return False;

        return  functToGive;

class Question_Probabilistic(Question_WayConditionIsChecked):

    def getFunctionToCheckWhetherNoPointsInTheBoxStatisfyCondition(self):
        return None;

    def formConditionToSatisfy(self, \
        numberOfSamples=config.defaultValues.formConditionToSatisfy_statistical_numberOfSamples):
        requires(isinstance(numberOfSamples, int) or (numberOfSamples == None));
        requires( ( numberOfSamples == None) or (numberOfSamples > 0));
    
        # We have to explicitly pass in numberOfSamples below since it is potentially
        # modified in the function, and thus a variable local to this local-function.
        def statisticalCheckForallConditionFails(thisBox, thisCondition, numberOfSamples):
            # Statistically checking that thisCondition FAILS EVERYWHERE in   #<<<<<<<<<<<<<<<<<<<<<<<<<<< NOTICE IT TRIES TO CHECK FOR FAILURE
            # the box.
            if(numberOfSamples == None):
                numberOfSamples = (2 * getDimensionOfBox(thisBox)) + 1;
            for thisSampleIndex in range(0, numberOfSamples):
                randomVector = getRandomVectorInBox(thisBox).reshape(getDimensionOfBox(thisBox), 1);
                if(thisCondition.pythonFormatEvaluation(randomVector)):
                    return False;  # ssh-rsa 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 abc@defg
            return True;
        
        return (lambda thisBox : all([\
                statisticalCheckForallConditionFails(thisBox, thisCondition, numberOfSamples) \
                for thisCondition in self.conditionsToBeConsistentWith]));


    

###############################################################################

###############################################################################

###############################################################################


class QuestionClass_What_Do_You_Do_When(Question_OutputDomain, Question_FormalUniversalQuant):
    getFunctionToCheckWhetherNoPointsInTheBoxStatisfyCondition = Question_FormalUniversalQuant.getFunctionToCheckWhetherNoPointsInTheBoxStatisfyCondition;
    pass;


class QuestionClass_When_Do_You(Question_InputDomain, Question_FormalUniversalQuant):
    getFunctionToCheckWhetherNoPointsInTheBoxStatisfyCondition = Question_FormalUniversalQuant.getFunctionToCheckWhetherNoPointsInTheBoxStatisfyCondition;
    pass;


class QuestionClass_What_Are_The_Circumstances_In_Which(Question_JointInputAndOutputDomain, Question_FormalUniversalQuant):
    getFunctionToCheckWhetherNoPointsInTheBoxStatisfyCondition = Question_FormalUniversalQuant.getFunctionToCheckWhetherNoPointsInTheBoxStatisfyCondition;
    pass;


class QuestionClass_What_Do_You_Ussually_Do_When(Question_OutputDomain, Question_Probabilistic):
    getFunctionToCheckWhetherNoPointsInTheBoxStatisfyCondition = Question_Probabilistic.getFunctionToCheckWhetherNoPointsInTheBoxStatisfyCondition;
    pass;


class QuestionClass_When_Do_You_Ussually(Question_InputDomain, Question_Probabilistic):
    getFunctionToCheckWhetherNoPointsInTheBoxStatisfyCondition = Question_Probabilistic.getFunctionToCheckWhetherNoPointsInTheBoxStatisfyCondition;
    pass;


class QuestionClass_What_Are_The_Usual_Circumstances_In_Which(Question_JointInputAndOutputDomain, Question_Probabilistic):
    getFunctionToCheckWhetherNoPointsInTheBoxStatisfyCondition = Question_Probabilistic.getFunctionToCheckWhetherNoPointsInTheBoxStatisfyCondition;
    pass;







