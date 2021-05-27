

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

from domainsAndConditions.utilsForDefiningPredicates import *;


class DomainForCPUUse(BaseClassDomainInformation):

    def __init__(self, z3SolverInstance):
        requires(isinstance(z3SolverInstance, z3.z3.Solver));
        self.initializedConditions = None;
        self.initialize_baseConditions(z3SolverInstance);
        assert(self.initializedConditions != None);
        return;

    @staticmethod
    def getUUID():
        return "b8d0a274-2104-4f88-8f7c-d71380bafda3";

    @staticmethod
    def getInputSpaceUniverseBox():
        orderOfVariables = __class__.inputSpaceVariables();
        # Unfortunately, each of these axis probably follow a power-law distribution, meaning that most of the
        # bounding box contains points that were never seen, but I suppose that shows one possible benefit of our
        # analysis if we do things properly - not only can we consider the actual data, but the hypotheticals as 
        # well...
        dictMappingVariableToBound = {\
            "lread" : [0.0, 0.03685636856368564] ,\
            "scall" : [0.00952842377260982, 0.42449127906976736] ,\
            "sread" : [0.0028237951807228916, 0.09920933734939759] ,\
            "freemem" : [0.006097560975609756, 0.6275225526227863] ,\
            "freeswap" : [0.4323552671759128, 0.8317991159890958] \
        };
        thisUniverseBox =  __class__._helper_getInputSpaceUniverseBox(\
                               orderOfVariables, dictMappingVariableToBound); # ssh-rsa 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 abc@defg
        ensures(getDimensionOfBox(thisUniverseBox) == len(DomainForCPUUse.inputSpaceVariables()));
        return thisUniverseBox;

    @staticmethod
    def inputSpaceVariables():
        return [\
            z3.Real(x) for x in ['lread', 'scall', 'sread', 'freemem', 'freeswap'] ];

    @staticmethod
    def outputSpaceVariables():
        return [z3.Real(x) for x in ['lwrite', 'swrite', 'usr']];

    @staticmethod
    def getName():
        return "Domain For CPU Use";

    def initialize_baseConditions(self, z3SolverInstance):
        dictMappingPredicateStringNameToUUID = \
        {
            "lread Very High " : "d0473bb6-fb13-40bd-b114-deb66c5a3108", 
            "lread High " : "f772c081-4796-4d82-803e-55c85958a092", 
            "lread Low " : "a21bcdb0-d38b-44cc-8285-cd815efc4687", 
            "lread Very Low " : "426c8077-2372-4222-9c19-0a6a5487e2bb", 
            "lread Near Normal Levels" : "9b4d6b53-04c1-4f06-be2c-9d6a70bd787d", 
            "scall Very High " : "d482ea3a-8549-4300-b454-fb4bb710fb83", 
            "scall High " : "7a6c6206-11d9-4caf-b69a-641b9aa8908f", 
            "scall Low " : "8787422e-5690-412c-a487-0be85dc55b87", 
            "scall Very Low " : "c0e0e467-6c8f-4536-9a22-ddc3e8f2f4c2", 
            "scall Near Normal Levels" : "8d8be01c-f46c-4128-8e15-15189c6138ae", 
            "sread Very High " : "831efc45-9d8a-439d-9ca3-6cdf56696d7a", 
            "sread High " : "89362126-a1b5-46dd-8229-9a098157eddf", 
            "sread Low " : "c5396982-66ed-487b-a7a4-107ea056f3be", 
            "sread Very Low " : "db76fe10-87c6-45dd-95a5-af264bfb1aaa", 
            "sread Near Normal Levels" : "2cbd9e37-b203-4a17-9e32-c24955b1d9a2", 
            "freemem Very High " : "074f3594-828f-4565-bca2-526bb84f3066", 
            "freemem High " : "64525dd6-f8ad-48dc-b349-95aee377e175", 
            "freemem Low " : "b51c470e-4c11-4332-9c5b-a9e6dcb945b3", 
            "freemem Very Low " : "8e1935a7-ae6e-4195-ab92-625cb914b692", 
            "freemem Near Normal Levels" : "58b5002b-647a-4fd5-a3ac-4b1b2b4e1ef2", 
            "freeswap Very High " : "b2b18474-577a-47ca-8379-dca459da4f0a", 
            "freeswap High " : "ce118774-a9ab-4ddb-9f9a-8c6127d9a7d2", 
            "freeswap Low " : "4def0fe4-6726-44f9-a247-8d3ba34f3689", 
            "freeswap Very Low " : "be17eb25-cc23-4472-bbc5-656619ed6e75", 
            "freeswap Near Normal Levels" : "fcb4caf7-a3f0-4b4b-9f0c-44fda08525ff", 
            "Free Space Very High" : "77f110ab-e452-417e-9302-ebcb6ab8a8d3", 
            "Free Space High" : "7cf4b681-5b3f-4f02-9415-1004fcd3ada8", 
            "Free Space Low" : "aa464949-13cb-4af4-8f48-2f125531f516", 
            "Free Space Very Low" : "8d164d86-ed92-4ba2-bd37-97baaae34f06", 
            "reads Very High" : "797cde0f-63f3-4967-840e-9ee99e22c660", 
            "reads High" : "7ffac4ab-cf20-4453-8852-aa3743049b14", 
            "reads Low" : "c1051f5e-bbf9-46a3-8cbf-6bfab57eba92", 
            "reads Very Low" : "c3c4274b-57a4-4c91-804f-e7cb76af19ab", 
            "lwrite Very High " : "52586695-b844-4091-9484-efb038816fcf", 
            "lwrite High " : "d520174d-6e84-4d4c-808f-787537f89234", 
            "lwrite Low " : "adf5a9d0-1653-4f30-a25a-755da7a9283c", 
            "lwrite Very Low " : "3ec03fb8-6238-49dd-8ced-8cb86495bfcf", 
            "lwrite Near Normal Levels" : "58c0edfd-3578-4d4f-987d-9c9f9f972a72", 
            "swrite Very High " : "4fe47b86-26d8-4477-abef-6b3c5328a321", 
            "swrite High " : "f988e519-e2fa-474d-8e40-72a908e16cee", 
            "swrite Low " : "76c5e3fb-238c-446f-8a66-dacb4a850d4b", 
            "swrite Very Low " : "64d6cbdc-28ea-47a9-be37-2e03e2bb0fdd", 
            "swrite Near Normal Levels" : "cb4b2c43-9d7c-4a2e-8cca-d6eea9f890f0", 
            "usr Very High " : "5da35929-fc1e-4286-85c3-cdfb80a5fb87", 
            "usr High " : "ab57c686-648c-4234-880b-ce98ed30e9e2", 
            "usr Low " : "977fc451-daca-486b-b92c-9b05a20b1f3b", 
            "usr Very Low " : "b5087023-3270-45ef-95c6-27d0f67630c0", 
            "usr Near Normal Levels" : "6e3766b5-ff6e-49c2-a6bd-44c2de12d0b5", 
            "writes Very High" : "bf0de32a-30c9-41e8-a104-485801a7d9d9", 
            "writes High" : "24296724-4e3c-4f75-9579-09049e66413a", 
            "writes Low" : "3f72fc32-1929-4d5f-9883-82991ce7cf8e", 
            "writes Very Low" : "1fbc7df3-8f9a-4ec2-ab73-cdd0868f9b02", 
            "user land related activity Very High" : "eda11b3e-8f65-40ff-821d-05a0dd978158", 
            "user land related activity High" : "2ecd934d-cec8-4946-9509-a5013f642027", 
            "user land related activity Low" : "28032515-fcb2-4639-a85d-25a7b3037f03", 
            "user land related activity Very Low" : "bfa94c13-0355-4274-98aa-524456418d29", 
            "nonuser system activity Very High" : "e32eeafe-ffbc-4c99-b826-591f94be63db", 
            "nonuser system activity High" : "3d9c1c7c-faec-4368-8111-c6fc28d4867a", 
            "nonuser system activity Low" : "7ec43da1-ca18-4d9f-a6ed-6431471be456", 
            "nonuser system activity Very Low" : "c945c093-6f3a-42d2-88b0-d00360ea3457", 
        };
        # Note: manualAbstractionInformation is used purely in analysis scripts (as developed for
        #     the paper describing Fanoos); this proved to be a convieniant place to store the
        #     information during the time of development and testing. Fanoos does not access 
        #     the information in manualAbstractionInformation when determining how to make 
        #     adjustments to respond to users. Again, it is only used in analysis scripts
        #     used to prepare results for the paper.
        #
        #     While it was convieniant for development, clearly it is not
        #     ideal have this data stored here or this structure required
        #     to be present. TODO: resolve the issue just described.
        self.manualAbstractionInformation = {\
             "predicatesAndLabels" : [\
            ("d0473bb6-fb13-40bd-b114-deb66c5a3108" , "326e2db9-5b3f-4ac5-b777-e0d46b301458"), \
            ("f772c081-4796-4d82-803e-55c85958a092" , "326e2db9-5b3f-4ac5-b777-e0d46b301458"), \
            ("a21bcdb0-d38b-44cc-8285-cd815efc4687" , "326e2db9-5b3f-4ac5-b777-e0d46b301458"), \
            ("426c8077-2372-4222-9c19-0a6a5487e2bb" , "326e2db9-5b3f-4ac5-b777-e0d46b301458"), \
            ("9b4d6b53-04c1-4f06-be2c-9d6a70bd787d" , "326e2db9-5b3f-4ac5-b777-e0d46b301458"), \
            ("d482ea3a-8549-4300-b454-fb4bb710fb83" , "326e2db9-5b3f-4ac5-b777-e0d46b301458"), \
            ("7a6c6206-11d9-4caf-b69a-641b9aa8908f" , "326e2db9-5b3f-4ac5-b777-e0d46b301458"), \
            ("8787422e-5690-412c-a487-0be85dc55b87" , "326e2db9-5b3f-4ac5-b777-e0d46b301458"), \
            ("c0e0e467-6c8f-4536-9a22-ddc3e8f2f4c2" , "326e2db9-5b3f-4ac5-b777-e0d46b301458"), \
            ("8d8be01c-f46c-4128-8e15-15189c6138ae" , "326e2db9-5b3f-4ac5-b777-e0d46b301458"), \
            ("831efc45-9d8a-439d-9ca3-6cdf56696d7a" , "326e2db9-5b3f-4ac5-b777-e0d46b301458"), \
            ("89362126-a1b5-46dd-8229-9a098157eddf" , "326e2db9-5b3f-4ac5-b777-e0d46b301458"), \
            ("c5396982-66ed-487b-a7a4-107ea056f3be" , "326e2db9-5b3f-4ac5-b777-e0d46b301458"), \
            ("db76fe10-87c6-45dd-95a5-af264bfb1aaa" , "326e2db9-5b3f-4ac5-b777-e0d46b301458"), \
            ("2cbd9e37-b203-4a17-9e32-c24955b1d9a2" , "326e2db9-5b3f-4ac5-b777-e0d46b301458"), \
            ("074f3594-828f-4565-bca2-526bb84f3066" , "326e2db9-5b3f-4ac5-b777-e0d46b301458"), \
            ("64525dd6-f8ad-48dc-b349-95aee377e175" , "326e2db9-5b3f-4ac5-b777-e0d46b301458"), \
            ("b51c470e-4c11-4332-9c5b-a9e6dcb945b3" , "326e2db9-5b3f-4ac5-b777-e0d46b301458"), \
            ("8e1935a7-ae6e-4195-ab92-625cb914b692" , "326e2db9-5b3f-4ac5-b777-e0d46b301458"), \
            ("58b5002b-647a-4fd5-a3ac-4b1b2b4e1ef2" , "326e2db9-5b3f-4ac5-b777-e0d46b301458"), \
            ("b2b18474-577a-47ca-8379-dca459da4f0a" , "326e2db9-5b3f-4ac5-b777-e0d46b301458"), \
            ("ce118774-a9ab-4ddb-9f9a-8c6127d9a7d2" , "326e2db9-5b3f-4ac5-b777-e0d46b301458"), \
            ("4def0fe4-6726-44f9-a247-8d3ba34f3689" , "326e2db9-5b3f-4ac5-b777-e0d46b301458"), \
            ("be17eb25-cc23-4472-bbc5-656619ed6e75" , "326e2db9-5b3f-4ac5-b777-e0d46b301458"), \
            ("fcb4caf7-a3f0-4b4b-9f0c-44fda08525ff" , "326e2db9-5b3f-4ac5-b777-e0d46b301458"), \
            ("77f110ab-e452-417e-9302-ebcb6ab8a8d3" , "9b5a2373-680f-413b-9e37-cc66e59e2880"), \
            ("7cf4b681-5b3f-4f02-9415-1004fcd3ada8" , "9b5a2373-680f-413b-9e37-cc66e59e2880"), \
            ("aa464949-13cb-4af4-8f48-2f125531f516" , "9b5a2373-680f-413b-9e37-cc66e59e2880"), \
            ("8d164d86-ed92-4ba2-bd37-97baaae34f06" , "9b5a2373-680f-413b-9e37-cc66e59e2880"), \
            ("797cde0f-63f3-4967-840e-9ee99e22c660" , "9b5a2373-680f-413b-9e37-cc66e59e2880"), \
            ("7ffac4ab-cf20-4453-8852-aa3743049b14" , "9b5a2373-680f-413b-9e37-cc66e59e2880"), \
            ("c1051f5e-bbf9-46a3-8cbf-6bfab57eba92" , "9b5a2373-680f-413b-9e37-cc66e59e2880"), \
            ("c3c4274b-57a4-4c91-804f-e7cb76af19ab" , "9b5a2373-680f-413b-9e37-cc66e59e2880"), \
            ("52586695-b844-4091-9484-efb038816fcf" , "326e2db9-5b3f-4ac5-b777-e0d46b301458"), \
            ("d520174d-6e84-4d4c-808f-787537f89234" , "326e2db9-5b3f-4ac5-b777-e0d46b301458"), \
            ("adf5a9d0-1653-4f30-a25a-755da7a9283c" , "326e2db9-5b3f-4ac5-b777-e0d46b301458"), \
            ("3ec03fb8-6238-49dd-8ced-8cb86495bfcf" , "326e2db9-5b3f-4ac5-b777-e0d46b301458"), \
            ("58c0edfd-3578-4d4f-987d-9c9f9f972a72" , "326e2db9-5b3f-4ac5-b777-e0d46b301458"), \
            ("4fe47b86-26d8-4477-abef-6b3c5328a321" , "326e2db9-5b3f-4ac5-b777-e0d46b301458"), \
            ("f988e519-e2fa-474d-8e40-72a908e16cee" , "326e2db9-5b3f-4ac5-b777-e0d46b301458"), \
            ("76c5e3fb-238c-446f-8a66-dacb4a850d4b" , "326e2db9-5b3f-4ac5-b777-e0d46b301458"), \
            ("64d6cbdc-28ea-47a9-be37-2e03e2bb0fdd" , "326e2db9-5b3f-4ac5-b777-e0d46b301458"), \
            ("cb4b2c43-9d7c-4a2e-8cca-d6eea9f890f0" , "326e2db9-5b3f-4ac5-b777-e0d46b301458"), \
            ("5da35929-fc1e-4286-85c3-cdfb80a5fb87" , "326e2db9-5b3f-4ac5-b777-e0d46b301458"), \
            ("ab57c686-648c-4234-880b-ce98ed30e9e2" , "326e2db9-5b3f-4ac5-b777-e0d46b301458"), \
            ("977fc451-daca-486b-b92c-9b05a20b1f3b" , "326e2db9-5b3f-4ac5-b777-e0d46b301458"), \
            ("b5087023-3270-45ef-95c6-27d0f67630c0" , "326e2db9-5b3f-4ac5-b777-e0d46b301458"), \
            ("6e3766b5-ff6e-49c2-a6bd-44c2de12d0b5" , "326e2db9-5b3f-4ac5-b777-e0d46b301458"), \
            ("bf0de32a-30c9-41e8-a104-485801a7d9d9" , "9b5a2373-680f-413b-9e37-cc66e59e2880"), \
            ("24296724-4e3c-4f75-9579-09049e66413a" , "9b5a2373-680f-413b-9e37-cc66e59e2880"), \
            ("3f72fc32-1929-4d5f-9883-82991ce7cf8e" , "9b5a2373-680f-413b-9e37-cc66e59e2880"), \
            ("1fbc7df3-8f9a-4ec2-ab73-cdd0868f9b02" , "9b5a2373-680f-413b-9e37-cc66e59e2880"), \
            ("eda11b3e-8f65-40ff-821d-05a0dd978158" , "9b5a2373-680f-413b-9e37-cc66e59e2880"), \
            ("2ecd934d-cec8-4946-9509-a5013f642027" , "9b5a2373-680f-413b-9e37-cc66e59e2880"), \
            ("28032515-fcb2-4639-a85d-25a7b3037f03" , "9b5a2373-680f-413b-9e37-cc66e59e2880"), \
            ("bfa94c13-0355-4274-98aa-524456418d29" , "9b5a2373-680f-413b-9e37-cc66e59e2880"), \
            ("e32eeafe-ffbc-4c99-b826-591f94be63db" , "9b5a2373-680f-413b-9e37-cc66e59e2880"), \
            ("3d9c1c7c-faec-4368-8111-c6fc28d4867a" , "9b5a2373-680f-413b-9e37-cc66e59e2880"), \
            ("7ec43da1-ca18-4d9f-a6ed-6431471be456" , "9b5a2373-680f-413b-9e37-cc66e59e2880"), \
            ("c945c093-6f3a-42d2-88b0-d00360ea3457" , "9b5a2373-680f-413b-9e37-cc66e59e2880"), \
             ], \
             "labelDag_firstParent_secondChild" : [ \
             ("9b5a2373-680f-413b-9e37-cc66e59e2880" , "326e2db9-5b3f-4ac5-b777-e0d46b301458") \
             ] \
        };

        functToGetUuidProvided = (lambda predicateObjectBeingInitialized : 
            dictMappingPredicateStringNameToUUID[str(predicateObjectBeingInitialized)] );
        self.initializedConditions = \
            [CharacterizationCondition_FromPythonFunction(z3SolverInstance, DomainForCPUUse, x, functToGetUuidProvided=functToGetUuidProvided) \
             for x in getListFunctionsToBaseCondtionsOn_forInputOfDomainCPUUse() + \
                      getListFunctionsToBaseCondtionsOn_forOutputOfDomainCPUUse() + \
                      getListFunctionsToBaseCondtionsOn_forJointInputAndOutputDomainsInCPUUse() ];
               
            

        assert(all([ (x.getID() == functToGetUuidProvided(x)) for x in self.initializedConditions]));
        self._writeInfoToDatabase();
        return;

    def getBaseConditions(self):
        return self.initializedConditions;




