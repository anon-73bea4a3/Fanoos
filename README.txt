** Fanoos: Multi-Resolution, Multi-Strength, Interactive Explanations for Learned Systems

Code and additional technical appendix to compliment submission to CIKM 2021
See writeup.pdf for the additional written material.


One can begin playing with the system by running:
python3 fanoos.py
See DEPENDENCIES.txt for a list of software dependencies this code has.


A public rsa key that allows us (the code authors) to deanonymize ourselves at a
later date (while currently being anonymous for double-blind review) can be
found in key.pub , and worked into parts of the code.



V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V
LICENSE
===============================================================================

If accepted, we intend to release the code publically under a GPL3.0 license.

^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^



V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V
Learned Systems And Domains Available in this Release
===============================================================================

Below files contain trained policies discussed in the paper along with code
used to generate/learn/tweak them:
    -------------------
    trainedNetworks/cpuPolynomialRegressionModel:
        ------------------
        polynomialRegressionTrial.py
            -----------------
            NOTE: data used to learn the model here-produced is from 
            https://www.openml.org/api/v1/json/data/562 and
            shared under CC-BY-4 (see https://creativecommons.org/licenses/by/4.0/
            and https://www.openml.org/cite). The data itself is not stored here 
            (one must run the script above to download it), but the model generated 
            (provided in the pickle file below) potentially may be considered a
            derivative work since it is trained using said data.
        -------------------
        trainedPolynomialModelInfo.pickle
        -------------------
    trainedNetworks/invertedDoublePendulumBulletEnv_v0:
        ---------------------
        convertInvertedPendulumNetworkToAlternateFormat.py
        ---------------------
        networkLayers_putIntoProperFormat.pickle
            ------------------
            This learned model has the potential to be considered a derived
            work from rl-baselines-zoo , which is shared under an MIT license.
            Please see https://github.com/araffin/rl-baselines-zoo/blob/master/LICENSE 
            for the license on the original learned network and 
            https://github.com/araffin/rl-baselines-zoo/tree/master/trained_agents/ppo2/InvertedDoublePendulumBulletEnv-v0
            for the original networks.
                ---------------------
                See the domain specification code for the inverted double
                pendulum (./domainsAndConditions/domainAndConditionsForInvertedDoublePendulum.py)
                to see further points to where the training code and environment specification
                for the network can be found. 

In addition to the above files which were discussed in the paper, two additional
models for testing and sanity-checking purposes can be found in:
    ------------------------------------
    trainedNetworks/modelForTesting
        ------------------------------------
        formModelForTesting_oneDimInput_oneDimOutput_identityFunction.py
            -------------------------------
            Produces the system stored in
            modelForTesting_oneDimInput_oneDimOutput_identityFunction.pickle .
            While the code in this file easily extends to more interesting functions,
            the function implemented and saved is simply a one-dimensional identity
            (i.e., f(x) = x)--- BEAR IN MIND the input-space bounding box when
            interpreting results (see the function getInputSpaceUniverseBox in 
            domainsAndConditions/domainAndConditionsFor_modelForTesting_oneDimInput_oneDimOutput.py )  
        ------------------------------------
        formModelForTesting_twoDimInput_threeDimOutput_identityFunctionAndAddition.py
            -------------------------------
            Produces the system stored in
            modelForTesting_twoDimInput_threeDimOutput_identityFunctionAndAddition.pickle .
            While the code in this file easily extends to more interesting functions,
            the function implemented and saved is a simple linear function from two inputs
            to three: f(x, y) = (x, y, x + y - 1) ---
            BEAR IN MIND the input-space bounding box when interpreting results
            (see the function getInputSpaceUniverseBox in 
            domainsAndConditions/domainAndConditionsFor_modelForTesting_twoDimInput_threeDimOutput.py )
        ------------------------------------
        modelForTesting_oneDimInput_oneDimOutput_identityFunction.pickle
        ------------------------------------
        modelForTesting_twoDimInput_threeDimOutput_identityFunctionAndAddition.pickle

We had intended to include in this release another series of learned system we 
analyzed which controlled a Dubins's-Car-Like. The learned systems were implemented
using the same architecture as policy network in the inverted double pendulum 
above. One network learned how to drive and steer effectively
while skidding/sliding around a circle, and another learned to drive straight under
similar environmental conditions. Unfortunately, due to lack of clarity in the
license for the training code, we are currently uncomfortable including the 
controllers learned in that software in this code release. An example of an early
domain used for these Dubins's-Car-Like system can be found at: 
domainsAndConditions/domainAndConditionsForCircleFollowing.py

^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^



V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V
Installations Instructions
-------------------------------------------------------------------------------
Both methods of installation listed below should result in Fanoos functioning
for typical users. We recommend using AWS (or other computer 
infrastructure which allows a native install) for the sake of performance. For
those who simply wish to casually interact with the system and get a high-level
idea of what interactions are like, the Docker install may be sufficient and
would be more convenient to setup. For added efficiency, there is a script
that will alter the python code to remove contracts from it, envokeable
with the command "python3 removePythonContracts.py"; we recommand against 
running the removePythonContracts.py script for any sort of casual interaction.
===============================================================================

V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V
Instructions for Installing on an AWS EC2 machine
===============================================================================

EC2 Instance:
    Ubuntu 18.04 instance (t2.micro EC2 instance - a "free-tier" server instance)
        specifically: Ubuntu Server 18.04 LTS (HVM), SSD Volume Type - ami-0a63f96e85105c6d3 (64-bit
        x86)
Security group settings:
    inbound: SSH, only from "my ip address"
    outbound:
        allow HTTPS from 0.0.0.0/0
        allow HTTP from 0.0.0.0/0
        same information ,but in table format just copied from AWS:
            Type Protocol Port range Destination Description - optional
            HTTP TCP 80 0.0.0.0/0 -
            HTTPS TCP 443 0.0.0.0/0
Commands to run once EC2 instance is running, and you access it by SSH:
    sudo apt update
    sudo apt upgrade -y python3
    sudo apt install -y python3-pip
    pip3 install scipy
    pip3 install sklearn
    pip3 install matplotlib
    git clone https://github.com/Z3Prover/z3
    cd z3
    python3 scripts/mk_make.py --python
    time ( cd build
      make
      sudo make install);
      # NOTE: For the author, these were the timing statistics:
      # real 22m58.712s
      # user 21m49.574s
      # sys 1m7.419s
    cd ..
    git clone https://github.com/anon-73bea4a3
    cd Fanoos
    # NOTE: from here you should be able to interact with the system using 
    # "python3 fanoos.py" without issue

^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^


V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V~V
Instructions for Installing via Docker Container
===============================================================================

To setup the latest version of Fanoos on docker, run the following commands in the
top-level of the code repo:
    docker build -t image_for_fanoos . ;
    docker create --name container_for_fanoos -ti --mount src=$(pwd),dst="/home/user8d0a0629178c48bdab52171a1f3b981d/fanoosCode",type=bind image_for_fanoos ;
    docker start container_for_fanoos ;
    docker exec -it -d -u root container_for_fanoos bash -c "cd /home/user8d0a0629178c48bdab52171a1f3b981d/fanoosCode; bash restOfInstall.sh; "

Using the above commands, first the basic environment is setup in a Docker 
container, then the rest of the install - particularly the time-consuming 
process of installing Z3 - is done in the background. Obvious caution should
be used when querying Docker, etc., prior to the install process finishing. 
Notice that, unlike the commands for AWS, these commands for Docker use the 
local version of the code (i.e., the code in this repository when you download 
it , whether that be today or years ago) as opposed to pulling the latest 
version of Fanoos's code available from GitHub.

^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^


^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^_^

ssh-rsa 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 abc@defg
