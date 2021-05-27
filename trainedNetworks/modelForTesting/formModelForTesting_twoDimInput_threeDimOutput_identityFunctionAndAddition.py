

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
   
    newFeatureNames = ["in_x", "in_y"] ;
    newTargetData_featureNames = ["out_u", "out_v", "out_w"];
    newBaseData_featureNames = newFeatureNames;    


    """
note: the layout of coefficients is:
    np.array( [
        [<coefficients for first output variable>],
        [<coefficients for second output variable>],
        .
        . 
        .
        [<coefficients for nth output variable>],
        ]);

example: 

     input box: [[0. 1.]
                 [0. 1.]]
 
     output: [[   3.5        6.105  ]
              [-100.2      -98.99999]]
    """



    resultsToReturn = \
        {"newFeatureNames" : newFeatureNames ,\
            "coefficients" : np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]]) , \
            "intercept" : np.array([0.0, 0.0, -1.0]) , \
            "namesOfTargetValues" : newTargetData_featureNames, \
            "orderOfNonFeaturizedObservationNames" : newBaseData_featureNames \
        };
    return resultsToReturn;



import pickle;
valueNames = ["in_x", "in_y", "out_u", "out_v", "out_w"];
targetNames =["out_u", "out_v", "out_w"]

A = getDefaultTargetAndNonTargetData(valueNames, targetNames);


trainedModelInfoDicts = tryDatasetWithPolynomialLinear(\
    A["indicesOfNewTargets"], \
    A["indicesOfNonTargets"] );

# TODO: see the todos at the end of the code for preparing the one 
#     dimensional identity function...
fh = open("./modelForTesting_twoDimInput_threeDimOutput_identityFunctionAndAddition.pickle", "wb");
pickle.dump(trainedModelInfoDicts, fh);
fh.close();



