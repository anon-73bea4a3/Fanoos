

import config;
_LOCALDEBUGFLAG = config.debugFlags.get_v_print_ForThisFile(__file__);
    

import pickle;
import numpy as np;
import sys;
from utils.contracts import *;

import config;

import uuid;

from databaseInterface.databaseValueTracker import ObjDatabaseValueTracker;
from databaseInterface.databaseIOManager import objDatabaseInterface, executeDatabaseCommandList;


from statesAndOperatorsAndSelection.descriptionOperator import *; 


class SelectorManagerBase():

    @staticmethod
    def setID():
        raise Exception("This class uses hard-coded UUIDs; the setID method is not necessary to envoke");
        return

    @staticmethod
    def getID():
        return "4f6a2f1d-23ec-4db8-8775-68d57759cfad";

    @staticmethod
    def getAllAvailableOperators():
        listOfAvailableOperators = [\
            Operator_IAL_7b16e7a5, \
            Operator_DAL_7b16e7a5, \
            Operator_HistoryExamination, \
            Operator_ManualPredicateReview, \
            Operator_AutoRevisePredicates_DAL_7b16e7a5, \
            Operator_AutoRevisePredicates_IAL_7b16e7a5 \
            ];
        return {x.getID() : x for x in listOfAvailableOperators};

    def _prepare(self):
        return;

    def prepareForSelectors(self): # TODO: this should probably be private but over-rideable by child classes...
        return;

    def prepareForWeigher(self): # TODO: this should probably be private but over-rideable by child classes..
        return;

    def __init__(self, domainInformation, loadedLearnedModel): # These two parameters should
        # be constant over the entire run....
        self._prepare();
        self.domainInformation = domainInformation;
        self.loadedLearnedModel = loadedLearnedModel;
        self.selectors = [];
        self.weigher = None;
        self.prepareForSelectors();
        self.prepareForWeigher();
        return;


    def getOperatorToUse(self, typeOfBoxesToGet, state, \
        objectForHistory, indexIntoQA, userResponce):
        raise NotImplementedError("Child classes must overwrite this.");
        return;


    def _cleanUpForSelectors(self):
        requires( (self.selectors is None) or isinstance(self.selectors, list));
        if(self.selectors is not None and len(self.selectors) > 0):
            for thisSelector in self.selectors:
                thisSelector.cleanUp();
        return;

    def _cleanUpForWeigher(self):
        if( self.weigher is not None ):
            self.weigher.cleanUp();
        return;

    def cleanUp(self):
        self._cleanUpForSelectors();
        self._cleanUpForWeigher();
        return;


class Manual_SelectorManager(SelectorManagerBase):

    @staticmethod
    def getID():
        return "1c612e8b-4545-4cc6-8c54-bb696caa0e48";

    def prepareForSelectors(self):
        raise Exception("Not Used in this Class.");
        return;

    def prepareForWeigher(self):
        raise Exception("Not Used in this Class.");
        return;

    def __init__(self, domainInformation, loadedLearnedModel): # These two parameters should
        # be constant over the entire run....
        self.domainInformation = domainInformation;
        self.loadedLearnedModel = loadedLearnedModel;
        self.selectors = None; # TODO: fill this in with selectors to come
        self.weigher = None;
        return;


    def getOperatorToUse(self, typeOfBoxesToGet, state, \
        objectForHistory, indexIntoQA, userResponce):
        dictMappingOptionsToOperatorUUIDs = {\
            "L" : Operator_DAL_7b16e7a5.getID(), \
            "M" : Operator_IAL_7b16e7a5.getID(), \
            "h" : Operator_HistoryExamination.getID(), \
            "u" : Operator_ManualPredicateReview.getID(), \
            "auto_u_L" : Operator_AutoRevisePredicates_DAL_7b16e7a5.getID(), \
            "auto_u_M" : Operator_AutoRevisePredicates_IAL_7b16e7a5.getID() \
            };
        dictMappingOperatorUUIDsToDescriptions = {\
            Operator_DAL_7b16e7a5.getID() : "less abstract", \
            Operator_IAL_7b16e7a5.getID() : "more abstract", \
            Operator_HistoryExamination.getID() : "history travel", \
            Operator_ManualPredicateReview.getID() : "manual predicate review", \
            Operator_AutoRevisePredicates_DAL_7b16e7a5.getID() : "auto predicate review: less abstract", \
            Operator_AutoRevisePredicates_IAL_7b16e7a5.getID() : "auto predicate review: more abstract" \
            };

        print("Note: responces are case-sensative");
        for thisOption in dictMappingOptionsToOperatorUUIDs:
                print("    " + thisOption + " - " + \
            dictMappingOperatorUUIDsToDescriptions[dictMappingOptionsToOperatorUUIDs[thisOption]]);
        print("------------------");

        thisLine = sys.stdin.readline();

        userResponceToRecord =  thisLine[:-1];# The -1 to remove the final newline...

        return self.getAllAvailableOperators()[\
            dictMappingOptionsToOperatorUUIDs[userResponceToRecord]]();        




class OriginalMethod_SelectorManager(SelectorManagerBase):
    """
    this function largely based on the code for class Manual_SelectorManager, 
    uuid 1c612e8b-4545-4cc6-8c54-bb696caa0e48
    """
 
    @staticmethod
    def getID():
        return "a6cf1bb2-bd1d-465a-9067-a2b8e2cc39de";

    def prepareForSelectors(self):
        raise Exception("Not Used in this Class.");
        return;

    def prepareForWeigher(self):
        raise Exception("Not Used in this Class.");
        return;

    def __init__(self, domainInformation, loadedLearnedModel): # These two parameters should
        # be constant over the entire run....
        self.domainInformation = domainInformation;
        self.loadedLearnedModel = loadedLearnedModel;
        self.selectors = None; # TODO: fill this in with selectors to come
        self.weigher = None;
        return;


    def getOperatorToUse(self, typeOfBoxesToGet, state, \
        objectForHistory, indexIntoQA, userResponce):
        dictMappingOptionsToOperatorUUIDs = {\
            "l" : Operator_DAL_7b16e7a5.getID(), \
            "m" : Operator_IAL_7b16e7a5.getID() \
            };

        return self.getAllAvailableOperators()[\
            dictMappingOptionsToOperatorUUIDs[userResponce]]();




