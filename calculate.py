import numpy as np
import pygame

def calculateCost(agentPos, agentChoice):
    return round(np.linalg.norm(np.array(agentPos) - np.array(agentChoice), ord=2), 2)

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
