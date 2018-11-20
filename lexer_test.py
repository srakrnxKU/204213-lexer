import unittest
from lexer import FiniteAutomata


class AutomataTest(unittest.TestCase):
    def test_init_fa(self):
        k = [1, 2, 3]
        sigma = ["a", "b"]
        moves = [(1, "a", 2, None), (2, "b", 3, "2"), (3, "b", 4, None), (4, "a", 1, "1")]
        start = 1
        fa = FiniteAutomata(k, sigma, moves, start)
        self.assertIsInstance(fa, FiniteAutomata)

    def test_no_move(self):
        k = [1, 2, 3]
        sigma = ["a", "b"]
        moves = [(1, "a", 2, None), (2, "b", 3, "2"), (3, "b", 4, None), (4, "a", 1, "1")]
        start = 1
        fa = FiniteAutomata(k, sigma, moves, start)
        self.assertEqual(fa.state, start)

    def test_moves(self):
        k = [1, 2, 3]
        sigma = ["a", "b"]
        moves = [(1, "a", 2, None), (2, "b", 3, "2"), (3, "b", 4, None), (4, "a", 1, "1")]
        start = 1
        fa = FiniteAutomata(k, sigma, moves, start)
        fa.move("a")
        self.assertEqual(fa.state, 2)
        fa.move("b")
        self.assertEqual(fa.state, 3)

    def test_moves_output(self):
        k = [1, 2, 3]
        sigma = ["a", "b"]
        moves = [(1, "a", 2, None), (2, "b", 3, "2"), (3, "b", 4, None), (4, "a", 1, "1")]
        start = 1
        fa = FiniteAutomata(k, sigma, moves, start)
        self.assertEqual(fa.move("a"), None)
        self.assertEqual(fa.move("b"), "2")

    def test_impossible_move(self):
        k = [1, 2, 3]
        sigma = ["a", "b"]
        moves = [(1, "a", 2, None), (2, "b", 3, "2"), (3, "b", 4, None), (4, "a", 1, "1")]
        start = 1
        fa = FiniteAutomata(k, sigma, moves, start)
        move_result = fa.move("b")
        self.assertEqual(move_result, False)
        self.assertEqual(fa.state, start)
        move_result = fa.move("a")
        move_result = fa.move("a")
        self.assertEqual(move_result, False)
        self.assertEqual(fa.state, start)


if __name__ == "__main__":
    unittest.main()
