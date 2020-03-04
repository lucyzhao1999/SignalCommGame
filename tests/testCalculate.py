import sys
sys.path.append('..')
import unittest
from ddt import ddt, data, unpack
from src.calculate import calculateCost, TransformCoord

@ddt
class TestEnvironment(unittest.TestCase):
    def setUp(self):
        self.gridSize = 30
        self.edgeSize = 5
        self.transformCoord = TransformCoord(self.gridSize, self.edgeSize)

    @data(
        ((3, 4),(3, 4), 0),
        ((1, 1), (2,2), 2),
        ((1, 3), (1,5), 2),
        ((2, 2), (1, 1), 2)
    )
    @unpack
    def testCalculateCost(self, agentPos, agentChoice, trueCost):
        cost = calculateCost(agentPos, agentChoice)
        self.assertEqual(cost, trueCost)

    @data(
        ((3, 4), False, (65, 95)),
        ((1, 1), False, (5,5)),
        ((1, 3), True, (20, 80))
    )
    @unpack
    def testCoordinateTransformation(self, position, center, trueCoords):
        coords = self.transformCoord(position, center)
        self.assertEqual(coords, trueCoords)


    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()


