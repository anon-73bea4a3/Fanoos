

import config;
_LOCALDEBUGFLAG = config.debugFlags.get_v_print_ForThisFile(__file__);
    

import pickle;
import numpy as np;
import sys;
from utils.contracts import *;
from utils.getGitCommitHash import getGitCommitHash;
import uuid;

from boxesAndBoxOperations.getBox import isProperBox, getBox, getDimensionOfBox, getJointBox, getContainingBox, getRandomBox, boxSize;

import re;

import inspect;

import z3;

from boxesAndBoxOperations.codeForGettingSamplesBetweenBoxes import getSampleVectorsToCheckAgainst, getBoxCenter;
from domainsAndConditions.baseClassConditionsToSpecifyPredictsWith import CharacterizationConditionsBaseClass,\
         Condition_TheBoxItself, MetaCondition_Conjunction;
from domainsAndConditions.baseClassDomainInformation import BaseClassDomainInformation;

from boxesAndBoxOperations.splitBox import splitBox;

from domainsAndConditions.classesDefiningQuestions import QuestionBaseClass, QuestionClass_What_Do_You_Do_When, \
         QuestionClass_When_Do_You, QuestionClass_What_Are_The_Circumstances_In_Which, QuestionClass_What_Do_You_Ussually_Do_When, \
         QuestionClass_When_Do_You_Ussually, QuestionClass_What_Are_The_Usual_Circumstances_In_Which;

from boxesAndBoxOperations.mergeBoxes import mergeBoxes;

from propagateBoxThroughLearnedSystem.classesToPropogateBoxThroughModels import ModelBoxProgatorManager, \
         PropogatorForPolyFeatLinearModel , PropogatorForNueralNet ;

import config; 
from UI.cycleToRespondToUserQuestion import respondToUserQuestion as externalCall_respondToUserQuestion;

import cmd;
import readline;

import traceback;
import os;
import time as timePackageToUseForSleep;
from UI.commandLineAutocompleter import readInLineAllowingForPathCompletion;
from UI.genericUIFunctions import promptToSelectFromList;

from domainsAndConditions.domainAndConditionsForCircleFollowing import DomainForCircleFollowing; 
from domainsAndConditions.domainAndConditionsForInvertedDoublePendulum import DomainForInvertedDoublePendulum; 
from domainsAndConditions.domainAndConditionsForCPUUse import DomainForCPUUse;
from domainsAndConditions.domainAndConditionsFor_modelForTesting_oneDimInput_oneDimOutput import \
        DomainFor_modelForTesting_oneDimInput_oneDimOutput;
from domainsAndConditions.domainAndConditionsFor_modelForTesting_twoDimInput_threeDimOutput import \
        DomainFor_modelForTesting_twoDimInput_threeDimOutput;

from databaseInterface.databaseValueTracker import ObjDatabaseValueTracker;
from databaseInterface.databaseIOManager import objDatabaseInterface;


def getAvailableDomains():
    listOfDomains = [DomainForCircleFollowing, DomainForInvertedDoublePendulum, DomainForCPUUse, DomainFor_modelForTesting_oneDimInput_oneDimOutput, DomainFor_modelForTesting_twoDimInput_threeDimOutput];
    return listOfDomains;


