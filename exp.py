import sys
import pygame

from draw import DisplayGame, DrawGrids, DrawItems, TransformCoord, DrawAgents, DrawCostBox,\
    DrawInitialScreen, DrawScreen, DrawTextbox, DisplayText

from calculate import calculateCost, checkEffectiveClick, CheckClickedReturn


class RunGame:
    def __init__(self, edgeSize,trueGoalIndex, agentsCoord,
                 signalsColor, signalsShape, signalsCoord, targetsColor, targetsShape, targetsCoord,
                 displayGame, drawInitialScreen, drawScreen,
                 checkEffectiveClick, checkClickedReturn, checkClickedInitialContinue):

        self.edgeSize = edgeSize

        self.trueGoalIndex = trueGoalIndex  # 0 or 1 or 2
        self.agentsCoord = agentsCoord  # [(5, 11), (5,1)] , signaler vs receiver

        self.targetsCoord = targetsCoord  # [(1, 1), (11, 1), (5, 5)]
        self.targetsColor = targetsColor
        self.targetsShape = targetsShape

        self.signalsCoord = signalsCoord  # [(2,11), (8, 11)]
        self.signalsColor = signalsColor
        self.signalsShape = signalsShape

        self.displayGame = displayGame
        self.drawInitialScreen = drawInitialScreen
        self.drawScreen = drawScreen

        self.checkEffectiveClick = checkEffectiveClick
        self.checkClickedReturn = checkClickedReturn
        self.checkClickedInitialContinue = checkClickedInitialContinue

    def __call__(self):
        game = self.displayGame()
        enterGame = False
        waitForInstruction = True
        while waitForInstruction:
            self.drawInitialScreen(game)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                clickedContinue = self.checkClickedInitialContinue()

                if event.type == pygame.MOUSEBUTTONDOWN and clickedContinue:
                    waitForInstruction = False
                    enterGame = True

            pygame.display.update()

        while enterGame:
            pygame.mouse.set_visible(False)

            currentAgent = 'signaler'
            fpsClock = pygame.time.Clock()

            signalerFrame = 0
            receiverFrame = 0

            signalerSelected = False
            receiverSelected = False

            signalerSelectedBoxX = 0
            signalerSelectedBoxY = 0
            receiverSelectedBoxX = 0
            receiverSelectedBoxY = 0

            signalerCoord = agentsCoord[0]
            receiverCoord = agentsCoord[1]

            trueGoalLoc = self.targetsCoord[self.trueGoalIndex]

            signalerFinalSelection = (0,0)
            receiverFinalSelection = (0,0)

            signalerStartTime = 0
            receiverStartTime = 0

            signalerChosenBox = (0,0)
            receiverChosenBox = (0,0)

            while True:
                fpsClock.tick(60)

                game = self.drawScreen(game, currentAgent, self.agentsCoord, self.signalsColor, self.signalsShape,
                                                 self.signalsCoord, self.targetsColor, self.targetsShape, self.targetsCoord)

                if currentAgent is 'signaler':

                    if signalerFrame is 0:
                        signalerStartTime = pygame.time.get_ticks() # time when the frame first shown

                    signalerActionOptions = self.targetsCoord + self.signalsCoord
                    signalerChoicesX = [self.edgeSize + (xCoord - 1) * gridSize for xCoord, yCoord in signalerActionOptions]
                    signalerChoicesY = [self.edgeSize + (yCoord - 1) * gridSize for xCoord, yCoord in signalerActionOptions]

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()

                        for effectiveGridNumber in range(len(signalerChoicesX)):
                            gridUpperLeftXPos = signalerChoicesX[effectiveGridNumber]
                            gridUpperLeftYPos = signalerChoicesY[effectiveGridNumber]

                            clickedBox = signalerActionOptions[effectiveGridNumber]
                            signalerClickedReturn = self.checkClickedReturn()

                            effectiveClick = self.checkEffectiveClick(gridUpperLeftXPos, gridUpperLeftYPos, gridSize)

                            if event.type == pygame.MOUSEBUTTONDOWN and effectiveClick:  # a box is pressed
                                signalerSelectedBoxX = gridUpperLeftXPos
                                signalerSelectedBoxY = gridUpperLeftYPos
                                signalerChosenBox = clickedBox
                                signalerSelected = True

                            if event.type == pygame.MOUSEBUTTONDOWN and signalerClickedReturn and signalerSelected:
                                signalerResponseTime = pygame.time.get_ticks() - signalerStartTime
                                signalerFinalSelection = signalerChosenBox

                                if signalerChosenBox is trueGoalLoc:
                                    print('signalerResponseTime ' + str(signalerResponseTime))
                                    pygame.quit()
                                    sys.exit()
                                else:
                                    currentAgent = 'receiver'

                    if signalerSelected:
                        game = self.drawScreen(game, currentAgent, self.agentsCoord, self.signalsColor, self.signalsShape,
                                               self.signalsCoord, self.targetsColor, self.targetsShape, self.targetsCoord)
                        indicatingBoxColor = (255, 0, 0)
                        pygame.draw.rect(game, indicatingBoxColor, (signalerSelectedBoxX + 3, signalerSelectedBoxY + 3, gridSize - 6, gridSize - 6),4)
                        signalerCost = calculateCost(signalerCoord, signalerChosenBox)
                        drawCostBox(game, signalerCost)

                    pygame.display.update()
                    signalerFrame = signalerFrame + 1

                else:
                    if receiverFrame is 0:
                        receiverStartTime = pygame.time.get_ticks()

                    game = self.drawScreen(game, currentAgent, self.agentsCoord, self.signalsColor,
                                                     self.signalsShape, self.signalsCoord, self.targetsColor,self.targetsShape, self.targetsCoord)
                    pygame.draw.rect(game, (255, 0, 0),(signalerSelectedBoxX + 3, signalerSelectedBoxY + 3, gridSize - 6, gridSize - 6),4)  # line width

                    receiverActionOptions = self.targetsCoord
                    receiverChoicesX = [self.edgeSize + (xCoord - 1) * gridSize for xCoord, yCoord in receiverActionOptions]
                    receiverChoicesY = [self.edgeSize + (yCoord - 1) * gridSize for xCoord, yCoord in receiverActionOptions]

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()

                        for effectiveGridNumber in range(len(receiverChoicesX)):
                            gridUpperLeftXPos = receiverChoicesX[effectiveGridNumber]
                            gridUpperLeftYPos = receiverChoicesY[effectiveGridNumber]
                            clickedBox = receiverActionOptions[effectiveGridNumber]

                            effectiveClick = self.checkEffectiveClick(gridUpperLeftXPos, gridUpperLeftYPos, gridSize)
                            receiverClickedReturn = self.checkClickedReturn()

                            if event.type == pygame.MOUSEBUTTONDOWN and effectiveClick:  # a box is pressed
                                receiverSelectedBoxX = gridUpperLeftXPos
                                receiverSelectedBoxY = gridUpperLeftYPos
                                receiverChosenBox = clickedBox
                                receiverSelected = True

                            if event.type == pygame.MOUSEBUTTONDOWN and receiverClickedReturn and receiverSelected:
                                receiverResponseTime = pygame.time.get_ticks() - receiverStartTime
                                receiverFinalSelection = receiverChosenBox
                                print('Signaler Selection: ' + str(signalerFinalSelection))
                                print('Receiver Selection: ' + str(receiverFinalSelection))
                                print('signalerResponseTime ' + str(signalerResponseTime))
                                print('receiverResponseTime ' + str(receiverResponseTime))
                                pygame.quit()
                                sys.exit()

                    if receiverSelected:
                        game = self.drawScreen(game, currentAgent, self.agentsCoord, self.signalsColor, self.signalsShape,
                                               self.signalsCoord, self.targetsColor, self.targetsShape, self.targetsCoord)
                        indicatingBoxColor = (0, 0, 255)
                        pygame.draw.rect(game, indicatingBoxColor,
                                         (receiverSelectedBoxX + 3, receiverSelectedBoxY + 3, gridSize - 6, gridSize - 6),4)  # line width
                        receiverCost = calculateCost(receiverCoord, receiverChosenBox)
                        drawCostBox(game, receiverCost)

                    receiverFrame = receiverFrame + 1

                    pygame.display.update()
                    fpsClock.tick(60)



BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

screenWidth = 1100
screenHeight = 700
caption = "Comm Game"
displayGame = DisplayGame(screenWidth, screenHeight, caption)

numCharPerLine = 30
displayText = DisplayText(numCharPerLine)
defaultFont = pygame.font.get_default_font()

instructionText = 'Welcome to the Game! Please press ''CONTINUE'' to start! Welcome to the Game! Please press ''CONTINUE'' to start!'
instructionBoxPos = (0, 0)
instructionSize = (screenWidth, screenHeight/3*2)
backgroundColor = WHITE
initialScreenFontName = defaultFont
initialScreenFontSize = 20
instructionTextColor = BLACK
drawInstructionText = DrawTextbox(displayText, instructionText, instructionBoxPos,
                                  instructionSize, backgroundColor, initialScreenFontName,
                                  initialScreenFontSize, instructionTextColor)
buttonText = 'CONTINUE'
buttonLoc = (screenWidth/7*3, screenHeight/7*5)
buttonSize = (120, 30)
buttonBoxColor = BLACK
buttonFontName = defaultFont
buttonFontSize = 15
buttonTextColor = WHITE
drawContinueButton = DrawTextbox(displayText, buttonText, buttonLoc,
                                  buttonSize, buttonBoxColor, buttonFontName,
                                  buttonFontSize, buttonTextColor)

