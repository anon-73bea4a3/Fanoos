

import config;
_LOCALDEBUGFLAG = config.debugFlags.get_v_print_ForThisFile(__file__);
    

from utils.contracts import *;
from boxesAndBoxOperations.getBox import isProperBox, getBox, getDimensionOfBox, getJointBox, getContainingBox, getRandomBox;
import numpy as np;

def sideInformationIsProper(sideInformation):
    # The side information must either be none or an integer expressable in 5 bits. Why 5 bits? See 
    # <root of git repo>/CEGARLikeAnalysis/refinementPathRecorder.py
    try:
        return ( (sideInformation is None) or \
            (isinstance(sideInformation, int) and (sideInformation >= 0 and sideInformation < 32)) );
    except:
        return False;
    raise Exception("Control should never reach here");
    return;

# The scalingFactors option below is useful for times when the box under
# consideration is composed of axis that represent different units of have
# different sensitivites. For example, if a box is (number of inches to the moon) X (radians of orientation of travel)
# , it may be allowable to have the first coordinate vary by +/-4 without 
# effecting anything , while if the second coordinate can change by that much, what
# it represents can before completely altered. That is an example of both a difference
# in scale and a difference in type leading to scaling to be desireable. Another example
# that is simply a difference in scaling is (number of inches to reach the moon) x (number of inches surgery is from major artery)
#
# When scalingFactors as a nan value in a position, the resulting
# box in not split along the axis that has that nan value...
def splitBox(thisBox, stringSpecifyingStyleOfSplit, scalingFactors=None, sideInformation=None):
    requires(isProperBox(thisBox));
    requires(isinstance(stringSpecifyingStyleOfSplit, str));
    requires((isinstance(scalingFactors, type(None))) or (isinstance(scalingFactors, np.ndarray)));
    requires((isinstance(scalingFactors, type(None))) or (scalingFactors.shape==tuple([getDimensionOfBox(thisBox)])));
    requires( sideInformationIsProper(sideInformation) );

    if(isinstance(scalingFactors, type(None))):
        raise Exception("While scalingFactors = None is supported in splitBox currently, use of " + \
            "None as the scalling axis has been disabled elsewhere in the code. Thus, this is a " +\
            "sign that the caller is in error - which is why this function (splitBox) is raising an " + \
            "exception to alert the user to something that should not be occuring if the code is in " + \
            "sync on the latest revisions.");

    dictMappingStyleOfSplitToFunction = {\
        "halvingAllAxis" : splitBox_halvingAllAxis ,\
        "halfLongestAxis" : splitBox_halfLongestAxis, \
        "randomSplittingLongestAxis" : splitBox_randomSplittingLongestAxis, \
        "randomNumberOfUniformSplits_old" :  splitBox_randomNumberOfUniformSplits_old, \
        "randomNumberOfUniformSplits" :  splitBox_randomNumberOfUniformSplits \
        };

    if(stringSpecifyingStyleOfSplit not in dictMappingStyleOfSplitToFunction.keys()):
        raise Exception("splitBox: stringSpecifyingStyleOfSplit not in dictMappingStyleOfSplitToFunction.keys()");

    boxToSplit = thisBox;
    if(not isinstance(scalingFactors, type(None))):
       boxToSplit = thisBox / scalingFactors.reshape((getDimensionOfBox(thisBox), 1));
    boxToSplit[np.isnan(boxToSplit)] = 0;


    rawReturn =  dictMappingStyleOfSplitToFunction[stringSpecifyingStyleOfSplit](boxToSplit, sideInformation);
    valueToReturn = [];
    if(not isinstance(scalingFactors, type(None))):
        for thisTempBox in rawReturn:
            valueToReturn.append(thisTempBox  *  scalingFactors.reshape((getDimensionOfBox(thisBox), 1)));
            valueToReturn[-1][np.isnan(scalingFactors)] = \
                    thisBox[np.isnan(scalingFactors)]
    else:
        valueToReturn = rawReturn;


    # The value valueToReturn is allowed to be None when the splitting
    # procedure values to produce a new box - that is, the point is a 
    # fixed point for the splitting procedure. Letting the calling
    # function now this by returning None explicitly can be helpful.
    ensures((valueToReturn == None) or (isinstance(valueToReturn, list)));
    ensures((valueToReturn == None) or (len(valueToReturn)  >= 2));
    ensures((valueToReturn == None) or all([isProperBox(x) for x in valueToReturn]));
    ensures((valueToReturn == None) or np.all(np.isclose(getContainingBox(valueToReturn), thisBox)));
    # Below basically says that if valueToReturn is not-None and 
    # the user did not specify a scaling factor, than equality should hold.... this is probably
    # a skectchy guarentee to even try to make considering we want to allow
    # more advanced splitting, but for now it looks like it will hold, and it is nice to know.
    ensures((valueToReturn == None) or (isinstance(scalingFactors, type(None)) or np.all(np.isclose(getContainingBox(valueToReturn), thisBox))));
    return valueToReturn;



def splitBox_halvingAllAxis(thisBox):
    raise Exception("Not Yet Implemented");

def splitBox_halfLongestAxis(thisBox):
    requires(isProperBox(thisBox));
    
    if(np.all(thisBox[:, 0] == thisBox[:, 1])):
        # The box is completely flat, nothing can be split...
        return None;
 
    indexOfAxisToSplitOn = np.argmax(thisBox[:, 1] - thisBox[:,0]);
    middleOfAxisValue = np.mean(thisBox[indexOfAxisToSplitOn, :]);

    boxA = thisBox.copy();
    boxB = thisBox.copy();

    boxA[indexOfAxisToSplitOn, :] = np.array([thisBox[indexOfAxisToSplitOn, 0], middleOfAxisValue]);

    boxB[indexOfAxisToSplitOn, :] = np.array([middleOfAxisValue, thisBox[indexOfAxisToSplitOn, 1]]);

    return [boxA, boxB];