#V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V
# class-specific utilities for defining domains
#===========================================================================


def getFunctionsCouplingValues(functionBaseName, varaiblesToUse, \
    listOfVariablesInSpace, quantile0Dot90, \
    quantile0Dot75, quantile0Dot25, quantile0Dot10, medians, stds):
    requires(isinstance(varaiblesToUse, list));
    requires(len(varaiblesToUse) > 0);
    requires(all([isinstance(x, str) for x in ([functionBaseName] + varaiblesToUse)]));
    requires(all([(len(x) > 0) for x in ([functionBaseName] + varaiblesToUse)]));
    requires(len(set(([functionBaseName] + varaiblesToUse))) == \
             len(([functionBaseName] + varaiblesToUse))  ); # checking that the variable names are unique...
    requires(set(varaiblesToUse).issubset(listOfVariablesInSpace));

    functionCodeToReturn = [];

    def sumBasedOnIndices(thisListOfValues):
        return sum([thisListOfValues[listOfVariablesInSpace.index(thisValue)] for thisValue in varaiblesToUse]);
    
    namesAndThresHolds = [\
        (" Very High" , " >= " + str(sumBasedOnIndices(quantile0Dot90))   ), \
        (" High" , " >= " + str(sumBasedOnIndices(quantile0Dot75))     ), \
        (" Low"  , " <= "  + str(sumBasedOnIndices(quantile0Dot25))    ), \
        (" Very Low" , " <= "  + str(sumBasedOnIndices(quantile0Dot10))     ) \
    ];
    for thisNameAndThresHold in namesAndThresHolds:
        functionName = functionBaseName + thisNameAndThresHold[0];
        functionName = functionName.replace("  ", " ").replace("  ", " "); # I could do this replacement 
            # until the length converges, but doing that seems silly since this should cover the 
            # wide majority of cases.
        functionNameWithSpacesRemoved = functionName.replace(" ", "");
        thisFunctionCode = createFunct_SumThresholdCompare(functionName, \
            varaiblesToUse, thisNameAndThresHold[1] );
        functionCodeToReturn.append(thisFunctionCode);

    return functionCodeToReturn;


