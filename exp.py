import pygame

from draw import DisplayGame, DrawGrids, DrawItems, DrawAgents, DrawCostBox,\
    DrawInitialScreen, DrawScreen, DrawTextbox, DisplayText
from calculate import calculateCost, checkEffectiveClick, TransformCoord, CheckClickedReturn
from experiment import RunGame


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

screenWidth = 1100
screenHeight = 700
caption = "Comm Game"
displayGame = DisplayGame(screenWidth, screenHeight, caption, fullScreen=False)
game = displayGame()

numCharPerLine = 30
spacingFontSizeRatio = 3/2
displayText = DisplayText(game, numCharPerLine, spacingFontSizeRatio)
defaultFont = pygame.font.get_default_font()

instructionText = 'Welcome to the Game! Please press ''CONTINUE'' to start! Welcome to the Game! Please press ''CONTINUE'' to start!'
instructionBoxPos = (0, 0)
instructionSize = (screenWidth, screenHeight/3*2)
backgroundColor = WHITE
initialScreenFontName = defaultFont
initialScreenFontSize = 20
instructionTextColor = BLACK
drawInstructionText = DrawTextbox(game, displayText, instructionText, instructionBoxPos,
                                  instructionSize, backgroundColor, initialScreenFontName,
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

drawInitialScreen = DrawInitialScreen(game, backgroundColor, drawInstructionText, drawContinueButton)
checkClickedInitialContinue = CheckClickedReturn(buttonLoc, buttonSize)

numberOfGrids = 11
edgeSize = 20
gridSize = (screenHeight - edgeSize * 2) / numberOfGrids  # 60
lineColor = BLACK
lineWidth = 3
drawGrids = DrawGrids(game, numberOfGrids, gridSize, edgeSize, lineColor, lineWidth)

transformCoord = TransformCoord(gridSize, edgeSize)

blueFigure = pygame.image.load("blueFigure.png")
redFigure = pygame.image.load("redFigure.png")
drawAgents = DrawAgents(game, transformCoord, redFigure, blueFigure)

signalsSize = gridSize - lineWidth * 2
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
costNumberCenterPos = (costBoxPosX + costBoxWidth / 2, costBoxPosY + costBoxHeight / 3 * 2)
drawCostBox = DrawCostBox(game, displayText, costText, costBoxPos, costBoxSize, lineColor, lineWidth,
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

blueMouse = pygame.image.load("BlueMouse.png").convert_alpha()
redMouse = pygame.image.load("RedMouse.png").convert_alpha()
drawScreen = DrawScreen(game, drawGrids, drawAgents, drawSignal, drawTarget, drawCostBox, drawReturnBox,
                        redMouse, blueMouse, backgroundColor)

checkClickedReturn = CheckClickedReturn(returnBoxPos, returnBoxSize)


trueGoalIndex = 0
agentsCoord = [(6, 11), (6, 1)]  # , signaler vs receiver

signalsCoord = [(2, 10), (10, 10)]
signalsShape = ['square', 'square']
signalsColor = [(255, 191, 0), (255, 191, 0)]

targetsCoord = [(1, 1), (11, 1), (6, 6)]
targetsColor = [(133, 222, 2), (133, 222, 2), (178, 132, 190)]
targetsShape = ['circle', 'square', 'circle']


runGame = RunGame(game, edgeSize, trueGoalIndex, agentsCoord, gridSize,
                 signalsColor, signalsShape, signalsCoord, targetsColor, targetsShape, targetsCoord,
                 displayGame, drawInitialScreen, drawScreen, calculateCost, drawCostBox,
                 checkEffectiveClick, checkClickedReturn, checkClickedInitialContinue, transformCoord)
runGame()