def splitBox_randomSplittingLongestAxis(thisBox, sideInformation=None):
    requires(isProperBox(thisBox));
    requires( sideInformationIsProper(sideInformation) );

    raise Exception("This splitting process is not currently supported due to the " + \
        "inability to effectively store the split boundaries (which are random " +\
        "floating-point values) in the limits of the sideInformation we are currently " +\
        "willing and able to store.");

    if(np.all(thisBox[:, 0] == thisBox[:, 1])):
        # The box is completely flat, nothing can be split...
        return None;

    indexOfAxisToSplitOn = np.argmax(thisBox[:, 1] - thisBox[:,0]);
    # middleOfAxisValue = np.mean(thisBox[indexOfAxisToSplitOn, :]);
    numberOfRandomValuesToUse = np.random.randint(2,5);
    newCutOffs = \
        np.sort(np.random.rand(numberOfRandomValuesToUse) * (thisBox[indexOfAxisToSplitOn,1] - thisBox[indexOfAxisToSplitOn,0]) + thisBox[indexOfAxisToSplitOn,0]);
    newCutoffs = [thisBox[indexOfAxisToSplitOn, 0]] + list(newCutOffs) + [thisBox[indexOfAxisToSplitOn, 1]];

    boxesToReturn = [];
    assert(len(newCutoffs) > 1);
    for thisIndex in range(0, len(newCutoffs) - 1):
        newBox = thisBox.copy();
        newBox[indexOfAxisToSplitOn, :] = np.array([newCutoffs[thisIndex], newCutoffs[thisIndex + 1]]);
        boxesToReturn.append(newBox);

    return boxesToReturn;



def splitBox_randomNumberOfUniformSplits_old(thisBox, sideInformation=None):
    requires(isProperBox(thisBox));
    requires( sideInformationIsProper(sideInformation) );

    if(np.all(thisBox[:, 0] == thisBox[:, 1])):
        # The box is completely flat, nothing can be split...
        return None;

    indexOfAxisToSplitOn = np.argmax(thisBox[:, 1] - thisBox[:,0]);
    # middleOfAxisValue = np.mean(thisBox[indexOfAxisToSplitOn, :]);
    numberOfRandomValuesToUse = sideInformation;
    if(numberOfRandomValuesToUse is None):
        numberOfRandomValuesToUse = np.random.randint(0,11);
        if(numberOfRandomValuesToUse < 4):
            numberOfRandomValuesToUse = 2; """ ssh-rsa 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 abc@defg  """
        else:
            numberOfRandomValuesToUse = int(numberOfRandomValuesToUse / 2);
    assert(isinstance(numberOfRandomValuesToUse, int));
    assert(numberOfRandomValuesToUse >= 2);
    assert(numberOfRandomValuesToUse <= 5);
    newCutOffs = \
       [ ((float(x) / numberOfRandomValuesToUse) * (thisBox[indexOfAxisToSplitOn,1] - thisBox[indexOfAxisToSplitOn,0]) + thisBox[indexOfAxisToSplitOn,0]) \
         for x in range(1, numberOfRandomValuesToUse)];
    newCutoffs = [thisBox[indexOfAxisToSplitOn, 0]] + list(newCutOffs) + [thisBox[indexOfAxisToSplitOn, 1]];

    boxesToReturn = [];
    assert(len(newCutoffs) > 1);
    for thisIndex in range(0, len(newCutoffs) - 1):
        newBox = thisBox.copy();
        newBox[indexOfAxisToSplitOn, :] = np.array([newCutoffs[thisIndex], newCutoffs[thisIndex + 1]]);
        boxesToReturn.append(newBox);

    return boxesToReturn;




def splitBox_randomNumberOfUniformSplits(thisBox, sideInformation=None):
    requires(isProperBox(thisBox));
    requires( sideInformationIsProper(sideInformation) );

    if(np.all(thisBox[:, 0] == thisBox[:, 1])):
        # The box is completely flat, nothing can be split...
        return None;

    indexOfAxisToSplitOn = np.argmax(thisBox[:, 1] - thisBox[:,0]);
    # 4/5 probability of numberOfRandomValuesToUse == 2, 1/5 probability of numberOfRandomValuesToUse == 3

    numberOfRandomValuesToUse= sideInformation;
    if(numberOfRandomValuesToUse is None):
        numberOfRandomValuesToUse = int(np.random.randint(0,5) >= 4) + 2;
    assert(isinstance(numberOfRandomValuesToUse, int));
    assert(numberOfRandomValuesToUse >= 2);
    assert(numberOfRandomValuesToUse <= 3);
    newCutOffs = \
       [ ((float(x) / numberOfRandomValuesToUse) * (thisBox[indexOfAxisToSplitOn,1] - thisBox[indexOfAxisToSplitOn,0]) + thisBox[indexOfAxisToSplitOn,0]) \
         for x in range(1, numberOfRandomValuesToUse)];
    newCutoffs = [thisBox[indexOfAxisToSplitOn, 0]] + list(newCutOffs) + [thisBox[indexOfAxisToSplitOn, 1]];

    boxesToReturn = [];
    assert(len(newCutoffs) > 1);
    for thisIndex in range(0, len(newCutoffs) - 1):
        newBox = thisBox.copy();
        newBox[indexOfAxisToSplitOn, :] = np.array([newCutoffs[thisIndex], newCutoffs[thisIndex + 1]]);
        boxesToReturn.append(newBox);

    return boxesToReturn;


