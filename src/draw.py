import pygame

WHITE = (255, 255, 255)
BLACK = (0,0,0)


class DisplayGame:
    def __init__(self, screenWidth, screenHeight, caption, fullScreen):
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.caption = caption
        self.fullScreen = fullScreen

    def __call__(self):
        pygame.init()
        if self.fullScreen:
            game = pygame.display.set_mode((self.screenWidth, self.screenHeight), pygame.FULLSCREEN)
        else:
            game = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        pygame.display.init()
        pygame.display.set_caption(self.caption)
        pygame.fastevent.init()
        return game


class DrawGrids:
    def __init__(self, game, drawShade, numberOfGrids, gridSize, edgeSize, lineColor, lineWidth, shadeHeight, shadeColor = BLACK):
        self.game = game
        self.drawShade = drawShade
        self.numberOfGrids = numberOfGrids
        self.gridSize = gridSize
        self.edgeSize = edgeSize
        self.lineColor = lineColor
        self.lineWidth = lineWidth
        self.shadeHeight = shadeHeight
        self.shadeColor = shadeColor

    def __call__(self, fillGray):
        for i in range(self.numberOfGrids + 1):  # draw grids
            pygame.draw.line(self.game, self.lineColor, (self.edgeSize, self.edgeSize + i * self.gridSize),
                             (self.edgeSize + self.numberOfGrids * self.gridSize, self.edgeSize + i * self.gridSize),self.lineWidth)  # horizontalLine
            pygame.draw.line(self.game, self.lineColor, (self.edgeSize + i * self.gridSize, self.edgeSize),
                             (self.edgeSize + i * self.gridSize, self.edgeSize + self.numberOfGrids * self.gridSize), self.lineWidth)  # verticalLine

        if fillGray:
            shadeUpperLeftCoord = (1, self.numberOfGrids - self.shadeHeight+ 1)
            shadeGridWidth = self.numberOfGrids
            shadeGridHeight = self.shadeHeight
            self.drawShade(shadeUpperLeftCoord, self.shadeColor, shadeGridWidth, shadeGridHeight)

        return self.game


class DrawItems:
    def __init__(self, game, transformCoord, itemsSize, lineWidth = 2, lineColor = BLACK):
        self.game = game
        self.transformCoord = transformCoord
        self.itemsSize = itemsSize
        self.lineWidth = lineWidth
        self.lineColor = lineColor

    def __call__(self, colorList, shapeList, coordList):
        numOfItems = len(colorList)
        for itemIndex in range(numOfItems):
            itemColor = colorList[itemIndex]
            itemPos = coordList[itemIndex]
            itemPosCoord = self.transformCoord(itemPos, center=True)
            radius = int(self.itemsSize / 2)

            itemShape = shapeList[itemIndex]

            if itemShape == 'circle':
                pygame.draw.circle(self.game, itemColor, itemPosCoord, radius)
                pygame.draw.circle(self.game, self.lineColor, itemPosCoord, radius, self.lineWidth)

            if itemShape == 'square':
                upperLeftX = itemPosCoord[0] - radius
                upperLeftY = itemPosCoord[1] - radius
                pygame.draw.rect(self.game, itemColor,
                                 pygame.Rect(upperLeftX, upperLeftY, self.itemsSize, self.itemsSize))

            if itemShape == 'triangle':
                lowerLeftCoord = (itemPosCoord[0] - radius, itemPosCoord[1] + radius)
                lowerRightCoord = (itemPosCoord[0] + radius, itemPosCoord[1] + radius)
                upperCornerCoord = (itemPosCoord[0], itemPosCoord[1] - radius)
                if itemColor is not None:
                    pygame.draw.polygon(self.game, itemColor, [lowerLeftCoord, lowerRightCoord, upperCornerCoord])
                pygame.draw.polygon(self.game, self.lineColor, [lowerLeftCoord, lowerRightCoord, upperCornerCoord], self.lineWidth)

        return self.game



