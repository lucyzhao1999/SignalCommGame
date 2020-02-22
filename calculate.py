import numpy as np
import pygame

def calculateCost(agentPos, agentChoice):
    return round(np.linalg.norm(np.array(agentPos) - np.array(agentChoice), ord=2), 2)


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
