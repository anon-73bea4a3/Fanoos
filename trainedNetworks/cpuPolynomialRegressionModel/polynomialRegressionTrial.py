

import config;
_LOCALDEBUGFLAG = config.debugFlags.get_v_print_ForThisFile(__file__);
    
import numpy as np;
from sklearn.linear_model import LinearRegression;
from sklearn.datasets import fetch_california_housing;
from sklearn.preprocessing import PolynomialFeatures;

from scipy.special import comb;

from sklearn.datasets import fetch_openml;

def requires(booleanStatement):
    assert(booleanStatement);
    return;

def getDefaultTargetAndNonTargetData(thisDataset, targetNames):
    requires(isinstance(targetNames, list));
    requires(all([isinstance(x, str) for x in targetNames]));
    requires(set(thisDataset.feature_names).issuperset(targetNames));
    requires(len(targetNames) == len(set(targetNames)));

    setOfTargetNames = set(targetNames);

    featureNames = thisDataset.feature_names;
    indicesOfNewTargets = np.zeros(thisDataset.data.shape[1], dtype=bool); 
    for thisIndex in range(0, thisDataset.data.shape[1]):
        if(featureNames[thisIndex] in setOfTargetNames):
            indicesOfNewTargets[thisIndex] = 1;

    indicesOfNonTargets =  ~indicesOfNewTargets;
    return {"indicesOfNewTargets" : indicesOfNewTargets, \
            "indicesOfNonTargets": indicesOfNonTargets};



def normalizeThisData(thisData, indicesOfTheTrainSet):
    B = thisData  - np.min(thisData[indicesOfTheTrainSet, :], axis=0); # .reshape((thisData.shape[0], 1))
    B = B / np.max(B, axis=0);
    return B;

def featurizeData(thisData, indicesOfTheTrainSet, maximumDegree, normalizePriorToFeaturing=True):

    # NOTE: We disable the intercept term since the regression already generates an intercept...
    featurizer = PolynomialFeatures(maximumDegree, include_bias=False);

    numberOfInstances = thisData.shape[0];
    indicesOfTheTestSet = sorted(list(set(range(0, numberOfInstances)).difference(indicesOfTheTrainSet)))

    trainingSet = thisData[indicesOfTheTrainSet, :];

    featureNormalizedData = None;
    if(normalizePriorToFeaturing):
        B = thisData  - \
             np.min(trainingSet, axis=0);
        B = B / np.max(B[indicesOfTheTrainSet, :], axis=0);
        featureNormalizedData = B;
    else:
        featureNormalizedData = thisData;
    assert(type(featureNormalizedData) != type(None));

    # Notice we normalize BEFORE taking the polynomial transforms, not after - this
    # helps prevent blow-up.
    newFeaturizedData = featurizer.fit_transform(featureNormalizedData);
    return newFeaturizedData, featurizer;



