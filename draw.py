import pygame


class DisplayGame:
    def __init__(self, screenWidth, screenHeight, caption):
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.caption = caption

    def __call__(self):
        pygame.init()
        game = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        pygame.display.set_caption(self.caption)
        return game


class DrawGrids:
    def __init__(self, numberOfGrids, gridSize, edgeSize, lineColor, lineWidth):
        self.numberOfGrids = numberOfGrids
        self.gridSize = gridSize
        self.edgeSize = edgeSize
        self.lineColor = lineColor
        self.lineWidth = lineWidth

    def __call__(self, game):
        for i in range(self.numberOfGrids + 1):  # draw grids
            pygame.draw.line(game, self.lineColor, (self.edgeSize, self.edgeSize + i * self.gridSize),
                             (self.edgeSize + self.numberOfGrids * self.gridSize, self.edgeSize + i * self.gridSize),self.lineWidth)  # horizontalLine
            pygame.draw.line(game, self.lineColor, (self.edgeSize + i * self.gridSize, self.edgeSize),
                             (self.edgeSize + i * self.gridSize, self.edgeSize + self.numberOfGrids * self.gridSize), self.lineWidth)  # verticalLine
        return game


class DrawItems:
    def __init__(self, transformCoord, itemsSize):
        self.transformCoord = transformCoord
        self.itemsSize = itemsSize

    def __call__(self, game, colorList, shapeList, coordList):
        for i in range(len(colorList)):
            currentColor = colorList[i]
            centerCoord = self.transformCoord(coordList[i], center=True)
            radius = int(self.itemsSize / 2)

            if shapeList[i] == 'circle':
                pygame.draw.circle(game, currentColor, centerCoord, radius)

            if shapeList[i] == 'square':
                upperLeftX = centerCoord[0] - radius
                upperLeftY = centerCoord[1] - radius
                pygame.draw.rect(game, currentColor,
                                 pygame.Rect(upperLeftX, upperLeftY, self.itemsSize, self.itemsSize))

        return game


class TransformCoord:
    def __init__(self, gridSize, edgeSize):
        self.gridSize = gridSize
        self.edgeSize = edgeSize

    def __call__(self, coords, center=False):
        if center:  # make the coords the center of the shape
            xLoc = int((coords[0] - 1) * self.gridSize + self.edgeSize + self.gridSize / 2)
            yLoc = int((coords[1] - 1) * self.gridSize + self.edgeSize + self.gridSize / 2)
        else:
            xLoc = int((coords[0] - 1) * self.gridSize + self.edgeSize)
            yLoc = int((coords[1] - 1) * self.gridSize + self.edgeSize)

        return (xLoc, yLoc)


class DrawAgents:
    def __init__(self, redFigure, blueFigure, transformCoord):
        self.redFigure = redFigure
        self.blueFigure = blueFigure
        self.transformCoord = transformCoord

    def __call__(self, game, agentsCoord):
        signalerLoc = self.transformCoord(agentsCoord[0])
        receiverLoc = self.transformCoord(agentsCoord[1])

        game.blit(self.redFigure, signalerLoc)
        game.blit(self.blueFigure, receiverLoc)

        return game


class DrawCostBox:
    def __init__(self, displayText, costText, costBoxPos, costBoxSize, lineColor, lineWidth, fontName, fontSize, costTextColor):
        self.displayText = displayText
        self.costText = costText
        self.costBoxPos = costBoxPos
        self.costBoxSize = costBoxSize
        self.lineColor = lineColor
        self.lineWidth = lineWidth
        self.fontName = fontName
        self.fontSize = fontSize
        self.costTextColor = costTextColor

    def __call__(self, game, cost = None):
        costBoxX, costBoxY = self.costBoxPos
        costBoxWidth, costBoxHeight = self.costBoxSize
        newBoxLocSize = (costBoxX + self.lineWidth, costBoxY + self.lineWidth,
                         costBoxWidth - self.lineWidth * 2,costBoxHeight - self.lineWidth * 2)
        pygame.draw.rect(game, (255, 255, 255), newBoxLocSize) # cover old info by a new white box

        pygame.draw.rect(game, self.lineColor, self.costBoxPos + self.costBoxSize, self.lineWidth)
        textCenter = (costBoxX + costBoxWidth/2, costBoxY + costBoxHeight/3)
        self.displayText(game, self.costText, self.fontName, self.fontSize, self.costTextColor, textCenter)

        if cost is not None:
            costNumberCenter = (costBoxX + costBoxWidth / 2, costBoxY + costBoxHeight / 3 * 2)
            self.displayText(game, str(cost), self.fontName, self.fontSize, self.costTextColor, costNumberCenter)


