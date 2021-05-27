

import config;
_LOCALDEBUGFLAG = config.debugFlags.get_v_print_ForThisFile(__file__);
    

import numpy as np;
from sklearn.linear_model import LinearRegression;

from scipy.special import comb;

from sklearn.datasets import fetch_openml;

def requires(booleanStatement):
    assert(booleanStatement);
    return;

def getDefaultTargetAndNonTargetData(valueNames, targetNames):
    requires(isinstance(targetNames, list));
    requires(all([isinstance(x, str) for x in targetNames]));
    requires(set(valueNames).issuperset(targetNames));
    requires(len(targetNames) == len(set(targetNames)));

    setOfTargetNames = set(targetNames);

    indicesOfNewTargets = np.zeros(len(valueNames), dtype=bool); 
    for thisIndex in range(0, len(valueNames)):
        if(valueNames[thisIndex] in setOfTargetNames):
            indicesOfNewTargets[thisIndex] = 1;

    indicesOfNonTargets =  ~indicesOfNewTargets;
    return {"indicesOfNewTargets" : indicesOfNewTargets, \
            "indicesOfNonTargets": indicesOfNonTargets};



def normalizeThisData(thisData, indicesOfTheTrainSet):
    B = thisData  - np.min(thisData[indicesOfTheTrainSet, :], axis=0);
    B = B / np.max(B, axis=0);
    return B;


def tryDatasetWithPolynomialLinear(indicesOfNewTargets, indicesOfNonTargets):
    requires(isinstance(indicesOfNewTargets, np.ndarray));
    requires(isinstance(indicesOfNonTargets, np.ndarray));
    requires(not np.any(indicesOfNewTargets & indicesOfNonTargets));
    requires(indicesOfNewTargets.dtype == np.dtype('bool'));
    requires(indicesOfNonTargets.dtype == np.dtype('bool'));
      
    newFeatureNames = ["in_x"] ;
    newTargetData_featureNames = ["out_y"];
    newBaseData_featureNames = newFeatureNames;    

    resultsToReturn = \
        {"newFeatureNames" : newFeatureNames ,\
            "coefficients" : np.array([[1.00]]) , \
            "intercept" : np.array([[0.0]]) , \
            "namesOfTargetValues" : newTargetData_featureNames, \
            "orderOfNonFeaturizedObservationNames" : newBaseData_featureNames \
        };
    return resultsToReturn;



import pickle;
valueNames = ["in_x", "out_y"];
targetNames =['out_y']

A = getDefaultTargetAndNonTargetData(valueNames, targetNames);


trainedModelInfoDicts = tryDatasetWithPolynomialLinear(\
    A["indicesOfNewTargets"], \
    A["indicesOfNonTargets"] );


# TODO: in general, for models stored or prepared, for the sake of record-keeping
#     and future error checking, put in the data trained and the code used to train it...
# TODO: include UUIDs with the trained model material....
fh = open("./modelForTesting_oneDimInput_oneDimOutput_identityFunction.pickle", "wb");
pickle.dump(trainedModelInfoDicts, fh);
fh.close();



