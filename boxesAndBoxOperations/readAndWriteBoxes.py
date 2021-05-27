

import config;
_LOCALDEBUGFLAG = config.debugFlags.get_v_print_ForThisFile(__file__);
    

from utils.contracts import *;
from boxesAndBoxOperations.getBox import getBox, getRandomBox, isProperBox, getDimensionOfBox; 
import struct;
import numpy as np;

def writeBox(fileHandle, thisBox, metaData):
    requires(isProperBox(thisBox));
    requires(isinstance(metaData, list));
    requires(len(metaData) == 2);
    requires(isinstance(metaData[0], int));
    requires(isinstance(metaData[1], int));
    requires(metaData[0] >= 0);
    requires(metaData[1] >= 0);
    requires(metaData[0] <= 255);
    requires(metaData[1] <= 255);

    # Below we write out the metadata
    for thisMetaDataInt in metaData:
        fileHandle.write(struct.pack( "B", thisMetaDataInt));
    
    numberOfBytesThatAFloatHasOnThisSystem = 4; # makes assumptions
        # about the system running this code, unless the library
        # in question standardized it....

    numberOfDimensions = getDimensionOfBox(thisBox);

    boundIndex = 0;
    while(boundIndex < 2):

        variableIndex = 0;
        while(variableIndex < numberOfDimensions):
 
            valueToWriteOut = thisBox[variableIndex, boundIndex];
            assert(isinstance(valueToWriteOut, float));
            numberOfBytesWritten = fileHandle.write(struct.pack( "f", valueToWriteOut));
            assert(numberOfBytesWritten == numberOfBytesThatAFloatHasOnThisSystem);

            assert(variableIndex < variableIndex + 1); # weak overflow check... should  not 
               # be necessary in python, but always good practice to include.
            variableIndex = variableIndex + 1;

        assert(boundIndex in {0, 1});
        boundIndex = boundIndex + 1

    return;


def readBoxFromFile(fhToRead, dimensionOfBox, numberOfBytesThatAFloatHasOnThisSystem):
    requires(isinstance(dimensionOfBox, int));
    requires(dimensionOfBox > 0);

    boxToReturn = np.zeros((dimensionOfBox, 2));

    valueToUnpack = [fhToRead.read(1), fhToRead.read(1)]; # reading this way might
        # defeat many of the purposes of trying to implement a read buffer on top 
        # of the output of this function...
    if(len(valueToUnpack[0]) == 0):
        return None;
    metaData = [struct.unpack( "B", valueToUnpack[x])[0] for x in [0,1]]; # somewhat hacky way to write this.....

    boundIndex = 0; # ssh-rsa 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 abc@defg
    while(boundIndex < 2):

        variableIndex = 0;
        while(variableIndex < dimensionOfBox):

            valueToUnpack = fhToRead.read(numberOfBytesThatAFloatHasOnThisSystem);
            if(len(valueToUnpack) == 0):
                assert(boundIndex == 0 and variableIndex == 0); # in other words, not just 
                    # part of the way through reading a box.
                return None;
            unpackedValue = struct.unpack( "f", valueToUnpack)[0];
            assert(isinstance(unpackedValue, float));
            assert(not np.isnan(unpackedValue));

            boxToReturn[variableIndex , boundIndex] = unpackedValue;

            assert(variableIndex < variableIndex + 1); # weak overflow check... should  not 
               # be necessary in python, but always good practice to include.
            variableIndex = variableIndex + 1;

        assert(boundIndex in {0, 1});
        boundIndex = boundIndex + 1
    
    ensures(isProperBox(boxToReturn));
    return (boxToReturn, metaData);

def readBoxes(fhToRead):

    numberOfBytesThatAStructIntHasOnThisSystem = 4;
    numberOfBytesThatAFloatHasOnThisSystem = 4; # makes assumptions
        # about the system running this code, unless the library
        # in question standardized it....

    contentOfFile = fhToRead.read(numberOfBytesThatAStructIntHasOnThisSystem);
    dimensionOfBoxes = struct.unpack("i", contentOfFile)[0];
    assert(isinstance(dimensionOfBoxes, int));
    assert(dimensionOfBoxes > 0);

    numberOfFloatsNeededToDefineABox = 2 * dimensionOfBoxes; # one set of dimensionOfBoxes
        # many floats to define the lower bound, one set of dimensionOfBoxes to define the
        # upper bound.
    numberOfBytesPerBox = numberOfBytesThatAFloatHasOnThisSystem * numberOfFloatsNeededToDefineABox;

    listOfBoxesToReturn = [];
    
    boxIndex = 0;
    while(True):
        thisPotentialBox = readBoxFromFile(fhToRead,dimensionOfBoxes,\
            numberOfBytesThatAFloatHasOnThisSystem);
        if(not isinstance(thisPotentialBox, type(None))):
            listOfBoxesToReturn.append(thisPotentialBox);
        else:
            break;

        assert(boxIndex < boxIndex + 1); # weak overflow check... should  not 
            # be necessary in python, but always good practice to include.
        boxIndex = boxIndex + 1;
    assert(len(listOfBoxesToReturn) == boxIndex);
    # assert(boxIndex == numberOfBoxes);  

    return listOfBoxesToReturn;