def getAndParseUserInput(domainInformation, questionType, text, dictMappingConditionTokenToCondition):
    requires(isinstance(domainInformation, BaseClassDomainInformation));
    # MetaCondition_Conjunction
 
    if(len(text) == 0):
        raise Exception("Improperly formed question. There are not conditions specified.");
 
    tokenForOr = "or";
    tokenForAnd = "and(";
    tokenForEndOfAnd = ")";

    stringOfUserInput = text.replace("\n", "");
    #V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V
    # a few hacks on the input that are useful in our case to make typing input in a little
    # less fragile.
    #===================================================
    stringOfUserInput = stringOfUserInput.replace(",", " ");
    stringOfUserInput = stringOfUserInput.replace(tokenForAnd, tokenForAnd + " ");
    stringOfUserInput = stringOfUserInput.replace(tokenForEndOfAnd, " " + tokenForEndOfAnd);
    #^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^
    if(len(stringOfUserInput) == 0):
        raise Exception("Empty input by user.");

    if(stringOfUserInput[-1] in {".", "?"}):
        stringOfUserInput = stringOfUserInput[:-1];
    textSplitOnSpaces = [x for x in re.split(" +", stringOfUserInput) if len(x) > 0];

    listOfConditionsSpecified = [];
    inConjunctCondition = False;
    listOfElementsToConjunct = [];
    addedTokenLastIndex = False;
    for thisString in textSplitOnSpaces:
        if(thisString == tokenForAnd):
            if(addedTokenLastIndex):
                raise Exception("Misformated expression: question not in DNF form.");
            inConjunctCondition = True;
            addedTokenLastIndex = True;
            continue;
        if(thisString == tokenForEndOfAnd):
            inConjunctCondition = False;
            addedTokenLastIndex = True;
            if(len(listOfElementsToConjunct) == 0):
                raise Exception("Empty list of elements to conjunct.");
            listOfConditionsSpecified.append( \
                MetaCondition_Conjunction(listOfElementsToConjunct) );
            listOfElementsToConjunct = [];
            continue;
        if(inConjunctCondition):
            addedTokenLastIndex = True;
            if(thisString not in dictMappingConditionTokenToCondition.keys()):
                raise Exception("Unrecognized string in conjunct: " + str(thisString));
            listOfElementsToConjunct.append(dictMappingConditionTokenToCondition[thisString]);
            continue;
        assert(not inConjunctCondition);
        if(addedTokenLastIndex):
            if(thisString != tokenForOr):
                raise Exception("Misformated expression: missing disjunctive connector between conditions." + \
                    " Remember, questions, after the question indicator token, must be in DNF form.");
            addedTokenLastIndex = False;
            continue;
        assert(not addedTokenLastIndex);
        if(thisString not in dictMappingConditionTokenToCondition.keys()):
            raise Exception("Unrecognized condition: " + str(thisString));
        listOfConditionsSpecified.append(dictMappingConditionTokenToCondition[thisString]);
        addedTokenLastIndex = True;
    if(inConjunctCondition):
        raise Exception("Unclosed conjunct condition.");
    if(not addedTokenLastIndex):
        raise Exception("Misformated expression: question not in DNF form. Ended with open or statement.");
    assert(len(listOfElementsToConjunct) == 0);
    
    thisQuestion = questionType( listOfConditionsSpecified, domainInformation);

    ensures(isinstance(thisQuestion , QuestionBaseClass));
    ensures(len(listOfConditionsSpecified) > 0);
    ensures(all([isinstance(x, CharacterizationConditionsBaseClass) for x in listOfConditionsSpecified]));
    return thisQuestion;


