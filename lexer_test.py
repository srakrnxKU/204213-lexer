import unittest
from lexer import AutomataWithOutput
from lexer import Lexer


class AutomataTest(unittest.TestCase):
    def test_init_fa(self):
        moves = [(1, "a", 2, None), (2, "b", 3, "2"), (3, "b", 4, None), (4, "a", 1, "1")]
        error_moves = []
        start = 1
        fa = AutomataWithOutput(moves, error_moves, start)
        self.assertIsInstance(fa, AutomataWithOutput)

    def test_no_move(self):
        moves = [(1, "a", 2, None), (2, "b", 3, "2"), (3, "b", 4, None), (4, "a", 1, "1")]
        error_moves = []
        start = 1
        fa = AutomataWithOutput(moves, error_moves, start)
        self.assertEqual(fa.state, start)

    def test_moves(self):
        moves = [(1, "a", 2, None), (2, "b", 3, "2"), (3, "b", 4, None), (4, "a", 1, "1")]
        error_moves = []
        start = 1
        fa = AutomataWithOutput(moves, error_moves, start)
        fa.move("a")
        self.assertEqual(fa.state, 2)
        fa.move("b")
        self.assertEqual(fa.state, 3)

    def test_moves_output(self):
        moves = [(1, "a", 2, None), (2, "b", 3, "2"), (3, "b", 4, None), (4, "a", 1, "1")]
        error_moves = []
        start = 1
        fa = AutomataWithOutput(moves, error_moves, start)
        self.assertEqual(fa.move("a"), None)
        self.assertEqual(fa.move("b"), "2")

    def test_impossible_move(self):
        moves = [
            (1, "a", 2, None),
            (2, "b", 3, "2"),
            (3, "b", 4, None),
            (4, "a", 1, "1"),
            ("error", "1", 1, "3"),
        ]
        error_moves = []
        start = 1
        fa = AutomataWithOutput(moves, error_moves, start)
        move_result = fa.move("b")
        self.assertEqual(fa.state, "error")
        move_result = fa.move("1")
        self.assertEqual(move_result, "3")
        self.assertEqual(fa.state, 1)


class LexerTest(unittest.TestCase):
    l = Lexer()

    def test_empty_move(self):
        result = self.l.move("")
        self.assertEqual(result, [])

    def test_literal_move(self):
        result = self.l.move("+-")
        self.assertEqual(result, [("+", "LITERAL"), ("-", "LITERAL")])
        result = self.l.move("  - +   ")
        self.assertEqual(result, [("-", "LITERAL"), ("+", "LITERAL")])

    def test_identifier_move(self):
        result = self.l.move("abc123")
        self.assertEqual(result, [("abc123", "IDEN")])
        result = self.l.move("abc123 def")
        self.assertEqual(result, [("abc123", "IDEN"), ("def", "IDEN")])
        result = self.l.move("   m no   ")
        self.assertEqual(result, [("m", "IDEN"), ("no", "IDEN")])

    def test_literal_with_identifier(self):
        result = self.l.move("abc123+def-g")
        self.assertEqual(
            result,
            [
                ("abc123", "IDEN"),
                ("+", "LITERAL"),
                ("def", "IDEN"),
                ("-", "LITERAL"),
                ("g", "IDEN"),
            ],
        )
        result = self.l.move("abc123 def-g")
        self.assertEqual(
            result, [("abc123", "IDEN"), ("def", "IDEN"), ("-", "LITERAL"), ("g", "IDEN")]
        )
        result = self.l.move("    pqr    st +   u  ")
        self.assertEqual(
            result, [("pqr", "IDEN"), ("st", "IDEN"), ("+", "LITERAL"), ("u", "IDEN")]
        )

    def test_constant_no_decimal_point(self):
        result = self.l.move("123")
        self.assertEqual(result, [("123", "CONST")])
        result = self.l.move("   123    ")
        self.assertEqual(result, [("123", "CONST")])
        result = self.l.move("   123   456 ")
        self.assertEqual(result, [("123", "CONST"), ("456", "CONST")])

    def test_constant_with_literals(self):
        result = self.l.move("123+45")
        self.assertEqual(result, [("123", "CONST"), ("+", "LITERAL"), ("45", "CONST")])
        result = self.l.move("   123 +   45 ")
        self.assertEqual(result, [("123", "CONST"), ("+", "LITERAL"), ("45", "CONST")])

    def test_constant_identifiers_literals(self):
        result = self.l.move("12a+1b23")
        self.assertEqual(
            result,
            [
                ("12", "CONST"),
                ("a", "IDEN"),
                ("+", "LITERAL"),
                ("1", "CONST"),
                ("b23", "IDEN"),
            ],
        )
        result = self.l.move("    12a + 1b23 c34")
        self.assertEqual(
            result,
            [
                ("12", "CONST"),
                ("a", "IDEN"),
                ("+", "LITERAL"),
                ("1", "CONST"),
                ("b23", "IDEN"),
                ("c34", "IDEN"),
            ],
        )

    def test_unknown_chars_error(self):
        result = self.l.move("!@")
        self.assertEqual(result, [("!@", "ERROR")])
        result = self.l.move(" !@  jtf")
        self.assertEqual(result, [("!@", "ERROR"), ("jtf", "IDEN")])
        result = self.l.move(" !@123")
        self.assertEqual(result, [("!@", "ERROR"), ("123", "CONST")])
        result = self.l.move(" !@ABC12.3$$")
        self.assertEqual(
            result,
            [
                ("!@", "ERROR"),
                ("ABC12", "IDEN"),
                (".", "ERROR"),
                ("3", "CONST"),
                ("$$", "ERROR"),
            ],
        )

    def test_decimal(self):
        result = self.l.move("123.")
        self.assertEqual(result, [("123.", "ERROR")])
        result = self.l.move("123.45")
        self.assertEqual(result, [("123.45", "CONST")])


if __name__ == "__main__":
    unittest.main()
