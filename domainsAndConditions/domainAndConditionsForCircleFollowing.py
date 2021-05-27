

import config;
_LOCALDEBUGFLAG = config.debugFlags.get_v_print_ForThisFile(__file__);
    

import numpy as np;
import sys;
from utils.contracts import *;

from boxesAndBoxOperations.getBox import getDimensionOfBox ;

import re;

import z3;

from domainsAndConditions.baseClassConditionsToSpecifyPredictsWith import CharacterizationConditionsBaseClass, CharacterizationCondition_FromPythonFunction;
from domainsAndConditions.baseClassDomainInformation import BaseClassDomainInformation ;



class DomainForCircleFollowing(BaseClassDomainInformation):


    def __init__(self, z3SolverInstance):
        requires(isinstance(z3SolverInstance, z3.z3.Solver));
        raise Exception("The domain for the Circle Following controllerd " + \
            "is not supported in this code release. See the README.txt file. "+\
            "Inclusion of this domain's source code is purely for " + \
            "reference for the curious - we selected to show an " + \
            "implementation that is old in respect to updates of Fanoos.");
        self.initializedConditions = None;
        self.initialize_baseConditions(z3SolverInstance);
        assert(self.initializedConditions != None);
        return;

    @staticmethod
    def getUUID():
        return "8827094e-c421-463f-98f5-36dc411f29e7";

    @staticmethod
    def getInputSpaceUniverseBox():
        orderOfVariables = __class__.inputSpaceVariables();
        dictMappingVariableToBound = {\
            "inputDx" : [-0.25 , 0.25],\
            "inputTheta" : [-np.pi /2.0 , np.pi /2.0],\
            "inputDxDot" : [-1.5 , 1.5],\
            "inputThetaDot" : [-3.625 , 3.625] \
        };
        thisUniverseBox =  __class__._helper_getInputSpaceUniverseBox(\
                               orderOfVariables, dictMappingVariableToBound);
        ensures(getDimensionOfBox(thisUniverseBox) == len(DomainForCircleFollowing.inputSpaceVariables()));
        return thisUniverseBox;

    @staticmethod
    def inputSpaceVariables():
        # see the function _state_to_relative in ./envs/circle_env.py , line 113.
        return [z3.Real("inputDx"), z3.Real("inputTheta"), z3.Real("inputDxDot"), z3.Real("inputThetaDot")]; 

    @staticmethod
    def outputSpaceVariables():
        return [z3.Real("outputVelocity"), z3.Real("outputSteeringAngle")];


    @staticmethod
    def getName():
        return "Domain for Circle Following [not supported in this release; see README.txt]";

    def initialize_baseConditions(self, z3SolverInstance):
        dictMappingPredicateStringNameToUUID = \
        {
            "Close To Target Position" : "9ee7ee55-c605-4e58-a7a3-aba6973de71c", 
            "NotClose To Target Position" : "49d3939c-2bdc-42f2-b97b-e6c223afcd45", 
            "NotFar To Target Position" : "47148b78-cea3-4f6e-8174-b578bc8ba924", 
            "Far To Target Position" : "c93e7cd5-d2a1-4544-b48c-ac80b69f7686", 
            "Moving Toward Target Position" : "fb18ac46-407b-4e32-a4ed-b0e8ee565778", 
            "Moving Quickly Toward Target Position" : "24795eb1-067e-4e8d-864a-d94150da9658", 
            "Moving Slowly Toward Target Position" : "18555dce-9f90-454f-a206-357e6cd39da6", 
            "Moving Away From Target Position" : "2d226265-9a7e-4c35-863d-5ace4304bdca", 
            "Moving Quickly Away From Target Position" : "440e8ab1-8db4-4921-bb7f-4b95c2feed69", 
            "Moving Slowly Away From Target Position" : "4cb7ed4f-762f-4964-877b-5d26398833e8", 
            "Close To Target Orientation" : "efc4aded-b408-4bfa-8b95-17f381faa155", 
            "NotClose To Target Orientation" : "025472ee-f2f0-4fd2-853b-d651305d7443", 
            "NotFar To Target Orientation" : "3ff7e1c6-966e-4170-91f4-4db8b02d6e9f", 
            "Far To Target Orientation" : "b7d26e79-2f04-49ff-a73f-3ce68c52dc4a", 
            "Moving Toward Target Orientation" : "977d6db2-26a4-4808-a44c-3930f35303d3", 
            "Moving Quickly Toward Target Orientation" : "102a4a1f-728e-4084-9ddd-bfcc5d556e56", 
            "Moving Slowly Toward Target Orientation" : "f4f6c19e-63c5-4e40-8163-ed0bac55605a", 
            "Moving Away From Target Orientation" : "d6687f9c-f937-45b4-a9c6-83ac73b9b519", 
            "Moving Quickly Away From Target Orientation" : "23c33313-6238-491a-bfbf-a13a50241c86", 
            "Moving Slowly Away From Target Orientation" : "99722d5a-472e-49d6-b2a5-ce9fd238135c", 
            "Moving at Low Speed" : "3ffc400e-4d80-42e8-8f04-5e63c9fed46e", 
            "Moving at Moderate Speed" : "20a2e808-ba75-4711-8180-21ac2220b02f", 
            "Moving at High Speed" : "0f39b35a-9742-48a8-a6fc-aef30b07ca30", 
            "Steering Close to Center" : "98e04364-4d18-4086-9d03-faeff2983771", 
            "Steering to Right" : "63d94834-6936-42ab-8bc4-007486059a4a", 
            "Steering to Left" : "8029d02d-e719-4016-8231-b31301f112d6", 
            "Steering Far to Right" : "97adc025-0842-455c-b4a5-d98fe6d06bf9", 
            "Steering Far to Left" : "7b554b6a-1800-4a9b-ab34-58d5fac2fada"
        };
        functToGetUuidProvided = (lambda predicateObjectBeingInitialized : 
            dictMappingPredicateStringNameToUUID[str(predicateObjectBeingInitialized)] );
    
        self.initializedConditions = \
            [CharacterizationCondition_FromPythonFunction(z3SolverInstance, DomainForCircleFollowing, x, functToGetUuidProvided=functToGetUuidProvided) \
             for x in getListFunctionsToBaseCondtionsOn_forInputOfDomainCircleFollowing() + \
                      getListFunctionsToBaseCondtionsOn_forOutputOfDomainCircleFollowing() ];
        assert(all([ (x.getID() == functToGetUuidProvided(x)) for x in self.initializedConditions]));
        self._writeInfoToDatabase();
        return;

    def getBaseConditions(self):
        return self.initializedConditions;


