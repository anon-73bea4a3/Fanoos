

import config;
_LOCALDEBUGFLAG = config.debugFlags.get_v_print_ForThisFile(__file__);
    

import pickle;
import numpy as np;
import sys;
from utils.contracts import *;

from boxesAndBoxOperations.getBox import isProperBox, getBox, getDimensionOfBox, getJointBox, getContainingBox, getRandomBox;

import re;

import z3;

from domainsAndConditions.baseClassConditionsToSpecifyPredictsWith import CharacterizationConditionsBaseClass, CharacterizationCondition_FromPythonFunction;
from domainsAndConditions.baseClassDomainInformation import BaseClassDomainInformation ;

from domainsAndConditions.utilsForDefiningPredicates import *;

import uuid;

class DomainForInvertedDoublePendulum(BaseClassDomainInformation):

    def __init__(self, z3SolverInstance):
        requires(isinstance(z3SolverInstance, z3.z3.Solver));
        self.initializedConditions = None;
        self.initialize_baseConditions(z3SolverInstance);
        assert(self.initializedConditions != None);
        return;

    @staticmethod
    def getUUID():
        return "8a324d03-1391-4f4e-9589-4e4978fb4fbb";

    @staticmethod
    def getInputSpaceUniverseBox():

        # physical model specification at: bullet3/examples/pybullet/gym/pybullet_data/mjcf/inverted_double_pendulum.xml
        #     commit 3d87fb3b84eb9faed580ef7b69bb4cb9cb693907
        # state specification at: bullet3/examples/pybullet/gym/pybullet_envs/robot_pendula.py
        #     commit 3d87fb3b84eb9faed580ef7b69bb4cb9cb693907
        """
        examples/pybullet/gym/pybullet_envs/robot_pendula.py
          def apply_action(self, a):
            assert (np.isfinite(a).all())
            self.slider.set_motor_torque(200 * float(np.clip(a[0], -1, +1)))
        
          def calc_state(self):
            theta, theta_dot = self.j1.current_position()
            gamma, gamma_dot = self.j2.current_position()
            x, vx = self.slider.current_position()
            self.pos_x, _, self.pos_y = self.pole2.pose().xyz()
            assert (np.isfinite(x))
            return np.array([
                x,
                vx,
                self.pos_x,
                np.cos(theta),
                np.sin(theta),
                theta_dot,
                np.cos(gamma),
                np.sin(gamma),
                gamma_dot,
            ])
        """
        # Some notes on how the bounds below were considered:
        """

        We purposefully enlarge the range of some of the variables below, so to 
        explore what the robot would do in situations it would not normally find 
        itself in (since it controls its environment from the beginning of the run.


        <redacted some code path used to generate below; aim to add in later commit>
        ====================================
        Statistics for the input domain. Variable order: ["x", "vx", "endOfPole2_x", "pole1Angle", "pole1Angle_rateOfChange", "pole2Angle",  "pole2Angle_rateOfChange" ]
        See the function pushBoxThrough in <redacted some code path used to generate below; aim to add in later commit>
        median
        [-9.17087654e-01 -1.01356242e-01 -9.16462040e-01  1.11590028e-03
         -1.41741023e-02  6.40714566e-05  3.43284677e-03]
        mean
        [-8.36584234e-01 -5.55825160e-02 -8.36006938e-01 -3.95094858e-04
         -1.10845849e-04  4.09024498e-05  1.50040207e-04]
        std
        [0.24976108 0.21574221 0.24066486 0.0217573  0.24092117 0.00551252
         0.2698615 ]
        min
        [-0.97297198 -0.75622999 -0.96496589 -0.09813181 -0.3220316  -0.03076772
         -0.60042353]
        5% quantile
        [-0.96169371 -0.57010988 -0.96055381 -0.03824488 -0.28818685 -0.00612778
         -0.31254109]
        10% quantile
        [-0.95352224 -0.21671905 -0.95255887 -0.0086053  -0.28213323 -0.0053891
         -0.30915195]
        25% quantile
        [-0.92539008 -0.14963331 -0.92511681 -0.00406909 -0.249706   -0.00275462
         -0.29033308]
        75% quantile
        [-0.91029063  0.12560582 -0.91298939  0.00584924  0.244057    0.00259336
          0.28829787]
        90% quantile
        [-0.57014145  0.1653117  -0.53118565  0.01190971  0.28264124  0.00525244
          0.308271  ]
        95% quantile
        [-0.012156    0.16972019 -0.07910288  0.03293236  0.28733768  0.00616469
          0.31369203]
        max
        [0.05946957 0.23917278 0.00220712 0.05317138 0.51959322 0.02087447
         0.33615193]
        ====================================
        Statistics on abs of the input domain. Variable order: ["x", "vx", "endOfPole2_x", "pole1Angle", "pole1Angle_rateOfChange", "pole2Angle",  "pole2Angle_rateOfChange" ]
        median
        [0.91708765 0.14007734 0.91646204 0.00463563 0.2465699  0.00271302
         0.28928026]
        mean
        [0.83944368 0.17516411 0.83607112 0.01119903 0.22970913 0.00367768
         0.2486114 ]
        std
        [0.23997518 0.137665   0.24044178 0.01865791 0.07264117 0.00410661
         0.10496485]
        min
        [0. 0. 0. 0. 0. 0. 0.]
        5% quantile
        [0.05787052 0.09214573 0.07910288 0.00050955 0.04641253 0.00023093
         0.01096292]
        10% quantile
        [0.57014145 0.10333252 0.53118565 0.00103595 0.09850179 0.00058252
         0.02011684]
        25% quantile
        [0.91029063 0.11111132 0.91298939 0.00248957 0.22880583 0.0012283
         0.27657566]
        75% quantile
        [0.92539008 0.16597374 0.92511681 0.00836597 0.27732796 0.00477952
         0.30694401]
        90% quantile
        [0.95352224 0.23168947 0.95255887 0.03493198 0.28769558 0.00616469
         0.31307735]
        95% quantile
        [0.96169371 0.57010988 0.96055381 0.05266948 0.29233937 0.00957688
         0.31733186]
        max
        [0.97297198 0.75622999 0.96496589 0.09813181 0.51959322 0.03076772
         0.60042353]
        ====================================
        Statistics on the input domain. Variable order: [action,value ]
        median
        [0.01559919 2.84733465]
        mean
        [4.08913092e-05 2.88180130e+00]
        std
        [0.89601406 0.07568831]
        min
        [-1.         2.8295681]
        5% quantile
        [-1.         2.8341802]
        10% quantile
        [-1.          2.83570324]
        25% quantile
        [-1.          2.84043188]
        75% quantile
        [1.         2.87173254]
        90% quantile
        [1.         3.04098518]
        95% quantile
        [1.        3.0745709]
        max
        [1.         3.09394765]
        ====================================
        Statistics on abs of the input domain. Variable order: [action,value ]
        median
        [1.         2.84733465]
        mean
        [0.81950511 2.8818013 ]
        std
        [0.36228795 0.07568831]
        min
        [2.33136512e-05 2.82956810e+00]
        5% quantile
        [0.02753463 2.8341802 ]
        10% quantile
        [0.05367255 2.83570324]
        25% quantile
        [0.96223713 2.84043188]
        75% quantile
        [1.         2.87173254]
        90% quantile
        [1.         3.04098518]
        95% quantile
        [1.        3.0745709]
        max
        [1.         3.09394765]
        """

        """
        V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~~V~V~V~V~V~V~V~V~V
        SOME NOTES ABOUT endOfPole2_x : 
        ==========================================================================
        The representation we feed into the policy-frontend (see convertInvertedPendulumNetworkToAlternateFormat.py)
        uses endOfPole2_x as the delta between the measured-x-value of pole2 - roughly the x-value of the 
        "end" of pole2, but again see convertInvertedPendulumNetworkToAlternateFormat.py for further description - 
        and the x-value of the robot's main cart. The policy itself, however, expects endOfPole2_x to be
        in respect to the global space. The conversion is trivial addition between x and endOfPole2_x  - but again,
        here, we use endOfPole2_x as relative to x , while the policy accepts endOfPole2_x in respect to the global 
        coordinates. 

        A deeper issue that this illuminates is the fact that endOfPole2_x is certainly
        not independant from the other input values - in fact, given the phyisical parameters
        of the robot have been fixed already, endOfPole2_x should entirely be a function of
        x, pole1Angle and pole2Angle . Arguable, the rest of the input values are actually
        independant of the other input values - endOfPole2_x is the only one that seems to
        have this clear dependancy, which limits which points in the overall input space
        are actually possible. We note here that it should be the case that:
            endOfPole2_x = 0.3 * sin(pole2Angle + pole1Angle) + 0.6 * sin(pole1Angle) + x ;
            The 0.6 is the length of pole1. Pole 2 also has this length, but the bullet simulator
            returns position in respect to the center of mass roughly. One can find where
            there values are specified and discussion of their use in inverted_double_pendulum.xml and
            gym_pendulum_envs.py , particularly the function step in the class InvertedDoublePendulumBulletEnv , 
            located in the latter file .
            ===============
            The reason we have sin here as oppossed to cos is because pole1Angle is 
            take in respect to the vertical (e.g., pole1Angle corresponds to being parrallel
            with the y-axis). <redactions of some content here>
            So, sin(pole1Angle) actually corresponds to the normalized x-projection of pole1,
            and similar can be said for sin(pole2Angle + pole1Angle), noting that pole2Angle is
            measured relative to pole1Angle (i.e., pole2Angle == 0 means that pole2 aligns
            with pole1 - if pole1 is at pi*0.7 radians in respect to the global coordinates and
            pole2Angle is zero, then pole2 is at pi*0.7 radians in respect to the global coordinates).
        With this formula noted, it would be possible to remove the variable endOfPole2_x from the input
        space by modifying convertInvertedPendulumNetworkToAlternateFormat.py to derive a box for the 
        value based on x, pole1Angle, and pole2Angle (similar to what is done to get the sin and cos
        for the angles which the policy expects) . The code to produce a box over endOfPole2_x in this 
        fashion should be straight-forward given that code already exists in that file to produce 
        boxes over the sin of an angle ; the formula for the box over endOfPole2_x would easily be
            box(endOfPole2_x) =  0.3 * box( sin(box(pole2Angle) + box(pole1Angle)) ) + 0.6 * box( sin( box(pole1Angle) ) ) + box(x) ;
        while the "uncertainty"/size of box(endOfPole2_x)  might be larger than for the rest of the input
        boxes due to these summations, there is little that can be helped about it due to the deterministic
        nature of the boxes.

        Another possibliy would be to expand the interface for the domains to include a function
        for rejecting boxes from the CEGAR-analysis due to them not being physically possible. That would 
        help alivate construction of the box-propagator (the thing that shoves boxes through the 
        learned component we are considering) and what input space the box-propagator expects from 
        issues of the input space having internal dependancies. In general, having too many factors
        to consider when designing the box-propagator or the input space that the reachability eats-away
        at some of the point of this code, which aims to handle these sort of concerns for the user - 
        not expect the user to already to have had to solve some of them prior to using Fanoos. But this 
        may be a softer point - any given analysis stem has its strengths, weakness, barriers, etc. ...
        not to excuse the weaknesses though... This easily leads to a digression about analyzing complex,
        some commentary on-which can be found in appendix A of the writeup.

        For now we keep endOfPole2_x in the explicit input-space for the reachability. For one thing,
        doing it this way removes having to explictly embed arm-length in the code; really, this is a 
        silly point since it is almost certainly the case that the trained policy in part relies on 
        these arm-length factors. Another benefit, however, is that it is easier to:
            (1) have the system pick up properties of the controller that depend on endOfPole2_x for the most-part- 
                given how endOfPole2_x was likely included despite its technical redundancy because its 
                informative merits (e.g., which side of the base pole2 might be extending past), how the 
                policy reacts in respect to this parameter seems like something reasonbly likely to be 
                worth discussing.
            (2) similar to (1), but mostly from a coding and z3-runtime perspective, it is easier to define
                predicates that use endOfPole2_x when it is an explicit member of the space.
        All the points I just mentioned provide a good argument for extending the interface of the domains
        to filter boxes based on physical realizability, as oppossed to shoving calculations under the 
        hood to implicitly - as oppossed to explictly - consider variables of importance to the policy.
        A counter-argument to this, however, is the reasonable work I did on this before, keeping the 
        reachability-end using the angle-representation below as oppossed to the sin-and-cos representation
        the policy itself expects. ....hm.... anyway, for now, we keep endOfPole2_x as part of the input
        space, just tweaking the representation we use here to be a delta-value as oppossed to a global coordinate, 
        as mentioned above.

        ^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^
        """
        orderOfVariables = __class__.inputSpaceVariables();
        dictMappingVariableToBound = {\
            "x" : [-1 , 1], \
            "vx" : [-0.8 , 0.8], \
            "endOfPole2_x" : [-0.5, 0.5], \
            "pole1Angle" : [-0.2 , 0.2], \
            "pole1Angle_rateOfChange" : [-0.6 , 0.6], \
            "pole2Angle" : [-0.04, 0.04], \
            "pole2Angle_rateOfChange" : [-0.7, 0.7]\
        };
        thisUniverseBox =  __class__._helper_getInputSpaceUniverseBox(\
                               orderOfVariables, dictMappingVariableToBound);
        ensures(getDimensionOfBox(thisUniverseBox) == len(DomainForInvertedDoublePendulum.inputSpaceVariables()));
        return thisUniverseBox;

    @staticmethod
    def inputSpaceVariables():
        return [\
            z3.Real(x) for x in ["x", "vx", "endOfPole2_x", \
                                 "pole1Angle", "pole1Angle_rateOfChange", \
                                 "pole2Angle", "pole2Angle_rateOfChange" ]   ];

    @staticmethod
    def outputSpaceVariables():
        return [z3.Real("outputTorque"), z3.Real("stateValueEstimate")];

    @staticmethod
    def getName():
        return "Domain For Inverted Double Pendulum"


    def initialize_baseConditions(self, z3SolverInstance):
        dictMappingPredicateStringNameToUUID = \
        {
            "x Very High  Magnitude" : "21b3fb5b-efd9-4406-a7fe-b80937881e21", 
            "x High  Magnitude" : "f3c2655f-fa5c-4020-9dc8-c20a47401796", 
            "x Low  Magnitude" : "0155f83a-ef30-4a61-adda-c1321480240f", 
            "x Very Low  Magnitude" : "8de9828f-6ec7-4240-8293-b76d3d92f3f2", 
            "x Magnitude Near Normal Levels" : "7389a08e-03d4-4c89-8b58-3a2c7c203933", 
            "vx Very High  Magnitude" : "f3c56183-c013-4b2e-b11d-65244231dadd", 
            "vx High  Magnitude" : "e7f2daf6-b041-4f4a-88b9-999a4590cfc0", 
            "vx Low  Magnitude" : "f361d7bc-d6a7-4692-b38f-593e4f403d15", 
            "vx Very Low  Magnitude" : "23cd37d1-e48b-41f5-8f37-5988e9410d0f", 
            "vx Magnitude Near Normal Levels" : "69e9a231-c08e-498a-b1cb-08def786cb0c", 
            "endOfPole2_x Very High  Magnitude" :  "701785bd-f91f-4818-a997-e68258f56edb", \
            "endOfPole2_x High  Magnitude" :  "af4c0da5-b6d2-4500-8fa0-117cb812e182", \
            "endOfPole2_x Low  Magnitude" :  "44dca983-9b7f-4516-b9a7-62a47aa259d5", \
            "endOfPole2_x Very Low  Magnitude" :  "c88184e3-6914-43ae-920b-5e7f47b5c63c", \
            "endOfPole2_x Magnitude Near Normal Levels" :  "f30f1e19-a9f7-4c7f-a852-14afc5a4b9af", \
            "pole1Angle Very High  Magnitude" : "1ea9d650-b3e8-4d07-b80d-2ee64e2ee09b", 
            "pole1Angle High  Magnitude" : "f0b1a37b-f937-41e1-907f-1faec3c9a1dd", 
            "pole1Angle Low  Magnitude" : "7661646a-34db-45a8-95d6-e8d3da8ddf4d", 
            "pole1Angle Very Low  Magnitude" : "8640c6d3-12cc-438e-adf3-b84583faab65", 
            "pole1Angle Magnitude Near Normal Levels" : "9dfc2e8e-4915-4172-b856-b5b20946c393", 
            "pole1Angle_rateOfChange Very High  Magnitude" : "b7d2f662-2205-41a2-a920-cf674a09e8e4", 
            "pole1Angle_rateOfChange High  Magnitude" : "0bb61b1e-4816-4d98-99c7-41e02c85e011", 
            "pole1Angle_rateOfChange Low  Magnitude" : "491fc8a3-d091-48c6-a132-56c544cd181f", 
            "pole1Angle_rateOfChange Very Low  Magnitude" : "41a5302e-8e9c-4e63-8a29-fa2b11060e21", 
            "pole1Angle_rateOfChange Magnitude Near Normal Levels" : "a5c62d0b-386c-4e1b-bc5b-40f27e7c7cca", 
            "pole2Angle Very High  Magnitude" : "960482b5-8323-40c7-8e0a-07b64ef6e75b", 
            "pole2Angle High  Magnitude" : "44c88c08-c354-401d-a100-ae94f573391d", 
            "pole2Angle Low  Magnitude" : "2a9b0032-a39f-4faa-9664-af5209745722", 
            "pole2Angle Very Low  Magnitude" : "f95a4c4a-6cec-49fd-abf1-64f9283f33a5", 
            "pole2Angle Magnitude Near Normal Levels" : "44268c62-371f-44d4-a966-5a4e8d588d7d", 
            "pole2Angle_rateOfChange Very High  Magnitude" : "17e5a6e2-37fc-4523-aaee-9b6ac7384c0d", 
            "pole2Angle_rateOfChange High  Magnitude" : "d3d548ee-292a-43f4-99c3-1b9cbcd3ca71", 
            "pole2Angle_rateOfChange Low  Magnitude" : "4fef3e42-87f7-49d9-8e59-d9a70f52b906", 
            "pole2Angle_rateOfChange Very Low  Magnitude" : "60e5a29e-1ae8-47d2-b062-d537c089e11f", 
            "pole2Angle_rateOfChange Magnitude Near Normal Levels" : "35c790a9-f001-4dd4-9869-f855e0e2a5c4", 
            "pole1 Angle At of Above X Axis " : "40d2185a-0a53-46fb-82c4-2df793ac2f99", 
            "pole1 Moving Counter-Clockwise " : "78546928-bda7-4354-be99-7bf2dc6a2f07", 
            "Both poles pointed to the left" : "15ab5d6a-7038-4c65-b429-82de8f575486", 
            "Anchor Point Moving Left" : "12247f40-220f-49ed-bc3c-ef38c6c54be9", 
            "pole1 Moving Clockwise " : "2871af7f-a7cc-46ce-8527-00dfc5e0956f", 
            "Pole2 Moving Counter-Clockwise " : "015fb99b-fd06-4eae-9b73-95449f12dc51", 
            "pole1 Angle At of Above X Axis " : "d5886347-c798-4da7-86e5-61feb4b87ab8", 
            "pole2 On Left" : "1757016b-4dec-4310-80fa-4be7580c7afc", 
            "Pole1 On Left" : "9154a8c3-e99a-42f5-81aa-544b176bed74", 
            "Anchor Point Moving Right" : "7b62d162-2820-464b-964d-5fc853f9724e", 
            "Anchor Point Barely Moving If At All" : "ed362df9-9e7c-4d32-9249-84c8746ffd01", 
            "Pole2 Moving Clockwise " : "41b0753a-ab87-4157-bc27-65c63c0b242b", 
            "Pole2 Angle At of Above X Axis " : "b077175f-d944-4d1a-a1da-323677470aa8",
            "Pole1 On Right" : "34e8cd54-ff78-449e-9c2b-75813da7c8b2", 
            "pole2 Close to Vertical" : "7e63953e-d315-43fc-a5e8-1c3a1fc2a43a", 
            "Both poles pointed to the right" : "d12ad5c6-5e8e-4732-b8ae-07ee867927d9", 
            "pole1 Moving Barely" : "e1c004da-1dcd-4ece-82b5-448a0216e50a", 
            "Poles are Bent Like the arc in a a D" : "2dd966e1-5043-4762-bb5a-929e12c66e56", 
            "Poles are Roughly Straight in Respect To Each Other" : "964ab2ae-c908-4e32-b933-b84b91556688", 
            "pole2 On Right" : "90e03923-c6ff-4450-9a9f-84ea3576fa59", 
            "Pole2 Moving Barely" : "60f1be4c-c509-403b-86e2-1e9b6623d8cd", 
            "Pole1 Close to Vertical" : "761c320e-c078-4c1a-92f0-a8c4aa582c5d", 
            "Poles are Bent" : "6d7ef156-be5c-4744-9a3f-22f7c7a3c2f8", 
            "Poles are Bent Like the Arc in a C" : "ecb3670b-62aa-4ba1-9992-7eb6af738e68", 
            "outputTorque Very High  Magnitude" : "b1aaa0bf-5924-47e8-b9a6-cf56144b1b62", 
            "outputTorque High  Magnitude" : "e32a60e7-0a21-4220-a2cd-95f9cf87f8cb", 
            "outputTorque Low  Magnitude" : "42e9fef2-1928-4254-ac42-1b33d8abbf97", 
            "outputTorque Very Low  Magnitude" : "fecc6e90-4737-4648-bcf6-c70ed6433fb1", 
            "outputTorque Magnitude Near Normal Levels" : "695de8ac-8a76-409d-8941-63f65753cce0", 
            "stateValueEstimate Very High " : "761dc8bb-feab-439d-9ec8-a59be174ef11", 
            "stateValueEstimate High " : "238126d9-bf56-4945-9c4f-c9e04f7dda4a", 
            "stateValueEstimate Low " : "91982534-0a66-4530-886a-89f1be12b93a", 
            "stateValueEstimate Very Low " : "fa4a360c-9613-484e-a212-b9cb314bf2a1", 
            "stateValueEstimate Near Normal Levels" : "d496f7b5-6dfb-47b8-a1e9-2ead59f667fc", 
            "Speed Constant Assuming No Friction" : "91151f23-dea7-4298-871f-b6b3f0088d95", 
            "Speed Decreasing Assuming No Friction" : "9f21d925-53ed-413c-b633-e4026c102a1e", 
            "Speed Increasing Assuming No Friction" : "30298f0e-3fc0-4494-8daf-d94628226276",
            "Pole 2 is on the right of the robot chassy" :  "4370399d-f9a6-4eb2-ab5e-1eed108c58de", \
            "outputTorque is less than or equal to zero" :  "085b2bcd-f3ab-4b03-977e-61109e45b6b5", \
            "Speed Close to Constant Assuming No Friction" :  "502ab6e8-3cc3-4ace-baa3-053c05170810", \
            "Pole 2 is on the left of the robot chassy" :  "cdf7d079-c309-4ae2-8fd9-305156f745f7", \
            "outputTorque is greater than or equal to zero" :  "c32bbe98-04ce-46fc-b347-c26dc79ae051" \
        }
        # Note: manualAbstractionInformation is used purely in analysis scripts (as developed for
        #     the paper describing Fanoos); this proved to be a convieniant place to store the
        #     information during the time of development and testing. Fanoos does not access 
        #     the information in manualAbstractionInformation when determining how to make 
        #     adjustments to respond to users. Again, it is only used in analysis scripts
        #     used to prepare results for the paper.
        #
        #     While it was convieniant for development, clearly it is not
        #     ideal have this data stored here or this structure required
        #     to be present. TODO: resolve the issue just described.
        self.manualAbstractionInformation = {\
            "predicatesAndLabels" : [\
            ("21b3fb5b-efd9-4406-a7fe-b80937881e21", "347e9ab6-6712-43b8-9aff-737b9f1774d2"), \
            ("f3c2655f-fa5c-4020-9dc8-c20a47401796", "347e9ab6-6712-43b8-9aff-737b9f1774d2"), \
            ("0155f83a-ef30-4a61-adda-c1321480240f", "347e9ab6-6712-43b8-9aff-737b9f1774d2"), \
            ("8de9828f-6ec7-4240-8293-b76d3d92f3f2", "347e9ab6-6712-43b8-9aff-737b9f1774d2"), \
            ("7389a08e-03d4-4c89-8b58-3a2c7c203933", "347e9ab6-6712-43b8-9aff-737b9f1774d2"), \
            ("f3c56183-c013-4b2e-b11d-65244231dadd", "347e9ab6-6712-43b8-9aff-737b9f1774d2"), \
            ("e7f2daf6-b041-4f4a-88b9-999a4590cfc0", "347e9ab6-6712-43b8-9aff-737b9f1774d2"), \
            ("f361d7bc-d6a7-4692-b38f-593e4f403d15", "347e9ab6-6712-43b8-9aff-737b9f1774d2"), \
            ("23cd37d1-e48b-41f5-8f37-5988e9410d0f", "347e9ab6-6712-43b8-9aff-737b9f1774d2"), \
            ("69e9a231-c08e-498a-b1cb-08def786cb0c", "347e9ab6-6712-43b8-9aff-737b9f1774d2"), \
            ("701785bd-f91f-4818-a997-e68258f56edb", "347e9ab6-6712-43b8-9aff-737b9f1774d2"), \
            ("af4c0da5-b6d2-4500-8fa0-117cb812e182", "347e9ab6-6712-43b8-9aff-737b9f1774d2"), \
            ("44dca983-9b7f-4516-b9a7-62a47aa259d5", "347e9ab6-6712-43b8-9aff-737b9f1774d2"), \
            ("c88184e3-6914-43ae-920b-5e7f47b5c63c", "347e9ab6-6712-43b8-9aff-737b9f1774d2"), \
            ("f30f1e19-a9f7-4c7f-a852-14afc5a4b9af", "347e9ab6-6712-43b8-9aff-737b9f1774d2"), \
            ("1ea9d650-b3e8-4d07-b80d-2ee64e2ee09b", "347e9ab6-6712-43b8-9aff-737b9f1774d2"), \
            ("f0b1a37b-f937-41e1-907f-1faec3c9a1dd", "347e9ab6-6712-43b8-9aff-737b9f1774d2"), \
            ("7661646a-34db-45a8-95d6-e8d3da8ddf4d", "347e9ab6-6712-43b8-9aff-737b9f1774d2"), \
            ("8640c6d3-12cc-438e-adf3-b84583faab65", "347e9ab6-6712-43b8-9aff-737b9f1774d2"), \
            ("9dfc2e8e-4915-4172-b856-b5b20946c393", "347e9ab6-6712-43b8-9aff-737b9f1774d2"), \
            ("b7d2f662-2205-41a2-a920-cf674a09e8e4", "347e9ab6-6712-43b8-9aff-737b9f1774d2"), \
            ("0bb61b1e-4816-4d98-99c7-41e02c85e011", "347e9ab6-6712-43b8-9aff-737b9f1774d2"), \
            ("491fc8a3-d091-48c6-a132-56c544cd181f", "347e9ab6-6712-43b8-9aff-737b9f1774d2"), \
            ("41a5302e-8e9c-4e63-8a29-fa2b11060e21", "347e9ab6-6712-43b8-9aff-737b9f1774d2"), \
            ("a5c62d0b-386c-4e1b-bc5b-40f27e7c7cca", "347e9ab6-6712-43b8-9aff-737b9f1774d2"), \
            ("960482b5-8323-40c7-8e0a-07b64ef6e75b", "347e9ab6-6712-43b8-9aff-737b9f1774d2"), \
            ("44c88c08-c354-401d-a100-ae94f573391d", "347e9ab6-6712-43b8-9aff-737b9f1774d2"), \
            ("2a9b0032-a39f-4faa-9664-af5209745722", "347e9ab6-6712-43b8-9aff-737b9f1774d2"), \
            ("f95a4c4a-6cec-49fd-abf1-64f9283f33a5", "347e9ab6-6712-43b8-9aff-737b9f1774d2"), \
            ("44268c62-371f-44d4-a966-5a4e8d588d7d", "347e9ab6-6712-43b8-9aff-737b9f1774d2"), \
            ("17e5a6e2-37fc-4523-aaee-9b6ac7384c0d", "347e9ab6-6712-43b8-9aff-737b9f1774d2"), \
            ("d3d548ee-292a-43f4-99c3-1b9cbcd3ca71", "347e9ab6-6712-43b8-9aff-737b9f1774d2"), \
            ("4fef3e42-87f7-49d9-8e59-d9a70f52b906", "347e9ab6-6712-43b8-9aff-737b9f1774d2"), \
            ("60e5a29e-1ae8-47d2-b062-d537c089e11f", "347e9ab6-6712-43b8-9aff-737b9f1774d2"), \
            ("35c790a9-f001-4dd4-9869-f855e0e2a5c4", "347e9ab6-6712-43b8-9aff-737b9f1774d2"), \
            ("d5886347-c798-4da7-86e5-61feb4b87ab8", "84fc6cc0-0107-4c6c-8f64-d49f165118ad"), \
            ("78546928-bda7-4354-be99-7bf2dc6a2f07", "84fc6cc0-0107-4c6c-8f64-d49f165118ad"), \
            ("15ab5d6a-7038-4c65-b429-82de8f575486", "1b541080-2d54-488f-876b-c1308d73b452"), \
            ("12247f40-220f-49ed-bc3c-ef38c6c54be9", "84fc6cc0-0107-4c6c-8f64-d49f165118ad"), \
            ("2871af7f-a7cc-46ce-8527-00dfc5e0956f", "84fc6cc0-0107-4c6c-8f64-d49f165118ad"), \
            ("015fb99b-fd06-4eae-9b73-95449f12dc51", "84fc6cc0-0107-4c6c-8f64-d49f165118ad"), \
            ("1757016b-4dec-4310-80fa-4be7580c7afc", "84fc6cc0-0107-4c6c-8f64-d49f165118ad"), \
            ("b077175f-d944-4d1a-a1da-323677470aa8", "84fc6cc0-0107-4c6c-8f64-d49f165118ad"), \
            ("9154a8c3-e99a-42f5-81aa-544b176bed74", "84fc6cc0-0107-4c6c-8f64-d49f165118ad"), \
            ("7b62d162-2820-464b-964d-5fc853f9724e", "84fc6cc0-0107-4c6c-8f64-d49f165118ad"), \
            ("ed362df9-9e7c-4d32-9249-84c8746ffd01", "1b541080-2d54-488f-876b-c1308d73b452"), \
            ("41b0753a-ab87-4157-bc27-65c63c0b242b", "84fc6cc0-0107-4c6c-8f64-d49f165118ad"), \
            ("34e8cd54-ff78-449e-9c2b-75813da7c8b2", "84fc6cc0-0107-4c6c-8f64-d49f165118ad"), \
            ("7e63953e-d315-43fc-a5e8-1c3a1fc2a43a", "5b27a5f8-256f-4f2a-b8c1-a9d787f62677"), \
            ("d12ad5c6-5e8e-4732-b8ae-07ee867927d9", "1b541080-2d54-488f-876b-c1308d73b452"), \
            ("e1c004da-1dcd-4ece-82b5-448a0216e50a", "5b27a5f8-256f-4f2a-b8c1-a9d787f62677"), \
            ("2dd966e1-5043-4762-bb5a-929e12c66e56", "1b541080-2d54-488f-876b-c1308d73b452"), \
            ("964ab2ae-c908-4e32-b933-b84b91556688", "1b541080-2d54-488f-876b-c1308d73b452"), \
            ("90e03923-c6ff-4450-9a9f-84ea3576fa59", "84fc6cc0-0107-4c6c-8f64-d49f165118ad"), \
            ("60f1be4c-c509-403b-86e2-1e9b6623d8cd", "5b27a5f8-256f-4f2a-b8c1-a9d787f62677"), \
            ("761c320e-c078-4c1a-92f0-a8c4aa582c5d", "5b27a5f8-256f-4f2a-b8c1-a9d787f62677"), \
            ("6d7ef156-be5c-4744-9a3f-22f7c7a3c2f8", "1b541080-2d54-488f-876b-c1308d73b452"), \
            ("ecb3670b-62aa-4ba1-9992-7eb6af738e68", "1b541080-2d54-488f-876b-c1308d73b452"), \
            ("b1aaa0bf-5924-47e8-b9a6-cf56144b1b62", "347e9ab6-6712-43b8-9aff-737b9f1774d2"), \
            ("e32a60e7-0a21-4220-a2cd-95f9cf87f8cb", "347e9ab6-6712-43b8-9aff-737b9f1774d2"), \
            ("42e9fef2-1928-4254-ac42-1b33d8abbf97", "347e9ab6-6712-43b8-9aff-737b9f1774d2"), \
            ("fecc6e90-4737-4648-bcf6-c70ed6433fb1", "347e9ab6-6712-43b8-9aff-737b9f1774d2"), \
            ("695de8ac-8a76-409d-8941-63f65753cce0", "347e9ab6-6712-43b8-9aff-737b9f1774d2"), \
            ("761dc8bb-feab-439d-9ec8-a59be174ef11", "347e9ab6-6712-43b8-9aff-737b9f1774d2"), \
            ("238126d9-bf56-4945-9c4f-c9e04f7dda4a", "347e9ab6-6712-43b8-9aff-737b9f1774d2"), \
            ("91982534-0a66-4530-886a-89f1be12b93a", "347e9ab6-6712-43b8-9aff-737b9f1774d2"), \
            ("fa4a360c-9613-484e-a212-b9cb314bf2a1", "347e9ab6-6712-43b8-9aff-737b9f1774d2"), \
            ("d496f7b5-6dfb-47b8-a1e9-2ead59f667fc", "347e9ab6-6712-43b8-9aff-737b9f1774d2"), \
            ("91151f23-dea7-4298-871f-b6b3f0088d95", "1b541080-2d54-488f-876b-c1308d73b452"), \
            ("9f21d925-53ed-413c-b633-e4026c102a1e", "1b541080-2d54-488f-876b-c1308d73b452"), \
            ("30298f0e-3fc0-4494-8daf-d94628226276", "1b541080-2d54-488f-876b-c1308d73b452"), \
            ("21b3fb5b-efd9-4406-a7fe-b80937881e21", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("f3c2655f-fa5c-4020-9dc8-c20a47401796", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("0155f83a-ef30-4a61-adda-c1321480240f", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("8de9828f-6ec7-4240-8293-b76d3d92f3f2", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("7389a08e-03d4-4c89-8b58-3a2c7c203933", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("f3c56183-c013-4b2e-b11d-65244231dadd", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("e7f2daf6-b041-4f4a-88b9-999a4590cfc0", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("f361d7bc-d6a7-4692-b38f-593e4f403d15", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("23cd37d1-e48b-41f5-8f37-5988e9410d0f", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("69e9a231-c08e-498a-b1cb-08def786cb0c", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("701785bd-f91f-4818-a997-e68258f56edb", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("af4c0da5-b6d2-4500-8fa0-117cb812e182", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("44dca983-9b7f-4516-b9a7-62a47aa259d5", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("c88184e3-6914-43ae-920b-5e7f47b5c63c", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("f30f1e19-a9f7-4c7f-a852-14afc5a4b9af", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("1ea9d650-b3e8-4d07-b80d-2ee64e2ee09b", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("f0b1a37b-f937-41e1-907f-1faec3c9a1dd", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("7661646a-34db-45a8-95d6-e8d3da8ddf4d", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("8640c6d3-12cc-438e-adf3-b84583faab65", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("9dfc2e8e-4915-4172-b856-b5b20946c393", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("b7d2f662-2205-41a2-a920-cf674a09e8e4", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("0bb61b1e-4816-4d98-99c7-41e02c85e011", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("491fc8a3-d091-48c6-a132-56c544cd181f", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("41a5302e-8e9c-4e63-8a29-fa2b11060e21", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("a5c62d0b-386c-4e1b-bc5b-40f27e7c7cca", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("960482b5-8323-40c7-8e0a-07b64ef6e75b", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("44c88c08-c354-401d-a100-ae94f573391d", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("2a9b0032-a39f-4faa-9664-af5209745722", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("f95a4c4a-6cec-49fd-abf1-64f9283f33a5", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("44268c62-371f-44d4-a966-5a4e8d588d7d", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("17e5a6e2-37fc-4523-aaee-9b6ac7384c0d", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("d3d548ee-292a-43f4-99c3-1b9cbcd3ca71", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("4fef3e42-87f7-49d9-8e59-d9a70f52b906", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("60e5a29e-1ae8-47d2-b062-d537c089e11f", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("35c790a9-f001-4dd4-9869-f855e0e2a5c4", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("d5886347-c798-4da7-86e5-61feb4b87ab8", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("78546928-bda7-4354-be99-7bf2dc6a2f07", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("15ab5d6a-7038-4c65-b429-82de8f575486", "f933bc57-f657-48b9-9b30-166399918e1d"), \
            ("12247f40-220f-49ed-bc3c-ef38c6c54be9", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("2871af7f-a7cc-46ce-8527-00dfc5e0956f", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("015fb99b-fd06-4eae-9b73-95449f12dc51", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("1757016b-4dec-4310-80fa-4be7580c7afc", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("b077175f-d944-4d1a-a1da-323677470aa8", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("9154a8c3-e99a-42f5-81aa-544b176bed74", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("7b62d162-2820-464b-964d-5fc853f9724e", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("ed362df9-9e7c-4d32-9249-84c8746ffd01", "f933bc57-f657-48b9-9b30-166399918e1d"), \
            ("41b0753a-ab87-4157-bc27-65c63c0b242b", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("34e8cd54-ff78-449e-9c2b-75813da7c8b2", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("7e63953e-d315-43fc-a5e8-1c3a1fc2a43a", "f933bc57-f657-48b9-9b30-166399918e1d"), \
            ("d12ad5c6-5e8e-4732-b8ae-07ee867927d9", "f933bc57-f657-48b9-9b30-166399918e1d"), \
            ("e1c004da-1dcd-4ece-82b5-448a0216e50a", "f933bc57-f657-48b9-9b30-166399918e1d"), \
            ("2dd966e1-5043-4762-bb5a-929e12c66e56", "f933bc57-f657-48b9-9b30-166399918e1d"), \
            ("964ab2ae-c908-4e32-b933-b84b91556688", "f933bc57-f657-48b9-9b30-166399918e1d"), \
            ("90e03923-c6ff-4450-9a9f-84ea3576fa59", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("60f1be4c-c509-403b-86e2-1e9b6623d8cd", "f933bc57-f657-48b9-9b30-166399918e1d"), \
            ("761c320e-c078-4c1a-92f0-a8c4aa582c5d", "f933bc57-f657-48b9-9b30-166399918e1d"), \
            ("6d7ef156-be5c-4744-9a3f-22f7c7a3c2f8", "f933bc57-f657-48b9-9b30-166399918e1d"), \
            ("ecb3670b-62aa-4ba1-9992-7eb6af738e68", "f933bc57-f657-48b9-9b30-166399918e1d"), \
            ("b1aaa0bf-5924-47e8-b9a6-cf56144b1b62", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("e32a60e7-0a21-4220-a2cd-95f9cf87f8cb", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("42e9fef2-1928-4254-ac42-1b33d8abbf97", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("fecc6e90-4737-4648-bcf6-c70ed6433fb1", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("695de8ac-8a76-409d-8941-63f65753cce0", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("761dc8bb-feab-439d-9ec8-a59be174ef11", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("238126d9-bf56-4945-9c4f-c9e04f7dda4a", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("91982534-0a66-4530-886a-89f1be12b93a", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("fa4a360c-9613-484e-a212-b9cb314bf2a1", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("d496f7b5-6dfb-47b8-a1e9-2ead59f667fc", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("91151f23-dea7-4298-871f-b6b3f0088d95", "f933bc57-f657-48b9-9b30-166399918e1d"), \
            ("9f21d925-53ed-413c-b633-e4026c102a1e", "f933bc57-f657-48b9-9b30-166399918e1d"), \
            ("30298f0e-3fc0-4494-8daf-d94628226276", "f933bc57-f657-48b9-9b30-166399918e1d"), \
            ("4370399d-f9a6-4eb2-ab5e-1eed108c58de", "84fc6cc0-0107-4c6c-8f64-d49f165118ad"), \
            ("4370399d-f9a6-4eb2-ab5e-1eed108c58de", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("085b2bcd-f3ab-4b03-977e-61109e45b6b5", "84fc6cc0-0107-4c6c-8f64-d49f165118ad"), \
            ("085b2bcd-f3ab-4b03-977e-61109e45b6b5", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("cdf7d079-c309-4ae2-8fd9-305156f745f7", "84fc6cc0-0107-4c6c-8f64-d49f165118ad"), \
            ("cdf7d079-c309-4ae2-8fd9-305156f745f7", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("c32bbe98-04ce-46fc-b347-c26dc79ae051", "84fc6cc0-0107-4c6c-8f64-d49f165118ad"), \
            ("c32bbe98-04ce-46fc-b347-c26dc79ae051", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ("502ab6e8-3cc3-4ace-baa3-053c05170810", "1b541080-2d54-488f-876b-c1308d73b452"), \
            ("502ab6e8-3cc3-4ace-baa3-053c05170810", "f933bc57-f657-48b9-9b30-166399918e1d")  \
            ], \
            "labelDag_firstParent_secondChild" : [ \
            ("5b27a5f8-256f-4f2a-b8c1-a9d787f62677", "347e9ab6-6712-43b8-9aff-737b9f1774d2"), \
            ("5b27a5f8-256f-4f2a-b8c1-a9d787f62677", "84fc6cc0-0107-4c6c-8f64-d49f165118ad"), \
            ("1b541080-2d54-488f-876b-c1308d73b452", "347e9ab6-6712-43b8-9aff-737b9f1774d2"), \
            ("1b541080-2d54-488f-876b-c1308d73b452", "84fc6cc0-0107-4c6c-8f64-d49f165118ad"), \
            ("1b541080-2d54-488f-876b-c1308d73b452", "5b27a5f8-256f-4f2a-b8c1-a9d787f62677"), \
            ("f933bc57-f657-48b9-9b30-166399918e1d", "aeca763c-cec3-4c0c-ba03-da90d0f8d1cb"), \
            ] \
        };

        functToGetUuidProvided = (lambda predicateObjectBeingInitialized : 
            dictMappingPredicateStringNameToUUID[str(predicateObjectBeingInitialized)] );

        listFunctionsToBaseCondtionsOn = \
            getListFunctionsToBaseCondtionsOn_forInputOfDomainInvertedDoublePendulum() + \
            getListFunctionsToBaseCondtionsOn_forOutputOfDomainInvertedDoublePendulum()+ \
            getListFunctionsToBaseCondtionsOn_forJointOfDomainInvertedDoublePendulum();

        self.initializedConditions = \
            [CharacterizationCondition_FromPythonFunction(z3SolverInstance, DomainForInvertedDoublePendulum, x, functToGetUuidProvided=functToGetUuidProvided) \
             for x in listFunctionsToBaseCondtionsOn];

        assert(all([ (x.getID() == functToGetUuidProvided(x)) for x in self.initializedConditions]));
        self._writeInfoToDatabase();
        return;

    def getBaseConditions(self):
        return self.initializedConditions;



#V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V
# Conditions over the input domain
#===========================================================================


otherFunctionsForInputDomain = """

# Note that below is in respect to the input space representation we are dealing 
# with here, not the space the policy is expecting...
def funct_endPole2OnLeft(endOfPole2_x):
    \"\"\"Pole 2 is on the left of the robot chassy\"\"\"
    return endOfPole2_x <= 0;

# Note that below is in respect to the input space representation we are dealing 
# with here, not the space the policy is expecting...
def funct_endPole2OnRight(endOfPole2_x):
    \"\"\"Pole 2 is on the right of the robot chassy\"\"\"
    return endOfPole2_x >= 0;

# moving left or right=====================================

def funct_vxMovingLeft(vx):
    \"\"\"Anchor Point Moving Left\"\"\"
    return vx < 0;

def funct_vxMovingRight(vx):
    \"\"\"Anchor Point Moving Right\"\"\"
    return vx > 0;

def funct_vxBarelyMovingIfAtAll(vx):
    \"\"\"Anchor Point Barely Moving If At All\"\"\"
    valueOf5PercentQuantileOnAbsVx = 0.09214573;
    if(isinstance(vx, z3.z3.ArithRef)):
        assert(isinstance(vx, z3.z3.ArithRef));
        return z3Abs(vx) < valueOf5PercentQuantileOnAbsVx;
    else:
        return abs(vx) < valueOf5PercentQuantileOnAbsVx;
    raise Exception("Control should not reach here");
    return;


def funct_pole1CloseToVertical(pole1Angle):
    \"\"\"Pole1 Close to Vertical\"\"\"
    valueOf5PercentQuantileOnAbsPole1Angle = 0.00050955; 
    if(isinstance(pole1Angle, z3.z3.ArithRef)):
        assert(isinstance(pole1Angle, z3.z3.ArithRef));
        return z3Abs(pole1Angle) < valueOf5PercentQuantileOnAbsPole1Angle;
    else:
        return abs(pole1Angle) < valueOf5PercentQuantileOnAbsPole1Angle;
    raise Exception("Control should not reach here");
    return;


def funct_pole1OnLeft(pole1Angle):
    \"\"\"Pole1 On Left\"\"\"
    if(isinstance(pole1Angle, z3.z3.ArithRef)):
        return pole1Angle < 0;
    else:
        return pole1Angle  < 0;
    raise Exception("Control should not reach here");
    return;

def funct_pole1OnRight(pole1Angle):
    \"\"\"Pole1 On Right\"\"\"
    if(isinstance(pole1Angle, z3.z3.ArithRef)):
        return pole1Angle > 0;
    else:
        return pole1Angle > 0;
    raise Exception("Control should not reach here");
    return;



def funct_pole2CloseToVertical(pole2Angle, pole1Angle):
    \"\"\"pole2 Close to Vertical\"\"\"
    valueOf5PercentQuantileOnAbspole2Angle = 0.00023093; 
    if(isinstance(pole2Angle, z3.z3.ArithRef)):
        assert(isinstance(pole2Angle, z3.z3.ArithRef));
        return z3.Or( z3Abs(pole2Angle + pole1Angle) < valueOf5PercentQuantileOnAbspole2Angle, \
                      2* np.pi - z3Abs(pole2Angle + pole1Angle) < valueOf5PercentQuantileOnAbspole2Angle );
    else:
        return (abs(pole2Angle + pole1Angle) < valueOf5PercentQuantileOnAbspole2Angle) or \
               ( 2 * np.pi - abs(pole2Angle + pole1Angle) < valueOf5PercentQuantileOnAbspole2Angle);
    raise Exception("Control should not reach here");
    return;

def funct_pole2OnLeft(pole2Angle, pole1Angle):
    \"\"\"pole2 On Left\"\"\"
    if(isinstance(pole2Angle, z3.z3.ArithRef)):
        return z3.Xor(pole2Angle + pole1Angle < 0, z3Abs(pole2Angle + pole1Angle) > np.pi);
    else:
        return xor(pole2Angle + pole1Angle < 0, abs(pole2Angle + pole1Angle) > np.pi);
    raise Exception("Control should not reach here");
    return;

def funct_pole2OnRight(pole2Angle, pole1Angle):
    \"\"\"pole2 On Right\"\"\"
    if(isinstance(pole2Angle, z3.z3.ArithRef)):
        return z3.Xor(pole2Angle + pole1Angle > 0, z3Abs(pole2Angle + pole1Angle) > np.pi);
    else:
        return xor(pole2Angle + pole1Angle > 0, abs(pole2Angle + pole1Angle) > np.pi);
    raise Exception("Control should not reach here");
    return;

#================================================================

# poles moving clockwise or counter-clockwise====

def funct_pole2MovingClockwise(pole2Angle_rateOfChange):
    \"\"\"Pole2 Moving Clockwise \"\"\"
    return pole2Angle_rateOfChange > 0;


def funct_pole2MovingCounterClockwise(pole2Angle_rateOfChange):
    \"\"\"Pole2 Moving Counter-Clockwise \"\"\"
    return pole2Angle_rateOfChange < 0;


def funct_pole2MovingBarely(pole2Angle_rateOfChange):
    \"\"\"Pole2 Moving Barely\"\"\"
    valueOf5PercentQuantileOnAbsPole2AngleRateOfChange = 0.01096292;
    if(isinstance(pole2Angle_rateOfChange, z3.z3.ArithRef)):
        return z3Abs(pole2Angle_rateOfChange) < valueOf5PercentQuantileOnAbsPole2AngleRateOfChange;
    else:
        return abs(pole2Angle_rateOfChange) < valueOf5PercentQuantileOnAbsPole2AngleRateOfChange;
    raise Exception("Control should not reach here");
    return;


def funct_pole1MovingClockwise(pole1Angle_rateOfChange):
    \"\"\"pole1 Moving Clockwise \"\"\"
    return pole1Angle_rateOfChange > 0;


def funct_pole1MovingCounterClockwise(pole1Angle_rateOfChange):
    \"\"\"pole1 Moving Counter-Clockwise \"\"\"
    return pole1Angle_rateOfChange < 0;


def funct_pole1MovingBarely(pole1Angle_rateOfChange):
    \"\"\"pole1 Moving Barely\"\"\"
    valueOf5PercentQuantileOnAbspole1AngleRateOfChange = 0.04641253;
    if(isinstance(pole1Angle_rateOfChange, z3.z3.ArithRef)):
        return z3Abs(pole1Angle_rateOfChange) < valueOf5PercentQuantileOnAbspole1AngleRateOfChange;
    else:
        return abs(pole1Angle_rateOfChange) < valueOf5PercentQuantileOnAbspole1AngleRateOfChange;
    raise Exception("Control should not reach here");
    return;


def funct_bothPolesPointedToLeft(pole1Angle, pole2Angle):
    \"\"\"Both poles pointed to the left\"\"\"

    def funct_pole2OnLeft(pole2Angle, pole1Angle):
        \"\"\"pole2 On Left\"\"\"
        if(isinstance(pole2Angle, z3.z3.ArithRef)):
            return z3.Xor(pole2Angle + pole1Angle < 0, z3Abs(pole2Angle + pole1Angle) > np.pi);
        else:
            return xor(pole2Angle + pole1Angle < 0, abs(pole2Angle + pole1Angle) > np.pi);
        raise Exception("Control should not reach here");
        return;

    def funct_pole1OnLeft(pole1Angle):
        \"\"\"Pole1 On Left\"\"\"
        if(isinstance(pole1Angle, z3.z3.ArithRef)):
            return pole1Angle < 0;
        else:
            return pole1Angle  < 0;
        raise Exception("Control should not reach here");
        return;

    if(isinstance(pole2Angle, z3.z3.ArithRef)):
        assert(isinstance(pole1Angle, z3.z3.ArithRef));
        return z3.And( funct_pole1OnLeft(pole1Angle) , funct_pole2OnLeft(pole2Angle, pole1Angle)  );
    else:
        return (funct_pole1OnLeft(pole1Angle) and funct_pole2OnLeft(pole2Angle, pole1Angle) );
    raise Exception("Control should not reach here");
    return;



def funct_bothPolesPointedToRight(pole1Angle, pole2Angle):
    \"\"\"Both poles pointed to the right\"\"\"

    def funct_pole1OnRight(pole1Angle):
        \"\"\"Pole1 On Right\"\"\"
        if(isinstance(pole1Angle, z3.z3.ArithRef)):
            return pole1Angle > 0;
        else:
            return pole1Angle > 0;
        raise Exception("Control should not reach here");
        return;
    
    def funct_pole2OnRight(pole2Angle, pole1Angle):
        \"\"\"pole2 On Right\"\"\"
        if(isinstance(pole2Angle, z3.z3.ArithRef)):
            return z3.Xor(pole2Angle + pole1Angle > 0, z3Abs(pole2Angle + pole1Angle) > np.pi);
        else:
            return xor(pole2Angle + pole1Angle > 0, abs(pole2Angle + pole1Angle) > np.pi);
        raise Exception("Control should not reach here");
        return;

    if(isinstance(pole2Angle, z3.z3.ArithRef)):
        assert(isinstance(pole1Angle, z3.z3.ArithRef));
        return z3.And( funct_pole1OnRight(pole1Angle) , funct_pole2OnRight(pole2Angle, pole1Angle) );
    else:
        return ( funct_pole1OnRight(pole1Angle) and funct_pole2OnRight(pole2Angle, pole1Angle) );
    raise Exception("Control should not reach here");
    return;

def funct_polesRoughtlyStraight(pole1Angle, pole2Angle):
    \"\"\"Poles are Roughly Straight in Respect To Each Other\"\"\"
    IQROfPole2Angles=0.0052; 
    if(isinstance(pole2Angle, z3.z3.ArithRef)):
        assert(isinstance(pole1Angle, z3.z3.ArithRef));
        return z3Abs(pole2Angle) <= IQROfPole2Angles;
    else:
        return abs(pole2Angle) <= IQROfPole2Angles;
    raise Exception("Control should not reach here");
    return;


def funct_polesInCBend(pole1Angle, pole2Angle):
    \"\"\"Poles are Bent Like the Arc in a C\"\"\"
    if(isinstance(pole2Angle, z3.z3.ArithRef)):
        assert(isinstance(pole1Angle, z3.z3.ArithRef));
        return z3.Or(\
               z3.And(pole1Angle < 0, pole1Angle > -np.pi/2, pole2Angle + pole1Angle > 0 , pole2Angle + pole1Angle <= np.pi) , \
               z3.And(pole1Angle < -np.pi/2, pole2Angle + pole1Angle < -np.pi , pole2Angle + pole1Angle >= -1.5 * np.pi) , \
               );
    else:
        return any([\
               all([pole1Angle < 0, pole1Angle > -np.pi/2, pole2Angle + pole1Angle > 0 , pole2Angle + pole1Angle <= np.pi]) , \
               all([pole1Angle < -np.pi/2, pole2Angle + pole1Angle < -np.pi , pole2Angle + pole1Angle >= -1.5 * np.pi]) , \
               ]);
    raise Exception("Control should not reach here");
    return;



def funct_polesInDBend(pole1Angle, pole2Angle):
    \"\"\"Poles are Bent Like the arc in a a D\"\"\"
    # below, recall that our angles exist in [-np.pi, np,pi] (at least on of these bounds might be exclusive...)...
    if(isinstance(pole2Angle, z3.z3.ArithRef)):
        assert(isinstance(pole1Angle, z3.z3.ArithRef));
        return z3.Or(\
               z3.And(pole1Angle > 0, pole1Angle < np.pi/2, pole2Angle + pole1Angle > 0 , pole2Angle + pole1Angle >= -np.pi) , \
               z3.And(pole1Angle > np.pi/2, pole2Angle + pole1Angle > np.pi , pole2Angle + pole1Angle <= 1.5 * np.pi) , \
               );
    else:
        return any([\
               all([pole1Angle > 0, pole1Angle < np.pi/2, pole2Angle + pole1Angle > 0 , pole2Angle + pole1Angle >= -np.pi]) , \
               all([pole1Angle > np.pi/2, pole2Angle + pole1Angle > np.pi , pole2Angle + pole1Angle <= 1.5 * np.pi]) , \
               ]);
    raise Exception("Control should not reach here");
    return;



def funct_polesAreBent(pole2Angle):
    \"\"\"Poles are Bent\"\"\"
    IQROfPole2Angles=0.0052; 
    if(isinstance(pole2Angle, z3.z3.ArithRef)):
        return z3Abs(pole2Angle) > IQROfPole2Angles;
    else:
        return abs(pole2Angle) > IQROfPole2Angles;
    raise Exception("Control should not reach here");
    return;




# poles above or below the line x=0....====
def funct_pole2AtOrAboveXAxis(pole2Angle, pole1Angle ):
    \"\"\"Pole2 Angle At of Above X Axis \"\"\"
    if(isinstance(pole2Angle, z3.z3.ArithRef)):
        return z3Abs(pole2Angle + pole1Angle ) >= np.pi / 2;
    else:
        return abs(pole2Angle + pole1Angle ) >= np.pi / 2;
    raise Exception("Control should not reach here");
    return;


def funct_pole2AtOrBelowXAxis(pole2Angle, pole1Angle):
    \"\"\"Pole2 Angle At of Above X Axis \"\"\"
    if(isinstance(pole2Angle, z3.z3.ArithRef)):
        return z3Abs(pole2Angle + pole1Angle ) <= np.pi / 2;
    else:
        return abs(pole2Angle + pole1Angle ) <= np.pi / 2;
    raise Exception("Control should not reach here");
    return;


def funct_pole1AtOrAboveXAxis(pole1Angle):
    \"\"\"pole1 Angle At of Above X Axis \"\"\"
    if(isinstance(pole1Angle, z3.z3.ArithRef)):
        return z3Abs(pole1Angle) >= np.pi / 2;
    else:
        return abs(pole1Angle) >= np.pi / 2;
    raise Exception("Control should not reach here");
    return;


def funct_pole1AtOrBelowXAxis(pole1Angle):
    \"\"\"pole1 Angle At of Above X Axis \"\"\"
    if(isinstance(pole1Angle, z3.z3.ArithRef)):
        return z3Abs(pole1Angle) <= np.pi / 2;
    else:
        return abs(pole1Angle) <= np.pi / 2;
    raise Exception("Control should not reach here");
    return;

"""



def getListFunctionsToBaseCondtionsOn_forInputOfDomainInvertedDoublePendulum():
    listOfFunctionCodes =[];
    inputSpaceVariables = ["x", "vx", "endOfPole2_x", \
                                 "pole1Angle", "pole1Angle_rateOfChange", \
                                 "pole2Angle", "pole2Angle_rateOfChange" ];
    medians = [0.91708765, 0.14007734, 0.00365422, 0.00463563, 0.2465699,  0.00271302, \
        0.28928026]
    stds = [0.23997518, 0.137665, 0.01593154, 0.01865791, 0.07264117, 0.00410661, \
        0.10496485]
    quantile0Dot10 = [0.57014145, 0.10333252, 0.00075904, 0.00103595, 0.09850179, 0.00058252,\
        0.02011684]
    quantile0Dot25 = [0.91029063, 0.11111132, 0.0019229, 0.00248957, 0.22880583, 0.0012283,\
        0.27657566]
    quantile0Dot75 = [0.92539008, 0.16597374, 0.00588772, 0.00836597, 0.27732796, 0.00477952, \
        0.30694401]
    quantile0Dot90 = [0.95352224, 0.23168947, 0.03269801, 0.03493198, 0.28769558, 0.00616469, \
        0.31307735]

    listOfFunctionCodes = \
        getFunctionCodeBasedOnThresholdsAndIndividualVariables(inputSpaceVariables, quantile0Dot90, \
            quantile0Dot75, quantile0Dot25, quantile0Dot10, medians, stds, indicesOfVariablesToUseBoolFor=set([0,1,2,3,4,5,6]));
    listOfFunctionCodes.append(otherFunctionsForInputDomain);

    return convertCodeListToListOfFunctions(listOfFunctionCodes);


#^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^


#V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V
# Conditions over the output domain
#===========================================================================


otherFunctionsForOutputDomain = """

def funct_outputTorquePositive(outputTorque):
    \"\"\"outputTorque is greater than or equal to zero\"\"\"
    return outputTorque >= 0;

def funct_outputTorqueNegative(outputTorque):
    \"\"\"outputTorque is less than or equal to zero\"\"\"
    return outputTorque <= 0;

""";


def getListFunctionsToBaseCondtionsOn_forOutputOfDomainInvertedDoublePendulum():
    listOfFunctionCodes =[];
    inputSpaceVariables = ["outputTorque", "stateValueEstimate"];
    # We modify the bounds to account for the fact that we want the abs to be applied to 
    # to the output torque...
    dictMappingVariableToBound = {\
            "outputTorque" : [0.0 , 1.0], \
            "stateValueEstimate" : [-3.98 , 1.42] \
    };
    quantile0Dot90 = [1.0, 3.04098518];
    quantile0Dot75 = [1.0, 2.87173254];
    quantile0Dot25 = [0.96223713, 2.84043188];
    quantile0Dot10 = [0.05367255, 2.83570324];
    medians = [1.0, 2.84733465];
    stds = [0.36228795, 0.07568831];
    listOfFunctionCodes = \
        getFunctionCodeBasedOnThresholdsAndIndividualVariables(inputSpaceVariables, quantile0Dot90, \
            quantile0Dot75, quantile0Dot25, quantile0Dot10, medians, stds, indicesOfVariablesToUseBoolFor=set([0]));
    listOfFunctionCodes.append(otherFunctionsForOutputDomain);

    return convertCodeListToListOfFunctions(listOfFunctionCodes);

#^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^



#V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V
# Conditions over the joint domain
#===========================================================================

otherFunctionsForJointDomain = """

def funct_speedIncreasing(vx, outputTorque):
    \"\"\"Speed Increasing Assuming No Friction\"\"\"
    return vx * outputTorque > 0;


def funct_speedDecreasing(vx, outputTorque):
    \"\"\"Speed Decreasing Assuming No Friction\"\"\"
    return vx * outputTorque < 0;


def funct_speedConstant(vx, outputTorque):
    \"\"\"Speed Constant Assuming No Friction\"\"\"
    return outputTorque == 0; # This predicate will probably never be used since it 
        # specifies a lower dimensional space... it is a sanity check, then....


def funct_speedCloseToConstant(vx, outputTorque):
    \"\"\"Speed Close to Constant Assuming No Friction\"\"\"
    quartileTenPercentForAbsOutputTorque = 0.05367255;
    if(isinstance(outputTorque, z3.z3.ArithRef)):
        return z3Abs(outputTorque) < quartileTenPercentForAbsOutputTorque; 
    else:
        return abs(outputTorque) < quartileTenPercentForAbsOutputTorque;
    raise Exception("Control should not reach here.");
    return;

""";

def getListFunctionsToBaseCondtionsOn_forJointOfDomainInvertedDoublePendulum():
    listOfFunctionCodes = [];
    listOfFunctionCodes.append(otherFunctionsForJointDomain);

    # TODO: joint conditions that joint together certain subsets of the different operators
    return convertCodeListToListOfFunctions(listOfFunctionCodes); # ssh-rsa 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 abc@defg

#================================================================

#^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^







