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
        self.p = sorry.pawn("YELLOW", None, 3)
        self.p1 = sorry.pawn("YELLOW", None, 1)

    def test_position_1(self):
        self.assertEqual(self.b.position(self.p, 10), 13)

    def test_position_2(self):
        self.assertEqual(self.b.position(self.p, 20), 23)

    def test_position_3(self):
        self.assertEqual(self.b.position(self.p1, 6), 167)

    def test_position_4(self):
        self.assertEqual(self.b.position(self.p1, 9), 164)

    def test_slide_1(self):
        self.assertEqual(self.b.slide(4), 4)

    def test_slide_2(self):
        self.assertEqual(self.b.slide(1), 4)

    def test_slide_3(self):
        self.assertEqual(self.b.slide(39), 43)

    def test_in_home_1(self):
        self.assertTrue(self.b.in_home(sorry.pawn("YELLOW", None, 167)))

    def test_in_home_2(self):
        self.assertFalse(self.b.in_home(self.p))

    def test_in_safetyzone_1(self):
        self.assertFalse(self.b.in_safetyzone(self.p1))

    def test_in_safetyzone_2(self):
        self.assertTrue(self.b.in_safetyzone(sorry.pawn("YELLOW", None, 162)))

    def test_dist_home_1(self):
        self.assertEqual(self.b.dist_home(self.p1), 6)

    def test_dist_home_2(self):
        self.assertEqual(self.b.dist_home(self.p), 64)
    
    def test_distance_1(self):
        self.assertEqual(self.b.distance(self.p, self.p1), 58)

    def test_distance_2(self):
        self.assertEqual(self.b.distance(self.p, sorry.pawn("YELLOW", None, 4)), 1)

class CardTest(unittest.TestCase):
    def setUp(self):
        self.p1 = sorry.pawn("YELLOW", None, 3)
        self.p2 = sorry.pawn("YELLOW", None, -1)
        self.p3 = sorry.pawn("RED", None, 43)
        self.b = sorry.board()

    def test_cardcommon_1(self):
        c = sorry.cardcommon()
        c.apply(self.p1, None, 0, self.b, 4)
        self.assertEqual(self.p1.position, 7)

    def test_card1_1(self):
        c = sorry.card1()
        c.apply(self.p1, None, c.CARD_MODE[1], self.b)
        self.assertEqual(self.p1.position, 4)

    def test_card1_2(self):
        c = sorry.card1()
        c.apply(self.p2, None, c.CARD_MODE[0], self.b)
        self.assertEqual(self.p2.position, 3)

    def test_card2_1(self):
        c = sorry.card2()
        c.apply(self.p1, None, c.CARD_MODE[1], self.b)
        self.assertEqual(self.p1.position, 5)

    def test_card2_2(self):
        c = sorry.card2()
        c.apply(self.p2, None, c.CARD_MODE[0], self.b)
        self.assertEqual(self.p1.position, 3)

    def test_card3_1(self):
        c = sorry.card3()
        c.apply(self.p1, None, 0, self.b)
        self.assertEqual(self.p1.position, 6)

    def test_card4_1(self):
        c = sorry.card4()
        c.apply(self.p3, None, 0, self.b)
        self.assertEqual(self.p3.position, 39)

    def test_card5_1(self):
        c = sorry.card5()
        c.apply(self.p1, None, 0, self.b)
        self.assertEqual(self.p1.position, 8)

    def test_card7_1(self):
        c = sorry.card7()
        c.apply(self.p1, None, 0, self.b)
        self.assertEqual(self.p1.position, 10)

    def test_card8_1(self):
        c = sorry.card8()
        c.apply(self.p1, None, 0, self.b)
        self.assertEqual(self.p1.position, 11)

    def test_card10_1(self):
        c = sorry.card10()
        c.apply(self.p1, None, "FORWARD", self.b)
        self.assertEqual(self.p1.position, 13)

    def test_card10_2(self):
        c = sorry.card10()
        c.apply(self.p1, None, "BACKWARD", self.b)
        self.assertEqual(self.p1.position, 2)

    def test_card11_1(self):
        c = sorry.card11()
        c.apply(self.p1, None, "FORWARD", self.b)
        self.assertEqual(self.p1.position, 14)

    def test_card11_2(self):
        c = sorry.card11()
        c.apply(self.p1, self.p3, "EXCHANGE", self.b)
        self.assertEqual(self.p1.position, 43)
        self.assertEqual(self.p3.position, 3)

    def test_card12_1(self):
        c = sorry.card12()
        c.apply(self.p1, None, "FORWARD", self.b)
        self.assertEqual(self.p1.position, 15)

    def test_cardsorry(self):
        c = sorry.cardsorry()
        c.apply(self.p1, self.p3, 0, self.b)
        self.assertEqual(self.p1.position, 43)
        self.assertEqual(self.p3.position, -1)

class PlayerTest(unittest.TestCase):
    def setUp(self):
        self.p = sorry.player("Jack", "YELLOW", None)

    def test_is_win_1(self):
        self.assertFalse(self.p.is_win())

class StrategyTest(unittest.TestCase):
    def setUp(self):
        self.g = sorry.game()
        self.s = sorry.strategy(self.g)
        self.p = sorry.player("Bob", "YELLOW", self.s)
        self.s.set_player(self.p)

    def test_filtersortpawns_1(self):
        self.assertEqual(self.s.filtersortpawns(), self.s._player._pawns)

    def test_filtersortpawns_2(self):
        self.s._player._pawns = [sorry.pawn("YELLOW", self.s._player, 7),
                                sorry.pawn("YELLOW", self.s._player, 9),
                                sorry.pawn("YELLOW", self.s._player, 2),
                                sorry.pawn("YELLOW", self.s._player, 3)]
        self.assertEqual(self.s.filtersortpawns()[0].position, 9)

    def test_card1_2_common_strategy(self):
        card = sorry.card1()
        out = False
        self.s.card1_2_common_strategy(card)
        for pawn in self.s._player.pawns:
            if pawn.position > 0:
                out = True
        self.assertTrue(out)
        
        i = 0
        self.s.card1_2_common_strategy(card)
        for pawn in self.s._player.pawns:
            i += pawn.position
        self.assertEqual(i, 1)

    def test_only_move_cards_common_strategy_1(self):
        card1 = sorry.card3()
        card2 = sorry.card1()
        self.s.card1_2_common_strategy(card2)
        self.s.only_move_cards_common_strategy(card1)
        self.assertEqual(self.s._player._pawns[0].position, 6)

    def test_only_move_cards_common_strategy_2(self):
        card1 = sorry.card3()
        self.assertFalse(self.s.only_move_cards_common_strategy(card1))

    def test_move_backwards_strategy_1(self):
        card = sorry.card4()
        self.assertFalse(self.s.move_backwards_strategy(card))

#    def test_move_backwards_strategy_2(self):
#        card1 = sorry.card1()
#        card2 = sorry.card4() 
#        self.s.card1_2_common_strategy(card1)
#        self.s.move_backwards_strategy(card2)
#        self.assertEqual(self.s._player._pawns[0].position, 0)

if __name__ == "__main__":
    unittest.main()