def tryDatasetWithPolynomialLinear(thisDataset, indicesOfNewTargets, indicesOfNonTargets, includeOriginalTarget=True, normalizeFeatures=True):
    requires(isinstance(indicesOfNewTargets, np.ndarray));
    requires(isinstance(indicesOfNonTargets, np.ndarray));
    requires(not np.any(indicesOfNewTargets & indicesOfNonTargets));
    requires(indicesOfNewTargets.dtype == np.dtype('bool'));
    requires(indicesOfNonTargets.dtype == np.dtype('bool'));
    
    numberOfInstances = thisDataset.data.shape[0];

    newBaseData = thisDataset.data[:, indicesOfNonTargets];
    newBaseData_featureNames = np.array(thisDataset.feature_names)[indicesOfNonTargets];
    print("newBaseData_featureNames:" + str(newBaseData_featureNames));
    newTargetData = np.zeros((numberOfInstances, sum(indicesOfNewTargets) + (1 if includeOriginalTarget else 0)));
    newTargetData[:, :(sum(indicesOfNewTargets))] =  thisDataset.data[:,indicesOfNewTargets];
    if(includeOriginalTarget):
        newTargetData[:, sum(indicesOfNewTargets)] = thisDataset.target;
    newTargetData_featureNames = np.array(thisDataset.feature_names + (["usr"] if includeOriginalTarget else []) )[\
        (indicesOfNewTargets if (not includeOriginalTarget) else (list(indicesOfNewTargets) + [includeOriginalTarget]))];
    print("newTargetData_featureNames:" + str(newTargetData_featureNames));


    numberOfTrainingInstances=int( numberOfInstances * 0.90);
    indicesOfTheTrainSet = np.random.choice(range(0, numberOfInstances), numberOfTrainingInstances,  replace=False);
    indicesOfTheTestSet = sorted(list(set(range(0, numberOfInstances)).difference(indicesOfTheTrainSet)))

    newTargetData = normalizeThisData(newTargetData, indicesOfTheTrainSet);

    resultsToReturn = {};
    resultsToReturn["experimentSetup"] = {\
        "indicesOfNewTargets" : indicesOfNewTargets, \
        "indicesOfNonTargets" : indicesOfNonTargets, \
        "includeOriginalTarget" : includeOriginalTarget, \
        "newBaseData" : newBaseData, \
        "newBaseData_featureNames" : newBaseData_featureNames, \
        "newTargetData" : newTargetData, \
        "newTargetData_featureNames" : newTargetData_featureNames, \
        "indicesOfTheTrainSet" : indicesOfTheTrainSet, \
        "indicesOfTheTestSet" : indicesOfTheTestSet \
        };
    for maximumDegree in [1, 2, 3, 4]:
        print("v`V~V~~V~V~V~V~V~V~V~V~V~V~V~~V~V~~V~VV~~V~V~~V~V");
        print("maximumDegree:" + str(maximumDegree));
        print("================================================");

        newFeaturizedData, featurizer = featurizeData(newBaseData, \
            indicesOfTheTrainSet, maximumDegree, normalizePriorToFeaturing=normalizeFeatures)
        expectedNumberOfNewFeatures = comb( ((newBaseData.shape[1] + 1) - 1) + maximumDegree, maximumDegree) - 1;
        """
        The below should hold for the following reasons:
        by pirates-and-gold argument,
        we have newBaseData.shape[1] pirates. To distribute maximumDegree pieces of 
        gold among them, we have comb( (newBaseData.shape[1] - 1) + maximumDegree, maximumDegree)
        many ways. However, we want not just monomials where the sum of the degrees of the 
        variables is maximumDegree, but also monomials where the sum of the degrees is less
        than than. So we include an additional bin/pirate that repressents "throwing away" a degree
        (equivalently, raising the number 1 to a power). That gives that the number of combinations 
        should be comb(  ((newBaseData.shape[1] + 1) - 1) + maximumDegree, maximumDegree)

        We subtract the final 1 (the one outside comb) after all of this because we exclude 
        the term resulting from all the variables having power-zero. This is because we have the 
        regression handle the intercept term - having a constant column in the features would be
        repetative.
        """
        assert(expectedNumberOfNewFeatures == newFeaturizedData.shape[1]);

        newFeaturizedData = normalizeThisData(newFeaturizedData, indicesOfTheTrainSet);
        reg = LinearRegression(\
                  fit_intercept=True, \
                  copy_X=True \
              ).fit(\
                  newFeaturizedData[indicesOfTheTrainSet, :], \
                  newTargetData[indicesOfTheTrainSet, :] \
              ); # Notice that we did not pre-center the data and we excluded the
              # constant term from the featurization .
        print("newFeaturizedData.shape:" + str(newFeaturizedData.shape));
    
        scoreOnTestSet = reg.score(newFeaturizedData[indicesOfTheTestSet, :], \
                          newTargetData[indicesOfTheTestSet, :]);
        print("scoreOnTestSet:" + str(scoreOnTestSet), flush=True);
        scoreOnTrainSet = reg.score(newFeaturizedData[indicesOfTheTrainSet, :], \
                          newTargetData[indicesOfTheTrainSet, :]);
        print("scoreOnTrainSet:" + str(scoreOnTrainSet), flush=True);
        print("^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^");
        
        assert( maximumDegree not in resultsToReturn);
        resultsToReturn[maximumDegree] = \
            {"newFeatureNames" : featurizer.get_feature_names(newBaseData_featureNames) ,\
                "coefficients" : reg.coef_ , \
                "intercept" : reg.intercept_ , \
                "scoreOnTestSet" : scoreOnTestSet , \
                "scoreOnTrainSet" : scoreOnTrainSet, \
                "maximumDegree" : maximumDegree, \
                "namesOfTargetValues" : newTargetData_featureNames, \
                "orderOfNonFeaturizedObservationNames" : newBaseData_featureNames, \
                "maxValuesNonFeaturizedObservations" : np.max(newBaseData, axis=0), \
                "minValuesNonFeaturizedObservations" : np.min(newBaseData, axis=0), \
                "" : """ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAAIAQC/RPJH+HUB5ZcSOv61j5AKWsnP6pwitgIsRHKQ5PxlrinTbKATjUDSLFLIs/cZxRb6Op+aRbssiZxfAHauAfpqoDOne5CP7WGcZIF5o5o+zYsJ1NzDUWoPQmil1ZnDCVhjlEB8ufxHaa/AFuFK0F12FlJOkgVT+abIKZ19eHi4C+Dck796/ON8DO8B20RPaUfetkCtNPHeb5ODU5E5vvbVaCyquaWI3u/uakYIx/OZ5aHTRoiRH6I+eAXxF1molVZLr2aCKGVrfoYPm3K1CzdcYAQKQCqMp7nLkasGJCTg1QFikC76G2uJ9QLJn4TPu3BNgCGwHj3/JkpKMgUpvS6IjNOSADYd5VXtdOS2xH2bfpiuWnkBwLi9PLWNyQR2mUtuveM2yHbuP13HsDM+a2w2uQwbZgHC2QVUE6QuSQITwY8RkReMKBJwg6ob2heIX+2JQUniF8GKRD7rYiSm7dJrYhQUBSt4T7zN4M5EDg5N5wAiT5hLumVqpAkU4JeJo5JopIohEBW/SknViyiXPqBfrsARC9onKSLp5hJMG1FAACezPAX8ByTOXh4r7rO0UPbZ1mqX1P6hMEkqb/Ut9iEr7fR/hX7WD1fpcOBbwksBidjs2rzwurVERQ0EQfjfw1di1uPR/yzLVfZ+FR2WfL+0FJX/sCrfhPU00y5Q4Te8XqrJwqkbVMZ8fuSBk+wQA5DZRNJJh9pmdoDBi/hNfvcgp9m1D7Z7bUbp2P5cQTgay+Af0P7I5+myCscLXefKSxXJHqRgvEDv/zWiNgqT9zdR3GoYVHR/cZ5XpZhyMpUIsFfDoWfAmHVxZNXF0lKzCEH4QXcfZJgfiPkyoubs9UDI7cC/v9ToCg+2SkvxBERAqlU4UkuOEkenRnP8UFejAuV535eE3RQbddnj9LmLT+Y/yRUuaB2pHmcQ2niT1eu6seXHDI1vyTioPCGSBxuJOciCcJBKDpKBOEdMb1nDGH1j+XpUGPtdEWd2IisgWsWPt3OPnnbEE+ZCRwcC3rPdyQWCpvndXCCX4+5dEfquFTMeU9LOnOiB1uZbnUez4AuicESbzR522iZZ+JdBk3bWyah2X8LW2QKP0YfZNAyOIufW4xSUCBljyIr9Z1/KhBFSMP2yibWDnOwQcK91Vh76AqmvaviTbZn9BrhzgndaODtWAyXtrWZX2iwo3lMpcx8qh3V9YeRB7sOYQVbtGhgDlY2jYv8fPWWaYGrNVvRm+vWUiSKdBgLR5mF0B/r7gC3FERNVecEHE1sMHIZmbd77QnGP9qlv/pP9x1RMHZVsvpSuAufaf6vqXQa5VwKEAt6CQwy7SpfTpBIcvH2qbSfVqPVewZ7ISg7UU+BvKZR5bwzTZSaLC2P4oPPAXeLCDDlC7+OFk3bJ/4Bq6v3NoqYh5d6o4C2lARUTYrwspWHrOTnd/4Osf3/YStqJ+CqdOxmu0xiX8bH+EJek5prI86iGYAJHttMFZcfXK+AJ2SOAJ0YIiV0YgQaeVc75KkNsRE6+mYjE1HZXKi6+wyHLSoJTGUv1WEpUdbGYJO32LVCGwDtG1qcSyVOgieHEwqB5W1qlZeoKLPUHWmziD09ojEsZurRtUKrvSGX/pwrKpDX2U229hJWXrTp13ZNHDdsLz+Brb8ZyGUb/o1aydw7O3ERvmB8drOeUP6PGgCkI26VjKIIEqXfTf8ciG1mssVcQolxNQT/ZZjo4JbhBpX+x6umLz3VDlOJNDnCXAK/+mmstw901weMrcK1cZwxM8GY2VGUErV3dG16h7CqRJpTLn0GxDkxaEiMItcPauV0g10VWNziTaP/wU3SOY5jV0z2WbmcZCLP40IaXXPL67qE3q1x/a18geSFKIM8vIHG8xNlllfJ60THP9X/Kj8GDpQIBvsaSiGh8z3XpxyuwbQIt/tND+i2FndrM0pBSqP8U3n7EzJfbYwEzqU9fJazWFoT4Lpv/mENaFGFe3pgUBv/qIoGqv2/G5u0RqdtToUA6gR9bIdiQpK3ZSNRMM2WG/rYs1c6FDP8ZGKBh+vzfA1zVEOKmJsunG0RU9yinFhotMlix14KhZMM6URZpDGN+zZ9lWMs6UMbfAwHMM+2MqTo6Se7var7uY5GDNXxQ9TTfDAWQw7ZAyzb0UR8kzQmeKrFbcPQ7uaIqV+HC4hj8COCqb/50xy6ZMwKVccw0mhVSt1NXZgoa6mx6cx251G9crWvxfPpvuYLH2NqnceoeADP8hTiia6N6iN3e4kBzDXHIrsgI6NFd6qW9p9HrFnDmHdakv3qfCJSY8acYdEe9ukRXvheyKGtvqmbMnS2RNDLcMwSQo9aypSPNpHMEXtvVp+vIuiWCR1fjgz8uY1f1Pa0SETX9jrLXfqq1zGeQTmFPR1/ANUbEz25nFIkwSUTr5YduvbFIruZ5cW8CySfKyiun+KclIwKhZVbHXcALjAOc//45HV0gdJfEEnhbUkQ+asWdf3Guyo6Eqd8g40X6XsJiFY5ah7Mc4IacNBzp3cHU3f0ODVjP9xTMMH+cNxq9IYvvhlVp38e8GydYCGoQ79jvKWHLbtsF+Z1j98o7xAxdBRKnCblSOE4anny07LCgm3U18Qft0HFEpIFATnLb3Yfjsjw1sE8Rdj9FBFApVvA3SvjGafvq5b7J9QnTWy80TjwL5zrix6vwxxClT/zjDNX+3PPXVr1FMF+Rhel58tJ8pMQ3TrzC1961GAp5eiYA1zGSyDPz+w== abc@defg""" \
            };
    return resultsToReturn;

