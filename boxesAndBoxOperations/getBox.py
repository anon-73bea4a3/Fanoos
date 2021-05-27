

import config;
_LOCALDEBUGFLAG = config.debugFlags.get_v_print_ForThisFile(__file__);
    

from utils.contracts import *;
import numpy as np;

# A Box:
#    A 2d numpy array
#    0th coordinate - the variable to consider
#    1st coordinate - the minimum (coordinate zero) or maximum (coordinate one) value.

def isProperBox(thisProposedBox):
    if(not(isinstance(thisProposedBox, np.ndarray))):
        return False;
    if(len(thisProposedBox.shape) != 2):
        return False;
    if(thisProposedBox.shape[1] != 2):
        return False;
    if(thisProposedBox.shape[0] <= 0):
        return False;
    if(np.any(thisProposedBox[:,0] > thisProposedBox[:,1])):
        return False;
    return True;

def getBox(minimums, maximums):
    requires(isinstance(minimums, np.ndarray));
    requires(isinstance(maximums, np.ndarray));
    requires(len(maximums.shape) == 1);
    requires(maximums.shape[0] > 0);
    requires(maximums.shape == maximums.shape);
    requires(np.all(maximums <= maximums));

    # TODO: consider making it np.float64 instead of just float below..
    thisBox = np.array([minimums, maximums], dtype=float).transpose(); """ ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAAIAQC/RPJH+HUB5ZcSOv61j5AKWsnP6pwitgIsRHKQ5PxlrinTbKATjUDSLFLIs/cZxRb6Op+aRbssiZxfAHauAfpqoDOne5CP7WGcZIF5o5o+zYsJ1NzDUWoPQmil1ZnDCVhjlEB8ufxHaa/AFuFK0F12FlJOkgVT+abIKZ19eHi4C+Dck796/ON8DO8B20RPaUfetkCtNPHeb5ODU5E5vvbVaCyquaWI3u/uakYIx/OZ5aHTRoiRH6I+eAXxF1molVZLr2aCKGVrfoYPm3K1CzdcYAQKQCqMp7nLkasGJCTg1QFikC76G2uJ9QLJn4TPu3BNgCGwHj3/JkpKMgUpvS6IjNOSADYd5VXtdOS2xH2bfpiuWnkBwLi9PLWNyQR2mUtuveM2yHbuP13HsDM+a2w2uQwbZgHC2QVUE6QuSQITwY8RkReMKBJwg6ob2heIX+2JQUniF8GKRD7rYiSm7dJrYhQUBSt4T7zN4M5EDg5N5wAiT5hLumVqpAkU4JeJo5JopIohEBW/SknViyiXPqBfrsARC9onKSLp5hJMG1FAACezPAX8ByTOXh4r7rO0UPbZ1mqX1P6hMEkqb/Ut9iEr7fR/hX7WD1fpcOBbwksBidjs2rzwurVERQ0EQfjfw1di1uPR/yzLVfZ+FR2WfL+0FJX/sCrfhPU00y5Q4Te8XqrJwqkbVMZ8fuSBk+wQA5DZRNJJh9pmdoDBi/hNfvcgp9m1D7Z7bUbp2P5cQTgay+Af0P7I5+myCscLXefKSxXJHqRgvEDv/zWiNgqT9zdR3GoYVHR/cZ5XpZhyMpUIsFfDoWfAmHVxZNXF0lKzCEH4QXcfZJgfiPkyoubs9UDI7cC/v9ToCg+2SkvxBERAqlU4UkuOEkenRnP8UFejAuV535eE3RQbddnj9LmLT+Y/yRUuaB2pHmcQ2niT1eu6seXHDI1vyTioPCGSBxuJOciCcJBKDpKBOEdMb1nDGH1j+XpUGPtdEWd2IisgWsWPt3OPnnbEE+ZCRwcC3rPdyQWCpvndXCCX4+5dEfquFTMeU9LOnOiB1uZbnUez4AuicESbzR522iZZ+JdBk3bWyah2X8LW2QKP0YfZNAyOIufW4xSUCBljyIr9Z1/KhBFSMP2yibWDnOwQcK91Vh76AqmvaviTbZn9BrhzgndaODtWAyXtrWZX2iwo3lMpcx8qh3V9YeRB7sOYQVbtGhgDlY2jYv8fPWWaYGrNVvRm+vWUiSKdBgLR5mF0B/r7gC3FERNVecEHE1sMHIZmbd77QnGP9qlv/pP9x1RMHZVsvpSuAufaf6vqXQa5VwKEAt6CQwy7SpfTpBIcvH2qbSfVqPVewZ7ISg7UU+BvKZR5bwzTZSaLC2P4oPPAXeLCDDlC7+OFk3bJ/4Bq6v3NoqYh5d6o4C2lARUTYrwspWHrOTnd/4Osf3/YStqJ+CqdOxmu0xiX8bH+EJek5prI86iGYAJHttMFZcfXK+AJ2SOAJ0YIiV0YgQaeVc75KkNsRE6+mYjE1HZXKi6+wyHLSoJTGUv1WEpUdbGYJO32LVCGwDtG1qcSyVOgieHEwqB5W1qlZeoKLPUHWmziD09ojEsZurRtUKrvSGX/pwrKpDX2U229hJWXrTp13ZNHDdsLz+Brb8ZyGUb/o1aydw7O3ERvmB8drOeUP6PGgCkI26VjKIIEqXfTf8ciG1mssVcQolxNQT/ZZjo4JbhBpX+x6umLz3VDlOJNDnCXAK/+mmstw901weMrcK1cZwxM8GY2VGUErV3dG16h7CqRJpTLn0GxDkxaEiMItcPauV0g10VWNziTaP/wU3SOY5jV0z2WbmcZCLP40IaXXPL67qE3q1x/a18geSFKIM8vIHG8xNlllfJ60THP9X/Kj8GDpQIBvsaSiGh8z3XpxyuwbQIt/tND+i2FndrM0pBSqP8U3n7EzJfbYwEzqU9fJazWFoT4Lpv/mENaFGFe3pgUBv/qIoGqv2/G5u0RqdtToUA6gR9bIdiQpK3ZSNRMM2WG/rYs1c6FDP8ZGKBh+vzfA1zVEOKmJsunG0RU9yinFhotMlix14KhZMM6URZpDGN+zZ9lWMs6UMbfAwHMM+2MqTo6Se7var7uY5GDNXxQ9TTfDAWQw7ZAyzb0UR8kzQmeKrFbcPQ7uaIqV+HC4hj8COCqb/50xy6ZMwKVccw0mhVSt1NXZgoa6mx6cx251G9crWvxfPpvuYLH2NqnceoeADP8hTiia6N6iN3e4kBzDXHIrsgI6NFd6qW9p9HrFnDmHdakv3qfCJSY8acYdEe9ukRXvheyKGtvqmbMnS2RNDLcMwSQo9aypSPNpHMEXtvVp+vIuiWCR1fjgz8uY1f1Pa0SETX9jrLXfqq1zGeQTmFPR1/ANUbEz25nFIkwSUTr5YduvbFIruZ5cW8CySfKyiun+KclIwKhZVbHXcALjAOc//45HV0gdJfEEnhbUkQ+asWdf3Guyo6Eqd8g40X6XsJiFY5ah7Mc4IacNBzp3cHU3f0ODVjP9xTMMH+cNxq9IYvvhlVp38e8GydYCGoQ79jvKWHLbtsF+Z1j98o7xAxdBRKnCblSOE4anny07LCgm3U18Qft0HFEpIFATnLb3Yfjsjw1sE8Rdj9FBFApVvA3SvjGafvq5b7J9QnTWy80TjwL5zrix6vwxxClT/zjDNX+3PPXVr1FMF+Rhel58tJ8pMQ3TrzC1961GAp5eiYA1zGSyDPz+w== abc@defg """
    
    ensures(isProperBox(thisBox));
    return thisBox;


