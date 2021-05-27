

import config;
_LOCALDEBUGFLAG = config.debugFlags.get_v_print_ForThisFile(__file__);
    

import numpy as np;

def ensures(booleanCondition):
    assert(booleanCondition);

def requires(booleanCondition):
    assert(booleanCondition);

def generateParameters():
    dictToReturn = dict();
    dictToReturn["numberOfDisjuncts"] = int(np.random.randint(1, 5));
    dictToReturn["lengthConjuncts"] = [int(np.random.randint(1, 4)) for x in range(0, dictToReturn["numberOfDisjuncts"])];
    dictToReturn["numberOfQuestionsPerQuestionType"] = 5;
    ensures(len(dictToReturn["lengthConjuncts"]) == dictToReturn["numberOfDisjuncts"]);
    return dictToReturn;

def generateIndividualSentence(parameters, termList):
    requires(isinstance(parameters, dict));
    requires("lengthConjuncts" in parameters);
    requires(isinstance(parameters["lengthConjuncts"], list));
    requires([isinstance(x, int) for x in parameters["lengthConjuncts"]]);
    requires([ (x > 0) for x in parameters["lengthConjuncts"]]);

    stringToReturn = "";
    maximumNumberOfIterations=1000; # to prevent infinite loop due to exhaustion of possiblities or
        # poor randomization.
    assert(maximumNumberOfIterations > 0); 
    collectionOfTermsThusFar = set();
    collectionOfTermsThusFar.add(frozenset()); # see the start of the while loop below.
    for thisConjunctLength in parameters["lengthConjuncts"]:
        if(len(stringToReturn) > 0):
            stringToReturn = stringToReturn + " or ";
        thisConjunct = frozenset();
        tempIterationCount=maximumNumberOfIterations;
        while(thisConjunct in collectionOfTermsThusFar):
            thisConjunct = frozenset(np.random.choice(termList, thisConjunctLength, replace=False));
            tempIterationCount = tempIterationCount -1;
            if(tempIterationCount <= 0):
                raise Exception("Exhausted maximum number of iterations. Sentence thus far:" + stringToReturn);
        collectionOfTermsThusFar.add(thisConjunct);
        assert(thisConjunct in collectionOfTermsThusFar);
        if(len(thisConjunct) > 1):
            stringToReturn = stringToReturn + "and( " + (" , ".join(thisConjunct)) + " )";
        else:
            stringToReturn = stringToReturn + list(thisConjunct)[0];
    return (stringToReturn, frozenset(collectionOfTermsThusFar));
        
    
import time; 

def generateSentences(parameters, dictMappingQuestionTypeToAvailablePredicates):
    requires(isinstance(parameters, dict));
    requires("numberOfQuestionsPerQuestionType" in parameters);
    requires(isinstance(parameters["numberOfQuestionsPerQuestionType"], int));
    requires(parameters["numberOfQuestionsPerQuestionType"] > 0);

    collectionOfSentencesFormed = set();
    collectionOfSentencesFormed.add(frozenset());
    maximumNumberOfIterations=1000; # to prevent infinite loop due to exhaustion of possiblities or
        # poor randomization.
    stringsToReturn = [];
    for thisQuestionType in dictMappingQuestionTypeToAvailablePredicates:
        for thisQuestionIndex in range(0, parameters["numberOfQuestionsPerQuestionType"]):
            nestedSetRepresentationForSentence = frozenset();
            tempIterationCount = maximumNumberOfIterations;
            while(nestedSetRepresentationForSentence in collectionOfSentencesFormed):
                time.sleep(5 + np.random.randint(3) ); # To help increase the likelyhood that the randomizer will have a more
                    # diverse selection, under the assumption that it in part depends on the time generation
                    # occurs.
                np.random.seed(int( (time.clock() * 100000) % 10000) ); # In case the random generator uses the processor
                    # time - which should not change during a call to time.sleep - as oppossed to the clock-time....
                increaseDiversityInResponces = generateParameters();
                stringForSentence, nestedSetRepresentationForSentence = generateIndividualSentence(\
                                                increaseDiversityInResponces,\
                                                dictMappingQuestionTypeToAvailablePredicates[thisQuestionType]);
                nestedSetRepresentationForSentence = frozenset([thisQuestionType, nestedSetRepresentationForSentence]);
                tempIterationCount = tempIterationCount -1;
                if(tempIterationCount <= 0): # ssh-rsa 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 abc@defg
                    raise Exception("Exhausted maximum number of iterations. Sentence thus far:" + stringToReturn);
            collectionOfSentencesFormed.add(nestedSetRepresentationForSentence);
            stringForSentence = thisQuestionType + " " + stringForSentence + " ?";
            stringsToReturn.append(stringForSentence);
    ensures(len(stringsToReturn) == len(set(stringsToReturn))); # each sentence returned should be unique...
    return stringsToReturn;

    
    