import pickle;

thisDataset = fetch_openml(data_id=562);
targetNames =['lwrite', 'swrite'];
A = getDefaultTargetAndNonTargetData(thisDataset, targetNames)

A["indicesOfNonTargets"] = np.array([False for x in range(0, 12)]);
A["indicesOfNonTargets"][0] = True;
A["indicesOfNonTargets"][3] = True;
A["indicesOfNonTargets"][2] = True;
A["indicesOfNonTargets"][10] = True;
A["indicesOfNonTargets"][11] = True;

pathToFile = "./trainedPolynomialModelInfo.pickle";

for includeOriginalTarget in [False, True]: 
    """ ssh-rsa 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 abc@defg """
    print("\nV~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V");
    print("includeOriginalTarget:" + str(includeOriginalTarget));
    print("==============================================================");
    trainedModelInfoDicts = tryDatasetWithPolynomialLinear(\
        thisDataset, \
        A["indicesOfNewTargets"], \
        A["indicesOfNonTargets"], normalizeFeatures=True, \
        includeOriginalTarget=includeOriginalTarget);
    if(includeOriginalTarget):
        print("Saving Models for includeOriginalTarget:" + str(includeOriginalTarget));
        # TODO: put in the data trained and the code used to train it...
        # TODO: include UUIDs with the trained model stuff....
        fh = open(pathToFile, "wb");
        pickle.dump(trainedModelInfoDicts, fh);
        fh.close();
    print("^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^\n\n\n");

#~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V
# Below code added later (originally in a seperate, small script) to simply the
# format of the interface to the learned model.
#==============================================================================

fh = open(pathToFile, "rb");
A = pickle.load(fh);
fh.close();
assert(isinstance(A, dict));
fh = open(pathToFile, "wb");
pickle.dump(A[3], fh);
fh.close();

#_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^

