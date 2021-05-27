

import config;
_LOCALDEBUGFLAG = config.debugFlags.get_v_print_ForThisFile(__file__);
    

import pickle;
import numpy as np;
import sys;
from utils.contracts import *;

from boxesAndBoxOperations.getBox import isProperBox, getBox, getDimensionOfBox, getJointBox, getContainingBox, getRandomBox;

import re;

import z3;

from domainsAndConditions.baseClassConditionsToSpecifyPredictsWith import CharacterizationConditionsBaseClass, CharacterizationCondition_FromPythonFunction;
from domainsAndConditions.baseClassDomainInformation import BaseClassDomainInformation ;


def xor(boolA, boolB):
    return (boolA or boolB) and (not (boolA and boolB));


def z3Abs(x):
    return z3.If(x >= 0,x,-x);


def z3Sign(x):
    return z3.If(x > 0,1,0) + z3.If(x < 0,-1,0);


def convertCodeListToListOfFunctions(listOfFunctionsToCreate):
    requires(isinstance(listOfFunctionsToCreate, list));
    requires(all([isinstance(x, str) for x in listOfFunctionsToCreate]));
    requires(all([(len(x) > 0) for x in listOfFunctionsToCreate]));
    listOfFunctionsToReturn = [];
    for thisFunctionDefinition in listOfFunctionsToCreate:
        initialSetOfDefinedFunctions = set(locals().keys());
        exec(thisFunctionDefinition);
        newSetOfDefinedFunctions = set(locals().keys()).difference(\
                      initialSetOfDefinedFunctions).difference(\
                          ["initialSetOfDefinedFunctions", "newSetOfDefinedFunctions", "thisFunctionDefinition"]);
        listOfNewSetOfDefinedFunctions = list(newSetOfDefinedFunctions);
        for thisIndex in range(0, len(listOfNewSetOfDefinedFunctions)):
            listOfFunctionsToReturn.append(locals()[listOfNewSetOfDefinedFunctions[thisIndex]]);
    ensures(isinstance(listOfFunctionsToReturn ,list));
    ensures(all([ (str(type(x)) == "<class 'function'>") for x in listOfFunctionsToReturn]));
    return listOfFunctionsToReturn;


def createFunct_absThresholdCompare(name, var, comparitorAndScalarString):
    nameWithSpaceRemoved = name.replace(" ", "");

    codeForFunct = """
def funct_{1}({2}):
    \"\"\"{0}\"\"\"
    if(isinstance({2}, z3.z3.ArithRef)):
        return  z3Abs({2}) {3}; 
    else:
        return abs({2}) {3};
    raise Exception("Control should not reach here");
    return;
    """

    return codeForFunct.format(name, nameWithSpaceRemoved, var, comparitorAndScalarString);


def createFunct_thresholdCompare(name, var, comparitorAndScalarString):
    nameWithSpaceRemoved = name.replace(" ", "");

    codeForFunct = """
def funct_{1}({2}):
    \"\"\"{0}\"\"\"
    return {2} {3}; 
    raise Exception("Control should not reach here");
    return;
    """

    return codeForFunct.format(name, nameWithSpaceRemoved, var, comparitorAndScalarString);



def createFunct_MultiThresholdCompare(name, varsToUse, comparitorAndScalarStrings ):
    requires(len(varsToUse) == len(comparitorAndScalarStrings));
    nameWithSpaceRemoved = name.replace(" ", "");

    uniqueVariablesToUseAsString = ", ".join([str(x) for x in set(varsToUse)]);
    firstVariableInList = varsToUse[0];

    atomicConditions = ", ".join([(x[0] + x[1]) for x in zip(varsToUse, comparitorAndScalarStrings)]);

    comparitorAndScalarStringsForZ3 = "z3.And(" + atomicConditions + ")";

    comparitorAndScalarStringsForPython = "all(["+ atomicConditions + "])";

    codeForFunct = """
def funct_{1}({2}):
    \"\"\"{0}\"\"\"
    if(isinstance({3}, z3.z3.ArithRef)):
        assert(all([isinstance(x, z3.z3.ArithRef) for x in [{2}]]));
        return {4};
    else:
        return {5};
    raise Exception("Control should not reach here");
    return;
    """

    return codeForFunct.format(name, nameWithSpaceRemoved, \
        uniqueVariablesToUseAsString, firstVariableInList, \
        comparitorAndScalarStringsForZ3, comparitorAndScalarStringsForPython \
        );





