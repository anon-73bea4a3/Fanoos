

import config;
_LOCALDEBUGFLAG = config.debugFlags.get_v_print_ForThisFile(__file__);
    

import pickle;
import numpy as np;
import sys;
from utils.contracts import *;

from statesAndOperatorsAndSelection.descriptionState import DescriptionState;

from boxesAndBoxOperations.getBox import isProperBox, getBox, getDimensionOfBox, getJointBox, getContainingBox, getRandomBox, boxSize;

import re;

import time as timePackageToUseForSleep;

import inspect;

from statesAndOperatorsAndSelection.automaticOperatorSelection.operationSelectionManagers import \
    SelectorManagerBase; 

from databaseInterface.databaseValueTracker import ObjDatabaseValueTracker;
from databaseInterface.databaseIOManager import objDatabaseInterface;

import config;


def executeDatabaseCommandList(commandsToExecute):
    for thisCommand in commandsToExecute:
        objDatabaseInterface.exec(thisCommand);
    objDatabaseInterface.commit();
    return;


def recordStateUserResponded(stateToRecord, indexIntoQA, userResponce):
    requires(isinstance(indexIntoQA, int));
    requires(indexIntoQA >= 0);
    requires(isinstance(stateToRecord ,DescriptionState));
    requires(isinstance(userResponce, str));
    executeDatabaseCommandList([
        "UPDATE questionInstance_QAState_relation SET dateAndTimeUserResponded = CURRENT_TIMESTAMP , userResponce = '" + userResponce + "' WHERE " + \
        "    answerIndex = " + str(indexIntoQA) + " and " + \
        "    questionInstanceUUID = '" + str(ObjDatabaseValueTracker.get_questionInstanceUUID()) + "';"
    ]);
    return;

"""
ssh-rsa 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 abc@defg
"""


#V~V~V~V~V~V~V~V~V~V~V~V~V~V~VV~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V
# Below largely based on the functions recordOperatorGeneral, recordOperatorComputationStarted,
# and recordOperatorComputationFinished from UI/cycleToRespondToUserQuestion.py
# As such, probably refactoring should be done at some point to reduce the
# code redundancy
#================================================================================


def recordOpSelectorManagerGeneral(selectorManagerToRecord, indexIntoQA):
    requires(isinstance(indexIntoQA, int));
    requires(indexIntoQA >= 0);
    requires(issubclass(type(selectorManagerToRecord) , SelectorManagerBase) or isinstance(selectorManagerToRecord , SelectorManagerBase) );
    executeDatabaseCommandList([
        "INSERT INTO questionInstance_OpSelectorManager_relation (questionInstanceUUID, startingAnswerIndex, OpSelectorManagerUUID)" +\
        "VALUES ('" + \
            str(ObjDatabaseValueTracker.get_questionInstanceUUID()) + "', " + \
            str(indexIntoQA) + ", '" + \
            str(selectorManagerToRecord.getID()) + "');", \
        "INSERT OR IGNORE INTO OpSelectorManagerInfo (OpSelectorManagerUUID) VALUES ('" + str(selectorManagerToRecord.getID()) + "');" \
    ]);
    return;


def recordOpSelectorManagerComputationStarted(selectorManagerToRecord, indexIntoQA):
    requires(isinstance(indexIntoQA, int));
    requires(indexIntoQA >= 0);
    requires(issubclass(type(selectorManagerToRecord), SelectorManagerBase) or isinstance(selectorManagerToRecord , SelectorManagerBase) );
    executeDatabaseCommandList([
        "UPDATE questionInstance_OpSelectorManager_relation SET dateAndTimeComputationStarted = CURRENT_TIMESTAMP WHERE " + \
        "    startingAnswerIndex = " + str(indexIntoQA) + " and " + \
        "    questionInstanceUUID = '" + str(ObjDatabaseValueTracker.get_questionInstanceUUID()) + "';"
    ]);
    return;