#V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~VV~V~V~V~V~V~V~V~V~V~~V~V~V
# Input domain
#-----------------------------------------------------------------------------


def z3Abs(x):
    return z3.If(x >= 0,x,-x)


def z3Sign(x):
    return z3.If(x > 0,1,0) + z3.If(x < 0,-1,0);




def createFunctToUseInInputDescription_RelativeDistanceToTarget(endPartOfName, adjectiveForDescription, var, comparitorAndScalarString):
    codeForFunct = """
def funct_{0}ToTarget{1}({2}):
    \"\"\"{0} To Target {1}\"\"\"
    if(isinstance({2}, z3.z3.ArithRef)):
        return z3Abs({2}) {3};
    else:
        return np.abs({2}) {3};
    raise Exception("Control should not reach here");
    return;
    """

    return codeForFunct.format(adjectiveForDescription, endPartOfName, var, comparitorAndScalarString);



def createFunctToUseInInputDescription_MovingTowardTargetWithNoCommentOnSpeed(endPartOfName, var, varDot):

    codeForFunct = """
def funct_MovingTowardTarget{1}({2}, {3}):
    \"\"\"Moving Toward Target {1}\"\"\"
    if(isinstance({2}, z3.z3.ArithRef)):
        return (z3Sign({2}) + z3Sign({3}) == 0);
    else:
        return (np.sign({2}) + np.sign({3}) == 0);
    raise Exception("Control should not reach here");
    return;
    """

    return codeForFunct.format("", endPartOfName, var, varDot);



def createFunctToUseInInputDescription_MovingTowardTargetAtSpeed(endPartOfName, adjectiveForDescription, var, varDot, comparitorAndScalarString):

    codeForFunct = """
def funct_Moving{0}TowardTarget{1}({2}, {3}):
    \"\"\"Moving {0} Toward Target {1}\"\"\"
    if(isinstance({2}, z3.z3.ArithRef)):
        return z3.And( z3Sign({2}) + z3Sign({3}) == 0, \\
                       z3Abs({3}) {4});
    else:
        return  (np.sign({2}) + np.sign({3}) == 0) and \\
               (np.abs({3}) {4} );
    raise Exception("Control should not reach here");
    return;
    """

    return codeForFunct.format(adjectiveForDescription, endPartOfName, var, varDot, comparitorAndScalarString);