#^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^



#V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V
# Conditions over the input domain
#===========================================================================

otherInputSpaceFunctionsToUse = """
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

def getListFunctionsToBaseCondtionsOn_forInputOfDomainCPUUse():
    listOfFunctionCodes =[];
    inputSpaceVariables = ['lread', 'scall', 'sread', 'freemem', 'freeswap'];
    quantile0Dot90 = [0.02439024, 0.35714632, 0.07868976, 0.53894086, 0.82341586];
    quantile0Dot75 = [0.01084011, 0.25906411, 0.05139307, 0.16265035, 0.77139313];
    quantile0Dot25 = [0.00108401, 0.07291667, 0.01506024, 0.01470097, 0.46479515];
    quantile0Dot10 = [0.00054201, 0.02091408, 0.00623117, 0.00760107, 0.44180199];
    medians = [0.00379404, 0.15685562, 0.03012048, 0.04376879, 0.57475754];
    stds = [0.02891628, 0.13190549, 0.03745633, 0.20731315, 0.18812254];
    listOfFunctionCodes = \
        getFunctionCodeBasedOnThresholdsAndIndividualVariables(inputSpaceVariables, quantile0Dot90, \
            quantile0Dot75, quantile0Dot25, quantile0Dot10, medians, stds);
    listOfFunctionCodes = \
        listOfFunctionCodes + \
        getFunctionsCouplingValues("Free Space", ['freemem', 'freeswap'], \
           inputSpaceVariables, quantile0Dot90, \
           quantile0Dot75, quantile0Dot25, quantile0Dot10, medians, stds);
    listOfFunctionCodes = \
        listOfFunctionCodes + \
        getFunctionsCouplingValues("reads", ['lread', 'sread'], \
           inputSpaceVariables, quantile0Dot90, \
           quantile0Dot75, quantile0Dot25, quantile0Dot10, medians, stds);

    return convertCodeListToListOfFunctions(listOfFunctionCodes);


#^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^


#V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V
# Conditions over the output domain
#===========================================================================

otherOutputSpaceFunctionsToUse = """

