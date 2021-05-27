


-- NOTE: We do not delete older versioning information so we know that a database has been migrated
--     from an older version.
CREATE TABLE IF NOT EXISTS dataBaseInfo (dateCreated string, versionNumber float, primary key(dateCreated, versionNumber));
INSERT OR IGNORE INTO dataBaseInfo (dateCreated, versionNumber) VALUES ('day22 month3 year2021', 'release.1');


-- the below table could be expanded to include other metadata....
CREATE TABLE IF NOT EXISTS sessionInfo (
    sessionUUID string primary key, 
    dateAndTimeStarted datetime default current_timestamp NOT NULL,
    dateAndTimeFinished datetime,
    userUUID string, -- may be NULL
    domainUUID string NOT NULL,
    pathToSystemAnalyzed string NOT NULL, 
    gitCommitHash string NOT NULL,
    randomSeeds blob NOT NULL 
);

-- below table is expandable to include other metadata
CREATE TABLE IF NOT EXISTS users (
    userUUID string
);


CREATE TABLE IF NOT EXISTS session_questionInstance_relation(
    sessionUUID string NOT NULL,
    questionInstanceUUID string NOT NULL,
    primary key (sessionUUID, questionInstanceUUID)
);

-- below table could be expanded to include other metadata.
CREATE TABLE IF NOT EXISTS questionInstanceInfo(
    questionInstanceUUID string primary key,
    questionInstanceType string default 'MISSING' NOT NULL , -- have to add the 'MISSING' value to try to make this
        -- compatable with previous versions of the database
    questionInstanceContentTextUncleaned blob default 'MISSING' NOT NULL ,
    dateAndTimeStarted datetime default current_timestamp NOT NULL,
    dateAndTimeFinished datetime
);


-- Note that the same QAStateUUID may appear MULTIPLE TIMES for the same question,
-- If nothing else than because of the history travel operator....
CREATE TABLE IF NOT EXISTS questionInstance_QAState_relation(
    questionInstanceUUID string NOT NULL,
    answerIndex integer NOT NULL,
    QAStateUUID string NOT NULL,
    dateAndTimeAnswerShown datetime,
    dateAndTimeUserResponded datetime, /*
ssh-rsa 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 abc@defg */
    userResponce text,
    primary key (questionInstanceUUID, answerIndex),
    check( ( (userResponce is NULL) and (dateAndTimeUserResponded is NULL)) or
           ( (userResponce is not NULL) and (dateAndTimeUserResponded is not NULL)) )
);

-- startingAnswer ===(operator)===> finalAnswer . Below, we use the index for the starting answer...
-- Note that the same QAOperatorUUID may appear MULTIPLE TIMES for the same question
CREATE TABLE IF NOT EXISTS questionInstance_QAOperator_relation(
    questionInstanceUUID string NOT NULL,
    startingAnswerIndex integer NOT NULL,
    QAOperatorUUID string NOT NULL,
    dateAndTimeComputationStarted datetime,
    dateAndTimeComputationFinished datetime,
    primary key (questionInstanceUUID, startingAnswerIndex)
);

-- other information may be present below...
CREATE TABLE IF NOT EXISTS QAStateInfo(
    QAStateUUID primary key
);




-- Below, in general, the same QAState may appear multiple times, including with the same fieldName string...
CREATE TABLE IF NOT EXISTS QAStateValues(
    QAStateUUID string NOT NULL,
    fieldName string NOT NULL,
    parentUUID string,
    childUUID string,
    fieldValue blob 
);


CREATE TABLE IF NOT EXISTS QAOperatorValues(
    questionInstanceUUID string NOT NULL,
    QAOperatorUUID NOT NULL,
    startingAnswerIndex integer NOT NULL,
    fieldName string NOT NULL,
    fieldValue blob,
    check( startingAnswerIndex >= 0)
);


-- below can include other metadata....
CREATE TABLE IF NOT EXISTS domainInfo(
    domainUUID string primary key,
    typeString string NOT NULL
);

-- each predicate should only be listed under one domainUUID, and 
-- each predicate should only have to appear once under a domain UUID, thus
-- it makes sense for the predicates to be primary keys...
CREATE TABLE IF NOT EXISTS domain_predicate_relation(
    domainUUID string NOT NULL,
    predicateUUID string primary key,
    check( predicateUUID NOT LIKE "%frozenset%")
);


