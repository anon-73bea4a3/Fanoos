

import config;
_LOCALDEBUGFLAG = config.debugFlags.get_v_print_ForThisFile(__file__);
    

import pickle;
import numpy as np;
import sys;
from utils.contracts import *;

import re;

import uuid;

from statesAndOperatorsAndSelection.descriptionState import DescriptionState, FirstState_DescriptionState;
from domainsAndConditions.baseClassDomainInformation import BaseClassDomainInformation;
from domainsAndConditions.classesDefiningQuestions import QuestionBaseClass;
from descriptionGeneration.generateDescription import generateDescription;

from propagateBoxThroughLearnedSystem.classesToPropogateBoxThroughModels import ModelBoxProgatorManager;

from databaseInterface.databaseValueTracker import ObjDatabaseValueTracker;
from databaseInterface.databaseIOManager import objDatabaseInterface, executeDatabaseCommandList;

from CEGARLikeAnalysis.CEGARLikeAnalysisMain import timingInfoForLocation_2e048534_BoxTest ; 

from utils.distributionStatics import distributionStatics;

import time as timePackageToUseForSleep;

import config;

class DescriptionOperator():

    def recordTimeStats(self, timeMeasurements, locationLabel):
        requires(isinstance(timeMeasurements, list));
        requires(all([isinstance(x, float) for x in timeMeasurements]));
        requires(isinstance(locationLabel, str));
        requires(len(locationLabel) > 0);
        # The below requires basically checks that the location label contains a UUID...
        requires(re.match("^.*[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}.*$", locationLabel) is not None);

        def helper_recordInDatabse(fieldName, valueToRecord):
            requires(isinstance(fieldName, str));
            requires(len(fieldName) > 0);
            commandToExecute = \
                "INSERT INTO QAOperatorValues (" + \
                "    questionInstanceUUID, QAOperatorUUID, startingAnswerIndex, fieldName, fieldValue ) VALUES (" + \
                "\'" + ObjDatabaseValueTracker.get_questionInstanceUUID() + "\', " + \
                "\'" + self.getID() + "\', " + \
                str(self.indexIntoQA)  + ", " + \
                "\'" + fieldName + "\', ? );";
            objDatabaseInterface.interfaceBleed_insertValuesForBlob(\
                commandToExecute, [valueToRecord]  );
            
        helper_recordInDatabse("allTimings:" + locationLabel, timeMeasurements);
        distributionStaticsForTimeValues = distributionStatics(timeMeasurements);
        baseLabelToUse = "timingStats:" + locationLabel + ":";
        for thisKey in distributionStaticsForTimeValues:
            if((distributionStaticsForTimeValues["numberOfDataPoints"] == 0) and (thisKey != "numberOfDataPoints")):
                continue;
            if((distributionStaticsForTimeValues["numberOfDataPoints"] == 1) and (thisKey not in {"numberOfDataPoints", "median"})):
                continue;
            helper_recordInDatabse(baseLabelToUse + thisKey, \
                                   distributionStaticsForTimeValues[thisKey]);
        objDatabaseInterface.commit();
        return



    @staticmethod
    def getID():
        uuid = "1b29f22c-eaf8-458a-b419-ce38c152df8e";
        return uuid;

    def setID(self):
        raise Exception("""This class does not support assigning new UUIDs.""");

    def __init__(self):
        raise Exception("Child classes must overwrite...");
        return;

    def internal_apply(self, parsedUserQuestion, domainInformation, loadedLearnedModel, state, objectForHistory):
        raise Exception("Child classes must overwrite...");
        return;   

    def apply(self, parsedUserQuestion, domainInformation, loadedLearnedModel, state, objectForHistory, indexIntoQA):
        requires(isinstance(parsedUserQuestion, QuestionBaseClass));
        requires(isinstance(domainInformation, BaseClassDomainInformation));
        requires(isinstance(loadedLearnedModel, ModelBoxProgatorManager));
        requires(isinstance(state, DescriptionState));
        requires(isinstance(objectForHistory, list));
        requires(isinstance(indexIntoQA, int));
        requires(indexIntoQA >= 0);

        self.indexIntoQA = indexIntoQA;
        stateToReturn = \
            self.internal_apply(parsedUserQuestion, domainInformation, loadedLearnedModel, state, objectForHistory);

        ensures(isinstance(stateToReturn, DescriptionState));
        return stateToReturn;

import traceback;

import cmd;
from UI.genericUIFunctions import myLinuxStyleMoreCommand, displayForUser, promptToSelectFromList;