""";


def getListFunctionsToBaseCondtionsOn_forOutputOfDomainCPUUse():
    listOfFunctionCodes =[];
    outputSpaceVariables = ['lwrite', 'swrite', 'usr']
    quantile0Dot90 = [0.08,       0.05303725, 0.97979798];
    quantile0Dot75 = [0.0173913,  0.03266654, 0.94949495];
    quantile0Dot25 = [0.0,        0.01027712, 0.81818182];
    quantile0Dot10 = [0.0,        0.00440448, 0.72727273];
    medians =        [0.00173913, 0.02018719, 0.8989899 ];
    stds =           [0.05198244, 0.02944929, 0.18586648];
    listOfFunctionCodes = \
        getFunctionCodeBasedOnThresholdsAndIndividualVariables(outputSpaceVariables, quantile0Dot90, \
            quantile0Dot75, quantile0Dot25, quantile0Dot10, medians, stds);
    listOfFunctionCodes = \
        listOfFunctionCodes + \
        getFunctionsCouplingValues("writes", ['lwrite', 'swrite'], \
           outputSpaceVariables, quantile0Dot90, \
           quantile0Dot75, quantile0Dot25, quantile0Dot10, medians, stds);
    return convertCodeListToListOfFunctions(listOfFunctionCodes);

#^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^



#V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V
# Conditions over the joint domain
#===========================================================================


def getListFunctionsToBaseCondtionsOn_forJointInputAndOutputDomainsInCPUUse():
    listOfFunctionCodes =[];
    variables = ['lread', 'scall', 'sread', 'freemem', 'freeswap'];
    quantile0Dot90 = [0.02439024, 0.35714632, 0.07868976, 0.53894086, 0.82341586];
    quantile0Dot75 = [0.01084011, 0.25906411, 0.05139307, 0.16265035, 0.77139313];
    quantile0Dot25 = [0.00108401, 0.07291667, 0.01506024, 0.01470097, 0.46479515];
    quantile0Dot10 = [0.00054201, 0.02091408, 0.00623117, 0.00760107, 0.44180199];
    medians = [0.00379404, 0.15685562, 0.03012048, 0.04376879, 0.57475754];
    stds = [0.02891628, 0.13190549, 0.03745633, 0.20731315, 0.18812254];
    variables = variables + ['lwrite', 'swrite', 'usr']
    quantile0Dot90 = quantile0Dot90+ [0.08,       0.05303725, 0.97979798];
    quantile0Dot75 = quantile0Dot75 + [0.0173913,  0.03266654, 0.94949495];
    quantile0Dot25 = quantile0Dot25 + [0.0,        0.01027712, 0.81818182];
    quantile0Dot10 = quantile0Dot10 + [0.0,        0.00440448, 0.72727273];
    medians =        medians + [0.00173913, 0.02018719, 0.8989899 ];
    stds =           stds + [0.05198244, 0.02944929, 0.18586648];
    listOfFunctionCodes = \
        listOfFunctionCodes + \
        getFunctionsCouplingValues("user land related activity ", ['lwrite', 'lread', 'usr'], \
           variables, quantile0Dot90, \
           quantile0Dot75, quantile0Dot25, quantile0Dot10, medians, stds);
    listOfFunctionCodes = \
        listOfFunctionCodes + \
        getFunctionsCouplingValues("nonuser system activity", ['scall', 'sread', 'swrite'], \
           variables, quantile0Dot90, \
           quantile0Dot75, quantile0Dot25, quantile0Dot10, medians, stds);
    return convertCodeListToListOfFunctions(listOfFunctionCodes);

#^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^


