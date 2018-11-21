"""
Lexer programme for Theory of Computation course,
Sirakorn Lamyai (5910500023)
Department of Computer Engineering, Kasetsart U.
"""

import sys


class AutomataWithOutput:
    def __init__(self, moves, error_moves, start):
        self.moves = moves
        self.error_moves = error_moves
        self.start = start
        self.state = start

    def move(self, inp):
        move = [i for i in self.moves if i[0] == self.state and inp in i[1]]
        if len(move) == 0:
            before_state = self.state
            self.state = "error"
            in_error = [i[1] for i in self.error_moves if i[0] == before_state]
            if len(in_error) > 0:
                return in_error[0]
        else:
            self.state = move[0][2]
            return move[0][3]


class Lexer:
    numerics = list("0123456789")
    characters = list("qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM")
    operators = list("+-*/()")
    dot = ["."]
    whitespaces = [" ", "\n", "\r", "\t"]
    terminator = ["\0"]

    moves = [
        ("start", terminator, "terminated", None),
        ("start", operators, "literals", None),
        ("start", whitespaces, "start", None),
        ("start", characters, "identifiers", None),
        ("start", numerics, "constants", None),
        ("literals", operators, "literals", "LITERAL"),
        ("literals", terminator, "terminated", "LITERAL"),
        ("literals", whitespaces, "start", "LITERAL"),
        ("literals", numerics, "constants", "LITERAL"),
        ("literals", characters, "identifiers", "LITERAL"),
        ("identifiers", characters, "identifiers", None),
        ("identifiers", numerics, "identifiers", None),
        ("identifiers", operators, "literals", "IDEN"),
        ("identifiers", terminator, "terminated", "IDEN"),
        ("identifiers", whitespaces, "start", "IDEN"),
        ("constants", numerics, "constants", None),
        ("constants", whitespaces, "start", "CONST"),
        ("constants", terminator, "terminated", "CONST"),
        ("constants", operators, "literals", "CONST"),
        ("constants", characters, "identifiers", "CONST"),
        ("constants", dot, "constants-dot", None),
        ("constants-dot", terminator, "terminated", "ERROR"),
        ("constants-dot", numerics, "constant-decimals", None),
        ("constants-dot", characters, "identifiers", "ERROR"),
        ("constants-dot", operators, "literals", "ERROR"),
        ("constant-decimals", numerics, "constant-decimals", None),
        ("constant-decimals", whitespaces, "start", "CONST"),
        ("constant-decimals", terminator, "terminated", "CONST"),
        ("constant-decimals", operators, "literals", "CONST"),
        ("constant-decimals", characters, "identifiers", "CONST"),
        ("identifiers", dot, "dot-error", "IDEN"),
        ("dot-error", terminator, "terminated", "ERROR"),
        ("dot-error", operators, "literals", "ERROR"),
        ("dot-error", whitespaces, "dot-error", "ERROR"),
        ("dot-error", characters, "identifiers", "ERROR"),
        ("dot-error", numerics, "constants", "ERROR"),
        ("error", terminator, "terminated", "ERROR"),
        ("error", whitespaces, "start", "ERROR"),
        ("error", numerics, "constants", "ERROR"),
        ("error", operators, "literals", "ERROR"),
        ("error", characters, "identifiers", "ERROR"),
    ]

    error_moves = [
        ("start", None),
        ("identifiers", "IDEN"),
        ("literals", "LITERAL"),
        ("constants", "CONST"),
        ("constants-dot", None),
        ("constant-decimals", "CONST"),
        ("error", "ERROR")
    ]

    def __init__(self, debug=False):
        self.fa = AutomataWithOutput(self.moves, self.error_moves, "start")
        self.debug = debug
        self.results = []

    def single_move(self, char):
        return self.fa.move(char)

    def move(self, string):
        self.fa.state = "start"
        res = []
        part = ""
        string += "\0"
        for i in string:
            part += i
            output = self.single_move(i)
            if self.debug:
                print("{} {} {}".format(i, self.fa.state, output))
            if output != None:
                res.append((part[:-1].strip(), output))
                part = i.strip()
        return res


if __name__ == "__main__":
    l = Lexer(debug=False)
    inp = "".join(sys.stdin.readlines())
    results = l.move(inp)
    for result in results:
        print("{}\t{}".format(result[1], result[0]))
