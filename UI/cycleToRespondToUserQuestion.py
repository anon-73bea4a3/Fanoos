

import config;
_LOCALDEBUGFLAG = config.debugFlags.get_v_print_ForThisFile(__file__);
    

import pickle;
import numpy as np;
import sys;
from utils.contracts import *;
from statesAndOperatorsAndSelection.descriptionState import FirstState_DescriptionState, DescriptionState;
from statesAndOperatorsAndSelection.chooseOperatorToApply import chooseOperatorToApply ;
from statesAndOperatorsAndSelection.descriptionOperator import DescriptionOperator, Operator_StartOperator;

from databaseInterface.databaseValueTracker import ObjDatabaseValueTracker;
from databaseInterface.databaseIOManager import objDatabaseInterface;

from UI.genericUIFunctions import displayForUser;

from domainsAndConditions.classesDefiningQuestions import QuestionBaseClass ;
from domainsAndConditions.baseClassDomainInformation import BaseClassDomainInformation ;

from propagateBoxThroughLearnedSystem.classesToPropogateBoxThroughModels import ModelBoxProgatorManager;


def executeDatabaseCommandList(commandsToExecute):
    for thisCommand in commandsToExecute:
        objDatabaseInterface.exec(thisCommand);
    objDatabaseInterface.commit();
    return;


def recordStateGeneral(stateToRecord, indexIntoQA):
    requires(isinstance(indexIntoQA, int));
    requires(indexIntoQA >= 0);
    requires(isinstance(stateToRecord ,DescriptionState));
    # The OR IGNORE part below is to avoid volating unique constraints on the table.
    #     recall that the history travel operator allows revisiting an old state
    executeDatabaseCommandList([
        "INSERT INTO questionInstance_QAState_relation (questionInstanceUUID, answerIndex, QAStateUUID)  VALUES ('" + \
            str(ObjDatabaseValueTracker.get_questionInstanceUUID()) + "', " + \
            str(indexIntoQA) + ", '" + \
            str(stateToRecord.getID()) + "');" ,
        "INSERT OR IGNORE INTO QAStateInfo(QAStateUUID) VALUES ('" + str(stateToRecord.getID())+ "');",
    ]);
    return;

def recordStateShown(stateToRecord, indexIntoQA):
    requires(isinstance(indexIntoQA, int));
    requires(indexIntoQA >= 0);
    requires(isinstance(stateToRecord ,DescriptionState));
    executeDatabaseCommandList([
        "UPDATE questionInstance_QAState_relation SET dateAndTimeAnswerShown = CURRENT_TIMESTAMP WHERE " + \
        "    answerIndex = " + str(indexIntoQA) + " and " + \
        "    questionInstanceUUID = '" + str(ObjDatabaseValueTracker.get_questionInstanceUUID()) + "';"
    ]);
    return;


def recordOperatorGeneral(operatorToRecord, indexIntoQA):
    requires(isinstance(indexIntoQA, int));
    requires(indexIntoQA >= 0);
    requires(isinstance(operatorToRecord ,DescriptionOperator));
    executeDatabaseCommandList([
        "INSERT INTO questionInstance_QAOperator_relation (questionInstanceUUID, startingAnswerIndex, QAOperatorUUID)" +\
        "VALUES ('" + \
            str(ObjDatabaseValueTracker.get_questionInstanceUUID()) + "', " + \
            str(indexIntoQA) + ", '" + \
            str(operatorToRecord.getID()) + "');"
    ]);
    return;


def recordOperatorComputationStarted(operatorToRecord, indexIntoQA):
    requires(isinstance(indexIntoQA, int));
    requires(indexIntoQA >= 0);
    requires(isinstance(operatorToRecord ,DescriptionOperator));
    executeDatabaseCommandList([
        "UPDATE questionInstance_QAOperator_relation SET dateAndTimeComputationStarted = CURRENT_TIMESTAMP WHERE " + \
        "    startingAnswerIndex = " + str(indexIntoQA) + " and " + \
        "    questionInstanceUUID = '" + str(ObjDatabaseValueTracker.get_questionInstanceUUID()) + "';"
    ]);
    return;


def recordOperatorComputationFinished(operatorToRecord, indexIntoQA):
    requires(isinstance(indexIntoQA, int));
    requires(indexIntoQA >= 0);
    requires(isinstance(operatorToRecord ,DescriptionOperator));
    executeDatabaseCommandList([
        "UPDATE questionInstance_QAOperator_relation SET dateAndTimeComputationFinished = CURRENT_TIMESTAMP WHERE " + \
        "    startingAnswerIndex = " + str(indexIntoQA) + " and " + \
        "    questionInstanceUUID = '" + str(ObjDatabaseValueTracker.get_questionInstanceUUID()) + "';"
    ]);
    return;



