

import config;
_LOCALDEBUGFLAG = config.debugFlags.get_v_print_ForThisFile(__file__);
    
import config;

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
from boxesAndBoxOperations.getBox import *; 
from utils.contracts import *;


class drawBoxes():

    def __init__(self, axis1ToProjectOnto, axis2ToProjectOnto, universeBox):
        requires(isProperBox(universeBox));
        requires(isinstance(axis1ToProjectOnto, int));
        requires(isinstance(axis2ToProjectOnto, int));
        requires(axis1ToProjectOnto >= 0);
        requires(axis2ToProjectOnto >= 0);
        requires(axis1ToProjectOnto < getDimensionOfBox(universeBox));
        requires(axis2ToProjectOnto < getDimensionOfBox(universeBox));
        self.axis1ToProjectOnto = axis1ToProjectOnto;
        self.axis2ToProjectOnto = axis2ToProjectOnto;
        self.universeBox = universeBox;
        self.relavantSubVolumeOfUniverseBox = self.volumeOfBoxExcludingChosenAxis(self.universeBox);
        return;

    def convertBoxToPatch(self, thisBox):
        requires(isProperBox(thisBox));
        xVals = thisBox[self.axis1ToProjectOnto, :];
        assert(xVals[0] <= xVals[1]);
        yVals = thisBox[self.axis2ToProjectOnto, :];
        assert(yVals[0] <= yVals[1]);
        thisAlphaValue = self.volumeOfBoxExcludingChosenAxis(thisBox) / self.relavantSubVolumeOfUniverseBox;
        assert(thisAlphaValue >= 0.0);
        assert(thisAlphaValue <= 1.0);
        return Rectangle((xVals[0], yVals[0]), xVals[1] - xVals[0], yVals[1] - yVals[0], alpha=thisAlphaValue, ec=(0,0,0,1), linewidth=1.5,facecolor="g");

    @staticmethod
    def getPlotLimits(thisAxisIndex, theseBoxes):
        requires(hasattr(theseBoxes, '__iter__')); # checking it is iterable...
        requires(all([isProperBox(x) for x in theseBoxes]));
        requires(thisAxisIndex >= 0);
        requires(thisAxisIndex < getDimensionOfBox(theseBoxes[0]));
        minVal = np.min([thisBox[thisAxisIndex, 0] for thisBox in theseBoxes]);
        maxVal = np.max([thisBox[thisAxisIndex, 1] for thisBox in theseBoxes]);
        return (minVal, maxVal);
        
    def volumeOfBoxExcludingChosenAxis(self, thisBox):
        denominator = np.prod(np.diff(thisBox[[self.axis1ToProjectOnto, self.axis2ToProjectOnto], :], axis=1));
        if(np.isclose(denominator, 0.0)):
            return 0.0; 
        return np.prod(np.diff(thisBox, axis=1)) / np.prod(np.diff(thisBox[[self.axis1ToProjectOnto, self.axis2ToProjectOnto], :], axis=1));

    def setAxisLimits(self, ax, theseBoxes):
        requires(hasattr(theseBoxes, '__iter__')); # checking it is iterable...
        requires(all([isProperBox(x) for x in theseBoxes]));
        firstAxisLimits = self.getPlotLimits(self.axis1ToProjectOnto, theseBoxes);
        twoDotFivePercentOfRangeOfFirstAxis = 0.025 * (firstAxisLimits[1] - firstAxisLimits[0]);
        secondAxisLimits = self.getPlotLimits(self.axis2ToProjectOnto, theseBoxes);
        twoDotFivePercentOfRangeOfSecondAxis = 0.025 * (secondAxisLimits[1] - secondAxisLimits[0]);
        ax.set_xlim(firstAxisLimits[0] - twoDotFivePercentOfRangeOfFirstAxis, \
                    firstAxisLimits[1] + twoDotFivePercentOfRangeOfFirstAxis);
        ax.set_ylim(secondAxisLimits[0] - twoDotFivePercentOfRangeOfSecondAxis, \
                    secondAxisLimits[1] + twoDotFivePercentOfRangeOfSecondAxis);
        return;

    def drawBoxesOnAxis(self, ax, fig, theseBoxes, boxColors):
        requires(hasattr(theseBoxes, '__iter__')); # checking it is iterable...
        requires(all([isProperBox(x) for x in theseBoxes]));
        requires(hasattr(boxColors, '__iter__')); # checking it is iterable...
        requires(len(theseBoxes) == len(boxColors)); # probably not safe to check given the
            # weaker requirements above....
        requires(all([isinstance(x, str) for x in boxColors]));
        
        self.miniminumVolBox = np.min([self.volumeOfBoxExcludingChosenAxis(x) for x in theseBoxes]);

        boxesConvertedToPltRectangles = [];
        for thisBox in theseBoxes:
            boxesConvertedToPltRectangles.append(self.convertBoxToPatch(thisBox));

        [ax.add_artist(x) for x in boxesConvertedToPltRectangles];

        self.setAxisLimits(ax, theseBoxes);
        leftPadSize = (ax.get_xlim()[1] - ax.get_xlim()[0]) * 0.07;
        hieght = ax.get_ylim()[1] - ax.get_ylim()[0];
        leftX = ax.get_xlim()[0] - leftPadSize;
        alphaScale = [
             Rectangle((leftX, ax.get_ylim()[0] + x * hieght),\
             leftPadSize, hieght * 0.2, alpha=(x * 1.25), ec=(0,0,0,1), linewidth=1.5,facecolor="g")
             for x in \
             [0.0, 0.20, 0.4, 0.6, 0.8] ];
        [ax.add_artist(x) for x in alphaScale];
        [ax.text( (ax.get_xlim()[0] - leftPadSize * 0.66), (ax.get_ylim()[0] + (x + 0.1) * hieght), str((x * 1.25)) , rotation=90, fontsize=20) 
             for x in \
             [0.0, 0.20, 0.4, 0.6, 0.8] ];
        ax.set_xlim(ax.get_xlim()[0] - leftPadSize, ax.get_xlim()[1]);
        return;