class Operator_ManualPredicateReview(DescriptionOperator):

    class ManualPredicateReviewPrompt(cmd.Cmd):
        prompt="(Fanoos: Manual Predicate Review)"; 

        @staticmethod
        def _standardWait():
            timeForSleep=config.defaultValues.responceDelayTimeForUnexpectedInputes;
            print("Sleeping " + str(timeForSleep) + " seconds before responding....", flush=True);
            timePackageToUseForSleep.sleep(timeForSleep);
            return;

        def default(*x, **kwargs):
            __class__._standardWait();
            cmd.Cmd.default(*x, **kwargs);
            return;

        def emptyline(*x, **kwargs):
            __class__._standardWait();
            print("Ignoring Empty Line.", flush=True);
            return;


        """
ssh-rsa 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 abc@defg
"""

        def secondInit(self, parsedUserQuestion, domainInformation, loadedLearnedModel, state, objectForHistory, hackyListToContainStateToReturn):
            requires(isinstance(hackyListToContainStateToReturn, list));
            requires(len(hackyListToContainStateToReturn) == 0);
            self.parsedUserQuestion = parsedUserQuestion;
            self.domainInformation = domainInformation;
            self.loadedLearnedModel = loadedLearnedModel;
            self.currentState = state;
            self.objectForHistory = objectForHistory;
            self.historyForThisQuestion = self.objectForHistory[-1][1];
            self.statesVisitedInThisQuestion = [x[0].getID() for x in self.historyForThisQuestion];
            self.hackyListToContainStateToReturn =  hackyListToContainStateToReturn;
            self.newlyAllowedPredicates = set();
            self.newlyDisallowedPredicate = set();
            self.allNamedPredicatesInDomain = self.domainInformation.getBaseConditions().copy();
            self.UUIDsOfAllNamedPredicatesInDomain = [x.getID() for x in self.allNamedPredicatesInDomain];
            self.infoOnPredicatesThatOccurInCurrentState = self.forInternalUse_getNamedPredicateUUIDsInCurrentState();
            return;

        def do_exit(self, arg):
            requires(isinstance(self.hackyListToContainStateToReturn, list));
            requires(len(self.hackyListToContainStateToReturn) == 0);
            newState = DescriptionState();
            print("Updating allowed/disallowed predicates. NOTE: changes will not be reflected " + \
                  "until the next time a new description is generated (such as by requesting a " + \
                  "description that is more abstract as oppossed to one that is less abstract).", flush =True);
            newState.setDescription(self.currentState.getDescription());
            newState.setContinuationForRawInputDomainBoxes(self.currentState.getContinuationForRawInputDomainBoxes());
            newState.setContinuationToBoxesToDescribe(self.currentState.getContinuationToBoxesToDescribe());
            newState.sideInformationDict = self.currentState.sideInformationDict;
            newState.internalDictionary["mostRecentOperatorParameters"] = self.currentState.getCopyOfParameters();
            newState.internalDictionary["mostRecentOperatorParameters"]["removedPredicates"].difference_update(\
                self.newlyAllowedPredicates);
            newState.internalDictionary["mostRecentOperatorParameters"]["removedPredicates"].update(\
                self.newlyDisallowedPredicate );
            self.hackyListToContainStateToReturn.append(newState);
            ensures(isinstance(self.hackyListToContainStateToReturn, list));
            ensures(len(self.hackyListToContainStateToReturn) == 1);
            return True;

        def forInternalUse_getNamedPredicateUUIDsInCurrentState(self):
            commandToExecute = "SELECT A.childUUID as predUUID, count(*) as numOccurances " + \
                "FROM QAStateValues as A " + \
                "WHERE  " + \
                "    (A.fieldName = 'd:root' or A.fieldName = 'd:parent_child') " + \
                "    AND (A.childUUID NOT LIKE \"frozenset%\") " + \
                "    AND QAStateUUID = \"" + self.currentState.getID() + "\" " + \
                "    AND EXISTS (SELECT * FROM predicateInfo WHERE predicateUUID=childUUID) GROUP BY childUUID; ";
            results = objDatabaseInterface.exec(commandToExecute);
            valuesToReturn = [(x["numOccurances"], 
                              x["predUUID"], 
                              str([y for y in self.allNamedPredicatesInDomain if y.getID() == x["predUUID"]][0])    ) \
                             for x in results ];
            valuesToReturn.sort(reverse=True); # I reverse them so to show the most frequently occuring predicates first.
            return valuesToReturn;


        def do_list_named_predicates_in_current_state(self, args):
            print("================", flush=True);
            print("predicate UUID,\tnumber of occurances in description,\tstring description of predicate", flush=True);
            valuesToPrint =  self.infoOnPredicatesThatOccurInCurrentState;
            valuesToPrint = [ (str(x[1]) + "\t" + str(x[0]) + "\t" + str(x[2])) for x in valuesToPrint];
            myLinuxStyleMoreCommand(valuesToPrint);
            return;


        def forInternalUse_completeState(self, thisString, setToRemove):
            requires(isinstance(thisString, str));
            return [x for x in self.UUIDsOfAllNamedPredicatesInDomain if (str(x).startswith(thisString) and (x not in setToRemove))];

        def do_print_current_state(self, args):
            displayForUser(self.currentState, \
                self.currentState.getSideInformation("dictMappingConditionIDToVolumeCoveredAndUniqueVolumeCovered")\
            ); # there should only be one state - though it may have been visited multiple
            # times - that has the user-specified UUID;
            return;
 
        def do_list_disallowed_predicates(self, args):

            def getPredDescriptionGivenUUID(thisUUID):
                return [y for y in self.allNamedPredicatesInDomain if y.getID() == thisUUID][0];

            originalDisallowed = self.currentState.internalDictionary[\
                                     "mostRecentOperatorParameters"]["removedPredicates"];
            originalDisallowed = [ (x + "\t" + str(getPredDescriptionGivenUUID(x))) for x in originalDisallowed.difference(self.newlyAllowedPredicates)];
            newlyDisallowed = [ ("newly disallowed: " + x + "\t" + str(getPredDescriptionGivenUUID(x))) for x in self.newlyDisallowedPredicate];
            print("===================\nDisallowed predicates:\npredicate UUID,\tstring description of predicate", flush=True);
            myLinuxStyleMoreCommand(newlyDisallowed + originalDisallowed);
            return;

        def do_list_allowed_predicates(self, args):

            def getPredDescriptionGivenUUID(thisUUID):
                return [y for y in self.allNamedPredicatesInDomain  if y.getID() == thisUUID][0];

            originalAllowed = set(self.UUIDsOfAllNamedPredicatesInDomain ).difference(self.currentState.internalDictionary[\
                                     "mostRecentOperatorParameters"]["removedPredicates"]);
            originalAllowed = [ (x + "\t" + str(getPredDescriptionGivenUUID(x))) for x in originalAllowed.difference(self.newlyDisallowedPredicate)];
            newlyAllowed = [ ("newly disallowed: " + x + "\t" + str(getPredDescriptionGivenUUID(x))) for x in self.newlyAllowedPredicates];
            print("===================\nDisallowed predicates:\npredicate UUID,\tstring description of predicate", flush=True);
            myLinuxStyleMoreCommand(newlyAllowed + originalAllowed);
            return;


        def do_allow_predicate(self, args):
            args = args.replace(" " , "");
            if(args not in self.UUIDsOfAllNamedPredicatesInDomain):
                print("Error: allow_predicate requires one argument: the UUID of the predicate to disallow. However, " + \
                      " the argument(s) provided do not seem to be a UUID for a predicate in the domain.", flush=True);
            originallyDisallowed = self.currentState.internalDictionary[\
                                    "mostRecentOperatorParameters"]["removedPredicates"];
            originallyAllowed = set(self.UUIDsOfAllNamedPredicatesInDomain).difference(originallyDisallowed);
            if(args in originallyAllowed):
                print("Predicate that was requested to be made newly allowed was already allowed. Doing nothing.", flush=True);
                return;
            self.newlyAllowedPredicates.update([args]);
            self.newlyDisallowedPredicate.difference_update([args]);
            ensures(args in self.newlyAllowedPredicates);
            ensures(args not in self.newlyDisallowedPredicate);
            ensures(self.newlyAllowedPredicates.issubset(self.UUIDsOfAllNamedPredicatesInDomain));
            ensures(self.newlyDisallowedPredicate.issubset(self.UUIDsOfAllNamedPredicatesInDomain));
            ensures(len(self.newlyAllowedPredicates.difference(self.newlyDisallowedPredicate)) ==
                len(self.newlyAllowedPredicates)); # i.e., that the sets are disjiont...
            return


        def complete_allow_predicate(s, text, line, start_index, end_index):
            try:
                originalAllowed = set(s.UUIDsOfAllNamedPredicatesInDomain ).difference(s.currentState.internalDictionary[\
                                     "mostRecentOperatorParameters"]["removedPredicates"]);
                return s.forInternalUse_completeState(text, originalAllowed);
            except:
                errorMessageIndented = "    " + traceback.format_exc().replace("\n", "\n    ");
                print(errorMessageIndented, flush=True);
            return;


        def do_disallow_predicate(self, args):
            args = args.replace(" " , "");
            if(args not in self.UUIDsOfAllNamedPredicatesInDomain):
                print("Error: disallow_predicate requires one argument: the UUID of the predicate to disallow. However, " + \
                      " the argument(s) provided do not seem to be a UUID for a predicate in the domain.", flush=True);
            originallyDisallowed = self.currentState.internalDictionary[\
                                    "mostRecentOperatorParameters"]["removedPredicates"];
            originallyAllowed = set(self.UUIDsOfAllNamedPredicatesInDomain).difference(originallyDisallowed);
            if(args in originallyDisallowed):
                print("Predicate that was requested to be made newly disallowed was already disallowed. Doing nothing.", flush=True);
                return;
            self.newlyAllowedPredicates.difference_update([args]);
            self.newlyDisallowedPredicate.update([args]);
            ensures(args not in self.newlyAllowedPredicates);
            ensures(args in self.newlyDisallowedPredicate);
            ensures(self.newlyAllowedPredicates.issubset(self.UUIDsOfAllNamedPredicatesInDomain));
            ensures(self.newlyDisallowedPredicate.issubset(self.UUIDsOfAllNamedPredicatesInDomain));
            ensures(len(self.newlyAllowedPredicates.difference(self.newlyDisallowedPredicate)) ==
                len(self.newlyAllowedPredicates)); # i.e., that the sets are disjiont...
            return


        def complete_disallow_predicate(s, text, line, start_index, end_index):
            try:
                originalDisallowed = s.currentState.internalDictionary[\
                                     "mostRecentOperatorParameters"]["removedPredicates"];
                return s.forInternalUse_completeState(text, originalDisallowed);
            except:
                errorMessageIndented = "    " + traceback.format_exc().replace("\n", "\n    ");
                print(errorMessageIndented, flush=True);
            return;


    @staticmethod
    def getID():
        uuid = "8502c81c-1afb-4d6c-b910-05328c4350d1";
        return uuid;


    def __init__(self):
        assert(self.getID() == "8502c81c-1afb-4d6c-b910-05328c4350d1");
        return;

    def internal_apply(self, parsedUserQuestion, domainInformation, loadedLearnedModel, state, objectForHistory):
        hackyListToContainStateToReturn = [];
        operatorPrompt = self.ManualPredicateReviewPrompt();
        operatorPrompt.secondInit(parsedUserQuestion, domainInformation, loadedLearnedModel, state, objectForHistory, hackyListToContainStateToReturn);
        operatorPrompt.cmdloop();
        ensures(isinstance(hackyListToContainStateToReturn, list));
        ensures(len(hackyListToContainStateToReturn) == 1);
        return hackyListToContainStateToReturn[0];




