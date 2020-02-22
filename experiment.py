import sys
import pygame

RED = (255, 0, 0)
BLUE = (0,0,255)
class RunGame:
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


