

import config;
_LOCALDEBUGFLAG = config.debugFlags.get_v_print_ForThisFile(__file__);
    

from utils.quickResetZ3Solver import quickResetZ3Solver;

import numpy as np;
import sys;
from utils.contracts import *;

from boxesAndBoxOperations.getBox import isProperBox, getBox, getDimensionOfBox, getJointBox, getContainingBox, getRandomBox, \
    boxAContainsBoxB, boxContainsVector;

import uuid;
import re;

import z3;

from domainsAndConditions.baseClassDomainInformation import BaseClassDomainInformation ;


class CharacterizationConditionsBaseClass():

    def __str__(self):
        raise NotImplementedError(); # child classes must override this.

    def checkInitialization(self):
        assert(isinstance(self.z3Solver, z3.z3.Solver)); 
        assert(isinstance(self.expectedNumberOfDimensions, int));
        assert(self.expectedNumberOfDimensions > 0);
        assert(isinstance(self.listMappingPositionToVariableName, list));
        assert(len(self.listMappingPositionToVariableName) == self.expectedNumberOfDimensions);
        assert(all([isinstance(x, z3.z3.ArithRef) for x in self.listMappingPositionToVariableName]));
        assert(re.match("^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", \
               self.getID()) != None);
        assert(isinstance(self.relaventVariables(), frozenset));
        assert(all([isinstance(x, z3.z3.ArithRef) for x in self.relaventVariables()]));
        assert(self.relaventVariables().issubset(self.listMappingPositionToVariableName));
        return;

    def setID(self, uuidProvided=None):
        requires((uuidProvided is None) or isinstance(uuidProvided, str));
        requires((uuidProvided is None) or (len(uuidProvided) > 0));
        self.uuid = uuidProvided if (uuidProvided is not None) else str(uuid.uuid4());
        ensures(isinstance(self.uuid , str));
        ensures(len(self.uuid) > 0);
        return

    def getID(self):
        return self.uuid;

    def __init__(self, z3SolverInstance, functToGetUuidProvided=None):
        raise NotImplementedError(); # child classes must implement.
        self.expectedNumberOfDimensions = 5;
        self.z3FormattedCondition = "";
        self.listMappingPositionToVariableName = [];
        self.z3Solver = z3SolverInstance;
        self.setID(uuidProvided=(None if (functToGetUuidProvided is None) else (functToGetUuidProvided(self))) ); # ssh-rsa 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 abc@defg
        self.checkInitialization();
        raise NotImplementedError(); # child classes must implement.


    def defaultSlowImplementation_pythonFormatEvaluation(self, vectorToEvaluateAgainst):
        requires(isinstance(vectorToEvaluateAgainst, np.ndarray));
        vectorToEvaluateAgainst = self.handleCaseOfJointBox(vectorToEvaluateAgainst); # hacky to put this before a requires... TODO: fix this....
        requires(vectorToEvaluateAgainst.shape == (self.expectedNumberOfDimensions, 1)); 
        precondition = z3.And([\
            float(vectorToEvaluateAgainst[thisIndex]) == self.listMappingPositionToVariableName[thisIndex] \
            for thisIndex in range(0, self.expectedNumberOfDimensions) ]);
        quickResetZ3Solver(self.z3Solver);
        formulaToCheck = z3.And(precondition, self.z3FormattedCondition); # "And" as oppossed to "Implies" since
            # z3 is checking for satisfiability - so "Implies" would be trivial to satisfy by failing the hypothesis....
        self.z3Solver.add(formulaToCheck);
        verdict = (self.z3Solver.check() == z3.z3.sat);
        return verdict;

    def relaventVariables(self):
        raise NotImplementedError(); # child classes must implement.


    def pythonFormatEvaluation(self, vectorToEvaluateAgainst):
        return self.defaultSlowImplementation_pythonFormatEvaluation(vectorToEvaluateAgainst);

    def convertBoxToFormulaConstraints(self, thisBox):
        requires(isProperBox(thisBox));
        thisBox = self.handleCaseOfJointBox(thisBox); # hacky to put this before a requires... TODO: fix this....
        requires(getDimensionOfBox(thisBox) == self.expectedNumberOfDimensions);
        F = z3.And([ \
            z3.And( float(thisBox[index, 0]) <= self.listMappingPositionToVariableName[index], \
                    self.listMappingPositionToVariableName[index] <= float(thisBox[index, 1]) \
                  ) \
            for index in range(0, self.expectedNumberOfDimensions) \
            if self.listMappingPositionToVariableName[index] in self.relaventVariables()]);
        return F;
    
    def allMembersOfBoxSatisfyCondition(self, thisBox):
        requires(isProperBox(thisBox));
        thisBox = self.handleCaseOfJointBox(thisBox); # hacky to put this before a requires... TODO: fix this....
        requires(getDimensionOfBox(thisBox) == self.expectedNumberOfDimensions);
        quickResetZ3Solver(self.z3Solver);
        formulaToCheck = \
            z3.ForAll(self.listMappingPositionToVariableName, \
                z3.Implies(\
                    self.convertBoxToFormulaConstraints(thisBox), \
                    self.z3FormattedCondition \
                ) \
            );
        self.z3Solver.add(formulaToCheck);
        verdict = (self.z3Solver.check() == z3.z3.sat);
        return verdict;

    def existsMemberOfBoxSatifyingCondition(self, thisBox):
        requires(isProperBox(thisBox));
        thisBox = self.handleCaseOfJointBox(thisBox); # hacky to put this before a requires... TODO: fix this....
        requires(getDimensionOfBox(thisBox) == self.expectedNumberOfDimensions);
        quickResetZ3Solver(self.z3Solver);
        formulaToCheck = \
            z3.Exists(self.listMappingPositionToVariableName, \
                z3.And(\
                    self.convertBoxToFormulaConstraints(thisBox), \
                    self.z3FormattedCondition \
                ) \
            );
        self.z3Solver.add(formulaToCheck);
        verdict = (self.z3Solver.check() == z3.z3.sat);
        return verdict;

    def handleCaseOfJointBox(self, thisBox):
        if(thisBox.shape[0] == self.expectedNumberOfDimensions): # using shape[0] here kind of bleeds the box-inferface I had set up, but doing this here also allows for handling vectors appropraitely - or, rather, should 
            return thisBox;
        else:
            assert(len(thisBox) == self.numberOfDimensionsInAJointBox);
            return self.functionToMapJointBoxToRelaventVariables(thisBox);