class Operator_HistoryExamination(DescriptionOperator):

    class HistoryExaminationPrompt(cmd.Cmd):
        prompt="(Fanoos: History Travel)";

        @staticmethod
        def _standardWait():
            timeForSleep=config.defaultValues.responceDelayTimeForUnexpectedInputes;
            print("Sleeping " + str(timeForSleep) + " seconds before responding....", flush=True);
            timePackageToUseForSleep.sleep(timeForSleep);
            return;

        def default(*x, **kwargs):
            __class__._standardWait();
            cmd.Cmd.default(*x, **kwargs);
            return;

        def emptyline(*x, **kwargs):
            __class__._standardWait();
            print("Ignoring Empty Line.", flush=True);
            return;

        def secondInit(self, parsedUserQuestion, domainInformation, loadedLearnedModel, state, objectForHistory, hackyListToContainStateToReturn):
            requires(isinstance(hackyListToContainStateToReturn, list));
            requires(len(hackyListToContainStateToReturn) == 0);
            self.parsedUserQuestion = parsedUserQuestion;
            self.domainInformation = domainInformation;
            self.loadedLearnedModel = loadedLearnedModel;
            self.currentState = state;
            self.objectForHistory = objectForHistory;
            self.historyForThisQuestion = self.objectForHistory[-1][1];
            self.statesVisitedInThisQuestion = [x[0].getID() for x in self.historyForThisQuestion];
            self.hackyListToContainStateToReturn =  hackyListToContainStateToReturn;
            return;
         
        def do_show_history(self, args):
            if(len(args)> 0):
                print("warning: show_history does not take any arguments. Ignorng.", flush=True);
                return;
            def convertStatesToString(thisStateUUID):
                if(thisStateUUID == self.currentState.getID()):
                    return str(thisStateUUID) + "  <=== (current state)";
                else:
                    return str(thisStateUUID);

            myLinuxStyleMoreCommand([convertStatesToString(x) for x in self.statesVisitedInThisQuestion]);
            return;

        def forInternalUse_getStateMatchingUUID(self, args, functionName):
            requires(isinstance(functionName, str));
            requires(len(functionName) > 0);
            if(isinstance(args, list) and len(args) != 1):
                print(functionName + " requires one argument: the uuid of the state to print. Ignorng.", flush=True); 
                return None;
            thisUUID = args;
            if(isinstance(args, list)):
                thisUUID = args[0];
            stateWithUUID = [x[0] for x in self.historyForThisQuestion if x[0].getID() == thisUUID];
            if(len(stateWithUUID) == 0):
                print("No state has been visited while answering this question that has that UUID", flush=True);
                return None;
            # NOTE: len(stateWithUUID) may be greater than one, since we may, by travelling in the history,
            #     revisit the same state multiple times.
            return stateWithUUID[0];

        def do_print_state(self, args):
            thisState = self.forInternalUse_getStateMatchingUUID(args, "print_state");
            if(thisState != None):
                displayForUser(thisState, \
                    thisState.getSideInformation("dictMappingConditionIDToVolumeCoveredAndUniqueVolumeCovered")\
                ); # there should only be one state - though it may have been visited multiple
                # times - that has the user-specified UUID;
            return;


        def forInternalUse_completeState(self, thisString):
            requires(isinstance(thisString, str));
            return [x for x in self.statesVisitedInThisQuestion if (str(x).startswith(thisString))];

        def complete_print_state(s, text, line, start_index, end_index): 
            try:
                return s.forInternalUse_completeState(text);
            except:
                errorMessageIndented = "    " + traceback.format_exc().replace("\n", "\n    ");
                print(errorMessageIndented, flush=True);
            return;


        def do_return_to_state(self,args):
            thisState = self.forInternalUse_getStateMatchingUUID(args, "return_to_state");
            if(thisState != None):
                self.currentState = thisState;
            return;

        def complete_return_to_state(s, text, line, start_index, end_index):
            try:
                return s.forInternalUse_completeState(text);
            except:
                errorMessageIndented = "    " + traceback.format_exc().replace("\n", "\n    ");
                print(errorMessageIndented, flush=True);
            return;



        def do_exit(self, arg):
            requires(isinstance(self.hackyListToContainStateToReturn, list));
            requires(len(self.hackyListToContainStateToReturn) == 0);
            self.hackyListToContainStateToReturn.append(self.currentState);
            ensures(isinstance(self.hackyListToContainStateToReturn, list));
            ensures(len(self.hackyListToContainStateToReturn) == 1);
            return True;

         
    @staticmethod
    def getID():
        uuid = "38928f9a-0bef-4c48-92f9-f2a07c0831c2";
        return uuid;

    def __init__(self):
        assert(self.getID() == "38928f9a-0bef-4c48-92f9-f2a07c0831c2");
        return;

    def internal_apply(self, parsedUserQuestion, domainInformation, loadedLearnedModel, state, objectForHistory):
        hackyListToContainStateToReturn = [];
        operatorPrompt = self.HistoryExaminationPrompt();
        operatorPrompt.secondInit(parsedUserQuestion, domainInformation, loadedLearnedModel, state, objectForHistory, hackyListToContainStateToReturn);
        operatorPrompt.cmdloop();
        ensures(isinstance(hackyListToContainStateToReturn, list));
        ensures(len(hackyListToContainStateToReturn) == 1);
        return hackyListToContainStateToReturn[0];