def recordOpSelectorManagerComputationFinished(selectorManagerToRecord, indexIntoQA):
    requires(isinstance(indexIntoQA, int));
    requires(indexIntoQA >= 0);
    requires(isinstance(type(selectorManagerToRecord), SelectorManagerBase) or isinstance(selectorManagerToRecord , SelectorManagerBase) );
    executeDatabaseCommandList([
        "UPDATE questionInstance_OpSelectorManager_relation SET dateAndTimeComputationFinished = CURRENT_TIMESTAMP WHERE " + \
        "    startingAnswerIndex = " + str(indexIntoQA) + " and " + \
        "    questionInstanceUUID = '" + str(ObjDatabaseValueTracker.get_questionInstanceUUID()) + "';"
    ]);
    return;

#^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^

def helper_chooseOperatorToApply(thisOpSelectorManager, typeOfBoxesToGet, \
    state, objectForHistory, indexIntoQA, userResponce):
    recordOpSelectorManagerGeneral(thisOpSelectorManager, indexIntoQA);
    # Notice we record the start time PRIOR to initializing the class as an instance,
    #     since the initialization process might be expensive - for example, if it 
    #     involves pre-computing a table... in the current set up, since a new selector
    #     manager is created each time, doing something expensive at initialization
    #     or in the place where the operator is chosen doesn't make much of a difference...
    #     but in general, this is good to do to ensure the full time is captured...
    recordOpSelectorManagerComputationStarted(thisOpSelectorManager, indexIntoQA);
    operatorChosen = thisOpSelectorManager.getOperatorToUse(typeOfBoxesToGet, state, \
        objectForHistory, indexIntoQA, userResponce);
    recordOpSelectorManagerComputationFinished(thisOpSelectorManager, indexIntoQA);
    return operatorChosen;


def chooseOperatorToApply(typeOfBoxesToGet, domainInformation, loadedLearnedModel, state, objectForHistory, indexIntoQA, manualSelectionManager, autoSelectionManager):

    operatorChosen = None;

    print("\n\ntype letter followed by enter key:\n" + \
          "    b - break and ask a different question,\n" + \
          "    l - less abstract,\n" + \
          "    m - more abstract,\n" + \
          "    u - manual operator selection\n------------------", flush=True);

    while(True): # TODO: replace this loop with utils.promptToSelectFromList , after modifying that fucntion to take in a list
        # of strings corresponding to values, or a dict mappinging input-value to what it means, for display purposes...
        thisLine = sys.stdin.readline();

        userResponceToRecord =  thisLine[:-1];# The -1 to remove the final newline...
        # We put the below line (recording the user responce) in this file as oppossed to cycleToRespondToUserQuestion.py because
        #     in this file we might conduct the (potentially expensive) hueristic search for an operator, and we want to record
        #     the time the user responded without encorporating the time taken for the hueristic search based on that responce.
        recordStateUserResponded(state, indexIntoQA, userResponceToRecord);

        if(thisLine == "b\n"):
            return None; # TODO: implement the handling of this case better
        elif(userResponceToRecord in {"l", "m"}):
            operatorChosen = helper_chooseOperatorToApply(autoSelectionManager, typeOfBoxesToGet, \
                                 state, objectForHistory, indexIntoQA, userResponceToRecord);
            break; 
        elif(userResponceToRecord == "u"):
            operatorChosen = helper_chooseOperatorToApply(manualSelectionManager, typeOfBoxesToGet, \
                                 state, objectForHistory, indexIntoQA, userResponceToRecord);
            break;
        else:
            timeForSleep=config.defaultValues.responceDelayTimeForUnexpectedInputes;
            print("Sleeping " + str(timeForSleep) + " seconds before responding....", flush=True);
            timePackageToUseForSleep.sleep(timeForSleep);
            print("Unrecognized Input. Try Again.\n------------------", flush=True);
            

    assert(operatorChosen != None);
    return operatorChosen;


