def calculateCost(agentPos, agentChoice):
    agentX, agentY = agentPos
    choiceX, choiceY = agentChoice
    cost = abs(agentX - choiceX) + abs(agentY - choiceY)
    # round(np.linalg.norm(np.array(agentPos) - np.array(agentChoice), ord=2), 2)
    return cost


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

class StayWithinBoundary:
    def __init__(self, gridCoordMinValue, numberOfGrids):
        self.gridCoordMinValue = gridCoordMinValue
        self.numberOfGrids = numberOfGrids

    def __call__(self, intendedCoord):
        nextX, nextY = intendedCoord
        if nextX < self.gridCoordMinValue:
            nextX = self.gridCoordMinValue
        if nextX > self.numberOfGrids:
            nextX = self.numberOfGrids
        if nextY < self.gridCoordMinValue:
            nextY = self.gridCoordMinValue
        if nextY > self.numberOfGrids:
            nextY = self.numberOfGrids
        return nextX, nextY
