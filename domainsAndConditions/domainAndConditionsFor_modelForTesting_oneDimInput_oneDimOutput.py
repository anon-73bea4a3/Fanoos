

import config;
_LOCALDEBUGFLAG = config.debugFlags.get_v_print_ForThisFile(__file__);
    

import numpy as np;
from utils.contracts import *;

from boxesAndBoxOperations.getBox import getDimensionOfBox;

import z3;

from domainsAndConditions.baseClassConditionsToSpecifyPredictsWith import CharacterizationConditionsBaseClass, CharacterizationCondition_FromPythonFunction;
from domainsAndConditions.baseClassDomainInformation import BaseClassDomainInformation ;

from domainsAndConditions.utilsForDefiningPredicates import *;


class DomainFor_modelForTesting_oneDimInput_oneDimOutput(BaseClassDomainInformation):

    def __init__(self, z3SolverInstance):
        requires(isinstance(z3SolverInstance, z3.z3.Solver));
        self.initializedConditions = None;
        self.initialize_baseConditions(z3SolverInstance);
        assert(self.initializedConditions != None);
        return;

    @staticmethod
    def getUUID():
        return "e2773e2f-9109-4444-8a51-37ba22dd3ceb";

    @staticmethod
    def getInputSpaceUniverseBox():
        orderOfVariables = __class__.inputSpaceVariables();
        dictMappingVariableToBound = {\
            "in_x" : [-5.0, 5.0] \
        };
        thisUniverseBox =  __class__._helper_getInputSpaceUniverseBox(\
                               orderOfVariables, dictMappingVariableToBound);
        ensures(getDimensionOfBox(thisUniverseBox) == len(DomainFor_modelForTesting_oneDimInput_oneDimOutput.inputSpaceVariables()));
        return thisUniverseBox;

    @staticmethod
    def inputSpaceVariables():
        return [\
            z3.Real(x) for x in ["in_x"] ];

    @staticmethod
    def outputSpaceVariables():
        return [z3.Real(x) for x in ["out_y"]];

    @staticmethod
    def getName():
        return "Domain For modelForTesting_oneDimInput_oneDimOutput";

    def initialize_baseConditions(self, z3SolverInstance):
        dictMappingPredicateStringNameToUUID = \
        {
        "INNEG10DOT0TONEG9DOT0" : "db2a1ddb-8088-4068-9f69-3968646858f0" , \
        "INNEG10DOT0TONEG9DOT5" : "d4649337-1c95-40f0-9af3-75e3fd7db819" , \
        "INNEG9DOT5TONEG9DOT0" : "fb30abf2-b099-49de-886a-3c48a1fa9387" , \
        "INNEG9DOT0TONEG8DOT0" : "75db05ee-70cb-4c08-bc17-c711f1d5f7db" , \
        "INNEG9DOT0TONEG8DOT5" : "975ee971-50ca-4e93-80d1-80574b3da93d" , \
        "INNEG8DOT5TONEG8DOT0" : "d9b7684c-14e4-4326-8410-018e11e91709" , \
        "INNEG8DOT0TONEG7DOT0" : "44adc0c5-81ce-4286-b414-86e97fac5e0f" , \
        "INNEG8DOT0TONEG7DOT5" : "c6945de5-d222-4974-956c-c80eb3cdbaf5" , \
        "INNEG7DOT5TONEG7DOT0" : "2f7a0541-27ec-48fb-977e-a48d7b2e4e1c" , \
        "INNEG7DOT0TONEG6DOT0" : "8c1360e7-40e7-4f8d-9def-e9c81b92dfa0" , \
        "INNEG7DOT0TONEG6DOT5" : "60733d02-f787-471d-b0a1-16d5f87eb4c5" , \
        "INNEG6DOT5TONEG6DOT0" : "4de52ebc-4c80-43e9-9d2d-b02615d9a87c" , \
        "INNEG6DOT0TONEG5DOT0" : "b88952f9-7824-4be9-b05c-32ac0e61f727" , \
        "INNEG6DOT0TONEG5DOT5" : "8dad23fd-54a7-4e15-b7a4-3c00721881a6" , \
        "INNEG5DOT5TONEG5DOT0" : "4e7a95d8-6ae9-4544-b9d4-4907a0830506" , \
        "INNEG5DOT0TONEG4DOT0" : "1da5d485-b94b-4234-bc5f-28ff807e5e44" , \
        "INNEG5DOT0TONEG4DOT5" : "bd357a9c-3c18-4134-817f-c6ced25b5bff" , \
        "INNEG4DOT5TONEG4DOT0" : "1a23a2b1-a37a-480b-b5fc-83e05660f645" , \
        "INNEG4DOT0TONEG3DOT0" : "f4be9bfc-bdbf-43f1-b3b1-48842ec8c929" , \
        "INNEG4DOT0TONEG3DOT5" : "1def8aea-92fc-4998-95ce-2d1f76cb8d99" , \
        "INNEG3DOT5TONEG3DOT0" : "ea5ed997-ca51-4da1-a344-c38e064407b4" , \
        "INNEG3DOT0TONEG2DOT0" : "dfc7f432-b738-4198-afa5-a8a2c8f41ebe" , \
        "INNEG3DOT0TONEG2DOT5" : "fc85d7a3-6bb7-4a76-ad4e-fa84fbfb9c2a" , \
        "INNEG2DOT5TONEG2DOT0" : "70952127-d35e-4a4c-98bd-60a4d87370ff" , \
        "INNEG2DOT0TONEG1DOT0" : "77dd1811-dc71-44e8-a364-e343d6a60f69" , \
        "INNEG2DOT0TONEG1DOT5" : "7ca63199-3618-49ea-950c-98b061ef1226" , \
        "INNEG1DOT5TONEG1DOT0" : "6bb3434e-9d46-4fb1-b507-e15f08ad4b93" , \
        "INNEG1DOT0TO0DOT0" : "207bad2a-5aea-484e-8ba5-a24d26189a79" , \
        "INNEG1DOT0TONEG0DOT5" : "1387a719-7347-4090-b2ee-5667510380c8" , \
        "INNEG0DOT5TO0DOT0" : "a13abe92-ebd1-4b80-b266-5ef1c473b911" , \
        "IN0DOT0TO1DOT0" : "a4aff326-51d9-461d-a789-031438936e49" , \
        "IN0DOT0TO0DOT5" : "9f1a2c66-009f-4440-a536-6dd19fd34235" , \
        "IN0DOT5TO1DOT0" : "98017e69-1e3d-4a08-99bd-50ca1eb02a6f" , \
        "IN1DOT0TO2DOT0" : "aa456821-34d0-4960-b414-62aeffabcacb" , \
        "IN1DOT0TO1DOT5" : "85cc3d8d-501d-4688-91d4-c2101876c781" , \
        "IN1DOT5TO2DOT0" : "b46f835a-d295-40c9-a08c-c7045efa49e6" , \
        "IN2DOT0TO3DOT0" : "bc9c72cd-5fca-42b5-b94f-4a4e69666ac0" , \
        "IN2DOT0TO2DOT5" : "83b55d67-52f0-4869-86e1-add216bb5dae" , \
        "IN2DOT5TO3DOT0" : "67d30b36-dbda-4d54-88c6-0d549ec1061d" , \
        "IN3DOT0TO4DOT0" : "35328f41-ddba-4225-98f4-a26c4211cf27" , \
        "IN3DOT0TO3DOT5" : "e6ed9b47-4e4b-41b0-afef-bcbe49a29bac" , \
        "IN3DOT5TO4DOT0" : "d9760c1d-18cf-4c02-b821-771cba6f6bc2" , \
        "IN4DOT0TO5DOT0" : "f7a6bbf3-631f-482a-b80c-c6aae74f6ea9" , \
        "IN4DOT0TO4DOT5" : "4988ab15-3a26-4764-8537-97cc4862be60" , \
        "IN4DOT5TO5DOT0" : "6c28d7ab-9c76-4446-a428-3758d4561c89" , \
        "IN5DOT0TO6DOT0" : "7d381ad9-0c24-47d3-947c-ccc2ac803f7f" , \
        "IN5DOT0TO5DOT5" : "8336a5a2-fd71-42f4-a6a1-2e15df02a203" , \
        "IN5DOT5TO6DOT0" : "9230da5a-1812-4b8a-925a-5ae8cfcfa11a" , \
        "IN6DOT0TO7DOT0" : "00aa1dca-1f6f-4bb0-8823-388ed399d498" , \
        "IN6DOT0TO6DOT5" : "ff5197aa-c33c-4934-abee-7fa1b1cb7874" , \
        "IN6DOT5TO7DOT0" : "0490c272-b652-41ff-9d20-34804d1b2d7f" , \
        "IN7DOT0TO8DOT0" : "549429a0-0f23-4be5-a577-f43a186eae5a" , \
        "IN7DOT0TO7DOT5" : "5316a69e-338f-4ac6-b441-e1b2a0cc86b8" , \
        "IN7DOT5TO8DOT0" : "dd73dace-91fe-44a0-b086-05ebdd1f1bf1" , \
        "IN8DOT0TO9DOT0" : "02e99885-9d1e-44ab-b0d5-8c419a58a7a9" , \
        "IN8DOT0TO8DOT5" : "e4d03482-1bce-495b-9a5c-7ee3fb9e21b9" , \
        "IN8DOT5TO9DOT0" : "f34c630d-9113-4e44-990e-4f95fd3135a6" , \
        "IN9DOT0TO10DOT0" : "c3c1a22c-4652-4d1d-869b-a5dec1c3a9a1" , \
        "IN9DOT0TO9DOT5" : "698ad6b8-dddb-4571-9354-0c75d6506b77" , \
        "IN9DOT5TO10DOT0" : "ea758b0c-d239-469e-a663-a1ef90c9e2d5" , \
        "OUTNEG20DOT0TONEG19DOT0" : "eca0431d-d6c7-41ae-ac85-8db0cc9e7fa9" , \
        "OUTNEG20DOT0TONEG19DOT5" : "caa61dbf-e329-4c3a-973d-e6ae67bb110b" , \
        "OUTNEG19DOT5TONEG19DOT0" : "7fba4426-b3db-41dd-9f96-553cf1180f1d" , \
        "OUTNEG19DOT0TONEG18DOT0" : "e83a19ec-f3fb-4d1e-bcfa-83a2f8bb9725" , \
        "OUTNEG19DOT0TONEG18DOT5" : "3bab596b-7558-49d8-aaaa-17bbddd84a09" , \
        "OUTNEG18DOT5TONEG18DOT0" : "7541b77a-fbb7-4c78-a338-1e9d96215a12" , \
        "OUTNEG18DOT0TONEG17DOT0" : "9afad965-b784-48c4-98df-a05a6f2b7039" , \
        "OUTNEG18DOT0TONEG17DOT5" : "eca4d162-e876-4ad1-9449-bee6525375dc" , \
        "OUTNEG17DOT5TONEG17DOT0" : "45dfda64-f777-4f6c-bfec-a106d765cd66" , \
        "OUTNEG17DOT0TONEG16DOT0" : "5302e37b-0898-46fb-9782-3642620cfe3d" , \
        "OUTNEG17DOT0TONEG16DOT5" : "b3fde4fb-cdab-4627-b6c9-f1e36a77f098" , \
        "OUTNEG16DOT5TONEG16DOT0" : "06368a59-13e0-4a2a-a54a-4f04a222f5c2" , \
        "OUTNEG16DOT0TONEG15DOT0" : "1ff64a31-4736-4460-b49f-5b76abcea767" , \
        "OUTNEG16DOT0TONEG15DOT5" : "ecc98606-8bcf-4f20-a20a-b917775f8b4c" , \
        "OUTNEG15DOT5TONEG15DOT0" : "789ad1c3-8661-4ec1-9aea-a2b79b84855e" , \
        "OUTNEG15DOT0TONEG14DOT0" : "9894ac1f-7dd7-445d-94df-f8f13af9ccd8" , \
        "OUTNEG15DOT0TONEG14DOT5" : "c8a07542-a614-46f5-b5bb-8d8cdb57c148" , \
        "OUTNEG14DOT5TONEG14DOT0" : "9f4094ad-53f6-4e72-8c53-9284d22bb019" , \
        "OUTNEG14DOT0TONEG13DOT0" : "a497b214-4bb0-47b8-b196-087f54089079" , \
        "OUTNEG14DOT0TONEG13DOT5" : "010954a7-4065-4964-82c4-33436fa70ab9" , \
        "OUTNEG13DOT5TONEG13DOT0" : "3f650c7d-c7c6-482f-8901-825a312fd166" , \
        "OUTNEG13DOT0TONEG12DOT0" : "65668c81-91ce-4b99-b5f8-b5153c3bdf4d" , \
        "OUTNEG13DOT0TONEG12DOT5" : "ad576223-b6fa-45d8-835b-ad4172a2239f" , \
        "OUTNEG12DOT5TONEG12DOT0" : "7a6743e0-9e91-4c27-be77-bfc73b1b39d3" , \
        "OUTNEG12DOT0TONEG11DOT0" : "b0b8086e-5d55-4e71-a5ec-87b9c98ed676" , \
        "OUTNEG12DOT0TONEG11DOT5" : "67fff4e5-1faa-4f80-8b7a-c43d82442b0e" , \
        "OUTNEG11DOT5TONEG11DOT0" : "35a52222-598e-4960-b492-678bba0fce11" , \
        "OUTNEG11DOT0TONEG10DOT0" : "72b3c2b5-bcab-4383-999e-d51dfddb998c" , \
        "OUTNEG11DOT0TONEG10DOT5" : "82f9550e-28fa-46e1-930d-f693713aebad" , \
        "OUTNEG10DOT5TONEG10DOT0" : "b1c39fb2-cbf7-47d1-b2af-b77a6cc1bdf0" , \
        "OUTNEG10DOT0TONEG9DOT0" : "92822b83-935e-4156-b3f7-4808a6ced03e" , \
        "OUTNEG10DOT0TONEG9DOT5" : "bb34bbe3-05fa-488e-b751-eb7acb5cec0a" , \
        "OUTNEG9DOT5TONEG9DOT0" : "68326877-cb25-4648-ac83-4b76b896ff18" , \
        "OUTNEG9DOT0TONEG8DOT0" : "c55c3123-bf1d-4f60-81b4-76f246cf8afd" , \
        "OUTNEG9DOT0TONEG8DOT5" : "bb5c30d5-6b7a-4bf5-8964-37e2df41b59f" , \
        "OUTNEG8DOT5TONEG8DOT0" : "bf7cca2e-dad7-4151-9aaf-f554085dd0c0" , \
        "OUTNEG8DOT0TONEG7DOT0" : "abf8c152-efc7-4080-be00-156dea19fc66" , \
        "OUTNEG8DOT0TONEG7DOT5" : "33e66e3f-b892-45a7-b561-686efb3297aa" , \
        "OUTNEG7DOT5TONEG7DOT0" : "2b325745-4704-49d7-9dc7-b9de6777fafe" , \
        "OUTNEG7DOT0TONEG6DOT0" : "9840c2ea-4e99-466c-90ef-d6719d105a97" , \
        "OUTNEG7DOT0TONEG6DOT5" : "56172fd3-ed15-49f9-a4ff-1bf926b6434b" , \
        "OUTNEG6DOT5TONEG6DOT0" : "763a52a7-f2e0-43c9-9b5b-bd5f5b927302" , \
        "OUTNEG6DOT0TONEG5DOT0" : "3409e94e-aea4-42a5-840f-576e3c3220b7" , \
        "OUTNEG6DOT0TONEG5DOT5" : "755c8c70-e985-408a-930a-f109eb5f8745" , \
        "OUTNEG5DOT5TONEG5DOT0" : "2eea665f-7545-4ded-94bb-f7955dd54884" , \
        "OUTNEG5DOT0TONEG4DOT0" : "954a4686-fa13-4446-b96b-2a6303411e46" , \
        "OUTNEG5DOT0TONEG4DOT5" : "6d6294c7-58a5-4800-a438-cf3dcd03d2ad" , \
        "OUTNEG4DOT5TONEG4DOT0" : "7fa6139b-7c1a-4d34-be1c-8fa1d1226a1c" , \
        "OUTNEG4DOT0TONEG3DOT0" : "a4cee924-b854-4ead-9083-199942afccf4" , \
        "OUTNEG4DOT0TONEG3DOT5" : "551bbac7-58bf-4945-a3ef-e96f516653e2" , \
        "OUTNEG3DOT5TONEG3DOT0" : "160bff8b-3357-41d3-9d63-26b8e966179f" , \
        "OUTNEG3DOT0TONEG2DOT0" : "8d8293ce-89ee-498f-9880-24bfa7420b12" , \
        "OUTNEG3DOT0TONEG2DOT5" : "27c78ed8-050c-4316-8a0a-ae82e7954642" , \
        "OUTNEG2DOT5TONEG2DOT0" : "51977ca9-b25f-496e-b4c0-af84d07311b8" , \
        "OUTNEG2DOT0TONEG1DOT0" : "7b5e5b5f-f9eb-4c77-a891-d1d880cd261c" , \
        "OUTNEG2DOT0TONEG1DOT5" : "08c6c569-07c6-4d6a-9841-8789041ef762" , \
        "OUTNEG1DOT5TONEG1DOT0" : "4fc97087-d6c7-4276-acf5-549d0143cd46" , \
        "OUTNEG1DOT0TO0DOT0" : "4601bca8-aa1b-41ad-b221-9facc8c038d2" , \
        "OUTNEG1DOT0TONEG0DOT5" : "d43cfb34-8b7b-43ba-a972-e8f655db7611" , \
        "OUTNEG0DOT5TO0DOT0" : "a70a708f-4909-43ae-be7a-63422934f4e3" , \
        "OUT0DOT0TO1DOT0" : "c955d7aa-b9dd-42c6-a540-b114d46d2686" , \
        "OUT0DOT0TO0DOT5" : "f5d67024-ce6e-4892-9945-9f9ad513ed08" , \
        "OUT0DOT5TO1DOT0" : "a5df56a9-ad7f-4faf-995e-94b69d6f0ca5" , \
        "OUT1DOT0TO2DOT0" : "e6730f20-bf15-4ad1-a06e-475988465844" , \
        "OUT1DOT0TO1DOT5" : "4ecad452-6426-4249-a144-c47abaf2df34" , \
        "OUT1DOT5TO2DOT0" : "4a44d303-21da-4610-b425-233c24e1e7da" , \
        "OUT2DOT0TO3DOT0" : "9116e981-d0c5-4c0c-b453-8c85fc68f5ba" , \
        "OUT2DOT0TO2DOT5" : "47396771-b87c-4484-a283-ed71ef5b2909" , \
        "OUT2DOT5TO3DOT0" : "cadf35c6-ac3e-46eb-a963-c1ca43d4ae7a" , \
        "OUT3DOT0TO4DOT0" : "5e121664-7763-4f88-8455-2ed4080fcc0e" , \
        "OUT3DOT0TO3DOT5" : "5bef15be-d773-4dd9-b876-f31d9dfd254f" , \
        "OUT3DOT5TO4DOT0" : "30499201-8c99-4707-89e7-fdd571bfbe96" , \
        "OUT4DOT0TO5DOT0" : "37ab02df-76d3-4b5c-a01a-29ccfab28e55" , \
        "OUT4DOT0TO4DOT5" : "f4ab6d8d-8bd6-41a8-9b17-f0f346af873c" , \
        "OUT4DOT5TO5DOT0" : "cdfb3975-e1fc-436c-8bd6-4f9269506878" , \
        "OUT5DOT0TO6DOT0" : "fd110be0-5997-4ee7-8f71-8e609598ec90" , \
        "OUT5DOT0TO5DOT5" : "333fb950-24a9-4631-a3b4-df89d740ac47" , \
        "OUT5DOT5TO6DOT0" : "df5b287c-eef1-4555-81ef-7a1a1e96ee4e" , \
        "OUT6DOT0TO7DOT0" : "c567b7d5-e8fa-491a-8ce9-66e659c6ecef" , \
        "OUT6DOT0TO6DOT5" : "87cdeb87-1156-4447-b0c1-6c17f3bbfb28" , \
        "OUT6DOT5TO7DOT0" : "dd106603-e8ab-410a-adcb-5e850282e02b" , \
        "OUT7DOT0TO8DOT0" : "032edbd0-0772-49f5-988e-31373608f571" , \
        "OUT7DOT0TO7DOT5" : "3b9e6b42-1981-40b9-887f-3634d786ad70" , \
        "OUT7DOT5TO8DOT0" : "5c278635-df0a-4a9c-8ec0-b3d155903b11" , \
        "OUT8DOT0TO9DOT0" : "2b1c2cd3-49e5-4615-96e0-dd1f69554db9" , \
        "OUT8DOT0TO8DOT5" : "1dc11ab2-cb24-4c96-9b3a-dbcd41fccd45" , \
        "OUT8DOT5TO9DOT0" : "d11e9636-8daa-4d9b-9fb4-79618909a003" , \
        "OUT9DOT0TO10DOT0" : "fe1af115-3d25-45d9-bd66-34b2113998f5" , \
        "OUT9DOT0TO9DOT5" : "308a0f34-44f9-4d3a-a296-7b21c012c5f5" , \
        "OUT9DOT5TO10DOT0" : "7a95baff-d474-4ce8-af32-e7581b3276a1" , \
        "OUT10DOT0TO11DOT0" : "3fe00ffe-d076-4e6a-b8f4-0dfc1f965a21" , \
        "OUT10DOT0TO10DOT5" : "cacf032c-3ffe-4f60-be62-66da9c97d998" , \
        "OUT10DOT5TO11DOT0" : "48796d8e-e9e9-49a5-b279-93ac3a809cd2" , \
        "OUT11DOT0TO12DOT0" : "35e61753-bf23-4b51-a7ba-b3b948c045c6" , \
        "OUT11DOT0TO11DOT5" : "7f2389a0-b496-44c7-8ab9-a16b2667e31e" , \
        "OUT11DOT5TO12DOT0" : "36a2ccd5-403d-4548-a55f-858a4cfaf6e7" , \
        "OUT12DOT0TO13DOT0" : "50832367-90f7-4c5b-bf55-866635619adf" , \
        "OUT12DOT0TO12DOT5" : "c1f15fd9-3bfb-41bd-9ece-aacf2edc4aef" , \
        "OUT12DOT5TO13DOT0" : "1879b3ed-e7b5-403c-a36c-3e0ab972bc73" , \
        "OUT13DOT0TO14DOT0" : "89ddf0f4-f62b-493c-a144-beeda5d0ef7e" , \
        "OUT13DOT0TO13DOT5" : "4aa53bf2-8ee6-4ee8-8af1-216e508cee9f" , \
        "OUT13DOT5TO14DOT0" : "49da7445-8626-453f-ae6f-879135a41b9d" , \
        "OUT14DOT0TO15DOT0" : "313318a4-4672-41ac-b6ba-341e6cee6dc3" , \
        "OUT14DOT0TO14DOT5" : "56e63bd6-a515-4cea-9ca8-3fed50420ced" , \
        "OUT14DOT5TO15DOT0" : "cbaab60b-aeb1-4a7a-974c-19e4fe94f1e9" , \
        "OUT15DOT0TO16DOT0" : "c320030d-5099-4e63-b45a-139b8fd74e8e" , \
        "OUT15DOT0TO15DOT5" : "7f814059-80b2-41a1-ba50-d5e2bf92ff4a" , \
        "OUT15DOT5TO16DOT0" : "a47bc767-56a9-4b66-b24d-d50d4b6fe811" , \
        "OUT16DOT0TO17DOT0" : "5a46ce6e-d2ca-4688-8a7e-88a8cb896f6c" , \
        "OUT16DOT0TO16DOT5" : "5117bf37-c52e-4822-a76d-e939f4a6e001" , \
        "OUT16DOT5TO17DOT0" : "a8930162-48e7-4d67-ae42-c669c57d6faf" , \
        "OUT17DOT0TO18DOT0" : "9a972a7e-a831-4d13-9206-58275a771029" , \
        "OUT17DOT0TO17DOT5" : "c360b4ac-84c5-4b78-87a7-c6d5ad4a4ae3" , \
        "OUT17DOT5TO18DOT0" : "933c15a3-ecae-42bb-9411-9e4b7097e4e5" , \
        "OUT18DOT0TO19DOT0" : "d23386ce-18e8-4c59-a4bd-57d4b6c1e9cd" , \
        "OUT18DOT0TO18DOT5" : "08c56c57-5a47-43b7-a07f-dcc99ac32ead" , \
        "OUT18DOT5TO19DOT0" : "73531737-bdb7-4d10-85f1-dd53502ecdd1" , \
        "OUT19DOT0TO20DOT0" : "877d7acd-2021-4573-9bdb-9e7c44c8d83b" , \
        "OUT19DOT0TO19DOT5" : "8cb80ff2-8ce0-4aa7-a917-ab049f29ab70" , \
        "OUT19DOT5TO20DOT0" : "b73bd413-2e4a-48db-bf8a-046488a837c8" \
        };
        # Note: manualAbstractionInformation, generally speaking, is a
        #     structured used purely in analysis scripts (as developed for
        #     the paper describing Fanoos); placing this information
        #     in the class defining the domain proved to be a convieniant place to store the
        #     information during the time of development and testing. Fanoos does not access 
        #     the information in manualAbstractionInformation when determining how to make 
        #     adjustments to respond to users. Again, it is only used in analysis scripts
        #     used to prepare results for the paper. While this sanity-checking
        #     code does not have results discussed in the paper at the time of
        #     writting this comment, we needed to fill the information for 
        #     this structure; while Fanoos itself does not examin content in
        #     manualAbstractionInformation, some code (such as checking code, e.g., contracts)
        #     expect the structure to be present and obey basic properties such as
        #     number of entries.
        #
        #     While it was convieniant for development, clearly it is not
        #     ideal have this data stored here or this structure required
        #     to be present. TODO: resolve the issue just described.
        self.manualAbstractionInformation = {\
             "predicatesAndLabels" : [\
        ("INNEG10DOT0TONEG9DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("INNEG10DOT0TONEG9DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("INNEG9DOT5TONEG9DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("INNEG9DOT0TONEG8DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("INNEG9DOT0TONEG8DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("INNEG8DOT5TONEG8DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("INNEG8DOT0TONEG7DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("INNEG8DOT0TONEG7DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("INNEG7DOT5TONEG7DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("INNEG7DOT0TONEG6DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("INNEG7DOT0TONEG6DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("INNEG6DOT5TONEG6DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("INNEG6DOT0TONEG5DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("INNEG6DOT0TONEG5DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("INNEG5DOT5TONEG5DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("INNEG5DOT0TONEG4DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("INNEG5DOT0TONEG4DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("INNEG4DOT5TONEG4DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("INNEG4DOT0TONEG3DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("INNEG4DOT0TONEG3DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("INNEG3DOT5TONEG3DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("INNEG3DOT0TONEG2DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("INNEG3DOT0TONEG2DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("INNEG2DOT5TONEG2DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("INNEG2DOT0TONEG1DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("INNEG2DOT0TONEG1DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("INNEG1DOT5TONEG1DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("INNEG1DOT0TO0DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("INNEG1DOT0TONEG0DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("INNEG0DOT5TO0DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("IN0DOT0TO1DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("IN0DOT0TO0DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("IN0DOT5TO1DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("IN1DOT0TO2DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("IN1DOT0TO1DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("IN1DOT5TO2DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("IN2DOT0TO3DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("IN2DOT0TO2DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("IN2DOT5TO3DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("IN3DOT0TO4DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("IN3DOT0TO3DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("IN3DOT5TO4DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("IN4DOT0TO5DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("IN4DOT0TO4DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("IN4DOT5TO5DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("IN5DOT0TO6DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("IN5DOT0TO5DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("IN5DOT5TO6DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("IN6DOT0TO7DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("IN6DOT0TO6DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("IN6DOT5TO7DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("IN7DOT0TO8DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("IN7DOT0TO7DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("IN7DOT5TO8DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("IN8DOT0TO9DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("IN8DOT0TO8DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("IN8DOT5TO9DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("IN9DOT0TO10DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("IN9DOT0TO9DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("IN9DOT5TO10DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUTNEG20DOT0TONEG19DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("OUTNEG20DOT0TONEG19DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUTNEG19DOT5TONEG19DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUTNEG19DOT0TONEG18DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("OUTNEG19DOT0TONEG18DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUTNEG18DOT5TONEG18DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUTNEG18DOT0TONEG17DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("OUTNEG18DOT0TONEG17DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUTNEG17DOT5TONEG17DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUTNEG17DOT0TONEG16DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("OUTNEG17DOT0TONEG16DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUTNEG16DOT5TONEG16DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUTNEG16DOT0TONEG15DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("OUTNEG16DOT0TONEG15DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUTNEG15DOT5TONEG15DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUTNEG15DOT0TONEG14DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("OUTNEG15DOT0TONEG14DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUTNEG14DOT5TONEG14DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUTNEG14DOT0TONEG13DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("OUTNEG14DOT0TONEG13DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUTNEG13DOT5TONEG13DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUTNEG13DOT0TONEG12DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("OUTNEG13DOT0TONEG12DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUTNEG12DOT5TONEG12DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUTNEG12DOT0TONEG11DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("OUTNEG12DOT0TONEG11DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUTNEG11DOT5TONEG11DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUTNEG11DOT0TONEG10DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("OUTNEG11DOT0TONEG10DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUTNEG10DOT5TONEG10DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUTNEG10DOT0TONEG9DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("OUTNEG10DOT0TONEG9DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUTNEG9DOT5TONEG9DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUTNEG9DOT0TONEG8DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("OUTNEG9DOT0TONEG8DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUTNEG8DOT5TONEG8DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUTNEG8DOT0TONEG7DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("OUTNEG8DOT0TONEG7DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUTNEG7DOT5TONEG7DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUTNEG7DOT0TONEG6DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("OUTNEG7DOT0TONEG6DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUTNEG6DOT5TONEG6DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUTNEG6DOT0TONEG5DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("OUTNEG6DOT0TONEG5DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUTNEG5DOT5TONEG5DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUTNEG5DOT0TONEG4DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("OUTNEG5DOT0TONEG4DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUTNEG4DOT5TONEG4DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUTNEG4DOT0TONEG3DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("OUTNEG4DOT0TONEG3DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUTNEG3DOT5TONEG3DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUTNEG3DOT0TONEG2DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("OUTNEG3DOT0TONEG2DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUTNEG2DOT5TONEG2DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUTNEG2DOT0TONEG1DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("OUTNEG2DOT0TONEG1DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUTNEG1DOT5TONEG1DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUTNEG1DOT0TO0DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("OUTNEG1DOT0TONEG0DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUTNEG0DOT5TO0DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUT0DOT0TO1DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("OUT0DOT0TO0DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUT0DOT5TO1DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUT1DOT0TO2DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("OUT1DOT0TO1DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUT1DOT5TO2DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUT2DOT0TO3DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("OUT2DOT0TO2DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUT2DOT5TO3DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUT3DOT0TO4DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("OUT3DOT0TO3DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUT3DOT5TO4DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUT4DOT0TO5DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("OUT4DOT0TO4DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUT4DOT5TO5DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUT5DOT0TO6DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("OUT5DOT0TO5DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUT5DOT5TO6DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUT6DOT0TO7DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("OUT6DOT0TO6DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUT6DOT5TO7DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUT7DOT0TO8DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("OUT7DOT0TO7DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUT7DOT5TO8DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUT8DOT0TO9DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("OUT8DOT0TO8DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUT8DOT5TO9DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUT9DOT0TO10DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("OUT9DOT0TO9DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUT9DOT5TO10DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUT10DOT0TO11DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("OUT10DOT0TO10DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUT10DOT5TO11DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUT11DOT0TO12DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("OUT11DOT0TO11DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUT11DOT5TO12DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUT12DOT0TO13DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("OUT12DOT0TO12DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUT12DOT5TO13DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUT13DOT0TO14DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("OUT13DOT0TO13DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUT13DOT5TO14DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUT14DOT0TO15DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("OUT14DOT0TO14DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUT14DOT5TO15DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUT15DOT0TO16DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("OUT15DOT0TO15DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUT15DOT5TO16DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUT16DOT0TO17DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("OUT16DOT0TO16DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUT16DOT5TO17DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUT17DOT0TO18DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("OUT17DOT0TO17DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUT17DOT5TO18DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUT18DOT0TO19DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("OUT18DOT0TO18DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUT18DOT5TO19DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUT19DOT0TO20DOT0" , "84c05409-74a7-4d75-8ab6-daf96f76f675"), \
        ("OUT19DOT0TO19DOT5" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4"), \
        ("OUT19DOT5TO20DOT0" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4") \
             ], \
             "labelDag_firstParent_secondChild" : [ \
             ("84c05409-74a7-4d75-8ab6-daf96f76f675" , "d7082112-67c2-42c0-a9e9-df89f1ad86d4") \
             ] \
        };

        self.manualAbstractionInformation["predicatesAndLabels"] = \
             [ (dictMappingPredicateStringNameToUUID[x[0]] , x[1]) for x in self.manualAbstractionInformation["predicatesAndLabels"]];

        functToGetUuidProvided = (lambda predicateObjectBeingInitialized : 
            dictMappingPredicateStringNameToUUID[str(predicateObjectBeingInitialized)] );
    
        self.initializedConditions = \
            [CharacterizationCondition_FromPythonFunction(z3SolverInstance, DomainFor_modelForTesting_oneDimInput_oneDimOutput, x, functToGetUuidProvided=functToGetUuidProvided) \
             for x in getListFunctionsToBaseCondtionsOn_forInputOfDomainThisUse() + \
                      getListFunctionsToBaseCondtionsOn_forOutputOfDomainThisUse() + \
                      getListFunctionsToBaseCondtionsOn_forJointInputAndOutputDomainsInThisUse() ];
        assert(all([ (x.getID() == functToGetUuidProvided(x)) for x in self.initializedConditions]));
        self._writeInfoToDatabase();
        return;

    def getBaseConditions(self):
        return self.initializedConditions;




#V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V
# class-specific utilities for defining domains
#===========================================================================

def getFiniteInterval(variableType, nameOfPredicate, lowerBound, upperBound):
    requires(isinstance(nameOfPredicate, str));
    requires(variableType in {"input", "output"});
    requires(isinstance(nameOfPredicate, str));
    requires(len(nameOfPredicate) > 0);
    requires(len(set(nameOfPredicate).intersection([" ", "\n", "\r", "\t"])) == 0);
    requires(isinstance(lowerBound, float));
    requires(isinstance(upperBound, float));
    requires(np.isfinite(lowerBound));
    requires(np.isfinite(upperBound));
    requires(lowerBound <= upperBound);

    templateString = """
def funct_{0}({1}):
    \"\"\"{0}\"\"\"
    if(isinstance({1}, z3.z3.ArithRef)):
        return z3.And( {1} <= {3}, {1} >= {2} );
    else:
        return ({1} <= {3}) and ({1} >= {2} );
    raise Exception("Control should not reach here");
    return;
    """;
 
    variableNameString = "in_x";
    if(variableType == "output"):
        variableNameString = "out_y";
    assert(variableNameString in {"in_x", "out_y"});

    return templateString.format(nameOfPredicate, variableNameString, str(lowerBound), str(upperBound) );


# The below function in principle could be done with getFiniteInterval if z3 supported infinite values, but its standard theory does not seem to support
# them, which, honestly, is reasonable.
def getInfiniteInterval(variableType, nameOfPredicate, boundary, aboveOrBelow):
    requires(isinstance(nameOfPredicate, str));
    requires(variableType in {"input", "output"});
    requires(isinstance(nameOfPredicate, str));
    requires(len(nameOfPredicate) > 0);
    requires(len(set(nameOfPredicate).intersection([" ", "\n", "\r", "\t"])) == 0);
    requires(isinstance(boundary, float));
    requires(np.isfinite(boundary));
    requires(aboveOrBelow in {"lowerBound", "upperBound"});

    templateString = """
def funct_{0}({1}):
    \"\"\"{0}\"\"\"
    if(isinstance({1}, z3.z3.ArithRef)):
        return {2} <= {3};
    else:
        return {2} <= {3};
    raise Exception("Control should not reach here");
    return;
    """;

    variableNameString = "in_x";
    if(variableType == "output"):
        variableNameString = "out_y";
    assert(variableNameString in {"in_x", "out_y"});

    stringToReturn = "";
    if(aboveOrBelow == "upperBound"):
        stringToReturn = templateString.format(nameOfPredicate, variableNameString, variableNameString, str(boundry) )
    else:
        assert(aboveOrBelow == "lowerBound");
        stringToReturn = templateString.format(nameOfPredicate, variableNameString, str(boundry), variableNameString)

    return stringToReturn ;




#^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^



#V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V
# Conditions over the input domain
#===========================================================================

otherInputSpaceFunctionsToUse = """

"""



def getListFunctionsToBaseCondtionsOn_forInputOfDomainThisUse():
    listOfFunctionCodes =[];
    def boundsToName(lower, upper):
        A = str(lower).replace(".", "DOT").replace("-", "NEG");
        B = str(upper).replace(".", "DOT").replace("-", "NEG");
        return "IN" + A + "TO" + B;

    def formPredicateHere(lower, upper):
        return getFiniteInterval("input", boundsToName(lower, upper), lower, upper);

    for thisStartIndex in range(-10, 10):
        thisStartIndex = float(thisStartIndex);
        upperIndex = thisStartIndex + 1.0;
        middleIndex = thisStartIndex + 0.5;
        #  nameOfPredicate, lowerBound, upperBound)
        listOfFunctionCodes = listOfFunctionCodes + \
            [ formPredicateHere(thisStartIndex, upperIndex), formPredicateHere(thisStartIndex, middleIndex), formPredicateHere(middleIndex, upperIndex) ];

    return convertCodeListToListOfFunctions(listOfFunctionCodes);


#^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^


#V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V
# Conditions over the output domain
#===========================================================================

otherOutputSpaceFunctionsToUse = """

""";


def getListFunctionsToBaseCondtionsOn_forOutputOfDomainThisUse():
    listOfFunctionCodes =[];
    def boundsToName(lower, upper):
        A = str(lower).replace(".", "DOT").replace("-", "NEG");
        B = str(upper).replace(".", "DOT").replace("-", "NEG");
        return "OUT" + A + "TO" + B;

    def formPredicateHere(lower, upper):
        return getFiniteInterval("output", boundsToName(lower, upper), lower, upper);

    for thisStartIndex in range(-20, 20):
        thisStartIndex = float(thisStartIndex);
        upperIndex = thisStartIndex + 1.0;
        middleIndex = thisStartIndex + 0.5;
        #  nameOfPredicate, lowerBound, upperBound)
        listOfFunctionCodes = listOfFunctionCodes + \
            [ formPredicateHere(thisStartIndex, upperIndex), formPredicateHere(thisStartIndex, middleIndex), formPredicateHere(middleIndex, upperIndex) ];



    return convertCodeListToListOfFunctions(listOfFunctionCodes);

#^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^



#V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V
# Conditions over the joint domain
#===========================================================================


def getBox(nameOfPredicate, lowerBoundInput, upperBoundInput, lowerBoundOutput, upperBoundOutput):
    requires(isinstance(lowerBoundInput, float));
    requires(isinstance(upperBoundInput, float));
    requires(isinstance(lowerBoundOutput, float));
    requires(isinstance(upperBoundOutput, float));
    requires(np.isfinite(lowerBoundInput));
    requires(np.isfinite(upperBoundInput));
    requires(np.isfinite(lowerBoundOutput));
    requires(np.isfinite(upperBoundOutput));
    requires(lowerBoundInput <= upperBoundInput);
    requires(lowerBoundOutput <= upperBoundOutput);


    templateString = """
def funct_{0}(in_x, out_y):
    \"\"\"{0}\"\"\"
    if(isinstance(in_x, z3.z3.ArithRef)):
        return z3.And( in_x <= {3}, in_x >= {2}, out_y  <= {5}, out_y >= {4} );
    else:
        return (in_x <= {3}) and (in_x >= {2} ) and (out_y  <= {5}) and (out_y >= {4});
    raise Exception("Control should not reach here");
    return;
    """;

    return templateString.format(nameOfPredicate, str(lowerBoundInput), str(upperBoundInput), str(lowerBoundOutput), str(upperBoundOutput) );


# circle, 
# halfplane
# negation (or maybe just allow the user to pass in the inequality.. but actually negation would be useful for things later on... )


def getHalfPlane(nameOfPredicate, slope, intercept, inequality):
    requires(isinstance(slope, float));
    requires(isinstance(intercept, float));
    requires(np.isfinite(intercept));
    requires(np.isfinite(slope));
    requires(isinstance(inequality, str));
    requires(inequality in {"=<", "=>", "<", ">"});


    templateString = """
def funct_{0}(in_x, out_y):
    \"\"\"{0}\"\"\"
    return  in_x * {1} + {2} {3} out_y ;
    raise Exception("Control should not reach here");
    return;
    """;

    return templateString.format(nameOfPredicate, str(slope), str(intercept), str(inequality));


def getCicle(nameOfPredicate, in_x_center, out_y_center, radius, inequality):
    requires(isinstance(in_x_center, float));
    requires(np.isfinite(in_x_center));
    requires(isinstance(out_y_center, float));
    requires(np.isfinite(out_y_center));
    requires(isinstance(radius, float));
    requires(np.isfinite(radius));
    requires(isinstance(inequality, str));
    requires(inequality in {"=<", "=>", "<", ">"});


    templateString = """
def funct_{0}(in_x, out_y):
    \"\"\"{0}\"\"\"
    return  (in_x - {1}) ** 2  + (out_y - {2}) {3} {4} ;
    raise Exception("Control should not reach here");
    return;
    """;

    return templateString.format(nameOfPredicate, str(in_x_center), str(out_y_center), str(inequality), str(radius ** 2) );







def getListFunctionsToBaseCondtionsOn_forJointInputAndOutputDomainsInThisUse():
    listOfFunctionCodes =[];
    return convertCodeListToListOfFunctions(listOfFunctionCodes);

#^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^