drawInitialScreen = DrawInitialScreen(backgroundColor, drawInstructionText, drawContinueButton)
checkClickedInitialContinue = CheckClickedReturn(buttonLoc, buttonSize)

numberOfGrids = 11
edgeSize = 20
gridSize = (screenHeight - edgeSize * 2) / numberOfGrids  # 60
lineColor = BLACK
lineWidth = 3
drawGrids = DrawGrids(numberOfGrids, gridSize, edgeSize, lineColor, lineWidth)

transformCoord = TransformCoord(gridSize, edgeSize)

blueFigure = pygame.image.load("blueFigure.png")
redFigure = pygame.image.load("redFigure.png")
drawAgents = DrawAgents(redFigure, blueFigure, transformCoord)

signalsSize = gridSize - lineWidth * 2
drawSignal = DrawItems(transformCoord, signalsSize)
targetsSize = 40
drawTarget = DrawItems(transformCoord, targetsSize)

costText = 'The cost of this movement = '
costBoxPos = (700, edgeSize)
costBoxSize = (350, 75)
costBoxFontName = defaultFont
costBoxFontSize = 15
costTextColor = BLACK
drawCostBox = DrawCostBox(displayText, costText, costBoxPos, costBoxSize, lineColor, lineWidth, costBoxFontName, costBoxFontSize, costTextColor)

returnText = 'CONFIRM'
returnBoxPos = (820, 120)
returnBoxSize = (100, 30)
returnBoxColor = BLACK
returnBoxFontName = defaultFont
returnBoxFontSize = 15
returnTextColor = WHITE
drawReturnBox = DrawTextbox(displayText, returnText, returnBoxPos, returnBoxSize, returnBoxColor, returnBoxFontName,
                            returnBoxFontSize, returnTextColor)

blueMouse = pygame.image.load("BlueMouse.png")
redMouse = pygame.image.load("RedMouse.png")
drawScreen = DrawScreen(drawGrids, drawAgents, drawSignal, drawTarget, drawCostBox, drawReturnBox,
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

runGame = RunGame(edgeSize, trueGoalIndex, agentsCoord, signalsColor, signalsShape, signalsCoord,
                  targetsColor, targetsShape, targetsCoord, displayGame, drawInitialScreen,
                  drawScreen, checkEffectiveClick, checkClickedReturn, checkClickedInitialContinue)

runGame()