import inspect;

class CharacterizationCondition_FromPythonFunction(CharacterizationConditionsBaseClass):

    def __init__(self, z3SolverInstance, domainClass, functionToBaseConditionOn, functToGetUuidProvided=None):
        requires(isinstance(z3SolverInstance, z3.Solver));
        requires(issubclass(domainClass, BaseClassDomainInformation));
        requires(isinstance(functionToBaseConditionOn.__doc__, str));
        requires(len(functionToBaseConditionOn.__doc__) > 0);
        self.functionToBaseConditionOn = functionToBaseConditionOn;
        variablesPresentInFunctionArguments = inspect.getargspec(functionToBaseConditionOn).args;
        self.relaventVariablesSet = frozenset([z3.Real(x) for x in variablesPresentInFunctionArguments]);
        self.numberOfDimensionsInAJointBox = len(domainClass.inputSpaceVariables()) + len(domainClass.outputSpaceVariables());
        if(set(self.relaventVariablesSet).issubset(domainClass.inputSpaceVariables())):
            self.listMappingPositionToVariableName = domainClass.inputSpaceVariables();
            # Note that by using the syntax [:k,] below, it works for both boxes and vectors as intended. See the
            # places where self.functionToMapJointBoxToRelaventVariables is used to see why it is good both are supported.
            self.functionToMapJointBoxToRelaventVariables = (lambda x: x[:len(domainClass.inputSpaceVariables()),]); # assumes the order of the joint box is input-space followed by output-space
        elif(set(self.relaventVariablesSet).issubset(domainClass.outputSpaceVariables())):
            self.listMappingPositionToVariableName = domainClass.outputSpaceVariables();
            # Note that by using the syntax [:k,] below, it works for both boxes and vectors as intended. See the
            # places where self.functionToMapJointBoxToRelaventVariables is used to see why it is good both are supported.
            self.functionToMapJointBoxToRelaventVariables = (lambda x: x[len(domainClass.inputSpaceVariables()):,]); # assumes the order of the join box is input-space followed by output-space
        elif(set(self.relaventVariablesSet).issubset(domainClass.inputSpaceVariables() + domainClass.outputSpaceVariables())): # If it is a joint box, it should always be this <================================================
            self.listMappingPositionToVariableName = domainClass.inputSpaceVariables() + domainClass.outputSpaceVariables();
            self.functionToMapJointBoxToRelaventVariables = (lambda x: x); # assumes the order of the join box is input-space followed by output-space
        else:
            
            raise Exception("The provided function uses references variables not in the domain information.\n" + \
                            "The relavent set of variables: " + str(variablesPresentInFunctionArguments) + "\n" + \
                            "Known input variables: " + str(domainClass.inputSpaceVariables()) + "\n" + \
                            "Known output variables: " + str(domainClass.outputSpaceVariables()) + "\n");
        assert(all([isinstance(x, z3.z3.ArithRef) for x in self.listMappingPositionToVariableName]));
        assert(set(self.relaventVariablesSet).issubset(self.listMappingPositionToVariableName));

        self.dictMappingVariableNameToIndex = dict();
        for thisIndex in range(0, len(self.listMappingPositionToVariableName)):
            self.dictMappingVariableNameToIndex[self.listMappingPositionToVariableName[thisIndex]] = thisIndex;
        assert(\
            all([  (self.listMappingPositionToVariableName[self.dictMappingVariableNameToIndex[varName]] == varName) \
                   for varName in self.listMappingPositionToVariableName]\
        ));
        assert(set(self.dictMappingVariableNameToIndex.keys()) == set(self.listMappingPositionToVariableName));
        assert(set(self.dictMappingVariableNameToIndex.keys()).issuperset(self.relaventVariablesSet));
        assert(set(self.dictMappingVariableNameToIndex.values()) == set(range(0, len(self.listMappingPositionToVariableName))));

        self.z3FormattedCondition = \
            functionToBaseConditionOn(**{str(x) : x for x in self.relaventVariablesSet});

        self.expectedNumberOfDimensions = len(self.listMappingPositionToVariableName);
        self.z3Solver = z3SolverInstance;
        self.setID(uuidProvided=(None if (functToGetUuidProvided is None) else (functToGetUuidProvided(self))));
        self.checkInitialization();
        return;


    def relaventVariables(self):
        return self.relaventVariablesSet;

    def pythonFormatEvaluation(self, vectorToEvaluateAgainst):
        vectorToEvaluateAgainst = self.handleCaseOfJointBox(vectorToEvaluateAgainst);
        requires(isinstance(vectorToEvaluateAgainst, np.ndarray));
        requires(len(vectorToEvaluateAgainst.shape) == 2);
        requires(vectorToEvaluateAgainst.shape[0] == self.expectedNumberOfDimensions);
        return self.functionToBaseConditionOn(\
            **{str(thisVar) : vectorToEvaluateAgainst[self.dictMappingVariableNameToIndex[thisVar],0] \
               for thisVar in self.relaventVariables() });

    def __str__(self):
        return self.functionToBaseConditionOn.__doc__;