import time;

class Operator_FreshGenerateAllBoxes(DescriptionOperator):
   
    @staticmethod
    def getID():
        uuid = "f883e116-398c-45b3-b0d4-638d3b875190";
        return uuid;


    def __init__(self):
        assert(self.getID() == "f883e116-398c-45b3-b0d4-638d3b875190");
        raise Exception("Child classes must override");
        return;

    def changeParameter(self, parsedUserQuestion, domainInformation, loadedLearnedModel, stateAppliedTo, objectForHistory):
        raise Exception("Child classes must override");
        ensures(isinstance(dictToReturn, dict));
        return dictToReturn;

    def internal_apply(self, parsedUserQuestion, domainInformation, loadedLearnedModel, stateAppliedTo, objectForHistory):
        newState = DescriptionState();
        dictOfNewParameters = self.changeParameter(parsedUserQuestion, domainInformation, loadedLearnedModel, stateAppliedTo, objectForHistory);
        newState.internalDictionary["mostRecentOperatorParameters"] = dictOfNewParameters;
        
        startTime =  time.process_time(); #location79441a4e-30de-4e64-9ac7-27b2b4b7b503_CEGARLikeAnalysis
        (listOfBoxesToDescribe, listMappingAxisIndexToVariableInQuestion, continuationFor_rawInputDomainBoxes) = \
        parsedUserQuestion.getBoxesToDescribe(loadedLearnedModel, newState );
        assert("function" in str(type(continuationFor_rawInputDomainBoxes)) );
        endTime =  time.process_time(); 
        self.recordTimeStats(timingInfoForLocation_2e048534_BoxTest, "location2e048534-c79b-4177-a79d-cc0ef71384d4_boxTest");
        self.recordTimeStats([endTime - startTime], "location79441a4e-30de-4e64-9ac7-27b2b4b7b503_CEGARLikeAnalysis");

        # Below, "BTD" stands for "Boxes To Describe"
        newState.setContinuationToBoxesToDescribe(\
            newState.generationContinuationToListOfBoxesUsingOutsideMemoryStorage("BTD_", listOfBoxesToDescribe)\
        );
        newState.setContinuationForRawInputDomainBoxes(continuationFor_rawInputDomainBoxes);

        conditionsList = domainInformation.getBaseConditions().copy();
        # filtering for those conditions that only discuss the relavent variables...
        conditionsList = [x for x in conditionsList 
            if x.relaventVariables().issubset(listMappingAxisIndexToVariableInQuestion)];
        conditionsList = [x for x in conditionsList \
            if x.getID() not in newState.internalDictionary["mostRecentOperatorParameters"]["removedPredicates"]];
    
        startTime = time.process_time(); # location6e888203-1d65-4f09-9601-fefc60dbb13a_generateDescription
        temp = generateDescription(\
                   listOfBoxesToDescribe, \
                   conditionsList, \
                   listMappingAxisIndexToVariableInQuestion, \
                   newState \
               );
        endTime = time.process_time();
        self.recordTimeStats([endTime - startTime], "location6e888203-1d65-4f09-9601-fefc60dbb13a_generateDescription"); 
        description = temp["description"];
        newState.setDescription(description);

        newState.setSideInformation("dictMappingConditionIDToVolumeCoveredAndUniqueVolumeCovered", \
            temp["dictMappingConditionIDToVolumeCoveredAndUniqueVolumeCovered"] );

        ensures(isinstance(newState, DescriptionState));
        return newState;


