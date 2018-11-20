import unittest
from lexer import AutomataWithOutput
from lexer import Lexer


class AutomataTest(unittest.TestCase):
    def test_init_fa(self):
        moves = [(1, "a", 2, None), (2, "b", 3, "2"), (3, "b", 4, None), (4, "a", 1, "1")]
        start = 1
        fa = AutomataWithOutput(moves, start)
        self.assertIsInstance(fa, AutomataWithOutput)

    def test_no_move(self):
        moves = [(1, "a", 2, None), (2, "b", 3, "2"), (3, "b", 4, None), (4, "a", 1, "1")]
        start = 1
        fa = AutomataWithOutput(moves, start)
        self.assertEqual(fa.state, start)

    def test_moves(self):
        moves = [(1, "a", 2, None), (2, "b", 3, "2"), (3, "b", 4, None), (4, "a", 1, "1")]
        start = 1
        fa = AutomataWithOutput(moves, start)
        fa.move("a")
        self.assertEqual(fa.state, 2)
        fa.move("b")
        self.assertEqual(fa.state, 3)

    def test_moves_output(self):
        moves = [(1, "a", 2, None), (2, "b", 3, "2"), (3, "b", 4, None), (4, "a", 1, "1")]
        start = 1
        fa = AutomataWithOutput(moves, start)
        self.assertEqual(fa.move("a"), None)
        self.assertEqual(fa.move("b"), "2")

    def test_impossible_move(self):
        moves = [(1, "a", 2, None), (2, "b", 3, "2"), (3, "b", 4, None), (4, "a", 1, "1")]
        start = 1
        fa = AutomataWithOutput(moves, start)
        move_result = fa.move("b")
        self.assertEqual(move_result, False)
        self.assertEqual(fa.state, start)
        move_result = fa.move("a")
        move_result = fa.move("a")
        self.assertEqual(move_result, False)
        self.assertEqual(fa.state, start)


class LexerTest(unittest.TestCase):
    l = Lexer()

    def test_empty_move(self):
        result = self.l.move("")
        self.assertEqual(result, [])

    def test_literal_move(self):
        result = self.l.move("+-")
        self.assertEqual(result, [("+", "LITERAL"), ("-", "LITERAL")])


"""     def test_identifier_move(self):
        result = self.l.move("abc123")
        self.assertEqual(result, [("abc123", "IDEN")]) """


if __name__ == "__main__":
    unittest.main()
