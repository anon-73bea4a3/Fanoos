

import config;
_LOCALDEBUGFLAG = config.debugFlags.get_v_print_ForThisFile(__file__);
    

from utils.contracts import *; 


class refinementPathInfo():
    """
    This class relies on a depth-first storage scheme for leaves having been used.

    Save:
    1 byte for: depth
    1 byte for:
        1 bit for the sat solver result about existance
        2 bits about the sat solver result for forall match (if the function is not provided, 
            then we mark it with the value 2)
        5 bits to indicate how the box was refined (bisection, trisection, etc., with a enough space to specify
            something more sophisticated if something along those lines is adopted later)

    At the start, when there are not previous results to load, this can simply always return inapplicable.
    """

    @staticmethod
    def _byteEncode(A, B, C):
        return (A & 1) | ( (B & 3) << 1 ) | ( (C & 31) << 3);

    @staticmethod
    def _byteDecode(b):
        return ( b & 1, \
                ( b >> 1) & 3,\
                ( b >> 3) & 31 );

    def __init__(self):
        self.byteList = bytearray();
        self.iteratorCounter = 0;
        self.forCheckPurposes_currentPath = [0];
        self.highlevelParametersForSplitting = dict(); # This is called "high-level"
            # in contrast to the 5-bits dedicated in every pair of bytes in 
            # self.byteList used to specify how any stochastic process invoked on a
            # per-split basis turned out.
        return;

    def __iter__(self):
        return self;

    @staticmethod
    def _noneOrSatForallR_to_int(thisValue):
        requires( thisValue in {True, False, None});
        if(thisValue is None):
            return 2;
        else:
            return int(thisValue)

    @staticmethod
    def _int_to_noneOrSatForallR(thisValue):
        requires( thisValue in {0,1,2});
        if(thisValue == 2):
            return None;
        else:
            return bool(thisValue);

    def append(self, depth, satSolverExistanceResult, noneOrSatSolverForallResult, refinementDone):
        requires( isinstance(depth, int));
        requires( depth >= 0 );
        requires( depth < 256);
        requires( isinstance(satSolverExistanceResult, bool));
        requires( noneOrSatSolverForallResult in {True, False, None});
        self.byteList.append(depth);
        self.byteList.append( \
            self._byteEncode(\
                int(satSolverExistanceResult), \
                self._noneOrSatForallR_to_int(noneOrSatSolverForallResult), \
                refinementDone)\
            );
        return;


    def __next__(self):
        headVal = self.head();
        self.advance();
        if( headVal is not None ):
           return headVal;
        else:
           raise StopIteration;

    def __rawGet(self, index):
        requires(isinstance(index,int));
        if( (index >= -len(self.byteList)) and
            (index < len(self.byteList)) ):
           val = self._byteDecode(self.byteList[index + 1]);
           valueToReturn =  (\
               int(self.byteList[index]), \
               bool(val[0]), \
               self._int_to_noneOrSatForallR(val[1]), \
               val[2]);
           return valueToReturn;
        else:
           return None;

    def get(self,index):
        requires(isinstance(index,0));
        requires(index >= 0);
        internalIndex = index * 2;
        assert(internalIndex >= index); # weak overflow check that should be
            # unnecessary in Python, but still good to do.
        return self.__rawGet(internalIndex);


    def end(self):
        return self.__rawGet(-2);


    def head(self):
        return self.__rawGet(self.iteratorCounter);

    def resetHead(self):
        # TODO: check invariants
        self.iteratorCounter = 0;
        self.forCheckPurposes_currentPath = [0];
        return;


    def getHead_depth(self):
        assert(self.iteratorCounter % 2 == 0); # this is an assert as oppossed
            # to a requires since it should be an internally guaranteed invariant,
            # not a requirement on user inputs.
        if(self.iteratorCounter < len(self.byteList) ):
           return self.byteList[self.iteratorCounter];
        else:
           return None;

    def getHead_satSolverExistanceResult(self):
        assert(self.iteratorCounter % 2 == 0); # this is an assert as oppossed
            # to a requires since it should be an internally guaranteed invariant,
            # not a requirement on user inputs.
        if(self.iteratorCounter < len(self.byteList) ):
           val = self._byteDecode(self.byteList[self.iteratorCounter + 1]);
           return bool(val[0]);
        else:
           return None;

    def getHead_noneOrSatSolverForallResult(self):
        assert(self.iteratorCounter % 2 == 0); # this is an assert as oppossed
            # to a requires since it should be an internally guaranteed invariant,
            # not a requirement on user inputs.
        if(self.iteratorCounter < len(self.byteList) ):
           val = self._byteDecode(self.byteList[self.iteratorCounter + 1]);
           return self._int_to_noneOrSatForallR(val[1]);
        else:
           return None;

    def getHead_refinementDone(self):
        assert(self.iteratorCounter % 2 == 0); # this is an assert as oppossed
            # to a requires since it should be an internally guaranteed invariant,
            # not a requirement on user inputs.
        if(self.iteratorCounter < len(self.byteList) ):
           val = self._byteDecode(self.byteList[self.iteratorCounter + 1]);
           return val[2];
        else:
           return None;


    def advance(self): 
        priorDepth = self.getHead_depth();

        self.iteratorCounter = self.iteratorCounter + 2;
        assert(self.iteratorCounter % 2 == 0); # this is an assert as oppossed
            # to a requires since it should be an internally guaranteed invariant,
            # not a requirement on user inputs.

        newDepth = self.getHead_depth();   

        assert(newDepth is None or len(self.forCheckPurposes_currentPath) >= newDepth); # Depth
            # should only ever increase one level at a time....
        if(newDepth is not None):
            assert(priorDepth is not None);

            if(newDepth == len(self.forCheckPurposes_currentPath)):
                self.forCheckPurposes_currentPath.append(-1);
                assert(len(self.forCheckPurposes_currentPath ) == newDepth + 1); # This should
                    # increase only one level at a time. Also, thankfully the practical uses cases and
                    # Python's special integers make me not worry about overflow on this line.
            if(priorDepth < newDepth):
                self.forCheckPurposes_currentPath[newDepth] = -1;

            self.forCheckPurposes_currentPath[newDepth] = \
                self.forCheckPurposes_currentPath[newDepth] + 1;

        return;


    def getCopyOfCurrentPath(self):
        if(self.getHead_depth() is None):
            return [];
        return self.forCheckPurposes_currentPath[:(self.getHead_depth() + 1)].copy();

    def headIsApplicable(self, currentDepth):
        requires(isinstance(currentDepth, int));
        requires(currentDepth >= 0);
        return ( self.getHead_depth() == currentDepth);

    def _goToNextDepthDecrease(self, startDepth):
        headVal = self.head();
        while(headVal is not None): # While the code used previously a for-loop for this,
            # that strategy turned out to be hard to do while keeping in sync with the 
            # path-name tracking ( a feature I added later). Thus, I have
            # changed the code - both this loop and the self.advance function - 
            # to further decouple value-returns and value-advancement to support
            # less error-prone path tracking.
            if( startDepth >= headVal[0]):
                assert(startDepth == headVal[0]);
                return headVal;
            self.advance();
            headVal = self.head();
        return None;

    def goToNextDepthDecreaseIfTooDeep(self, desiredDepth):
        currentDepth = self.getHead_depth();
        if( (currentDepth is None) or (currentDepth > desiredDepth ) ):
            nextVal = self._goToNextDepthDecrease(desiredDepth);
        return;