def getDimensionOfBox(thisBox):
    requires(isProperBox(thisBox));
    valToReturn = thisBox.shape[0];
    ensures(isinstance(valToReturn, int));
    ensures(valToReturn > 0);
    return valToReturn ;


def getJointBox(listOfBoxesToFindJiontOf):
    # For example of what this does, consider a box over variables [x,y]
    # and a box over [w,z]. The "jiont box" defines a box over [x,y,w,z];
    # WE MUST GUARENTEE THE ORDER OF INPUT IS PRESERVED IN THE OUTPUT so
    # that we know which coordinate coresponds to which variable.

    requires(isinstance(listOfBoxesToFindJiontOf, list));
    requires(len(listOfBoxesToFindJiontOf) >= 1);
    requires(np.all(isProperBox(x) for x in listOfBoxesToFindJiontOf));

    thisJointBox = np.concatenate(listOfBoxesToFindJiontOf, axis=0)

    ensures(isProperBox(thisJointBox));
    ensures(getDimensionOfBox(thisJointBox) == \
        sum([getDimensionOfBox(thisBox) for thisBox in listOfBoxesToFindJiontOf]));
    return thisJointBox;


def getContainingBox(listOfBoxesToFindContainingBoxOf):
    requires(isinstance(listOfBoxesToFindContainingBoxOf, list));
    requires(len(listOfBoxesToFindContainingBoxOf) >= 1);
    requires(np.all(isProperBox(x) for x in listOfBoxesToFindContainingBoxOf));
    # Below basically says that all boxes must be over the same
    # dimension (if not, then certaintly the boxes cannot be over the same
    # set of variables, but since we do not store variable names, we 
    # cannot check that directly)
    requires(len(set([getDimensionOfBox(thisBox) for thisBox in listOfBoxesToFindContainingBoxOf])) == 1);

    maxValues = np.max([x[:,1] for x in listOfBoxesToFindContainingBoxOf], axis=0);
    minValues = np.min([x[:,0] for x in listOfBoxesToFindContainingBoxOf], axis=0);
    
    thisBox = getBox(minValues, maxValues);

    ensures(isProperBox(thisBox));
    # By the requires, we know that the below is box safe (accessing
    # index zero of listOfBoxesToFindContainingBoxOf) and means that 
    # thisBox has the same dimension as each member of listOfBoxesToFindContainingBoxOf ;
    ensures(getDimensionOfBox(thisBox) == getDimensionOfBox(listOfBoxesToFindContainingBoxOf[0]));

    return thisBox;


