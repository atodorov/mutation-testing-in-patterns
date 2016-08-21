import sandwich
import unittest

class TestSandwich(unittest.TestCase):
    def setUp(self):
        self.sandwich_1 = sandwich.Sandwich()
        self.sandwich_2 = sandwich.Sandwich()

    def test_default_objects_are_always_equal(self):
        """
            Newly created objects with the same attribute values
            (e.g. default ones) are always equal. At the same time
            != will return False for the same objects.
        """
        self.assertEqual(self.sandwich_1, self.sandwich_2)
        self.assertFalse(self.sandwich_1 != self.sandwich_2)


    def test_object_does_not_equal_None(self):
        """
            An object instance is never equal to None.
            Tests the if statement in the __eq__ method.
        """
        self.assertNotEqual(self.sandwich_1, None)


    def test_objects_differing_by_one_attribute_are_not_equal(self):
        """
            Objects are never equal if at least one attribute differs.
            To test all attributes we loop over each at a time,
            update the values and compare the objects.
        """
        for atr in ['meat', 'bread']:
            setattr(self.sandwich_1, atr, 'test')
            setattr(self.sandwich_2, atr, '')
            # comparison works both ways so test it both ways
            self.assertNotEqual(self.sandwich_1, self.sandwich_2)
            self.assertNotEqual(self.sandwich_2, self.sandwich_1)
            setattr(self.sandwich_1, atr, '')
            setattr(self.sandwich_2, atr, '')

class TestSandwichWithMayoAndEggs(unittest.TestCase):
    def setUp(self):
        self.sandwich_1 = sandwich.SandwichWithMayoAndEggs()
        self.sandwich_2 = sandwich.SandwichWithMayoAndEggs()

    def test_object_does_not_equal_None(self):
        self.assertNotEqual(self.sandwich_1, None)

    def test_default_values(self):
        self.assertEqual(self.sandwich_1.mayo, True)
        self.assertEqual(self.sandwich_1.eggs, 2)

    def test_objects_differing_by_one_attribute_are_not_equal(self):
        """ this time object attributes are of different types"""
        # meat
        self.sandwich_1.meat = 'Chicken'
        self.sandwich_2.meat = ''
        self.assertNotEqual(self.sandwich_1, self.sandwich_2)
        self.assertNotEqual(self.sandwich_2, self.sandwich_1)
        self.sandwich_1.meat = ''
        self.sandwich_2.meat = ''

        # bread
        self.sandwich_1.bread = 'Baguette'
        self.sandwich_2.bread = ''
        self.assertNotEqual(self.sandwich_1, self.sandwich_2)
        self.assertNotEqual(self.sandwich_2, self.sandwich_1)
        self.sandwich_1.bread = ''
        self.sandwich_2.bread = ''

        # mayo
        self.sandwich_1.mayo = True
        self.sandwich_2.mayo = False
        self.assertNotEqual(self.sandwich_1, self.sandwich_2)
        self.assertNotEqual(self.sandwich_2, self.sandwich_1)
        self.sandwich_1.mayo = False
        self.sandwich_2.mayo = False

        self.sandwich_1.eggs = 2
        self.sandwich_2.eggs = 0
        self.assertNotEqual(self.sandwich_1, self.sandwich_2)
        self.assertNotEqual(self.sandwich_2, self.sandwich_1)
        self.sandwich_1.eggs = 0
        self.sandwich_2.eggs = 0

if __name__ == "__main__":
    unittest.main()