class MetaCondition_Conjunction(CharacterizationConditionsBaseClass):
    def __init__(self, listOfConditionsToConjunct):
        requires(isinstance(listOfConditionsToConjunct, list));
        requires(len(listOfConditionsToConjunct) > 0);
        self.listOfConditionsToConjunct = listOfConditionsToConjunct;
        self.z3Solver = listOfConditionsToConjunct[0].z3Solver;
        self.z3FormattedCondition = z3.And([x.z3FormattedCondition for x in listOfConditionsToConjunct]);
        self.setID();
        return;

    def pythonFormatEvaluation(self, vectorToEvaluateAgainst):
        for thisCondition in self.listOfConditionsToConjunct:
            if(not thisCondition.pythonFormatEvaluation(vectorToEvaluateAgainst)):
                return False;
        return True;

    def allMembersOfBoxSatisfyCondition(self, thisBox):
        for thisCondition in self.listOfConditionsToConjunct:
            if(not thisCondition.allMembersOfBoxSatisfyCondition(thisBox)):
                return False;
        return True;

    def existsMemberOfBoxSatifyingCondition(self, thisBox):
        requires(isProperBox(thisBox));
        quickResetZ3Solver(self.z3Solver);
        conditionToCheck = \
            z3.And([\
                z3.And(\
                    x.convertBoxToFormulaConstraints(thisBox), \
                    x.z3FormattedCondition \
                ) \
                for x in self.listOfConditionsToConjunct \
            ] );
        setOfVariablesToQuantifyOver = set();
        for thisCondition in self.listOfConditionsToConjunct:
            setOfVariablesToQuantifyOver.update(thisCondition.listMappingPositionToVariableName);
        formulaToCheck = \
            z3.Exists(list(setOfVariablesToQuantifyOver), \
                conditionToCheck \
            );
        self.z3Solver.add(formulaToCheck);
        verdict = (self.z3Solver.check() == z3.z3.sat);
        return verdict;

    def relaventVariables(self):
        setToReturn = set();
        for thisCondition in self.listOfConditionsToConjunct:
            setToReturn.update(thisCondition.relaventVariables());
            assert(setToReturn.issuperset(thisCondition.relaventVariables()));
        return frozenset(setToReturn);

    def setID(self):
        self.uuid = frozenset([x.getID() for x in self.listOfConditionsToConjunct]);
        return

    def __str__(self):
        # We sort the below in order to ensure that the order is fixed based on the content -
        # two instances with the same parameters should produce the same string representation.
        return "And("+ (", ".join(sorted([str(x) for x in self.listOfConditionsToConjunct]))) + ")";