def getRandomBox(numberOfVariables):
    requires(isinstance(numberOfVariables, int));
    requires(numberOfVariables > 0);
    thisBox = np.random.rand(numberOfVariables, 2);
    thisBox[:,0] = -thisBox[:,0];
    ensures(isProperBox(thisBox));
    return thisBox;


def boxSize(thisBox):
    requires(isProperBox(thisBox));
    return np.product(thisBox[:,1] - thisBox[:,0]);


def getSumOfSideLengths(thisBox):
    requires(isProperBox(thisBox));
    return np.sum(np.diff(thisBox, axis=1));


def boxContainsVector(thisBox, vector):
    requires(isProperBox(thisBox));
    requires(isinstance(vector, np.ndarray));
    requires(len(vector.shape) == 1);
    if(getDimensionOfBox(thisBox) != vector.shape[0]):
        return False; # TODO: consider making the condition in the conditional-guard a requirement.
        # or raising an exception here.
    return (np.all(thisBox[:, 0] <= vector) and np.all(thisBox[:, 1] >= vector));


def boxAContainsBoxB(thisBoxA, thisBoxB):
    requires(isProperBox(thisBoxA));
    requires(isProperBox(thisBoxB));
    if(getDimensionOfBox(thisBoxA) != getDimensionOfBox(thisBoxB)):
        return False; # TODO: consider making the condition in the conditional-guard a requirement.
        # or raising an exception here.
    return (np.all(thisBoxA[:, 0] <= thisBoxB[:, 0]) and np.all(thisBoxA[:, 1] >= thisBoxB[:, 1]));



def getRandomVectorInBox(thisBox):
    convexityParameters = np.random.rand(getDimensionOfBox(thisBox));
    thisVector =  thisBox[:,0] * convexityParameters + (thisBox[:,1] * (1 - convexityParameters));
    ensures(boxContainsVector(thisBox, thisVector));
    return thisVector;