def createFunctToUseInInputDescription_MovingAwayFromTargetWithNoCommentOnSpeed(endPartOfName, var, varDot):

    codeForFunct = """
def funct_MovingAwayFromTarget{1}({2}, {3}):
    \"\"\"Moving Away From Target {1}\"\"\"
    if(isinstance({2}, z3.z3.ArithRef)):
        return z3.Not(z3Sign({2}) + z3Sign({3}) == 0);
    else:
        return (np.sign({2}) + np.sign({3}) != 0);
    raise Exception("Control should not reach here");
    return;
    """

    return codeForFunct.format("", endPartOfName, var, varDot);


def createFunctToUseInInputDescription_MovingAwayFromTargetAtSpeed(endPartOfName, adjectiveForDescription, var, varDot, comparitorAndScalarString):

    codeForFunct = """
def funct_Moving{0}AwayFromTarget{1}({2}, {3}):
    \"\"\"Moving {0} Away From Target {1}\"\"\"
    if(isinstance({2}, z3.z3.ArithRef)):
        return z3.And( z3.Not(z3Sign({2}) + z3Sign({3}) == 0), \\
                       z3Abs({3}) {4});
    else:
        return (np.sign({2}) + np.sign({3}) != 0) and \\
               (np.abs({3}) {4} );
    raise Exception("Control should not reach here");
    return;
    """

    return codeForFunct.format(adjectiveForDescription, endPartOfName, var, varDot, comparitorAndScalarString);


def getListFunctionsToBaseCondtionsOn_forInputOfDomainCircleFollowing():
    listOfFunctionsToCreate = [\
        createFunctToUseInInputDescription_RelativeDistanceToTarget("Position", "Close", "inputDx", "< 0.025"), \
        createFunctToUseInInputDescription_RelativeDistanceToTarget("Position", "NotClose", "inputDx", ">= 0.025"), \
        createFunctToUseInInputDescription_RelativeDistanceToTarget("Position", "NotFar", "inputDx", "< 0.1"), \
        createFunctToUseInInputDescription_RelativeDistanceToTarget("Position", "Far", "inputDx", ">= 0.1"), \
        createFunctToUseInInputDescription_MovingTowardTargetWithNoCommentOnSpeed("Position", "inputDx", "inputDxDot"), \
        createFunctToUseInInputDescription_MovingTowardTargetAtSpeed("Position", "Quickly", "inputDx", "inputDxDot", " > 0.75"), \
        createFunctToUseInInputDescription_MovingTowardTargetAtSpeed("Position", "Slowly", "inputDx", "inputDxDot", " <= 0.1"), \
        createFunctToUseInInputDescription_MovingAwayFromTargetWithNoCommentOnSpeed("Position", "inputDx", "inputDxDot"), \
        createFunctToUseInInputDescription_MovingAwayFromTargetAtSpeed("Position", "Quickly", "inputDx", "inputDxDot", " > 0.75"), \
        createFunctToUseInInputDescription_MovingAwayFromTargetAtSpeed("Position", "Slowly", "inputDx", "inputDxDot", " <= 0.1"), \
        createFunctToUseInInputDescription_RelativeDistanceToTarget("Orientation", "Close", "inputTheta", "< 0.1"), \
        createFunctToUseInInputDescription_RelativeDistanceToTarget("Orientation", "NotClose", "inputTheta", ">= 0.1"), \
        createFunctToUseInInputDescription_RelativeDistanceToTarget("Orientation", "NotFar", "inputTheta", "< 0.3"), \
        createFunctToUseInInputDescription_RelativeDistanceToTarget("Orientation", "Far", "inputTheta", ">= 0.3"), \
        createFunctToUseInInputDescription_MovingTowardTargetWithNoCommentOnSpeed("Orientation", "inputTheta", "inputThetaDot"), \
        createFunctToUseInInputDescription_MovingTowardTargetAtSpeed("Orientation", "Quickly", "inputTheta", "inputThetaDot", " > 0.75"), \
        createFunctToUseInInputDescription_MovingTowardTargetAtSpeed("Orientation", "Slowly", "inputTheta", "inputThetaDot", " <= 0.1"), \
        createFunctToUseInInputDescription_MovingAwayFromTargetWithNoCommentOnSpeed("Orientation", "inputTheta", "inputThetaDot"), \
        createFunctToUseInInputDescription_MovingAwayFromTargetAtSpeed("Orientation", "Quickly", "inputTheta", "inputThetaDot", " > 0.75"), \
        createFunctToUseInInputDescription_MovingAwayFromTargetAtSpeed("Orientation", "Slowly", "inputTheta", "inputThetaDot", " <= 0.1") \
        ];

    listOfFunctionsToReturn = [];
    for thisFunctionDefinition in listOfFunctionsToCreate:
        initialSetOfDefinedFunctions = set(locals().keys());
        exec(thisFunctionDefinition);
        newSetOfDefinedFunctions = set(locals().keys()).difference(\
                      initialSetOfDefinedFunctions).difference(\
                          ["initialSetOfDefinedFunctions", "newSetOfDefinedFunctions", "thisFunctionDefinition"]);
        assert(len(newSetOfDefinedFunctions) == 1);
        listOfFunctionsToReturn.append(locals()[list(newSetOfDefinedFunctions)[0]]);
    assert(len(listOfFunctionsToReturn) == len(listOfFunctionsToCreate));
    
    return listOfFunctionsToReturn;