from boxesAndBoxOperations.readAndWriteBoxes import readBoxes;
from CEGARLikeAnalysis import labelsForBoxes ;
from CEGARLikeAnalysis.labelsForBoxes import *;

def helper_frontEnd_drawBox(boxes):
    requires(all([isProperBox(x) for x in boxes]));

    """
ssh-rsa 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 abc@defg
"""

    # Below is a bit of a hack to allow for handling both the input and the output
    #     space boxes in a semi-sensible manner without having to shove the input-space
    #     box as a whole through the model we are trying to analyze. There is nothing wrong
    #     with that, it just would take more work and be a tangent to what we are trying to 
    #     do at the moment.
    universeBox = getBox(np.min(boxes, axis =0)[:, 0], np.max(boxes, axis=0)[:, 1]);
    print("apparent bounds on boxes:" + str(universeBox));

    colors = ['g' for index in boxes];


    maxIndex = getDimensionOfBox(universeBox);
    for firstIndex in range(0, maxIndex):
        for secondIndex in range(firstIndex + 1, maxIndex):
            if((firstIndex, secondIndex) != (0, 3)):
                continue;
            fig, ax = plt.subplots(1);
            plt.tick_params(labelsize=20)
            plt.xlabel('lread', fontsize=40);
            plt.ylabel('freemem', fontsize=40);
            DB = drawBoxes(firstIndex,secondIndex, universeBox);
            DB.drawBoxesOnAxis(ax, fig, boxes, colors);
            plt.show()

    return;


def frontEnd_drawBox(fileName):
    requires(isinstance(fileName, str));
    requires(len(fileName) > 0);

    tempFH = open(fileName, "rb");
    boxesToPlot = [x[0] for x in readBoxes(tempFH) if ((x[1][1] &  labelsForBoxes.LOWESTLEVEL_FALSESOMEWHEREANDEXHAUSTEDLOOKING) > 0)];
    tempFH.close();

    helper_frontEnd_drawBox(boxesToPlot);
    return;





