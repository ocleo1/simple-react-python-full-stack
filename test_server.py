# - *- coding: utf-8 - *-

import unittest

class MyCalculator:
    def add(self, x, y):
        return x + y

    def subtract(self, x, y):
        return x - y

class TestMyCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = MyCalculator()

    def test_add(self):
        self.assertEqual(self.calc.add(1, 2), 3)
        self.assertEqual(self.calc.add(-1, 1), 0)
        self.assertEqual(self.calc.add(0, 0), 0)

    def test_subtract(self):
        self.assertEqual(self.calc.subtract(5, 3), 2)
        self.assertEqual(self.calc.subtract(7, 9), -2)
        self.assertEqual(self.calc.subtract(0, 0), 0)

    def tearDown(self):
        del self.calc

if __name__ == '__main__':
    unittest.main()
