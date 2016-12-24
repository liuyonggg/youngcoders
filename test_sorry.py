import unittest
import sorry

class SafetyzoneTest(unittest.TestCase):
    def setUp(self):
        self.sf = sorry.safetyzone("Yellow", 2, 100)

    def test_in_safetyzone_1(self):
        self.assertFalse(self.sf.in_safetyzone(100))

    def test_in_safetyzone_2(self):
        self.assertTrue(self.sf.in_safetyzone(101))

    def test_in_safetyzone_3(self):
        with self.assertRaises(AssertionError):
            self.sf.in_safetyzone(201)

    def test_entering_safetyzone_1(self):
        self.assertTrue(self.sf.entering_safetyzone(2))

    def test_entering_safetyzone_2(self):
        self.assertFalse(self.sf.entering_safetyzone(4))

    def test_in_or_entering_safetyzone_1(self):
        self.assertTrue(self.sf.in_or_entering_safetyzone(2))

    def test_in_or_entering_safetyzone_2(self):
        self.assertTrue(self.sf.in_or_entering_safetyzone(102))

    def test_in_or_entering_safetyzone_3(self):
        self.assertFalse(self.sf.in_or_entering_safetyzone(1))

    def test_in_home_1(self):
        self.assertTrue(self.sf.in_home(108))

    def test_in_home_2(self):
        self.assertFalse(self.sf.in_home(2))

    def test_position_1(self):
        self.assertEqual(self.sf.position(101, 4), 105)

    def test_position_2(self):
        self.assertEqual(self.sf.position(107, 3), 106)

    def test_positon_3(self):
        with self.assertRaises(AssertionError):
            self.sf.position(5, 34)

    def test_positon_4(self):
        self.assertEqual(self.sf.position(2, 3), 105)
        
class BoardTest(unittest.TestCase):
    def setUp(self):
        self.b = sorry.board()
        self.p = sorry.pawn("YELLOW", None, 0)

    def test_position(self):
        print self.b.position(self.p, 10)

if __name__ == "__main__":
    unittest.main()