-- below can include other metadata....
CREATE TABLE IF NOT EXISTS predicateInfo(
    predicateUUID string primary key,
    stringName string NOT NULL, -- ideally this would be unique across the entire table...
    typeString string NOT NULL, -- ideally this would be unique across the entire table, but updates might have to be made at some point....
    check( predicateUUID NOT LIKE "%frozenset%")
);



-- each predicate may have multiple labels, 
-- each label may be applied to multiple predicates,
-- but if something is listed in this table, it should
-- at least have both fields present
CREATE TABLE IF NOT EXISTS predicate_label_relation(
     predicateUUID string NOT NULL,
     labelUUID string NOT NULL,
     primary key(predicateUUID, labelUUID),
     check( predicateUUID NOT LIKE "%frozenset%")
);

-- TODO: check DAG constraints in the labelings provided...
-- NOTE: PARENTS ARE CONSIDERED MORE ABSTRACT THAN CHILDREN....
CREATE TABLE IF NOT EXISTS labelDAG(
    parentLabelUUID string NOT NULL,
    childLabelUUID  string NOT NULL,
    primary key(parentLabelUUID, childLabelUUID),
    check( parentLabelUUID NOT LIKE "%frozenset%"),
    check( childLabelUUID NOT LIKE "%frozenset%")
);


CREATE TABLE IF NOT EXISTS terminalOutput(
    sessionUUID string NOT NULL,
    orderIndex integer NOT NULL,
    dateAndTimeInput datetime default current_timestamp NOT NULL,
    channelName string NOT NULL,
    valueOnChannel  blob NOT NULL,
    primary key(sessionUUID, orderIndex),
    check( orderIndex >= 0)
);




--V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V
-- Indices useful for when collecting and analyzing statistics
---------------------------------------------------------------------------------
CREATE INDEX IF NOT EXISTS "q_a_questionInstance_QAState_relation" ON questionInstance_QAState_relation (questionInstanceUUID , answerIndex);
CREATE INDEX IF NOT EXISTS "q_a_Q_questionInstance_QAState_relation" ON questionInstance_QAState_relation (questionInstanceUUID , answerIndex , QAStateUUID);
--
CREATE INDEX IF NOT EXISTS "Q_f_c_QAStateValues" ON QAStateValues (QAStateUUID,fieldName,childUUID) WHERE childUUID IS NOT NULL;
CREATE INDEX IF NOT EXISTS "Q_f_QAStateValues" ON QAStateValues (QAStateUUID,fieldName);
CREATE INDEX IF NOT EXISTS "Q_c_QAStateValues" ON QAStateValues (QAStateUUID,childUUID) WHERE childUUID IS NOT NULL;
CREATE INDEX IF NOT EXISTS "Q_p_c_QAStateValues" ON QAStateValues (QAStateUUID,parentUUID,childUUID) WHERE childUUID IS NOT NULL AND parentUUID IS NOT NULL;
--
CREATE INDEX IF NOT EXISTS "p_predicate_label_relation" ON predicate_label_relation (predicateUUID);
--^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^



CREATE TABLE IF NOT EXISTS questionInstance_OpSelectorManager_relation(
    questionInstanceUUID string NOT NULL,
    startingAnswerIndex integer NOT NULL,
    OpSelectorManagerUUID string NOT NULL,
    dateAndTimeComputationStarted datetime,
    dateAndTimeComputationFinished datetime,
    primary key (questionInstanceUUID, startingAnswerIndex)
);

-- other information may be present below...
CREATE TABLE IF NOT EXISTS OpSelectorManagerInfo(
    OpSelectorManagerUUID primary key
);

CREATE TABLE IF NOT EXISTS OpSelectorManagerValues(
    questionInstanceUUID string NOT NULL,
    OpSelectorManagerUUID NOT NULL,
    startingAnswerIndex integer NOT NULL,
    fieldName string NOT NULL,
    parentUUID string,
    childUUID string,
    fieldValue blob
    check( startingAnswerIndex >= 0)
);


--=====================================================================