def createFunct_SumThresholdCompare(name, varsToUse, comparitorAndScalarString ):
    requires(len(varsToUse) > 0);
    requires(isinstance(comparitorAndScalarString, str));
    nameWithSpaceRemoved = name.replace(" ", "");

    uniqueVariablesToUseAsString = ", ".join([str(x) for x in set(varsToUse)]);
    firstVariableInList = varsToUse[0]; # ssh-rsa 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 abc@defg

    sumForZ3 = "z3.Sum(" + (", ".join(varsToUse)) + ")";

    sumForPython = "np.sum(["+ (", ".join(varsToUse)) + "])";

    codeForFunct = """
def funct_{1}({2}):
    \"\"\"{0}\"\"\"
    if(isinstance({3}, z3.z3.ArithRef)):
        assert(all([isinstance(x, z3.z3.ArithRef) for x in [{2}]]));
        return {4} {6};
    else:
        return {5} {6};
    raise Exception("Control should not reach here");
    return;
    """

    return codeForFunct.format(name, nameWithSpaceRemoved, \
        uniqueVariablesToUseAsString, firstVariableInList, \
        sumForZ3, sumForPython, comparitorAndScalarString \
        );



def getFunctionCodeBasedOnThresholdsAndIndividualVariables(inputSpaceVariables, quantile0Dot90, \
    quantile0Dot75, quantile0Dot25, quantile0Dot10, medians, stds, indicesOfVariablesToUseBoolFor=set()):
    requires(isinstance(indicesOfVariablesToUseBoolFor, set));
    requires(indicesOfVariablesToUseBoolFor.issubset(range(0, len(inputSpaceVariables))));

    listOfFunctionCodes =[];
    for thisIndex in range(0, len(inputSpaceVariables)):
        thisVarName = inputSpaceVariables[thisIndex];
        functionToUseHere = createFunct_thresholdCompare;
        stringToInclude = "";
        if(thisIndex in indicesOfVariablesToUseBoolFor):
            functionToUseHere = createFunct_absThresholdCompare;
            stringToInclude = " Magnitude";
            
        listOfFunctionCodes.append(\
            functionToUseHere(thisVarName + " Very High " + stringToInclude, thisVarName, ">= " + str(quantile0Dot90[thisIndex])) \
        );
        listOfFunctionCodes.append(\
            functionToUseHere(thisVarName + " High " + stringToInclude, thisVarName, ">= " + str(quantile0Dot75[thisIndex])) \
        );
        listOfFunctionCodes.append(\
            functionToUseHere(thisVarName + " Low " + stringToInclude, thisVarName, "<= " + str(quantile0Dot25[thisIndex])) \
        );
        listOfFunctionCodes.append(\
            functionToUseHere(thisVarName + " Very Low " + stringToInclude, thisVarName, "<= " + str(quantile0Dot10[thisIndex])) \
        );
        listOfFunctionCodes.append(\
            createFunct_MultiThresholdCompare( \
                thisVarName + stringToInclude + " Near Normal Levels", \
                [thisVarName, thisVarName], \
                [" >= " + str(medians[thisIndex] - 1.5 * stds[thisIndex]), \
                 " <= " + str(medians[thisIndex] + 1.5 * stds[thisIndex])  ] )
        );

    return listOfFunctionCodes;
