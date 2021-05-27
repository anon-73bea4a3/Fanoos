


-- NOTE below line can be replace by getting the records with fieldname 'namedPredicates' from the table
--     HelperTableForCollectedStatistics in ./collectingResults/scriptToCollectResults_initial.sql  
CREATE TEMPORARY TABLE numberTimesNamedPredicateUsedInStates (
	QAStateUUID string, 
	predicateUUID string, 
	num integer NOT NULL, 
	primary key(QAStateUUID, predicateUUID)
);
INSERT INTO numberTimesNamedPredicateUsedInStates --the complicated portion of the below checks basically are to ensure the predicate being dealt with is a named-predicate, not a whole conjunct, and not a box-itself predicate....
SELECT A.QAStateUUID, A.childUUID, count(*) FROM QAStateValues as A WHERE (A.fieldName = 'd:root' or A.fieldName = 'd:parent_child') AND (A.childUUID NOT LIKE "frozenset%") AND EXISTS (SELECT * FROM predicateInfo WHERE predicateUUID=childUUID)GROUP BY QAStateUUID, childUUID;



CREATE TEMPORARY TABLE consequetiveStatesAndResponces (firstQAStateUUID string NOT NULL, 
	                                           secondQAStateUUID string NOT NULL,
                                                   userFirstResponce string, -- may be NULL due to initial states...
                                                   userSecondResponce string NOT NULL, -- TODO: resolve difficulties here in cases where a computation errored-out or when the user responce is 'b'...
						   questionInstanceUUID string NOT NULL,
						   indexFirstState integer NOT NULL,
						   indexSecondState integer NOT NULL,
                                                   check( (userFirstResponce is not NULL) or (userSecondResponce is not NULL)),
						   check( (userFirstResponce IS NOT NULL) OR (indexFirstState == 0))
                                                   ); -- NOTE: possibly not a great idea to make this a temporary table <redacted> 
	
INSERT INTO consequetiveStatesAndResponces (
	firstQAStateUUID , 
	secondQAStateUUID, 
	userFirstResponce, 
	userSecondResponce,
        questionInstanceUUID,
	indexFirstState,
	indexSecondState
) 
SELECT stateTabA.QAStateUUID, 
       stateTabB.QAStateUUID, 
       stateTabA.userResponce , 
       stateTabB.userResponce, 
       stateTabB.questionInstanceUUID, 
       stateTabA.answerIndex, 
       stateTabB.answerIndex 
FROM
     questionInstance_QAState_relation as stateTabA ,
     questionInstance_QAState_relation as stateTabB
WHERE
    stateTabB.questionInstanceUUID = stateTabA.questionInstanceUUID AND 
    stateTabB.answerIndex = stateTabA.answerIndex + 1 
    AND stateTabB.userResponce IS NOT NULL -- might revise this later, but for now it seems reasonable to address / mitigate any unforeseen bugs elsewhere
;


CREATE TEMPORARY TABLE predicateCountsOverConsequetiveStatesWithFullInfo(
    predicateCountedForFirstStateOrSecond string NOT NULL,	
    predicateUUID string NOT NULL,  -- certainly not unique, so not a primary key...
    numFirst integer default 0,
    numSecond integer default 0,
    firstQAStateUUID string NOT NULL,
    secondQAStateUUID string NOT NULL,
    userFirstResponce string NOT NULL,
    userSecondResponce string NOT NULL,
    questionInstanceUUID string NOT NULL,
    indexFirstState integer NOT NULL,
    indexSecondState integer NOT NULL,
    check(numFirst >= 0),
    check(numSecond >= 0),
    check( numFirst >= 1 or numSecond >= 1),
    primary key(predicateCountedForFirstStateOrSecond, predicateUUID, questionInstanceUUID, indexFirstState)
);
INSERT INTO predicateCountsOverConsequetiveStatesWithFullInfo (
    predicateCountedForFirstStateOrSecond,
    predicateUUID, 
    numFirst, --- notice this line ; compare it to the line in the next query 
    firstQAStateUUID, 
    secondQAStateUUID, 
    userFirstResponce, 
    userSecondResponce,
    questionInstanceUUID,
    indexFirstState,
    indexSecondState )
SELECT 
        'count for first state',
        A.predicateUUID,
        A.num,
        B.firstQAStateUUID ,
        B.secondQAStateUUID,
        B.userFirstResponce,
        B.userSecondResponce,
        B.questionInstanceUUID,
        B.indexFirstState,
        B.indexSecondState    
FROM
numberTimesNamedPredicateUsedInStates AS A, 
consequetiveStatesAndResponces AS B
WHERE
B.firstQAStateUUID = A.QAStateUUID;

INSERT INTO predicateCountsOverConsequetiveStatesWithFullInfo (
    predicateCountedForFirstStateOrSecond,
    predicateUUID,
    numSecond, --- notice this line ; compare it to the line in the previous query 
    firstQAStateUUID,
    secondQAStateUUID,
    userFirstResponce,
    userSecondResponce,
    questionInstanceUUID,
    indexFirstState,
    indexSecondState )
SELECT
        'count for second state',
        A.predicateUUID,
        A.num,
        B.firstQAStateUUID ,
        B.secondQAStateUUID,
        B.userFirstResponce,
        B.userSecondResponce,
        B.questionInstanceUUID,
        B.indexFirstState,
        B.indexSecondState
FROM
numberTimesNamedPredicateUsedInStates AS A,
consequetiveStatesAndResponces AS B
WHERE
B.secondQAStateUUID = A.QAStateUUID AND
(B.indexFirstState > 0); -- the initial state has no description or user feedback, it is simply the root of a responce tree...



CREATE TEMPORARY TABLE predicateCountsAndResponces(
    predicateUUID string NOT NULL,  -- certainly not unique, so not a primary key...
    numFirst integer default 0,
    numSecond integer default 0,
    userFirstResponce string NOT NULL,
    userSecondResponce string NOT NULL,
    questionInstanceUUID string NOT NULL,
    indexFirstState integer NOT NULL,
    check(numFirst >= 0),
    check(numSecond >= 0),
    check( numFirst >= 1 or numSecond >= 1),
    primary key(predicateUUID, questionInstanceUUID, indexFirstState)
);
INSERT INTO predicateCountsAndResponces(
    predicateUUID,
    numFirst,
    numSecond,
    userFirstResponce,
    userSecondResponce, 
    questionInstanceUUID,
    indexFirstState
)
SELECT 
    predicateUUID,
    max(numFirst),
    max(numSecond),
    userFirstResponce,
    userSecondResponce,
    questionInstanceUUID,
    indexFirstState
FROM 
predicateCountsOverConsequetiveStatesWithFullInfo 
GROUP BY 
predicateUUID, questionInstanceUUID, indexFirstState;

DROP TABLE numberTimesNamedPredicateUsedInStates;
DROP TABLE consequetiveStatesAndResponces;
DROP TABLE predicateCountsOverConsequetiveStatesWithFullInfo;