class DrawCostBox:
    def __init__(self, game, displayText, costText, costTextCenter, costBoxPos, costBoxSize,
                 lineColor, lineWidth, fontName, fontSize,
                 costTextColor, costNumberCenterPos):
        self.game = game
        self.displayText = displayText
        self.costText = costText
        self.costTextCenter = costTextCenter
        self.costBoxPos = costBoxPos
        self.costBoxSize = costBoxSize
        self.lineColor = lineColor
        self.lineWidth = lineWidth
        self.fontName = fontName
        self.fontSize = fontSize
        self.costTextColor = costTextColor
        self.costNumberCenterPos = costNumberCenterPos

    def __call__(self, cost = None):
        costBoxX, costBoxY = self.costBoxPos
        costBoxWidth, costBoxHeight = self.costBoxSize

        coverBoxPos = (costBoxX + self.lineWidth, costBoxY + self.lineWidth)
        coverBoxSize = (costBoxWidth - self.lineWidth * 2,costBoxHeight - self.lineWidth * 2)

        pygame.draw.rect(self.game, WHITE, coverBoxPos+ coverBoxSize) # cover old info by a new white box
        pygame.draw.rect(self.game, self.lineColor, self.costBoxPos + self.costBoxSize, self.lineWidth)

        self.displayText(self.costText, self.fontName, self.fontSize, self.costTextColor, self.costTextCenter)

        if cost is not None:
            self.displayText(str(cost), self.fontName, self.fontSize, self.costTextColor, self.costNumberCenterPos)
         
        return self.game


class DisplayText:
    def __init__(self, game, numCharPerLine, spacingFontSizeRatio):
        self.game = game
        self.numCharPerLine = numCharPerLine
        self.spacingFontSizeRatio = spacingFontSizeRatio

    def __call__(self, text, fontName, fontSize, fontColor, firstLineCenter, underline = False):
        numLines = int(len(text) / self.numCharPerLine) + 1
        spacing = fontSize * self.spacingFontSizeRatio
        lineSeq = [text[currentLine * self.numCharPerLine: (currentLine + 1) * self.numCharPerLine] for currentLine in
                   range(numLines)]

        font = pygame.font.Font(fontName, fontSize)
        if underline:
            font.set_underline(True)

        antialias = True # prevent from being jaggy
        lineSurfaces = [font.render(line, antialias, fontColor) for line in lineSeq]

        firstLineCenterX, firstLineCenterY = firstLineCenter
        for lineNumber in range(len(lineSurfaces)):
            lineSurface = lineSurfaces[lineNumber]
            lineCenter = (firstLineCenterX, firstLineCenterY + spacing * lineNumber)
            lineRect = lineSurface.get_rect(center=lineCenter)
            self.game.blit(lineSurface, lineRect)

        return self.game


class DrawTextbox:
    def __init__(self, game, displayText, text, textboxPos, textboxSize, textboxColor, textboxFontName, textboxFontSize,
                 textboxTextColor):
        self.game = game
        self.displayText = displayText
        self.text = text
        self.textboxPos = textboxPos
        self.textboxSize = textboxSize
        self.textboxColor = textboxColor
        self.textboxFontName = textboxFontName
        self.textboxFontSize = textboxFontSize
        self.textboxTextColor = textboxTextColor

    def __call__(self, underline = False):
        pygame.draw.rect(self.game, self.textboxColor, self.textboxPos + self.textboxSize)
        textboxX, textboxY = self.textboxPos
        textboxWidth, textboxHeight = self.textboxSize
        textCenter = (textboxX + textboxWidth/2, textboxY + textboxHeight/2)

        self.displayText(self.text, self.textboxFontName, self.textboxFontSize,
                         self.textboxTextColor, textCenter, underline)
         
        return self.game


class DrawInitialScreen:
    def __init__(self, game, backgroundColor, drawInstructionText):
        self.game = game
        self.backgroundColor = backgroundColor
        self.drawInstructionText = drawInstructionText

    def __call__(self):
        self.game.fill(self.backgroundColor)
        self.drawInstructionText()
        pygame.display.init()

        return self.game


