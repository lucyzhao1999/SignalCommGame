import pygame
import sys
import os

sys.path.append(os.path.join('..'))
from src.draw import DisplayGame, DrawGrids, DrawItems, DrawAgent, DrawCostBox, \
    DrawInitialScreen, DrawScreen, DrawTextbox, DisplayText, DrawShade

from src.calculate import calculateCost, TransformCoord, StayWithinBoundary
from src.experiment import RunSignalerGame, MoveAgent

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (255, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0,0,255)

screenWidth = 1100
screenHeight = 700
caption = "Signal Game"
displayGame = DisplayGame(screenWidth, screenHeight, caption, fullScreen=False)
game = displayGame()

numCharPerLine = 30
spacingFontSizeRatio = 3 / 2
displayText = DisplayText(game, numCharPerLine, spacingFontSizeRatio)

instructionText = 'Welcome to the Game! Please press any key to start!'
instructionBoxPos = (0, 0)
instructionSize = (screenWidth, screenHeight / 3 * 2)
textboxColor = WHITE
defaultFont = pygame.font.get_default_font()
initialScreenFontName = defaultFont
initialScreenFontSize = 20
instructionTextColor = BLACK
drawInstructionText = DrawTextbox(game, displayText, instructionText, instructionBoxPos,
                                  instructionSize, textboxColor, initialScreenFontName,
                                  initialScreenFontSize, instructionTextColor)

backgroundColor = WHITE
drawInitialScreen = DrawInitialScreen(game, backgroundColor, drawInstructionText)

# main display
numberOfGrids = 11
edgeSize = 20
gridSize = (screenHeight - edgeSize * 2) / numberOfGrids  # 60
transformCoord = TransformCoord(gridSize, edgeSize)

drawShade = DrawShade(game, transformCoord, gridSize)

lineColor = BLACK
lineWidth = 3
shadeColor = (0, 0, 0, 50)
shadeHeight = 5
drawGrids = DrawGrids(game, drawShade, numberOfGrids, gridSize, edgeSize, lineColor, lineWidth, shadeHeight)

signalsSize = 40
drawSignal = DrawItems(game, transformCoord, signalsSize)
targetsSize = 40
drawTarget = DrawItems(game, transformCoord, targetsSize)

costText = 'The cost of this movement = '
costBoxSignalerPosX = 700
costBoxSignalerPosY = edgeSize
costBoxSignalerPos = (costBoxSignalerPosX, costBoxSignalerPosY)
costBoxWidth = 350
costBoxHeight = 75
costBoxSize = (costBoxWidth, costBoxHeight)
costBoxFontName = defaultFont
costBoxFontSize = 15
costTextColor = BLACK
costTextSignalerCenter = (costBoxSignalerPosX + costBoxWidth / 2, costBoxSignalerPosY + costBoxHeight / 3)
costNumberCenterSignalerPos = (costBoxSignalerPosX + costBoxWidth / 2, costBoxSignalerPosY + costBoxHeight / 3 * 2)

drawSignalerCostBox = DrawCostBox(game, displayText, costText, costTextSignalerCenter, costBoxSignalerPos, costBoxSize, lineColor, lineWidth,
                          costBoxFontName, costBoxFontSize, costTextColor, costNumberCenterSignalerPos)


costBoxReceiverPosX = costBoxSignalerPosX
costBoxReceiverPosY = costBoxSignalerPosY + costBoxHeight + edgeSize
costBoxReceiverPos = (costBoxReceiverPosX, costBoxReceiverPosY)
costTextReceiverCenter = (costBoxReceiverPosX + costBoxWidth / 2, costBoxReceiverPosY + costBoxHeight / 3)
costNumberCenterReceiverPos = (costBoxReceiverPosX + costBoxWidth / 2, costBoxReceiverPosY + costBoxHeight / 3 * 2)

drawReceiverCostBox = DrawCostBox(game, displayText, costText, costTextReceiverCenter, costBoxReceiverPos, costBoxSize, lineColor, lineWidth,
                          costBoxFontName, costBoxFontSize, costTextColor, costNumberCenterReceiverPos)


blueFigure = pygame.image.load('../figures/blueFigure.png')
redFigure = pygame.image.load('../figures/redFigure.png')
drawSignaler = DrawAgent(game, transformCoord, redFigure)
drawReceiver = DrawAgent(game, transformCoord, blueFigure)

drawScreen = DrawScreen(game, drawGrids, drawSignal, drawTarget, backgroundColor)

# experiment manipulation
agentsCoord = [(6, 11), (6, 1)]  # signaler vs receiver

signalsCoord = [(2, 10), (10, 10)]
signalsShape = ['triangle', 'square']
signalsColor = [None, GREEN]

targetsCoord = [(1, 1), (11, 1), (6, 6)]
targetsColor = [GREEN, PURPLE, GREEN]
targetsShape = ['triangle', 'circle', 'circle']
trueGoalIndex = 0

gridCoordMinValue = 1
stayWithinBoundary = StayWithinBoundary(gridCoordMinValue, numberOfGrids)

moveAgent = MoveAgent(stayWithinBoundary)

runGame = RunSignalerGame(game, trueGoalIndex, agentsCoord,
                 signalsColor, signalsShape, signalsCoord,
                 targetsColor, targetsShape, targetsCoord,
                 displayGame, drawInitialScreen, drawScreen, drawSignaler, drawReceiver, calculateCost,
                drawSignalerCostBox, drawReceiverCostBox,
                 moveAgent, drawShade)

receiverTrajectory = [(6,1), (5,1), (4,1), (4,2), (3,2), (2,2), (1,2), (1,1)]
runGame(receiverTrajectory)