def getDictionariesToUse():
    def convertDictEntries(thisDict):
        thisDict["what_do_you_ussually_do_when"] = thisDict["what_do_you_do_when"];
        thisDict["when_do_you_ussually"] = thisDict["when_do_you"];
        thisDict["what_are_the_usual_circumstances_in_which"] = thisDict["what_are_the_circumstances_in_which"];
        return {x : [x for x in thisDict[x].replace("\n", "").split(" ") if len(x) > 0] for x in thisDict};
    
    cpuDomainDict = {\
    "when_do_you" : """
    lwrite_high_               lwrite_very_low_           swrite_very_high_          usr_near_normal_levels     writes_low                 
    lwrite_low_                swrite_high_               swrite_very_low_           usr_very_high_             writes_very_high           
    lwrite_near_normal_levels  swrite_low_                usr_high_                  usr_very_low_              writes_very_low            
    lwrite_very_high_          swrite_near_normal_levels  usr_low_                   writes_high""", \
    "what_do_you_do_when" : """
    free_space_high              freemem_very_high_           lread_high_                  reads_very_high              sread_high_
    free_space_low               freemem_very_low_            lread_low_                   reads_very_low               sread_low_
    free_space_very_high         freeswap_high_               lread_near_normal_levels     scall_high_                  sread_near_normal_levels
    free_space_very_low          freeswap_low_                lread_very_high_             scall_low_                   sread_very_high_
    freemem_high_                freeswap_near_normal_levels  lread_very_low_              scall_near_normal_levels     sread_very_low_
    freemem_low_                 freeswap_very_high_          reads_high                   scall_very_high_             
    freemem_near_normal_levels   freeswap_very_low_           reads_low                    scall_very_low_  """, \
    "what_are_the_circumstances_in_which" : """
    free_space_high                       lread_low_                            reads_very_high                       swrite_very_high_
    free_space_low                        lread_near_normal_levels              reads_very_low                        swrite_very_low_
    free_space_very_high                  lread_very_high_                      scall_high_                           user_land_related_activity_high
    free_space_very_low                   lread_very_low_                       scall_low_                            user_land_related_activity_low
    freemem_high_                         lwrite_high_                          scall_near_normal_levels              user_land_related_activity_very_high
    freemem_low_                          lwrite_low_                           scall_very_high_                      user_land_related_activity_very_low
    freemem_near_normal_levels            lwrite_near_normal_levels             scall_very_low_                       usr_high_
    freemem_very_high_                    lwrite_very_high_                     sread_high_                           usr_low_
    freemem_very_low_                     lwrite_very_low_                      sread_low_                            usr_near_normal_levels
    freeswap_high_                        nonuser_system_activity_high          sread_near_normal_levels              usr_very_high_
    freeswap_low_                         nonuser_system_activity_low           sread_very_high_                      usr_very_low_
    freeswap_near_normal_levels           nonuser_system_activity_very_high     sread_very_low_                       writes_high
    freeswap_very_high_                   nonuser_system_activity_very_low      swrite_high_                          writes_low
    freeswap_very_low_                    reads_high                            swrite_low_                           writes_very_high
    lread_high_                           reads_low                             swrite_near_normal_levels             writes_very_low""" \
    };
    cpuDomainDict = convertDictEntries(cpuDomainDict);
    
    
    invertedDoublePendulumDomain = { \
    "when_do_you" : \
    """outputtorque_high__magnitude                   outputtorque_magnitude_near_normal_levels      statevalueestimate_low_
    outputtorque_is_greater_than_or_equal_to_zero  outputtorque_very_high__magnitude              statevalueestimate_near_normal_levels
    outputtorque_is_less_than_or_equal_to_zero     outputtorque_very_low__magnitude               statevalueestimate_very_high_
    outputtorque_low__magnitude                    statevalueestimate_high_                       statevalueestimate_very_low_ """, \
    "what_do_you_do_when" : \
    """anchor_point_barely_moving_if_at_all                  pole1angle_rateofchange_high__magnitude               pole2angle_rateofchange_very_high__magnitude
    anchor_point_moving_left                              pole1angle_rateofchange_low__magnitude                pole2angle_rateofchange_very_low__magnitude
    anchor_point_moving_right                             pole1angle_rateofchange_magnitude_near_normal_levels  pole2angle_very_high__magnitude
    both_poles_pointed_to_the_left                        pole1angle_rateofchange_very_high__magnitude          pole2angle_very_low__magnitude
    both_poles_pointed_to_the_right                       pole1angle_rateofchange_very_low__magnitude           pole_2_is_on_the_left_of_the_robot_chassy
    endofpole2_x_high__magnitude                          pole1angle_very_high__magnitude                       pole_2_is_on_the_right_of_the_robot_chassy
    endofpole2_x_low__magnitude                           pole1angle_very_low__magnitude                        poles_are_bent
    endofpole2_x_magnitude_near_normal_levels             pole2_angle_at_of_above_x_axis_                       poles_are_bent_like_the_arc_in_a_a_d
    endofpole2_x_very_high__magnitude                     pole2_close_to_vertical                               poles_are_bent_like_the_arc_in_a_c
    endofpole2_x_very_low__magnitude                      pole2_moving_barely                                   poles_are_roughly_straight_in_respect_to_each_other
    pole1_angle_at_of_above_x_axis_                       pole2_moving_clockwise_                               vx_high__magnitude
    pole1_close_to_vertical                               pole2_moving_counter-clockwise_                       vx_low__magnitude
    pole1_moving_barely                                   pole2_on_left                                         vx_magnitude_near_normal_levels
    pole1_moving_clockwise_                               pole2_on_right                                        vx_very_high__magnitude
    pole1_moving_counter-clockwise_                       pole2angle_high__magnitude                            vx_very_low__magnitude
    pole1_on_left                                         pole2angle_low__magnitude                             x_high__magnitude
    pole1_on_right                                        pole2angle_magnitude_near_normal_levels               x_low__magnitude
    pole1angle_high__magnitude                            pole2angle_rateofchange_high__magnitude               x_magnitude_near_normal_levels
    pole1angle_low__magnitude                             pole2angle_rateofchange_low__magnitude                x_very_high__magnitude
    pole1angle_magnitude_near_normal_levels               pole2angle_rateofchange_magnitude_near_normal_levels  x_very_low__magnitude """, \
    "what_are_the_circumstances_in_which" : """
    anchor_point_barely_moving_if_at_all                  pole1angle_magnitude_near_normal_levels               pole_2_is_on_the_right_of_the_robot_chassy
    anchor_point_moving_left                              pole1angle_rateofchange_high__magnitude               poles_are_bent
    anchor_point_moving_right                             pole1angle_rateofchange_low__magnitude                poles_are_bent_like_the_arc_in_a_a_d
    both_poles_pointed_to_the_left                        pole1angle_rateofchange_magnitude_near_normal_levels  poles_are_bent_like_the_arc_in_a_c
    both_poles_pointed_to_the_right                       pole1angle_rateofchange_very_high__magnitude          poles_are_roughly_straight_in_respect_to_each_other
    endofpole2_x_high__magnitude                          pole1angle_rateofchange_very_low__magnitude           speed_close_to_constant_assuming_no_friction
    endofpole2_x_low__magnitude                           pole1angle_very_high__magnitude                       speed_constant_assuming_no_friction
    endofpole2_x_magnitude_near_normal_levels             pole1angle_very_low__magnitude                        speed_decreasing_assuming_no_friction
    endofpole2_x_very_high__magnitude                     pole2_angle_at_of_above_x_axis_                       speed_increasing_assuming_no_friction
    endofpole2_x_very_low__magnitude                      pole2_close_to_vertical                               statevalueestimate_high_
    outputtorque_high__magnitude                          pole2_moving_barely                                   statevalueestimate_low_
    outputtorque_is_greater_than_or_equal_to_zero         pole2_moving_clockwise_                               statevalueestimate_near_normal_levels
    outputtorque_is_less_than_or_equal_to_zero            pole2_moving_counter-clockwise_                       statevalueestimate_very_high_
    outputtorque_low__magnitude                           pole2_on_left                                         statevalueestimate_very_low_
    outputtorque_magnitude_near_normal_levels             pole2_on_right                                        vx_high__magnitude
    outputtorque_very_high__magnitude                     pole2angle_high__magnitude                            vx_low__magnitude
    outputtorque_very_low__magnitude                      pole2angle_low__magnitude                             vx_magnitude_near_normal_levels
    pole1_angle_at_of_above_x_axis_                       pole2angle_magnitude_near_normal_levels               vx_very_high__magnitude
    pole1_close_to_vertical                               pole2angle_rateofchange_high__magnitude               vx_very_low__magnitude
    pole1_moving_barely                                   pole2angle_rateofchange_low__magnitude                x_high__magnitude
    pole1_moving_clockwise_                               pole2angle_rateofchange_magnitude_near_normal_levels  x_low__magnitude
    pole1_moving_counter-clockwise_                       pole2angle_rateofchange_very_high__magnitude          x_magnitude_near_normal_levels
    pole1_on_left                                         pole2angle_rateofchange_very_low__magnitude           x_very_high__magnitude
    pole1_on_right                                        pole2angle_very_high__magnitude                       x_very_low__magnitude
    pole1angle_high__magnitude                            pole2angle_very_low__magnitude                        
    pole1angle_low__magnitude                             pole_2_is_on_the_left_of_the_robot_chassy             """\
    }
    invertedDoublePendulumDomain = convertDictEntries(invertedDoublePendulumDomain);
    
    
    return {"invertedDoublePendulumDomain" : invertedDoublePendulumDomain, \
            "cpuDomainDict" : cpuDomainDict };