class DrawTextbox:
    def __init__(self, displayText, text, textboxPos, textboxSize, textboxColor, textboxFontName, textboxFontSize,
                 textboxTextColor):

        self.displayText = displayText
        self.text = text
        self.textboxPos = textboxPos
        self.textboxSize = textboxSize
        self.textboxColor = textboxColor
        self.textboxFontName = textboxFontName
        self.textboxFontSize = textboxFontSize
        self.textboxTextColor = textboxTextColor

    def __call__(self, game, underline = False):
        pygame.draw.rect(game, self.textboxColor, self.textboxPos + self.textboxSize)
        textboxX, textboxY = self.textboxPos
        textboxWidth, textboxHeight = self.textboxSize
        textCenter = (textboxX + textboxWidth/2, textboxY + textboxHeight/2)

        self.displayText(game, self.text, self.textboxFontName, self.textboxFontSize,
                         self.textboxTextColor, textCenter, underline)


class DrawScreen:
    def __init__(self, drawGrids, drawAgents, drawSignal, drawTarget, drawCostBox,drawReturnBox,
                 redMouse, blueMouse, backgroundColor):
        self.drawGrids = drawGrids
        self.drawAgents = drawAgents
        self.drawTarget = drawTarget
        self.drawSignal = drawSignal
        self.drawCostBox = drawCostBox
        self.drawReturnBox = drawReturnBox

        self.redMouse = redMouse
        self.blueMouse = blueMouse
        self.backgroundColor = backgroundColor

    def __call__(self, game, currentAgent, agentsCoord, signalsColor, signalsShape, signalsCoord,
                 targetsColor, targetsShape, targetsCoord):
        game.fill(self.backgroundColor)

        game = self.drawGrids(game)
        game = self.drawAgents(game, agentsCoord)
        game = self.drawSignal(game, signalsColor, signalsShape, signalsCoord)
        game = self.drawTarget(game, targetsColor, targetsShape, targetsCoord)

        self.drawCostBox(game)
        self.drawReturnBox(game, underline = True)

        # set mouse
        game.blit(self.redMouse if currentAgent is "signaler" else self.blueMouse,
                  (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))
        return game


class DrawInitialScreen:
    def __init__(self, backgroundColor, drawInstructionText, drawContinueButton):
        self.backgroundColor = backgroundColor
        self.drawInstructionText = drawInstructionText
        self.drawContinueButton = drawContinueButton

    def __call__(self, game):
        game.fill(self.backgroundColor)
        self.drawInstructionText(game)
        self.drawContinueButton(game, underline = True)


class DisplayText:
    def __init__(self, numCharPerLine):
        self.numCharPerLine = numCharPerLine

    def __call__(self, game, text, fontName, fontSize, fontColor, firstLineCenter, underline = False):
        numLines = int(len(text) / self.numCharPerLine) + 1
        spacing = fontSize / 2 * 3

        lineSeq = [text[currentLine * self.numCharPerLine: (currentLine + 1) * self.numCharPerLine] for currentLine in
                   range(numLines)]
        font = pygame.font.Font(fontName, fontSize)
        if underline: font.set_underline(True)

        lineSurfaces = [font.render(line, True, fontColor) for line in lineSeq]

        firstLineCenterX, firstLineCenterY = firstLineCenter

        for lineNumber in range(len(lineSurfaces)):
            lineSurface = lineSurfaces[lineNumber]
            lineCenter = (firstLineCenterX, firstLineCenterY + spacing * lineNumber)
            lineRect = lineSurface.get_rect(center=lineCenter)
            game.blit(lineSurface, lineRect)

