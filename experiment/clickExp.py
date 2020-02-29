import pygame

from src.draw import DisplayGame, DrawGrids, DrawItems, DrawAgents, DrawCostBox,\
    DrawClickInitialScreen, DrawClickScreen, DrawTextbox, DisplayText, DrawShade
from src.calculate import calculateCost, TransformCoord
from src.experiment import checkEffectiveClick, CheckClickedReturn, RunClickGame


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (255, 0, 255)
GREEN = (0, 255, 0)

screenWidth = 1100
screenHeight = 700
caption = "Signal Game"
displayGame = DisplayGame(screenWidth, screenHeight, caption, fullScreen=False)
game = displayGame()

numCharPerLine = 30
spacingFontSizeRatio = 3/2
displayText = DisplayText(game, numCharPerLine, spacingFontSizeRatio)

instructionText = 'Welcome to the Game! Please press ''CONTINUE'' to start! Welcome to the Game! Please press ''CONTINUE'' to start!'
instructionBoxPos = (0, 0)
instructionSize = (screenWidth, screenHeight/3*2)
textboxColor = WHITE
defaultFont = pygame.font.get_default_font()
initialScreenFontName = defaultFont
initialScreenFontSize = 20
instructionTextColor = BLACK
drawInstructionText = DrawTextbox(game, displayText, instructionText, instructionBoxPos,
                                  instructionSize, textboxColor, initialScreenFontName,
                                  initialScreenFontSize, instructionTextColor)
buttonText = 'CONTINUE'
buttonLoc = (screenWidth/7*3, screenHeight/7*5)
buttonSize = (120, 30)
buttonBoxColor = BLACK
buttonFontName = defaultFont
buttonFontSize = 15
buttonTextColor = WHITE
drawContinueButton = DrawTextbox(game, displayText, buttonText, buttonLoc,
                                  buttonSize, buttonBoxColor, buttonFontName,
                                  buttonFontSize, buttonTextColor)

backgroundColor = WHITE
drawInitialScreen = DrawClickInitialScreen(game, backgroundColor, drawInstructionText, drawContinueButton)

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

blueFigure = pygame.image.load('../figures/blueFigure.png')
redFigure = pygame.image.load('../figures/redFigure.png')
drawAgents = DrawAgents(game, transformCoord, redFigure, blueFigure)

signalsSize = 40
drawSignal = DrawItems(game, transformCoord, signalsSize)
targetsSize = 40
drawTarget = DrawItems(game, transformCoord, targetsSize)

costText = 'The cost of this movement = '
costBoxPosX = 700
costBoxPosY = edgeSize
costBoxPos = (costBoxPosX, costBoxPosY)
costBoxWidth = 350
costBoxHeight = 75
costBoxSize = (costBoxWidth, costBoxHeight)
costBoxFontName = defaultFont
costBoxFontSize = 15
costTextColor = BLACK
costTextCenter = (costBoxPosX + costBoxWidth/2, costBoxPosY + costBoxHeight/3)
costNumberCenterPos = (costBoxPosX + costBoxWidth / 2, costBoxPosY + costBoxHeight / 3 * 2)

drawCostBox = DrawCostBox(game, displayText, costText, costTextCenter, costBoxPos, costBoxSize, lineColor, lineWidth,
                          costBoxFontName, costBoxFontSize, costTextColor, costNumberCenterPos)

returnText = 'CONFIRM'
returnBoxPos = (820, 120)
returnBoxSize = (100, 30)
returnBoxColor = BLACK
returnBoxFontName = defaultFont
returnBoxFontSize = 15
returnTextColor = WHITE
drawReturnBox = DrawTextbox(game, displayText, returnText, returnBoxPos, returnBoxSize, returnBoxColor, returnBoxFontName,
                            returnBoxFontSize, returnTextColor)

blueMouse = pygame.image.load('../figures/BlueMouse.png').convert_alpha()
redMouse = pygame.image.load('../figures/RedMouse.png').convert_alpha()
drawScreen = DrawClickScreen(game, drawGrids, drawAgents, drawSignal, drawTarget, drawCostBox, drawReturnBox,
                        redMouse, blueMouse, backgroundColor)

# experiment manipulation
agentsCoord = [(6, 11), (6, 1)]  # signaler vs receiver

signalsCoord = [(2, 10), (10, 10)]
signalsShape = ['triangle', 'square']
signalsColor = [None, GREEN]

targetsCoord = [(1, 1), (11, 1), (6, 6)]
targetsColor = [GREEN, PURPLE, GREEN]
targetsShape = ['triangle', 'circle', 'circle']
trueGoalIndex = 0

checkClickedInitialContinue = CheckClickedReturn(buttonLoc, buttonSize)
checkClickedReturn = CheckClickedReturn(returnBoxPos, returnBoxSize)

runGame = RunClickGame(game, edgeSize, trueGoalIndex, agentsCoord, gridSize,
                 signalsColor, signalsShape, signalsCoord, targetsColor, targetsShape, targetsCoord,
                 displayGame, drawInitialScreen, drawScreen, calculateCost, drawCostBox,
                 checkEffectiveClick, checkClickedReturn, checkClickedInitialContinue, transformCoord)
runGame()