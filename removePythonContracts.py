

# This is not intended to be a general solution - and it is easy to 
# see ways this could fail to work as intended (handling comments, 
# functions with names ending in the substring "assert", etc.) - but for the code
# as written and as reasonably written in the foreseeable future,
# this should be sufficient.

def removeContractsFromFile(fileName):    
    fh = open(fileName, "r");
    fileContent = fh.read();
    fh.close();
     
    contentToKeep = [];
    paranCount=0;
    justFinish=False;
    for thisChar in fileContent:
        if(paranCount > 0):
            paranCount= paranCount + (thisChar =="(") -  (thisChar ==")");
            #thisChar = "@";
            justFinish=True;
        else:
            if( (not justFinish) or (thisChar != ";")):
                contentToKeep.append(thisChar);
            justFinish = False;

        for thisContract in ["assert(", "ensures(", "requires("]:
            lenTC = len(thisContract);
            if("".join(contentToKeep[-lenTC:]) == thisContract):
                paranCount = 1;
                temp = [contentToKeep.pop() for x in range(0,lenTC)];
                temp.reverse();
                assert("".join(temp) == thisContract);
                justFinish=True;
                [contentToKeep.append(x) for x in "pass; "];
    
    fh =open(fileName, "w");
    fh.write("".join(contentToKeep));
    fh.flush();
    fh.close();
    return;


filesToClear = [\
    "./fanoos.py",
    "./handleDisplayOfCopyrightDuringInteractions.py",
    "./__init__.py",
    "./trainedNetworks/invertedDoublePendulumBulletEnv_v0/convertInvertedPendulumNetworkToAlternateFormat.py",
    "./trainedNetworks/cpuPolynomialRegressionModel/polynomialRegressionTrial.py",
    "./trainedNetworks/modelForTesting/formModelForTesting_twoDimInput_threeDimOutput_identityFunctionAndAddition.py",
    "./trainedNetworks/modelForTesting/formModelForTesting_oneDimInput_oneDimOutput_identityFunction.py",
    "./run_drawBoxes.py",
    "./UI/genericUIFunctions.py",
    "./UI/fanoosFrontend.py",
    "./UI/__init__.py",
    "./UI/commandLineAutocompleter.py",
    "./UI/cycleToRespondToUserQuestion.py",
    "./UI/captureTerminalOutput.py",
    "./domainsAndConditions/baseClassDomainInformation.py",
    "./domainsAndConditions/utilsForDefiningPredicates.py",
    "./domainsAndConditions/domainAndConditionsForInvertedDoublePendulum.py",
    "./domainsAndConditions/baseClassConditionsToSpecifyPredictsWith.py",
    "./domainsAndConditions/__init__.py",
    "./domainsAndConditions/domainAndConditionsFor_modelForTesting_oneDimInput_oneDimOutput.py",
    "./domainsAndConditions/domainAndConditionsFor_modelForTesting_twoDimInput_threeDimOutput.py",
    "./domainsAndConditions/domainAndConditionsForCircleFollowing.py",
    "./domainsAndConditions/domainAndConditionsForCPUUse.py",
    "./domainsAndConditions/classesDefiningQuestions.py",
    "./collectingResults/drawBoxes.py",
    "./propagateBoxThroughLearnedSystem/classesToPropogateBoxThroughModels.py",
    "./propagateBoxThroughLearnedSystem/__init__.py",
    "./propagateBoxThroughLearnedSystem/inputBoxToActivationFunctionOutputContainingInterval.py",
    "./propagateBoxThroughLearnedSystem/propogateValuesThroughRegression.py",
    "./propagateBoxThroughLearnedSystem/inputBoxToNetwork.py",
    "./statesAndOperatorsAndSelection/__init__.py",
    "./statesAndOperatorsAndSelection/chooseOperatorToApply.py",
    "./statesAndOperatorsAndSelection/descriptionState.py",
    "./statesAndOperatorsAndSelection/automaticOperatorSelection/operationSelectionManagers.py",
    "./statesAndOperatorsAndSelection/automaticOperatorSelection/__init__.py",
    "./statesAndOperatorsAndSelection/descriptionOperator.py",
    "./databaseInterface/databaseIOManager.py",
    "./databaseInterface/databaseValueTracker.py",
    "./boxesAndBoxOperations/mergeBoxes.py",
    "./boxesAndBoxOperations/__init__.py",
    "./boxesAndBoxOperations/getBox.py",
    "./boxesAndBoxOperations/readAndWriteBoxes.py",
    "./boxesAndBoxOperations/codeForGettingSamplesBetweenBoxes.py",
    "./boxesAndBoxOperations/CEGARFileWrittingManager.py",
    "./boxesAndBoxOperations/splitBox.py",
    "./experimentInfulstructure/randomlyGenerateQueriesToRun.py",
    "./utils/getGitCommitHash.py",
    "./utils/distributionStatics.py",
    "./utils/__init__.py",
    "./utils/getStringTimeNow.py",
    "./utils/quickResetZ3Solver.py",
    "./utils/getPathToThisDirectory.py",
    "./CEGARLikeAnalysis/refinementPathManager.py",
    "./CEGARLikeAnalysis/__init__.py",
    "./CEGARLikeAnalysis/labelsForBoxes.py",
    "./CEGARLikeAnalysis/CEGARLikeAnalysisMain.py",
    "./descriptionGeneration/__init__.py",
    "./descriptionGeneration/generateDescription.py",
    "./descriptionGeneration/removePredicatesImpliedByOthers.py",
    "./descriptionGeneration/draftCodeForMulitVariantConditionLearning.py",
    "./config/randomSeedSetting.py",
    "./config/defaultValues.py",
    "./config/__init__.py"];

for thisFile in filesToClear:
    removeContractsFromFile(thisFile);