class DrawScreen:
    def __init__(self, game, drawGrids, drawSignal, drawTarget,backgroundColor):
        self.game = game
        self.drawGrids = drawGrids
        self.drawTarget = drawTarget
        self.drawSignal = drawSignal
        self.backgroundColor = backgroundColor

    def __call__(self, currentAgent, signalsColor, signalsShape, signalsCoord,
                 targetsColor, targetsShape, targetsCoord):
        self.game.fill(self.backgroundColor)
        self.drawGrids(fillGray = False if currentAgent is 'signaler' else True)
        self.drawSignal(signalsColor, signalsShape, signalsCoord)
        self.drawTarget(targetsColor, targetsShape, targetsCoord)

        return self.game


class DrawAgent:
    def __init__(self, game, transformCoord, figure):
        self.transformCoord = transformCoord
        self.game = game
        self.figure = figure

    def __call__(self, agentsCoord):
        location = self.transformCoord(agentsCoord)
        self.game.blit(self.figure, location)

        return self.game




class DrawShade:
    def __init__(self, game, transformCoord, gridSize):
        self.game = game
        self.transformCoord = transformCoord
        self.gridSize = gridSize

    def __call__(self, shadeUpperLeftCoord, originalColor, shadeGridWidth = 1, shadeGridHeight = 1, shadeAlpha = 50):
        shadeColor = originalColor + (shadeAlpha,)
        shadeWidthPix = shadeGridWidth* self.gridSize
        shadeHeightPix = shadeGridHeight* self.gridSize
        fillSquare = pygame.Surface((shadeWidthPix, shadeHeightPix), pygame.SRCALPHA)
        pygame.draw.rect(fillSquare, shadeColor, fillSquare.get_rect())
        shadePos = self.transformCoord(shadeUpperLeftCoord)
        self.game.blit(fillSquare, shadePos)



class DrawAgents:
    def __init__(self, game, transformCoord, redFigure, blueFigure):
        self.transformCoord = transformCoord
        self.game = game
        self.redFigure = redFigure
        self.blueFigure = blueFigure

    def __call__(self, agentsCoord):
        signalerLoc = self.transformCoord(agentsCoord[0])
        receiverLoc = self.transformCoord(agentsCoord[1])

        self.game.blit(self.redFigure, signalerLoc)
        self.game.blit(self.blueFigure, receiverLoc)

        return self.game


class DrawClickScreen:
    def __init__(self, game, drawGrids, drawAgents, drawSignal, drawTarget, drawCostBox,drawReturnBox,
                 redMouse, blueMouse, backgroundColor):
        self.game = game
        self.drawGrids = drawGrids
        self.drawAgents = drawAgents
        self.drawTarget = drawTarget
        self.drawSignal = drawSignal
        self.drawCostBox = drawCostBox
        self.drawReturnBox = drawReturnBox

        self.redMouse = redMouse
        self.blueMouse = blueMouse
        self.backgroundColor = backgroundColor

    def __call__(self, currentAgent, agentsCoord, signalsColor, signalsShape, signalsCoord,
                 targetsColor, targetsShape, targetsCoord):
        self.game.fill(self.backgroundColor)
        self.drawGrids(fillGray = False if currentAgent is 'signaler' else True)
        self.drawAgents(agentsCoord)
        self.drawSignal(signalsColor, signalsShape, signalsCoord)
        self.drawTarget(targetsColor, targetsShape, targetsCoord)
        self.drawCostBox()
        self.drawReturnBox(underline = True)

        # set mouse
        self.game.blit(self.redMouse if currentAgent is "signaler" else self.blueMouse,
                  (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))

        return self.game


class DrawClickInitialScreen:
    def __init__(self, game, backgroundColor, drawInstructionText, drawContinueButton):
        self.game = game
        self.backgroundColor = backgroundColor
        self.drawInstructionText = drawInstructionText
        self.drawContinueButton = drawContinueButton

    def __call__(self):
        self.game.fill(self.backgroundColor)
        self.drawInstructionText()
        self.drawContinueButton(underline = True)
        pygame.display.init()

        return self.game