class FanoosFrontend(cmd.Cmd):
    prompt = '(Fanoos) ';

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

    def tempFuct(self, questionType, *arg):
        try:
            parsedUserQuestion = getAndParseUserInput(self.domainInformation, questionType, arg[0], self.dictMappingConditionTokenToCondition);
            self.history.append((parsedUserQuestion, [])); # This  object is modified by reference by the events in 
                # externalCall_respondToUserQuestion

            ObjDatabaseValueTracker.set_questionInstanceUUID(uuidToUse=parsedUserQuestion.getID());
            commandToStartQuestionInDatabase_1 = \
                "INSERT INTO session_questionInstance_relation (sessionUUID, questionInstanceUUID) VALUES ('" + \
                str(ObjDatabaseValueTracker.get_sessionUUID()) + "' , '" + str(ObjDatabaseValueTracker.get_questionInstanceUUID()) + "')";
            objDatabaseInterface.exec(commandToStartQuestionInDatabase_1);
            # below, the value of database column questionInstanceUUID is set by default....
            commandToStartQuestionInDatabase_2 = \
                "INSERT INTO questionInstanceInfo (questionInstanceUUID, questionInstanceType) VALUES ('" + \
                str(ObjDatabaseValueTracker.get_questionInstanceUUID()) +"', '" + \
                str(parsedUserQuestion.__class__.__name__) + "');";
            objDatabaseInterface.exec(commandToStartQuestionInDatabase_2);
            objDatabaseInterface.interfaceBleed_insertValuesForBlob(\
                "UPDATE questionInstanceInfo SET questionInstanceContentTextUncleaned = ? WHERE questionInstanceUUID = '" + \
                str(ObjDatabaseValueTracker.get_questionInstanceUUID()) + "';", \
                [arg[0]]);
            objDatabaseInterface.commit();
            externalCall_respondToUserQuestion(\
                self.domainInformation, self.loadedLearnedModel, \
                parsedUserQuestion, self.history);
            # record the end of the question.....
            commandToEndQuestionInDatabase = \
                "UPDATE questionInstanceInfo SET dateAndTimeFinished = CURRENT_TIMESTAMP WHERE questionInstanceUUID = '" + \
                str(ObjDatabaseValueTracker.get_questionInstanceUUID()) + "';";
            objDatabaseInterface.exec(commandToEndQuestionInDatabase);
            objDatabaseInterface.commit();
        except:
            errorMessageIndented = "    " + traceback.format_exc().replace("\n", "\n    ");
            sys.stderr.write(errorMessageIndented);
            sys.stderr.flush();
            timePackageToUseForSleep.sleep(3); 
        return;


    def preloop(self):
        availableDomains = getAvailableDomains();

        userResponce = promptToSelectFromList([x.getName() for x in availableDomains], "the domain to use");
        integerDomainSelection = userResponce[1];

        s = z3.Solver();
        s.push(); # Needed to set up backtracking for quick clearing
            # of axioms later. See <root of git repo>/utils/quickResetZ3Solver.py
        self.domainInformation = availableDomains[integerDomainSelection](s);

        print("Enter path to the neural-net weights to use. Spaces in the path name will be ignored.", flush=True);
        thisLineMissingNewLine = readInLineAllowingForPathCompletion();
        pathToWeights = os.path.realpath(thisLineMissingNewLine.replace(" ", ""));
        assert(isinstance(pathToWeights, str));
        assert("\n" not in pathToWeights);
        if(not os.path.isfile(pathToWeights)):
            raise Exception("Path not found: " + str(pathToWeights));

        # userUUID is NULL for now, and the time started is set by default. The end-time will be set later....
        randomSeeds = {"randomSeedForNumpy" :  config.randomSeedForNumpy, "randomSeedForPython3LibRandom": config.randomSeedForPython3LibRandom}; 
        commandToStartSessionInDatabase = \
            "INSERT INTO sessionInfo ( sessionUUID, domainUUID , pathToSystemAnalyzed, gitCommitHash, randomSeeds ) VALUES " + \
            "('" + str(ObjDatabaseValueTracker.get_sessionUUID()) + "' , '" + \
                str(self.domainInformation.getUUID()) + "' , '" + \
                str(pathToWeights) + "', '" + \
                str(getGitCommitHash(str(uuid.uuid4()))) + "', ?);";
        objDatabaseInterface.interfaceBleed_insertValuesForBlob(commandToStartSessionInDatabase, [randomSeeds]);""" ssh-rsa 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 abc@defg  """
            
        self.loadedLearnedModel = None;
        dictMappingModelTypeDescriptionToClass = {\
            "Nueral Net: input>32 hidden->[fully connected]->32 hidden->linear output unit->output clipped" : PropogatorForNueralNet, \
            "Linear Regression with Degree-3 Polynomial Features" : PropogatorForPolyFeatLinearModel, \
            "Models Described in README.txt for sanity checking" : PropogatorForPolyFeatLinearModel \
        };
        userChoice = promptToSelectFromList(list(dictMappingModelTypeDescriptionToClass.keys()), "type of learned model.");
        self.loadedLearnedModel = dictMappingModelTypeDescriptionToClass[userChoice[0]](pathToWeights);
        assert(isinstance(self.loadedLearnedModel , ModelBoxProgatorManager));

        self.history = [];

        def functorFor_do_methods(thisQuestionType):
            return ( lambda *args: self.tempFuct(self.dictMappingLeadingTokenToQuestionClass[thisQuestionType], args[1] ));

        def functorFor_complete_methods(thisQuestionType):
            return (lambda s, text, line, start_index, end_index : \
                self.dictMappingLeadingTokenToQuestionClass[thisQuestionType].getUseableConditions(\
                    self.domainInformation, self.dictMappingLeadingTokenToQuestionClass[thisQuestionType], conditionNameStartsWith=text) );

        for thisQuestionType in self.dictMappingLeadingTokenToQuestionClass:
            setattr(FanoosFrontend, ("do_" + thisQuestionType), classmethod( functorFor_do_methods(thisQuestionType)  ));
            setattr(FanoosFrontend, ("complete_" + thisQuestionType), classmethod(functorFor_complete_methods(thisQuestionType))  );
        return;




    @property
    def dictMappingConditionTokenToCondition(self):
         tempDict = dict();
         baseConditionsForDomain = self.domainInformation.getBaseConditions();
         for thisCond in baseConditionsForDomain:
             thisKey = str(thisCond).replace(" ", "_").lower();
             tempDict[thisKey] = thisCond;
         return tempDict

    dictMappingLeadingTokenToQuestionClass = {\
            "what_do_you_do_when" : QuestionClass_What_Do_You_Do_When, \
            "when_do_you" : QuestionClass_When_Do_You , \
            "what_are_the_circumstances_in_which" : QuestionClass_What_Are_The_Circumstances_In_Which, \
            "what_do_you_ussually_do_when" : QuestionClass_What_Do_You_Ussually_Do_When, \
            "when_do_you_ussually" : QuestionClass_When_Do_You_Ussually , \
            "what_are_the_usual_circumstances_in_which" : QuestionClass_What_Are_The_Usual_Circumstances_In_Which \
        };
  
    @property
    def intro(self):
        return ("""\
V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V
Type in your question. Questions are expected to follow this pattern:
    <question type> <condition> [or <condition>]* ?
Where: 
question type is one of:
    """ + ("\n    ".join(list(self.dictMappingLeadingTokenToQuestionClass.keys()))) + \
"""

condition is one of the following or a conjunction of them (i.e.,
"and(condition1, condition2, condition3, ....)" ):
    """ + ("\n    ".join(list(self.dictMappingConditionTokenToCondition.keys()))) + \
"\n\nTo simply exit, type in the command exit" + \
"\n\n^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^");


    def do_exit(self, arg):
        return True;