class Operator_StartOperator(Operator_FreshGenerateAllBoxes):
    """This operator just uses the parameters provided by the first state to 
       generate the boxes, etc., for the first state...."""
    
    @staticmethod 
    def getID():
        uuid = "31497f97-4fa9-4ecd-bbce-0b267d847bf4";
        return uuid


    def __init__(self):
        assert(self.getID() == "31497f97-4fa9-4ecd-bbce-0b267d847bf4");
        return;

    def changeParameter(self, parsedUserQuestion, domainInformation, loadedLearnedModel, stateAppliedTo, objectForHistory):
        requires(isinstance(stateAppliedTo ,FirstState_DescriptionState));
        dictToReturn = stateAppliedTo.getCopyOfParameters();
        ensures(isinstance(dictToReturn, dict));
        return dictToReturn;


class Operator_IncreaseAbstractionLevel():
    def __init__(self):
        raise NotImplementedError("Child classes must override.");
        return;

class Operator_DecreaseAbstractionLevel():
    def __init__(self):
        raise NotImplementedError("Child classes must override.");
        return;



class Operator_IAL_7b16e7a5(Operator_IncreaseAbstractionLevel, Operator_FreshGenerateAllBoxes):
    
    @staticmethod
    def getID():
        uuid = "4475bdbc-0fbf-4dbd-aa1c-c19b9c8bf1f0";
        return uuid;

    def __init__(self):
        assert(self.getID() == "4475bdbc-0fbf-4dbd-aa1c-c19b9c8bf1f0");
        return;

    def changeParameter(self, parsedUserQuestion, domainInformation, loadedLearnedModel, stateAppliedTo, objectForHistory):
        oldParameters = stateAppliedTo.getCopyOfParameters();
        parameters = stateAppliedTo.getCopyOfParameters();
        parameters["floatValueForBoxDivisionCutoff"] = oldParameters["floatValueForBoxDivisionCutoff"] * 2.0;
        parameters["limitOnNumberOfTimesToMerge"] = 0;
        parameters["splitOnlyOnRelaventVariables"] = False;
        parameters["precisionForMerging"] = max(1.0, oldParameters["precisionForMerging"] - 1.0); 
        parameters["numberOfSamplesToTry"] = oldParameters["numberOfSamplesToTry"];
        parameters["produceGreaterAbstraction"] = True; 
        parameters["exponentialComponent"] = oldParameters["exponentialComponent"] * 1.25;
        ensures(isinstance(parameters, dict));
        ensures(set(parameters.keys()).issuperset(oldParameters.keys()));
        return parameters;



