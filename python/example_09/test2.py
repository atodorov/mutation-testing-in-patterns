import roads
import unittest

class TestRoadLimits(unittest.TestCase):
    def test_urban_road(self):
        road = roads.UrbanRoad()
        self.assertEqual(road.speedLimit, 50)

    def test_rural_road(self):
        road = roads.RuralRoad()
        self.assertEqual(road.speedLimit, 90)

    def test_motorway(self):
        road = roads.Motorway()
        self.assertEqual(road.speedLimit, 130)
        self.assertEqual(road.minSpeed, 50)


if __name__ == "__main__":
    unittest.main()
