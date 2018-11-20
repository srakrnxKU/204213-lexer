"""
Lexer programme for Theory of Computation course,
Sirakorn Lamyai (5910500023)
Department of Computer Engineering, Kasetsart U.
"""


class AutomataWithOutput:
    def __init__(self, moves, start):
        self.moves = moves
        self.start = start
        self.state = start

    def move(self, inp):
        move = [i for i in self.moves if i[0] == self.state and inp in i[1]]
        if len(move) == 0:
            self.state = self.start
            return False
        self.state = move[0][2]
        return move[0][3]


class Lexer:
    numerics = list("0123456789")
    characters = list("qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM")
    operators = list("+-*/=()")
    dot = ["."]
    whitespaces = [" ", "\n", "\r", "\t"]
    terminator = ["\0"]

    moves = [
        ("start", terminator, "sterminated", None),
        ("start", operators, "literals", None),
        ("start", whitespaces, "start", None),
        ("literals", operators, "literals", "LITERAL"),
        ("literals", terminator, "terminated", "LITERAL"),
        ("literals", whitespaces, "start", "LITERAL"),
        ("start", characters, "identifiers", None),
        ("identifiers", characters, "identifiers", None),
        ("identifiers", numerics, "identifiers", None),
        ("identifiers", operators, "literals", "IDEN"),
        ("literals", characters, "identifiers", "LITERAL"),
        ("identifiers", terminator, "terminated", "IDEN"),
        ("identifiers", whitespaces, "start", "IDEN"),
    ]

    def __init__(self):
        self.fa = AutomataWithOutput(self.moves, "start")
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
            if output != None:
                res.append((part[:-1].strip(), output))
                part = i.strip()
        return res