class Condition_TheBoxItself(CharacterizationConditionsBaseClass):
    def __init__(self, z3Solver, thisBox, listMappingAxisIndexToVariableInQuestion):
        requires(isProperBox(thisBox));
        requires(isinstance(listMappingAxisIndexToVariableInQuestion, list));
        requires(all([isinstance(x, z3.z3.ArithRef) for x in listMappingAxisIndexToVariableInQuestion]));
        requires( len(listMappingAxisIndexToVariableInQuestion) == getDimensionOfBox(thisBox));

        self.expectedNumberOfDimensions = getDimensionOfBox(thisBox);
        self.listMappingPositionToVariableName = listMappingAxisIndexToVariableInQuestion;
        self.personalBox = thisBox;
        self.z3Solver = z3Solver; # Including for uniformity of interface so that the 
            # metaConditions can use it, not that it is used in this class itself.
        self.z3FormattedCondition = self.convertBoxToFormulaConstraints(thisBox); # None;
        self.setID();
        return;

    def defaultSlowImplementation_pythonFormatEvaluation(self, vectorToEvaluateAgainst):
        raise NotImplementedError();

    def pythonFormatEvaluation(self, vectorToEvaluateAgainst):
        return boxContainsVector(self.personalBox, vectorToEvaluateAgainst.reshape(max(vectorToEvaluateAgainst.shape),));
   
    def allMembersOfBoxSatisfyCondition(self, thisBox):
        return boxAContainsBoxB(self.personalBox, thisBox);

    def existsMemberOfBoxSatifyingCondition(self, thisBox):
        raise NotImplementedError();

    def relaventVariables(self):
        return frozenset(self.listMappingPositionToVariableName);

    def __str__(self):
        labeledValuesOfBoxes = [\
            str(self.listMappingPositionToVariableName[thisIndex]) + " : " +\
            str(self.personalBox[thisIndex, :]).replace("\n", ",") \
            for thisIndex in range(0, len(self.listMappingPositionToVariableName)) \
            ];
        return "Box(" + ( ", ".join(labeledValuesOfBoxes) ) + ")";

    def convertBoxToFormulaConstraints(self, thisBox):
        requires(isProperBox(thisBox));
        F = z3.And([ \
            z3.And( float(thisBox[index, 0]) <= self.listMappingPositionToVariableName[index], \
                    self.listMappingPositionToVariableName[index] <= float(thisBox[index, 1]) \
                  ) \
            for index in range(0, self.expectedNumberOfDimensions) ]);
        return F;