class Operator_DAL_7b16e7a5(Operator_DecreaseAbstractionLevel, Operator_FreshGenerateAllBoxes):

    @staticmethod
    def getID():
        uuid = "e374ce99-215e-4cfd-8724-da1c2e6ace44";
        return uuid;


    def __init__(self):
        assert(self.getID() == "e374ce99-215e-4cfd-8724-da1c2e6ace44");
        return;

    def changeParameter(self, parsedUserQuestion, domainInformation, loadedLearnedModel, stateAppliedTo, objectForHistory):
        oldParameters = stateAppliedTo.getCopyOfParameters();
        parameters = stateAppliedTo.getCopyOfParameters();
        parameters["floatValueForBoxDivisionCutoff"] = oldParameters["floatValueForBoxDivisionCutoff"] / 2.0;
        parameters["limitOnNumberOfTimesToMerge"] = 0;  
        parameters["splitOnlyOnRelaventVariables"] = False;
        parameters["precisionForMerging"] = oldParameters["precisionForMerging"] + 1.0;
        parameters["numberOfSamplesToTry"] = oldParameters["numberOfSamplesToTry"];
        parameters["produceGreaterAbstraction"] = False;
        parameters["exponentialComponent"] = 0.0; 
        ensures(isinstance(parameters, dict));
        ensures(set(parameters.keys()).issuperset(oldParameters.keys()));
        return parameters;

    

# TODO: refactor the code to allow the other function to inherit these...

class ManagerForReviewingAndChangingAllowedStatusOfPredicates():
    """
    Largely a copy of the content in ManualPredicateReviewPrompt internal-class of Operator_ManualPredicateReview
    """

    def __init__(self, parsedUserQuestion, domainInformation, loadedLearnedModel, state, objectForHistory):
        # TODO: requires and ensures....
        self.parsedUserQuestion = parsedUserQuestion;
        self.domainInformation = domainInformation;
        self.loadedLearnedModel = loadedLearnedModel;
        self.currentState = state;
        self.objectForHistory = objectForHistory;
        self.historyForThisQuestion = self.objectForHistory[-1][1];
        self.statesVisitedInThisQuestion = [x[0].getID() for x in self.historyForThisQuestion];
        self.newlyAllowedPredicates = set();
        self.newlyDisallowedPredicate = set();
        self.allNamedPredicatesInDomain = self.domainInformation.getBaseConditions().copy();
        self.UUIDsOfAllNamedPredicatesInDomain = [x.getID() for x in self.allNamedPredicatesInDomain];
        self.infoOnPredicatesThatOccurInCurrentState = self.forInternalUse_getNamedPredicateUUIDsInCurrentState();
        return;

    def applyAndExit(self):
        removedPredicates = self.currentState.getCopyOfParameters()["removedPredicates"].copy();
        forCheckPurposes_removedPredicates_asString = str(removedPredicates); # to check that the below operations
            # do not modify the original state...
        removedPredicates.difference_update(\
            self.newlyAllowedPredicates);
        removedPredicates.update(\
            self.newlyDisallowedPredicate );
        # Below are sorted to address issues with, say, sets not matching up in positions. 
        # If the counts of each letter is the same, then very likely the originals were the
        # same...
        assert(sorted(forCheckPurposes_removedPredicates_asString) == \
            sorted(str(self.currentState.getCopyOfParameters()["removedPredicates"])));
        return removedPredicates;

    def forInternalUse_getNamedPredicateUUIDsInCurrentState(self):
        commandToExecute = "SELECT A.childUUID as predUUID, count(*) as numOccurances " + \
            "FROM QAStateValues as A " + \
            "WHERE  " + \
            "    (A.fieldName = 'd:root' or A.fieldName = 'd:parent_child') " + \
            "    AND (A.childUUID NOT LIKE \"frozenset%\") " + \
            "    AND QAStateUUID = \"" + self.currentState.getID() + "\" " + \
            "    AND EXISTS (SELECT * FROM predicateInfo WHERE predicateUUID=childUUID) GROUP BY childUUID; ";
        results = objDatabaseInterface.exec(commandToExecute);
        valuesToReturn = [(x["numOccurances"], 
                          x["predUUID"], 
                          str([y for y in self.allNamedPredicatesInDomain if y.getID() == x["predUUID"]][0])    ) \
                         for x in results ];
        valuesToReturn.sort(reverse=True); # I reverse them so to show the most frequently occuring predicates first.
        return valuesToReturn;

 
    def do_list_disallowed_predicates(self):
        # TODO: checks on the sets

        def getPredDescriptionGivenUUID(thisUUID):
            return [y for y in self.allNamedPredicatesInDomain if y.getID() == thisUUID][0];

        originalDisallowed = self.currentState.internalDictionary[\
                                 "mostRecentOperatorParameters"]["removedPredicates"];
        originalDisallowed = originalDisallowed.difference(self.newlyAllowedPredicates);
        newlyDisallowed = self.newlyDisallowedPredicate;
        assert(len(newlyDisallowed.intersection(originalDisallowed)) == 0);
        return (newlyDisallowed + originalDisallowed);

    def do_list_allowed_predicates(self):
        # TODO: checks on the sets
        def getPredDescriptionGivenUUID(thisUUID):
            return [y for y in self.allNamedPredicatesInDomain  if y.getID() == thisUUID][0];

        originalAllowed = set(self.UUIDsOfAllNamedPredicatesInDomain ).difference(self.currentState.internalDictionary[\
                                 "mostRecentOperatorParameters"]["removedPredicates"]);
        originalAllowed = originalAllowed.difference(self.newlyDisallowedPredicate);
        newlyAllowed = self.newlyAllowedPredicates;
        assert(len(newlyAllowed.intersection(originalAllowed)) == 0);
        return newlyAllowed + originalAllowed;


    def do_allow_predicate(self, args):
        # TODO: check that the arguments are of the expected form with a regular expression (i.e., that the arguments are a single UUID)
        args = args.replace(" " , "");
        if(args not in self.UUIDsOfAllNamedPredicatesInDomain):
            print("Error: allow_predicate requires one argument: the UUID of the predicate to disallow. However, " + \
                  " the argument(s) provided do not seem to be a UUID for a predicate in the domain.", flush=True);
        originallyDisallowed = self.currentState.internalDictionary[\
                                "mostRecentOperatorParameters"]["removedPredicates"];
        originallyAllowed = set(self.UUIDsOfAllNamedPredicatesInDomain).difference(originallyDisallowed);
        if(args in originallyAllowed):
            print("Predicate that was requested to be made newly allowed was already allowed. Doing nothing.", flush=True);
            return;
        self.newlyAllowedPredicates.update([args]);
        self.newlyDisallowedPredicate.difference_update([args]);
        ensures(args in self.newlyAllowedPredicates);
        ensures(args not in self.newlyDisallowedPredicate);
        ensures(self.newlyAllowedPredicates.issubset(self.UUIDsOfAllNamedPredicatesInDomain));
        ensures(self.newlyDisallowedPredicate.issubset(self.UUIDsOfAllNamedPredicatesInDomain));
        ensures(len(self.newlyAllowedPredicates.difference(self.newlyDisallowedPredicate)) ==
            len(self.newlyAllowedPredicates)); # i.e., that the sets are disjiont...
        return;


    def do_disallow_predicate(self, args):
        # TODO: check that the arguments are of the expected form with a regular expression (i.e., that the arguments are a single UUID)
        args = args.replace(" " , "");
        if(args not in self.UUIDsOfAllNamedPredicatesInDomain):
            print("Error: disallow_predicate requires one argument: the UUID of the predicate to disallow. However, " + \
                  " the argument(s) provided do not seem to be a UUID for a predicate in the domain.", flush=True);
        originallyDisallowed = self.currentState.internalDictionary[\
                                "mostRecentOperatorParameters"]["removedPredicates"];
        originallyAllowed = set(self.UUIDsOfAllNamedPredicatesInDomain).difference(originallyDisallowed);
        if(args in originallyDisallowed):
            print("Predicate that was requested to be made newly disallowed was already disallowed. Doing nothing.", flush=True);
            return;
        self.newlyAllowedPredicates.difference_update([args]);
        self.newlyDisallowedPredicate.update([args]);
        ensures(args not in self.newlyAllowedPredicates);
        ensures(args in self.newlyDisallowedPredicate);
        ensures(self.newlyAllowedPredicates.issubset(self.UUIDsOfAllNamedPredicatesInDomain));
        ensures(self.newlyDisallowedPredicate.issubset(self.UUIDsOfAllNamedPredicatesInDomain));
        ensures(len(self.newlyAllowedPredicates.difference(self.newlyDisallowedPredicate)) ==
            len(self.newlyAllowedPredicates)); # i.e., that the sets are disjiont...
        return;