from databaseInterface.databaseValueTracker import ObjDatabaseValueTracker;




class refinementPathsManager():

    def reset(self):
        self.old = refinementPathInfo();
        self.new = refinementPathInfo();
        return;

    def __init__(self):
        self.old = refinementPathInfo();
        self.new = refinementPathInfo();
        return;

    def replaceOld(self):
        self.old = self.new;
        self.old.resetHead();
        self.new = refinementPathInfo();
        return;


# If one wants to perform additional checks to ensure the
# previous refinement results being loaded are still applicable, they
# might elect to use the below class (in the block comment) instead
# of the class refinementPathsManager for RefPathManager . However, while
# these additional checks are nice to do, they are largely unnecessary and
# would just cost extra - thought almost certainly negligible - resources.
"""
class refinementPathsManager_withAdditionalSafetyChecks():

    def reset(self):
        self.__old = refinementPathInfo();
        self.__new = refinementPathInfo();
        self.__uuidOfCurrentQuestionThatResultsApplyTo = \
            ObjDatabaseValueTracker.get_questionInstanceUUID();
        return;

    def __init__(self):
        self.__old = refinementPathInfo();
        self.__new = refinementPathInfo();
        self.__uuidOfCurrentQuestionThatResultsApplyTo = None;
        return;

    def __sameQuestionThanResultsStoredInternally(self):
        return (self.__uuidOfCurrentQuestionThatResultsApplyTo == \
                ObjDatabaseValueTracker.get_questionInstanceUUID() );

    @property
    def old(self):
        if(not self.__sameQuestionThanResultsStoredInternally()):
            raise Exception("Trying to access refinement results for " + \
                "different question");
        return self.__old;

    @property
    def new(self):
        if(not self.__sameQuestionThanResultsStoredInternally()):
            raise Exception("Trying to access refinement results for " + \
                "different question");
        return self.__new;


    def replaceOld(self):
        self.__old = self.__new;
        self.__old.resetHead();
        self.__new = refinementPathInfo();
        return;
"""



RefPathManager = refinementPathsManager();









