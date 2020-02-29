import sys
import pygame

RED = (255, 0, 0)
BLUE = (0,0,255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (255, 0, 255)
GREEN = (0, 255, 0)


def checkEffectiveClick(gridUpperLeftXPos, gridUpperLeftYPos, gridSize):
    mouse_pos = pygame.mouse.get_pos()
    grid = (gridUpperLeftXPos, gridUpperLeftYPos, gridSize, gridSize)
    return pygame.Rect(grid).collidepoint(mouse_pos[0], mouse_pos[1])


class CheckClickedReturn:
    def __init__(self,returnBoxUpperLeftLoc, boxSize):
        self.returnBoxUpperLeftLoc = returnBoxUpperLeftLoc
        self.boxSize = boxSize

    def __call__(self):
        mouse_pos = pygame.mouse.get_pos()
        grid = self.returnBoxUpperLeftLoc + self.boxSize
        return pygame.Rect(grid).collidepoint(mouse_pos[0], mouse_pos[1])


class RunClickGame:
    def __init__(self, game, edgeSize, trueGoalIndex, agentsCoord, gridSize,
                 signalsColor, signalsShape, signalsCoord, targetsColor, targetsShape, targetsCoord,
                 displayGame, drawInitialScreen, drawScreen, calculateCost, drawCostBox,
                 checkEffectiveClick, checkClickedReturn, checkClickedInitialContinue, transformCoord,
                 FPS = 60,
                 indicatingBoxLineWidth = 3,
                 signalerColor = RED,
                 receiverColor = BLUE):
        self.game = game
        self.edgeSize = edgeSize

        self.trueGoalIndex = trueGoalIndex  # 0 or 1 or 2
        self.agentsCoord = agentsCoord  # [(5, 11), (5,1)] , signaler, receiver
        self.gridSize = gridSize

        self.targetsCoord = targetsCoord  # [(1, 1), (11, 1), (5, 5)]
        self.targetsColor = targetsColor
        self.targetsShape = targetsShape

        self.signalsCoord = signalsCoord  # [(2,11), (8, 11)]
        self.signalsColor = signalsColor
        self.signalsShape = signalsShape

        self.displayGame = displayGame
        self.drawInitialScreen = drawInitialScreen
        self.drawScreen = drawScreen
        self.calculateCost= calculateCost
        self.drawCostBox = drawCostBox

        self.checkEffectiveClick = checkEffectiveClick
        self.checkClickedReturn = checkClickedReturn
        self.checkClickedInitialContinue = checkClickedInitialContinue
        self.transformCoord = transformCoord

        self.FPS = FPS
        self.indicatingBoxLineWidth = indicatingBoxLineWidth
        self.signalerColor = signalerColor
        self.receiverColor = receiverColor

    def __call__(self):
        enterGame = False
        waitForInstruction = True
        fpsClock = pygame.time.Clock()

        while waitForInstruction:
            fpsClock.tick(self.FPS)
            self.drawInitialScreen()

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
            fpsClock.tick(self.FPS)
            pygame.mouse.set_visible(False)

            currentAgent = 'signaler'

            signalerFrame = 0
            receiverFrame = 0

            signalerSelected = False
            receiverSelected = False

            signalerSelectedBoxX = 0
            signalerSelectedBoxY = 0
            receiverSelectedBoxX = 0
            receiverSelectedBoxY = 0

            signalerCoord = self.agentsCoord[0]
            receiverCoord = self.agentsCoord[1]

            trueGoalLoc = self.targetsCoord[self.trueGoalIndex]

            signalerFinalSelection = (0,0)
            receiverFinalSelection = (0,0)

            signalerStartTime = 0
            receiverStartTime = 0

            signalerChosenBox = (0,0)
            receiverChosenBox = (0,0)

            signalerActionOptions = self.targetsCoord + self.signalsCoord
            receiverActionOptions = self.targetsCoord

            while True:
                self.drawScreen(currentAgent, self.agentsCoord, self.signalsColor, self.signalsShape,
                                self.signalsCoord, self.targetsColor, self.targetsShape, self.targetsCoord)

                if currentAgent is 'signaler':
                    if signalerFrame is 0:
                        signalerStartTime = pygame.time.get_ticks() # time when the frame first shown

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()

                        for effectiveGrid in signalerActionOptions:
                            effectiveGridUpperLeftXPos, effectiveGridUpperLeftYPos = self.transformCoord(effectiveGrid)
                            clickedEffectiveGrid = self.checkEffectiveClick(effectiveGridUpperLeftXPos, effectiveGridUpperLeftYPos,
                                                                      self.gridSize)
                            signalerClickedReturn = self.checkClickedReturn()

                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if clickedEffectiveGrid:  # a box is pressed
                                    signalerSelectedBoxX = effectiveGridUpperLeftXPos
                                    signalerSelectedBoxY = effectiveGridUpperLeftYPos
                                    signalerChosenBox = effectiveGrid
                                    signalerSelected = True

                                if signalerSelected and signalerClickedReturn:
                                    signalerResponseTime = pygame.time.get_ticks() - signalerStartTime
                                    signalerFinalSelection = signalerChosenBox

                                    if signalerFinalSelection is trueGoalLoc:
                                        print('Signaler Selection: ' + str(signalerFinalSelection))
                                        print('signalerResponseTime ' + str(signalerResponseTime))
                                        pygame.quit()
                                        sys.exit()
                                    else:
                                        currentAgent = 'receiver'

                    if signalerSelected:
                        pygame.draw.rect(self.game, self.signalerColor, (signalerSelectedBoxX + self.indicatingBoxLineWidth,
                                                                         signalerSelectedBoxY + self.indicatingBoxLineWidth,
                                                                         self.gridSize - 2*self.indicatingBoxLineWidth,
                                                                         self.gridSize - 2*self.indicatingBoxLineWidth),self.indicatingBoxLineWidth)
                        signalerCost = self.calculateCost(signalerCoord, signalerChosenBox)
                        self.drawCostBox(signalerCost)

                    pygame.display.update()
                    signalerFrame = signalerFrame + 1

                else:
                    if receiverFrame is 0:
                        receiverStartTime = pygame.time.get_ticks()

                    self.drawScreen(currentAgent, self.agentsCoord, self.signalsColor,
                                    self.signalsShape, self.signalsCoord, self.targetsColor,self.targetsShape, self.targetsCoord)
                    pygame.draw.rect(self.game, self.signalerColor,(signalerSelectedBoxX + 3, signalerSelectedBoxY + 3, self.gridSize - 6, self.gridSize - 6),4)  # line width

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()

                        for effectiveGrid in receiverActionOptions:
                            effectiveGridUpperLeftXPos, effectiveGridUpperLeftYPos = self.transformCoord(effectiveGrid)
                            clickedEffectiveGrid = self.checkEffectiveClick(effectiveGridUpperLeftXPos, effectiveGridUpperLeftYPos,
                                                                      self.gridSize)
                            receiverClickedReturn = self.checkClickedReturn()

                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if clickedEffectiveGrid:  # a box is pressed
                                    receiverSelectedBoxX = effectiveGridUpperLeftXPos
                                    receiverSelectedBoxY = effectiveGridUpperLeftYPos
                                    receiverChosenBox = effectiveGrid
                                    receiverSelected = True

                                if receiverSelected and receiverClickedReturn:
                                    receiverResponseTime = pygame.time.get_ticks() - receiverStartTime
                                    receiverFinalSelection = receiverChosenBox
                                    print('Signaler Selection: ' + str(signalerFinalSelection))
                                    print('Receiver Selection: ' + str(receiverFinalSelection))
                                    print('signalerResponseTime ' + str(signalerResponseTime))
                                    print('receiverResponseTime ' + str(receiverResponseTime))
                                    pygame.quit()
                                    sys.exit()

                    if receiverSelected:
                        pygame.draw.rect(self.game, self.receiverColor, (receiverSelectedBoxX + self.indicatingBoxLineWidth,
                                                                         receiverSelectedBoxY + self.indicatingBoxLineWidth,
                                                                         self.gridSize - 2*self.indicatingBoxLineWidth,
                                                                         self.gridSize - 2*self.indicatingBoxLineWidth),self.indicatingBoxLineWidth)

                        receiverCost = self.calculateCost(receiverCoord, receiverChosenBox)
                        self.drawCostBox(receiverCost)

                    receiverFrame = receiverFrame + 1
                    pygame.display.update()


class MoveAgent:
    def __init__(self, stayWithinBoundary):
        self.stayWithinBoundary = stayWithinBoundary

    def __call__(self, subjectAction, currentPosition):
        currentX, currentY = currentPosition
        if subjectAction == pygame.K_UP:
            currentY -= 1

        if subjectAction == pygame.K_DOWN:
            currentY += 1

        if subjectAction == pygame.K_LEFT:
            currentX -= 1

        if subjectAction == pygame.K_RIGHT:
            currentX += 1

        signalerCoord = self.stayWithinBoundary((currentX, currentY))
        return signalerCoord


class RunReceiverGame:
    def __init__(self, game, trueGoalIndex, agentsCoord,signalsColor, signalsShape, signalsCoord,
                 targetsColor, targetsShape, targetsCoord,
                 displayGame, drawInitialScreen, drawScreen, drawSignaler, drawReceiver, calculateCost,
                 drawSignalerCostBox, drawReceiverCostBox,
                 moveAgent, drawShade,
                 signalerColor=RED, receiverColor=BLUE, FPS=60, movementLag = 5
                 ):
        self.game = game

        self.trueGoalIndex = trueGoalIndex  # 0 or 1 or 2
        self.agentsCoord = agentsCoord  # [(5, 11), (5,1)] , signaler, receiver

        self.targetsCoord = targetsCoord  # [(1, 1), (11, 1), (5, 5)]
        self.targetsColor = targetsColor
        self.targetsShape = targetsShape

        self.signalsCoord = signalsCoord  # [(2,11), (8, 11)]
        self.signalsColor = signalsColor
        self.signalsShape = signalsShape

        self.displayGame = displayGame
        self.drawInitialScreen = drawInitialScreen
        self.drawScreen = drawScreen
        self.drawSignaler = drawSignaler
        self.drawReceiver = drawReceiver

        self.calculateCost = calculateCost

        self.drawSignalerCostBox = drawSignalerCostBox
        self.drawReceiverCostBox = drawReceiverCostBox

        self.drawShade = drawShade

        self.FPS = FPS
        self.signalerColor = signalerColor
        self.receiverColor = receiverColor

        self.moveAgent = moveAgent
        self.movementLag = movementLag

    def __call__(self, signalerTrajectory):
        signalerInitialCoord, receiverInitialCoord = self.agentsCoord
        receiverCoord = receiverInitialCoord

        enterGame = False
        waitForInstruction = True
        fpsClock = pygame.time.Clock()

        currentAgent = 'signaler'

        signalerFrame = 0
        receiverFrame = 0

        trueGoalLoc = self.targetsCoord[self.trueGoalIndex]
        receiverActionOptions = self.targetsCoord

        signalerRound = True

        signalerWaitIndex = 0
        receiverCost = 0

        signalerCost = 0

        while waitForInstruction:
            fpsClock.tick(self.FPS)
            self.drawInitialScreen()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    waitForInstruction = False
                    enterGame = True

            pygame.display.update()

        while enterGame:
            fpsClock.tick(self.FPS)
            if signalerRound:
                self.drawScreen(currentAgent, self.signalsColor, self.signalsShape,
                                self.signalsCoord, self.targetsColor, self.targetsShape, self.targetsCoord)

                self.drawReceiver(receiverInitialCoord)

                currentSignalerCoord = signalerTrajectory[signalerFrame]
                self.drawSignaler(currentSignalerCoord)
                signalerCost = self.calculateCost(currentSignalerCoord, signalerInitialCoord)
                self.drawSignalerCostBox(signalerCost)


                if signalerFrame is len(signalerTrajectory)-1:
                    self.drawShade(currentSignalerCoord, self.signalerColor)
                    if signalerWaitIndex is self.movementLag - 1:
                        signalerRound = False
                        currentAgent = 'receiver'

                signalerWaitIndex +=1
                if signalerWaitIndex is self.movementLag:
                    signalerWaitIndex = 0
                    signalerFrame +=1

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

            else:
                self.drawScreen(currentAgent, self.signalsColor, self.signalsShape,
                                self.signalsCoord, self.targetsColor, self.targetsShape, self.targetsCoord)
                self.drawSignalerCostBox(signalerCost)
                self.drawShade(currentSignalerCoord, self.signalerColor)

                if receiverFrame is 0:
                    receiverStartTime = pygame.time.get_ticks()  # time when the frame first shown

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.KEYDOWN:
                        subjectAction = event.key
                        receiverCoord = self.moveAgent(subjectAction, receiverCoord)
                        receiverCost = self.calculateCost(receiverCoord, receiverInitialCoord)

                        if subjectAction == pygame.K_RETURN:
                            chosenEffectiveBox = receiverCoord in receiverActionOptions
                            if chosenEffectiveBox:
                                receiverFinalSelection = receiverCoord
                                receiverResponseTime = pygame.time.get_ticks() - receiverStartTime

                                print('Signaler Selection: ' + str(receiverFinalSelection))
                                print('signalerResponseTime ' + str(receiverResponseTime))

                                pygame.quit()
                                sys.exit()

                self.drawReceiverCostBox(receiverCost)
                self.drawReceiver(receiverCoord)

                onEffectiveGrid = receiverCoord in receiverActionOptions
                if onEffectiveGrid:
                    self.drawShade(receiverCoord, self.receiverColor)

                receiverFrame +=1

            pygame.display.update()



class RunSignalerGame:
    def __init__(self, game, trueGoalIndex, agentsCoord,signalsColor, signalsShape, signalsCoord,
                 targetsColor, targetsShape, targetsCoord,
                 displayGame, drawInitialScreen, drawScreen, drawSignaler, drawReceiver, calculateCost,
                 drawSignalerCostBox, drawReceiverCostBox,
                 moveAgent, drawShade,
                 signalerColor=RED, receiverColor=BLUE, FPS=60, movementLag = 5
                 ):
        self.game = game

        self.trueGoalIndex = trueGoalIndex  # 0 or 1 or 2
        self.agentsCoord = agentsCoord  # [(5, 11), (5,1)] , signaler, receiver

        self.targetsCoord = targetsCoord  # [(1, 1), (11, 1), (5, 5)]
        self.targetsColor = targetsColor
        self.targetsShape = targetsShape

        self.signalsCoord = signalsCoord  # [(2,11), (8, 11)]
        self.signalsColor = signalsColor
        self.signalsShape = signalsShape

        self.displayGame = displayGame
        self.drawInitialScreen = drawInitialScreen
        self.drawScreen = drawScreen
        self.drawSignaler = drawSignaler
        self.drawReceiver = drawReceiver

        self.calculateCost = calculateCost
        self.drawSignalerCostBox = drawSignalerCostBox
        self.drawReceiverCostBox = drawReceiverCostBox

        self.drawShade = drawShade

        self.FPS = FPS
        self.signalerColor = signalerColor
        self.receiverColor = receiverColor

        self.moveAgent = moveAgent
        self.movementLag = movementLag

    def __call__(self, receiverTrajectory):
        signalerInitialCoord, receiverInitialCoord = self.agentsCoord
        signalerCoord = signalerInitialCoord

        enterGame = False
        waitForInstruction = True
        fpsClock = pygame.time.Clock()

        currentAgent = 'signaler'

        signalerFrame = 0
        receiverFrame = 0

        trueGoalLoc = self.targetsCoord[self.trueGoalIndex]
        signalerActionOptions = self.targetsCoord + self.signalsCoord


        signalerRound = True
        signalerCost = 0
        receiverWaitIndex = 0
        while waitForInstruction:
            fpsClock.tick(self.FPS)
            self.drawInitialScreen()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    waitForInstruction = False
                    enterGame = True

            pygame.display.update()


        while enterGame:
            fpsClock.tick(self.FPS)

            if signalerRound:
                self.drawScreen(currentAgent, self.signalsColor, self.signalsShape,
                                self.signalsCoord, self.targetsColor, self.targetsShape, self.targetsCoord)
                self.drawReceiver(receiverInitialCoord)

                if signalerFrame is 0:
                    signalerStartTime = pygame.time.get_ticks()  # time when the frame first shown

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.KEYDOWN:
                        subjectAction = event.key
                        signalerCoord = self.moveAgent(subjectAction, signalerCoord)
                        signalerCost = self.calculateCost(signalerCoord, signalerInitialCoord)

                        if subjectAction == pygame.K_RETURN:
                            chosenEffectiveBox = signalerCoord in signalerActionOptions
                            if chosenEffectiveBox:
                                signalerFinalSelection = signalerCoord
                                signalerResponseTime = pygame.time.get_ticks() - signalerStartTime

                                print('Signaler Selection: ' + str(signalerFinalSelection))
                                print('signalerResponseTime ' + str(signalerResponseTime))

                                if signalerFinalSelection is trueGoalLoc:
                                    pygame.quit()
                                    sys.exit()
                                else:
                                    signalerRound = False

                self.drawSignaler(signalerCoord)
                self.drawSignalerCostBox(signalerCost)

                onEffectiveGrid = signalerCoord in signalerActionOptions
                if onEffectiveGrid:
                    self.drawShade(signalerCoord, self.signalerColor)

                signalerFrame += 1

            else:
                currentAgent = 'receiver'
                self.drawScreen(currentAgent, self.signalsColor, self.signalsShape,
                                self.signalsCoord, self.targetsColor, self.targetsShape, self.targetsCoord)
                self.drawSignaler(signalerCoord)
                self.drawShade(signalerCoord, self.signalerColor)
                self.drawSignalerCostBox(signalerCost)

                currentReceiverCoord = receiverTrajectory[receiverFrame]
                self.drawReceiver(currentReceiverCoord)

                receiverCost = self.calculateCost(currentReceiverCoord, receiverInitialCoord)
                self.drawReceiverCostBox(receiverCost)

                if receiverFrame is len(receiverTrajectory)-1:
                    self.drawShade(currentReceiverCoord, self.receiverColor)
                    if receiverWaitIndex is self.movementLag - 1:
                        pygame.quit()
                        sys.exit()

                receiverWaitIndex +=1
                if receiverWaitIndex is self.movementLag:
                    receiverWaitIndex = 0
                    receiverFrame +=1

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

            pygame.display.update()