class Operator_AutoRevisePredicates_BaseOperator(Operator_FreshGenerateAllBoxes):


    def computeTableOfPredicateUseInfoTempTable(self):
        objDatabaseInterface.executeScriptFile(\
            "./statesAndOperatorsAndSelection/setupTableForPredicateSelectionAlgorithm.sql");
        return;

    def cleanUpPredicateUseInfoTempTable(self):
        objDatabaseInterface.exec("DROP TABLE predicateCountsAndResponces;");
        return;

    def determineNewPredicatesToAllowOrDisallowAutomatically(self, parsedUserQuestion, domainInformation, loadedLearnedModel, stateAppliedTo, objectForHistory):
        assert(self.getID() == "dc5a4db9-b02e-4a7a-a34d-539b7bc28b58");
        raise Exception("Child classes must override.");
        return;        

    def forInternalUse_extraInternalParameters(self):
        self.abstractionLevelDirection = "increase"; 
        assert(self.getID() == "dc5a4db9-b02e-4a7a-a34d-539b7bc28b58");
        raise Exception("Child classes must override");
        return;

    @staticmethod
    def getID():
        uuid = "dc5a4db9-b02e-4a7a-a34d-539b7bc28b58";
        return uuid;

    def changeParameter(self, parsedUserQuestion, domainInformation, loadedLearnedModel, stateAppliedTo, objectForHistory):
        oldParameters = stateAppliedTo.getCopyOfParameters();

        # Notice that calling the below function here (then cleaning it at the end of
        #     this function) causes the table to be recomputed once each time this
        #     code is run. This is in contrast to, say, running it in the init function,
        #     which would cause it to run only when the operator is formed, which is
        #     just once at the start of loading of Fanoos.... Obviously, improvements
        #     that better support online updates are on the agenda, but for a vanilla
        #     implementation to release, its not a bad start
        self.computeTableOfPredicateUseInfoTempTable();

        self.thisPredicateManager= \
            ManagerForReviewingAndChangingAllowedStatusOfPredicates(\
            parsedUserQuestion, domainInformation, loadedLearnedModel, stateAppliedTo, objectForHistory);

        # The value returned by the below function currently is set to use 
        #     the value tracking, etc., in self.thisPredicateManager ... but that
        #     might prove repetative and unnecessarly add more code with minimal
        #     benefit, so we might just have the function determineNewPredicatesToAllowOrDisallowAutomatically
        #     directly return the values for predicates to remore later.
        self.determineNewPredicatesToAllowOrDisallowAutomatically(\
            parsedUserQuestion, domainInformation, loadedLearnedModel, stateAppliedTo, objectForHistory);

        parameters = stateAppliedTo.getCopyOfParameters();
        parameters["removedPredicates"] = self.thisPredicateManager.applyAndExit();
        parameters["produceGreaterAbstraction"] = (self.abstractionLevelDirection == "increase"); 

        self.cleanUpPredicateUseInfoTempTable();

        ensures(isinstance(parameters, dict));
        ensures(set(parameters.keys()).issuperset(oldParameters.keys()));
        return parameters;


    def __init__(self):
        self.forInternalUse_extraInternalParameters();
        return;