#^_^_^_^_^_^_^_^_^_^_^_^_^_^_^^_^_^_^^_^_^_^^_^_^_^_^_^^_^_^_^_^_^^_^_^_^_^_^_^_^



#V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~VV~V~V~V~V~V~V~V~V~V~~V~V~V
# Output domain
#-----------------------------------------------------------------------------




def createFunctToUseInOutputDescription_absThresholdCompare(name, var, comparitorAndScalarString):
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


def createFunctToUseInOutputDescription_thresholdCompare(name, var, comparitorAndScalarString):
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


def getListFunctionsToBaseCondtionsOn_forOutputOfDomainCircleFollowing():
    listOfFunctionsToCreate = [\
        createFunctToUseInOutputDescription_absThresholdCompare("Moving at Low Speed", "outputVelocity", " < 0.1 "), \
        createFunctToUseInOutputDescription_absThresholdCompare("Moving at Moderate Speed", "outputVelocity", " < 0.65 "), \
        createFunctToUseInOutputDescription_absThresholdCompare("Moving at High Speed", "outputVelocity", " >= 0.65 "),  \
        createFunctToUseInOutputDescription_absThresholdCompare("Steering Close to Center", "outputSteeringAngle", " <= 0.1 "),  \
        createFunctToUseInOutputDescription_thresholdCompare("Steering to Right", "outputSteeringAngle", " > 0"), \
        createFunctToUseInOutputDescription_thresholdCompare("Steering to Left", "outputSteeringAngle", " < 0"), \
        createFunctToUseInOutputDescription_thresholdCompare("Steering Far to Right", "outputSteeringAngle", " > np.pi / 8.0"), \
        createFunctToUseInOutputDescription_thresholdCompare("Steering Far to Left", "outputSteeringAngle", " < -np.pi / 8.0") \
        ];
    listOfFunctionsToReturn = [];
    for thisFunctionDefinition in listOfFunctionsToCreate:
        initialSetOfDefinedFunctions = set(locals().keys());
        exec(thisFunctionDefinition);
        newSetOfDefinedFunctions = set(locals().keys()).difference(\
                      initialSetOfDefinedFunctions).difference(\
                          ["initialSetOfDefinedFunctions", "newSetOfDefinedFunctions", "thisFunctionDefinition"]);
        assert(len(newSetOfDefinedFunctions) == 1);
        listOfFunctionsToReturn.append(locals()[list(newSetOfDefinedFunctions)[0]]);
    assert(len(listOfFunctionsToReturn) == len(listOfFunctionsToCreate));
    return listOfFunctionsToReturn;







#^_^_^_^_^_^_^_^_^_^_^_^_^_^_^^_^_^_^^_^_^_^^_^_^_^_^_^^_^_^_^_^_^^_^_^_^_^_^_^_^