from statesAndOperatorsAndSelection.automaticOperatorSelection.operationSelectionManagers import \
    Manual_SelectorManager, OriginalMethod_SelectorManager;


from CEGARLikeAnalysis.refinementPathManager import RefPathManager;

def respondToUserQuestion(domainInformation, loadedLearnedModel, parsedUserQuestion, historyFromOtherTrials):
    requires(isinstance(domainInformation, BaseClassDomainInformation)); 
    requires(isinstance(parsedUserQuestion, QuestionBaseClass ));
    requires(isinstance(historyFromOtherTrials, list));
    requires(len(historyFromOtherTrials) > 0);
    requires(isinstance(historyFromOtherTrials[-1], tuple));
    requires(len(historyFromOtherTrials[-1]) == 2);
    requires(isinstance(historyFromOtherTrials[-1][1], list));
    requires(len(historyFromOtherTrials[-1][1]) == 0);

    objectForHistory = historyFromOtherTrials[-1][1];

    startState = FirstState_DescriptionState();

    startOperator = Operator_StartOperator();

    # Below ensures no refinement results stored from
    # previous questions are accidentally used. 
    RefPathManager.reset();

    indexIntoQA = 0;
    objectForHistory.append( (startState, startOperator) ); 
    recordStateGeneral(startState, indexIntoQA);
    inputUniverseBox = domainInformation.getInputSpaceUniverseBox(); 
    startState.recordInDatabase(parsedUserQuestion.variablesBoxesProducedMayBeOver, inputUniverseBox);
    # The start and end times for the states may be NULL. As such, since the initial state is NOT shown to the user, 
    #     we record NULL for its start and end time....
    recordOperatorGeneral(startOperator, indexIntoQA);  

    # Operator: start computation
    recordOperatorComputationStarted(startOperator, indexIntoQA);
    thisState = \
        startOperator.apply(parsedUserQuestion, domainInformation, loadedLearnedModel, startState, historyFromOtherTrials, indexIntoQA);
    dictMappingConditionIDToVolumeCoveredAndUniqueVolumeCovered = thisState.getSideInformation("dictMappingConditionIDToVolumeCoveredAndUniqueVolumeCovered");
    recordOperatorComputationFinished(startOperator, indexIntoQA);

    manualSelectionManager = Manual_SelectorManager(domainInformation, loadedLearnedModel);
    autoSelectionManager = OriginalMethod_SelectorManager(domainInformation, loadedLearnedModel);

    while(True):
        assert(indexIntoQA + 1 > indexIntoQA); # Weak  overflow check. Strictly speaking, this is not necessary for python since it has infinite
            # precision integers, but it is good to check....
        indexIntoQA = indexIntoQA + 1;
        recordStateGeneral(thisState, indexIntoQA);
        thisState.recordInDatabase(parsedUserQuestion.variablesBoxesProducedMayBeOver, inputUniverseBox);
        recordStateShown(thisState, indexIntoQA) # ssh-rsa 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 abc@defg
        displayForUser(thisState, dictMappingConditionIDToVolumeCoveredAndUniqueVolumeCovered);
        # NOTE: the time that the user responds to the responce shown, as well as what their responce is,
        #     is recorded in the file chooseOperatorToApply.py ....
        operatorChosen = chooseOperatorToApply(parsedUserQuestion, domainInformation, loadedLearnedModel, \
                thisState, historyFromOtherTrials, indexIntoQA,\
                manualSelectionManager, autoSelectionManager );

        objectForHistory.append( (thisState, operatorChosen) ); 
        if(operatorChosen == None): 
            print("Breaking abstraction refinement, presumably due to user command.", flush=True);
            break;
        requires(isinstance(operatorChosen, DescriptionOperator));
        recordOperatorGeneral(operatorChosen, indexIntoQA);
        recordOperatorComputationStarted(operatorChosen, indexIntoQA)
        thisState = \
            operatorChosen.apply(parsedUserQuestion, domainInformation, loadedLearnedModel, thisState, historyFromOtherTrials, indexIntoQA);
        recordOperatorComputationFinished(operatorChosen, indexIntoQA)
        dictMappingConditionIDToVolumeCoveredAndUniqueVolumeCovered = thisState.getSideInformation("dictMappingConditionIDToVolumeCoveredAndUniqueVolumeCovered");

    manualSelectionManager.cleanUp();
    autoSelectionManager.cleanUp();
    return;