class Operator_AutoRevisePredicates_7b16e7a5(\
    Operator_AutoRevisePredicates_BaseOperator, Operator_IncreaseAbstractionLevel):

    @staticmethod
    def upperConfidenceBoundSelector(listOfNumberOfSuccesses, listOfNumberOfTimesTried):
        requires(isinstance(listOfNumberOfSuccesses, list));
        requires(isinstance(listOfNumberOfTimesTried, list));
        requires(len(listOfNumberOfTimesTried) == len(listOfNumberOfSuccesses));
        requires(all([ listOfNumberOfSuccesses[thisIndex] <= listOfNumberOfTimesTried[thisIndex] \
            for thisIndex in range(0, len(listOfNumberOfTimesTried))]));
        requires(all([ isinstance(x, int) for x in listOfNumberOfTimesTried ]));
        requires(all([ isinstance(x, int) for x in listOfNumberOfSuccesses  ]));
        requires(all([ (x >= 0) for x in listOfNumberOfSuccesses ]));
        A = np.array(listOfNumberOfSuccesses);
        B = np.array(listOfNumberOfTimesTried);
        indexToReturn = np.argmax( (A / B) + np.sqrt( 2 * np.log(np.sum(B)) / B) );
        assert(isinstance(indexToReturn, np.int64));
        indexToReturn = int(indexToReturn);
        ensures(isinstance(indexToReturn, int));
        ensures(indexToReturn >= 0);
        ensures(indexToReturn < len(listOfNumberOfTimesTried));
        return indexToReturn ;


    @staticmethod
    def convertStringSetToSQLStringList(thisStringList):
        requires(isinstance(thisStringList, list) or isinstance(thisStringList, set));
        requires(all([("'" not in x) for x in thisStringList]));
        return ", ".join(["'" + x + "'" for x in thisStringList]);



    def determineNewPredicatesToAllowOrDisallowAutomatically(self, parsedUserQuestion, domainInformation,\
        loadedLearnedModel, stateAppliedTo, objectForHistory):
        predicatesAvailable = [x[1] for x in self.thisPredicateManager.infoOnPredicatesThatOccurInCurrentState];
        if(len(predicatesAvailable) > 0):
            templateForQueryToIssue = \
            """
            SELECT count(*) AS numberOccurances, sum(userSecondResponce IN ({0})) AS numberSuccesses, predicateUUID
            FROM temp.predicateCountsAndResponces 
            WHERE userFirstResponce in ({1}) AND 
            predicateUUID in ({2}) 
            AND numFirst > numSecond 
            GROUP BY predicateUUID ORDER BY predicateUUID;
            """;
            queryToIssue = templateForQueryToIssue.format(
                self.convertStringSetToSQLStringList(self.desiredEndingUserInputs), \
                self.convertStringSetToSQLStringList(self.startingUserInputs), \
                self.convertStringSetToSQLStringList(predicatesAvailable) \
            );
            results = objDatabaseInterface.exec(queryToIssue);
            numberOccurancesPerPredicate = [x["numberOccurances"] for x in results];
            numberSuccessesPerPredicate = [x["numberSuccesses"] for x in results];
            predicateList = [x["predicateUUID"] for x in results];
            predicatesNotYetTried = set(predicatesAvailable).difference(predicateList);
            for thisPredicatesNotYetTried in predicatesNotYetTried:
                numberOccurancesPerPredicate.append(1);
                numberSuccessesPerPredicate.append(0);
                predicateList.append(thisPredicatesNotYetTried);
            indexOfPredicateToRemove = self.upperConfidenceBoundSelector(\
                numberSuccessesPerPredicate, numberOccurancesPerPredicate);
            self.thisPredicateManager.do_disallow_predicate(\
                predicateList[indexOfPredicateToRemove]);
        else:
            print("auto-predicate review: no named predicates present.", flush=True);
        return;

    @staticmethod
    def getID():
        uuid = "553060df-18ca-46d5-926d-2918b808a9fb";
        return uuid;

    def forInternalUse_extraInternalParameters(self):
        raise Exception("Child classes must override.");
        self.abstractionLevelDirection = "increase";
        self.startingUserInputs = set([""]);
        self.desiredEndingUserInputs = set([""]);
        assert(self.getID() == "553060df-18ca-46d5-926d-2918b808a9fb");
        return;



class Operator_AutoRevisePredicates_IAL_7b16e7a5(Operator_AutoRevisePredicates_7b16e7a5):

    def forInternalUse_extraInternalParameters(self):
        self.abstractionLevelDirection = "increase";
        self.startingUserInputs = set(["m", "auto_u_m"]);
        self.desiredEndingUserInputs = set(["l", "b", "auto_u_l"]);
        assert(self.getID() == "98fbcb97-45b1-4841-9087-19bc63934e38");
        return;

    @staticmethod
    def getID():
        uuid = "98fbcb97-45b1-4841-9087-19bc63934e38";
        return uuid;

class Operator_AutoRevisePredicates_DAL_7b16e7a5(Operator_AutoRevisePredicates_7b16e7a5):

    def forInternalUse_extraInternalParameters(self):
        self.abstractionLevelDirection = "decrease";
        self.startingUserInputs = set(["l", "auto_u_l"]);
        self.desiredEndingUserInputs = set(["m", "b", "auto_u_m"]);
        assert(self.getID() == "5fd1f949-d803-4188-a4db-e29451f868ca");
        return;

    @staticmethod
    def getID():
        uuid = "5fd1f949-d803-4188-a4db-e29451f868ca";
        return uuid;






