

import config;
_LOCALDEBUGFLAG = config.debugFlags.get_v_print_ForThisFile(__file__);
    

import numpy as np
from utils.contracts import *;

from boxesAndBoxOperations.getBox import isProperBox, getBox, getDimensionOfBox, getJointBox, getContainingBox, getRandomBox;

import uuid;

from utils.getGitCommitHash import gitCommitHashWhenThisCodeStartedRunning;
from utils.getStringTimeNow import *;

import re;

import struct;

import config;

def recordMetaDataForStart(thisUUID, dictMappingFileTypeToFileHandleToUse):
    requires(isinstance(thisUUID, str));
    requires(re.match("^[0-9a-f\-]+$", thisUUID) != None);
    requires(isinstance(dictMappingFileTypeToFileHandleToUse, dict));
    requires(list(dictMappingFileTypeToFileHandleToUse.keys()) == \
            ['boxes', 'metaData']);

    dictMappingFileTypeToFileHandleToUse["metaData"].write("UUID:" + thisUUID + "\n");
    dictMappingFileTypeToFileHandleToUse["metaData"].write("gitCommitHashWhenThisCodeStartedRunning:" + gitCommitHashWhenThisCodeStartedRunning + "\n");
    dictMappingFileTypeToFileHandleToUse["metaData"].write("time started running:" + getStringTimeNow() + "\n");
    dictMappingFileTypeToFileHandleToUse["metaData"].flush();
    return;

def recordMetaDataForFinish(dictMappingFileTypeToFileHandleToUse):
    requires(isinstance(dictMappingFileTypeToFileHandleToUse, dict));
    requires(list(dictMappingFileTypeToFileHandleToUse.keys()) == \
            ['boxes', 'metaData']);

    dictMappingFileTypeToFileHandleToUse["metaData"].write("time finished running:" + getStringTimeNow() + "\n");
    dictMappingFileTypeToFileHandleToUse["metaData"].flush();
    return;



def getFilesToSaveResultsIn(thisUUID, universeBox):
    requires(isinstance(thisUUID, str));
    requires(re.match("^[0-9a-f\-]+$", thisUUID) != None);
    requires(isProperBox(universeBox));

    #V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~VV~~V~V~V~VV~V~V~V~V~VV~V~V~V~V~V~V~V~V
    # Setting up files to write to
    #-------------------------------------------------------------------------
    # Below, CLA stands for CEGAR-Like Analysis
    basePath = "./tmp/CLA_";
    dictMappingFileTypeToFileHandleToUse = {\
        "boxes" : "",\
        "metaData" : "" \
        };
    for thisKey in dictMappingFileTypeToFileHandleToUse:
        dictMappingFileTypeToFileHandleToUse[thisKey] = \
            basePath + thisKey + "_" + thisUUID;
        if(thisKey  == "boxes"):
            dictMappingFileTypeToFileHandleToUse[thisKey] = dictMappingFileTypeToFileHandleToUse[thisKey] + ".bin";
            fh = open(dictMappingFileTypeToFileHandleToUse[thisKey], "wb");
        else:
            fh = open(dictMappingFileTypeToFileHandleToUse[thisKey], "w");
        dictMappingFileTypeToFileHandleToUse[thisKey] = fh; # ssh-rsa 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 abc@defg
    #^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^


    #V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~VV~~V~V~V~VV~V~V~V~V~VV~V~V~V~V~V~V~V~V
    # Writting important meta-data to set up files, etc.
    #-------------------------------------------------------------------------
    recordMetaDataForStart(thisUUID, dictMappingFileTypeToFileHandleToUse);
    dictMappingFileTypeToFileHandleToUse["metaData"].write("universeBox:" + str(universeBox).replace("\n", " ") + "\n");
    dictMappingFileTypeToFileHandleToUse["boxes"].write(struct.pack("i", getDimensionOfBox(universeBox)));
    #^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^


    for thisFh in dictMappingFileTypeToFileHandleToUse.values():
        thisFh.flush();

    ensures(isinstance(dictMappingFileTypeToFileHandleToUse, dict));
    ensures(list(dictMappingFileTypeToFileHandleToUse.keys()) == \
           ['boxes', 'metaData']);
    return dictMappingFileTypeToFileHandleToUse;



def closeFilesToSaveResultsIn(dictMappingFileTypeToFileHandleToUse):
    requires(isinstance(dictMappingFileTypeToFileHandleToUse, dict));
    requires(list(dictMappingFileTypeToFileHandleToUse.keys()) == \
            ['boxes', 'metaData']);
    recordMetaDataForFinish(dictMappingFileTypeToFileHandleToUse);
    for thisFH in dictMappingFileTypeToFileHandleToUse.values():
        thisFH.flush();
        thisFH.close();
    return;

from boxesAndBoxOperations.readAndWriteBoxes import writeBox;




class CEGARFileWrittingManager():

    def __init__(self, universeBox):
        requires(isProperBox(universeBox));
        self.uuid = str(uuid.uuid4());
        self.universeBox = universeBox;
        self.dictMappingFileTypeToFileHandleToUse = getFilesToSaveResultsIn(self.uuid, self.universeBox);
        self.writeBufferForBoxes = [];
        self.boxBufferSizeLimit = 1000;
        return;

    def closeFilesToSaveResultsIn(self):
        self._flushBoxBuffer();
        closeFilesToSaveResultsIn(self.dictMappingFileTypeToFileHandleToUse);
        return;

    def _flushBoxBuffer(self):
        for thisBoxAndMetaData in self.writeBufferForBoxes:
            writeBox(thisBoxAndMetaData[0], thisBoxAndMetaData[1], thisBoxAndMetaData[2]);
        for thisKey in self.dictMappingFileTypeToFileHandleToUse:
            self.dictMappingFileTypeToFileHandleToUse[thisKey].flush();
        self.writeBufferForBoxes = [];
        return;

    def writeBox(self, thisBox, thisBoxMetaData):
        requires(isProperBox(thisBox));
        requires(getDimensionOfBox(thisBox) == getDimensionOfBox(self.universeBox));
        requires(isinstance(thisBoxMetaData, list));
        requires(len(thisBoxMetaData) == 2);
        requires(isinstance(thisBoxMetaData[0], int));
        requires(isinstance(thisBoxMetaData[1], int));
        requires(thisBoxMetaData[0] >= 0);
        requires(thisBoxMetaData[1] >= 0);
        requires(thisBoxMetaData[0] <= 255);
        requires(thisBoxMetaData[1] <= 255);
        self.writeBufferForBoxes.append((self.dictMappingFileTypeToFileHandleToUse["boxes"], thisBox, thisBoxMetaData));
        if(len(self.writeBufferForBoxes) > self.boxBufferSizeLimit):
            self._flushBoxBuffer();
        return;

    def writeMetadata(self, tagValue, thisLine):
        requires(isinstance(tagValue, str));
        requires(len(tagValue) > 0);
        requires("\n" not in tagValue);
        requires(":" not in tagValue);
        requires(isinstance(thisLine, str));
        self.dictMappingFileTypeToFileHandleToUse["metaData"].write(\
            tagValue + ":" + thisLine.replace("\n", "<NEWLINE>") + "\n\n");
        self.dictMappingFileTypeToFileHandleToUse["metaData"].flush();
        return;