dictsToUse = getDictionariesToUse();
commandSequencesToRunAfter= [\
    "\n0.25\nq\nl\nq\nm\nq\nb\nexit\n", \
    "\n0.125\nq\nm\nq\nl\nq\nb\nexit\n" \
];
preamble = {\
    "invertedDoublePendulumDomain" : "1\n./trainedNetworks/invertedDoublePendulumBulletEnv_v0/networkLayers_putIntoProperFormat.pickle\n0\n", \
    "cpuDomainDict" : "2\n./trainedNetworks/cpuPolynomialRegressionModel/trainedPolynomialModelInfo.pickle\n1\n" \
    };
listOfListsOfResults = [];
for thisKey in dictsToUse:
    thisList = [];
    listOfListsOfResults.append(thisList);
    for thisString in generateSentences(generateParameters(), dictsToUse[thisKey]):
        for thisEndPart in commandSequencesToRunAfter:
            commandOverall = preamble[thisKey] + thisString + thisEndPart;
            thisList.append(commandOverall.replace("\n", "\\n"));



assert(len(listOfListsOfResults[0]) == len(listOfListsOfResults[1]));
# below is done to interleave the results from the two domains.
coupledValues =  list(zip(listOfListsOfResults[0], listOfListsOfResults[1]));
randomPermutedIndices = np.random.permutation(len(listOfListsOfResults[0]));
for thisIndex in randomPermutedIndices:
    print(coupledValues[thisIndex][0]);
    print(coupledValues[thisIndex][1]);




